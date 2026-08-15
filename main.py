"""
MOONSIDE Engine - entry point.

Alur:
1. Baca watchlist saham dari Google Sheet jurnal
2. Ambil pengumuman terbaru dari IDX (via Playwright, baca window.__NUXT__)
3. Filter: hanya kode saham yang ada di watchlist
4. Dedup: skip yang udah pernah dikirim (dicatat di tab Engine_Sent_Log)
5. Kirim ke channel Telegram
6. Catat sebagai "sudah dikirim"
"""

import sys
from datetime import datetime

from .config import Config
from .scraper import get_recent_announcements
from .telegram_notifier import send_announcement_alert
from . import sheets


def run(debug_raw: bool = False):
    Config.validate()

    if debug_raw:
        from .scraper import fetch_raw_announcements
        raw = fetch_raw_announcements()
        print(f"Dapat {len(raw)} raw item. Contoh item pertama:")
        print(raw[0] if raw else "(kosong)")
        return

    print("[1/5] Baca watchlist dari Google Sheet...")
    watchlist = set(sheets.get_watchlist())
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
    sent_ids = sheets.get_sent_ids()
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
            sheets.log_sent(item["id"], item["kode_saham"], item["judul"], now_str)
            print(f"      -> Terkirim: {item['kode_saham']} - {item['judul'][:50]}")

    print("Selesai.")


if __name__ == "__main__":
    debug = "--debug-raw" in sys.argv
    run(debug_raw=debug)
