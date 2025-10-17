import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, MessageHandler, filters
import openai
from fastapi import FastAPI
from mangum import Mangum  # se vuoi adattare per AWS Lambda, opzionale

# Configurazione logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Chiavi da variabili d'ambiente
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # es: https://gianni-bot-ijwl.onrender.com/webhook

openai.api_key = OPENAI_API_KEY

# Funzioni bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Ciao! Sono GIANNI, il tuo bot finanziario.")

async def sintesi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un analista finanziario sintetico."},
                {"role": "user", "content": "Genera un breve report in italiano sui principali movimenti dei mercati di oggi (massimo 10 righe)."}
            ]
        )
        text = response.choices[0].message.content
    except Exception as e:
        text = f"Errore durante la generazione del report: {e}"
    await update.message.reply_text(text)

# Creazione applicazione Telegram
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("oggi", sintesi))

# Configurazione FastAPI per webhook
fastapi_app = FastAPI()

@fastapi_app.post("/webhook")
async def webhook(update: dict):
    telegram_update = Update.de_json(update, app.bot)
    await app.update_queue.put(telegram_update)
    return {"ok": True}

# Avvio webhook su Telegram
async def main():
    await app.bot.set_webhook(WEBHOOK_URL)

import uvicorn

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    uvicorn.run(fastapi_app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
