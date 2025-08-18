<template>
  <div class="question-card">

    <!-- 1. الهيدر: اختيار السؤال + المؤقت -->
    <div class="sticky-navbar">
      <div class="navbar">
        <div class="custom-select-wrapper">
          <select
            v-model.number="selectedIndex"
            class="custom-select"
            aria-label="اختر سؤالاً"
          >
            <option
              v-for="(q, idx) in questions"
              :key="q.id"
              :value="idx"
            >
              سؤال {{ idx + 1 }} / {{ questions.length }} {{ statuses[idx] }}
            </option>
          </select>
          <span class="select-arrow">⌄</span>
        </div>

        <div class="timer" aria-label="المؤقت">
          <span class="timer-icon"></span>
          {{ formattedTime }}
        </div>
      </div>
    </div>

    <!-- 2. نص السؤال والإجابات -->
    <section class="question-section">
      <h2 id="question" class="question-text">
        {{ current[`question_${lang}`] }}
      </h2>
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
    </section>

    <!-- 3. شريط التحكم السفلي بأيقونات فقط -->
    <div class="footer-controls">
      <button
        class="control-btn"
        @click="$emit('prev')"
        :disabled="currentIndex === 0"
        aria-label="السابق"
      >
        ▼
      </button>

      <button
        v-if="hasText"
        class="control-btn"
        @click="openText"
        aria-label="عرض النص"
      >
        📄
      </button>

      <button
        class="control-btn"
        @click="$emit('toggle-lang')"
        aria-label="تبديل لغة"
      >
        🌐
      </button>

      <button
        class="control-btn"
        @click="$emit('next')"
        aria-label="التالي أو عرض النتيجة"
      >
        <template v-if="currentIndex < questions.length - 1">➡️</template>
        <template v-else>🏁</template>
      </button>
    </div>

    <!-- 4. مودال النص المرفق مع زرّ رجوع محترف -->
    <div
      id="text-screen"
      :class="{ active: showText }"
      @click.self="closeText"
    >
      <div class="modal-text">
        <div class="modal-header">
          <button
            class="modal-back"
            @click="closeText"
            aria-label="رجوع"
          >
            ←
          </button>
          <button
            class="modal-close"
            @click="closeText"
            aria-label="إغلاق"
          >
            ×
          </button>
        </div>
        <div class="attached-text">
          <template
            v-for="(line, idx) in attachedLines"
            :key="idx"
          >
            <p :class="idx % 2 === 0 ? 'en-line' : 'ar-line'">
              {{ line }}
            </p>
          </template>
        </div>
      </div>
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
  data() {
    return { showText: false };
  },
  computed: {
    answerOpts() {
      return [1,2,3,4].map(i => this.current[`answer${i}_${this.lang}`]);
    },
    attachedText() {
      return (
        this.current[`attached_text_${this.lang}`] ||
        this.current.attached_text ||
        ''
      ).trim();
    },
    hasText() {
      return this.attachedText.length > 0;
    },
    attachedLines() {
      return this.attachedText
        .split('\n')
        .map(l => l.trim())
        .filter(Boolean);
    },
    isAnswered() {
      return this.answered[this.current.id] !== undefined;
    },
    correctIndex() {
      return this.current.correct_answer - 1;
    },
    statuses() {
      return this.questions.map((q, idx) => {
        const ans = this.answered[q.id];
        if (ans == null) return '';
        return ans === this.questions[idx].correct_answer - 1
          ? '✅'
          : '❌';
      });
    },
    selectedIndex: {
      get() { return this.currentIndex; },
      set(val) { this.$emit('jump', val); }
    }
  },
  methods: {
    selectAnswer(idx) {
      this.$emit('answer', idx);
    },
    openText() {
      this.showText = true;
    },
    closeText() {
      this.showText = false;
    },
    getAnswerClass(idx) {
      if (!this.isAnswered) return '';
      if (idx === this.correctIndex) return 'correct';
      return this.answered[this.current.id] === idx ? 'wrong' : '';
    }
  }
};
</script>

<style scoped>
/*— فقط تعديل الدروب داون ليست لتصبح أفخم —*/
.custom-select-wrapper {
  position: relative;
  display: inline-block;
  width: 220px;
}

.custom-select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  width: 100%;
  padding: 0.75rem 1.5rem 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
 
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: box-shadow 0.2s, border-color 0.2s;
}

.custom-select:focus {
  outline: none;
  border-color: #6c63ff;
  box-shadow: 0 4px 12px rgba(108, 99, 255, 0.3);
}

.select-arrow {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
  font-size: 0.75rem;
  color: #6c63ff;
}
</style>
