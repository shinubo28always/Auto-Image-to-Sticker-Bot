import os
import threading
from io import BytesIO
from PIL import Image
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import Message

# Flask app for Render health check
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running"

# Telegram bot credentials
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Initialize Pyrogram Client
app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Start Flask app in a separate thread
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# Function to convert image to sticker (without resizing)
async def convert_to_sticker(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    webp_io = BytesIO()
    img.save(webp_io, format="WEBP")
    webp_io.name = "sticker.webp"
    webp_io.seek(0)
    return webp_io

# /start command handler
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply_text(
        "**Hi!**\n\n"
        "Send me any image and I will convert it into a Telegram sticker — *without resizing*.\n\n"
        "Bot by: [@AniReal_Support](https://t.me/AniReal_Support)",
        disable_web_page_preview=True
    )

# Photo handler
@app.on_message(filters.photo & filters.private)
async def handle_photo(client: Client, message: Message):
    msg = await message.reply("Processing image into sticker...")
    file = await message.download()
    with open(file, "rb") as f:
        webp_file = await convert_to_sticker(f.read())
    await message.reply_sticker(sticker=webp_file)
    await msg.delete()

# Start Pyrogram bot
app.run()
