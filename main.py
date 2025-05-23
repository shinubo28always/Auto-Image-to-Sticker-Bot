import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from PIL import Image
from io import BytesIO
from flask import Flask
import threading

# Flask app for Render health check
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running"

# Telegram credentials
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
UPDATE_CHANNEL = "+i9H909Qg9M5lMzE9"  # Set your channel username here (without @), or leave blank to disable

# Initialize bot
app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Force join check
async def is_subscribed(client, user_id):
    if not UPDATE_CHANNEL:
        return True  # Skip check if channel not set
    try:
        member = await client.get_chat_member(f"@{UPDATE_CHANNEL}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"[FORCE JOIN] Error: {e}")
        return False

# Sticker conversion
async def convert_to_sticker(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    webp_io = BytesIO()
    img.save(webp_io, format="WEBP")
    webp_io.name = "sticker.webp"
    webp_io.seek(0)
    return webp_io

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    user_id = message.from_user.id

    if not await is_subscribed(client, user_id):
        await message.reply_text(
            "🔒 **Please join our update channel to use this bot.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Here", url=f"https://t.me/+i9H909Qg9M5lMzE9")]
            ])
        )
        return

    await message.reply_photo(
        photo="https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg",  # Replace with your image URL
        caption=(
            "👋 **Hey there!**\n\n"
            "📸 **Just send me any photo — and I’ll turn it into a Telegram sticker while keeping its original size.**\n\n"
            "❌ **No crop.** ❌ **No compression.** ✅ **Just perfect stickers.**\n\n"
            "⚡️ **Fast. Simple. Beautiful.**\n\n"
            "🔗 **Support:** [@AniReal_Support](https://t.me/AniReal_Support)"
        ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Help", callback_data="help")
            ],
            [InlineKeyboardButton("Join Here", url=f"https://t.me/AniReal_Updates" if UPDATE_CHANNEL else "https://t.me/AniReal_Anime_Zone")]
        ]),
        disable_web_page_preview=True
    )

# Handle photo to sticker
@app.on_message(filters.photo)
async def handle_photo(client, message):
    user_id = message.from_user.id

    if not await is_subscribed(client, user_id):
        await message.reply_text(
            "🔒 **Please join our update channel to use this bot.**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Here", url=f"https://t.me/+i9H909Qg9M5lMzE9")]
            ])
        )
        return

    msg = await message.reply("Processing image into sticker...")
    file = await message.download()
    with open(file, "rb") as f:
        webp_file = await convert_to_sticker(f.read())
    await message.reply_sticker(sticker=webp_file)
    await msg.delete()

# Custom command
@app.on_message(filters.command("create_own_bot") & filters.private)
async def own_bot(client, message: Message):
    await message.reply_text(
        "👋Hello Dude! This is a Paid Bot.\n\nCreate Your Own Bot, Talk To My Senpai: [@AniReal_Support](https://t.me/AniReal_Support)",
        disable_web_page_preview=True
    )

# Callbacks for buttons
@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    if data == "about":
        await callback_query.message.edit_text(
            "**About This Bot:**\n\n"
            "This bot converts your photos to Telegram stickers while keeping their original size.\n\n"
            "Bot by: [@AniReal_Support](https://t.me/AniReal_Support)",
            disable_web_page_preview=True
        )
    elif data == "help":
        await callback_query.message.edit_text(
            "**Help & Features:**\n\n"
            "1. Send any image to convert it to sticker.\n"
            "2. No crop or resize — original aspect ratio is preserved.\n"
            "3. Fast response, clean design.\n\n"
            "Support: [@AniReal_Support](https://t.me/AniReal_Support)",
            disable_web_page_preview=True
        )

# Start Flask + Bot
if __name__ == "__main__":
    def run_flask():
        port = int(os.environ.get("PORT", 5000))
        flask_app.run(host="0.0.0.0", port=port)

    threading.Thread(target=run_flask).start()
    app.run()
