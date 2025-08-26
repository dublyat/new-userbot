from telethon import events, Button
from .config import load_config, save_config, ACCOUNTS_DIR
from .session_manager import handle_session_flow, init_session

config = load_config()
admins = config.get("admins", [])

def setup_commands(bot):

    @bot.on(events.NewMessage(pattern="/start"))
    async def start(event):
        if event.sender_id not in admins:
            return await event.reply("🚫 You are not authorized.")
        await event.reply("✅ Welcome!\nCommands:\n- /gen\n- /addgroup\n- /removegroup")

    @bot.on(events.NewMessage(pattern="/gen"))
    async def gen(event):
        if event.sender_id not in admins:
            return await event.reply("🚫 Not authorized.")
        init_session(event.sender_id)
        await event.respond("📞 Enter your **phone number** (with country code).", buttons=Button.clear())

    @bot.on(events.NewMessage())
    async def generic_handler(event):
        await handle_session_flow(event)

    @bot.on(events.CallbackQuery(data=lambda d: d.decode().startswith("show_string:")))
    async def reveal(event):
        if event.sender_id not in admins:
            return await event.answer("🚫 Not authorized.", alert=True)

        session_key = event.data.decode().split(":")[1]
        import os
        from telethon.sync import TelegramClient
        from .config import BOT_API_ID, BOT_API_HASH

        path = os.path.join(ACCOUNTS_DIR, f"{session_key}.session")

        if not os.path.exists(path):
            return await event.edit("❌ Session not found.")

        temp_client = TelegramClient(path, BOT_API_ID, BOT_API_HASH)
        await temp_client.connect()
        session_string = temp_client.session.save()
        await temp_client.disconnect()

        await event.edit(f"🔐 **String Session:**\n\n`{session_string}`\n\n⚠️ Keep this private!")

    @bot.on(events.NewMessage(pattern=r"^/addgroup"))
    async def add_group(event):
        if event.sender_id not in admins:
            return await event.reply("🚫 Not authorized.")
        if not event.is_group:
            return await event.reply("❌ Must be used in a group.")
        group_id = event.chat_id
        if group_id not in config["groups"]:
            config["groups"].append(group_id)
            save_config(config)
            await event.reply("✅ Group added.")
        else:
            await event.reply("⚠️ Already added.")

    @bot.on(events.NewMessage(pattern=r"^/removegroup"))
    async def remove_group(event):
        if event.sender_id not in admins:
            return await event.reply("🚫 Not authorized.")
        if not event.is_group:
            return await event.reply("❌ Must be used in a group.")
        group_id = event.chat_id
        if group_id in config["groups"]:
            config["groups"].remove(group_id)
            save_config(config)
            await event.reply("✅ Removed.")
        else:
            await event.reply("⚠️ Not found.")
