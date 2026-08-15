"""
============================================================
MOONSIDE IDX ENGINE (single-file version)
============================================================
Pengawas otomatis: baca watchlist saham dari jurnal harian, cocokkan dengan
pengumuman terbaru dari IDX, kirim notifikasi cuma untuk yang match ke
channel Telegram privat. Di luar watchlist = diabaikan total.

Semua logic ada di 1 file ini (config, scraper IDX, koneksi Google Sheets,
notifier Telegram, orkestrasi) supaya gampang di-develop lewat GitHub web
tanpa perlu mikirin struktur folder/import antar file.

Cara jalan:
    python engine.py                 -> jalan normal (baca watchlist, cek
                                         pengumuman baru, kirim notif)
    python engine.py --debug-raw     -> cuma ambil raw data dari IDX, print,
                                         tanpa kirim notif (buat debug kalau
                                         field mapping berubah)

Struktur file (cari komentar "==== BAGIAN: ... ====" untuk lompat ke bagian
yang mau diedit):
    1. CONFIG               - semua setting & environment variable
    2. SCRAPER IDX           - ambil pengumuman dari idx.co.id (Playwright)
    3. GOOGLE SHEETS         - baca watchlist, baca/tulis log dedup
    4. TELEGRAM NOTIFIER     - kirim pesan ke channel
    5. MAIN                  - orkestrasi alur end-to-end
============================================================
"""

import os
import sys
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests
import gspread
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright


# ============================================================
# ==== BAGIAN: 1. CONFIG ====
# Semua nilai sensitif diambil dari environment variable (GitHub Secrets
# saat jalan di GitHub Actions). JANGAN hardcode token/credential di sini.
# ============================================================

def env_or(name: str, default: str) -> str:
    """
    Seperti os.environ.get(name, default), TAPI juga pakai default kalau
    env var ADA tapi isinya string kosong "".

    Ini penting khusus untuk env var yang datang dari GitHub Secrets: kalau
    sebuah Secret belum pernah diisi di repo, GitHub Actions tetap mengoper
    env var itu ke proses (karena sudah dideklarasikan di ***env:*** pada
    engine.yml), tapi isinya "" -- bukan "tidak ada". os.environ.get biasa
    tidak akan fallback ke default dalam kasus ini, jadi butuh helper ini.
    """
    val = os.environ.get(name)
    return val if val else default


