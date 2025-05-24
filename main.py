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

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is running!"

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
FORCE_JOIN = os.environ.get("FORCE_JOIN", "+9Fo0r2Wngqk0YTBl")
JOIN_CHANNEL = "AniReal_Anime_Zone"
START_IMG = "https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg"

app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

async def convert_to_sticker(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    output = BytesIO()
    output.name = "sticker.webp"
    img.save(output, "WEBP")
    output.seek(0)
    return output

async def is_subscribed(client, user_id):
    try:
        member = await client.get_chat_member(FORCE_JOIN, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def start_markup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Help", callback_data="help")
        ],
        [InlineKeyboardButton("Join Here", url=f"https://t.me/{JOIN_CHANNEL}")]
    ])

def back_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Back to Home", callback_data="home")]
    ])

@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message: Message):
    if FORCE_JOIN and not await is_subscribed(client, message.from_user.id):
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Request to Join", url=f"https://t.me/{FORCE_JOIN.replace('@', '')}")],
            [InlineKeyboardButton("Try Again", callback_data="check_subscribe")]
        ])
        return await message.reply_text("🔒 **You must join the update channel to use this bot.**", reply_markup=buttons)

    await message.reply_photo(
        photo=START_IMG,
        caption=(
            "👋 **Hey there!**\n\n"
            "📸 **Send me a photo & I'll turn it into a full-quality sticker!**\n"
            "❌ No crop. ❌ No compression. ✅ Just clean HD stickers.\n\n"
            "⚡️ **Fast. Simple. Beautiful.**\n\n"
            "🔗 **Support:** [@AniReal_Support](https://t.me/AniReal_Support)"
        ),
        reply_markup=start_markup()
    )

@app.on_callback_query()
async def callback_query_handler(client: Client, callback_query: CallbackQuery):
    data = callback_query.data
    if data == "check_subscribe":
        if await is_subscribed(client, callback_query.from_user.id):
            await callback_query.message.delete()
            await start_handler(client, callback_query.message)
        else:
            await callback_query.answer("❌ You're still not joined!", show_alert=True)

    elif data == "about":
        await callback_query.message.edit_caption(
            caption=(
                "🤖 **Bot Information**\n\n"
                "Welcome to the **Auto Image to Sticker Bot**!\n\n"
                "🖼️ Convert your images into Telegram stickers without resizing or compression.\n"
                "✨ Full quality stickers, lightning fast.\n\n"
                "👨‍💻 Developer: [@AniReal_Support](https://t.me/AniReal_Support)"
            ),
            reply_markup=back_markup()
        )

    elif data == "help":
        await callback_query.message.edit_caption(
            caption=(
                "🆘 **How to Use This Bot**\n\n"
                "1️⃣ Send a photo\n"
                "2️⃣ Get HD sticker instantly\n\n"
                "💡 Tip: Avoid screenshots for best results.\n\n"
                "Need help? Contact: [@AniReal_Support](https://t.me/AniReal_Support)"
            ),
            reply_markup=back_markup()
        )

    elif data == "home":
        await callback_query.message.edit_caption(
            caption=(
                "👋 **Hey there!**\n\n"
                "📸 **Send me a photo & I'll turn it into a full-quality sticker!**\n"
                "❌ No crop. ❌ No compression. ✅ Just clean HD stickers.\n\n"
                "⚡️ **Fast. Simple. Beautiful.**\n\n"
                "🔗 **Support:** [@AniReal_Support](https://t.me/AniReal_Support)"
            ),
            reply_markup=start_markup()
        )

@app.on_message(filters.photo & filters.private)
async def photo_to_sticker(client, message):
    if message.from_user.is_self:
        return
    msg = await message.reply("Processing image into sticker...")
    file = await message.download()
    with open(file, "rb") as f:
        sticker = await convert_to_sticker(f.read())
    await message.reply_sticker(sticker)
    await msg.delete()

@app.on_message(filters.command("create_own_bot") & filters.private)
async def create_own_bot(client, message):
    await message.reply_text(
        "👋 Hey Dear.. This is a Paid Bot, Create Your Own Bot to Message Here:- @AniReal_Support"
    )

if __name__ == "__main__":
    def run_flask():
        port = int(os.environ.get("PORT", 5000))
        flask_app.run(host="0.0.0.0", port=port)

    threading.Thread(target=run_flask).start()
    app.run()
