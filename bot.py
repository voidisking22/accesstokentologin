#!/usr/bin/env python3
import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
import ff_core
import ff_gate

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
CONTACT_1 = os.getenv("CONTACT_1", "@voidisking")
CONTACT_2 = os.getenv("CONTACT_2", "@lordofzone")
SERVER_URL = os.getenv("SERVER_URL", "http://0.0.0.0:5030/")

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
log = logging.getLogger("ffbot")

USER_TOKENS = {}
AWAITING_TOKEN = set()  # user_ids currently in token-entry state


def contact_footer():
    return f"📩 ᴀɴʏ ɪssᴜᴇs → {CONTACT_1} ᴏʀ {CONTACT_2}"


def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎮 ʟᴏɢɪɴ ɢᴀᴍᴇ", callback_data="menu:login")],
        [InlineKeyboardButton("📖 ᴛᴜᴛᴏʀɪᴀʟ", callback_data="menu:tutorial")],
        [InlineKeyboardButton("👨‍💻 ᴀʙᴏᴜᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ", callback_data="menu:about")],
        [InlineKeyboardButton("📞 ᴄᴏɴᴛᴀᴄᴛ", url=f"https://t.me/{CONTACT_1.lstrip('@')}")],
    ])


def token_entry_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 ʜᴏᴡ ᴛᴏ ɢᴇᴛ ᴛᴏᴋᴇɴ", callback_data="menu:tutorial")],
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴍᴇɴᴜ", callback_data="menu:home")],
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴍᴇɴᴜ", callback_data="menu:home")]
    ])


async def gate(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> bool:
    user = update.effective_user
    if user is None:
        return False
    if user.id in ADMIN_IDS:
        return True
    if ff_gate.VERIFIED.get(user.id):
        return True
    ok = await ff_gate.check_all(ctx.bot, user.id)
    if ok:
        return True
    await ff_gate.send_gate(update, ctx.bot, user.id)
    return False


# ---------- /start ----------

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, ctx):
        return
    name = update.effective_user.first_name or "ᴛʀᴀɪɴᴇʀ"
    text = (
        f"👋 ʜᴇʏ *{name}*,\n\n"
        "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ *ᴠᴏɪᴅ ᴀᴄᴄᴇss ʟᴏɢɪɴ ʙᴏᴛ* 🔥\n\n"
        "ɪ ɢᴇɴᴇʀᴀᴛᴇ ᴀ sᴇᴄᴜʀᴇ ɢᴀʀᴇɴᴀ ᴍᴀᴊᴏʀ ʟᴏɢɪɴ ᴛᴏᴋᴇɴ ꜰᴏʀ ʏᴏᴜʀ "
        "ꜰʀᴇᴇ ꜰɪʀᴇ ᴀᴄᴄᴏᴜɴᴛ sᴏ ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴀᴛᴄʜᴇs "
        "ᴡɪᴛʜᴏᴜᴛ ᴛʜᴇ ᴜsᴜᴀʟ ʟɪᴍɪᴛs. ⚡\n\n"
        "ᴡʜᴀᴛ ɪ ᴅᴏ:\n"
        "• 🔑 ɢᴇɴᴇʀᴀᴛᴇ ʟᴏɢɪɴ ᴛᴏᴋᴇɴs ꜰʀᴏᴍ ʏᴏᴜʀ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ\n"
        "• 🧠 ᴠᴀʟɪᴅᴀᴛᴇ ᴛᴏᴋᴇɴs ᴀɢᴀɪɴsᴛ ɢᴀʀᴇɴᴀ sᴇʀᴠᴇʀs\n"
        "• 📦 ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ `localconfig.json` sᴇᴛᴜᴘ\n"
        "• 🚀 ᴋᴇᴇᴘ ʏᴏᴜ ɪɴ ᴛʜᴇ ɢᴀᴍᴇ, ᴍᴀᴛᴄʜ ᴀꜰᴛᴇʀ ᴍᴀᴛᴄʜ\n\n"
        "*ᴛᴀᴘ ᴀ ʙᴜᴛᴛᴏɴ ᴛᴏ ʙᴇɢɪɴ.* 👇\n\n"
        f"_{contact_footer()}_"
    )
    await update.message.reply_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu_keyboard()
    )


