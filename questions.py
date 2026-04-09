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

    if subject == "Mathematics":

        if topic == "Algebra":
            x = random.randint(2, 15)
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
                "exp": "Isolate x then divide",
                "topic": "Algebra"
            }

        if topic == "Probability":
            return {
                "q": "Probability of head in a fair coin toss?",
                "options": {"A": "1", "B": "1/2", "C": "1/3", "D": "0"},
                "answer": "B",
                "exp": "1 favorable out of 2 outcomes",
                "topic": "Probability"
            }

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
                "q": "Where did Mary go? (Library passage)",
                "passage": "Mary went to the library to study quietly.",
                "type": "comprehension",
                "options": {"A": "Market", "B": "Library", "C": "School", "D": "Home"},
                "answer": "B",
                "exp": "Passage states library",
                "topic": "Comprehension"
            }

    if subject == "Physics":
        return {
            "q": "Force is equal to?",
            "options": {"A": "mv", "B": "ma", "C": "m/a", "D": "v/t"},
            "answer": "B",
            "exp": "Newton's second law",
            "topic": topic
        }

    if subject == "Chemistry":
        return {
            "q": "Atomic number represents number of?",
            "options": {"A": "neutrons", "B": "protons", "C": "electrons", "D": "ions"},
            "answer": "B",
            "exp": "Atomic number = protons",
            "topic": topic
        }

    if subject == "Biology":
        return {
            "q": "Basic unit of life is?",
            "options": {"A": "organ", "B": "tissue", "C": "cell", "D": "system"},
            "answer": "C",
            "exp": "Cell is smallest unit",
            "topic": topic
        }
