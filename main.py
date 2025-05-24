import os import logging import asyncio from pyrogram import Client, filters from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery from PIL import Image from io import BytesIO from flask import Flask import threading

Flask app for Render health check

flask_app = Flask(name)

@flask_app.route('/') def home(): return "Bot is running"

Telegram bot credentials from environment variables

API_ID = int(os.environ.get("API_ID", 0)) API_HASH = os.environ.get("API_HASH", "") BOT_TOKEN = os.environ.get("BOT_TOKEN", "") FORCE_JOIN = os.environ.get("JOIN_CHANNEL", "https://t.me/+i9H909Qg9M5lMzE9") START_IMG = os.environ.get("START_IMG", "https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg")

Initialize Pyrogram Client

app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

Function to convert image to sticker

async def convert_to_sticker(image_bytes): img = Image.open(BytesIO(image_bytes)).convert("RGBA") webp_io = BytesIO() img.save(webp_io, format="WEBP") webp_io.name = "sticker.webp" webp_io.seek(0) return webp_io

Start command handler

@app.on_message(filters.command("start") & filters.private) async def start_handler(client, message: Message): try: if FORCE_JOIN.startswith("https://t.me/+"): invite_link = FORCE_JOIN.split("https://t.me/+", maxsplit=1)[-1] try: await client.get_chat_member(invite_link, message.from_user.id) except Exception: return await message.reply( "Please join the update channel to use this bot.", reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("Join Channel", url=FORCE_JOIN)], [InlineKeyboardButton("Refresh", callback_data="refresh")] ]) )

buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Help", callback_data="help")
        ],
        [InlineKeyboardButton("Join Here", url=FORCE_JOIN)]
    ])

    await message.reply_photo(
        photo=START_IMG,
        caption=(
            "👋 **Hey there!**\n\n"
            "📸 **Just send me any photo — and I’ll turn it into a Telegram sticker while keeping its original size.**\n\n"
            "❌ **No crop.** ❌ **No compression.** ✅ **Just perfect stickers.**\n\n"
            "⚡️ **Fast. Simple. Beautiful.**\n\n"
            "🔗 **Support:** [@AniReal_Support](https://t.me/AniReal_Support)"
        ),
        reply_markup=buttons
    )
except Exception as e:
    logging.error(str(e))

Force join refresh button

@app.on_callback_query(filters.regex("refresh")) async def refresh_handler(client, callback_query: CallbackQuery): await start_handler(client, callback_query.message) await callback_query.answer()

About & Help callbacks

@app.on_callback_query(filters.regex("about")) async def about_handler(client, callback_query: CallbackQuery): await callback_query.message.edit_text( """ 🤖 Bot Information

Welcome to the Auto Image to Sticker Bot!

🖼️ This bot instantly converts your photos into Telegram stickers — without resizing, cropping, or compression.

✨ Features: • Full-size image stickers • No quality loss • Super fast response • Easy to use

👨‍💻 Developer: @AniReal_Support """, disable_web_page_preview=True ) await callback_query.answer()

@app.on_callback_query(filters.regex("help")) async def help_handler(client, callback_query: CallbackQuery): await callback_query.message.edit_text( """ 🆘 How to Use This Bot

Using this bot is super simple:

1️⃣ Send me any photo
I’ll convert it into a Telegram sticker — while keeping its original size and quality.

2️⃣ Get your sticker instantly!
No crop. No compression. Just perfect HD stickers.

💡 Tips: • Use clear images for best sticker results
• Avoid screenshots with borders

❓ Need support or want your own bot?
Message: @AniReal_Support
""", disable_web_page_preview=True ) await callback_query.answer()

Custom command handler

@app.on_message(filters.command("create_own_bot") & filters.private) async def own_bot_handler(client, message: Message): await message.reply_text( "👋 Hey Dear.. This is a Paid Bot, Create Your Own Bot to Message Here:- @AniReal_Support" )

Image to sticker handler

@app.on_message(filters.photo & filters.private) async def handle_photo(client, message: Message): msg = await message.reply("Processing image into sticker...") file = await message.download() with open(file, "rb") as f: webp_file = await convert_to_sticker(f.read()) await message.reply_sticker(sticker=webp_file) await msg.delete()

Run both Flask app and Telegram bot

if name == "main": def run_flask(): port = int(os.environ.get("PORT", 5000)) flask_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()
app.run()

