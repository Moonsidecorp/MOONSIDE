/**
 * MOONSIDE Engine - Subscription & Access Control
 * ---------------------------------------------------
 * Ditambahkan ke project GAS bot MOONSIDE yang SUDAH ADA (bukan project baru).
 * Menangani: generate kode akses otomatis saat admin konfirmasi pembayaran,
 * redeem kode oleh member, invite ke channel privat, cek expiry harian.
 *
 * SETUP SEBELUM DIPAKAI:
 * 1. File > Project properties > Script properties, tambahkan:
 *    - BOT_TOKEN         : token bot Telegram MOONSIDE (JANGAN hardcode di sini)
 *    - ADMIN_CHAT_ID      : 5695908098  (chat_id kamu / admin)
 *    - CHANNEL_ID         : -1004318390858
 *    - SUBSCRIPTIONS_SHEET_ID : ID sheet jurnal kamu (sama dgn Engine)
 * 2. Sheet perlu tab baru bernama "Subscriptions" dengan header:
 *    kode | status | telegram_user_id | telegram_username | tanggal_generate |
 *    tanggal_redeem | tanggal_expired | catatan_admin
 * 3. Bot HARUS dijadikan admin di channel -1004318390858 dengan izin
 *    "Invite Users via Link" supaya bisa generate invite link sekali pakai.
 */

const PROPS = PropertiesService.getScriptProperties();
const BOT_TOKEN = PROPS.getProperty('BOT_TOKEN');
const ADMIN_CHAT_ID = PROPS.getProperty('ADMIN_CHAT_ID');
const CHANNEL_ID = PROPS.getProperty('CHANNEL_ID');
const SHEET_ID = PROPS.getProperty('SUBSCRIPTIONS_SHEET_ID');
const SUB_TAB_NAME = 'Subscriptions';
const SUBSCRIPTION_DAYS = 365;
const HARGA_LANGGANAN = 'Rp650.000 / tahun';

function getSubSheet_() {
  const ss = SpreadsheetApp.openById(SHEET_ID);
  let sheet = ss.getSheetByName(SUB_TAB_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SUB_TAB_NAME);
    sheet.appendRow([
      'kode', 'status', 'telegram_user_id', 'telegram_username',
      'tanggal_generate', 'tanggal_redeem', 'tanggal_expired', 'catatan_admin'
    ]);
  }
  return sheet;
}

