from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Bot Information Texts
START_TEXT = """
🤖 <b>Bot Information</b>

Welcome to the <b>Auto Image to Sticker Bot!</b>

🖼️ Instantly convert your photos into Telegram stickers — without resizing or compression.

✨ <b>Features:</b>
• Full-size image stickers
• No quality loss
• Super fast response
• Easy to use

🧑‍💻 <b>Developer:</b> @AniReal_Support
"""

HELP_TEXT = """
❓ <b>Help Guide</b>

1. Just send me a photo.
2. I will convert it into a full-size sticker.
3. No need to crop or resize!

🧑‍💻 <b>Developer:</b> @AniReal_Support
"""

ABOUT_TEXT = """
ℹ️ <b>About This Bot</b>

This bot was made to instantly convert any image into a Telegram sticker without compression.

⚙️ Powered by: Pyrogram

🧑‍💻 <b>Developer:</b> @AniReal_Support
"""

# Inline Buttons
BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Help", callback_data="help"),
        InlineKeyboardButton("About", callback_data="about")
    ],
    [
        InlineKeyboardButton("Back", callback_data="back")
    ]
])

# Start Command
@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text(
        START_TEXT,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

# Help Button Callback
@Client.on_callback_query(filters.regex("help"))
async def help_cb(client, query):
    await query.message.edit_text(
        HELP_TEXT,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

# About Button Callback
@Client.on_callback_query(filters.regex("about"))
async def about_cb(client, query):
    await query.message.edit_text(
        ABOUT_TEXT,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

# Back Button Callback
@Client.on_callback_query(filters.regex("back"))
async def back_cb(client, query):
    await query.message.edit_text(
        START_TEXT,
        reply_markup=BUTTONS,
        disable_web_page_preview=True
    )

# Custom Command: /create_own_bot
@Client.on_message(filters.command("create_own_bot") & filters.private)
async def create_bot(client, message):
    await message.reply_text(
        "👋 Hey Dear.. This is a Paid Bot, Create Your Own Bot to Message Here:- @AniReal_Support"
    )