# ---------- /help ----------

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, ctx):
        return
    text = (
        "📋 *ᴄᴏᴍᴍᴀɴᴅs*\n\n"
        "/start — ᴍᴀɪɴ ᴍᴇɴᴜ\n"
        "/help — ᴛʜɪs ʟɪsᴛ\n"
        "/login — sᴛᴀʀᴛ ᴛᴏᴋᴇɴ ʟᴏɢɪɴ ꜰʟᴏᴡ\n"
        "/settoken `<token>` — sᴀᴠᴇ ᴛᴏᴋᴇɴ ᴅɪʀᴇᴄᴛʟʏ\n"
        "/info — ᴀᴄᴄᴏᴜɴᴛ ɪɴꜰᴏ\n"
        "/jwt — ʙᴜɪʟᴅ ᴍᴀᴊᴏʀ ʟᴏɢɪɴ ᴊᴡᴛ\n"
        "/cleartoken — ᴡɪᴘᴇ sᴛᴏʀᴇᴅ ᴛᴏᴋᴇɴ\n\n"
        f"_{contact_footer()}_"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ---------- login flow ----------

async def login_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, ctx):
        return
    AWAITING_TOKEN.add(update.effective_user.id)
    text = (
        "🔐 *ᴛᴏᴋᴇɴ ʟᴏɢɪɴ*\n\n"
        "ᴘᴀsᴛᴇ ʏᴏᴜʀ *ꜰʀᴇᴇ ꜰɪʀᴇ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ* ʙᴇʟᴏᴡ.\n\n"
        "ᴛʜᴇ ᴛᴏᴋᴇɴ ɪs ᴀ ʟᴏɴɢ sᴛʀɪɴɢ ᴛʜᴀᴛ sᴛᴀʀᴛs ᴡɪᴛʜ `eyJ` ᴀɴᴅ "
        "ᴄᴏɴᴛᴀɪɴs ᴛʜʀᴇᴇ ᴘᴀʀᴛs sᴇᴘᴀʀᴀᴛᴇᴅ ʙʏ ᴅᴏᴛs.\n\n"
        "ᴀꜰᴛᴇʀ ʏᴏᴜ sᴇɴᴅ ɪᴛ, ɪ ᴠᴀʟɪᴅᴀᴛᴇ ɪᴛ ᴡɪᴛʜ ɢᴀʀᴇɴᴀ ᴀɴᴅ ʀᴇᴛᴜʀɴ "
        "ʏᴏᴜʀ ʟᴏɢɪɴ ᴛᴏᴋᴇɴ + sᴇᴛᴜᴘ sᴛᴇᴘs.\n\n"
        f"_{contact_footer()}_"
    )
    await update.message.reply_text(
        text, parse_mode=ParseMode.MARKDOWN, reply_markup=token_entry_keyboard()
    )


# ---------- token validation ----------

