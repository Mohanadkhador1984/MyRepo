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
          @click="selectLocalAnswer(idx)"
        >
          {{ ans }}
        </button>
      </div>
    </section>

    <!-- 3. شريط التحكم السفلي -->
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

    <!-- 4. نافذة النص المرفق -->
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

    <!-- 5. نافذة تأكيد إلغاء الامتحان -->
    <div v-if="showConfirm" class="modal-overlay" @click.self="closeModal">
      <div class="modal-window">
        <i class="fas fa-exclamation-circle modal-icon"></i>
        <h3 class="modal-title">تأكيد إلغاء الامتحان</h3>
        <p class="modal-text">
          هل تريد فعلاً إلغاء الامتحان؟ لن تتمكن من استئنافه بعد ذلك.
        </p>
        <div class="modal-actions">
          <button class="btn btn-outline" @click="closeModal">
            أكمل الامتحان
          </button>
          <button class="btn btn-danger" @click="confirmLeave">
            ألغي الامتحان
          </button>
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
      showText:     false,
      showConfirm:  false,
      examFinished: false,
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
    },
    allAnswered() {
      return Object.keys(this.answered).length >= this.questions.length;
    }
  },
  watch: {
    allAnswered(val) {
      if (val) this.finishExam();
    }
  },
  mounted() {
    history.pushState({ inQuiz: true }, '', location.href);
    window.addEventListener('popstate', this.handleBack);
    window.addEventListener('beforeunload', this.beforeUnload);
  },
  beforeUnmount() {
    window.removeEventListener('popstate', this.handleBack);
    window.removeEventListener('beforeunload', this.beforeUnload);
  },
  methods: {
    selectLocalAnswer(idx) {
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
    },

    // eslint-disable-next-line no-unused-vars
    handleBack(event) {
      if (!this.examFinished) {
        history.pushState({ inQuiz: true }, '', location.href);
        this.showConfirm = true;
      }
    },
    beforeUnload(e) {
      if (!this.examFinished) {
        const msg = 'الاختبار لم ينتهِ بعد. تأكيد الخروج وإلغاء الامتحان؟';
        e.returnValue = msg;
        return msg;
      }
    },
    closeModal() {
      this.showConfirm = false;
    },
    confirmLeave() {
      this.examFinished = true;
      this.finishExam();
      this.closeModal();
      history.back();
    },
    finishExam() {
      window.removeEventListener('popstate', this.handleBack);
      window.removeEventListener('beforeunload', this.beforeUnload);
      this.$emit('exam-finished');
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-window {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(12px);
  border-radius: 16px;
  padding: 1.8rem;
  width: 300px;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0,0,0,0.7);
  animation: slide-down 0.3s ease-out forwards;
}

.modal-icon {
  font-size: 2.2rem;
  color: #fbbf24;
  margin-bottom: 0.4rem;
}

.modal-title {
  font-family: 'Cairo', sans-serif;
  font-size: 1.4rem;
  color: #fbbf24;
  margin-bottom: 0.6rem;
}

.modal-text {
  font-family: 'Cairo', sans-serif;
  font-size: 0.95rem;
  color: #eee;
  margin-bottom: 1.2rem;
  line-height: 1.3;
}

.modal-actions {
  display: flex;
  gap: 0.6rem;
}

.btn {
  flex: 1;
  padding: 0.55rem 0.8rem;
  border-radius: 8px;
  font-family: 'Cairo', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.2s;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 10px rgba(0,0,0,0.5);
}

.btn-outline {
  background: transparent;
  border: 2px solid #16a34a;
  color: #16a34a;
}

.btn-outline:hover {
  background: #16a34a;
  color: #111;
}

.btn-danger {
  background: #dc2626;
  border: 2px solid #b91c1c;
  color: #fff;
}

.btn-danger:hover {
  background: #b91c1c;
}

@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-15px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}




/* حالة عرض النتائج */
.control-btn.next.finish {
  background: linear-gradient(90deg, #facc15, #f43f5e);
  box-shadow: 0 0 8px rgba(250, 204, 21, 0.8),
              0 0 16px rgba(244, 63, 94, 0.8);
  animation: blink 1s ease-in-out infinite alternate;
}

/* أيقونة وزوم بسيط */
.control-btn .icon {
  display: inline-block;
  font-size: 1.2rem;
  transition: transform 0.2s;
}

.control-btn.next.finish .icon {
  animation: pop 0.6s ease infinite;
}

/* Keyframes */
@keyframes blink {
  from { opacity: 1; }
  to   { opacity: 0.6; }
}

@keyframes pop {
  0%   { transform: scale(1); }
  50%  { transform: scale(1.3); }
  100% { transform: scale(1); }
}
</style>
