// ✅ تحميل الأصوات
const clickSound = new Audio('/static/quiz/sounds/click.mp3');
const correctSound = new Audio('/static/quiz/sounds/correct.mp3');
const wrongSound = new Audio('/static/quiz/sounds/wrong.mp3');
const bgMusic = new Audio('/static/quiz/sounds/bg-music.mp3');
bgMusic.loop = true;

// ✅ متغيرات الحالة
let allQuestions = [];
let questions = [];
let currentQuestionIndex = 0;
let correctCount = 0;
let totalSeconds = 90 * 60; // 90 دقيقة
let timer;
let currentLanguage = 'ar';
let currentYear = 1;
let currentBranch = 'A';
let answeredState = {};
const screenStack = [];
let allUsers = [];

// ✅ تحميل الأسئلة والمستخدمين
async function loadQuestions() {
  const response = await fetch('/static/quiz/data/questions.json');
  if (response.ok) {
    allQuestions = await response.json();
  } else {
    console.error("❌ فشل تحميل الأسئلة");
  }
}

async function loadUsers() {
  const res = await fetch('/static/quiz/data/users.json');
  if (!res.ok) throw new Error('فشل تحميل المستخدمين');
  allUsers = await res.json();
}

async function initQuiz() {
  try {
    await Promise.all([loadQuestions(), loadUsers()]);
    if (allUsers.length > 0) {
      document.getElementById('username').textContent = allUsers[0].username;
      document.getElementById('location').textContent = allUsers[0].location;
    }
  } catch (err) {
    console.error(err);
  }
}

window.addEventListener('load', initQuiz);

// ✅ عرض الشاشات
function showScreen(screenId) {
  document.querySelectorAll('.quiz-container').forEach(el => el.style.display = 'none');
  document.getElementById(screenId).style.display = 'block';
  screenStack.push(screenId);
  history.pushState({ screen: screenId }, '', '');
}

// ✅ اختيار الفرع / السنة
function selectBranch(branch) {
  currentBranch = branch;
  showScreen('year-screen');
}

function selectYear(year) {
  currentYear = year;
  showScreen('quiz-screen');
  filterQuestionsByYearAndBranch();
  startTimer();
}

// ✅ تصفية وتحميل الأسئلة
function filterQuestionsByYearAndBranch() {
  questions = allQuestions
    .filter(q => q.year === currentYear && q.type === currentBranch)
    .sort((a, b) => a.id - b.id);

  currentQuestionIndex = 0;
  correctCount = 0;
  answeredState = {};
  updateQuestionDropdown();
  loadQuestion();
}

// ✅ تحميل السؤال الحالي
function loadQuestion() {
  const q = questions[currentQuestionIndex];
  const lang = currentLanguage;

  document.getElementById("question").textContent = q[`question_${lang}`];
  updateQuestionDropdown();
  updateScoreSummary();

  const answersDiv = document.getElementById("answers");
  answersDiv.innerHTML = "";

  [q[`answer1_${lang}`], q[`answer2_${lang}`], q[`answer3_${lang}`], q[`answer4_${lang}`]]
    .forEach((text, index) => {
      const btn = document.createElement("button");
      btn.textContent = text;
      btn.classList.add("answer-button");
      btn.dataset.index = index;

      if (answeredState[q.id] !== undefined) {
        btn.disabled = true;
        const selected = answeredState[q.id];
        const correct = q.correct_answer - 1;
        if (index === correct) btn.classList.add("correct");
        else if (index === selected) btn.classList.add("wrong");
      } else {
        btn.onclick = () => checkAnswer(index);
      }

      answersDiv.appendChild(btn);
    });

  document.getElementById("result").textContent = "";

  const hasText = (q.attached_text_ar?.trim() !== '' || q.attached_text?.trim() !== '');
  document.getElementById("text-button").style.display = hasText ? "inline-block" : "none";
}

// ✅ التحقق من الإجابة
function checkAnswer(selectedIndex) {
  clickSound.play();
  const q = questions[currentQuestionIndex];
  const correctIndex = q.correct_answer - 1;

  document.querySelectorAll(".answers button").forEach((b, i) => {
    b.disabled = true;
    if (i === correctIndex) b.classList.add("correct");
    else if (i === selectedIndex) b.classList.add("wrong");
  });

  const resultEl = document.getElementById("result");
  resultEl.classList.remove("text-success", "text-danger");

  if (selectedIndex === correctIndex) {
    correctSound.play();
    correctCount++;
    resultEl.textContent = "إجابة صحيحة!";
    resultEl.classList.add("text-success");
  } else {
    wrongSound.play();
    resultEl.textContent = "إجابة خاطئة!";
    resultEl.classList.add("text-danger");
  }

  answeredState[q.id] = selectedIndex;
  updateScoreSummary();
}