async def _validate_and_reply(update: Update, ctx: ContextTypes.DEFAULT_TYPE, token: str):
    """Send validating message, try fetch_account_info + inspect, reply accordingly."""
    sent = await update.message.reply_text(
        "⏳ ᴠᴀʟɪᴅᴀᴛɪɴɢ ᴛᴏᴋᴇɴ ᴡɪᴛʜ ɢᴀʀᴇɴᴀ...",
        parse_mode=ParseMode.MARKDOWN
    )
    try:
        acc_uid, region, nickname, platform = ff_core.fEtChAcCoUnTiNfO(token)
        open_id = ff_core.iNsPeCtToKeN(token)
    except Exception as e:
        log.warning("token validation failed: %s", e)
        invalid_text = (
            "❌ *ɪɴᴠᴀʟɪᴅ ᴛᴏᴋᴇɴ.*\n\n"
            "ᴛʜᴇ ᴛᴏᴋᴇɴ ʏᴏᴜ ᴘʀᴏᴠɪᴅᴇᴅ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ᴠᴀʟɪᴅᴀᴛᴇᴅ ʙʏ "
            "ɢᴀʀᴇɴᴀ's sᴇʀᴠᴇʀs.\n"
            "ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.\n\n"
            "📋 *ʜᴏᴡ ᴛᴏ ᴜsᴇ*\n\n"
            "1. ᴄᴏᴘʏ ᴛʜᴇ sᴇʀᴠᴇʀ ᴜʀʟ ʙᴇʟᴏᴡ\n"
            f"`{SERVER_URL}`\n\n"
            "2. ɢᴏ ᴛᴏ ᴛʜɪs ᴅɪʀᴇᴄᴛᴏʀʏ:\n"
            "`/storage/emulated/0/Android/data/com.dts.freefiremax/files/`\n\n"
            "3. ᴄʀᴇᴀᴛᴇ ᴀ ɴᴇᴡ ꜰɪʟᴇ ɴᴀᴍᴇᴅ `localconfig.json`\n\n"
            "4. ᴘᴀsᴛᴇ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ᴄᴏɴᴛᴇɴᴛ ɪɴᴛᴏ ᴛʜᴇ ꜰɪʟᴇ:\n"
            "```json\n"
            "{\n"
            f'  "serverUrl": "{SERVER_URL}"\n'
            "}\n"
            "```\n\n"
            "5. sᴀᴠᴇ ᴛʜᴇ ꜰɪʟᴇ\n"
            "6. ᴏᴘᴇɴ ꜰʀᴇᴇ ꜰɪʀᴇ ᴏʀ ꜰʀᴇᴇ ꜰɪʀᴇ ᴍᴀx, ᴄʜᴏᴏsᴇ ᴀɴʏ "
            "ᴘʟᴀᴛꜰᴏʀᴍ ᴀɴᴅ ʟᴏɢɪɴ ᴛᴏ ʏᴏᴜʀ ɢᴀᴍᴇ ᴀᴄᴄᴏᴜɴᴛ\n"
            "7. ᴏɴᴄᴇ ʟᴏɢɢᴇᴅ ɪɴ, ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴀᴛᴄʜᴇs\n\n"
            "⚠️ ɴᴏᴛᴇ: ᴡᴏʀᴋs ᴡɪᴛʜ ʙᴏᴛʜ ꜰʀᴇᴇ ꜰɪʀᴇ ᴀɴᴅ ꜰʀᴇᴇ ꜰɪʀᴇ ᴍᴀx.\n"
            f"ᴅᴍ {CONTACT_1} ɪꜰ ʏᴏᴜ ꜰᴀᴄᴇ ᴀɴʏ ɪssᴜᴇs.\n\n"
            f"_{contact_footer()}_"
        )
        await sent.edit_text(
            invalid_text, parse_mode=ParseMode.MARKDOWN,
            reply_markup=token_entry_keyboard()
        )
        return
    USER_TOKENS[update.effective_user.id] = token
    AWAITING_TOKEN.discard(update.effective_user.id)
    valid_text = (
        "✅ *ᴛᴏᴋᴇɴ ᴠᴀʟɪᴅᴀᴛᴇᴅ.*\n\n"
        "🔓 ʏᴏᴜʀ ᴀᴄᴄᴏᴜɴᴛ ɪs ɴᴏᴡ ʟɪɴᴋᴇᴅ.\n\n"
        "📊 *ᴀᴄᴄᴏᴜɴᴛ ᴅᴇᴛᴀɪʟs*\n"
        f"👤 ɴɪᴄᴋɴᴀᴍᴇ : `{nickname}`\n"
        f"🌍 ʀᴇɢɪᴏɴ   : `{region}`\n"
        f"🆔 ᴜɪᴅ      : `{acc_uid}`\n"
        f"📱 ᴘʟᴀᴛꜰᴏʀᴍ : `{platform}`\n"
        f"🔑 ᴏᴘᴇɴ ɪᴅ  : `{open_id}`\n\n"
        "📋 *ɴᴇxᴛ sᴛᴇᴘs*\n\n"
        "1. ᴄᴏᴘʏ ᴛʜᴇ sᴇʀᴠᴇʀ ᴜʀʟ ʙᴇʟᴏᴡ\n"
        f"`{SERVER_URL}`\n\n"
        "2. ɢᴏ ᴛᴏ ᴛʜɪs ᴅɪʀᴇᴄᴛᴏʀʏ:\n"
        "`/storage/emulated/0/Android/data/com.dts.freefiremax/files/`\n\n"
        "3. ᴄʀᴇᴀᴛᴇ ᴀ ɴᴇᴡ ꜰɪʟᴇ ɴᴀᴍᴇᴅ `localconfig.json`\n\n"
        "4. ᴘᴀsᴛᴇ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ᴄᴏɴᴛᴇɴᴛ ɪɴᴛᴏ ᴛʜᴇ ꜰɪʟᴇ:\n"
        "```json\n"
        "{\n"
        f'  "serverUrl": "{SERVER_URL}"\n'
        "}\n"
        "```\n\n"
        "5. sᴀᴠᴇ ᴛʜᴇ ꜰɪʟᴇ\n"
        "6. ᴏᴘᴇɴ ꜰʀᴇᴇ ꜰɪʀᴇ ᴏʀ ꜰʀᴇᴇ ꜰɪʀᴇ ᴍᴀx, ᴄʜᴏᴏsᴇ ᴀɴʏ "
        "ᴘʟᴀᴛꜰᴏʀᴍ ᴀɴᴅ ʟᴏɢɪɴ ᴛᴏ ʏᴏᴜʀ ɢᴀᴍᴇ ᴀᴄᴄᴏᴜɴᴛ\n"
        "7. ᴏɴᴄᴇ ʟᴏɢɢᴇᴅ ɪɴ, ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴀᴛᴄʜᴇs\n\n"
        "⚠️ ɴᴏᴛᴇ: ᴡᴏʀᴋs ᴡɪᴛʜ ʙᴏᴛʜ ꜰʀᴇᴇ ꜰɪʀᴇ ᴀɴᴅ ꜰʀᴇᴇ ꜰɪʀᴇ ᴍᴀx.\n"
        f"ᴅᴍ {CONTACT_1} ɪꜰ ʏᴏᴜ ꜰᴀᴄᴇ ᴀɴʏ ɪssᴜᴇs.\n\n"
        "ᴜsᴇ /jwt ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ʏᴏᴜʀ ʟᴏɢɪɴ ᴛᴏᴋᴇɴ.\n\n"
        f"_{contact_footer()}_"
    )
    await sent.edit_text(
        valid_text, parse_mode=ParseMode.MARKDOWN,
        reply_markup=back_keyboard()
    )


