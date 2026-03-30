import os
import certifi
import asyncio
import sys
import time
import logging
import numpy as np

from sklearn.ensemble import RandomForestRegressor

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.compiler import transpile

os.environ['SSL_CERT_FILE'] = certifi.where()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ---------------- CONFIG ----------------

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


TOKEN = "8455087756:AAFye4e6CJsnvTvd6C5hPR27oe38_87yRmQ"

# ---------------- AUTO DELETE HELPER ----------------

async def send_auto_delete(chat, text, delay=12):
    msg = await chat.send_message(text)
    await asyncio.sleep(delay)
    try:
        await msg.delete()
    except:
        pass

async def delete_user_message(update):
    try:
        await update.message.delete()
    except:
        pass

# ---------------- QUANTUM KEY GENERATION ----------------

def generate_quantum_key(bits=8):
    qc = QuantumCircuit(bits, bits)
    qc.h(range(bits))
    qc.measure(range(bits), range(bits))

    simulator = Aer.get_backend('aer_simulator')
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1).result()
    counts = result.get_counts()

    return list(counts.keys())[0]

# ---------------- XOR ENCRYPTION ----------------

def xor_encrypt_decrypt(message, key):
    encrypted = ""
    for i in range(len(message)):
        encrypted += chr(ord(message[i]) ^ ord(key[i % len(key)]))
    return encrypted

# ---------------- ML MODEL ----------------

def extract_features(message):
    length = len(message)
    words = len(message.split())
    avg_word_len = sum(len(w) for w in message.split()) / words if words > 0 else 0
    special_chars = sum(not c.isalnum() for c in message)
    return [length, words, avg_word_len, special_chars]

X = np.array([
    [10, 2, 4, 0],
    [25, 5, 4.5, 1],
    [50, 10, 5, 2],
    [75, 15, 5.5, 3],
    [100, 20, 6, 5]
])

y = np.array([5, 8, 12, 18, 25])

time_model = RandomForestRegressor()
time_model.fit(X, y)

# ---------------- STORAGE ----------------

VOLATILE_VAULT = {}

# ---------------- AUTO CLEANUP ----------------

async def auto_cleanup(context: ContextTypes.DEFAULT_TYPE):
    current_time = time.time()

    expired = [
        user for user, data in VOLATILE_VAULT.items()
        if current_time > data["expiry"]
    ]

    for user in expired:
        VOLATILE_VAULT.pop(user, None)
        logging.info("🧹 Expired secret purged.")

# ---------------- START ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_user_message(update)
    await send_auto_delete(
        update.effective_chat,
        "🔐 ZERO-TRACE MODE ACTIVE\n\n""To send secret:\n" "/create @username\n\n" "To receive:\n" "/retrieve",
        delay=15
    )

# ---------------- CREATE ----------------

async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await delete_user_message(update)

    if not context.args:
        await send_auto_delete(
            update.effective_chat,
            "⚠ Usage: /create @username",
            delay=8
        )
        return

    target_username = context.args[0].replace("@", "")
    context.user_data["target_username"] = target_username
    context.user_data["waiting_for_secret"] = True

    await send_auto_delete(
        update.effective_chat,
        f"🌀 Quantum secure channel opened for @{target_username}.\nSend secret now.",
        delay=12
    )

# ---------------- HANDLE SECRET ----------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("waiting_for_secret"):
        await delete_user_message(update)
        return

    target_username = context.user_data["target_username"]
    secret_text = update.message.text

    quantum_key = generate_quantum_key()
    encrypted_secret = xor_encrypt_decrypt(secret_text, quantum_key)

    VOLATILE_VAULT[target_username] = {
        "secret": encrypted_secret,
        "key": quantum_key,
        "expiry": time.time() + 60
    }

    await delete_user_message(update)
    context.user_data.clear()

    await send_auto_delete(
        update.effective_chat,
        f"✅ Secret locked for @{target_username}. Valid 60s.",
        delay=10
    )

# ---------------- RETRIEVE ----------------

async def retrieve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await delete_user_message(update)

    username = update.effective_user.username

    if not username:
        await send_auto_delete(
            update.effective_chat,
            "❌ Set a Telegram username first.",
            delay=8
        )
        return

    entry = VOLATILE_VAULT.get(username)

    if not entry:
        await send_auto_delete(
            update.effective_chat,
            "❌ No secret found.",
            delay=8
        )
        return

    if time.time() > entry["expiry"]:
        VOLATILE_VAULT.pop(username, None)
        await send_auto_delete(
            update.effective_chat,
            "⌛ Secret expired.",
            delay=8
        )
        return

    # One-time access
    VOLATILE_VAULT.pop(username, None)

    decrypted_secret = xor_encrypt_decrypt(entry["secret"], entry["key"])

    features = extract_features(decrypted_secret)
    predicted_time = time_model.predict([features])[0]
    display_time = max(5, min(int(predicted_time), 30))

    secret_msg = await update.effective_chat.send_message(
        f"🔓 {decrypted_secret}\n\n⏳ Self-destruct in {display_time}s"
    )

    await asyncio.sleep(display_time)

    try:
        await secret_msg.delete()
    except:
        pass

# ---------------- MAIN ----------------

def main():
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("create", create))
    app.add_handler(CommandHandler("retrieve", retrieve))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.job_queue.run_repeating(auto_cleanup, interval=10, first=0)

    print("🚀 MAXIMUM ZERO-TRACE MODE ACTIVE")
    app.run_polling()

if __name__ == "__main__":
    main()
