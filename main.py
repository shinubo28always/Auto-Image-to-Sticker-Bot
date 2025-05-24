import os
import threading
from io import BytesIO
from flask import Flask
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery
)
Flask app for Render health check

flask_app = Flask(name)

@flask_app.route('/') def home(): return "Bot is running!"

Bot credentials

API_ID = int(os.environ.get("API_ID", 0)) API_HASH = os.environ.get("API_HASH", "") BOT_TOKEN = os.environ.get("BOT_TOKEN", "") FORCE_JOIN = os.environ.get("FORCE_JOIN", "") JOIN_CHANNEL = "AniReal_Anime_Zone" START_IMG = "https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg"

app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

Convert image to sticker

async def convert_to_sticker(image_bytes): img = Image.open(BytesIO(image_bytes)).convert("RGBA") webp_io = BytesIO() img.save(webp_io, format="WEBP") webp_io.name = "sticker.webp" webp_io.seek(0) return webp_io

Check if user is subscribed

async def is_subscribed(client, user_id): try: member = await client.get_chat_member(FORCE_JOIN, user_id) return member.status in ["member", "administrator", "creator"] except: return False

Start message

async def send_start(client, message_or_query): buttons = InlineKeyboardMarkup([ [ InlineKeyboardButton("About", callback_data="about"), InlineKeyboardButton("Help", callback_data="help") ], [InlineKeyboardButton("Join Here", url=f"https://t.me/{JOIN_CHANNEL}")] ])

caption = (
    "👋 **Hey there!**\n\n"
    "🗼️ **Just send me any photo — and I’ll turn it into a Telegram sticker while keeping its original size.**\n\n"
    "❌ **No crop.** ❌ **No compression.** ✅ **Just perfect stickers.**\n\n"
    "⚡️ **Fast. Simple. Beautiful.**\n\n"
    "🔗 **Support:** [@AniReal_Support](https://t.me/AniReal_Support)"
)

if isinstance(message_or_query, CallbackQuery):
    await message_or_query.message.edit_media(
        media=START_IMG,
        reply_markup=buttons
    )
    await message_or_query.message.edit_caption(caption, reply_markup=buttons)
else:
    await message_or_query.reply_photo(photo=START_IMG, caption=caption, reply_markup=buttons)

Start command

@app.on_message(filters.command("start") & filters.private) async def start_handler(client, message): if FORCE_JOIN and not await is_subscribed(client, message.from_user.id): buttons = InlineKeyboardMarkup([ [InlineKeyboardButton("Request to Join", url=f"https://t.me/{FORCE_JOIN.replace('@', '')}")], [InlineKeyboardButton("Try Again", callback_data="check_subscribe")] ]) await message.reply_text("🔐 You must join the update channel to use this bot.", reply_markup=buttons) return await send_start(client, message)

Callback query handler

@app.on_callback_query() async def callback_query_handler(client, query): data = query.data if data == "check_subscribe": if await is_subscribed(client, query.from_user.id): await send_start(client, query) else: await query.answer("❌ You're still not joined!", show_alert=True)

elif data == "about":
    text = (
        "🤖 **Bot Information**\n\n"
        "Welcome to the **Auto Image to Sticker Bot**!\n\n"
        "🖼️ Instantly convert your photos into Telegram stickers — without resizing or compression.\n\n"
        "✨ **Features:**\n"
        "• Full-size image stickers\n"
        "• No quality loss\n"
        "• Super fast response\n"
        "• Easy to use\n\n"
        "👨‍💻 **Developer:** [@AniReal_Support](https://t.me/AniReal_Support)"
    )
    await query.message.edit_caption(caption=text, reply_markup=query.message.reply_markup)

elif data == "help":
    text = (
        "🚘 **How to Use This Bot**\n\n"
        "1️⃣ **Send me any photo**\n"
        "I'll convert it into a Telegram sticker with full quality.\n\n"
        "2️⃣ **Get your sticker instantly!**\n"
        "No crop. No compression. Just perfect HD stickers.\n\n"
        "💡 **Tips:**\n"
        "• Use clear images for best results\n"
        "• Avoid screenshots with borders\n\n"
        "❓ Need help? Contact: [@AniReal_Support](https://t.me/AniReal_Support)"
    )
    await query.message.edit_caption(caption=text, reply_markup=query.message.reply_markup)

@app.on_message(filters.photo & filters.private) async def photo_to_sticker(client, message): if message.from_user.is_self: return try: photo = await message.download() img = Image.open(photo).convert("RGBA") output = BytesIO() output.name = "sticker.webp" img.save(output, "WEBP") output.seek(0) await message.reply_sticker(output) except Exception as e: await message.reply_text("Something went wrong:\n" + str(e))

Custom command

@app.on_message(filters.command("create_own_bot") & filters.private) async def create_own_bot(client, message): await message.reply_text( "👋 Hey Dear.. This is a Paid Bot, Create Your Own Bot to Message Here:- @AniReal_Support" )

if name == "main": def run_flask(): port = int(os.environ.get("PORT", 5000)) flask_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()
app.run()

