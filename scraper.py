"""
Scraper pengumuman IDX.

CATATAN PENTING: halaman /id/berita/pengumuman/ adalah Nuxt SSR (server-side
rendered) -- semua data pengumuman (untuk page yang sedang dibuka) sudah
tertanam langsung di HTML awal, di dalam blok:

    <script>window.__NUXT__ = (function(a, b, c, ...) { ... })(...)</script>

Ini BUKAN endpoint JSON terpisah yang bisa di-hit langsung pakai requests/
cloudscraper -- makanya sebelumnya tidak ketemu request Fetch/XHR apapun yang
membawa data pengumuman di DevTools. Untuk membacanya, kita jalankan browser
headless (Playwright) yang benar-benar merender halaman itu (termasuk
menjalankan JavaScript-nya sampai `window.__NUXT__` jadi object biasa), baru
kita ambil isinya lewat `page.evaluate()`.

ASUMSI YANG BELUM 100% TERVERIFIKASI (tolong konfirmasi kalau ternyata beda):
1. Field mapping di FIELD_MAP di bawah diambil dari satu contoh HTML yang
   sudah dicek manual. Kalau IDX ubah struktur datanya, field ini bisa basi.
2. Cara pindah halaman (page 2, 3, dst) DIDUGA lewat query param
   `?page=N` pada URL yang sama, TAPI ini belum diverifikasi karena
   perubahan halaman waktu itu tidak tercatat sebagai request terpisah di
   DevTools (kemungkinan client-side routing Nuxt). Kalau ternyata query
   param ini tidak mengubah data, fungsi di bawah otomatis mendeteksinya
   (item pertama sama dengan halaman sebelumnya) dan berhenti mengambil
   halaman berikutnya -- jadi worst case, engine tetap jalan tapi cuma
   dapat page 1 (10 pengumuman terbaru dari SEMUA emiten).

Kalau field mapping meleset, jalankan `python -m engine.main --debug-raw`
dan kirim contoh output-nya untuk disesuaikan mappingnya.
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

from .config import Config

WIB = ZoneInfo("Asia/Jakarta")

# Nama field asli di object announcement dari window.__NUXT__ (hasil cek
# manual terhadap satu contoh HTML halaman pengumuman).
FIELD_MAP = {
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
        raise RuntimeError("window.__NUXT__ tidak ditemukan di halaman -- struktur situs mungkin sudah berubah.")
    return state


def _find_announcement_list(nuxt_state: dict) -> list[dict]:
    """
    Cari list pengumuman di dalam nuxt_state['fetch'][...]['announcement'].
    Key persis di dalam 'fetch' (mis. 'data-v-340bfe62:0') bisa berubah kalau
    IDX update komponennya, jadi di sini kita cari secara generik: entry
    manapun di dalam 'fetch' yang punya key 'announcement' berisi list.
    """
    fetch_block = nuxt_state.get("fetch") or {}
    for _, entry in fetch_block.items():
        if isinstance(entry, dict) and isinstance(entry.get("announcement"), list):
            return entry["announcement"]

    raise RuntimeError(
        "Tidak ketemu list 'announcement' di dalam window.__NUXT__.fetch. "
        "Kemungkinan struktur halaman IDX sudah berubah -- jalankan --debug-raw "
        "dan cek struktur window.__NUXT__ secara manual."
    )


def fetch_raw_announcements() -> list[dict]:
    """
    Buka halaman pengumuman IDX pakai browser headless, kumpulkan pengumuman
    dari beberapa halaman (Config.IDX_PAGES_TO_FETCH), kembalikan list raw
    dict (field asli IDX, belum dinormalisasi).
    """
    all_items: list[dict] = []
    seen_ids: set[str] = set()
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

                page.goto(url, wait_until="networkidle", timeout=30000)
                nuxt_state = _extract_nuxt_state(page)
                items = _find_announcement_list(nuxt_state)

                if not items:
                    break

                first_id_this_page = items[0].get(FIELD_MAP["id"])
                if page_num > 1 and first_id_this_page == first_id_prev_page:
                    # Query param ?page=N sepertinya tidak mengubah data --
                    # berhenti di sini daripada mengambil duplikat terus.
                    break
                first_id_prev_page = first_id_this_page

                for item in items:
                    item_id = item.get(FIELD_MAP["id"])
                    if item_id and item_id not in seen_ids:
                        seen_ids.add(item_id)
                        all_items.append(item)
        finally:
            browser.close()

    return all_items


def get_recent_announcements() -> list[dict]:
    """Ambil pengumuman, normalisasi field, filter yang terlalu lama."""
    raw_items = fetch_raw_announcements()
    cutoff = datetime.now(WIB) - timedelta(days=Config.LOOKBACK_DAYS)

    normalized = []
    for item in raw_items:
        ann_id = item.get(FIELD_MAP["id"])
        kode = item.get(FIELD_MAP["kode_saham"])
        judul = item.get(FIELD_MAP["judul"])
        tanggal_raw = item.get(FIELD_MAP["tanggal"])
        attachments = item.get(FIELD_MAP["attachments"]) or []

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

        # Pilih attachment "utama": yang IsAttachment == False (dokumen
        # pokok), kalau tidak ada ambil yang pertama sebagai fallback.
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
