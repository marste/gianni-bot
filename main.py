import os
import logging
import yfinance as yf
from newsapi import NewsApiClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

if not BOT_TOKEN:
    raise ValueError("❌ Variabile BOT_TOKEN mancante su Render!")

# === NEWSAPI ===
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

# === DATI BORSA ===
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

# === NEWS ECONOMICHE ===
def get_finance_news():
    try:
        articles = newsapi.get_top_headlines(
            category="business",
            language="en",
            page_size=5,
        )["articles"]
        news_list = [f"{a['title']} ({a['source']['name']})" for a in articles if a.get("title")]
        return news_list
    except Exception as e:
        logging.error(f"Errore recupero news: {e}")
        return []

# === ANALISI SINTETICA ===
def summarize_market_news(news_list):
    if not news_list:
        return "Nessuna notizia significativa per spiegare i movimenti dei mercati oggi."

    # Soluzione heuristica: individua parole chiave tipiche e costruisce frase sintetica
    bullish_words = ["increase", "rise", "gain", "up", "strong"]
    bearish_words = ["drop", "fall", "decline", "down", "weak", "risk", "inflation"]

    bullish_count = sum(any(w in n.lower() for w in bullish_words) for n in news_list)
    bearish_count = sum(any(w in n.lower() for w in bearish_words) for n in news_list)

    if bullish_count > bearish_count:
        return "📈 I mercati mostrano tendenze positive oggi, supportati da notizie economiche favorevoli."
    elif bearish_count > bullish_count:
        return "📉 I mercati mostrano pressione al ribasso oggi, influenzati da notizie economiche negative."
    else:
        return "⚖️ Mercati stabili, senza segnali chiari dalle principali notizie economiche."

# === COMANDI TELEGRAM ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao 👋 Sono Gianni, il tuo analista virtuale dei mercati!\n\n"
        "Comandi disponibili:\n"
        "/oggi - Sintesi giornaliera dei mercati con analisi\n"
        "/settimana - Andamento settimanale e principali notizie"
    )

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_market_data()
    news_list = get_finance_news()

    msg = "📊 **Sintesi giornaliera dei mercati:**\n"
    for k, v in data.items():
        arrow = "🔺" if v and v > 0 else "🔻"
        msg += f"{k}: {arrow} {v}%\n" if v is not None else f"{k}: dati non disponibili\n"

    msg += "\n" + summarize_market_news(news_list)
    await update.message.reply_text(msg)

async def settimana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📅 **Sintesi settimanale:**\n"
    data = get_market_data()
    for k, v in data.items():
        arrow = "🔺" if v and v > 0 else "🔻"
        msg += f"{k}: {arrow} {v}% (variazione giornaliera)\n"

    news_list = get_finance_news()
    msg += "\n📰 Ultime notizie:\n" + "\n".join(news_list[:3])
    msg += "\n\n" + summarize_market_news(news_list)
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
