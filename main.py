import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import UserNotParticipant

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
FORCE_JOIN = "https://t.me/+i9H909Qg9M5lMzE9"
START_IMAGE = "https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg"
CUSTOM_REPLY = "ðŸ‘‹ Hey Dear.. This is a Paid Bot, Create Your Own Bot to Message Here:- @AniReal_Support"

app = Client("ImageToStickerBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("ðŸ“Œ About", callback_data="about"),
            InlineKeyboardButton("â“ Help", callback_data="help")
        ],
        [InlineKeyboardButton("ðŸ”— Join Here", url=https://t.me/AniReal_Anime_Zone)]
    ])

async def is_user_joined(client, user_id):
    try:
        await client.get_chat_member(FORCE_JOIN, user_id)
        return True
    except UserNotParticipant:
        return False

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    if not await is_user_joined(client, message.from_user.id):
        return await message.reply_photo(
            START_IMAGE,
            caption="ðŸ”’ Please join our update channel to use this bot.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ðŸ”— Join Here", url=https://t.me/+i9H909Qg9M5lMzE9)]])
        )
    await message.reply_photo(
        START_IMAGE,
        caption="ðŸ‘‹ **Hey there!**

ðŸ“¸ **Just send me any image and Iâ€™ll convert it into a sticker** â€” without resizing or quality loss.",
        reply_markup=get_start_buttons()
    )

@app.on_message(filters.command("create_own_bot"))
async def own_bot(client, message: Message):
    await message.reply_text(CUSTOM_REPLY)

@app.on_callback_query(filters.regex("about"))
async def about_callback(client, callback_query: CallbackQuery):
    text = """ðŸ¤– **Bot Information**

Welcome to the **Auto Image to Sticker Bot**!

ðŸ–¼ï¸ This bot instantly converts your photos into Telegram stickers â€” without **resizing**, **cropping**, or **compression**.

âœ¨ **Features:**
â€¢ Full-size image stickers
â€¢ No quality loss
â€¢ Super fast response
â€¢ Easy to use

ðŸ‘¨â€ðŸ’» **Developer:** [@AniReal_Support](https://t.me/AniReal_Support)
"""
    await callback_query.message.edit_text(text, disable_web_page_preview=True, reply_markup=get_start_buttons())

@app.on_callback_query(filters.regex("help"))
async def help_callback(client, callback_query: CallbackQuery):
    text = """ðŸ†˜ **How to Use This Bot**

Using this bot is super simple:

1ï¸âƒ£ **Send me any photo**  
Iâ€™ll convert it into a Telegram sticker â€” while keeping its original size and quality.

2ï¸âƒ£ **Get your sticker instantly!**  
No crop. No compression. Just perfect HD stickers.

ðŸ’¡ **Tips:**
â€¢ Use clear images for best sticker results  
â€¢ Avoid screenshots with borders

â“ **Need support or want your own bot?**  
Message: [@AniReal_Support](https://t.me/AniReal_Support)
"""
    await callback_query.message.edit_text(text, disable_web_page_preview=True, reply_markup=get_start_buttons())

@app.on_message(filters.photo)
async def image_to_sticker(client, message: Message):
    if not await is_user_joined(client, message.from_user.id):
        return await message.reply_text("ðŸ”’ You must join our update channel to use this bot.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ðŸ”— Join Here", url=FORCE_JOIN)]]))
    await message.reply_sticker(message.photo.file_id)

app.run()
