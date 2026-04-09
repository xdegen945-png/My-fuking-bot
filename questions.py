import random

TOPICS = {
    "Mathematics": {
        "core": ["Algebra", "Trigonometry", "Geometry", "Probability"],
        "extra": ["Sets", "Indices"]
    },
    "English": {
        "core": ["Grammar", "Lexis", "Comprehension", "Synonyms"],
        "extra": ["Antonyms", "Sentence Correction"]
    },
    "Physics": {
        "core": ["Mechanics", "Electricity", "Waves"],
        "extra": ["Heat"]
    },
    "Chemistry": {
        "core": ["Atomic Structure", "Bonding", "Acids"],
        "extra": ["Periodic Table"]
    },
    "Biology": {
        "core": ["Cell Biology", "Genetics", "Ecology"],
        "extra": ["Nutrition"]
    }
}


def generate_question(subject):
    import random

    topic_group = TOPICS[subject]

    # 70% core, 30% extra
    if random.random() < 0.7:
        topic = random.choice(topic_group["core"])
    else:
        topic = random.choice(topic_group["extra"])

    # ---------------- MATHEMATICS ----------------
    if subject == "Mathematics":

        if topic == "Algebra":
            x = random.randint(2, 10)
            b = random.randint(1, 20)

            return {
                "q": f"Solve: 2x + {b} = {2*x + b}",
                "options": {
                    "A": str(x),
                    "B": str(x+1),
                    "C": str(x-1),
                    "D": str(x+2)
                },
                "answer": "A",
                "exp": "Isolate x then divide by 2",
                "topic": "Algebra"
            }

        if topic == "Trigonometry":
            return {
                "q": "sin 30° = ?",
                "options": {
                    "A": "1",
                    "B": "1/2",
                    "C": "0",
                    "D": "√3"
                },
                "answer": "B",
                "exp": "Standard trig value",
                "topic": "Trigonometry"
            }

        if topic == "Probability":
            return {
                "q": "Probability of head in a fair coin toss?",
                "options": {
                    "A": "1",
                    "B": "1/3",
                    "C": "1/2",
                    "D": "2"
                },
                "answer": "C",
                "exp": "1 favorable / 2 outcomes",
                "topic": "Probability"
            }

    # ---------------- ENGLISH ----------------
    if subject == "English":

        if topic == "Grammar":
            return {
                "q": "She ____ to school yesterday.",
                "options": {
                    "A": "go",
                    "B": "goes",
                    "C": "went",
                    "D": "going"
                },
                "answer": "C",
                "exp": "Past tense required",
                "topic": "Grammar"
            }

        if topic == "Synonyms":
            return {
                "q": "Synonym of 'rapid'?",
                "options": {
                    "A": "slow",
                    "B": "fast",
                    "C": "weak",
                    "D": "late"
                },
                "answer": "B",
                "exp": "Rapid means fast",
                "topic": "Synonyms"
            }

    # ---------------- PHYSICS ----------------
    if subject == "Physics":

        return {
            "q": "Force is equal to?",
            "options": {
                "A": "mv",
                "B": "ma",
                "C": "m/a",
                "D": "v/t"
            },
            "answer": "B",
            "exp": "Newton's second law: F = ma",
            "topic": topic
        }

    # ---------------- CHEMISTRY ----------------
    if subject == "Chemistry":

        return {
            "q": "Atomic number is number of?",
            "options": {
                "A": "neutrons",
                "B": "protons",
                "C": "electrons",
                "D": "molecules"
            },
            "answer": "B",
            "exp": "Atomic number = protons",
            "topic": topic
        }

    # ---------------- BIOLOGY ----------------
    if subject == "Biology":

        return {
            "q": "Basic unit of life is?",
            "options": {
                "A": "organ",
                "B": "tissue",
                "C": "cell",
                "D": "system"
            },
            "answer": "C",
            "exp": "Cell is the smallest unit of life",
            "topic": topic
        }