function generateCode_() {
  // Format: MOONSIDE-XXXXXX (6 karakter acak alfanumerik uppercase)
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // tanpa 0/O/1/I biar gak ambigu
  let code = '';
  for (let i = 0; i < 6; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return `MOONSIDE-${code}`;
}

/**
 * Dipanggil admin setelah verifikasi pembayaran manual (QR/transfer BNI).
 * Contoh trigger: command bot "/konfirmasi <catatan opsional>" dari ADMIN_CHAT_ID.
 * Menghasilkan kode unik baru dan mengirimkannya ke admin untuk diteruskan
 * ke member (via WA/DM, sesuai alur kamu).
 */
function konfirmasiPembayaran(catatanAdmin) {
  const sheet = getSubSheet_();
  const kode = generateCode_();
  const now = new Date();

  sheet.appendRow([
    kode, 'belum_redeem', '', '',
    Utilities.formatDate(now, 'GMT+7', 'yyyy-MM-dd HH:mm:ss'),
    '', '', catanAdminSafe_(catatanAdmin)
  ]);

  sendTelegramMessage_(ADMIN_CHAT_ID,
    `✅ Kode akses baru dibuat:\n\n\`${kode}\`\n\n` +
    `Tarif: ${HARGA_LANGGANAN}\n` +
    `Kirim kode ini ke member. Kode berlaku 1x pakai, dan aktif selama ` +
    `${SUBSCRIPTION_DAYS} hari sejak di-redeem.`
  );

  return kode;
}

function catanAdminSafe_(catatan) {
  return catatan || '-';
}

/**
 * Dipanggil dari webhook handler utama bot kamu saat ada pesan masuk.
 * Cek apakah teks pesan match format kode (MOONSIDE-XXXXXX).
 * Kalau ya, proses redeem.
 */
function tryRedeemFromMessage(update) {
  const message = update.message;
  if (!message || !message.text) return false;

  const text = message.text.trim().toUpperCase();
  if (!text.match(/^MOONSIDE-[A-Z0-9]{6}$/)) return false;

  const chatId = message.chat.id;
  const username = message.from.username || '(tanpa username)';

  const sheet = getSubSheet_();
  const data = sheet.getDataRange().getValues();

  for (let row = 1; row < data.length; row++) {
    const [kode, status] = data[row];
    if (kode === text) {
      if (status === 'aktif') {
        sendTelegramMessage_(chatId, '⚠️ Kode ini sudah pernah dipakai sebelumnya.');
        return true;
      }
      if (status !== 'belum_redeem') {
        sendTelegramMessage_(chatId, '❌ Kode tidak valid atau sudah kadaluarsa.');
        return true;
      }

      // Valid, proses redeem
      const now = new Date();
      const expiry = new Date(now.getTime() + SUBSCRIPTION_DAYS * 24 * 60 * 60 * 1000);

      sheet.getRange(row + 1, 2).setValue('aktif');                    // status
      sheet.getRange(row + 1, 3).setValue(chatId);                     // telegram_user_id
      sheet.getRange(row + 1, 4).setValue(username);                   // telegram_username
      sheet.getRange(row + 1, 6).setValue(
        Utilities.formatDate(now, 'GMT+7', 'yyyy-MM-dd HH:mm:ss'));    // tanggal_redeem
      sheet.getRange(row + 1, 7).setValue(
        Utilities.formatDate(expiry, 'GMT+7', 'yyyy-MM-dd'));          // tanggal_expired

      const inviteLink = createOneTimeInviteLink_();
      sendTelegramMessage_(chatId,
        `🎉 Kode valid! Akses MOONSIDE Engine aktif sampai ` +
        `${Utilities.formatDate(expiry, 'GMT+7', 'dd MMM yyyy')}.\n\n` +
        `Join channel di sini (link sekali pakai, jangan disebar):\n${inviteLink}`
      );
      sendTelegramMessage_(ADMIN_CHAT_ID,
        `ℹ️ Kode ${text} berhasil di-redeem oleh @${username} (${chatId}).`
      );
      return true;
    }
  }

  sendTelegramMessage_(chatId, '❌ Kode tidak ditemukan. Pastikan penulisan benar.');
  return true;
}

function createOneTimeInviteLink_() {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/createChatInviteLink`;
  const payload = {
    chat_id: CHANNEL_ID,
    member_limit: 1,
    creates_join_request: false
  };
  const resp = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
  const json = JSON.parse(resp.getContentText());
  if (!json.ok) {
    throw new Error('Gagal buat invite link: ' + resp.getContentText());
  }
  return json.result.invite_link;
}

/**
 * Jalankan via time-based trigger (harian, misal jam 08:00 WIB).
 * - H-7 sebelum expired: kirim reminder perpanjangan
 * - Sudah expired: kick dari channel, update status
 */
function checkExpiringSubscriptions() {
  const sheet = getSubSheet_();
  const data = sheet.getDataRange().getValues();
  const today = new Date();

  for (let row = 1; row < data.length; row++) {
    const [kode, status, userId, username, , , expiredStr] = data[row];
    if (status !== 'aktif' || !expiredStr) continue;

    const expiredDate = new Date(expiredStr);
    const daysLeft = Math.ceil((expiredDate - today) / (1000 * 60 * 60 * 24));

    if (daysLeft === 7) {
      sendTelegramMessage_(userId,
        `⏰ Langganan MOONSIDE Engine kamu akan berakhir dalam 7 hari ` +
        `(${expiredStr}). Perpanjang sekarang (${HARGA_LANGGANAN}) biar nggak ` +
        `ketinggalan info penting.`
      );
    } else if (daysLeft < 0) {
      kickFromChannel_(userId);
      sheet.getRange(row + 1, 2).setValue('expired');
      sendTelegramMessage_(userId,
        `🔒 Langganan MOONSIDE Engine kamu sudah berakhir. Kamu dikeluarkan ` +
        `dari channel. Hubungi admin untuk perpanjang.`
      );
    }
  }
}

function kickFromChannel_(userId) {
  const banUrl = `https://api.telegram.org/bot${BOT_TOKEN}/banChatMember`;
  UrlFetchApp.fetch(banUrl, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ chat_id: CHANNEL_ID, user_id: userId }),
    muteHttpExceptions: true
  });
  // Unban langsung supaya user bisa join lagi di masa depan kalau perpanjang
  const unbanUrl = `https://api.telegram.org/bot${BOT_TOKEN}/unbanChatMember`;
  UrlFetchApp.fetch(unbanUrl, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ chat_id: CHANNEL_ID, user_id: userId, only_if_banned: true }),
    muteHttpExceptions: true
  });
}

function sendTelegramMessage_(chatId, text) {
  const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
  UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify({ chat_id: chatId, text: text, parse_mode: 'Markdown' }),
    muteHttpExceptions: true
  });
}
