import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# -------------------------------
# Configurazione chiavi API
# -------------------------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# -------------------------------
# Funzioni dei comandi Telegram
# -------------------------------

async def sintesi_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera una sintesi giornaliera dei mercati."""
    prompt = (
        "Scrivi un breve report in italiano (max 10 righe) sui principali movimenti dei mercati di oggi. "
        "Spiega in modo chiaro e conciso le ragioni dei movimenti economici principali, senza numeri o valori di indici."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        report = response.choices[0].message.content.strip()
    except Exception as e:
        report = f"Errore durante la generazione del report: {e}"

    await update.message.reply_text(f"**Sintesi giornaliera dei mercati:**\n{report}", parse_mode="Markdown")


async def approfondisci_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Genera un'analisi più approfondita dei mercati."""
    prompt = (
        "Scrivi un'analisi approfondita in italiano dei principali movimenti dei mercati di oggi. "
        "Motiva i movimenti principali e spiega fattori economici, politici e geopolitici. "
        "Mantieni il linguaggio chiaro e conciso."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        report = response.choices[0].message.content.strip()
    except Exception as e:
        report = f"Errore durante la generazione del report: {e}"

    await update.message.reply_text(f"**Analisi approfondita dei mercati:**\n{report}", parse_mode="Markdown")


# -------------------------------
# Main: avvio del bot
# -------------------------------

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Registrazione comandi
    app.add_handler(CommandHandler("sintesi", sintesi_command))
    app.add_handler(CommandHandler("approfondisci", approfondisci_command))

    # Avvio polling senza asyncio.run
    app.run_polling(stop_signals=None)
