import os from pyrogram import Client, filters from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message from PIL import Image from io import BytesIO from flask import Flask import threading

Flask app for Render health check

flask_app = Flask(name)

@flask_app.route('/') def home(): return "Bot is running"

Telegram bot credentials from environment variables

API_ID = int(os.environ.get("API_ID", 0)) API_HASH = os.environ.get("API_HASH", "") BOT_TOKEN = os.environ.get("BOT_TOKEN", "") FORCE_JOIN = os.environ.get("FORCE_JOIN", "https://t.me/+i9H909Qg9M5lMzE9") JOIN_CHANNEL = os.environ.get("JOIN_CHANNEL", "@AniReal_Anime_Zone")

Initialize Pyrogram Client

app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

Function to convert image to sticker

async def convert_to_sticker(image_bytes): img = Image.open(BytesIO(image_bytes)).convert("RGBA") webp_io = BytesIO() img.save(webp_io, format="WEBP") webp_io.name = "sticker.webp" webp_io.seek(0) return webp_io

Force join check

async def is_user_joined(client, user_id): try: member = await client.get_chat_member(FORCE_JOIN, user_id) return member.status in ["member", "administrator", "creator"] except: return False

Handler for /start command

@app.on_message(filters.command("start") & filters.private) async def start_handler(client, message: Message): if not await is_user_joined(client, message.from_user.id): buttons = InlineKeyboardMarkup([ [InlineKeyboardButton("Request Channel", url=FORCE_JOIN)], [InlineKeyboardButton("Try Again", callback_data="refresh")] ]) await message.reply_text( "You must join the update channel to use this bot.", reply_markup=buttons ) return

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("About", callback_data="about"),
        InlineKeyboardButton("Help", callback_data="help")
    ],
    [InlineKeyboardButton("Join Here", url="https://t.me/AniReal_Anime_Zone")]
])

await message.reply_photo(
    photo="https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg",
    caption=(
        "\uD83D\uDC4B **Hey there!**\n\n"
        "\uD83D\uDCF8 **Just send me any photo — and I’ll turn it into a Telegram sticker while keeping its original size.**\n\n"
        "❌ **No crop.** ❌ **No compression.** ✅ **Just perfect stickers.**\n\n"
        "⚡️ **Fast. Simple. Beautiful.**\n\n"
        "🔗 **Support:** [@AniReal_Support](https://t.me/AniReal_Support)"
    ),
    reply_markup=buttons
)

Callback query handler for buttons

@app.on_callback_query() async def callback_handler(client, callback_query): data = callback_query.data

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
        disable_web_page_preview=True
    )
elif data == "help":
    await callback_query.message.edit_text(
        "🆘 **How to Use This Bot**\n\n"
        "Using this bot is super simple:\n\n"
        "1️⃣ **Send me any photo**  \n"
        "I’ll convert it into a Telegram sticker — while keeping its original size and quality.\n\n"
        "2️⃣ **Get your sticker instantly!**  \n"
        "No crop. No compression. Just perfect HD stickers.\n\n"
        "💡 **Tips:**\n"
        "• Use clear images for best sticker results  \n"
        "• Avoid screenshots with borders\n\n"
        "❓ **Need support or want your own bot?**  \n"
        "Message: [@AniReal_Support](https://t.me/AniReal_Support)",
        disable_web_page_preview=True
    )
elif data == "refresh":
    await start_handler(client, callback_query.message)

Handler for incoming photos

@app.on_message(filters.photo & filters.private) async def handle_photo(client, message: Message): if not await is_user_joined(client, message.from_user.id): buttons = InlineKeyboardMarkup([ [InlineKeyboardButton("Request Channel", url=FORCE_JOIN)], [InlineKeyboardButton("Try Again", callback_data="refresh")] ]) await message.reply_text( "You must join the update channel to use this bot.", reply_markup=buttons ) return

msg = await message.reply("Processing image into sticker...")
file = await message.download()
with open(file, "rb") as f:
    webp_file = await convert_to_sticker(f.read())
await message.reply_sticker(sticker=webp_file)
await msg.delete()

Custom command

@app.on_message(filters.command("create_own_bot") & filters.private) async def create_own_bot(client, message: Message): await message.reply_text( "👋 Hey Dear.. This is an Paid Bot, Create Your Own Bot to Massage Here:- @AniReal_Support" )

Run both Flask app and Telegram bot

if name == "main": def run_flask(): port = int(os.environ.get("PORT", 5000)) flask_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()
app.run()
