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

    <!-- 4. نافذة النص المرفق مع زر رجوع عائم في الأسفل -->
    <div
      id="text-screen"
      :class="{ active: showText }"
      @keydown.esc="closeText"
    >
      <div class="modal-overlay" @click="closeText"></div>
      <div class="modal-text">
        <div class="modal-header">
          <h3>النص المرفق</h3>
          <!-- <button class="modal-close" @click="closeText" aria-label="إغلاق">×</button> -->
        </div>
        <div class="attached-body">
          <div class="attached-text">
            <template v-for="(line, idx) in attachedLines" :key="idx">
              <p :class="idx % 2 === 0 ? 'en-line' : 'ar-line'">
                {{ line }}
              </p>
            </template>
          </div>
          <button
            class="modal-back-floating"
            @click="closeText"
            aria-label="رجوع"
          >← رجوع</button>
        </div>
      </div>
    </div>

    <!-- 5. شاشة تأكيد الخروج عند الضغط على زر الرجوع في الجهاز -->
    <div v-if="showConfirm" class="confirm-overlay" @click.self="closeConfirm">
      <div class="confirm-dialog">
        <h3>تـأكيـد الخـروج</h3>
        <p>هل تريد فعلاً إلغاء الامتحان؟ لن تتمكن من استئنافه بعد ذلك.</p>
        <div class="confirm-actions">
          <button class="btn btn-outline" @click="closeConfirm">أكمل الامتحان</button>
          <button class="btn btn-danger"  @click="confirmLeave">إلغاء الامتحان</button>
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
    lang:          { type: String, required: true },
    formattedTime: { type: String, required: true }
  },
  data() {
    return {
      showText:    false,
      showConfirm: false,
      examFinished: false
    };
  },
  computed: {
    answerOpts() {
      return [1,2,3,4].map(i => this.current[`answer${i}_${this.lang}`]);
    },
    attachedText() {
      const txt = (
        this.current[`attached_text_${this.lang}`] ||
        this.current.attached_text ||
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
      return this.questions.map((q, i) => {
        const ans = this.answered[q.id];
        if (ans == null) return '';
        return ans === this.questions[i].correct_answer - 1 ? '✅' : '❌';
      });
    },
    selectedIndex: {
      get() { return this.currentIndex; },
      set(v) { this.$emit('jump', v); }
    }
  },
  methods: {
    selectAnswer(idx) {
      this.$emit('answer', idx);
    },
    openText() {
      this.showText = true;
      this.$nextTick(() => {
        document.getElementById('text-screen').focus();
      });
    },
    closeText() {
      this.showText = false;
    },
    getAnswerClass(idx) {
      if (!this.isAnswered) return '';
      if (idx === this.correctIndex) return 'correct';
      return this.answered[this.current.id] === idx ? 'wrong' : '';
    },
    // اعتراض زر الرجوع في المتصفح/الجهاز
    // eslint-disable-next-line no-unused-vars
    handlePopState(event) {
      if (!this.examFinished) {
        history.pushState({ inQuiz: true }, '', location.href);
        this.showConfirm = true;
      }
    },
    closeConfirm() {
      this.showConfirm = false;
    },
    confirmLeave() {
      this.examFinished = true;
      this.$emit('exam-finished');
      this.closeConfirm();
      history.back();
    }
  },
  mounted() {
    // منع الخروج المفاجئ
    history.pushState({ inQuiz: true }, '', location.href);
    window.addEventListener('popstate', this.handlePopState);
  },
  beforeUnmount() {
    window.removeEventListener('popstate', this.handlePopState);
  }
};
</script>

<style scoped>
/* الخلفية المموّهة للنص */
#text-screen .modal-overlay {
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(6px);
}

/* مودال تأكيد الخروج */
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
}
.confirm-dialog {
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem;
  width: 300px;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.confirm-dialog h3 {
  margin-bottom: 0.8rem;
  font-family: 'Cairo', sans-serif;
  color: #dc2626;
}
.confirm-dialog p {
  font-family: 'Cairo', sans-serif;
  margin-bottom: 1.2rem;
  color: #333;
}
.confirm-actions {
  display: flex;
  gap: 0.6rem;
}
.confirm-actions .btn {
  flex: 1;
  padding: 0.6rem;
  border-radius: 8px;
  font-family: 'Cairo', sans-serif;
  font-weight: 600;
  cursor: pointer;
  border: none;
}
.btn-outline {
  background: transparent;
  border: 2px solid #16a34a;
  color: #16a34a;
}
.btn-outline:hover {
  background: #16a34a;
  color: #fff;
}
.btn-danger {
  background: #dc2626;
  color: #fff;
}
.btn-danger:hover {
  background: #b91c1c;
}
</style>
