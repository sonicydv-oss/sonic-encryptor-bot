import telebot
import os
import marshal
import zlib
import base64
import tempfile

# ================= CONFIG =================
BOT_TOKEN = os.getenv("8337293828:AAHc6E4cs0VIkq6GatcpTdSJ3Q1d1xRXTB4")

# 🔐 Premium Users (Telegram User IDs)
PREMIUM_USERS = [
    7540772703,   # apna telegram user id yaha daal
]

BOT_NAME = "SONIC ENCRYPTOR"
# =========================================

bot = telebot.TeleBot(BOT_TOKEN)

def encrypt_py(code: str):
    compiled = compile(code, "<sonic-protected>", "exec")
    data = marshal.dumps(compiled)
    data = zlib.compress(data, 9)
    data = base64.b64encode(data)

    return f'''
# 🔒 {BOT_NAME}
# ⚠️ This file is encrypted & irreversible
# 👤 Protected by Sonic

import marshal, zlib, base64
exec(marshal.loads(zlib.decompress(base64.b64decode({data}))))
'''

def is_premium(user_id):
    return user_id in PREMIUM_USERS

# ================= COMMANDS =================

@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(
        m,
        f"⚡ *{BOT_NAME}*\n\n"
        "🔐 Send me any `.py` file\n"
        "I will encrypt & protect it\n\n"
        "⚠️ Encryption is irreversible\n"
        "👑 Premium users only",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["help"])
def help_cmd(m):
    bot.reply_to(
        m,
        "📌 *How to use:*\n"
        "1️⃣ Send a `.py` file\n"
        "2️⃣ Get encrypted `.py`\n"
        "3️⃣ Run normally using python\n\n"
        "⚠️ Original source cannot be recovered",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=["status"])
def status(m):
    bot.reply_to(m, "✅ Sonic Encryptor is ONLINE 24/7")

# ================= FILE HANDLER =================

@bot.message_handler(content_types=["document"])
def handle_file(m):
    user_id = m.from_user.id

    if not is_premium(user_id):
        bot.reply_to(m, "❌ Premium access required")
        return

    file_name = m.document.file_name

    if not file_name.endswith(".py"):
        bot.reply_to(m, "❌ Only .py files allowed")
        return

    try:
        file_info = bot.get_file(m.document.file_id)
        downloaded = bot.download_file(file_info.file_path)

        code = downloaded.decode("utf-8", errors="ignore")
        encrypted_code = encrypt_py(code)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix="_encrypted.py",
            mode="w",
            encoding="utf-8"
        ) as temp:
            temp.write(encrypted_code)
            temp_name = temp.name

        with open(temp_name, "rb") as f:
            bot.send_document(
                m.chat.id,
                f,
                caption="🔐 Encrypted by SONIC"
            )

        os.remove(temp_name)

    except Exception as e:
        bot.reply_to(m, f"❌ Error: {e}")

# ================= RUN =================
bot.infinity_polling()