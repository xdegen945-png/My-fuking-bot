import os
import time
import threading
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from questions import generate_question

TOKEN = os.getenv("BOT_TOKEN")

users = {}
EXAM_TIME = 30 * 60


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["English", "Mathematics"],
        ["Physics", "Chemistry"],
        ["Biology"]
    ]

    await update.message.reply_text(
        "📚 CBT MODE READY\nSelect subject:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# ---------------- TIMER ----------------
def auto_submit(user_id):
    if user_id in users:
        users[user_id]["submitted"] = True


# ---------------- UNIQUE QUESTION ----------------
def get_question(user_id):
    data = users[user_id]

    while True:
        q = generate_question(data["subject"])
        if q["q"] not in data["used"]:
            data["used"].add(q["q"])
            return q


# ---------------- SEND QUESTION ----------------
async def send_q(update, context):
    user_id = update.effective_user.id
    data = users[user_id]

    q = get_question(user_id)
    data["current_q"] = q

    if q.get("type") == "comprehension":
        text = f"""
📖 PASSAGE:

{q['passage']}

❓ {q['q']}
"""
    else:
        text = f"""
📘 Question {data['index']+1}/40

{q['q']}

A. {q['options']['A']}
B. {q['options']['B']}
C. {q['options']['C']}
D. {q['options']['D']}
"""

    keyboard = ReplyKeyboardMarkup(
        [["A", "B"], ["C", "D"]],
        resize_keyboard=True
    )

    await context.bot.send_message(user_id, text, reply_markup=keyboard)


# ---------------- SUBJECT SELECT ----------------
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    subjects = ["English", "Mathematics", "Physics", "Chemistry", "Biology"]

    # START EXAM
    if text in subjects:

        users[user_id] = {
            "subject": text,
            "index": 0,
            "score": 0,
            "weak": {},
            "start": time.time(),
            "submitted": False,
            "answered": False,
            "used": set(),
            "current_q": None
        }

        threading.Timer(EXAM_TIME, auto_submit, args=[user_id]).start()

        await send_q(update, context)
        return

    # IF NO EXAM
    if user_id not in users:
        await update.message.reply_text("Please select a subject first.")
        return

    data = users[user_id]

    if data["submitted"]:
        await dashboard(update, context)
        return

    q = data["current_q"]

    # IGNORE DOUBLE ANSWER
    if data["answered"]:
        return

    if text not in ["A", "B", "C", "D"]:
        await update.message.reply_text("Reply with A, B, C or D only.")
        return

    data["answered"] = True

    # CHECK ANSWER
    if text == q["answer"]:
        data["score"] += 1
        await update.message.reply_text("✅ Correct!\n\n📖 " + q["exp"])
    else:
        data["weak"][q["topic"]] = data["weak"].get(q["topic"], 0) + 1
        correct = q["options"][q["answer"]]
        await update.message.reply_text(f"❌ Wrong!\nCorrect: {correct}\n\n📖 {q['exp']}")

    # NEXT QUESTION FIX (THIS WAS YOUR MAIN BUG)
    data["index"] += 1
    data["answered"] = False

    if data["index"] >= 40:
        await dashboard(update, context)
    else:
        await send_q(update, context)


# ---------------- DASHBOARD ----------------
async def dashboard(update, context):
    user_id = update.message.from_user.id if update.message else update.effective_user.id
    data = users[user_id]

    time_taken = int(time.time() - data["start"])

    weak = sorted(data["weak"].items(), key=lambda x: x[1], reverse=True)
    weak_text = "\n".join([f"- {t}: {c}" for t, c in weak[:5]]) or "None 🎉"

    score = data["score"]
    percent = (score / 40) * 100

    await context.bot.send_message(
        user_id,
        f"""
📊 FINAL CBT RESULT

📌 Subject: {data['subject']}
📊 Score: {score}/40 ({percent:.1f}%)
⏱ Time: {time_taken//60}m {time_taken%60}s

🧠 Weak Topics:
{weak_text}

📈 Performance:
{"Excellent" if percent > 70 else "Average" if percent > 50 else "Needs Improvement"}
"""
    )

    del users[user_id]


# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
