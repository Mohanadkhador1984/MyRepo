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
let totalSeconds = 5400; // 90 دقيقة
let timer;
let currentLanguage = 'en';
let currentYear = 1;
let currentBranch = 'A';
let answeredState = {};
const screenStack = [];
let allUsers     = [];


// ✅ تحميل الأسئلة
async function loadQuestions() {
  const response = await fetch('/static/quiz/data/questions.json');
  if (response.ok) {
    allQuestions = await response.json();
  } else {
    console.error("❌ فشل تحميل الأسئلة من الملف");
  }
}



async function loadUsers() {
  const res = await fetch('/static/quiz/data/users.json');
  if (!res.ok) throw new Error('Failed to load users');
  allUsers = await res.json();
}


async function initQuiz() {
  try {
    await Promise.all([loadQuestions(), loadUsers()]);
    console.log('Questions:', allQuestions);
    console.log('Users:',     allUsers);
    // مثال: عرض أول مستخدم
    if (allUsers.length > 0) {
      document.getElementById('username').textContent = allUsers[0].username;
      document.getElementById('location').textContent = allUsers[0].location;
    }
    // متابعة لبقية منطق اللعبة…
  } catch (err) {
    console.error(err);
  }
}

window.addEventListener('load', initQuiz);





// ✅ عرض شاشة معينة
function showScreen(screenId) {
  document.querySelectorAll('.quiz-container').forEach(el => el.style.display = 'none');
  document.getElementById(screenId).style.display = 'block';
  screenStack.push(screenId);
  history.pushState({ screen: screenId }, '', '');
}

// ✅ اختيار الفرع
function selectBranch(branch) {
  currentBranch = branch;
  showScreen('year-screen');
}

// ✅ اختيار السنة
function selectYear(year) {
  currentYear = year;
  showScreen('quiz-screen');
  filterQuestionsByYearAndBranch();
  startTimer();
}

// ✅ تصفية الأسئلة
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

  const answers = [
    q[`answer1_${lang}`],
    q[`answer2_${lang}`],
    q[`answer3_${lang}`],
    q[`answer4_${lang}`]
  ];

  answers.forEach((text, index) => {
    const btn = document.createElement("button");
    btn.textContent = text;
    btn.classList.add("answer-button");
    btn.dataset.index = index;

    if (answeredState[q.id] !== undefined) {
      btn.disabled = true;
      const selected = answeredState[q.id];
      const correct = q.correct_answer - 1;
      if (index === correct) {
        btn.classList.add("correct");
      } else if (index === selected) {
        btn.classList.add("wrong");
      }
    } else {
      btn.onclick = () => checkAnswer(index);
    }

    answersDiv.appendChild(btn);
  });

  document.getElementById("result").textContent = "";

  const hasText = (q.attached_text_ar?.trim() !== '') || (q.attached_text?.trim() !== '');
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

  if (selectedIndex === correctIndex) {
    correctSound.play();
    correctCount++;
    document.getElementById("result").textContent = "إجابة صحيحة!";
  } else {
    wrongSound.play();
    document.getElementById("result").textContent = "إجابة خاطئة!";
  }

  answeredState[q.id] = selectedIndex;
  updateScoreSummary();
}

// ✅ الانتقال للسؤال التالي
function nextQuestion() {
  if (currentQuestionIndex < questions.length - 1) {
    currentQuestionIndex++;
    loadQuestion();
  } else {
    showFinalResult();
  }
}

// ✅ العودة للسؤال السابق
function prevQuestion() {
  if (currentQuestionIndex > 0) {
    currentQuestionIndex--;
    loadQuestion();
  }
}

// ✅ تحديث قائمة الأسئلة
function updateQuestionDropdown() {
  const select = document.getElementById("question-jump");
  select.innerHTML = "";
  questions.forEach((_, index) => {
    const option = document.createElement("option");
    option.value = index;
    option.textContent = `السؤال ${index + 1} من ${questions.length}`;
    if (index === currentQuestionIndex) option.selected = true;
    select.appendChild(option);
  });
}

