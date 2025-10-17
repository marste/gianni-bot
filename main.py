import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# ===================== CONFIG =====================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("⚠️ TELEGRAM_BOT_TOKEN non impostato!")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY non impostato!")

openai.api_key = OPENAI_API_KEY

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ===================== FUNZIONI =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! 🤖 GIANNI è online e in ascolto.")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Genera un report sintetico dei mercati di oggi.
    Solo testo in italiano, massimo 10 righe.
    """
    await update.message.reply_text("Generazione report in corso... ⏳")

    prompt = (
        "Fornisci un breve report sintetico dei principali movimenti dei mercati finanziari di oggi. "
        "Scrivi in italiano, linguaggio chiaro e conciso, massimo 10 righe. "
        "Non includere valori degli indici, solo le ragioni dei movimenti principali."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.5
        )
        report_text = response.choices[0].message.content.strip()
        await update.message.reply_text(f"**Sintesi giornaliera dei mercati:**\n{report_text}", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Errore durante la generazione del report: {e}")
        await update.message.reply_text("❌ Errore durante la generazione del report.")

# ===================== MAIN =====================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Comandi
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))

    logger.info("🤖 GIANNI è online e in ascolto...")
    # Su Render NON usare asyncio.run()
    app.run_polling(stop_signals=None)  # stop_signals=None evita conflitti con il loop già esistente

if __name__ == "__main__":
    main()
