import os
import time
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from questions import generate_question

TOKEN = os.getenv("BOT_TOKEN")

users = {}
EXAM_TIME = 30 * 60


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("English", callback_data="English"),
         InlineKeyboardButton("Mathematics", callback_data="Mathematics")],
        [InlineKeyboardButton("Physics", callback_data="Physics"),
         InlineKeyboardButton("Chemistry", callback_data="Chemistry")],
        [InlineKeyboardButton("Biology", callback_data="Biology")]
    ]

    await update.message.reply_text(
        "📚 CBT MODE READY\nChoose subject:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- TIMER ----------------
def auto_submit(user_id):
    if user_id in users:
        users[user_id]["submitted"] = True


# ---------------- SEND QUESTION ----------------
async def send_q(update, context):
    user_id = update.effective_user.id
    data = users[user_id]
    q = data["questions"][data["index"]]

    if q.get("type") == "comprehension":
        text = f"📖 PASSAGE:\n{q['passage']}\n\n❓ {q['q']}"
    else:
        text = f"📘 Q{data['index']+1}/40\n\n{q['q']}"

    keyboard = [
        [InlineKeyboardButton("A", callback_data="A"),
         InlineKeyboardButton("B", callback_data="B")],
        [InlineKeyboardButton("C", callback_data="C"),
         InlineKeyboardButton("D", callback_data="D")]
    ]

    await context.bot.send_message(user_id, text, reply_markup=InlineKeyboardMarkup(keyboard))


# ---------------- SUBJECT START ----------------
async def subject_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    subject = query.data

    users[user_id] = {
        "subject": subject,
        "questions": [generate_question(subject) for _ in range(40)],
        "index": 0,
        "score": 0,
        "weak": {},
        "start": time.time(),
        "submitted": False,
        "answered": False
    }

    threading.Timer(EXAM_TIME, auto_submit, args=[user_id]).start()

    await send_q(update, context)


# ---------------- ANSWER ----------------
async def answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    data = users[user_id]
    q = data["questions"][data["index"]]

    if data["answered"]:
        return

    data["answered"] = True

    if query.data == q["answer"]:
        data["score"] += 1
        await query.message.reply_text("✅ Correct!")
    else:
        data["weak"][q["topic"]] = data["weak"].get(q["topic"], 0) + 1
        correct = q["options"][q["answer"]]
        await query.message.reply_text(f"❌ Wrong!\nCorrect: {correct}")

    data["index"] += 1
    data["answered"] = False

    if data["index"] >= 40:
        await dashboard(update, context)
    else:
        await send_q(update, context)


# ---------------- DASHBOARD ----------------
async def dashboard(update, context):
    user_id = update.effective_user.id
    data = users[user_id]

    time_taken = int(time.time() - data["start"])

    weak = sorted(data["weak"].items(), key=lambda x: x[1], reverse=True)
    weak_text = "\n".join([f"{t}: {c}" for t, c in weak[:5]]) or "None"

    score = data["score"]
    percent = (score / 40) * 100

    await context.bot.send_message(
        user_id,
        f"""
📊 CBT RESULT DASHBOARD

📌 Subject: {data['subject']}
📊 Score: {score}/40 ({percent:.1f}%)
⏱ Time: {time_taken//60}m {time_taken%60}s

🧠 Weak Topics:
{weak_text}

📈 Performance: {"Excellent" if percent>70 else "Average" if percent>50 else "Needs Improvement"}
"""
    )

    del users[user_id]


# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(subject_handler, pattern="^(English|Mathematics|Physics|Chemistry|Biology)$"))
app.add_handler(CallbackQueryHandler(answer_handler, pattern="^(A|B|C|D)$"))

app.run_polling()
