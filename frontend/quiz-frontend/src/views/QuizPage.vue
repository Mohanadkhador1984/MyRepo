<template>
  <div class="relative min-h-screen p-4">
    <!-- 1) Show activation modal only when needed -->
    <ActivationModal
      v-if="showActivationModal"
      @activated="onActivated"
      @close="showActivationModal = false"
    />

    <!-- 2) Branch selector screen -->
    <BranchSelector
      v-if="screen === 'branch'"
      @select="goYear"
    />

    <!-- 3) Year selector screen -->
    <YearSelector
      v-else-if="screen === 'year'"
      :options="years"
      :activated="isActivated"
      :locked-years="lockedYears"
      @select="handleYearSelect"
    />

    <!-- 4) Loading / error -->
    <div v-else-if="loadingQuestions" class="text-center mt-10">
      جاري تحميل الأسئلة…
    </div>
    <div v-else-if="loadError" class="text-red-600 text-center mt-10">
      {{ loadError }}
    </div>

    <!-- 5) Quiz screen -->
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

    <div
      v-else-if="screen === 'quiz' && !questions.length"
      class="text-center mt-10"
    >
      لا توجد أسئلة لهذا الاختبار. الرجوع للاختيار.
    </div>

    <!-- 6) Attached text screen -->
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
          <!-- <button
            @click="backToQuiz"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition"
          >
            إغلاق
          </button> -->
        </div>
      </div>
    </div>

    <!-- 7) Results screen -->
    <ResultsChart
      v-else-if="screen === 'report'"
      :correct="correct"
      :wrong="wrong"
      :percentage="percentage"
      @reset="resetQuiz"
    />

    <!-- 8) Back button -->
    <BackButton
      v-if="screen !== 'branch'"
      @click="goBack"
    />
  </div>
</template>

<script>
/* eslint-disable */
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import BranchSelector  from '@/components/BranchSelector.vue'
import YearSelector    from '@/components/YearSelector.vue'
import ActivationModal from '@/components/ActivationModal.vue'
import QuestionCard    from '@/components/QuestionCard.vue'
import ResultsChart    from '@/components/ResultsChart.vue'
// import BackButton      from '@/components/BackButton.vue'
import { loadQuestionsFromJSON, fetchQuestionsFromAPI } from '@/services/quizService.js'
import { correctSound, wrongSound } from '@/utils/audio'

export default {
  name: 'QuizPage',
  components: {
    BranchSelector,
    YearSelector,
    ActivationModal,
    QuestionCard,
    ResultsChart,
    // BackButton
  },
  setup() {
    // 1) Screens & activation state
    const screen              = ref('branch')
    const isActivated         = ref(localStorage.getItem('activated') === 'true')
    const showActivationModal = ref(false)

    // 2) Year options and which are locked
    const years       = [2021, 2022, 2023, 2024]
    const lockedYears = ref([2022])

    // 3) Quiz data holders
    const branch           = ref(null)
    const allQ             = ref([])
    const questions        = ref([])
    const current          = ref(0)
    const answered         = reactive({})
    const correct          = ref(0)
    const lang             = ref('en')
    const attachedText     = ref('')
    const loadingQuestions = ref(false)
    const loadError        = ref(null)
    const totalSec         = ref(90 * 60)
    let   timer            = null

    // 4) Computed helpers
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
      return tot ? Math.round((correct.value/ tot) * 100) : 0
    })
    const formattedAttachedText = computed(() =>
      (attachedText.value || '')
        .split('\n')
        .filter(l => l.trim())
        .map((line, i) =>
          i % 2 === 0
            ? `<p style="direction:ltr;text-align:left"><strong>${line}</strong></p>`
            : `<p style="direction:rtl;text-align:right;margin-bottom:1rem">${line}</p>`
        )
        .join('')
    )

    // 5) Initialize question bank
    async function init() {
      loadingQuestions.value = true
      loadError.value = null
      try {
        const resp = await Promise.race([
          fetchQuestionsFromAPI(),
          loadQuestionsFromJSON()
        ])
        let data = resp.data ?? resp
        if (Array.isArray(data.questions)) data = data.questions
        allQ.value = Array.isArray(data) ? data : []
      } catch {
        loadError.value = 'تعذّر تحميل الأسئلة.'
      } finally {
        loadingQuestions.value = false
      }
    }

    // 6) Timer logic
    function startTimer() {
      clearInterval(timer)
      timer = setInterval(() => {
        if (totalSec.value-- <= 0) {
          clearInterval(timer)
          screen.value = 'report'
        }
      }, 1000)
    }

    // 7) Handle activation code entry
    function onActivated(code) {
      localStorage.setItem('activated', 'true')
      isActivated.value = true
      showActivationModal.value = false
      // Unlock year 2022 in the array
      lockedYears.value = lockedYears.value.filter(y => y !== 2022)
    }

    // 8) Branch → Year
    function goYear(chosen) {
      branch.value = chosen
      screen.value = 'year'
    }

    // 9) Year selection handler
    function handleYearSelect(y) {
      const num = Number(y)
      if (lockedYears.value.includes(num) && !isActivated.value) {
        showActivationModal.value = true
      } else {
        startQuiz(y)
      }
    }

    // 10) Start quiz for a valid year
    function startQuiz(y) {
      const yearNum = Number(y)
      loadingQuestions.value = true
      loadError.value = null

      const list = allQ.value.filter(
        q => q.year === yearNum && q.type === branch.value
      )
      loadingQuestions.value = false

      if (!list.length) {
        loadError.value = 'لا توجد أسئلة لهذا الاختبار.'
        return
      }

      questions.value = list.sort((a,b)=> a.id-b.id)
      current.value   = 0
      correct.value   = 0
      Object.keys(answered).forEach(k=> delete answered[k])
      totalSec.value  = 90*60
      screen.value    = 'quiz'
      startTimer()
    }

    // 11) Question interactions
    function selectAnswer(idx) {
      const q = questions.value[current.value]
      if (answered[q.id] != null) return
      answered[q.id] = idx
      if (idx === q.correct_answer - 1) {
        correctSound.currentTime = 0
        correctSound.play()
        correct.value++
      } else {
        wrongSound.currentTime = 0
        wrongSound.play()
      }
    }
    function nextQuestion() {
      if (current.value < questions.value.length - 1) current.value++
      else screen.value = 'report'
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
        q[`attached_text_${lang.value}`] ||
        q.attached_text ||
        'لا يوجد نص مرفق'
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

    // 12) Lifecycle
    onMounted(init)
    onBeforeUnmount(()=> clearInterval(timer))

    // 13) Return all for template
    return {
      screen,
      isActivated,
      showActivationModal,
      years,
      lockedYears,
      goYear,
      handleYearSelect,
      loadingQuestions,
      loadError,
      questions,
      current,
      answered,
      correct,
      wrong,
      lang,
      formattedTime,
      percentage,
      formattedAttachedText,
      selectAnswer,
      nextQuestion,
      prevQuestion,
      jumpToQuestion,
      toggleLanguage,
      openTextScreen,
      backToQuiz,
      goBack,
      resetQuiz,
      onActivated
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
