import os
import logging
import yfinance as yf
from newsapi import NewsApiClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- Token e chiave API ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

# --- Funzioni bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao 👋 Sono GIANNI, il tuo analista virtuale dei mercati finanziari globali 📊\n\n"
        "Comandi disponibili:\n"
        "• /oggi → Sintesi giornaliera con motivazioni dei movimenti\n"
        "• /approfondisci → Analisi dettagliata con notizie economiche"
    )

def get_stock_summary(ticker_symbol: str):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="2d")
    if len(hist) < 2:
        return None, None
    today_close = hist['Close'][-1]
    yesterday_close = hist['Close'][-2]
    change_pct = ((today_close - yesterday_close) / yesterday_close) * 100
    return today_close, change_pct

def get_market_news(query: str, n=3):
    articles = newsapi.get_everything(
        q=query, language='en', sort_by='publishedAt', page_size=n
    )
    news_list = []
    for a in articles['articles']:
        title = a['title']
        description = a['description'] or ""
        news_list.append(f"- {title}\n  {description}")
    return "\n\n".join(news_list) if news_list else "Nessuna notizia recente disponibile."

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sp500_val, sp500_change = get_stock_summary("^GSPC")
    nasdaq_val, nasdaq_change = get_stock_summary("^IXIC")
    euro_usd_val, euro_usd_change = get_stock_summary("EURUSD=X")

    def reason(change):
        if change is None:
            return "Dati non disponibili"
        if change > 1:
            return "Mercato in rialzo, supportato da dati economici positivi o guadagni aziendali."
        elif change < -1:
            return "Mercato in ribasso, influenzato da notizie negative o preoccupazioni economiche."
        else:
            return "Mercato stabile, senza movimenti significativi."

    msg = (
        f"📅 *Sintesi giornaliera*\n\n"
        f"S&P 500: {sp500_val:.2f} ({sp500_change:+.2f}%)\nMotivo: {reason(sp500_change)}\n\n"
        f"Nasdaq: {nasdaq_val:.2f} ({nasdaq_change:+.2f}%)\nMotivo: {reason(nasdaq_change)}\n\n"
        f"EUR/USD: {euro_usd_val:.4f} ({euro_usd_change:+.2f}%)\nMotivo: {reason(euro_usd_change)}"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def approfondisci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_msg = get_market_news("stock OR finance OR economy", n=5)
    await update.message.reply_text(f"🔍 *Analisi approfondita*\n\n{news_msg}", parse_mode="Markdown")

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", oggi))
    app.add_handler(CommandHandler("approfondisci", approfondisci))

    print("🤖 GIANNI è online e in ascolto...")
    app.run_polling(stop_signals=None)  # Nessun asyncio.run, compatibile con Render

if __name__ == "__main__":
    main()
