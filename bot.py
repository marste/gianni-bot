import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import aiohttp
import logging

# Configura il logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Prompt predefinito
PROMPT = "Scrivi un breve report sintetico in italiano spiegando le ragioni dei movimenti principali dei mercati di oggi. Mantieni il linguaggio chiaro e conciso, massimo 10 righe."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Invia un messaggio per ricevere un report sui movimenti dei mercati di oggi.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Chiama l'API di OpenAI
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o",  # O il modello disponibile con il tuo abbonamento
                "messages": [{"role": "user", "content": PROMPT}],
                "max_tokens": 200
            }
            async with session.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    reply = data["choices"][0]["message"]["content"]
                    await update.message.reply_text(reply)
                else:
                    await update.message.reply_text("Errore nella richiesta all'API. Riprova più tardi.")
    except Exception as e:
        logger.error(f"Errore: {e}")
        await update.message.reply_text("Si è verificato un errore. Riprova più tardi.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    # Inizializza il bot con il token
    application = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()

    # Aggiungi handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Avvia il bot
    application.run_polling()

if __name__ == "__main__":
    main()
