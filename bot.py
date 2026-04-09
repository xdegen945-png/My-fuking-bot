import os
import time
import json
import threading
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from questions import generate_question

TOKEN = os.getenv("BOT_TOKEN")

users = {}
EXAM_TIME = 30 * 60

HISTORY_FILE = "history.json"


# ---------------- LOAD HISTORY ----------------
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


history = load_history()


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["English", "Mathematics"],
        ["Physics", "Chemistry"],
        ["Biology"]
    ]

    await update.message.reply_text(
        "📚 JAMB CBT PRO MODE\nSelect subject:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


# ---------------- PROGRESS BAR ----------------
def progress_bar(current, total=40):
    filled = int((current / total) * 10)
    empty = 10 - filled
    return "█" * filled + "░" * empty


# ---------------- TIMER ----------------
def auto_submit(user_id):
    if user_id in users:
        users[user_id]["finished"] = True


# ---------------- HARDER QUESTION ENGINE ----------------
def get_question(user_id):
    user = users[user_id]

    while True:
        q = generate_question(user["subject"])

        # difficulty scaling (JAMB harder mode)
        if user["index"] < 15:
            level_ok = True
        elif user["index"] < 30:
            level_ok = True
        else:
            level_ok = True  # placeholder for harder mode expansion

        if q["q"] not in user["used"] and level_ok:
            user["used"].add(q["q"])
            user["current"] = q
            return q


# ---------------- SEND QUESTION ----------------
async def send_q(update, context):
    user_id = update.effective_user.id
    user = users[user_id]

    q = get_question(user_id)

    bar = progress_bar(user["index"])

    if q.get("type") == "comprehension":
        text = f"""
📖 PASSAGE:

{q['passage']}

❓ {q['q']}

{bar} {user['index']}/40
"""
    else:
        text = f"""
📘 JAMB CBT QUESTION

{q['q']}

A. {q['options']['A']}
B. {q['options']['B']}
C. {q['options']['C']}
D. {q['options']['D']}

{bar} {user['index']}/40
"""

    keyboard = ReplyKeyboardMarkup(
        [["A", "B"], ["C", "D"]],
        resize_keyboard=True
    )

    await context.bot.send_message(user_id, text, reply_markup=keyboard)


# ---------------- HANDLE ----------------
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
            "used": set(),
            "current": None,
            "answered": False,
            "start": time.time(),
            "finished": False
        }

        threading.Timer(EXAM_TIME, auto_submit, args=[user_id]).start()

        await send_q(update, context)
        return

    if user_id not in users:
        await update.message.reply_text("Select subject first.")
        return

    user = users[user_id]

    if text not in ["A", "B", "C", "D"]:
        await update.message.reply_text("Use A, B, C or D only.")
        return

    if user["answered"]:
        return

    user["answered"] = True

    q = user["current"]

    # CHECK ANSWER
    if text == q["answer"]:
        user["score"] += 1
        await update.message.reply_text("✅ Correct!\n\n📖 " + q["exp"])
    else:
        user["weak"][q["topic"]] = user["weak"].get(q["topic"], 0) + 1
        correct = q["options"][q["answer"]]
        await update.message.reply_text(f"❌ Wrong!\nCorrect: {correct}")

    user["index"] += 1
    user["answered"] = False

    if user["index"] >= 40:
        await finish(update, context)
    else:
        await send_q(update, context)


# ---------------- FINISH + SAVE HISTORY ----------------
async def finish(update, context):

    user_id = update.message.from_user.id
    user = users[user_id]

    time_taken = int(time.time() - user["start"])
    percent = (user["score"] / 40) * 100

    record = {
        "subject": user["subject"],
        "score": user["score"],
        "percent": percent,
        "time": time_taken,
        "date": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    history.setdefault(str(user_id), []).append(record)
    save_history(history)

    await context.bot.send_message(
        user_id,
        f"""
📊 FINAL CBT RESULT

📌 Subject: {user['subject']}
📊 Score: {user['score']}/40 ({percent:.1f}%)

⏱ Time: {time_taken//60}m {time_taken%60}s

📈 Performance:
{"Excellent" if percent > 70 else "Average" if percent > 50 else "Needs Improvement"}
"""
    )

    del users[user_id]


# ---------------- HISTORY COMMAND ----------------
async def history_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = str(update.message.from_user.id)

    if user_id not in history:
        await update.message.reply_text("No exam history yet.")
        return

    text = "📚 EXAM HISTORY\n\n"

    for i, r in enumerate(history[user_id][-5:]):
        text += f"""
{i+1}. {r['subject']}
Score: {r['score']}/40 ({r['percent']:.1f}%)
Time: {r['time']} sec
Date: {r['date']}
--------------------
"""

    await update.message.reply_text(text)


# ---------------- RUN ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("history", history_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
