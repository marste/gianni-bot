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

if not BOT_TOKEN or not NEWSAPI_KEY:
    raise ValueError("❌ Assicurati di avere BOT_TOKEN e NEWSAPI_KEY impostati!")

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

# === ANALISI AUTOMATICA ===
def generate_market_analysis(data, news_list, period="giornaliero"):
    analysis = []
    for k, v in data.items():
        if v is not None:
            if v > 0:
                analysis.append(f"{k} è in aumento di {v}% grazie a fattori positivi del mercato.")
            elif v < 0:
                analysis.append(f"{k} scende di {abs(v)}% per pressioni negative del mercato.")
            else:
                analysis.append(f"{k} rimane stabile.")
    if not analysis:
        return "Non ci sono dati sufficienti per generare l'analisi."
    
    # Aggiungi le notizie principali
    if news_list:
        analysis.append("Ultime notizie economiche:")
        analysis.extend(news_list[:3])
    
    # Limita a massimo 8 righe per non rendere troppo lungo
    return "\n".join(analysis[:8])

# === COMANDI TELEGRAM ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao 👋 Sono Gianni, il tuo analista virtuale gratuito!\n\n"
        "Comandi disponibili:\n"
        "/oggi - Sintesi giornaliera dei mercati\n"
        "/settimana - Andamento settimanale e principali notizie"
    )

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_market_data()
    news_list = get_finance_news()
    analysis = generate_market_analysis(data, news_list, period="giornaliero")

    msg = "📊 **Sintesi giornaliera dei mercati:**\n"
    for k, v in data.items():
        if v is not None:
            arrow = "🔺" if v > 0 else "🔻" if v < 0 else "➡️"
            msg += f"{k}: {arrow} {v}%\n"
        else:
            msg += f"{k}: dati non disponibili\n"
    msg += "\n" + analysis
    await update.message.reply_text(msg)

async def settimana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_market_data()
    news_list = get_finance_news()
    analysis = generate_market_analysis(data, news_list, period="settimanale")

    msg = "📅 **Sintesi settimanale:**\n"
    for k, v in data.items():
        if v is not None:
            arrow = "🔺" if v > 0 else "🔻" if v < 0 else "➡️"
            msg += f"{k}: {arrow} {v}% (variazione giornaliera)\n"
        else:
            msg += f"{k}: dati non disponibili\n"
    msg += "\n" + analysis
    await update.message.reply_text(msg)

# === MAIN ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", oggi))
    app.add_handler(CommandHandler("settimana", settimana))

    print("🤖 GIANNI gratuito è online e in ascolto...")
    app.run_polling()

if __name__ == "__main__":
    main()
