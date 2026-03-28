"""
SmartQuiz Flask Application
============================
Multi-user quiz web app with:
  - Student signup / login
  - Admin login with hardcoded credentials
  - Role-based access control
  - MongoDB (PyMongo) integration
  - Quiz taking and result viewing
"""

import os
from datetime import datetime, timezone
from functools import wraps

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "smartquiz-default-secret-key")

MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI is not set. Please create a .env file with your MongoDB Atlas connection string."
    )

client = MongoClient(MONGO_URI)
db = client.get_database("quizdb")

users_col = db["users"]
questions_col = db["questions"]
results_col = db["results"]

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@quiz.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_email" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "student":
            flash("Student access required.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def _build_categories():
    pipeline = [{"$group": {"_id": "$category", "count": {"$sum": 1}}}]
    category_counts = {doc["_id"]: doc["count"] for doc in questions_col.aggregate(pipeline)}

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

    for cat in categories:
        cat["count"] = category_counts.get(cat["name"], 0)

    return categories


@app.route("/")
def index():
    recent_scores = []
    if session.get("user_email"):
        recent_scores = list(
            results_col.find({"user_email": session["user_email"]}).sort("date", -1).limit(5)
        )

    return render_template(
        "index.html",
        categories=_build_categories(),
        recent_scores=recent_scores
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("signup.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("signup.html")

        if users_col.find_one({"email": email}):
            flash("Email already registered. Please log in.", "warning")
            return redirect(url_for("login"))

        users_col.insert_one({
            "name": name,
            "email": email,
            "password": generate_password_hash(password),
            "role": "student"
        })

        flash("Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = users_col.find_one({"email": email, "role": "student"})
        if user and check_password_hash(user["password"], password):
            session["user_email"] = email
            session["user_name"] = user["name"]
            session["role"] = "student"
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("quiz_home"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session["user_email"] = email
            session["user_name"] = "Admin"
            session["role"] = "admin"
            flash("Welcome, Admin!", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Invalid admin credentials.", "danger")

    return render_template("admin_login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@app.route("/quiz")
@login_required
@student_required
def quiz_home():
    categories = sorted(questions_col.distinct("category"))
    return render_template("quiz.html", categories=categories)


@app.route("/start_quiz", methods=["POST"])
@login_required
@student_required
def start_quiz():
    data = request.get_json(force=True)
    category = data.get("category", "").strip()

    if not category:
        return jsonify({"error": "Category is required."}), 400

    questions = list(
        questions_col.aggregate([
            {"$match": {"category": category}},
            {"$sample": {"size": 10}},
            {"$project": {"_id": 1, "question": 1, "options": 1, "answer": 1}}
        ])
    )

    if not questions:
        return jsonify({"error": f"No questions found for category: {category}"}), 404

    for q in questions:
        q["_id"] = str(q["_id"])

    return jsonify({"questions": questions})


@app.route("/submit_quiz", methods=["POST"])
@login_required
@student_required
def submit_quiz():
    data = request.get_json(force=True)

    category = data.get("category", "")
    score = int(data.get("score", 0))
    total = int(data.get("total", 0))
    time_taken = data.get("time_taken", "N/A")

    if not category or total <= 0:
        return jsonify({"error": "Invalid submission."}), 400

    percentage = round((score / total) * 100) if total else 0

    results_col.insert_one({
        "user_email": session["user_email"],
        "user_name": session["user_name"],
        "score": score,
        "total": total,
        "percentage": percentage,
        "category": category,
        "time_taken": time_taken,
        "date": datetime.now(timezone.utc)
    })

    return jsonify({"message": "Result saved successfully", "percentage": percentage})


@app.route("/results")
@login_required
@student_required
def results():
    student_results = list(
        results_col.find({"user_email": session["user_email"]}).sort("date", -1)
    )
    return render_template("results.html", results=student_results)


@app.route("/admin-dashboard")
@admin_required
def admin_dashboard():
    total_questions = questions_col.count_documents({})
    total_students = users_col.count_documents({"role": "student"})
    total_results = results_col.count_documents({})
    categories = questions_col.distinct("category")

    return render_template(
        "admin_dashboard.html",
        total_questions=total_questions,
        total_students=total_students,
        total_results=total_results,
        categories=categories
    )


@app.route("/add-question", methods=["GET", "POST"])
@admin_required
def add_question():
    categories = questions_col.distinct("category")

    if request.method == "POST":
        question_text = request.form.get("question", "").strip()
        option1 = request.form.get("option1", "").strip()
        option2 = request.form.get("option2", "").strip()
        option3 = request.form.get("option3", "").strip()
        option4 = request.form.get("option4", "").strip()
        correct_answer = request.form.get("answer", "").strip()
        category = request.form.get("category", "").strip()
        new_category = request.form.get("new_category", "").strip()

        if new_category:
            category = new_category

        if not all([question_text, option1, option2, option3, option4, correct_answer, category]):
            flash("All fields are required.", "danger")
            return render_template("add_question.html", categories=categories)

        questions_col.insert_one({
            "question": question_text,
            "options": [option1, option2, option3, option4],
            "answer": correct_answer,
            "category": category
        })

        flash("Question added successfully!", "success")
        return redirect(url_for("manage_questions"))

    return render_template("add_question.html", categories=categories)


@app.route("/edit-question/<question_id>", methods=["GET", "POST"])
@admin_required
def edit_question(question_id):
    try:
        oid = ObjectId(question_id)
    except Exception:
        flash("Invalid question ID.", "danger")
        return redirect(url_for("manage_questions"))

    question = questions_col.find_one({"_id": oid})
    categories = questions_col.distinct("category")

    if not question:
        flash("Question not found.", "danger")
        return redirect(url_for("manage_questions"))

    if request.method == "POST":
        question_text = request.form.get("question", "").strip()
        option1 = request.form.get("option1", "").strip()
        option2 = request.form.get("option2", "").strip()
        option3 = request.form.get("option3", "").strip()
        option4 = request.form.get("option4", "").strip()
        correct_answer = request.form.get("answer", "").strip()
        category = request.form.get("category", "").strip()
        new_category = request.form.get("new_category", "").strip()

        if new_category:
            category = new_category

        if not all([question_text, option1, option2, option3, option4, correct_answer, category]):
            flash("All fields are required.", "danger")
            return render_template("edit_question.html", question=question, categories=categories)

        questions_col.update_one(
            {"_id": oid},
            {"$set": {
                "question": question_text,
                "options": [option1, option2, option3, option4],
                "answer": correct_answer,
                "category": category
            }}
        )

        flash("Question updated successfully!", "success")
        return redirect(url_for("manage_questions"))

    return render_template("edit_question.html", question=question, categories=categories)


@app.route("/delete-question/<question_id>", methods=["POST"])
@admin_required
def delete_question(question_id):
    try:
        oid = ObjectId(question_id)
    except Exception:
        flash("Invalid question ID.", "danger")
        return redirect(url_for("manage_questions"))

    questions_col.delete_one({"_id": oid})
    flash("Question deleted.", "success")
    return redirect(url_for("manage_questions"))


@app.route("/manage-questions")
@admin_required
def manage_questions():
    category_filter = request.args.get("category", "")
    query = {"category": category_filter} if category_filter else {}
    questions = list(questions_col.find(query))
    categories = questions_col.distinct("category")

    return render_template(
        "manage_questions.html",
        questions=questions,
        categories=categories,
        selected_category=category_filter
    )


@app.route("/admin-results")
@admin_required
def admin_results():
    all_results = list(results_col.find().sort("date", -1))
    return render_template("admin_results.html", results=all_results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)