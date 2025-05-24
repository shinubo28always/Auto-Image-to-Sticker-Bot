import os
import threading
from io import BytesIO
from flask import Flask
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
START_IMG = "https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg"
JOIN_CHANNEL = "AniReal_Anime_Zone"

app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# Convert image to sticker
async def convert_to_sticker(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    webp_io = BytesIO()
    img.save(webp_io, format="WEBP")
    webp_io.name = "sticker.webp"
    webp_io.seek(0)
    return webp_io

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Help", callback_data="help")
        ],
        [InlineKeyboardButton("Join Here", url=f"https://t.me/{JOIN_CHANNEL}")]
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

# Callback queries (About, Help, Back)
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data
    if data == "about":
        await callback_query.message.edit_caption(
            caption=(
                "🤖 **Bot Information**\n\n"
                "Welcome to the **Auto Image to Sticker Bot**!\n\n"
                "🖼️ Instantly convert your photos into Telegram stickers — without resizing or compression.\n\n"
                "✨ **Features:**\n"
                "• Full-size image stickers\n"
                "• No quality loss\n"
                "• Super fast response\n"
                "• Easy to use\n\n"
                "👨‍💻 **Developer:** [@AniReal_Support](https://t.me/AniReal_Support)"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="start")]
            ])
        )
    elif data == "help":
        await callback_query.message.edit_caption(
            caption=(
                "🆘 **How to Use This Bot**\n\n"
                "1️⃣ **Send me any photo**\n"
                "I'll convert it into a Telegram sticker with full quality.\n\n"
                "2️⃣ **Get your sticker instantly!**\n"
                "No crop. No compression. Just perfect HD stickers.\n\n"
                "💡 **Tips:**\n"
                "• Use clear images for best results\n"
                "• Avoid screenshots with borders\n\n"
                "❓ Need help? Contact: [@AniReal_Support](https://t.me/AniReal_Support)"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="start")]
            ])
        )
    elif data == "start":
        await start_handler(client, callback_query.message)

# Convert photo to sticker
@app.on_message(filters.photo & filters.private)
async def photo_to_sticker(client, message):
    try:
        photo = await message.download()
        img = Image.open(photo).convert("RGBA")
        output = BytesIO()
        output.name = "sticker.webp"
        img.save(output, "WEBP")
        output.seek(0)
        await message.reply_sticker(output)
    except Exception as e:
        await message.reply_text("Something went wrong:\n" + str(e))

# Custom command
@app.on_message(filters.command("create_own_bot") & filters.private)
async def create_own_bot(client, message):
    await message.reply_text(
        "👋 Hey Dear.. This is an Paid Bot, Create Your Own Bot to Massage Here:- @AniReal_Support"
    )

# Start Flask and bot
if __name__ == "__main__":
    def run_flask():
        port = int(os.environ.get("PORT", 5000))
        flask_app.run(host="0.0.0.0", port=port)

    threading.Thread(target=run_flask).start()
    app.run()
