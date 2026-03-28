# SmartQuiz

SmartQuiz is a full-stack quiz web application built with **Flask**, **MongoDB**, **Bootstrap 5**, and **Vanilla JavaScript**.

It supports:

- Student signup and login
- Admin login
- Role-based access control
- Quiz categories
- Random quiz questions
- Result saving in MongoDB
- Student result history
- Admin question management
- Admin result viewing

---

## Features

### Student features
- Create a new account
- Log in as a student
- Choose a quiz category
- Take a 10-question quiz
- See score and time taken
- View past results

### Admin features
- Log in as admin
- View dashboard statistics
- Add new quiz questions
- Edit existing questions
- Delete questions
- View all student results

### Quiz features
- 8 categories:
  - General Knowledge
  - Science
  - Technology
  - Mathematics
  - History
  - Geography
  - Literature
  - Sports
- Randomized questions from MongoDB
- Score calculation
- Result storage
- Time tracking

---

## Project Structure

```text
SmartQuiz/
├── app.py
├── seed_db.py
├── Procfile
├── render.yaml
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── admin_login.html
│   ├── quiz.html
│   ├── results.html
│   ├── admin_dashboard.html
│   ├── admin_results.html
│   ├── manage_questions.html
│   ├── add_question.html
│   └── edit_question.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        ├── form-validation.js
        └── quiz.js
```

---

## Requirements

### What you need installed
Before running SmartQuiz, make sure you have:

- **Python 3.10+**
- **pip**
- **MongoDB Atlas account**
- **A web browser**
- Optional: **Git**

---

## Setup Guide for Beginners

Follow these steps carefully.

---

### Step 1: Download or clone the project

If you have the code in a Git repository:

```bash
git clone <your-repository-url>
cd SmartQuiz
```

If you downloaded the ZIP file, extract it and open the project folder.

---

### Step 2: Create a virtual environment

It is strongly recommended to use a virtual environment.

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

If activated correctly, your terminal will show `(venv)`.

---

### Step 3: Install dependencies

Run:

```bash
pip install -r requirements.txt
```

This installs:
- Flask
- PyMongo
- Gunicorn
- python-dotenv

---

### Step 4: Create the `.env` file

Create a file named `.env` in the project root.

Example:

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/quizdb?retryWrites=true&w=majority
SECRET_KEY=your-secret-key-here
ADMIN_EMAIL=admin@quiz.com
ADMIN_PASSWORD=admin123
```

#### What these variables mean
- `MONGO_URI` → your MongoDB Atlas connection string
- `SECRET_KEY` → Flask session secret
- `ADMIN_EMAIL` → admin login email
- `ADMIN_PASSWORD` → admin login password

---

### Step 5: Seed the database with questions

Before running the app, load sample questions into MongoDB:

```bash
python seed_db.py
```

This creates the `questions` collection and inserts quiz questions for all 8 categories.

---

### Step 6: Run the app locally

Start the Flask app:

```bash
python app.py
```

Then open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## Login Details

### Student
- Sign up using the signup page
- Then log in with your new email/password

### Admin
Default admin login:

```text
Email: admin@quiz.com
Password: admin123
```

You can change these in `.env`.

---

## How the app works

### Home page
- Shows the SmartQuiz landing page
- Displays quiz categories
- Links to login/signup

### Student quiz flow
1. Log in as student
2. Go to quiz page
3. Select a category
4. Click **Start Quiz**
5. Answer questions
6. View result
7. Result gets saved to MongoDB

### Results page
- Shows your previous quiz attempts
- Displays score, percentage, and time taken

### Admin dashboard
- Shows total questions
- Shows total students
- Shows total quizzes taken
- Links to question management and results

---

## MongoDB Collections

SmartQuiz uses these collections inside the `quizdb` database:

### `users`
Stores student and admin account data.

Example fields:
```json
{
  "name": "John Doe",it credential reject https//
  "email": "john@example.com",
  "password": "<hashed-password>",
  "role": "student"
}
```

### `questions`
Stores quiz questions.

Example fields:
```json
{
  "question": "What is the capital of France?",
  "options": ["Berlin", "Madrid", "Paris", "Rome"],
  "answer": "Paris",
  "category": "General Knowledge"
}
```

### `results`
Stores quiz results.

Example fields:
```json
{
  "user_email": "john@example.com",
  "user_name": "John Doe",
  "score": 8,
  "total": 10,
  "percentage": 80,
  "category": "Science",
  "time_taken": "1m 22s",
  "date": "2026-03-28T10:30:00Z"
}
```

---

## Deployment on Render

If you want to deploy this app to Render, follow these steps.

### Step 1: Push to GitHub
Make sure the project is pushed to GitHub.

### Step 2: Create a Web Service on Render
- Go to [Render](https://render.com)
- Create a new **Web Service**
- Connect your GitHub repository

### Step 3: Set build and start commands

#### Build Command
```bash
pip install -r requirements.txt
```

#### Start Command
```bash
gunicorn app:app
```

### Step 4: Add environment variables
Set these in Render:
- `MONGO_URI`
- `SECRET_KEY`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`

### Step 5: Seed MongoDB
Run:

```bash
python seed_db.py
```

You can do this locally or through Render shell if available.

---

## Important Files

### `app.py`
Main Flask application with all routes.

### `seed_db.py`
Seeds the MongoDB questions collection.

### `quiz.js`
Handles:
- category selection
- quiz loading
- timer
- scoring
- result submission

### `style.css`
Contains all custom styles for the UI.

### `base.html`
Shared layout used by all pages.

---

## Common Issues and Fixes

### 1. Template not found
If Flask says a template is missing, make sure the file exists in the `templates/` folder and the filename matches exactly.

### 2. MongoDB connection error
Check your `.env` file and confirm `MONGO_URI` is valid.

### 3. Quiz score shows 0
Make sure:
- `quiz.js` sends `score` and `total`
- `app.py` stores those values
- `start_quiz` returns `answer`

### 4. Admin results page crashes
Make sure saved result dates are stored as real datetime objects:

```python
"date": datetime.now(timezone.utc)
```

### 5. Admin dashboard shows wrong categories
Run `python seed_db.py` again so the `questions` collection contains all 8 categories.

---

## Development Notes

- The quiz uses random questions from MongoDB
- Questions are selected with `$sample`
- Student answers are checked client-side for immediate scoring
- Final score is saved to MongoDB
- Admin can manage quiz content without editing code

---

## Security Notes

- Do not commit `.env` to GitHub
- Keep `SECRET_KEY` private
- Change default admin credentials before deployment
- Use MongoDB Atlas access restrictions if possible

---

## Recommended Python Version

Use Python 3.10 or newer.

---

## License

Add your own license if needed.

---

## Support

If something is not working:
1. Check `.env`
2. Re-run `seed_db.py`
3. Restart Flask
4. Clear browser cache
5. Check browser console and terminal logs

---

## Quick Start Summary

```bash
git clone <repo-url>
cd SmartQuiz
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python seed_db.py
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## Default Admin Login

```text
Email: admin@quiz.com
Password: admin123
```

---

SmartQuiz is now ready to use.