<template>
  <div class="relative min-h-screen p-4">
    <!-- branch selector -->
    <BranchSelector
      v-if="screen === 'branch'"
      @select="goYear"
    />

    <!-- year selector -->
    <YearSelector
      v-else-if="screen === 'year'"
      :options="years"
      @select="startQuiz"
    />

    <!-- loading -->
    <div v-else-if="loadingQuestions" class="text-center mt-10">
      جاري تحميل الأسئلة…
    </div>

    <!-- load error -->
    <div v-else-if="loadError" class="text-red-600 text-center mt-10">
      {{ loadError }}
    </div>

    <!-- quiz -->
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

    <!-- no questions -->
    <div v-else-if="screen === 'quiz' && !questions.length" class="text-center mt-10">
      لا توجد أسئلة لهذا الاختبار. الرجوع للاختيار.
    </div>

    <!-- attached text modal -->
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

    <!-- results -->
    <ResultsChart
      v-else-if="screen === 'report'"
      :correct="correct"
      :wrong="wrong"
      :percentage="percentage"
      @reset="resetQuiz"
    />

    <!-- back button -->
    <BackButton v-if="screen !== 'branch'" @click="goBack" />
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { fetchWithTimeout } from '@/utils/fetchWithTimeout'
import { fetchQuestions, loadQuestionsFromJSON } from '@/services/quizService'
import { correctSound, wrongSound } from '@/utils/audio'

import BranchSelector from '@/components/BranchSelector.vue'
import YearSelector   from '@/components/YearSelector.vue'
import QuestionCard   from '@/components/QuestionCard.vue'
import ResultsChart   from '@/components/ResultsChart.vue'
import BackButton     from '@/components/BackButton.vue'

export default {
  name: 'QuizPage',
  components: {
    BranchSelector,
    YearSelector,
    QuestionCard,
    ResultsChart,
    BackButton
  },
  setup() {
    // screens: branch → year → quiz → report/text
    const screen = ref('branch')
    const branch = ref(null)
    const years  = [
      'الاختبار الأول','الاختبار الثاني','الاختبار الثالث',
      'الاختبار الرابع','الاختبار الخامس','الاختبار السادس',
      'الاختبار السابع','الاختبار الثامن','الاختبار التاسع',
      2022, 2023, 2024
    ]

    // all questions loaded from API or JSON
    const allQ = ref([])
    // filtered questions for the chosen year/branch
    const questions = ref([])

    const current      = ref(0)
    const answered     = reactive({})
    const correct      = ref(0)
    const lang         = ref('en')
    const attachedText = ref('')

    // loading/error state
    const loadingQuestions = ref(false)
    const loadError        = ref(null)

    // timer
    const totalSec = ref(90 * 60)
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
      const raw = attachedText.value || ''
      return raw
        .split('\n')
        .filter(l => l.trim())
        .map((line, i) =>
          i % 2 === 0
            ? `<p style="direction:ltr;text-align:left"><strong>${line}</strong></p>`
            : `<p style="direction:rtl;text-align:right;margin-bottom:1rem">${line}</p>`
        )
        .join('')
    })

    // ---------------------------------------------------------
    // 1) load questions: API race JSON fallback
    // ---------------------------------------------------------
    async function init() {
      loadingQuestions.value = true
      loadError.value = null

      let data = null
      try {
        data = await fetchWithTimeout(fetchQuestions(), 2500)
      } catch (apiErr) {
        console.warn('API failed or slow, falling back to JSON:', apiErr)
        try {
          data = await loadQuestionsFromJSON()
        } catch (jsonErr) {
          console.error('JSON fallback also failed:', jsonErr)
          loadError.value = 'تعذّر تحميل الأسئلة من API وJSON'
          return
        }
      } finally {
        loadingQuestions.value = false
      }

      allQ.value = Array.isArray(data) ? data : data.questions || data
    }

    // ---------------------------------------------------------
    // 2) choose branch → year → quiz flow
    // ---------------------------------------------------------
    function goYear(selectedBranch) {
      branch.value = selectedBranch
      screen.value = 'year'
    }

    function startQuiz(y) {
      questions.value = allQ.value
        .filter(q => q.year === y && q.type === branch.value)
        .sort((a, b) => a.id - b.id)

      if (!questions.value.length) {
        loadError.value = 'لا توجد أسئلة لهذا الاختبار.'
        screen.value = 'year'
        return
      }

      current.value = 0
      correct.value = 0
      Object.keys(answered).forEach(k => delete answered[k])
      totalSec.value = 90 * 60

      screen.value = 'quiz'
      startTimer()
    }

    // ---------------------------------------------------------
    // 3) timer
    // ---------------------------------------------------------
    function startTimer() {
      clearInterval(timer)
      timer = setInterval(() => {
        if (totalSec.value-- <= 0) {
          clearInterval(timer)
          screen.value = 'report'
        }
      }, 1000)
    }

    // ---------------------------------------------------------
    // 4) answer handling
    // ---------------------------------------------------------
    function selectAnswer(idx) {
      const q = questions.value[current.value]
      if (answered[q.id] != null) return

      answered[q.id] = idx
      const correctIdx = q.correct_answer - 1
      if (idx === correctIdx) {
        correctSound.currentTime = 0
        correctSound.play()
        correct.value++
      } else {
        wrongSound.currentTime = 0
        wrongSound.play()
      }
    }

    // ---------------------------------------------------------
    // 5) navigation
    // ---------------------------------------------------------
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
    function jumpToQuestion(i) {
      current.value = i
    }

    // ---------------------------------------------------------
    // 6) attached text & language toggle
    // ---------------------------------------------------------
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

    // ---------------------------------------------------------
    // 7) back & reset
    // ---------------------------------------------------------
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
      lang,
      formattedTime,
      percentage,
      attachedText,
      formattedAttachedText,
      loadingQuestions,
      loadError,
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
.error {
  color: red;
  text-align: center;
  margin: 1rem 0;
}
</style>
