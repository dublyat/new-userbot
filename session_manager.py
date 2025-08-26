import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
    PhoneCodeInvalidError
)
from telethon import events, Button
from .config import ACCOUNTS_DIR, save_config, load_config

BOT_API_ID = 24565808
BOT_API_HASH = "4eb74502af26e86c3571225a29243e3e"

config = load_config()
user_states = {}

async def handle_session_flow(event):
    user_id = event.sender_id
    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state["step"] == "awaiting_phone":
        phone = event.raw_text.strip()
        state["phone"] = phone
        state["session"] = StringSession()
        state["client"] = TelegramClient(state["session"], BOT_API_ID, BOT_API_HASH)

        try:
            await state["client"].connect()
            await state["client"].send_code_request(phone)
            state["step"] = "awaiting_code"
            await event.reply("📨 Code sent! Please enter the **login code**.")
        except PhoneNumberInvalidError:
            await event.reply("❌ Invalid phone number. Please try `/gen` again.")
            user_states.pop(user_id)
        except Exception as e:
            await event.reply(f"❌ Error: {e}")
            user_states.pop(user_id)

    elif state["step"] == "awaiting_code":
        code = event.raw_text.strip()
        phone = state["phone"]
        try:
            await state["client"].sign_in(phone=phone, code=code)
            await finalize_session(user_id, event)
        except SessionPasswordNeededError:
            state["step"] = "awaiting_password"
            await event.reply("🔐 2FA enabled. Please enter your **password**.")
        except PhoneCodeInvalidError:
            await event.reply("❌ Invalid code. Please try `/gen` again.")
            user_states.pop(user_id)
        except Exception as e:
            await event.reply(f"❌ Error: {e}")
            user_states.pop(user_id)

    elif state["step"] == "awaiting_password":
        password = event.raw_text.strip()
        try:
            await state["client"].sign_in(password=password)
            await finalize_session(user_id, event)
        except Exception as e:
            await event.reply(f"❌ 2FA failed: {e}")
            user_states.pop(user_id)

async def finalize_session(user_id, event):
    state = user_states[user_id]
    client = state["client"]
    session_string = client.session.save()

    me = await client.get_me()
    session_name = f"{me.id}_{me.username or 'user'}"
    session_path = os.path.join(ACCOUNTS_DIR, f"{session_name}.session")

    with open(session_path, "wb") as f:
        client.session.save(f)

    if session_name not in config["accounts"]:
        config["accounts"].append(session_name)
        save_config(config)

    await client.disconnect()
    user_states.pop(user_id)

    await event.respond(
        f"✅ Session saved for {me.first_name} (@{me.username or 'N/A'})\n\nClick to reveal the string session:",
        buttons=[Button.inline("🔑 Reveal String", data=f"show_string:{session_name}")]
    )

def init_session(user_id):
    user_states[user_id] = {"step": "awaiting_phone"}
