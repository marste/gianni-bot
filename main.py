import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# Configurazione logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Recupero delle chiavi API dalle variabili d'ambiente
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Funzione per generare il report dei mercati
async def genera_report():
    prompt = (
        "Fornisci un breve report sintetico in italiano, massimo 10 righe, "
        "spiegando le ragioni principali dei movimenti dei mercati finanziari di oggi. "
        "Mantieni un linguaggio chiaro e conciso."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        testo = response.choices[0].message.content.strip()
        return testo
    except Exception as e:
        logging.error(f"Errore durante la generazione del report: {e}")
        return "Errore nella generazione del report."

# Handler per il comando /report
async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sto generando il report dei mercati...")
    report = await genera_report()
    await update.message.reply_text(f"**Sintesi giornaliera dei mercati:**\n{report}", parse_mode="Markdown")

# Funzione principale
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("report", report_command))

    logging.info("🤖 GIANNI è online e in ascolto...")

    # Avvio del bot
    await app.run_polling(stop_signals=None)

# Esecuzione
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot interrotto.")
