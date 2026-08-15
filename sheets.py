"""
Koneksi ke Google Sheets via service account.
Baca watchlist saham dari jurnal, baca/tulis log pengumuman yang sudah dikirim.
"""

import json
import gspread
from google.oauth2.service_account import Credentials

from .config import Config

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]


def _get_client():
    if not Config.GOOGLE_SERVICE_ACCOUNT_JSON:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_JSON kosong.")
    info = json.loads(Config.GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return gspread.authorize(creds)


def get_watchlist() -> list[str]:
    """Ambil daftar kode saham dari tab jurnal, kolom yang dikonfigurasi."""
    client = _get_client()
    sheet = client.open_by_key(Config.SHEET_ID)
    ws = sheet.worksheet(Config.WATCHLIST_TAB_NAME)
    records = ws.get_all_records()  # list of dict, key = header row

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
        ws = sheet.add_worksheet(
            title=Config.SENT_LOG_TAB_NAME, rows=1000, cols=5
        )
        ws.append_row(["announcement_id", "kode_saham", "judul", "tanggal_kirim"])
        return ws


def get_sent_ids() -> set[str]:
    client = _get_client()
    ws = _get_or_create_log_sheet(client)
    values = ws.col_values(1)[1:]  # skip header
    return set(values)


def log_sent(announcement_id: str, kode_saham: str, judul: str, timestamp: str):
    client = _get_client()
    ws = _get_or_create_log_sheet(client)
    ws.append_row([announcement_id, kode_saham, judul, timestamp])
