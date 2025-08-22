<template>
  <div class="question-card">

    <!-- 1. الهيدر: اختيار السؤال + المؤقت -->
    <div class="navbar select">
      <div class="navbar">
        <select
          v-model.number="selectedIndex"
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

    <!-- 3. شريط التحكم السفلي (أيقونات فقط) -->
    <div class="footer-controls">
      <button
        class="control-btn"
        @click="$emit('prev')"
        :disabled="currentIndex === 0"
        aria-label="السابق"
      >⬅️</button>

      <button
        v-if="hasText"
        class="control-btn"
        @click="openText"
        aria-label="عرض النص المرفق"
      >📄</button>

      <button
        class="control-btn"
        @click="$emit('toggle-lang')"
        aria-label="تبديل لغة"
      >🌐</button>

      <button
        class="control-btn"
        @click="$emit('next')"
        aria-label="التالي أو عرض النتيجة"
      >
        <span v-if="currentIndex < questions.length - 1">➡️</span>
        <span v-else>🏁</span>
      </button>
    </div>

    <!-- 4. نافذة النص المرفق مع زر رجوع وإغلاق -->
    <div
      id="text-screen"
      :class="{ active: showText }"
      @click.self="closeText"
    >
      <div class="modal-text">
        <div class="modal-header">
          <button class="modal-back" @click="closeText" aria-label="رجوع">
            ← رجوع
          </button>
          <button class="modal-close" @click="closeText" aria-label="إغلاق">
            ×
          </button>
        </div>
        <div class="attached-text">
          <template v-for="(line, idx) in attachedLines" :key="idx">
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
    return {
      showText: false
    };
  },
  computed: {
    answerOpts() {
      return [1,2,3,4].map(i => this.current[`answer${i}_${this.lang}`]);
    },
    attachedText() {
      const txt = (
        this.current[`attached_text_${this.lang}`] ||
        this.current.attached_text  ||
        ''
      ).trim();
      return txt;
    },
    hasText() {
      const txt = this.attachedText;
      return txt.length > 0 && !/^[*_]+$/.test(txt);
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



