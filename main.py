import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from PIL import Image
from io import BytesIO
from flask import Flask
import threading

# Flask app for Render/Cyclic
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "Bot is running!"

# Bot credentials
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
JOIN_CHANNEL = "AniReal_Anime_Zone"  # Without '@'

# Pyrogram Client
app = Client("img-to-sticker-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Convert image to sticker
async def convert_to_sticker(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    webp_io = BytesIO()
    img.save(webp_io, format="WEBP")
    webp_io.name = "sticker.webp"
    webp_io.seek(0)
    return webp_io

# Inline buttons
buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("About", callback_data="about"),
        InlineKeyboardButton("Help", callback_data="help")
    ],
    [InlineKeyboardButton("Join Here", url="https://t.me/AniReal_Anime_Zone")]
])

# /start command with force join check
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    try:
        user = message.from_user.id
        member = await client.get_chat_member(JOIN_CHANNEL, user)
        if member.status not in ["member", "administrator", "creator"]:
            raise Exception("Not a member")
    except:
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{JOIN_CHANNEL}")],
            [InlineKeyboardButton("Refresh", callback_data="refresh")]
        ])
        return await message.reply(
            "**Join the update channel to use this bot.**",
            reply_markup=join_button
        )

    await message.reply_photo(
        photo="https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg",
        caption=(
            "👋 **Hey there!**\n\n"
            "📸 **Just send me any photo — and I’ll turn it into a Telegram sticker while keeping its original size.**\n\n"
            "❌ **No crop.** ❌ **No compression.** ✅ **Just perfect stickers.**\n\n"
            "⚡️ **Fast. Simple. Beautiful.**\n\n"
            "🔗 **Support:** [@AniReal_Support](https://t.me/AniReal_Support)"
        ),
        reply_markup=buttons
    )

# Handle photo message
@app.on_message(filters.photo & filters.private)
async def handle_photo(client, message: Message):
    try:
        user = message.from_user.id
        member = await client.get_chat_member(JOIN_CHANNEL, user)
        if member.status not in ["member", "administrator", "creator"]:
            raise Exception("Not a member")
    except:
        join_button = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=f"https://t.me/{JOIN_CHANNEL}")],
            [InlineKeyboardButton("Refresh", callback_data="refresh")]
        ])
        return await message.reply("**Please join the update channel to use this bot.**", reply_markup=join_button)

    msg = await message.reply("Processing image into sticker...")
    file = await message.download()
    with open(file, "rb") as f:
        sticker = await convert_to_sticker(f.read())
    await message.reply_sticker(sticker=sticker)
    await msg.delete()

# /create_own_bot command
@app.on_message(filters.command("create_own_bot") & filters.private)
async def create_bot(client, message: Message):
    await message.reply_text(
        "👋 Hey Dear.. This is an Paid Bot, Create Your Own Bot to Message Here:- @AniReal_Support"
    )

# CallbackQuery handler
@app.on_callback_query()
async def callback_handler(client, callback_query: CallbackQuery):
    data = callback_query.data
    if data == "about":
        await callback_query.message.edit_text(
            "🤖 **Bot Information**\n\n"
            "Welcome to the **Auto Image to Sticker Bot**!\n\n"
            "🖼️ This bot instantly converts your photos into Telegram stickers — without **resizing**, **cropping**, or **compression**.\n\n"
            "✨ **Features:**\n"
            "• Full-size image stickers\n"
            "• No quality loss\n"
            "• Super fast response\n"
            "• Easy to use\n\n"
            "👨‍💻 **Developer:** [@AniReal_Support](https://t.me/AniReal_Support)",
            disable_web_page_preview=True,
            reply_markup=buttons
        )
    elif data == "help":
        await callback_query.message.edit_text(
            "🆘 **How to Use This Bot**\n\n"
            "Using this bot is super simple:\n\n"
            "1️⃣ **Send me any photo**\n"
            "I’ll convert it into a Telegram sticker — while keeping its original size and quality.\n\n"
            "2️⃣ **Get your sticker instantly!**\n"
            "No crop. No compression. Just perfect HD stickers.\n\n"
            "💡 **Tips:**\n"
            "• Use clear images for best sticker results\n"
            "• Avoid screenshots with borders\n\n"
            "❓ **Need support or want your own bot?**\n"
            "Message: [@AniReal_Support](https://t.me/AniReal_Support)",
            disable_web_page_preview=True,
            reply_markup=buttons
        )
    elif data == "refresh":
        await start_command(client, callback_query.message)

# Run bot and Flask app together
if __name__ == "__main__":
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))).start()
    app.run()
