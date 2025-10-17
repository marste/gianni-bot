import os
import asyncio
import yfinance as yf
from telegram import Bot
from telegram.ext import CommandHandler, Application

TOKEN = os.getenv("BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("Ciao! Sono GIANNI 📊 Il tuo analista virtuale dei mercati finanziari.")

async def oggi(update, context):
    try:
        sp500 = yf.Ticker("^GSPC").history(period="1d")["Close"][-1]
        nasdaq = yf.Ticker("^IXIC").history(period="1d")["Close"][-1]
        ftsemib = yf.Ticker("FTSEMIB.MI").history(period="1d")["Close"][-1]
        text = (
            f"📊 *Mercati oggi*\n\n"
            f"S&P 500: {sp500:.2f}\n"
            f"Nasdaq: {nasdaq:.2f}\n"
            f"FTSE MIB: {ftsemib:.2f}"
        )
        await update.message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Errore nel recupero dati: {e}")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", oggi))
    print("🤖 GIANNI è online e in ascolto...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
