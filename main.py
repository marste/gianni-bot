import os
import logging
import yfinance as yf
import requests
from newsapi import NewsApiClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === CONFIGURAZIONE LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

if not BOT_TOKEN:
    raise ValueError("❌ Variabile BOT_TOKEN mancante su Render!")

# === INIZIALIZZA NEWSAPI ===
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

# === FUNZIONE: DATI BORSA ===
def get_market_data():
    symbols = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "Dow Jones": "^DJI",
        "Euro Stoxx 50": "^STOXX50E",
        "FTSE MIB": "FTSEMIB.MI",
        "Nikkei 225": "^N225",
        "Shanghai Comp.": "000001.SS",
    }

    data = {}
    for name, symbol in symbols.items():
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d")
        if len(hist) >= 2:
            prev = hist["Close"][-2]
            last = hist["Close"][-1]
            change = ((last - prev) / prev) * 100
            data[name] = round(change, 2)
        else:
            data[name] = None
    return data

# === FUNZIONE: NEWS ECONOMICHE ===
def get_finance_news():
    try:
        articles = newsapi.get_top_headlines(
            category="business",
            language="en",
            page_size=3,
        )["articles"]
        news_list = [f"📰 {a['title']} ({a['source']['name']})" for a in articles if a.get("title")]
        return "\n".join(news_list) if news_list else "Nessuna notizia economica rilevante oggi."
    except Exception as e:
        logging.error(f"Errore recupero news: {e}")
        return "Errore nel recupero delle notizie."

# === COMANDI TELEGRAM ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao 👋 Sono Gianni, il tuo analista virtuale dei mercati!\n\n"
        "Comandi disponibili:\n"
        "/oggi - Sintesi giornaliera dei mercati\n"
        "/settimana - Andamento settimanale e principali notizie"
    )

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_market_data()
    news = get_finance_news()

    msg = "📊 **Sintesi giornaliera dei mercati:**\n"
    for k, v in data.items():
        arrow = "🔺" if v and v > 0 else "🔻"
        msg += f"{k}: {arrow} {v}%\n" if v is not None else f"{k}: dati non disponibili\n"

    msg += "\n" + news
    await update.message.reply_text(msg)

async def settimana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📅 **Sintesi settimanale:**\n"
    data = get_market_data()
    for k, v in data.items():
        arrow = "🔺" if v and v > 0 else "🔻"
        msg += f"{k}: {arrow} {v}% (variazione giornaliera)\n"

    msg += "\n📰 Ultime notizie:\n" + get_finance_news()
    await update.message.reply_text(msg)

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
