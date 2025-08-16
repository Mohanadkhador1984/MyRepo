<template>
  <div class="quiz-page">

    <!-- اختيار الفرع -->
    <BranchSelector
      v-if="screen === 'branch'"
      @select="goYear"
    />

    <!-- اختيار السنة -->
    <YearSelector
      v-else-if="screen === 'year'"
      :options="years"
      @select="startQuiz"
    />

    <!-- تحميل الأسئلة -->
    <div v-else-if="loadingQuestions" class="text-center mt-10">
      جاري تحميل الأسئلة…
    </div>

    <!-- خطأ التحميل -->
    <div v-else-if="loadError" class="text-red-600 text-center mt-10">
      {{ loadError }}
    </div>

    <!-- عرض السؤال -->
    <QuestionCard
      v-else-if="screen === 'quiz' && questions.length"
      :questions="questions"
      :current="questions[current]"
      :currentIndex="current"
      :totalQuestions="questions.length"
      :answered="answered"
      :score="{ correct, wrong }"
      :lang="lang"
      :formattedTime="formattedTime"
      :show-open-text="hasExplicitText"
      @answer="selectAnswer"
      @next="nextQuestion"
      @prev="prevQuestion"
      @toggle-lang="toggleLanguage"
      @jump="jumpToQuestion"
      @open-text="openTextScreen"
    />

    <!-- لا توجد أسئلة -->
    <div v-else-if="screen === 'quiz' && !questions.length"
         class="text-center mt-10">
      لا توجد أسئلة لهذا الاختبار. الرجوع للاختيار.
    </div>

    <!-- مودال النص المرفق -->
    <div v-else-if="screen === 'text'"
         class="text-modal fixed inset-0 bg-black bg-opacity-50
                flex items-center justify-center z-50">
      <div class="modal-content bg-white rounded-lg shadow-lg
                  max-w-3xl w-full p-6 text-right space-y-4">
        <h2 class="text-xl font-bold border-b pb-2 flex items-center gap-2">
          <span>📘</span>
          <span>النص المرفق</span>
        </h2>

        <div class="attached-text max-h-96 overflow-y-auto
                    text-gray-700 leading-relaxed"
             v-html="formattedAttachedText" />

        <div class="text-right">
          <button class="close-text-btn"
                  @click="backToQuiz">
            إغلاق
          </button>
        </div>
      </div>
    </div>

    <!-- تقرير النتائج -->
    <ResultsChart
      v-else-if="screen === 'report'"
      :correct="correct"
      :wrong="wrong"
      :percentage="percentage"
      @reset="resetQuiz"
    />

    <!-- زر العودة العائم -->
    <button v-if="screen !== 'branch'"
            class="floating-back-btn"
            aria-label="رجوع"
            @click="goBack">
      <i class="fas fa-arrow-right rotate-180"></i>
    </button>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { loadQuestionsFromJSON, fetchQuestionsFromAPI } from '@/services/quizService.js'
import { correctSound, wrongSound } from '@/utils/audio'

import BranchSelector from '@/components/BranchSelector.vue'
import YearSelector   from '@/components/YearSelector.vue'
import QuestionCard   from '@/components/QuestionCard.vue'
import ResultsChart   from '@/components/ResultsChart.vue'

