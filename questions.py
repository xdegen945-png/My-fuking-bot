import random

TOPICS = {
    "Mathematics": {
        "core": ["Algebra", "Trigonometry", "Probability"],
        "extra": ["Sets", "Indices"]
    },
    "English": {
        "core": ["Grammar", "Lexis", "Comprehension"],
        "extra": ["Synonyms", "Antonyms"]
    },
    "Physics": {
        "core": ["Mechanics", "Electricity"],
        "extra": ["Waves"]
    },
    "Chemistry": {
        "core": ["Atomic Structure", "Acids"],
        "extra": ["Bonding"]
    },
    "Biology": {
        "core": ["Cell Biology", "Genetics"],
        "extra": ["Ecology"]
    }
}


def generate_question(subject):
    group = TOPICS[subject]

    topic = random.choice(group["core"] if random.random() < 0.7 else group["extra"])

    # ---------------- MATHEMATICS ----------------
    if subject == "Mathematics":

        if topic == "Algebra":
            x = random.randint(2, 12)
            b = random.randint(1, 20)

            return {
                "q": f"Solve: 3x + {b} = {3*x + b}",
                "options": {
                    "A": str(x),
                    "B": str(x+1),
                    "C": str(x-1),
                    "D": str(x+2)
                },
                "answer": "A",
                "exp": "Isolate x and divide",
                "topic": "Algebra"
            }

        if topic == "Probability":
            return {
                "q": "A coin is tossed once. Probability of head?",
                "options": {"A": "1", "B": "1/2", "C": "1/3", "D": "0"},
                "answer": "B",
                "exp": "One favorable outcome over two",
                "topic": "Probability"
            }

    # ---------------- ENGLISH ----------------
    if subject == "English":

        if topic == "Grammar":
            return {
                "q": "She ____ to school yesterday.",
                "options": {"A": "go", "B": "goes", "C": "went", "D": "going"},
                "answer": "C",
                "exp": "Past tense required",
                "topic": "Grammar"
            }

        if topic == "Comprehension":
            return {
                "type": "comprehension",
                "passage": "Mary went to the library to study. She borrowed two books and read quietly for hours.",
                "q": "Where did Mary go?",
                "options": {"A": "Market", "B": "Library", "C": "School", "D": "Home"},
                "answer": "B",
                "exp": "The passage says she went to the library.",
                "topic": "Comprehension"
            }

    # ---------------- PHYSICS ----------------
    if subject == "Physics":
        return {
            "q": "Force is equal to?",
            "options": {"A": "mv", "B": "ma", "C": "m/a", "D": "v/t"},
            "answer": "B",
            "exp": "Newton's second law",
            "topic": topic
        }

    # ---------------- CHEMISTRY ----------------
    if subject == "Chemistry":
        return {
            "q": "Atomic number is number of?",
            "options": {"A": "neutrons", "B": "protons", "C": "electrons", "D": "ions"},
            "answer": "B",
            "exp": "Atomic number = protons",
            "topic": topic
        }

    # ---------------- BIOLOGY ----------------
    if subject == "Biology":
        return {
            "q": "Basic unit of life is?",
            "options": {"A": "organ", "B": "tissue", "C": "cell", "D": "system"},
            "answer": "C",
            "exp": "Cell is smallest unit",
            "topic": topic
        }
