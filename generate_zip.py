import os
import zipfile

project_name = "telethon-userbot-manager"
files = {
    "bot/__init__.py": "",
    "bot/config.py": "your config.py code here",
    "bot/session_manager.py": "your session_manager.py code here",
    "bot/commands.py": "your commands.py code here",
    "bot/forwarder.py": "your forwarder.py code here",
    "bot/main.py": "your main.py code here",
    "requirements.txt": "telethon>=1.33\n",
    ".gitignore": "__pycache__/\naccounts/\nconfig.json\n*.session\n*.pyc\n.env\n",
    "README.md": "# Telethon Userbot Manager\n\nInstructions here...",
}

os.makedirs(project_name, exist_ok=True)

for path, content in files.items():
    full_path = os.path.join(project_name, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

zip_path = f"{project_name}.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, _, filenames in os.walk(project_name):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            zipf.write(file_path, os.path.relpath(file_path, project_name))

print(f"✅ Project zipped at: {zip_path}")
