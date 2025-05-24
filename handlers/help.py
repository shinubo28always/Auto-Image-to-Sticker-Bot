from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

HELP_TEXT = """
**Help Section**  
- Just send an image, and I'll convert it to a sticker.  
- No need to crop or resize, full-size sticker will be created.
"""

BACK_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Back", callback_data="back_cb")]]
)

@Client.on_message(filters.command("help"))
async def help_command(client, message: Message):
    await message.reply_text(
        HELP_TEXT,
        reply_markup=BACK_BUTTON
    )
