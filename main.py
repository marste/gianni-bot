import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI

# Recupera le chiavi dall'ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Assicurati di avere impostato BOT_TOKEN e OPENAI_API_KEY nelle variabili d'ambiente.")

# Inizializza il client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Funzione per generare la sintesi giornaliera
async def sintesi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = (
        "Scrivi un breve report in italiano (max 10 righe) sui principali movimenti dei mercati di oggi. "
        "Spiega in modo chiaro e conciso le ragioni dei movimenti economici principali, senza numeri o valori di indici."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        report = response.choices[0].message.content
    except Exception as e:
        report = f"Errore durante la generazione del report: {e}"

    await update.message.reply_text(f"**Sintesi giornaliera dei mercati:**\n{report}", parse_mode="Markdown")

# Funzione per generare analisi approfondita
async def approfondisci_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = (
        "Scrivi un'analisi approfondita in italiano sui principali movimenti dei mercati di oggi. "
        "Spiega cause, trend e fattori economici rilevanti, in modo chiaro e conciso (max 15 righe)."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        report = response.choices[0].message.content
    except Exception as e:
        report = f"Errore durante la generazione del report: {e}"

    await update.message.reply_text(f"**Analisi approfondita dei mercati:**\n{report}", parse_mode="Markdown")

# Funzione principale per avviare il bot
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("sintesi", sintesi_command))
    app.add_handler(CommandHandler("approfondisci", approfondisci_command))

    print("🤖 GIANNI è online e in ascolto...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
