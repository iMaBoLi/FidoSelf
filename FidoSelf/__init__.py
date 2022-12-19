from telethon import TelegramClient
from telethon.sessions import StringSession
from FidoSelf import config
import time

START_TIME = time.time()

client = TelegramClient(
    StringSession(str(config.SESSION)),
    config.API_ID,
    config.API_HASH,
).start()

client.bot = TelegramClient(
    "SelfBot",
    config.API_ID,
    config.API_HASH,
).start(bot_token=config.BOT_TOKEN)
