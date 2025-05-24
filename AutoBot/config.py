import os

API_ID = int(os.getenv("API_ID", "12345678"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

# Optional force subscribe (channel username or invite link)
FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL", "AniReal_Anime_Zone")

# Start image URL
START_IMG_URL = os.getenv("START_IMG_URL", "https://graph.org/file/5fb2a9e904ae7870b8862-fb58603ada523ac527.jpg")
