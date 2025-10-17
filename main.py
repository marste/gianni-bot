import os
import logging
import yfinance as yf
from newsapi import NewsApiClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configura logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

if not BOT_TOKEN:
    raise ValueError("❌ Variabile BOT_TOKEN mancante su Render!")

# Inizializza NewsAPI
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

# === COMANDI TELEGRAM ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao 👋 Sono Gianni, il tuo analista virtuale dei mercati!")

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Analisi giornaliera: in arrivo dati reali da Yahoo Finance...")

async def settimana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Sintesi settimanale: raccolgo le ultime notizie finanziarie...")

# === MAIN ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", oggi))
    app.add_handler(CommandHandler("settimana", settimana))

    print("🤖 GIANNI è online e in ascolto...")
    app.run_polling()

if __name__ == "__main__":
    main()
