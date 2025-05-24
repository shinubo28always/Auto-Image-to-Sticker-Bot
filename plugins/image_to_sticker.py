from pyrogram import Client, filters
from PIL import Image
from io import BytesIO

@Client.on_message(filters.photo & filters.private)
async def image_to_sticker(client, message):
    photo = await message.download()
    with Image.open(photo) as img:
        img = img.convert("RGBA")
        bio = BytesIO()
        bio.name = "sticker.webp"
        img.save(bio, "webp")
        bio.seek(0)
        await message.reply_sticker(bio)
