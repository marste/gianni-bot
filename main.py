import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chiavi da impostare su Render come variabili d'ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    logger.error("Devi impostare BOT_TOKEN nelle variabili d'ambiente!")
    exit(1)
if not OPENAI_API_KEY:
    logger.error("Devi impostare OPENAI_API_KEY nelle variabili d'ambiente!")
    exit(1)

openai.api_key = OPENAI_API_KEY

# Comandi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Ciao! Sono GIANNI, il tuo bot finanziario.")

async def sintesi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un breve report sintetico sui mercati globali"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un analista finanziario sintetico."},
                {"role": "user", "content": "Genera un breve report in italiano sui principali movimenti dei mercati di oggi. Linguaggio chiaro, massimo 10 righe."}
            ]
        )
        text = response.choices[0].message.content
    except Exception as e:
        text = f"Errore durante la generazione del report: {e}"
    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", sintesi))

    logger.info("🤖 GIANNI è online e in ascolto...")
    # run_polling blocca correttamente il loop e gestisce i segnali
    app.run_polling(stop_signals=None)

if __name__ == "__main__":
    main()
