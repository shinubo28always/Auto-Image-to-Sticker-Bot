import os
import threading
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image
from io import BytesIO
from flask import Flask

# Flask app for Render health check
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running"

# Environment variables
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
UPDATE_CHANNEL = os.environ.get("UPDATE_CHANNEL", "AniReal_Anime_Zone")

# Initialize Pyrogram Client
app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Check if user is subscribed
async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(chat_id=f"@{UPDATE_CHANNEL}", user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# Convert image to sticker
async def convert_to_sticker(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    webp_io = BytesIO()
    img.save(webp_io, format="WEBP")
    webp_io.name = "sticker.webp"
    webp_io.seek(0)
    return webp_io

# Handle photo to sticker
@app.on_message(filters.photo)
async def handle_photo(client, message: Message):
    if not await is_subscribed(client, message.from_user.id):
        await message.reply_text(
            "**You must join our update channel to use this bot.**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Here", url=f"https://t.me/AniReal_Chat_Group_Asia")]]
            )
        )
        return
    msg = await message.reply("Processing image into sticker...")
    file = await message.download()
    with open(file, "rb") as f:
        webp_file = await convert_to_sticker(f.read())
    await message.reply_sticker(sticker=webp_file)
    await msg.delete()

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    if not await is_subscribed(client, message.from_user.id):
        await message.reply_text(
            "**You must join our update channel to use this bot.**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Here", url=f"https://t.me/{UPDATE_CHANNEL}")]]
            )
        )
        return

    await message.reply_photo(
        photo="https://example.com/start.jpg",  # Replace with your image URL
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
            [
                InlineKeyboardButton("Join Here", url=f"https://t.me/AniReal_Anime_Zone")
            ]
        ])
    )

# /create_own_bot command
@app.on_message(filters.command("create_own_bot") & filters.private)
async def custom_create_bot_handler(client, message: Message):
    await message.reply_text(
        "👋Hello Due! This is a Paid Bot.\n\n"
        "**Create Your Own Bot, Talk My Senpai:** [@AniReal_Support](https://t.me/AniReal_Support)",
        disable_web_page_preview=True
    )

# About & Help button callbacks
@app.on_callback_query()
async def callback_handler(client, callback_query):
    data = callback_query.data
    if data == "about":
        await callback_query.message.reply_text(
            "**About This Bot:**\n\n"
            "This bot converts any image into a Telegram sticker without resizing or compression.\n"
            "Perfect for high-quality stickers.\n\n"
            "**Developer:** [@AniReal_Support](https://t.me/AniReal_Support)",
            disable_web_page_preview=True
        )
    elif data == "help":
        await callback_query.message.reply_text(
            "**How to Use:**\n\n"
            "1. Send me any image.\n"
            "2. I will turn it into a sticker — no crop, no resize.\n"
            "3. Enjoy using your sticker!\n\n"
            "**Features:**\n"
            "- Original size stickers\n"
            "- Force join system\n"
            "- Fast and simple\n\n"
            "Support: [@AniReal_Chat_Group_Asia](https://t.me/AniReal_Chat_Group_Asia)"
        )

# Run both Flask and Telegram bot
if __name__ == "__main__":
    def run_flask():
        port = int(os.environ.get("PORT", 5000))
        flask_app.run(host="0.0.0.0", port=port)

    threading.Thread(target=run_flask).start()
    app.run()