# ---------- legacy commands ----------

async def set_token(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, ctx):
        return
    token = " ".join(ctx.args).strip() if ctx.args else ""
    if not token:
        await update.message.reply_text(
            "ᴜsᴀɢᴇ: `/settoken <access_token>`", parse_mode=ParseMode.MARKDOWN
        )
        return
    await _validate_and_reply(update, ctx, token)


async def info(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, ctx):
        return
    token = USER_TOKENS.get(update.effective_user.id)
    if not token:
        await update.message.reply_text(
            "ɴᴏ ᴛᴏᴋᴇɴ sᴛᴏʀᴇᴅ. ᴜsᴇ /login ꜰɪʀsᴛ.",
            parse_mode=ParseMode.MARKDOWN, reply_markup=token_entry_keyboard()
        )
        return
    msg = await update.message.reply_text("⏳ ꜰᴇᴛᴄʜɪɴɢ ᴀᴄᴄᴏᴜɴᴛ ɪɴꜰᴏ...")
    try:
        acc_uid, region, nickname, platform = ff_core.fEtChAcCoUnTiNfO(token)
        text = (
            "📊 *ᴀᴄᴄᴏᴜɴᴛ ɪɴꜰᴏ*\n\n"
            f"👤 ɴɪᴄᴋɴᴀᴍᴇ : `{nickname}`\n"
            f"🌍 ʀᴇɢɪᴏɴ   : `{region}`\n"
            f"🆔 ᴜɪᴅ      : `{acc_uid}`\n"
            f"📱 ᴘʟᴀᴛꜰᴏʀᴍ : `{platform}`\n\n"
            f"_{contact_footer()}_"
        )
        await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_keyboard())
    except Exception as e:
        await msg.edit_text(
            f"❌ ꜰᴀɪʟᴇᴅ: `{e}`\n\n_{contact_footer()}_",
            parse_mode=ParseMode.MARKDOWN
        )


