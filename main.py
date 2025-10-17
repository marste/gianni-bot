import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono GIANNI, il tuo analista virtuale dei mercati finanziari 📈")

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oggi le borse globali sono in aggiornamento...")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", today))

    print("🤖 GIANNI è online e in ascolto...")

    # ✅ FIX: evita asyncio.run() e usa direttamente run_polling()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        # ✅ FIX per ambienti che hanno già un event loop (Render, Jupyter, etc.)
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()
