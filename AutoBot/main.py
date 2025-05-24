import os
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import API_ID, API_HASH, BOT_TOKEN, START_IMG_URL, FORCE_JOIN
from handlers import start, help, about, callback
from pyrogram import filters
from PIL import Image
from io import BytesIO

app = Client("autobot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    user = message.from_user.id

    # Force join check
    if FORCE_JOIN:
        try:
            await client.get_chat_member(FORCE_JOIN, user)
        except UserNotParticipant:
            return await message.reply(
                f"**Join the channel to use me!**",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{FORCE_JOIN}")]]
                )
            )

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Add to Group", url=f"https://t.me/{client.me.username}?startgroup=true")],
            [
                InlineKeyboardButton("Help", callback_data="help_cb"),
                InlineKeyboardButton("About", callback_data="about_cb")
            ]
        ]
    )
    await message.reply_photo(
        photo=START_IMG_URL,
        caption="**Hey! I'm an Image to Sticker Bot**\nSend me any image, and I’ll convert it to a sticker without resizing.",
        reply_markup=buttons
    )

@app.on_message(filters.photo & filters.private)
async def photo_to_sticker(client, message):
    photo = await message.download()
    with Image.open(photo) as img:
        img = img.convert("RGBA")
        bio = BytesIO()
        bio.name = "sticker.webp"
        img.save(bio, "webp")
        bio.seek(0)
        await message.reply_sticker(bio)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
