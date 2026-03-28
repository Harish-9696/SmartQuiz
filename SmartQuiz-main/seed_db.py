"""
seed_db.py – Seed the SmartQuiz MongoDB database with sample questions.
Run once: python seed_db.py
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Please create a .env file with your MongoDB Atlas connection string."
    )

client = MongoClient(MONGO_URI)
db = client.get_database("quizdb")
questions_col = db["questions"]

QUESTIONS = [
    # General Knowledge
    {"category": "General Knowledge", "question": "What is the capital of France?",
     "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": "Paris"},
    {"category": "General Knowledge", "question": "How many continents are there on Earth?",
     "options": ["5", "6", "7", "8"], "answer": "7"},
    {"category": "General Knowledge", "question": "What is the largest ocean on Earth?",
     "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"},
    {"category": "General Knowledge", "question": "Who painted the Mona Lisa?",
     "options": ["Van Gogh", "Picasso", "Da Vinci", "Michelangelo"], "answer": "Da Vinci"},
    {"category": "General Knowledge", "question": "What is the chemical symbol for gold?",
     "options": ["Go", "Gd", "Au", "Ag"], "answer": "Au"},
    {"category": "General Knowledge", "question": "Which planet is known as the Red Planet?",
     "options": ["Venus", "Mars", "Jupiter", "Saturn"], "answer": "Mars"},
    {"category": "General Knowledge", "question": "What is the longest river in the world?",
     "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "answer": "Nile"},
    {"category": "General Knowledge", "question": "How many sides does a hexagon have?",
     "options": ["5", "6", "7", "8"], "answer": "6"},
    {"category": "General Knowledge", "question": "What is the smallest country in the world?",
     "options": ["Monaco", "San Marino", "Vatican City", "Liechtenstein"], "answer": "Vatican City"},
    {"category": "General Knowledge", "question": "Which element has the atomic number 1?",
     "options": ["Helium", "Oxygen", "Hydrogen", "Carbon"], "answer": "Hydrogen"},

    # Science
    {"category": "Science", "question": "What is the powerhouse of the cell?",
     "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi body"], "answer": "Mitochondria"},
    {"category": "Science", "question": "What gas do plants absorb from the atmosphere?",
     "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": "Carbon Dioxide"},
    {"category": "Science", "question": "What is the speed of light (approx)?",
     "options": ["3×10^6 m/s", "3×10^8 m/s", "3×10^10 m/s", "3×10^12 m/s"], "answer": "3×10^8 m/s"},
    {"category": "Science", "question": "What force keeps planets in orbit around the Sun?",
     "options": ["Magnetism", "Gravity", "Friction", "Electrostatic"], "answer": "Gravity"},
    {"category": "Science", "question": "What is H2O commonly known as?",
     "options": ["Hydrogen peroxide", "Salt water", "Water", "Acid"], "answer": "Water"},
    {"category": "Science", "question": "Which organ pumps blood through the human body?",
     "options": ["Brain", "Liver", "Heart", "Lungs"], "answer": "Heart"},
    {"category": "Science", "question": "What is the boiling point of water at sea level?",
     "options": ["90°C", "95°C", "100°C", "105°C"], "answer": "100°C"},
    {"category": "Science", "question": "How many bones are in the adult human body?",
     "options": ["196", "206", "216", "226"], "answer": "206"},
    {"category": "Science", "question": "What planet is closest to the Sun?",
     "options": ["Venus", "Earth", "Mercury", "Mars"], "answer": "Mercury"},
    {"category": "Science", "question": "What is the hardest natural substance on Earth?",
     "options": ["Gold", "Iron", "Diamond", "Quartz"], "answer": "Diamond"},

    # Technology
    {"category": "Technology", "question": "What does CPU stand for?",
     "options": ["Central Processing Unit", "Computer Power Unit", "Core Processing Unit", "Central Power Unit"],
     "answer": "Central Processing Unit"},
    {"category": "Technology", "question": "What programming language is known as the language of the web (frontend)?",
     "options": ["Python", "Java", "JavaScript", "Ruby"], "answer": "JavaScript"},
    {"category": "Technology", "question": "What does HTML stand for?",
     "options": ["HyperText Markup Language", "High Tech Modern Language", "HyperText Machine Language", "Home Tool Markup Language"],
     "answer": "HyperText Markup Language"},
    {"category": "Technology", "question": "What does SQL stand for?",
     "options": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "Stored Query Language"],
     "answer": "Structured Query Language"},
    {"category": "Technology", "question": "Which company created the Python programming language?",
     "options": ["Google", "Microsoft", "Guido van Rossum (PSF)", "Apple"], "answer": "Guido van Rossum (PSF)"},
    {"category": "Technology", "question": "What does RAM stand for?",
     "options": ["Random Access Memory", "Read Access Memory", "Rapid Access Module", "Read And Modify"],
     "answer": "Random Access Memory"},
    {"category": "Technology", "question": "What does URL stand for?",
     "options": ["Uniform Resource Locator", "Universal Reference Link", "Uniform Reference Locator", "Universal Resource Locator"],
     "answer": "Uniform Resource Locator"},
    {"category": "Technology", "question": "Which data structure uses LIFO order?",
     "options": ["Queue", "Array", "Stack", "Tree"], "answer": "Stack"},
    {"category": "Technology", "question": "What is the binary representation of the decimal number 10?",
     "options": ["1010", "1100", "1001", "1110"], "answer": "1010"},
    {"category": "Technology", "question": "What does API stand for?",
     "options": ["Application Programming Interface", "Automated Process Integration", "Application Process Interface", "Advanced Programming Interface"],
     "answer": "Application Programming Interface"},

    # Mathematics
    {"category": "Mathematics", "question": "What is the value of π (pi) to two decimal places?",
     "options": ["3.12", "3.14", "3.16", "3.18"], "answer": "3.14"},
    {"category": "Mathematics", "question": "What is 12 × 12?",
     "options": ["124", "134", "144", "154"], "answer": "144"},
    {"category": "Mathematics", "question": "What is the square root of 144?",
     "options": ["10", "11", "12", "13"], "answer": "12"},
    {"category": "Mathematics", "question": "What is 15% of 200?",
     "options": ["25", "30", "35", "40"], "answer": "30"},
    {"category": "Mathematics", "question": "Solve: 2x + 5 = 15. What is x?",
     "options": ["3", "4", "5", "6"], "answer": "5"},
    {"category": "Mathematics", "question": "What is the sum of angles in a triangle?",
     "options": ["90°", "180°", "270°", "360°"], "answer": "180°"},
    {"category": "Mathematics", "question": "What is 2^10?",
     "options": ["512", "1024", "2048", "256"], "answer": "1024"},
    {"category": "Mathematics", "question": "What is the area of a circle with radius 7? (Use π ≈ 3.14)",
     "options": ["143.07", "153.94", "163.07", "173.94"], "answer": "153.94"},
    {"category": "Mathematics", "question": "What is the factorial of 5 (5!)?",
     "options": ["60", "100", "120", "150"], "answer": "120"},
    {"category": "Mathematics", "question": "What type of number is √2?",
     "options": ["Integer", "Rational", "Irrational", "Complex"], "answer": "Irrational"},

    # History
    {"category": "History", "question": "In which year did World War II end?",
     "options": ["1943", "1944", "1945", "1946"], "answer": "1945"},
    {"category": "History", "question": "Who was the first President of the United States?",
     "options": ["Abraham Lincoln", "Thomas Jefferson", "George Washington", "John Adams"], "answer": "George Washington"},
    {"category": "History", "question": "Which ancient wonder was located in Alexandria?",
     "options": ["Colossus of Rhodes", "Lighthouse of Alexandria", "Hanging Gardens", "Statue of Zeus"], "answer": "Lighthouse of Alexandria"},
    {"category": "History", "question": "What year did India gain independence?",
     "options": ["1945", "1946", "1947", "1948"], "answer": "1947"},
    {"category": "History", "question": "Who was known as the 'Iron Lady'?",
     "options": ["Angela Merkel", "Indira Gandhi", "Margaret Thatcher", "Golda Meir"], "answer": "Margaret Thatcher"},
    {"category": "History", "question": "The Berlin Wall fell in which year?",
     "options": ["1987", "1988", "1989", "1990"], "answer": "1989"},
    {"category": "History", "question": "Which empire was ruled by Julius Caesar?",
     "options": ["Greek Empire", "Ottoman Empire", "Roman Empire", "Persian Empire"], "answer": "Roman Empire"},
    {"category": "History", "question": "Who invented the telephone?",
     "options": ["Thomas Edison", "Nikola Tesla", "Alexander Graham Bell", "Samuel Morse"], "answer": "Alexander Graham Bell"},
    {"category": "History", "question": "In which city was the Titanic built?",
     "options": ["Liverpool", "Glasgow", "Belfast", "Southampton"], "answer": "Belfast"},
    {"category": "History", "question": "Who wrote the Declaration of Independence?",
     "options": ["George Washington", "Benjamin Franklin", "Thomas Jefferson", "John Adams"], "answer": "Thomas Jefferson"},

    # Geography
    {"category": "Geography", "question": "What is the capital of Australia?",
     "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"], "answer": "Canberra"},
    {"category": "Geography", "question": "Which is the largest country by area?",
     "options": ["Canada", "China", "USA", "Russia"], "answer": "Russia"},
    {"category": "Geography", "question": "On which continent is the Sahara Desert located?",
     "options": ["Asia", "Australia", "South America", "Africa"], "answer": "Africa"},
    {"category": "Geography", "question": "What is the tallest mountain in the world?",
     "options": ["K2", "Kangchenjunga", "Mount Everest", "Lhotse"], "answer": "Mount Everest"},
    {"category": "Geography", "question": "Which country has the most natural lakes?",
     "options": ["USA", "Russia", "Canada", "Brazil"], "answer": "Canada"},
    {"category": "Geography", "question": "What is the capital of Japan?",
     "options": ["Osaka", "Kyoto", "Hiroshima", "Tokyo"], "answer": "Tokyo"},
    {"category": "Geography", "question": "Which ocean is the largest?",
     "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"},
    {"category": "Geography", "question": "The Amazon River flows through which country?",
     "options": ["Peru", "Colombia", "Brazil", "Venezuela"], "answer": "Brazil"},
    {"category": "Geography", "question": "What is the smallest continent?",
     "options": ["Europe", "Antarctica", "Australia", "South America"], "answer": "Australia"},
    {"category": "Geography", "question": "Which country is home to the Great Barrier Reef?",
     "options": ["USA", "Philippines", "Australia", "Indonesia"], "answer": "Australia"},

    # Literature
    {"category": "Literature", "question": "Who wrote 'Romeo and Juliet'?",
     "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "answer": "William Shakespeare"},
    {"category": "Literature", "question": "What is the first book of the Bible?",
     "options": ["Exodus", "Genesis", "Psalms", "Matthew"], "answer": "Genesis"},
    {"category": "Literature", "question": "Who wrote '1984'?",
     "options": ["Aldous Huxley", "George Orwell", "Ray Bradbury", "H.G. Wells"], "answer": "George Orwell"},
    {"category": "Literature", "question": "Which novel features the character Atticus Finch?",
     "options": ["The Great Gatsby", "Of Mice and Men", "To Kill a Mockingbird", "Catcher in the Rye"], "answer": "To Kill a Mockingbird"},
    {"category": "Literature", "question": "Who wrote 'Pride and Prejudice'?",
     "options": ["Charlotte Brontë", "Emily Brontë", "Jane Austen", "Mary Shelley"], "answer": "Jane Austen"},
    {"category": "Literature", "question": "In which Shakespeare play does the character Hamlet appear?",
     "options": ["Othello", "Macbeth", "Hamlet", "King Lear"], "answer": "Hamlet"},
    {"category": "Literature", "question": "Who wrote 'The Odyssey'?",
     "options": ["Sophocles", "Plato", "Homer", "Virgil"], "answer": "Homer"},
    {"category": "Literature", "question": "What is the name of Harry Potter's owl?",
     "options": ["Crookshanks", "Hedwig", "Fawkes", "Scabbers"], "answer": "Hedwig"},
    {"category": "Literature", "question": "Who wrote 'Don Quixote'?",
     "options": ["Dante Alighieri", "Miguel de Cervantes", "Fyodor Dostoevsky", "Leo Tolstoy"], "answer": "Miguel de Cervantes"},
    {"category": "Literature", "question": "The character 'Jay Gatsby' appears in which novel?",
     "options": ["The Sun Also Rises", "Brave New World", "The Great Gatsby", "Moby Dick"], "answer": "The Great Gatsby"},

    # Sports
    {"category": "Sports", "question": "How many players are on a standard soccer (football) team?",
     "options": ["9", "10", "11", "12"], "answer": "11"},
    {"category": "Sports", "question": "In which sport is the term 'love' used to mean zero?",
     "options": ["Badminton", "Squash", "Tennis", "Ping Pong"], "answer": "Tennis"},
    {"category": "Sports", "question": "How many rings are on the Olympic flag?",
     "options": ["4", "5", "6", "7"], "answer": "5"},
    {"category": "Sports", "question": "Which country won the FIFA World Cup in 2018?",
     "options": ["Brazil", "Germany", "Croatia", "France"], "answer": "France"},
    {"category": "Sports", "question": "How long is a standard marathon?",
     "options": ["26.1 miles", "26.2 miles", "26.3 miles", "26.4 miles"], "answer": "26.2 miles"},
    {"category": "Sports", "question": "What sport is played at Wimbledon?",
     "options": ["Cricket", "Golf", "Tennis", "Polo"], "answer": "Tennis"},
    {"category": "Sports", "question": "How many players are there in a basketball team on court?",
     "options": ["4", "5", "6", "7"], "answer": "5"},
    {"category": "Sports", "question": "Which country is known as the birthplace of the Olympic Games?",
     "options": ["Italy", "Egypt", "Greece", "Turkey"], "answer": "Greece"},
    {"category": "Sports", "question": "In cricket, how many balls are in an over?",
     "options": ["4", "5", "6", "7"], "answer": "6"},
    {"category": "Sports", "question": "Which athlete is known as the 'fastest man in the world'?",
     "options": ["Carl Lewis", "Asafa Powell", "Usain Bolt", "Yohan Blake"], "answer": "Usain Bolt"},
]


def seed():
    questions_col.delete_many({})
    questions_col.insert_many(QUESTIONS)
    print(f"Seeded {len(QUESTIONS)} questions across 8 categories.")


if __name__ == "__main__":
    seed()