class Config:
    # --- Google Sheets ---
    SHEET_ID = env_or(
        "MOONSIDE_SHEET_ID",
        "1YjTmrg7mZgIIVUg8jf4MZ7vvv_X6KJGlGnBqgUyg-zs",
    )
    WATCHLIST_TAB_NAME = env_or("WATCHLIST_TAB_NAME", "📋 Master Tracking (PLAN A)")
    WATCHLIST_COLUMN_NAME = env_or("WATCHLIST_COLUMN_NAME", "Ticker")
    # Baris di mana header kolom (No, Plan, Sektor, Ticker, ...) berada di
    # tab watchlist. Di "Master Tracking (PLAN A)" ada 4 baris judul/catatan
    # sebelum header asli, jadi header ada di baris ke-5 (bukan baris 1).
    WATCHLIST_HEADER_ROW = int(env_or("WATCHLIST_HEADER_ROW", "5"))
    SENT_LOG_TAB_NAME = env_or("SENT_LOG_TAB_NAME", "Engine_Sent_Log")
    GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHANNEL_ID = env_or("TELEGRAM_CHANNEL_ID", "-1004318390858")

    # --- IDX ---
    # Halaman ini SSR (Nuxt) -- data pengumuman tertanam di window.__NUXT__,
    # bukan lewat endpoint JSON terpisah. Makanya dibaca pakai Playwright.
    IDX_ANNOUNCEMENT_URL = env_or(
        "IDX_ANNOUNCEMENT_URL",
        "https://www.idx.co.id/id/berita/pengumuman/",
    )
    # Berapa halaman (10 pengumuman/halaman, semua emiten) yang dicoba
    # dibaca tiap run. Naikkan kalau ada pengumuman yang kelewat.
    IDX_PAGES_TO_FETCH = int(env_or("IDX_PAGES_TO_FETCH", "3"))
    # Buffer aman: skip pengumuman yang lebih tua dari N hari.
    LOOKBACK_DAYS = int(env_or("LOOKBACK_DAYS", "2"))

    @classmethod
    def validate(cls):
        missing = []
        if not cls.GOOGLE_SERVICE_ACCOUNT_JSON:
            missing.append("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not cls.TELEGRAM_BOT_TOKEN:
            missing.append("TELEGRAM_BOT_TOKEN")
        if missing:
            raise RuntimeError(
                f"Environment variable belum diset: {', '.join(missing)}. "
                "Cek README.md bagian setup / GitHub Secrets."
            )


# ============================================================
# ==== BAGIAN: 2. SCRAPER IDX ====
# Baca window.__NUXT__ dari halaman pengumuman IDX pakai browser headless.
#
# CATATAN ASUMSI (belum 100% terverifikasi, cek kalau hasil aneh/kosong):
# 1. FIELD_MAP diambil dari 1 contoh HTML yang sudah dicek manual -- kalau
#    IDX ubah struktur datanya, field ini bisa basi.
# 2. Cara pindah halaman diduga lewat query param ?page=N -- kalau ternyata
#    tidak mengubah data, kode di bawah otomatis berhenti mengambil halaman
#    berikutnya (deteksi id item pertama sama dengan halaman sebelumnya).
# ============================================================

WIB = ZoneInfo("Asia/Jakarta")

IDX_FIELD_MAP = {
    "id": "Id",
    "kode_saham": "Code",
    "judul": "Title",
    "tanggal": "PublishDate",
    "attachments": "Attachments",
}


def _extract_nuxt_state(page) -> dict:
    """Ambil window.__NUXT__ setelah halaman selesai di-render browser."""
    state = page.evaluate("() => window.__NUXT__")
    if not state:
        raise RuntimeError(
            "window.__NUXT__ tidak ditemukan di halaman -- struktur situs "
            "mungkin sudah berubah."
        )
    return state


def _find_announcement_list(nuxt_state: dict) -> list:
    """
    Cari list pengumuman di dalam nuxt_state['fetch'][...]['announcement'].
    Key persis di dalam 'fetch' bisa berubah, jadi dicari secara generik:
    entry manapun di 'fetch' yang punya key 'announcement' berisi list.
    """
    fetch_block = nuxt_state.get("fetch") or {}
    for _, entry in fetch_block.items():
        if isinstance(entry, dict) and isinstance(entry.get("announcement"), list):
            return entry["announcement"]

    raise RuntimeError(
        "Tidak ketemu list 'announcement' di dalam window.__NUXT__.fetch. "
        "Kemungkinan struktur halaman IDX sudah berubah -- jalankan "
        "'python engine.py --debug-raw' dan cek struktur window.__NUXT__ "
        "secara manual."
    )


def fetch_raw_announcements() -> list:
    """
    Buka halaman pengumuman IDX pakai browser headless, kumpulkan pengumuman
    dari beberapa halaman (Config.IDX_PAGES_TO_FETCH), kembalikan list raw
    dict (field asli IDX, belum dinormalisasi).
    """
    all_items = []
    seen_ids = set()
    first_id_prev_page = None

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            )
        )

        try:
            for page_num in range(1, Config.IDX_PAGES_TO_FETCH + 1):
                url = Config.IDX_ANNOUNCEMENT_URL
                if page_num > 1:
                    sep = "&" if "?" in url else "?"
                    url = f"{url}{sep}page={page_num}"

                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    # Tunggu window.__NUXT__ benar-benar terisi, bukan cuma
                    # nunggu network "idle" -- situs modern sering punya
                    # polling/analytics background yang bikin networkidle
                    # tidak pernah tercapai walau konten utama sudah render.
                    page.wait_for_function(
                        "() => window.__NUXT__ !== undefined && window.__NUXT__ !== null",
                        timeout=20000,
                    )
                except Exception as e:
                    # Diagnostik: ambil sedikit isi halaman biar kelihatan
                    # apakah ini render lambat biasa atau halaman diblokir
                    # (misal Cloudflare challenge / captcha / IP diblokir).
                    try:
                        title = page.title()
                        snippet = page.content()[:300]
                    except Exception:
                        title, snippet = "(gagal ambil title)", "(gagal ambil isi halaman)"
                    print(f"[DEBUG] Gagal load halaman IDX. Title: {title!r}")
                    print(f"[DEBUG] Cuplikan HTML (300 char pertama): {snippet!r}")
                    raise

                nuxt_state = _extract_nuxt_state(page)
                items = _find_announcement_list(nuxt_state)

                if not items:
                    break

                first_id_this_page = items[0].get(IDX_FIELD_MAP["id"])
                if page_num > 1 and first_id_this_page == first_id_prev_page:
                    # ?page=N sepertinya tidak mengubah data -- berhenti
                    # daripada ambil duplikat terus.
                    break
                first_id_prev_page = first_id_this_page

                for item in items:
                    item_id = item.get(IDX_FIELD_MAP["id"])
                    if item_id and item_id not in seen_ids:
                        seen_ids.add(item_id)
                        all_items.append(item)
        finally:
            browser.close()

    return all_items


