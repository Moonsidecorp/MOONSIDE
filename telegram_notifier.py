"""Kirim notifikasi ke channel Telegram MOONSIDE Engine."""

import requests
from .config import Config


def send_announcement_alert(kode_saham: str, judul: str, tanggal: str, attachment_url: str | None):
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
