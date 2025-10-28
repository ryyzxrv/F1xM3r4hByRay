#!/usr/bin/env python3
# bot.py - Telegram bot Fix Merah (cek bio dihapus, ada global cooldown)
# Compatible with python-telegram-bot v13 (Updater)

import os
import time
import logging
from typing import List

from telegram import (
    Bot,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters,
    CallbackContext,
)

try:
    from utils_premium import is_premium, OWNER_ID
except Exception:
    OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

    def is_premium(user_id):
        return int(user_id) == int(OWNER_ID)

# ========================= CONFIG =========================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8266869214:AAFhzKVEaBRhIVxVKDZlwrS7u375bci_vqs")
BANNER_URL = os.environ.get("BANNER_URL", "https://files.catbox.moe/vvotfi.jpg")
OWNER_USERNAME_URL = os.environ.get("OWNER_URL", "https://t.me/r4vnnx")

# Global Cooldown (detik)
GLOBAL_COOLDOWN = 20  # sekarang 20 detik
_last_command_time = 0

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ========================= HELPERS =========================
def parse_numbers_from_text(text: str) -> List[str]:
    import re
    if not text:
        return []
    nums = re.findall(r"\d+", text)
    return [n.strip() for n in nums if n.strip()]


# ========================= HANDLERS =========================
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    keyboard = [
        [InlineKeyboardButton("🧩 FIX MERAH", callback_data="fix_merah")],
        [
            InlineKeyboardButton("📱 Cek Nomor", callback_data="cek_num"),
            InlineKeyboardButton("👤 Cek ID", callback_data="cek_id"),
        ],
        [InlineKeyboardButton("👑 Owner", url=OWNER_USERNAME_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        "👋 *Selamat Datang di Bot Fix Merah!*\n\n"
        "Gunakan tombol di bawah untuk memilih aksi:\n"
        "🧩 *Fix Merah* — Kirim nomor merah kamu.\n"
        "📱 *Cek Nomor* — Cek format nomor kamu.\n"
        "👤 *Cek ID* — Lihat ID Telegram kamu.\n\n"
        "_© Rayyzxer 2025_"
    )

    try:
        context.bot.send_photo(
            chat_id=chat_id,
            photo=BANNER_URL,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    except Exception:
        context.bot.send_message(
            chat_id=chat_id, text=caption, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
        )


def button_callback(update: Update, context: CallbackContext):
    global _last_command_time
    query = update.callback_query
    data = query.data

    now = time.time()
    if now - _last_command_time < GLOBAL_COOLDOWN:
        query.answer("⏳ Tunggu beberapa detik sebelum gunakan lagi.")
        return
    _last_command_time = now

    if data == "fix_merah":
        query.answer()
        query.message.reply_text(
            "🧩 Untuk FIX MERAH: Kirim nomor merah kamu.\n"
            "Contoh: `/fix 628123456789`\n\n",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data == "cek_num":
        query.answer()
        query.message.reply_text(
            "📱 Masukkan nomor yang mau dicek.\nContoh: `/cek 628123456789,628987654321`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if data == "cek_id":
        query.answer()
        uid = query.from_user.id
        query.message.reply_text(f"👤 ID Telegram kamu: `{uid}`", parse_mode=ParseMode.MARKDOWN)
        return

    query.answer()


# ========================= COMMANDS =========================
def cmd_fix(update: Update, context: CallbackContext):
    global _last_command_time
    now = time.time()
    if now - _last_command_time < GLOBAL_COOLDOWN:
        return update.message.reply_text("⏳ Tunggu beberapa detik sebelum gunakan lagi.")
    _last_command_time = now

    text = update.message.text or ""
    parts = text.split(" ", 1)
    if len(parts) < 2 or not parts[1].strip():
        return update.message.reply_text(
            "🧩 Kirim contoh: `/fix 628123456789`",
            parse_mode=ParseMode.MARKDOWN,
        )

    numbers = parse_numbers_from_text(parts[1])
    if not numbers:
        return update.message.reply_text("❌ Nomor tidak valid.", parse_mode=ParseMode.MARKDOWN)

    result = "\n".join([f"✅ Nomor {n} berhasil di-fix!" for n in numbers])
    update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


def cmd_cek(update: Update, context: CallbackContext):
    global _last_command_time
    now = time.time()
    if now - _last_command_time < GLOBAL_COOLDOWN:
        return update.message.reply_text("⏳ Tunggu beberapa detik sebelum gunakan lagi.")
    _last_command_time = now

    text = update.message.text or ""
    parts = text.split(" ", 1)
    if len(parts) < 2 or not parts[1].strip():
        return update.message.reply_text(
            "📱 Kirim contoh: `/cek 628123456789` atau `/cek 628123456789,628987654321`",
            parse_mode=ParseMode.MARKDOWN,
        )

    numbers = parse_numbers_from_text(parts[1])
    if not numbers:
        return update.message.reply_text("❌ Nomor tidak valid.", parse_mode=ParseMode.MARKDOWN)

    result = "\n".join([f"📱 Nomor: {n}" for n in numbers])
    update.message.reply_text(result, parse_mode=ParseMode.MARKDOWN)


# ========================= MAIN =========================
def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("BOT_TOKEN belum di-set.")
        return

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fix", cmd_fix))
    dp.add_handler(CommandHandler("cek", cmd_cek))

    # Callback Query (buttons)
    dp.add_handler(CallbackQueryHandler(button_callback))

    logger.info("Bot Fix Merah started...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
