<template>
  <div class="quiz-container">

    <!-- Dropdown + Attached-text button -->
    <div class="question-nav controls">
      <select
        v-model.number="selectedIndex"
        class="question-jump"
      >
        <option
          v-for="(q, idx) in questions"
          :key="q.id"
          :value="idx"
        >
          سؤال {{ idx + 1 }} من {{ questions.length }}
          {{ statuses[idx] }}
        </option>
      </select>
    </div>

    <!-- Score & Timer -->
    <div class="header-row">
      <div id="score-summary">
        صح: {{ score.correct }} | خطأ: {{ wrong }}
      </div>
      <div class="timer">
        <i class="timer-icon" /> {{ formattedTime }}
      </div>
    </div>

    <!-- نص مرفق -->
    <button
      v-if="hasText"
      class="open-text-btn"
      @click="$emit('open-text')"
      title="عرض النص المرفق"
    >📝</button>

    <!-- السؤال -->
    <h2 id="question">{{ current[`question_${lang}`] }}</h2>

    <!-- خيارات الإجابة -->
    <div class="answers">
      <button
        v-for="(ans, idx) in answerOpts"
        :key="idx"
        :disabled="isAnswered"
        :class="getAnswerClass(idx)"
        @click="selectAnswer(idx)"
      >
        {{ ans }}
      </button>
    </div>

    <!-- أزرار التنقل والأدوات -->
    <div class="nav-btns controls">
      <button @click="$emit('next')">
        {{ currentIndex === questions.length - 1 ? 'إظهار النتيجة' : 'التالي' }}
      </button>
      <button @click="$emit('toggle-lang')">🌐</button>
      <button
        @click="$emit('prev')"
        :disabled="currentIndex === 0"
      >السابق</button>
    </div>

  </div>
</template>

<script>
export default {
  name: 'QuestionCard',
  props: {
    questions:     { type: Array,  required: true },
    current:       { type: Object, required: true },
    currentIndex:  { type: Number, required: true },
    answered:      { type: Object, required: true },
    score:         { type: Object, required: true },
    lang:          { type: String, required: true },
    formattedTime: { type: String, required: true }
  },
  computed: {
    // بناء خيارات الإجابة
    answerOpts() {
      return [1, 2, 3, 4].map(i =>
        this.current[`answer${i}_${this.lang}`]
      )
    },
    // عدد الأسئلة الخاطئة
    wrong() {
      return Object.keys(this.answered).length - this.score.correct
    },
    // هل يوجد نص مرفق؟
    hasText() {
      return Boolean(
        this.current[`attached_text_${this.lang}`] ||
        this.current.attached_text
      )
    },
    // هل أُجيب على هذا السؤال؟
    isAnswered() {
      return this.answered[this.current.id] !== undefined
    },
    // فهرس الإجابة الصحيحة
    correctIndex() {
      return this.current.correct_answer - 1
    },
    // مصفوفة حالات الأسئلة: ✅ أو ❌ أو '' إذا لم يُجب بعد
    statuses() {
      return this.questions.map(q => {
        const ans = this.answered[q.id]
        if (ans == null) return ''
        return ans === (q.correct_answer - 1) ? '✅' : '❌'
      })
    },
    // v-model للـ select مع استخدام val في setter
    selectedIndex: {
      get() {
        return this.currentIndex
      },
      set(val) {
        this.$emit('jump', val)
      }
    }
  },
  methods: {
    selectAnswer(idx) {
      this.$emit('answer', idx)
    },
    getAnswerClass(idx) {
      if (!this.isAnswered) return 'option'
      if (idx === this.correctIndex) return 'option correct'
      if (idx === this.answered[this.current.id] && idx !== this.correctIndex)
        return 'option wrong'
      return 'option'
    }
  }
}
</script>