async def jwt_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, ctx):
        return
    uid = update.effective_user.id
    token = USER_TOKENS.get(uid)
    if not token:
        await update.message.reply_text(
            "ɴᴏ ᴛᴏᴋᴇɴ sᴛᴏʀᴇᴅ. ᴜsᴇ /login ꜰɪʀsᴛ.",
            parse_mode=ParseMode.MARKDOWN, reply_markup=token_entry_keyboard()
        )
        return
    msg = await update.message.reply_text("⏳ ʙᴜɪʟᴅɪɴɢ ᴊᴡᴛ...")
    try:
        acc_uid, region, nickname, platform = ff_core.fEtChAcCoUnTiNfO(token)
        open_id = ff_core.iNsPeCtToKeN(token)
        base = {"4": "Free Fire", "5": 1, "8": "android", "21": "en"}
        raw = ff_core.gEnErAtEmAjOrLoGiNrEsP(token, open_id, base, platform)
        out_path = f"/tmp/jwt_{uid}.bin"
        with open(out_path, "wb") as f:
            f.write(raw)
        text = (
            "🔑 *ᴊᴡᴛ ɢᴇɴᴇʀᴀᴛᴇᴅ*\n\n"
            f"👤 ɴɪᴄᴋɴᴀᴍᴇ : `{nickname}`\n"
            f"🌍 ʀᴇɢɪᴏɴ   : `{region}`\n"
            f"🆔 ᴜɪᴅ      : `{acc_uid}`\n"
            f"🔑 ᴏᴘᴇɴ ɪᴅ  : `{open_id}`\n"
            f"📦 ʙʏᴛᴇs    : `{len(raw)}`\n\n"
            f"_{contact_footer()}_"
        )
        await msg.edit_text(text, parse_mode=ParseMode.MARKDOWN)
        await update.message.reply_document(
            document=open(out_path, "rb"), filename=f"jwt_{uid}.bin"
        )
        os.remove(out_path)
    except Exception as e:
        await msg.edit_text(
            f"❌ ꜰᴀɪʟᴇᴅ: `{e}`\n\n_{contact_footer()}_",
            parse_mode=ParseMode.MARKDOWN
        )


async def clear_token(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, ctx):
        return
    USER_TOKENS.pop(update.effective_user.id, None)
    AWAITING_TOKEN.discard(update.effective_user.id)
    await update.message.reply_text("🗑 ᴛᴏᴋᴇɴ ᴡɪᴘᴇᴅ.")


# ---------- text handler ----------

async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not await gate(update, ctx):
        return
    uid = update.effective_user.id
    text = (update.message.text or "").strip()

    # explicit token-entry state, or auto-detect long token
    looks_like_token = len(text) > 40 and " " not in text
    if uid in AWAITING_TOKEN or looks_like_token:
        await _validate_and_reply(update, ctx, text)
        return

    await update.message.reply_text(
        "🤔 ᴜɴᴋɴᴏᴡɴ ɪɴᴘᴜᴛ.\nᴛᴀᴘ /start ᴛᴏ ᴏᴘᴇɴ ᴛʜᴇ ᴍᴇɴᴜ.",
        parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu_keyboard()
    )


# ---------- callback buttons ----------