// ✅ التنقل بين الأسئلة
function nextQuestion() {
  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex++;
    loadQuestion();
  } else {
    showFinalResult();
  }
}

function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    loadQuestion();
  }
}

// ✅ القائمة المنسدلة
function updateQuestionDropdown() {
  const select = document.getElementById("question-jump");
  select.innerHTML = "";
  questions.forEach((_, idx) => {
    const option = document.createElement("option");
    option.value = idx;
    option.textContent = `السؤال ${idx + 1} من ${questions.length}`;
    if (idx === currentQuestionIndex) option.selected = true;
    select.appendChild(option);
  });
}

function jumpToQuestion(index) {
  currentQuestionIndex = parseInt(index);
  loadQuestion();
}

// ✅ اللغة
function toggleLanguage() {
  currentLanguage = currentLanguage === 'ar' ? 'en' : 'ar';
  loadQuestion();
}

// ✅ ملخص النقاط
function updateScoreSummary() {
  const wrong = Object.keys(answeredState).length - correctCount;
  document.getElementById("score-summary").textContent =
    `إجابات صحيحة: ${correctCount} | خاطئة: ${wrong >= 0 ? wrong : 0}`;
}

// ✅ عرض النص
function openTextScreen() {
  const q = questions[currentQuestionIndex];
  const text = currentLanguage === 'ar' ? q.attached_text_ar : q.attached_text;
  document.getElementById("attached-text").textContent = text || "لا يوجد نص مرفق";
  showScreen("text-screen");
}

// ✅ العودة للرئيسية
function goHome() {
  location.reload();
}

// ✅ المؤقت الزمني
function startTimer() {
  clearInterval(timer);
  updateTimerDisplay();
  timer = setInterval(() => {
    if (totalSeconds <= 0) {
      clearInterval(timer);
      showFinalResult();
      return;
    }
    totalSeconds--;
    updateTimerDisplay();
  }, 1000);
}

function updateTimerDisplay() {
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = (totalSeconds % 60).toString().padStart(2, '0');
  document.getElementById('time').textContent = `00:${minutes}:${seconds}`;
}

// ✅ النتيجة النهائية
function showFinalResult() {
  clearInterval(timer);
  const correct = correctCount;
  const wrong = Object.keys(answeredState).length - correctCount;
  const total = correct + wrong;
  const percentage = total > 0 ? Math.round((correct / total) * 100) : 0;

  showScreen('report-screen');

  document.getElementById('correct-count').innerText = correct;
  document.getElementById('wrong-count').innerText = wrong;
  document.getElementById('percentage').innerText = `${percentage}%`;

  const msg = `📊 تقرير نتيجتي:\n✅ صحيحة: ${correct}\n❌ خاطئة: ${wrong}\n📈 نسبة النجاح: ${percentage}%`;
  const whatsappLink = `https://wa.me/963988131514?text=${encodeURIComponent(msg)}`;
  document.getElementById('whatsapp-share').href = whatsappLink;

  drawChart(correct, wrong);
}

// ✅ رسم الرسم البياني النهائي
function drawChart(correct, wrong) {
  const total = correct + wrong;
  const ctx = document.getElementById('resultChart').getContext('2d');

  const grad1 = ctx.createLinearGradient(0, 0, 0, 300);
  grad1.addColorStop(0, '#8cf29b');
  grad1.addColorStop(1, '#28a745');

  const grad2 = ctx.createLinearGradient(0, 0, 0, 300);
  grad2.addColorStop(0, '#ff8c8c');
  grad2.addColorStop(1, '#dc3545');

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['صحيحة', 'خاطئة'],
      datasets: [{
        data: [correct, wrong],
        backgroundColor: [grad1, grad2],
        borderWidth: 8,
        borderColor: '#fff',
        hoverOffset: 25
      }]
    },
    options: {
      cutout: '70%',
      plugins: {
        legend: { display: false }
      }
    }
  });
}

// ✅ دعم التثبيت كتطبيق PWA
let deferredPrompt;
const installBtn = document.getElementById('install-btn');

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;
  installBtn.style.display = 'flex';
});

installBtn.addEventListener('click', async () => {
  installBtn.style.display = 'none';
  if (deferredPrompt) {
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    deferredPrompt = null;
  }
});

window.addEventListener('appinstalled', () => {
  installBtn.style.display = 'none';
});

// ✅ التعامل مع زر الرجوع في المتصفح
window.addEventListener('popstate', () => {
  screenStack.pop();
  const prev = screenStack[screenStack.length - 1];
  if (prev) {
    document.querySelectorAll('.quiz-container').forEach(el => el.style.display = 'none');
    document.getElementById(prev).style.display = 'block';
  }
});

// ✅ تسجيل Service Worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register("{% static 'pwa/serviceworker.js' %}")
    .then(reg => console.log('✅ Service Worker مسجل:', reg.scope))
    .catch(err => console.error('❌ Service Worker فشل:', err));
}