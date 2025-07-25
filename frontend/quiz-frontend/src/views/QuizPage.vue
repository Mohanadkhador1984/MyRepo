<template>
  <div class="relative min-h-screen p-4">

    <!-- شاشة اختيار الفرع -->
    <BranchSelector
      v-if="screen === 'branch'"
      @select="goYear"
    />

    <!-- شاشة اختيار السنة -->
    <YearSelector
      v-else-if="screen === 'year'"
      :options="years"
      @select="startQuiz"
    />

    <!-- عند التحميل (قبل عرض أي شيء) -->
    <div v-else-if="loadingQuestions" class="text-center mt-10">
      جاري تحميل الأسئلة…
    </div>

    <!-- خطأ في التحميل -->
    <div v-else-if="loadError" class="text-red-600 text-center mt-10">
      {{ loadError }}
    </div>

    <!-- صفحة الأسئلة -->
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
      @answer="selectAnswer"
      @next="nextQuestion"
      @prev="prevQuestion"
      @toggle-lang="toggleLanguage"
      @jump="jumpToQuestion"
      @open-text="openTextScreen"
    />

    <!-- إذا لا توجد أسئلة بعد الاختيار -->
    <div v-else-if="screen === 'quiz' && !questions.length" class="text-center mt-10">
      لا توجد أسئلة لهذا الاختبار. الرجوع للاختيار.
    </div>

    <!-- مودال النص المرفق -->
    <div
      v-else-if="screen === 'text'"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg shadow-lg max-w-3xl w-full p-6 text-right space-y-4">
        <h2 class="text-xl font-bold border-b pb-2">📘 النص المرفق</h2>
        <div
          class="max-h-96 overflow-y-auto space-y-2 text-gray-700"
          v-html="formattedAttachedText"
        ></div>
        <div class="text-center">
          <button
            @click="backToQuiz"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition"
          >
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

    <!-- زر الرجوع العائم -->
    <BackButton
      v-if="screen !== 'branch'"
      @click="goBack"
    />
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { fetchQuestions } from '@/services/quizService'
import { correctSound, wrongSound } from '@/utils/audio'

import BranchSelector from '@/components/BranchSelector.vue'
import YearSelector   from '@/components/YearSelector.vue'
import QuestionCard   from '@/components/QuestionCard.vue'
import ResultsChart   from '@/components/ResultsChart.vue'
import BackButton     from '@/components/BackButton.vue'

export default {
  name: 'QuizPage',
  components: {
    BranchSelector, YearSelector,
    QuestionCard, ResultsChart, BackButton
  },

  setup() {
    const screen           = ref('branch')
    const branch           = ref(null)
    const years            = [
      'الاختبار الأول','الاختبار الثاني','الاختبار الثالث',
      'الاختبار الرابع','الاختبار الخامس','الاختبار السادس',
      'الاختبار السابع','الاختبار الثامن','الاختبار التاسع',
      2022, 2023, 2024
    ]
    const allQ             = ref([])
    const questions        = ref([])
    const current          = ref(0)
    const answered         = reactive({})
    const correct          = ref(0)
    const lang             = ref('en')
    const totalSec         = ref(90 * 60)
    const attachedText     = ref('')

    // حالات التحميل
    const loadingQuestions = ref(false)
    const loadError        = ref(null)

    let timer = null

    const wrong = computed(() =>
      Object.keys(answered).length - correct.value
    )

    const formattedTime = computed(() => {
      const m = String(Math.floor(totalSec.value / 60)).padStart(2, '0')
      const s = String(totalSec.value % 60).padStart(2, '0')
      return `00:${m}:${s}`
    })

    const percentage = computed(() => {
      const tot = correct.value + wrong.value
      return tot ? Math.round((correct.value / tot) * 100) : 0
    })

    const formattedAttachedText = computed(() => {
      const raw   = attachedText.value || ''
      const lines = raw.split('\n').filter(l => l.trim())
      return lines.reduce((html, line, idx) => {
        if (idx % 2 === 0) {
          return html + `<p style="direction:ltr;text-align:left"><strong>${line}</strong></p>`
        } else {
          return html + `<p style="direction:rtl;text-align:right;margin-bottom:1rem">${line}</p>`
        }
      }, '')
    })

    // 1) تحميل الأسئلة من API عند التركيب
    async function init() {
      loadingQuestions.value = true
      loadError.value = null

      try {
        const data = await fetchQuestions()
        allQ.value = data
      } catch (err) {
        console.error('QuizPage.init error:', err)
        loadError.value = err.message
      } finally {
        loadingQuestions.value = false
      }
    }

    // 2) الانتقال لشاشة السنة
    function goYear(br) {
      branch.value = br
      screen.value = 'year'
    }

    // 3) بدء الاختبار بعد اختيار السنة
    function startQuiz(y) {
      questions.value = allQ.value
      .filter(q => q.year === y && q.type === branch.value)
      .sort((a, b) => a.id - b.id)

        
      current.value = 0
      correct.value = 0
      Object.keys(answered).forEach(k => delete answered[k])

      // إذا لا توجد أسئلة لهذا الاختبار
      if (!questions.value.length) {
        loadError.value = 'لا توجد أسئلة لهذا الاختبار.'
        screen.value = 'year'
        return
      }

      screen.value = 'quiz'
      startTimer()
    }

    // 4) عداد الوقت
    function startTimer() {
      clearInterval(timer)
      totalSec.value = 90 * 60
      timer = setInterval(() => {
        if (totalSec.value-- <= 0) {
          clearInterval(timer)
          screen.value = 'report'
        }
      }, 1000)
    }

    // 5) اختيار الإجابة
    function selectAnswer(idx) {
      const q  = questions.value[current.value]
      const id = q.id
      if (answered[id] != null) return
      answered[id] = idx
      const correctIdx = q.correct_answer - 1
      if (idx === correctIdx) {
        correctSound.play()
        correct.value++
      } else {
        wrongSound.play()
      }
    }

    // 6) تنقل بين الأسئلة
    function nextQuestion() {
      if (current.value < questions.value.length - 1) {
        current.value++
      } else {
        screen.value = 'report'
      }
    }
    function prevQuestion() {
      if (current.value > 0) current.value--
    }
    function jumpToQuestion(idx) {
      current.value = idx
    }

    // 7) تبديل اللغة وعرض النص
    function toggleLanguage() {
      lang.value = lang.value === 'ar' ? 'en' : 'ar'
    }
    function openTextScreen() {
      const q = questions.value[current.value]
      attachedText.value =
        q[`attached_text_${lang.value}`] ||
        q.attached_text ||
        'لا يوجد نص مرفق'
      screen.value = 'text'
    }
    function backToQuiz() {
      screen.value = 'quiz'
    }

    // 8) زر الرجوع
    function goBack() {
      if (screen.value === 'text') backToQuiz()
      else if (screen.value === 'quiz') screen.value = 'year'
      else if (screen.value === 'year') screen.value = 'branch'
    }

    // 9) إعادة الاختبار
    function resetQuiz() {
      clearInterval(timer)
      screen.value = 'branch'
    }

    onMounted(init)
    onBeforeUnmount(() => clearInterval(timer))

    return {
      screen, years, questions, current, answered,
      correct, wrong, lang, formattedTime, percentage,
      attachedText, formattedAttachedText,
      loadingQuestions, loadError,
      goYear, startQuiz, selectAnswer,
      nextQuestion, prevQuestion, jumpToQuestion,
      toggleLanguage, openTextScreen, backToQuiz,
      goBack, resetQuiz
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
  text-align: center;
  margin: 1rem 0;
}
</style>
