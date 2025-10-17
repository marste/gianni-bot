import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

# --- Comandi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao 👋 Sono GIANNI, il tuo analista virtuale dei mercati finanziari globali 📊\n"
        "Comandi disponibili:\n"
        "• /oggi → sintesi giornaliera\n"
        "• /settimana → sintesi settimanale\n"
        "• /mese → sintesi mensile\n"
        "• /approfondisci → analisi dettagliata"
    )

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Sintesi giornaliera placeholder")

async def settimana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Sintesi settimanale placeholder")

async def mese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Sintesi mensile placeholder")

async def approfondisci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Analisi approfondita placeholder")


# --- Main ---
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Aggiungi handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", oggi))
    app.add_handler(CommandHandler("settimana", settimana))
    app.add_handler(CommandHandler("mese", mese))
    app.add_handler(CommandHandler("approfondisci", approfondisci))

    print("🤖 GIANNI è online e in ascolto...")

    # Run polling: non serve asyncio.run(), lascia che la libreria gestisca il loop
    app.run_polling(stop_signals=None)


if __name__ == "__main__":
    main()
