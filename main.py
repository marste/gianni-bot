import os
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono GIANNI 📊 Il tuo analista virtuale dei mercati finanziari.")

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sp500 = yf.Ticker("^GSPC").history(period="1d")["Close"][-1]
    nasdaq = yf.Ticker("^IXIC").history(period="1d")["Close"][-1]
    ftsemib = yf.Ticker("FTSEMIB.MI").history(period="1d")["Close"][-1]
    await update.message.reply_text(
        f"📊 *Mercati oggi*\n\n"
        f"S&P 500: {sp500:.2f}\n"
        f"Nasdaq: {nasdaq:.2f}\n"
        f"FTSE MIB: {ftsemib:.2f}",
        parse_mode="Markdown"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("oggi", oggi))

app.run_polling()
