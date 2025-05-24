from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import START_IMG_URL, FORCE_SUB_CHANNEL

START_TEXT = """
**Hey! I'm an Image to Sticker Bot**  
Just send me any image and I’ll convert it into a sticker **without resizing!**
"""

START_BUTTON = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Add to Group", url="https://t.me/YourBotUsername?startgroup=true")],
        [
            InlineKeyboardButton("Help", callback_data="help_cb"),
            InlineKeyboardButton("About", callback_data="about_cb")
        ]
    ]
)

HELP_TEXT = """
**Help Section**  
- Just send an image, and I'll convert it to a sticker.  
- No need to crop or resize, full-size sticker will be created.
"""

ABOUT_TEXT = """
**About This Bot**  
Made with Pyrogram  
Maintained by @AniReal_Support  
Source: [GitHub](https://github.com/shinubo28always/Auto-Image-to-Sticker-Bot)
"""

BACK_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Back", callback_data="back_cb")]]
)


@Client.on_message(filters.command("start"))
async def start(client, message: Message):
    if FORCE_SUB_CHANNEL:
        try:
            user = await client.get_chat_member(FORCE_SUB_CHANNEL, message.from_user.id)
            if user.status not in ("member", "administrator", "creator"):
                invite_link = await client.create_chat_invite_link(FORCE_SUB_CHANNEL)
                return await message.reply_text(
                    "**Join our channel first to use this bot.**",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Join Channel", url=invite_link.invite_link)]]
                    )
                )
        except:
            pass

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=START_TEXT,
        reply_markup=START_BUTTON
    )


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    if query.data == "help_cb":
        await query.message.edit_text(
            HELP_TEXT,
            reply_markup=BACK_BUTTON
        )

    elif query.data == "about_cb":
        await query.message.edit_text(
            ABOUT_TEXT,
            reply_markup=BACK_BUTTON
        )

    elif query.data == "back_cb":
        await query.message.edit_photo(
            photo=START_IMG_URL,
            caption=START_TEXT,
            reply_markup=START_BUTTON
        )
