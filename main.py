import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao 👋 Sono GIANNI, il tuo analista virtuale dei mercati finanziari globali 📊\n\n"
        "Comandi disponibili:\n"
        "• /oggi → sintesi giornaliera dei mercati\n"
        "• /settimana → sintesi settimanale\n"
        "• /mese → sintesi mensile\n"
        "• /approfondisci → analisi più dettagliata"
    )

async def oggi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 *Sintesi giornaliera (placeholder)*\n"
        "- S&P 500: +0.4%\n- Nasdaq: +0.6%\n- Euro Stoxx 50: -0.2%\n"
        "🪙 EUR/USD stabile, 🛢️ petrolio in calo.\nFonti: Reuters, Bloomberg.",
        parse_mode="Markdown"
    )

async def settimana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 *Sintesi settimanale (placeholder)*\n"
        "- Azioni USA in rialzo, Europa mista.\n- Oro stabile, petrolio in ripresa.\n"
        "💬 Outlook: prudenza su dati inflazione in arrivo.",
        parse_mode="Markdown"
    )

async def mese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📈 *Sintesi mensile (placeholder)*\n"
        "- Mercati in recupero grazie a tagli dei tassi USA.\n"
        "- EUR in rafforzamento contro USD.\n"
        "- Bitcoin sopra 70k $.\n"
        "Fonti: Investing.com, Yahoo Finance.",
        parse_mode="Markdown"
    )

async def approfondisci(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 Analisi approfondita in arrivo... (in questa sezione puoi integrare API reali da Investing, AlphaVantage o Yahoo Finance)."
    )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("oggi", oggi))
    app.add_handler(CommandHandler("settimana", settimana))
    app.add_handler(CommandHandler("mese", mese))
    app.add_handler(CommandHandler("approfondisci", approfondisci))

    print("🤖 GIANNI è online e in ascolto...")

    # ✅ Questo è il modo corretto e moderno
    await app.run_polling(close_loop=False)

if __name__ == "__main__":
    asyncio.run(main())