async def on_menu_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    user_id = q.from_user.id

    if data == "menu:home":
        name = q.from_user.first_name or "ᴛʀᴀɪɴᴇʀ"
        text = (
            f"👋 ʜᴇʏ *{name}*,\n\n"
            "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ *ᴠᴏɪᴅ ᴀᴄᴄᴇss ʟᴏɢɪɴ ʙᴏᴛ* 🔥\n\n"
            "*ᴛᴀᴘ ᴀ ʙᴜᴛᴛᴏɴ ᴛᴏ ʙᴇɢɪɴ.* 👇\n\n"
            f"_{contact_footer()}_"
        )
        await q.message.edit_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu_keyboard()
        )
        return

    if data == "menu:login":
        AWAITING_TOKEN.add(user_id)
        text = (
            "🔐 *ᴛᴏᴋᴇɴ ʟᴏɢɪɴ*\n\n"
            "ᴘᴀsᴛᴇ ʏᴏᴜʀ *ꜰʀᴇᴇ ꜰɪʀᴇ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ* ʙᴇʟᴏᴡ.\n\n"
            "ᴛʜᴇ ᴛᴏᴋᴇɴ sᴛᴀʀᴛs ᴡɪᴛʜ `eyJ` ᴀɴᴅ ʜᴀs ᴛʜʀᴇᴇ ᴘᴀʀᴛs "
            "sᴇᴘᴀʀᴀᴛᴇᴅ ʙʏ ᴅᴏᴛs.\n\n"
            f"_{contact_footer()}_"
        )
        await q.message.edit_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=token_entry_keyboard()
        )
        return

    if data == "menu:tutorial":
        text = (
            "📖 *ᴛᴜᴛᴏʀɪᴀʟ — ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ*\n\n"
            "*sᴛᴇᴘ 1* — ᴛᴀᴘ 🎮 ʟᴏɢɪɴ ɢᴀᴍᴇ\n"
            "ᴘᴀsᴛᴇ ʏᴏᴜʀ ꜰʀᴇᴇ ꜰɪʀᴇ ᴀᴄᴄᴇss ᴛᴏᴋᴇɴ.\n\n"
            "*sᴛᴇᴘ 2* — ᴡᴀɪᴛ ꜰᴏʀ ᴠᴀʟɪᴅᴀᴛɪᴏɴ\n"
            "ɪ ᴄʜᴇᴄᴋ ɪᴛ ᴡɪᴛʜ ɢᴀʀᴇɴᴀ's sᴇʀᴠᴇʀs.\n\n"
            "*sᴛᴇᴘ 3* — ᴄᴏᴘʏ ᴛʜᴇ sᴇʀᴠᴇʀ ᴜʀʟ ɪ ɢɪᴠᴇ ʏᴏᴜ\n"
            "ᴛʜᴇʏ ʟᴏᴏᴋ ʟɪᴋᴇ:\n"
            f"`{SERVER_URL}`\n\n"
            "*sᴛᴇᴘ 4* — ɢᴏ ᴛᴏ ᴛʜɪs ᴅɪʀᴇᴄᴛᴏʀʏ ᴡɪᴛʜ ᴀ ꜰɪʟᴇ ᴍᴀɴᴀɢᴇʀ\n"
            "`/storage/emulated/0/Android/data/com.dts.freefiremax/files/`\n\n"
            "*sᴛᴇᴘ 5* — ᴄʀᴇᴀᴛᴇ ᴀ ɴᴇᴡ ꜰɪʟᴇ ɴᴀᴍᴇᴅ `localconfig.json`\n\n"
            "*sᴛᴇᴘ 6* — ᴘᴀsᴛᴇ ᴛʜɪs ᴄᴏɴᴛᴇɴᴛ ᴇxᴀᴄᴛʟʏ:\n"
            "```json\n"
            "{\n"
            f'  "serverUrl": "{SERVER_URL}"\n'
            "}\n"
            "```\n\n"
            "*sᴛᴇᴘ 7* — sᴀᴠᴇ ᴛʜᴇ ꜰɪʟᴇ\n\n"
            "*sᴛᴇᴘ 8* — ᴏᴘᴇɴ ꜰʀᴇᴇ ꜰɪʀᴇ ᴏʀ ꜰʀᴇᴇ ꜰɪʀᴇ ᴍᴀx\n"
            "ᴄʜᴏᴏsᴇ ᴀɴʏ ᴘʟᴀᴛꜰᴏʀᴍ ᴀɴᴅ ʟᴏɢɪɴ ᴛᴏ ʏᴏᴜʀ ɢᴀᴍᴇ ᴀᴄᴄᴏᴜɴᴛ.\n\n"
            "*sᴛᴇᴘ 9* — ᴏɴᴄᴇ ʟᴏɢɢᴇᴅ ɪɴ, ʏᴏᴜ ᴄᴀɴ ᴘʟᴀʏ "
            "ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴀᴛᴄʜᴇs ⚡\n\n"
            "⚠️ ɴᴏᴛᴇ: ᴡᴏʀᴋs ᴡɪᴛʜ ʙᴏᴛʜ ꜰʀᴇᴇ ꜰɪʀᴇ ᴀɴᴅ ꜰʀᴇᴇ ꜰɪʀᴇ ᴍᴀx.\n"
            f"ᴅᴍ {CONTACT_1} ɪꜰ ʏᴏᴜ ꜰᴀᴄᴇ ᴀɴʏ ɪssᴜᴇs.\n\n"
            f"_{contact_footer()}_"
        )
        await q.message.edit_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_keyboard()
        )
        return

    if data == "menu:about":
        text = (
            "👨‍💻 *ᴀʙᴏᴜᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ*\n\n"
            "ᴛʜɪs ʙᴏᴛ ᴡᴀs ʙᴜɪʟᴛ ᴀɴᴅ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ:\n\n"
            "🧠 *ᴠᴏɪᴅ*\n"
            f"📩 {CONTACT_1}\n"
            f"📩 {CONTACT_2}\n\n"
            "ᴛᴇᴄʜ sᴛᴀᴄᴋ:\n"
            "• ᴘʏᴛʜᴏɴ 3.11\n"
            "• ᴘʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ 21.6\n"
            "• ɢᴀʀᴇɴᴀ ᴍᴀᴊᴏʀ ʟᴏɢɪɴ ᴘʀᴏᴛᴏᴄᴏʟ\n"
            "• ᴘʀᴏᴛᴏʙᴜꜰ 5.28.3\n\n"
            "ʀᴇᴘᴏʀᴛ ʙᴜɢs ᴏʀ ʀᴇǫᴜᴇsᴛ ꜰᴇᴀᴛᴜʀᴇs ᴛᴏ ᴛʜᴇ "
            "ᴄᴏɴᴛᴀᴄᴛs ᴀʙᴏᴠᴇ.\n\n"
            f"_{contact_footer()}_"
        )
        await q.message.edit_text(
            text, parse_mode=ParseMode.MARKDOWN, reply_markup=back_keyboard()
        )
        return


