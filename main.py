import os import threading from io import BytesIO from flask import Flask from PIL import Image from pyrogram import Client, filters from pyrogram.types import ( InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery )

Flask app for Render health check

flask_app = Flask(name)

@flask_app.route('/') def home(): return "Bot is running!"

API_ID = int(os.environ.get("API_ID", 0)) API_HASH = os.environ.get("API_HASH", "") BOT_TOKEN = os.environ.get("BOT_TOKEN", "") FORCE_JOIN = os.environ.get("FORCE_JOIN", "")  # Private Channel JOIN_CHANNEL = "AniReal_Anime_Zone"  # Public Channel START_IMG = "https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg"

app = Client("img-to-sticker-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def is_subscribed(client, user_id): try: member = await client.get_chat_member(FORCE_JOIN, user_id) return member.status in ("member", "administrator", "creator") except: return False

@app.on_message(filters.command("start") & filters.private) async def start_handler(client: Client, message: Message): if FORCE_JOIN: if not await is_subscribed(client, message.from_user.id): buttons = InlineKeyboardMarkup([ [InlineKeyboardButton("Request to Join", url=f"https://t.me/{FORCE_JOIN.replace('@', '')}")], [InlineKeyboardButton("Try Again", callback_data="check_subscribe")] ]) await message.reply_text("\ud83d\udd10 You must join the update channel to use this bot.", reply_markup=buttons) return

buttons = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("About", callback_data="about"),
        InlineKeyboardButton("Help", callback_data="help")
    ],
    [InlineKeyboardButton("Join Here", url=f"https://t.me/{JOIN_CHANNEL}")]
])
await message.reply_photo(
    photo=START_IMG,
    caption=START_MSG_TEXT,
    reply_markup=buttons
)

START_MSG_TEXT = ( "\ud83d\udc4b Hey there!\n\n" "\ud83d\udcf8 Just send me any photo — and I’ll turn it into a Telegram sticker while keeping its original size.\n\n" "\u274c No crop. \u274c No compression. \u2705 Just perfect stickers.\n\n" "\u26a1\ufe0f Fast. Simple. Beautiful.\n\n" "\ud83d\udd17 Support: @AniReal_Support" )

@app.on_callback_query() async def callback_handler(client: Client, query: CallbackQuery): if query.data == "check_subscribe": if await is_subscribed(client, query.from_user.id): await query.message.delete() await start_handler(client, query.message) else: await query.answer("\u274c You're still not joined!", show_alert=True)

elif query.data == "about":
    await query.message.edit_text(
        "\ud83e\udd16 **Bot Information**\n\n"
        "Welcome to the **Auto Image to Sticker Bot**!\n\n"
        "\ud83d\uddbc\ufe0f Instantly convert your photos into Telegram stickers — without resizing or compression.\n\n"
        "\u2728 **Features:**\n"
        "• Full-size image stickers\n"
        "• No quality loss\n"
        "• Super fast response\n"
        "• Easy to use\n\n"
        "\ud83d\udc68‍\ud83d\udcbb **Developer:** [@AniReal_Support](https://t.me/AniReal_Support)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Back", callback_data="start")]]
        ),
        disable_web_page_preview=True
    )

elif query.data == "help":
    await query.message.edit_text(
        "\ud83d\ude98 **How to Use This Bot**\n\n"
        "1\ufe0f\u20e3 **Send me any photo**\n"
        "I'll convert it into a Telegram sticker with full quality.\n\n"
        "2\ufe0f\u20e3 **Get your sticker instantly!**\n"
        "No crop. No compression. Just perfect HD stickers.\n\n"
        "\ud83d\udca1 **Tips:**\n"
        "• Use clear images for best results\n"
        "• Avoid screenshots with borders\n\n"
        "\u2753 Need help? Contact: [@AniReal_Support](https://t.me/AniReal_Support)",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Back", callback_data="start")]]
        ),
        disable_web_page_preview=True
    )

elif query.data == "start":
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("About", callback_data="about"),
            InlineKeyboardButton("Help", callback_data="help")
        ],
        [InlineKeyboardButton("Join Here", url=f"https://t.me/{JOIN_CHANNEL}")]
    ])
    await query.message.edit_media(
        media=query.message.photo,
        reply_markup=buttons
    )
    await query.message.edit_caption(START_MSG_TEXT, reply_markup=buttons)

@app.on_message(filters.photo & filters.private) async def handle_photo(client, message): try: photo = await message.download() img = Image.open(photo).convert("RGBA") webp_io = BytesIO() webp_io.name = "sticker.webp" img.save(webp_io, format="WEBP") webp_io.seek(0) await message.reply_sticker(webp_io) except Exception as e: await message.reply_text("Something went wrong:\n" + str(e))

@app.on_message(filters.command("create_own_bot") & filters.private) async def own_bot_cmd(client, message): await message.reply_text("\ud83d\udc4b Hey Dear.. This is a Paid Bot, Create Your Own Bot to Message Here:- @AniReal_Support")

if name == 'main': def run_flask(): port = int(os.environ.get("PORT", 5000)) flask_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()
app.run()

