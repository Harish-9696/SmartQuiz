import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from bson import ObjectId
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

load_dotenv()

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------------------
# MongoDB connection
# ---------------------------------------------------------------------------
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Please create a .env file with your MongoDB Atlas connection string."
    )

client = MongoClient(MONGO_URI)
db = client.get_database("quizdb")

questions_col = db["questions"]
results_col = db["results"]
users_col = db["users"]

# ---------------------------------------------------------------------------
# Helper: default user (single-user demo app)
# ---------------------------------------------------------------------------
DEFAULT_USER = "Harish"


def _ensure_user():
    """Insert the default user document if it doesn't exist yet."""
    if not users_col.find_one({"name": DEFAULT_USER}):
        users_col.insert_one({"name": DEFAULT_USER})


# ---------------------------------------------------------------------------
# Page Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """
    Home page – shows hero section, quiz categories, and recent scores.
    """
    _ensure_user()

    # Count questions per category for the category cards
    pipeline = [
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ]
    category_counts = {doc["_id"]: doc["count"] for doc in questions_col.aggregate(pipeline)}

    # Pre-defined category list with icons (Font Awesome classes)
    categories = [
        {"name": "General Knowledge", "icon": "fa-globe", "color": "purple"},
        {"name": "Science", "icon": "fa-flask", "color": "blue"},
        {"name": "Technology", "icon": "fa-laptop-code", "color": "teal"},
        {"name": "Mathematics", "icon": "fa-calculator", "color": "orange"},
        {"name": "History", "icon": "fa-landmark", "color": "red"},
        {"name": "Geography", "icon": "fa-map-marked-alt", "color": "green"},
        {"name": "Literature", "icon": "fa-book-open", "color": "pink"},
        {"name": "Sports", "icon": "fa-football-ball", "color": "yellow"},
    ]

    # Attach real question counts (or 0 if none seeded yet)
    for cat in categories:
        cat["count"] = category_counts.get(cat["name"], 0)

    # Recent scores for the current user (latest 5)
    recent_scores = list(
        results_col.find({"user": DEFAULT_USER})
        .sort("date", -1)
        .limit(5)
    )

    return render_template(
        "index.html",
        user=DEFAULT_USER,
        categories=categories,
        recent_scores=recent_scores,
    )


@app.route("/quiz")
def quiz():
    """
    Take Quiz page – lets the user pick a category and start the quiz.
    """
    category_names = sorted(questions_col.distinct("category"))
    return render_template("quiz.html", user=DEFAULT_USER, categories=category_names)


@app.route("/results")
def results():
    """
    Results page – shows summary stats and full quiz history.
    """
    all_results = list(results_col.find({"user": DEFAULT_USER}).sort("date", -1))

    total_quizzes = len(all_results)
    avg_score = 0
    best_score = 0

    if total_quizzes > 0:
        percentages = [
            round((r["score"] / r["total"]) * 100) if r["total"] else 0
            for r in all_results
        ]
        avg_score = round(sum(percentages) / total_quizzes)
        best_score = max(percentages)

    return render_template(
        "results.html",
        user=DEFAULT_USER,
        all_results=all_results,
        total_quizzes=total_quizzes,
        avg_score=avg_score,
        best_score=best_score,
    )


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.route("/start_quiz", methods=["POST"])
def start_quiz():
    """
    API endpoint – returns up to 10 random questions for the given category.
    """
    data = request.get_json(force=True)
    category = data.get("category", "").strip()

    if not category:
        return jsonify({"error": "Category is required"}), 400

    pipeline = [
        {"$match": {"category": category}},
        {"$sample": {"size": 10}},
        {"$project": {"_id": 0, "question": 1, "options": 1, "answer": 1}},
    ]
    questions = list(questions_col.aggregate(pipeline))

    if not questions:
        return jsonify({"error": f"No questions found for category: {category}"}), 404

    return jsonify({"questions": questions})


@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    """
    API endpoint – receives quiz answers, saves results to MongoDB.
    """
    data = request.get_json(force=True)

    category = data.get("category", "Unknown")
    score = int(data.get("score", 0))
    total = int(data.get("total", 0))
    time_taken = data.get("time_taken", "N/A")

    percentage = round((score / total) * 100) if total else 0

    result_doc = {
        "user": DEFAULT_USER,
        "category": category,
        "score": score,
        "total": total,
        "percentage": percentage,
        "time_taken": time_taken,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
    }

    results_col.insert_one(result_doc)

    return jsonify({"message": "Result saved successfully", "percentage": percentage})


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)