# MOONSIDE IDX Engine

Pengawas otomatis: baca watchlist saham dari jurnal harian kamu, cocokkan
dengan pengumuman terbaru dari IDX, kirim notifikasi cuma untuk yang match ke
channel Telegram privat. Di luar watchlist = diabaikan total.

Terdiri dari 2 bagian terpisah:
1. **`engine/`** — Python + GitHub Actions, scraper & notifier (repo ini)
2. **`subscriptions.gs`** — Google Apps Script, ditempel ke project GAS bot
   MOONSIDE kamu yang sudah ada, untuk kelola akses berbayar

---

## Bagian 1: Setup Engine (scraper)

### Checklist sebelum jalan

- [ ] Buat Service Account Google Cloud, download JSON key
- [ ] Share Google Sheet jurnal ke email service account (read/write)
- [ ] Isi GitHub Secrets di repo ini
- [ ] Bot Telegram MOONSIDE sudah jadi **admin** di channel target
- [ ] Test manual via `workflow_dispatch` sebelum lepas ke cron otomatis

### 1. Cara kerja scraper (PENTING dibaca dulu)

Halaman `https://www.idx.co.id/id/berita/pengumuman/` ternyata **server-side
rendered (Nuxt SSR)** — semua data pengumuman sudah tertanam langsung di HTML
awal (`window.__NUXT__`), BUKAN lewat endpoint JSON terpisah yang bisa
di-hit langsung. Karena itu scraper sekarang pakai **Playwright** (browser
headless): buka halamannya sungguhan, biarkan JavaScript-nya jalan, baru baca
`window.__NUXT__` setelah render selesai. Ini juga otomatis bypass Cloudflare
karena memang browser asli, bukan pura-pura seperti request biasa.

Field mapping (`FIELD_MAP` di `engine/scraper.py`) diambil dari satu contoh
HTML yang sudah dicek manual — `Code` (ticker), `Title` (judul), `PublishDate`
(tanggal), `Attachments` (lampiran PDF). Kalau IDX mengubah struktur datanya
di masa depan dan hasil jadi kosong/aneh, jalankan:
```
python -m engine.main --debug-raw
```
lalu kirim contoh output-nya — field mapping bisa disesuaikan lagi.

**Catatan soal jumlah halaman yang dibaca:** tiap halaman berisi 10
pengumuman terbaru dari SEMUA emiten (belum difilter watchlist). Karena
engine jalan tiap 15 menit, default-nya membaca 3 halaman (30 pengumuman)
sebagai buffer. Bisa diubah lewat `IDX_PAGES_TO_FETCH` di GitHub Secrets
kalau ternyata masih ada yang kelewat.

### 2. Service Account (akses Google Sheet)

1. https://console.cloud.google.com/ → buat project baru (atau pakai yang ada)
2. Aktifkan **Google Sheets API**
3. IAM & Admin → Service Accounts → Create → beri nama `moonside-engine`
4. Buka service account itu → Keys → Add Key → JSON → download
5. Buka Google Sheet jurnal kamu → Share → paste email service account
   (formatnya `xxx@xxx.iam.gserviceaccount.com`) → beri akses **Editor**
6. Isi seluruh isi file JSON tadi (as-is) ke GitHub Secret
   `GOOGLE_SERVICE_ACCOUNT_JSON`

### 3. GitHub Secrets yang perlu diisi

Repo → Settings → Secrets and variables → Actions:

| Secret | Isi |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | isi file JSON service account |
| `TELEGRAM_BOT_TOKEN` | token dari @BotFather |
| `TELEGRAM_CHANNEL_ID` | ID channel Telegram target |
| `MOONSIDE_SHEET_ID` | ID sheet jurnal kamu |
| `IDX_ANNOUNCEMENT_URL` | opsional, default sudah benar (`https://www.idx.co.id/id/berita/pengumuman/`) — isi hanya kalau URL-nya berubah |
| `IDX_PAGES_TO_FETCH` | opsional, default `3` |
| `WATCHLIST_TAB_NAME` / `WATCHLIST_COLUMN_NAME` | isi kalau beda dari default (`Journal` / `Kode Saham`) |

### 4. Sesuaikan nama tab/kolom watchlist

Di `engine/config.py`, cek default:
- `WATCHLIST_TAB_NAME = "Journal"` → ganti sesuai nama tab asli
- `WATCHLIST_COLUMN_NAME = "Kode Saham"` → ganti sesuai header kolom asli

(atau override via GitHub Secrets dengan nama yang sama)

### 5. Test manual

Repo → Actions → **MOONSIDE Engine** → **Run workflow** (jangan tunggu
jadwal cron). Cek log tiap step, pastikan sampai ke "Selesai." tanpa error.
Kalau step 2 (ambil pengumuman IDX) error atau dapat 0 item, jalankan
`python -m engine.main --debug-raw` secara lokal untuk debug lebih detail.

---

## Bagian 2: Setup Subscription (`subscriptions.gs`)

*(tidak ada perubahan dari sebelumnya)*

1. Buka project GAS bot MOONSIDE yang sudah ada
2. Buat file script baru, paste isi `subscriptions.gs`
3. Project Settings → Script Properties, tambahkan:
   - `BOT_TOKEN`
   - `ADMIN_CHAT_ID`
   - `CHANNEL_ID`
   - `SUBSCRIPTIONS_SHEET_ID`
4. Pastikan bot MOONSIDE jadi **admin channel** dengan izin "Invite Users via Link"
5. Hubungkan `tryRedeemFromMessage(update)` ke webhook handler utama bot kamu
   (dipanggil di awal, sebelum command lain diproses)
6. Buat time-based trigger harian untuk `checkExpiringSubscriptions()`
7. Tambahkan cara admin memicu `konfirmasiPembayaran(catatan)`

Test alur lengkap sebelum dipakai member sungguhan:
payment manual → `konfirmasiPembayaran()` → kode keluar → kirim kode dari
akun Telegram lain → cek dapat invite link → join channel → cek row di tab
`Subscriptions` ke-update dengan benar.