// ✅ الانتقال مباشرة لسؤال
function jumpToQuestion(index) {
  currentQuestionIndex = parseInt(index);
  loadQuestion();
}

// ✅ تغيير اللغة
function toggleLanguage() {
  currentLanguage = currentLanguage === 'ar' ? 'en' : 'ar';
  loadQuestion();
}

// ✅ تحديث ملخص النقاط
function updateScoreSummary() {
  const wrong = Object.keys(answeredState).length - correctCount;
  document.getElementById("score-summary").textContent =
    `إجابات صحيحة: ${correctCount} | خاطئة: ${wrong >= 0 ? wrong : 0}`;
}

// ✅ عرض النتيجة النهائية
function showFinalResult() {
  const total = questions.length;
  const wrongCount = total - correctCount;
  const percentage = Math.round((correctCount / total) * 100);

  document.getElementById("quiz-screen").innerHTML = `
    <h1>النتيجة النهائية</h1>
    <p>إجابات صحيحة: ${correctCount}</p>
    <p>إجابات خاطئة: ${wrongCount}</p>
    <p>المجموع النهائي: ${percentage}%</p>
    <canvas id="resultChart"></canvas>
    <button class="btn btn-warning mt-3" onclick="location.reload()">إعادة المحاولة</button>
  `;

  const ctx = document.getElementById('resultChart').getContext('2d');
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['صحيحة', 'خاطئة'],
      datasets: [{
        data: [correctCount, wrongCount],
        backgroundColor: ['#28a745', '#dc3545'],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: '#fff'
          }
        }
      }
    }
  });
}

// ✅ عرض النص المرفق
function openTextScreen() {
  const q = questions[currentQuestionIndex];
  const text = currentLanguage === 'ar' ? q.attached_text_ar : q.attached_text;
  document.getElementById("attached-text").textContent = text || "لا يوجد نص مرفق";
  showScreen("text-screen");
}

// ✅ العودة إلى الصفحة الرئيسية
function goHome() {
  location.reload();
}

// ✅ تشغيل المؤقت
function startTimer() {
  clearInterval(timer);
  timer = setInterval(() => {
    if (totalSeconds <= 0) {
      clearInterval(timer);
      showFinalResult();
      return;
    }
    totalSeconds--;
    const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
    const seconds = (totalSeconds % 60).toString().padStart(2, '0');
    document.getElementById('timer').textContent = `00:${minutes}:${seconds}`;
  }, 1000);
}

 let deferredPrompt;
  const installBtn = document.getElementById('install-btn');
  const installContainer = document.getElementById('install-container');

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
      if (outcome === 'accepted') {
        console.log('✅ المستخدم وافق على التثبيت');
      } else {
        console.log('❌ المستخدم رفض التثبيت');
      }
      deferredPrompt = null;
    }
  });

  window.addEventListener('appinstalled', () => {
    console.log('✅ التطبيق تم تثبيته');
    installBtn.style.display = 'none';
  });
  


  loadQuestions(); // تحميل الأسئلة


// ✅ التعامل مع زر الرجوع
window.addEventListener('popstate', () => {
  screenStack.pop();
  const prev = screenStack[screenStack.length - 1];
  if (prev) {
    document.querySelectorAll('.quiz-container').forEach(el => el.style.display = 'none');
    document.getElementById(prev).style.display = 'block';
  }
});
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/serviceworker.js')
      .then((registration) => {
        console.log('✅ Service Worker مسجل عند:', registration.scope);
      })
      .catch((error) => {
        console.error('❌ فشل تسجيل Service Worker:', error);
      });
  });
}

function updateProgress(percent) {
  const progress = document.getElementById('progress');
  const progressText = document.getElementById('progress-text');
  progress.style.width = percent + '%';
  progressText.textContent = percent + '%';
}