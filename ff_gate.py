#!/usr/bin/env python3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import TelegramError

CHANNELS = [
    {"name": "ᴠᴏɪᴅ ᴀᴜᴛᴏ ʟɪᴋᴇ",     "handle": "@voidautolike",       "url": "https://t.me/voidautolike"},
    {"name": "ᴋɪɴɢ ᴠᴏɪᴅ ɢᴄ",       "handle": "@kingvoidofficialgc", "url": "https://t.me/kingvoidofficialgc"},
    {"name": "ᴋɪɴɢ ᴠᴏɪᴅ ᴏꜰꜰɪᴄɪᴀʟ", "handle": "@kingvoidofficials",  "url": "https://t.me/kingvoidofficials"},
]

VERIFIED = {}


def join_keyboard():
    rows = [[InlineKeyboardButton(f"📢 ᴊᴏɪɴ {c['name']}", url=c['url'])] for c in CHANNELS]
    rows.append([InlineKeyboardButton("✅ ɪ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ — ᴠᴇʀɪꜰʏ", callback_data="gate:verify")])
    return InlineKeyboardMarkup(rows)


async def is_member(bot, channel_handle, user_id):
    try:
        member = await bot.get_chat_member(chat_id=channel_handle, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except TelegramError:
        return False


async def check_all(bot, user_id):
    if VERIFIED.get(user_id):
        return True
    for c in CHANNELS:
        if not await is_member(bot, c["handle"], user_id):
            return False
    VERIFIED[user_id] = True
    return True


async def missing_channels(bot, user_id):
    out = []
    for c in CHANNELS:
        if not await is_member(bot, c["handle"], user_id):
            out.append(c)
    return out


async def send_gate(update, bot, user_id):
    text = (
        "🔒 *ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ*\n\n"
        "ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ, ᴊᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ʙᴇʟᴏᴡ.\n"
        "ᴛʜᴇɴ ᴛᴀᴘ *ɪ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ — ᴠᴇʀɪꜰʏ*. 👇"
    )
    if update.callback_query:
        await update.callback_query.message.edit_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=join_keyboard()
        )
    else:
        await update.message.reply_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=join_keyboard()
        )