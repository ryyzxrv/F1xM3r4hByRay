import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
from utils_premium import is_premium, add_premium, get_premium_status, OWNER_ID

# ---------------- CONFIG ----------------
TELEGRAM_TOKEN = "8266869214:AAFhzKVEaBRhIVxVKDZlwrS7u375bci_vqs"
ACCOUNTS_FILE = "accounts.json"

SUBJECT = "Questions Whatsapp for Android"

BODY_TEMPLATE = """Құрметті WhatsApp 
Жеке нөмірімді тіркеу кезінде мәселе туындады, қызыл суреті бар хабарлама болды “Login not available” ол кезде менің жеке номерім болатын.
WhatsApp бұл мәселені тез қарап, дұрыс тіркеле аламын деп үміттенемін.
менің жеке нөмірім [{phone}]
Мұның бәрі меннен [Junn] алғыс айту.
"""

def load_config():
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

CONFIG = load_config()
CURRENT_INDEX = 0


# ---------------- EMAIL SYSTEM ----------------
def choose_account():
    global CURRENT_INDEX
    accounts = CONFIG["accounts"]
    account = accounts[CURRENT_INDEX % len(accounts)]
    CURRENT_INDEX += 1
    return account


def send_email(account, subject, body, to_email):
    msg = MIMEMultipart()
    msg["From"] = account["email"]
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(account.get("smtp", "smtp.gmail.com"), account.get("port", 587))
        server.starttls()
        server.login(account["email"], account["password"])
        server.sendmail(account["email"], to_email, msg.as_string())
        server.quit()
        return (
            "✅ *Sudah berhasil terkirim!*\n"
            "⌛ Tunggu *20 detik*...\n\n"
            "Kalau berhasil, *doain yang bikin cepat kaya* 😎\n"
            "Kalau ada kendala, hubungi: [@r4nvxx](https://t.me/r4nvxx)"
        )
    except Exception as e:
        return f"❌ *Gagal mengirim!*\n\n🧾 Error: `{e}`"


# ---------------- HANDLERS ----------------
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🧩 FIX MERAH", callback_data="fix_merah")],
        [
            InlineKeyboardButton("📱 Cek Nomor", callback_data="cek_num"),
            InlineKeyboardButton("👤 Cek ID", callback_data="cek_id"),
        ],
        [InlineKeyboardButton("💬 Cek Bio", callback_data="cek_bio")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    photo_url = "https://i.imgur.com/V8uDFY9.jpeg"
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo_url,
        caption=(
            "👋 *Selamat Datang di Email Bot Fix Merah!*\n\n"
            "Gunakan tombol di bawah untuk memilih aksi:\n\n"
            "🧩 *Fix Merah* — Kirim nomor merah kamu.\n"
            "📱 *Cek Nomor* — Cek format nomor kamu.\n"
            "👤 *Cek ID* — Lihat ID Telegram kamu.\n"
            "💬 *Cek Bio* — Info tambahan.\n\n"
            "_Dibuat oleh [@r4nvxx](https://t.me/r4nvxx)_"
        ),
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    if query.data == "fix_merah":
        if not is_premium(user_id):
            query.edit_message_caption(
                caption=(
                    "🚫 *Akses Ditolak!*\n\n"
                    "Fitur 🧩 *Fix Merah* hanya untuk pengguna *Premium*.\n\n"
                    "📅 Gunakan perintah */premium* untuk melihat status kamu.\n\n"
                    "🎯 Upgrade premium untuk menikmati semua fitur!"
                ),
                parse_mode="Markdown",
            )
            return

        context.user_data["mode"] = "fix_merah"
        query.edit_message_caption(
            caption="🧩 *Kirim Nomor Merah kamu sekarang*\n\nContoh: `+628123456789`",
            parse_mode="Markdown",
        )

    elif query.data == "cek_id":
        uid = query.from_user.id
        query.edit_message_caption(
            caption=f"👤 *ID Telegram kamu:* `{uid}`", parse_mode="Markdown"
        )

    elif query.data == "cek_bio":
        query.edit_message_caption(
            caption="💬 *Bot ini dibuat untuk membantu kirim email Fix Merah secara otomatis.*\n\n📌 Dibuat oleh [@r4nvxx](https://t.me/r4nvxx)",
            parse_mode="Markdown",
        )


def handle_number(update: Update, context: CallbackContext):
    if context.user_data.get("mode") != "fix_merah":
        return

    user_id = update.message.from_user.id
    if not is_premium(user_id):
        update.message.reply_text(
            "🚫 *Fitur ini hanya untuk pengguna Premium!*\nKetik /premium untuk cek status kamu.",
            parse_mode="Markdown",
        )
        context.user_data["mode"] = None
        return

    phone_number = update.message.text.strip()
    if not phone_number.startswith("+"):
        update.message.reply_text("❗ Kirim nomor merah yang benar.\nContoh: `+628123456789`", parse_mode="Markdown")
        return

    to_email = CONFIG.get("to_email")
    account = choose_account()
    body = BODY_TEMPLATE.format(phone=phone_number)
    result = send_email(account, SUBJECT, body, to_email)
    update.message.reply_text(f"{result}\n\n📱 Nomor: `{phone_number}`", parse_mode="Markdown")
    context.user_data["mode"] = None


# ---------------- PREMIUM SYSTEM ----------------
def addprem_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if str(user_id) != str(OWNER_ID):
        update.message.reply_text("🚫 *Kamu tidak punya izin menambah premium!*", parse_mode="Markdown")
        return

    if len(context.args) < 2:
        update.message.reply_text("⚙️ Format: `/addprem @username 10d`", parse_mode="Markdown")
        return

    target = context.args[0].replace("@", "")
    days_str = context.args[1]
    if not days_str.endswith("d"):
        update.message.reply_text("❗ Gunakan format hari, contoh: `10d`", parse_mode="Markdown")
        return

    days = int(days_str[:-1])
    expire = add_premium(target, days)
    exp_str = datetime.fromtimestamp(expire).strftime("%d-%m-%Y %H:%M")

    update.message.reply_text(
        f"✅ *Berhasil menambah premium*\n👤 User: `{target}`\n🕓 Durasi: *{days} hari*\n📅 Exp: `{exp_str}`",
        parse_mode="Markdown",
    )


def premium_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    status = get_premium_status(user_id)
    update.message.reply_text(status, parse_mode="Ma
# ---------------- MAIN ----------------
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addprem", addprem_command))
    dp.add_handler(CommandHandler("premium", premium_command))
    dp.add_handler(CallbackQueryHandler(button_callback))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_number))

    updater.start_polling()
    print("🤖 Bot berjalan... tekan CTRL+C untuk berhenti.")
    updater.idle()


if __name__ == "__main__":
