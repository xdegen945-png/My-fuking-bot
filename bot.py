import time
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from questions import generate_questions

TOKEN = "8273000596:AAHcVC5IYNMtf-t02YPLxu5VgusZPtg9cFo"

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["English", "Mathematics"],
        ["Physics", "Chemistry"],
        ["Biology"]
    ]

    await update.message.reply_text(
        "📚 Select a subject:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    subjects = ["English", "Mathematics", "Physics", "Chemistry", "Biology"]

    if text in subjects:
        users[user_id] = {
            "questions": generate_questions(text, 20),
            "index": 0,
            "score": 0,
            "start_time": time.time()
        }
        await send_question(update, context)
        return

    if user_id in users:
        data = users[user_id]
        q = data["questions"][data["index"]]

        if text == q["a"]:
            data["score"] += 1
            await update.message.reply_text(
                f"✅ Correct!\n\n📖 {q['exp']}"
            )
        else:
            await update.message.reply_text(
                f"❌ Wrong!\nCorrect: {q['a']}\n\n📖 {q['exp']}"
            )

        data["index"] += 1

        if data["index"] < len(data["questions"]):
            await send_question(update, context)
        else:
            total_time = int(time.time() - data["start_time"])
            await update.message.reply_text(
                f"🎉 Finished!\nScore: {data['score']}/20\n⏱ Time: {total_time}s"
            )
            del users[user_id]

async def send_question(update, context):
    user_id = update.message.from_user.id
    data = users[user_id]
    q = data["questions"][data["index"]]

    options = "\n".join(q["o"])

    await update.message.reply_text(
        f"Q{data['index']+1}: {q['q']}\n\n{options}"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