async def on_verify_button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("ᴄʜᴇᴄᴋɪɴɢ...")
    user_id = q.from_user.id
    missing = await ff_gate.missing_channels(ctx.bot, user_id)
    if not missing:
        ff_gate.VERIFIED[user_id] = True
        await q.message.edit_text(
            "✅ *ᴠᴇʀɪꜰɪᴇᴅ.* sᴇɴᴅ /start ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        names = "\n".join(f"• {c['name']}" for c in missing)
        await q.message.edit_text(
            f"❌ *sᴛɪʟʟ ɴᴏᴛ ᴊᴏɪɴᴇᴅ:*\n{names}\n\nᴊᴏɪɴ ᴀʟʟ, ᴛʜᴇɴ ᴛᴀᴘ ᴠᴇʀɪꜰʏ ᴀɢᴀɪɴ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ff_gate.join_keyboard()
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("login", login_cmd))
    app.add_handler(CommandHandler("settoken", set_token))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("jwt", jwt_cmd))
    app.add_handler(CommandHandler("cleartoken", clear_token))
    app.add_handler(CallbackQueryHandler(on_menu_button, pattern=r"^menu:"))
    app.add_handler(CallbackQueryHandler(on_verify_button, pattern=r"^gate:verify$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    log.info("ᴠᴏɪᴅ ʟᴏɢɪɴ ʙᴏᴛ sᴛᴀʀᴛɪɴɢ")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()