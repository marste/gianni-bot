import os
import logging
import yfinance as yf
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

# --- Funzioni dei comandi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao 👋 Sono GIANNI, il tuo analista virtuale dei mercati finanziari globali 📊\n"
        "Comandi disponibili:\n"
        "• /oggi → sintesi giornaliera dei mercati\n"
        "• /settimana → sintesi settimanale\n"
        "• /mese → sintesi mensile\n"
        "• /approfondisci → analisi più dettagliata"
    )

def get_stock_summary(ticker_symbol: str):
    """Restituisce chiusura odierna, variazione %, e breve analisi"""
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="2d")  # ultimi 2 giorni
    if len(hist) < 2:
        return "Dati insufficienti"
    
    today_close = hist['Close'][-1]
    yesterday_close = hist['Close'][-2]
    change_pct = ((today_close - yesterday_close) / yesterday_close) * 100
    
    if change_pct > 1:
        reason = "Mercato in rialzo, probabilmente supportato da buoni dati economici o guadagni aziendali."
    elif change_pct < -1:
        reason = "Mercato in ribasso, possibili preoccupazioni economiche o notizie negative."
    else:
        reason = "Movimento limitato, mercato stabile."
    
    return f"{today_close:.2f} ({change_pct:+.2f}%)\n{reason}"

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sp500 = get_stock_summary("^GSPC")
    nasdaq = get_stock_summary("^IXIC")
    euro_usd = get_stock_summary("EURUSD=X")
    
    msg = (
        f"📅 *Sintesi giornaliera*\n\n"
        f"S&P 500: {sp500}\n"
        f"Nasdaq: {nasdaq}\n"
        f"EUR/USD: {euro_usd}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def settimana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Placeholder semplice, puoi aggiungere trend settimanale
    await update.message.reply_text("📊 Sintesi settimanale ancora in sviluppo (puoi aggiungere trend settimanali).")

async def mese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Sintesi mensile ancora in sviluppo (puoi aggiungere trend mensili).")

async def approfondisci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Analisi approfondita ancora in sviluppo (puoi integrare notizie e motivazioni dettagliate).")

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
    app.run_polling(stop_signals=None)

if __name__ == "__main__":
    main()
