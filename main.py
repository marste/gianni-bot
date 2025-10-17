import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def genera_report():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un analista finanziario sintetico."},
                {"role": "user", "content": "Genera un breve report in italiano sui principali movimenti dei mercati di oggi. Linguaggio chiaro, massimo 10 righe, senza valori numerici."}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        logger.error(f"Errore durante la generazione del report: {e}")
        return "Errore durante la generazione del report."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono GIANNI, il tuo analista virtuale dei mercati. Usa /oggi per avere il report sintetico.")

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto generando il report dei mercati di oggi...")
    report = await genera_report()
    await update.message.reply_text(report)

# --- Main senza asyncio.run() ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("oggi", oggi))

logger.info("🤖 GIANNI è online e in ascolto...")
# Run polling direttamente, Render gestisce il loop
app.run_polling(stop_signals=None)
