import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai
import requests

# Configurazioni
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # per notizie finanziarie

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

# Funzione per recuperare notizie economiche recenti
def get_market_news():
    url = ("https://newsapi.org/v2/top-headlines?"
           "category=business&language=it&pageSize=10&apiKey=" + NEWSAPI_KEY)
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        news_text = " ".join([a["title"] + ". " + (a.get("description") or "") for a in articles])
        return news_text
    except Exception as e:
        print(f"Errore recuperando notizie: {e}")
        return ""

# Funzione per generare report sintetico
def generate_market_report(news_text):
    prompt = (
        "Leggi queste notizie economiche e crea un breve report in italiano, chiaro e conciso, "
        "massimo 10 righe, spiegando le principali ragioni dei movimenti dei mercati oggi:\n\n"
        f"{news_text}"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        report = response.choices[0].message.content.strip()
        return report
    except Exception as e:
        print(f"Errore OpenAI: {e}")
        return "Non sono riuscito a generare il report oggi."

# Handler Telegram
async def sintesi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto generando la sintesi dei mercati...")
    news = get_market_news()
    report = generate_market_report(news)
    await update.message.reply_text(report)

# Avvio bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("sintesi", sintesi))
    print("🤖 GIANNI è online e in ascolto...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
