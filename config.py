"""
Konfigurasi MOONSIDE Engine.
SEMUA nilai sensitif diambil dari environment variables (GitHub Secrets saat
jalan di GitHub Actions). Jangan pernah hardcode token/credential di sini.
"""

import os


class Config:
    # --- Google Sheets ---
    # Sheet ID diambil dari URL:
    # https://docs.google.com/spreadsheets/d/<INI_SHEET_ID>/edit
    SHEET_ID = os.environ.get(
        "MOONSIDE_SHEET_ID",
        "1YjTmrg7mZgIIVUg8jf4MZ7vvv_X6KJGlGnBqgUyg-zs",  # sheet jurnal kamu
    )

    # Nama tab (worksheet) tempat watchlist 60 saham disimpan.
    # GANTI sesuai nama tab asli di sheet kamu.
    WATCHLIST_TAB_NAME = os.environ.get("WATCHLIST_TAB_NAME", "Journal")

    # Nama kolom (header row) yang berisi kode saham, misal "Kode Saham" / "Ticker".
    WATCHLIST_COLUMN_NAME = os.environ.get("WATCHLIST_COLUMN_NAME", "Kode Saham")

    # Tab buat nyimpen histori pengumuman yang SUDAH dikirim (dedup).
    # Kalau belum ada, script akan buat otomatis.
    SENT_LOG_TAB_NAME = os.environ.get("SENT_LOG_TAB_NAME", "Engine_Sent_Log")

    # Isi JSON credential service account (ditaruh sebagai secret string, bukan file)
    GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    # Channel privat MOONSIDE Engine Alerts (format -100xxxxxxxxxx)
    TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "-1004318390858")

    # --- IDX ---
    # CATATAN PENTING (update dari investigasi DevTools):
    # Halaman /id/berita/pengumuman/ TERNYATA server-side rendered (Nuxt SSR) --
    # datanya tertanam langsung di dalam <script>window.__NUXT__ = ...</script>
    # pada HTML awal, BUKAN lewat endpoint JSON terpisah yang bisa di-hit
    # langsung. Makanya scraper sekarang pakai Playwright (browser headless)
    # untuk membuka halaman itu, menjalankan JS-nya, lalu membaca
    # window.__NUXT__ setelah halaman selesai render.
    IDX_ANNOUNCEMENT_URL = os.environ.get(
        "IDX_ANNOUNCEMENT_URL",
        "https://www.idx.co.id/id/berita/pengumuman/",
    )

    # Berapa halaman (page 1, 2, 3, ...) yang dicoba dibaca tiap run. Tiap
    # halaman berisi 10 pengumuman terbaru (dari SEMUA emiten, belum difilter
    # watchlist). Dengan jadwal tiap 15 menit, 3 halaman (30 pengumuman)
    # dianggap buffer aman. Naikkan kalau ternyata masih ada yang kelewat
    # (cek log "X pengumuman ditemukan" -- kalau sering pas 30 x 3, kemungkinan
    # ada yang kepotong, naikkan angka ini).
    IDX_PAGES_TO_FETCH = int(os.environ.get("IDX_PAGES_TO_FETCH", "3"))

    # Berapa hari ke belakang yang mau dicek tiap run (buffer aman, filter
    # sekunder setelah pengambilan halaman di atas)
    LOOKBACK_DAYS = int(os.environ.get("LOOKBACK_DAYS", "2"))

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
                "Cek README.md bagian setup."
            )
