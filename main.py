import asyncio
from telethon import TelegramClient
from .commands import setup_commands
from .config import load_config
from .forwarder import auto_forwarder

BOT_API_ID = 24565808
BOT_API_HASH = "4eb74502af26e86c3571225a29243e3e"
BOT_TOKEN = "your_bot_token_here"

config = load_config()

bot = TelegramClient("bot_controller", BOT_API_ID, BOT_API_HASH).start(bot_token=BOT_TOKEN)
setup_commands(bot)

async def start_all():
    await bot.start()
    tasks = [asyncio.create_task(auto_forwarder(session)) for session in config["accounts"]]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_all())
