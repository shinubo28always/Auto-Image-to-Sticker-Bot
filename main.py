import os import threading from io import BytesIO from flask import Flask from PIL import Image from pyrogram import Client, filters from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

app = Flask(name)

API_ID = int(os.getenv("API_ID", "")) API_HASH = os.getenv("API_HASH", "") BOT_TOKEN = os.getenv("BOT_TOKEN", "") FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL", "")

START_IMG = "https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg" START_MSG = """ Hey! I'm an Image to Sticker Bot

Send me any photo, and I'll turn it into a sticker without resizing.

Made with love by @AniReal_Support """

REPLY_TEXT = "👋 Hey Dear.. This is a Paid Bot, Create Your Own Bot to Message Here:- @AniReal_Support" JOIN_CHANNEL = "https://t.me/AniReal_Anime_Zone"

bot = Client("AutoStickerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.route('/') def home(): return "Bot is running."

@bot.on_message(filters.command("start") & filters.private) async def start(client: Client, message: Message): if FORCE_SUB_CHANNEL: try: user = await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id) if user.status not in ["member", "administrator", "creator"]: raise Exception("Not a member") except: try: await message.reply_photo( photo=START_IMG, caption="Please Join My Updates Channel to Use Me", reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("Join Channel", url=JOIN_CHANNEL)] ]) ) return except: return

await message.reply_photo(
    photo=START_IMG,
    caption=START_MSG,
    reply_markup=InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Help", callback_data="help"),
            InlineKeyboardButton("About", callback_data="about")
        ]
    ])
)

@bot.on_callback_query() async def cb_handler(client: Client, query: CallbackQuery): if query.data == "help": await query.message.edit_caption( caption="Send me a photo and I'll convert it into a full-size sticker!", reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("Back", callback_data="start")] ]) ) elif query.data == "about": await query.message.edit_caption( caption="Bot by @AniReal_Support\nUses Pyrogram & PIL for high quality sticker conversion.", reply_markup=InlineKeyboardMarkup([ [InlineKeyboardButton("Back", callback_data="start")] ]) ) elif query.data == "start": await query.message.edit_caption( caption=START_MSG, reply_markup=InlineKeyboardMarkup([ [ InlineKeyboardButton("Help", callback_data="help"), InlineKeyboardButton("About", callback_data="about") ] ]) )

@bot.on_message(filters.private & filters.photo) async def convert_to_sticker(client: Client, message: Message): if message.from_user.is_bot: return photo = await message.download() img = Image.open(photo).convert("RGBA") output = BytesIO() output.name = "sticker.webp" img.save(output, format="WEBP") output.seek(0) await message.reply_sticker(sticker=output)

threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))).start()

bot.run()