def get_recent_announcements() -> list:
    """Ambil pengumuman, normalisasi field, filter yang terlalu lama."""
    raw_items = fetch_raw_announcements()
    cutoff = datetime.now(WIB) - timedelta(days=Config.LOOKBACK_DAYS)

    normalized = []
    for item in raw_items:
        ann_id = item.get(IDX_FIELD_MAP["id"])
        kode = item.get(IDX_FIELD_MAP["kode_saham"])
        judul = item.get(IDX_FIELD_MAP["judul"])
        tanggal_raw = item.get(IDX_FIELD_MAP["tanggal"])
        attachments = item.get(IDX_FIELD_MAP["attachments"]) or []

        if not (ann_id and kode and judul):
            continue  # data gak lengkap, skip daripada kirim notif ngaco

        publish_dt = None
        if tanggal_raw:
            try:
                publish_dt = datetime.fromisoformat(tanggal_raw).replace(tzinfo=WIB)
            except ValueError:
                publish_dt = None

        if publish_dt and publish_dt < cutoff:
            continue

        main_attachment = None
        for att in attachments:
            if att.get("IsAttachment") is False:
                main_attachment = att.get("FullSavePath")
                break
        if not main_attachment and attachments:
            main_attachment = attachments[0].get("FullSavePath")

        normalized.append(
            {
                "id": str(ann_id),
                "kode_saham": str(kode).strip().upper(),
                "judul": str(judul).strip(),
                "tanggal_raw": tanggal_raw,
                "attachment": main_attachment,
            }
        )

    return normalized


# ============================================================
# ==== BAGIAN: 3. GOOGLE SHEETS ====
# Baca watchlist saham dari jurnal, baca/tulis log pengumuman yang sudah
# dikirim (buat dedup).
# ============================================================

SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _get_sheets_client():
    if not Config.GOOGLE_SERVICE_ACCOUNT_JSON:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON kosong.")
    info = json.loads(Config.GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = Credentials.from_service_account_info(info, scopes=SHEETS_SCOPES)
    return gspread.authorize(creds)


def get_watchlist() -> list:
    """Ambil daftar kode saham dari tab jurnal, kolom yang dikonfigurasi."""
    client = _get_sheets_client()
    sheet = client.open_by_key(Config.SHEET_ID)
    ws = sheet.worksheet(Config.WATCHLIST_TAB_NAME)
    records = ws.get_all_records(head=Config.WATCHLIST_HEADER_ROW)

    col = Config.WATCHLIST_COLUMN_NAME
    codes = set()
    for row in records:
        val = str(row.get(col, "")).strip().upper()
        if val:
            codes.add(val)
    return sorted(codes)


def _get_or_create_log_sheet(client):
    sheet = client.open_by_key(Config.SHEET_ID)
    try:
        return sheet.worksheet(Config.SENT_LOG_TAB_NAME)
    except gspread.exceptions.WorksheetNotFound:
        ws = sheet.add_worksheet(title=Config.SENT_LOG_TAB_NAME, rows=1000, cols=5)
        ws.append_row(["announcement_id", "kode_saham", "judul", "tanggal_kirim"])
        return ws


def get_sent_ids() -> set:
    client = _get_sheets_client()
    ws = _get_or_create_log_sheet(client)
    values = ws.col_values(1)[1:]  # skip header
    return set(values)


def log_sent(announcement_id: str, kode_saham: str, judul: str, timestamp: str):
    client = _get_sheets_client()
    ws = _get_or_create_log_sheet(client)
    ws.append_row([announcement_id, kode_saham, judul, timestamp])


# ============================================================
# ==== BAGIAN: 4. TELEGRAM NOTIFIER ====
# Kirim notifikasi ke channel Telegram MOONSIDE Engine.
# ============================================================

def send_announcement_alert(kode_saham: str, judul: str, tanggal: str, attachment_url):
    text = (
        f"🛰️ *MOONSIDE Engine*\n\n"
        f"📌 *{kode_saham}*\n"
        f"{judul}\n\n"
        f"🕒 {tanggal}\n"
    )
    if attachment_url:
        text += f"[Lampiran]({attachment_url})"

    url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": Config.TELEGRAM_CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    resp = requests.post(url, json=payload, timeout=15)
    if not resp.ok:
        print(f"[WARN] Gagal kirim notif untuk {kode_saham}: {resp.text}")
    return resp.ok


# ============================================================
# ==== BAGIAN: 5. MAIN ====
# Orkestrasi alur end-to-end:
# 1. Baca watchlist dari Google Sheet
# 2. Ambil pengumuman terbaru dari IDX
# 3. Filter sesuai watchlist
# 4. Dedup (skip yang sudah pernah dikirim)
# 5. Kirim ke Telegram & catat log
# ============================================================

def run(debug_raw: bool = False):
    Config.validate()

    if debug_raw:
        raw = fetch_raw_announcements()
        print(f"Dapat {len(raw)} raw item. Contoh item pertama:")
        print(raw[0] if raw else "(kosong)")
        return

    print("[1/5] Baca watchlist dari Google Sheet...")
    watchlist = set(get_watchlist())
    print(f"      -> {len(watchlist)} saham di watchlist: {sorted(watchlist)}")

    if not watchlist:
        print("[STOP] Watchlist kosong. Cek WATCHLIST_TAB_NAME / WATCHLIST_COLUMN_NAME.")
        return

    print("[2/5] Ambil pengumuman terbaru dari IDX (Playwright)...")
    announcements = get_recent_announcements()
    print(f"      -> {len(announcements)} pengumuman ditemukan (semua emiten)")

    print("[3/5] Filter sesuai watchlist...")
    matched = [a for a in announcements if a["kode_saham"] in watchlist]
    print(f"      -> {len(matched)} match dengan watchlist kamu")

    print("[4/5] Cek dedup (yang sudah pernah dikirim)...")
    sent_ids = get_sent_ids()
    new_items = [a for a in matched if a["id"] not in sent_ids]
    print(f"      -> {len(new_items)} pengumuman BARU (belum pernah dikirim)")

    print("[5/5] Kirim notifikasi & catat log...")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for item in new_items:
        ok = send_announcement_alert(
            kode_saham=item["kode_saham"],
            judul=item["judul"],
            tanggal=item["tanggal_raw"] or now_str,
            attachment_url=item["attachment"],
        )
        if ok:
            log_sent(item["id"], item["kode_saham"], item["judul"], now_str)
            print(f"      -> Terkirim: {item['kode_saham']} - {item['judul'][:50]}")

    print("Selesai.")


if __name__ == "__main__":
    debug = "--debug-raw" in sys.argv
    run(debug_raw=debug)
