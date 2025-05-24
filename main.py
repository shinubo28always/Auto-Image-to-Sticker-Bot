import os from pyrogram import Client, filters from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery from PIL import Image from io import BytesIO from flask import Flask import threading

Flask for Render health check

flask_app = Flask(name)

@flask_app.route('/') def home(): return "Bot is running"

Telegram credentials

API_ID = int(os.environ.get("API_ID", 0)) API_HASH = os.environ.get("API_HASH", "") BOT_TOKEN = os.environ.get("BOT_TOKEN", "") FORCE_JOIN = "https://t.me/+i9H909Qg9M5lMzE9"  # Private join channel JOIN_CHANNEL = "https://t.me/AniReal_Anime_Zone"  # Public channel button link

Pyrogram bot

app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

Convert image to sticker

async def convert_to_sticker(image_bytes): img = Image.open(BytesIO(image_bytes)).convert("RGBA") webp_io = BytesIO() img.save(webp_io, format="WEBP") webp_io.name = "sticker.webp" webp_io.seek(0) return webp_io

Force Join Check

async def check_force_join(client, message): try: user = await client.get_chat_member(FORCE_JOIN, message.from_user.id) if user.status in ("kicked", "left"): raise Exception except: buttons = InlineKeyboardMarkup([ [InlineKeyboardButton("Join Request Channel", url=FORCE_JOIN)], [InlineKeyboardButton("Try Again", callback_data="retry_join")] ]) await message.reply("You must join the channel to use this bot.", reply_markup=buttons) return False return True

Start command

@app.on_message(filters.command("start") & filters.private) async def start_cmd(client, message: Message): if not await check_force_join(client, message): return

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("About", callback_data="about"),
        InlineKeyboardButton("Help", callback_data="help")
    ],
    [InlineKeyboardButton("Join Here", url=JOIN_CHANNEL)]
])

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

Retry button callback

@app.on_callback_query(filters.regex("retry_join")) async def retry_join(client, callback_query: CallbackQuery): await callback_query.message.delete() await start_cmd(client, callback_query.message)

About and Help callbacks

@app.on_callback_query(filters.regex("about")) async def about_callback(client, callback_query: CallbackQuery): await callback_query.message.edit_text( "🤖 Bot Information\n\n" "Welcome to the Auto Image to Sticker Bot!\n\n" "🖼️ This bot instantly converts your photos into Telegram stickers — without resizing, cropping, or compression.\n\n" "✨ Features:\n" "• Full-size image stickers\n" "• No quality loss\n" "• Super fast response\n" "• Easy to use\n\n" "👨‍💻 Developer: @AniReal_Support", disable_web_page_preview=True )

@app.on_callback_query(filters.regex("help")) async def help_callback(client, callback_query: CallbackQuery): await callback_query.message.edit_text( "🆘 How to Use This Bot\n\n" "Using this bot is super simple:\n\n" "1️⃣ Send me any photo\nI’ll convert it into a Telegram sticker — while keeping its original size and quality.\n\n" "2️⃣ Get your sticker instantly!\nNo crop. No compression. Just perfect HD stickers.\n\n" "💡 Tips:\n• Use clear images for best sticker results\n• Avoid screenshots with borders\n\n" "❓ Need support or want your own bot?\nMessage: @AniReal_Support", disable_web_page_preview=True )

Custom command

@app.on_message(filters.command("create_own_bot") & filters.private) async def create_bot(client, message): await message.reply_text("👋 Hey Dear.. This is an Paid Bot, Create Your Own Bot to Massage Here:- @AniReal_Support")

Handle photos

@app.on_message(filters.photo & filters.private) async def handle_photo(client, message: Message): if not await check_force_join(client, message): return msg = await message.reply("Processing image into sticker...") file = await message.download() with open(file, "rb") as f: webp_file = await convert_to_sticker(f.read()) await message.reply_sticker(sticker=webp_file) await msg.delete()

Run Flask + Bot

if name == 'main': def run_flask(): port = int(os.environ.get("PORT", 5000)) flask_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()
app.run()

