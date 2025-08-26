import asyncio
import random
import os
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from .config import ACCOUNTS_DIR, load_config

BOT_API_ID = 24565808
BOT_API_HASH = "4eb74502af26e86c3571225a29243e3e"

config = load_config()

async def auto_forwarder(session_name):
    session_path = os.path.join(ACCOUNTS_DIR, f"{session_name}.session")
    client = TelegramClient(session_path, BOT_API_ID, BOT_API_HASH)
    await client.start()

    while True:
        try:
            messages = await client(GetHistoryRequest(peer='me', limit=20, offset_id=0,
                                                      max_id=0, min_id=0, add_offset=0, hash=0))
            if not messages.messages:
                await asyncio.sleep(60)
                continue

            msg = random.choice(messages.messages)
            for group_id in config["groups"]:
                try:
                    await client.forward_messages(group_id, msg)
                    print(f"[{session_name}] Forwarded to {group_id}")
                except Exception as e:
                    print(f"[{session_name}] Forward failed: {e}")

            await asyncio.sleep(random.randint(60, 300))
        except Exception as e:
            print(f"[{session_name}] Error: {e}")
            await asyncio.sleep(120)
