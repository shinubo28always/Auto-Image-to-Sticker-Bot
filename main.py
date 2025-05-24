import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from plugins.image_to_sticker import image_to_sticker
from handlers.start import start_handler, create_own_bot_handler
from handlers.callback import callback_handler
from config import API_ID, API_HASH, BOT_TOKEN

logging.basicConfig(level=logging.INFO)

app = Client(
    "AutoStickerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start(_, message: Message):
    await start_handler(_, message)

# /create_own_bot command
@app.on_message(filters.command("create_own_bot") & filters.private)
async def create_bot(_, message: Message):
    await create_own_bot_handler(_, message)

# Callback button handler
@app.on_callback_query()
async def callback_query_handler(_, callback_query):
    await callback_handler(_, callback_query)

# Handle image messages
@app.on_message(filters.photo & filters.private)
async def handle_image(_, message: Message):
    await image_to_sticker(_, message)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
