from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import os

BOT_TOKEN = os.getenv("7957102663:AAHPE7waIXIJAsy7vP10M3bkkpsn64aPDQk")
REPLICATE_API_KEY = os.getenv("r8_cDM4rjC3glUyjl4lWyd9ELQSVMO3RFF399qzX")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello!\n"
        "Main test bot hoon.\n"
        "Koi bhi message bhejo 🙂"
    )

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Tumne likha: {text}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Bot chal raha hai...")
    app.run_polling()

if __name__ == "__main__":
    main()
