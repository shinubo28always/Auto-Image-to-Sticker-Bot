from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

ABOUT_TEXT = """
**About This Bot**  
Made with Pyrogram  
Maintained by @AniReal_Support  
Source: [GitHub](https://github.com/shinubo28always/Auto-Image-to-Sticker-Bot)
"""

BACK_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Back", callback_data="back_cb")]]
)

@Client.on_message(filters.command("about"))
async def about_command(client, message: Message):
    await message.reply_text(
        ABOUT_TEXT,
        reply_markup=BACK_BUTTON
    )
