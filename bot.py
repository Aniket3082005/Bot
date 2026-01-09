import os
import asyncio
import requests
from io import BytesIO
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("7957102663:AAHPE7waIXIJAsy7vP10M3bkkpsn64aPDQk")
REPLICATE_API_KEY = os.getenv("r8_cDM4rjC3glUyjl4lWyd9ELQSVMO3RFF399qzX")

# 🔒 Reference face images (RAW GitHub URLs)
REFERENCE_IMAGES = [
    "https://raw.githubusercontent.com/Aniket3082005/model-face/refs/heads/main/ref1.jpg",
    "https://raw.githubusercontent.com/Aniket3082005/model-face/refs/heads/main/ref2.jpg",
    "https://raw.githubusercontent.com/Aniket3082005/model-face/refs/heads/main/ref3.jpg",
    "https://raw.githubusercontent.com/Aniket3082005/model-face/refs/heads/main/ref4.jpg",
    "https://raw.githubusercontent.com/Aniket3082005/model-face/refs/heads/main/ref5.jpg",
    "https://raw.githubusercontent.com/Aniket3082005/model-face/refs/heads/main/ref6.jpg",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Face-Lock AI Bot Ready\n\n"
        "Prompt bhejo 👇\n"
        "Example:\n"
        "fashion photoshoot, studio lighting"
    )

def generate_image(prompt):
    headers = {
        "Authorization": f"Token {REPLICATE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        # 🔥 FaceID / IP-Adapter based model (Replicate)
        "version": "b3b4f4c33f9f8e6f1e7a9b44c6fdc2a6c58e8fbb8c70b2c9e0e2b7e9b9c6f0a1",
        "input": {
            "prompt": prompt,
            "face_image": REFERENCE_IMAGES,
            "width": 1024,
            "height": 1024,
            "num_steps": 30,
            "guidance_scale": 7.5
        }
    }

    res = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json=payload,
        timeout=60
    )

    data = res.json()
    prediction_id = data["id"]

    while True:
        poll = requests.get(
            f"https://api.replicate.com/v1/predictions/{prediction_id}",
            headers=headers,
            timeout=60
        ).json()

        if poll["status"] == "succeeded":
            return poll["output"][0]

        if poll["status"] == "failed":
            raise Exception(poll)

async def generate_and_send(context, chat_id, prompt):
    try:
        image_url = generate_image(prompt)
        img_data = requests.get(image_url, timeout=60).content
        image = BytesIO(img_data)

        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image,
            caption="✅ Face-locked image ready"
        )

    except Exception as e:
        print("ERROR:", e)
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Image generate nahi ho payi"
        )

async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Image generate ho rahi hai...")
    asyncio.create_task(
        generate_and_send(context, update.effective_chat.id, update.message.text)
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))
    print("🤖 Face-Lock Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
