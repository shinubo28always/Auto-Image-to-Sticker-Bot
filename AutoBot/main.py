from pyrogram import Client
from handlers import start, callback

app = Client("my_bot")

start.register_handlers(app)
callback.register_callbacks(app)

app.run()