export default {
  name: 'QuizPage',
  components: { BranchSelector, YearSelector, QuestionCard, ResultsChart },
  setup() {
    // الشاشات والحالة
    const screen           = ref('branch')
    const loadingQuestions = ref(false)
    const loadError        = ref('')
    const lang             = ref('en')

    // فروع وسنوات
    const years        = [
      'الاختبار الأول','الاختبار الثاني','الاختبار الثالث',
      'الاختبار الرابع','الاختبار الخامس','الاختبار السادس',
      'الاختبار السابع','الاختبار الثامن','الاختبار التاسع',
      2022, 2023, 2024
    ]
    const lockedYears = [2022]
    const isActivated = ref(localStorage.getItem('activated') === 'true')
    const branch      = ref('')

    // الأسئلة والحالة
    const allQ      = ref([])
    const questions = ref([])
    const current   = ref(0)
    const answered  = reactive({})
    const correct   = ref(0)
    const totalSec  = ref(90 * 60)
    let timer       = null

    // حساب النتائج
    const wrong = computed(() =>
      Object.keys(answered).length - correct.value
    )

    const percentage = computed(() => {
      const tot = correct.value + wrong.value
      return tot ? Math.round((correct.value / tot) * 100) : 0
    })

    // تنسيق الوقت
    const formattedTime = computed(() => {
      const m = String(Math.floor(totalSec.value / 60)).padStart(2, '0')
      const s = String(totalSec.value % 60).padStart(2, '0')
      return `00:${m}:${s}`
    })

    // النص المرفق
    const attachedText = ref('')
    const formattedAttachedText = computed(() =>
      attachedText.value
        .split('\n')
        .filter(l => l.trim())
        .map((line, i) =>
          i % 2 === 0
            ? `<p style="direction:ltr;text-align:left">
                 <strong>${line}</strong></p>`
            : `<p style="direction:rtl;text-align:right;margin-bottom:1rem">
                 ${line}</p>`
        ).join('')
    )
    // إخفاء الزر/الأيقونة إذا لا يوجد نص واضح
    const hasExplicitText = computed(() => {
      const txt = attachedText.value.trim()
      return txt && !/^[*_-\s]+$/.test(txt)
    })

    // تحميل البيانات
    async function init() {
      loadingQuestions.value = true
      loadError.value = ''
      try {
        const resp = await Promise.race([
          fetchQuestionsFromAPI(),
          loadQuestionsFromJSON()
        ])
        let data = resp.data ?? resp
        if (Array.isArray(data.questions)) data = data.questions
        allQ.value = Array.isArray(data) ? data : []
      } catch (err) {
        console.error('❌ فشل تحميل:', err)
        loadError.value = 'تعذّر تحميل الأسئلة.'
      } finally {
        loadingQuestions.value = false
      }
    }

    // الانتقالات
    function goYear(selectedBranch) {
      branch.value = selectedBranch
      screen.value = 'year'
      loadError.value = ''
    }

    function startQuiz(y) {
      loadError.value = ''
      const yearNum = Number(y)
      if (lockedYears.includes(yearNum) && !isActivated.value) {
        loadError.value = 'هذه السنة مقفلة. الرجاء التفعيل.'
        return
      }
      questions.value = allQ.value
        .filter(q => q.year === yearNum && q.type === branch.value)
        .sort((a, b) => a.id - b.id)
      if (!questions.value.length) {
        loadError.value = 'لا توجد أسئلة لهذا الاختبار.'
        return
      }
      // تهيئة
      current.value = 0
      correct.value = 0
      Object.keys(answered).forEach(k => delete answered[k])
      totalSec.value = 90 * 60
      screen.value = 'quiz'
      startTimer()
    }

    function startTimer() {
      clearInterval(timer)
      timer = setInterval(() => {
        if (totalSec.value <= 0) {
          clearInterval(timer)
          screen.value = 'report'
        } else {
          totalSec.value--
        }
      }, 1000)
    }

    function selectAnswer(idx) {
      const q = questions.value[current.value]
      if (answered[q.id] != null) return

      answered[q.id] = idx
      const correctIdx = q.correct_answer - 1
      if (idx === correctIdx) {
        correctSound.currentTime = 0
        correctSound.play()
          .catch(() => {
            correctSound.load()
            correctSound.play()
          })
        correct.value++
      } else {
        wrongSound.currentTime = 0
        wrongSound.play()
          .catch(() => {
            wrongSound.load()
            wrongSound.play()
          })
      }
    }

    function nextQuestion() {
      if (current.value < questions.value.length - 1) {
        current.value++
      } else {
        clearInterval(timer)
        screen.value = 'report'
      }
    }
    function prevQuestion() {
      if (current.value > 0) current.value--
    }
    function jumpToQuestion(i) {
      current.value = i
    }

    function toggleLanguage() {
      lang.value = lang.value === 'ar' ? 'en' : 'ar'
    }

    function openTextScreen() {
      const q = questions.value[current.value]
      attachedText.value =
        q[`attached_text_${lang.value}`] || q.attached_text || ''
      screen.value = 'text'
    }
    function backToQuiz() {
      screen.value = 'quiz'
    }

    function goBack() {
      if (screen.value === 'text') backToQuiz()
      else if (screen.value === 'quiz') screen.value = 'year'
      else if (screen.value === 'year') screen.value = 'branch'
    }

    function resetQuiz() {
      clearInterval(timer)
      screen.value = 'branch'
    }

    onMounted(init)
    onBeforeUnmount(() => clearInterval(timer))

    return {
      screen,
      years,
      questions,
      current,
      answered,
      correct,
      wrong,
      percentage,
      formattedTime,
      loadingQuestions,
      loadError,
      lang,
      formattedAttachedText,
      hasExplicitText,
      goYear,
      startQuiz,
      selectAnswer,
      nextQuestion,
      prevQuestion,
      jumpToQuestion,
      toggleLanguage,
      openTextScreen,
      backToQuiz,
      goBack,
      resetQuiz
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.quiz-page { font-family: 'Cairo', sans-serif; position: relative; min-height: 100vh; padding: 1rem; }
.text-modal .modal-content { position: relative; }

/* زر إغلاق النص يومض */
.close-text-btn {
  margin-top: 1.5rem;
  padding: 0.6rem 1.2rem;
  background: #3b82f6;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  animation: blink 1.2s infinite alternate;
}
@keyframes blink {
  0% { opacity: 1; }
  100% { opacity: 0.6; }
}

/* زر العودة العائم */
.floating-back-btn {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  width: 48px;
  height: 48px;
  background: #8b5cf6;
  color: #fff;
  border: none;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  cursor: pointer;
  transition: background .2s, transform .1s;
  z-index: 1001;
}
.floating-back-btn:hover {
  background: #7c3aed;
  transform: scale(1.05);
}
.rotate-180 { transform: rotate(180deg); }
</style>
