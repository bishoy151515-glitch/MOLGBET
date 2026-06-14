import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def prompt(match):
    return f"""
حلل المباراة التالية كتوقعات كرة قدم، باللغة المصرية.
ممنوع تقول مضمون أو أكيد.
اكتب:
🏆 المباراة
📊 التحليل
🎯 أفضل ترشيح
📌 ترشيحات إضافية
⚖️ درجة الثقة
🚫 المخاطر

المباراة:
{match}
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أهلاً 👋\nابعت:\n/predict Brazil vs Morocco"
    )

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match = " ".join(context.args)

    if not match:
        await update.message.reply_text("اكتب المباراة بعد الأمر:\n/predict Egypt vs Belgium")
        return

    await update.message.reply_text("جاري التحليل... ⏳")

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt(match)
    )

    await update.message.reply_text(
        response.output_text + "\n\n⚠️ التوقعات تحليل احتمالي وليست مضمونة."
    )

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))

app.run_polling()
