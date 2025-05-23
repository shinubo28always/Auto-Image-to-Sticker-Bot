import os
from pyrogram import Client, filters
from PIL import Image
from io import BytesIO

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

app = Client("img-to-sticker-bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

async def convert_to_sticker(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert("RGBA")
    webp_io = BytesIO()
    img.save(webp_io, format="WEBP")
    webp_io.name = "sticker.webp"
    webp_io.seek(0)
    return webp_io

@app.on_message(filters.photo)
async def handle_photo(client, message):
    msg = await message.reply("Processing image into sticker...")
    file = await message.download()
    with open(file, "rb") as f:
        webp_file = await convert_to_sticker(f.read())
    await message.reply_sticker(sticker=webp_file)
    await msg.delete()

print("Bot is running...")
app.run()
