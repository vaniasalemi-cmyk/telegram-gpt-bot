from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

import os
TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["سلام", "حالت چطوره؟"], ["بازی", "کمک"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        "سلام! من ربات چت‌باتت هستم 😎 گزینه‌ای انتخاب کن یا پیام بده:",
        reply_markup=reply_markup
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if user_text.lower() == "سلام":
        reply = "سلام! خوبی؟"
    elif user_text.lower() == "حالت چطوره؟":
        reply = "من خوبم، مرسی که پرسیدی 😄"
    elif user_text.lower() == "بازی":
        reply = "میخوای یه بازی حدس عدد انجام بدیم؟"
    elif user_text.lower() == "کمک":
        reply = "می‌تونی یه پیام بنویسی و من جواب میدم، یا یکی از گزینه‌ها رو انتخاب کن."
    else:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_text,
            max_tokens=100
        )
        reply = response.choices[0].text.strip()
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))
app.run_polling()
