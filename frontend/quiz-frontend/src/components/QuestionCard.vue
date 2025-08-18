
<template>
  <div class="question-card">
    <!-- ✅ الهيدر الرئيسي للتطبيق -->
   

    <!-- ✅ شريط التنقل الثابت الجديد -->
    <div class="sticky-navbar">
      <div class="navbar">
        <select v-model.number="selectedIndex" aria-label="اختر سؤالاً">
          <option v-for="(q, idx) in questions" :key="q.id" :value="idx">
            سؤال {{ idx + 1 }} / {{ questions.length }} {{ statuses[idx] }}
          </option>
        </select>

        
        <div class="timer" aria-label="المؤقت">
          <span class="timer-icon"></span> {{ formattedTime }}
        </div>
      </div>
    </div>



  

    <!-- 2. نص السؤال -->
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

    <!-- 4. شريط التحكم السفلي -->
    <div class="footer-controls">
      <button
        class="control-btn"
        @click="$emit('prev')"
        :disabled="currentIndex === 0"
        aria-label="السؤال السابق"
      >
        ⬅️ السابق
      </button>

      <button
        v-if="hasText"
        class="control-btn"
        @click="openText"
        title="فتح النص المرفق"
        aria-label="فتح النص المرفق"
      >
        📄 نص
      </button>

      <button
        class="control-btn"
        @click="$emit('toggle-lang')"
        :aria-label="lang === 'ar' ? 'تبديل إلى الإنجليزية' : 'Switch to Arabic'"
      >
        🌐 {{ lang === 'ar' ? 'EN' : 'AR' }}
      </button>

      <button
        class="control-btn"
        @click="$emit('next')"
        aria-label="السؤال التالي أو عرض النتيجة"
      >
        {{ currentIndex === questions.length - 1 ? 'عرض النتيجة 🏁' : 'التالي ➡️' }}
      </button>
    </div>

    <!-- 5. نافذة النص المرفق -->
    <div id="text-screen" :class="{ active: showText }" @click.self="closeText">
      <div class="modal-text">
        <button class="close-btn" @click="closeText" aria-label="إغلاق النص">
          &times;
        </button>
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
      return [1, 2, 3, 4].map(i => this.current[`answer${i}_${this.lang}`]);
    },
    wrong() {
      return Object.keys(this.answered).length - this.score.correct;
    },
    attachedText() {
      return (
        this.current[`attached_text_${this.lang}`] ||
        this.current.attached_text ||
        ''
      ).trim();
    },
    hasText() {
      return this.attachedText.length > 0 && !/^[*_-\s]+$/.test(this.attachedText);
    },
    attachedLines() {
      return this.attachedText
        .split('\n')
        .map(line => line.trim())
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
        return ans === this.questions[idx].correct_answer - 1 ? '✅' : '❌';
      });
    },
    selectedIndex: {
      get() {
        return this.currentIndex;
      },
      set(val) {
        this.$emit('jump', val);
      }
    }
  },
  methods: {
    openText() {
      this.showText = true;
    },
    closeText() {
      this.showText = false;
    },
    selectAnswer(idx) {
      this.$emit('answer', idx);
    },
    getAnswerClass(idx) {
      if (!this.isAnswered) return '';
      if (idx === this.correctIndex) return 'correct';
      if (idx === this.answered[this.current.id]) return 'wrong';
      return '';
    }
  }
};
</script>

