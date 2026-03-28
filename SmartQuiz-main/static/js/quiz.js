/**
 * SmartQuiz Frontend Logic
 * Dropdown flow + proper answer tracking
 */

const setupPanel = document.getElementById("setupPanel");
const categorySelect = document.getElementById("categorySelect");
const startQuizBtn = document.getElementById("startQuizBtn");
const setupError = document.getElementById("setupError");

const quizPanel = document.getElementById("quizPanel");
const quizCategoryLabel = document.getElementById("quizCategoryLabel");
const timerDisplay = document.getElementById("timerDisplay");
const timerText = document.getElementById("timerText");
const quizProgressBar = document.getElementById("quizProgressBar");
const questionCounter = document.getElementById("questionCounter");
const scoreCounter = document.getElementById("scoreCounter");
const questionText = document.getElementById("questionText");
const optionsContainer = document.getElementById("optionsContainer");
const nextBtn = document.getElementById("nextBtn");

const resultPanel = document.getElementById("resultPanel");
const scoreText = document.getElementById("scoreText");
const resultHeading = document.getElementById("resultHeading");
const resultSubtext = document.getElementById("resultSubtext");
const resultProgressBar = document.getElementById("resultProgressBar");
const resultPercentageText = document.getElementById("resultPercentageText");
const statCorrect = document.getElementById("statCorrect");
const statWrong = document.getElementById("statWrong");
const statTime = document.getElementById("statTime");
const retakeBtn = document.getElementById("retakeBtn");

let questions = [];
let currentIndex = 0;
let selectedAnswer = null;
let score = 0;
let timerInterval = null;
let secondsLeft = 600;
let startTimeStamp = null;
let chosenCategory = "";
let answers = {};   // <-- IMPORTANT: store answers here

startQuizBtn.addEventListener("click", async function () {
  chosenCategory = categorySelect.value;

  if (!chosenCategory) {
    showSetupError("Please select a category before starting the quiz.");
    return;
  }

  hideSetupError();
  startQuizBtn.disabled = true;
  startQuizBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i>Loading…';

  try {
    const response = await fetch("/start_quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ category: chosenCategory }),
    });

    const data = await response.json();

    if (!response.ok) {
      showSetupError(data.error || "Failed to load questions. Please try again.");
      resetStartButton();
      return;
    }

    questions = data.questions;
    beginQuiz();
  } catch (err) {
    showSetupError("Connection error. Please check your network and try again.");
    resetStartButton();
  }
});

function beginQuiz() {
  currentIndex = 0;
  score = 0;
  secondsLeft = 600;
  startTimeStamp = Date.now();
  answers = {};

  setupPanel.classList.add("d-none");
  quizPanel.classList.remove("d-none");
  resultPanel.classList.add("d-none");

  quizCategoryLabel.textContent = chosenCategory;
  timerDisplay.className = "sq-timer-badge";
  updateTimerDisplay(secondsLeft);
  startTimer();
  renderQuestion();
}

function startTimer() {
  if (timerInterval) clearInterval(timerInterval);

  timerInterval = setInterval(function () {
    secondsLeft--;

    if (secondsLeft <= 0) {
      clearInterval(timerInterval);
      finishQuiz();
      return;
    }

    updateTimerDisplay(secondsLeft);

    if (secondsLeft <= 60) {
      timerDisplay.className = "sq-timer-badge sq-timer-danger";
    } else if (secondsLeft <= 180) {
      timerDisplay.className = "sq-timer-badge sq-timer-warning";
    }
  }, 1000);
}

