import random

QUESTIONS = {

# ================= MATHEMATICS =================
"Mathematics": [

# Algebra (HIGH FREQUENCY)
{"q": "Solve: 2x + 7 = 3x - 5",
 "o": ["10", "12", "8", "6"],
 "a": "12",
 "exp": "2x + 7 = 3x - 5 → x = 12"},

{"q": "If x² - 9 = 0, find x",
 "o": ["3", "-3", "±3", "9"],
 "a": "±3",
 "exp": "x² = 9 → x = ±3"},

{"q": "Simplify: (x + 2)(x - 2)",
 "o": ["x² - 4", "x² + 4", "x² - 2", "x² + 2"],
 "a": "x² - 4",
 "exp": "(a+b)(a-b)=a²-b²"},

# Trigonometry
{"q": "tan 45° = ?",
 "o": ["0", "1", "√3", "1/2"],
 "a": "1",
 "exp": "Standard trig value"},

{"q": "sin²θ + cos²θ = ?",
 "o": ["1", "0", "2", "-1"],
 "a": "1",
 "exp": "Basic identity"},

# Probability
{"q": "Probability of getting a 6 on a die?",
 "o": ["1/6", "1/2", "1/3", "6"],
 "a": "1/6",
 "exp": "1 favorable out of 6"}
],

# ================= ENGLISH =================
"English": [

# Lexis & Structure (VERY IMPORTANT)
{"q": "Choose correct: Neither the teacher nor the students _____ ready.",
 "o": ["is", "are", "was", "be"],
 "a": "are",
 "exp": "Verb agrees with nearest subject (students)"},

{"q": "She has been waiting _____ two hours.",
 "o": ["since", "for", "from", "at"],
 "a": "for",
 "exp": "Use 'for' with duration"},

# Synonyms
{"q": "Synonym of 'obtain'?",
 "o": ["lose", "get", "reject", "avoid"],
 "a": "get",
 "exp": "Obtain means get"},

# Antonyms
{"q": "Opposite of 'hostile'?",
 "o": ["friendly", "angry", "violent", "rude"],
 "a": "friendly",
 "exp": "Hostile = unfriendly"},

# Interpretation
{"q": "He kicked the bucket means?",
 "o": ["played football", "died", "ran away", "fell"],
 "a": "died",
 "exp": "Idiom meaning"}
],

# ================= PHYSICS =================
"Physics": [

# Mechanics
{"q": "A body of mass 2kg accelerates at 3m/s². Force = ?",
 "o": ["6N", "5N", "3N", "2N"],
 "a": "6N",
 "exp": "F = ma = 2 × 3 = 6N"},

{"q": "Velocity = ?",
 "o": ["distance/time", "displacement/time", "force/time", "mass/time"],
 "a": "displacement/time",
 "exp": "Velocity uses displacement"},

# Electricity
{"q": "V = IR is known as?",
 "o": ["Newton law", "Ohm's law", "Hooke law", "Faraday law"],
 "a": "Ohm's law",
 "exp": "Basic electricity law"}
],

# ================= CHEMISTRY =================
"Chemistry": [

# Atomic Structure
{"q": "Mass number = ?",
 "o": ["protons", "protons + neutrons", "electrons", "atoms"],
 "a": "protons + neutrons",
 "exp": "Mass number = p + n"},

# Bonding
{"q": "Covalent bond involves?",
 "o": ["sharing", "transfer", "loss", "gain"],
 "a": "sharing",
 "exp": "Electrons are shared"},

# Acids & Bases
{"q": "pH of neutral solution?",
 "o": ["0", "7", "14", "1"],
 "a": "7",
 "exp": "Neutral = 7"}
],

# ================= BIOLOGY =================
"Biology": [

# Cell Biology
{"q": "Organelle responsible for energy?",
 "o": ["nucleus", "ribosome", "mitochondria", "cell wall"],
 "a": "mitochondria",
 "exp": "Produces ATP"},

# Genetics
{"q": "Trait passed from parents is?",
 "o": ["gene", "cell", "organ", "protein"],
 "a": "gene",
 "exp": "Genes carry traits"},

# Physiology
{"q": "Blood is pumped by?",
 "o": ["lungs", "brain", "heart", "kidney"],
 "a": "heart",
 "exp": "Heart pumps blood"}
]
}

def generate_questions(subject, count=20):
    q = QUESTIONS[subject][:]
    random.shuffle(q)

    while len(q) < count:
        q.extend(QUESTIONS[subject])
        random.shuffle(q)

    return q[:count]
