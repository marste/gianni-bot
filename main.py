import os
import logging
import yfinance as yf
from newsapi import NewsApiClient
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# === LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY or not NEWSAPI_KEY:
    raise ValueError("❌ Assicurati di avere BOT_TOKEN, NEWSAPI_KEY e OPENAI_API_KEY impostati!")

openai.api_key = OPENAI_API_KEY
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

# === ANALISI GPT ===
def generate_market_analysis(data, news_list, period="giornaliero"):
    news_text = "\n".join(news_list) if news_list else "Nessuna notizia rilevante."
    market_text = "\n".join([f"{k}: {v}%" for k, v in data.items() if v is not None])

    prompt = f"""
Sei un analista finanziario professionista.
Analizza i mercati finanziari {period} basandoti sui seguenti dati:
{market_text}

Le ultime notizie economiche:
{news_text}

Scrivi un breve report sintetico in italiano spiegando le ragioni dei movimenti principali dei mercati. Mantieni il linguaggio chiaro e conciso, massimo 5 righe.
"""

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=200
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Errore GPT: {e}")
        return "Non sono riuscito a generare l'analisi in questo momento."

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
    analysis = generate_market_analysis(data, news_list, period="giornaliero")

    msg = "📊 **Sintesi giornaliera dei mercati:**\n"
    for k, v in data.items():
        arrow = "🔺" if v and v > 0 else "🔻"
        msg += f"{k}: {arrow} {v}%\n" if v is not None else f"{k}: dati non disponibili\n"

    msg += "\n" + analysis
    await update.message.reply_text(msg)

async def settimana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_market_data()
    news_list = get_finance_news()
    analysis = generate_market_analysis(data, news_list, period="settimanale")

    msg = "📅 **Sintesi settimanale:**\n"
    for k, v in data.items():
        arrow = "🔺" if v and v > 0 else "🔻"
        msg += f"{k}: {arrow} {v}% (variazione giornaliera)\n" if v is not None else f"{k}: dati non disponibili\n"

    msg += "\n📰 Ultime notizie:\n" + "\n".join(news_list[:3])
    msg += "\n\n" + analysis
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