function updateTimerDisplay(secs) {
  const mins = Math.floor(secs / 60);
  const s = secs % 60;
  timerText.textContent = `${String(mins).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

function renderQuestion() {
  selectedAnswer = null;
  nextBtn.disabled = true;

  const q = questions[currentIndex];
  const total = questions.length;

  const progressPct = (currentIndex / total) * 100;
  quizProgressBar.style.width = progressPct + "%";

  questionCounter.textContent = `Question ${currentIndex + 1} of ${total}`;
  scoreCounter.textContent = `Score: ${score}`;
  questionText.textContent = q.question;
  optionsContainer.innerHTML = "";

  const letters = ["A", "B", "C", "D"];

  q.options.forEach(function (option, idx) {
    const btn = document.createElement("button");
    btn.className = "sq-option";
    btn.setAttribute("aria-label", `Option ${letters[idx]}: ${option}`);
    btn.innerHTML = `
      <span class="sq-option-letter">${letters[idx]}</span>
      <span>${option}</span>
    `;
    btn.addEventListener("click", function () {
      handleOptionSelect(option, btn);
    });
    optionsContainer.appendChild(btn);
  });
}

function handleOptionSelect(option, clickedBtn) {
  if (selectedAnswer !== null) return;

  selectedAnswer = option;

  const allOptions = optionsContainer.querySelectorAll(".sq-option");
  allOptions.forEach(function (btn) {
    btn.disabled = true;
    btn.classList.remove("selected");
  });

  clickedBtn.classList.add("selected");
  nextBtn.disabled = false;
}

nextBtn.addEventListener("click", function () {
  const currentQuestion = questions[currentIndex];
  const correctAnswer = currentQuestion.answer;

  // store answer using question id
  answers[currentQuestion._id] = selectedAnswer;

  if (selectedAnswer === correctAnswer) score++;

  currentIndex++;

  if (currentIndex < questions.length) {
    renderQuestion();
  } else {
    finishQuiz();
  }
});

function finishQuiz() {
  clearInterval(timerInterval);

  const elapsedSecs = Math.floor((Date.now() - startTimeStamp) / 1000);
  const mins = Math.floor(elapsedSecs / 60);
  const secs = elapsedSecs % 60;
  const timeTaken = `${mins}m ${String(secs).padStart(2, "0")}s`;

  const total = questions.length;
  const percentage = total ? Math.round((score / total) * 100) : 0;

  quizPanel.classList.add("d-none");
  resultPanel.classList.remove("d-none");

  scoreText.textContent = `${score}/${total}`;
  resultProgressBar.style.width = percentage + "%";
  resultPercentageText.textContent = `${percentage}% correct`;
  statCorrect.textContent = score;
  statWrong.textContent = total - score;
  statTime.textContent = timeTaken;

  if (percentage >= 80) {
    resultHeading.textContent = "🎉 Excellent!";
    resultSubtext.textContent = "Outstanding performance! You really know your stuff.";
  } else if (percentage >= 60) {
    resultHeading.textContent = "👍 Good Job!";
    resultSubtext.textContent = "Solid effort! A little more practice and you'll ace it.";
  } else if (percentage >= 40) {
    resultHeading.textContent = "🙂 Not Bad!";
    resultSubtext.textContent = "Keep practising – you're getting there!";
  } else {
    resultHeading.textContent = "📚 Keep Studying!";
    resultSubtext.textContent = "Don't give up! Every attempt makes you smarter.";
  }

  submitResult(chosenCategory, score, total, timeTaken);
}

async function submitResult(category, score, total, timeTaken) {
  try {
    await fetch("/submit_quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category: category,
        score: score,
        total: total,
        time_taken: timeTaken,
      }),
    });
  } catch (err) {
    console.warn("Could not save result to server:", err);
  }
}

retakeBtn.addEventListener("click", function () {
  resultPanel.classList.add("d-none");
  setupPanel.classList.remove("d-none");

  resetStartButton();
  timerText.textContent = "10:00";
  timerDisplay.className = "sq-timer-badge";
  quizProgressBar.style.width = "0%";
  setupError.classList.add("d-none");
});

function showSetupError(message) {
  setupError.textContent = message;
  setupError.classList.remove("d-none");
}

function hideSetupError() {
  setupError.classList.add("d-none");
  setupError.textContent = "";
}

function resetStartButton() {
  startQuizBtn.disabled = false;
  startQuizBtn.innerHTML = '<i class="fa-solid fa-play me-2"></i>Start Quiz';
}