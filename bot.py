import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
)

# ====== المفاتيح ======
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENAI_KEY}",
    "Content-Type": "application/json"
}

# ====== دوال البوت ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("اسألني سؤال", callback_data="ask")],
        [InlineKeyboardButton("مساعدة", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلين! أنا بوتك الذكي 😎\nاضغط على الأزرار تحت لتبدأ",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "تقدر ترسللي أي سؤال وأنا برد عليك   😁\n"
        "زر 'اسألني سؤال' لتجربة مباشرة."
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "ask":
        await query.edit_message_text("يلا، أرسل سؤالك وهرد عليك 😎")
    elif query.data == "help":
        await query.edit_message_text(
            "😁\n"
            "بس هات سؤالك أو اضغط 'اسألني سؤال'"
        )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": user_text}]
    }
    try:
        r = requests.post(OPENAI_URL, headers=headers, json=payload, timeout=30)
        answer = r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        answer = "صار شي غلط 🤯 حاول مرة ثانية"

    await update.message.reply_text(answer)

# ====== تشغيل البوت ======
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # أوامر رئيسية
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # التعامل مع أزرار
    app.add_handler(CallbackQueryHandler(button_handler))

    # التعامل مع الرسائل النصية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()

if __name__ == "__main__":
    main()
