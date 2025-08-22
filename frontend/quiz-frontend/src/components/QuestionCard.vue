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
      <!-- الخلفية المموّهة -->
      <div class="modal-overlay" @click="closeText"></div>

      <!-- صندوق النص المميز -->
      <div class="modal-text">
        <!-- رأس المودال -->
        <div class="modal-header">
          <h3>النص المرفق</h3>
          <button class="modal-close" @click="closeText" aria-label="إغلاق">×</button>
        </div>

        <!-- جسم المودال -->
        <div class="attached-body">
          <div class="attached-text">
            <template v-for="(line, idx) in attachedLines" :key="idx">
              <p :class="idx % 2 === 0 ? 'en-line' : 'ar-line'">
                {{ line }}
              </p>
            </template>
          </div>
          <!-- زر الرجوع العائم -->
          <button
            class="modal-back-floating"
            @click="closeText"
            aria-label="رجوع"
          >
            ← رجوع
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
    }
  }
};
</script>

<style scoped>
/* النص المرفق – شاشة مودال كاملة */
#text-screen {
  position: fixed;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
#text-screen.active {
  display: flex;
  animation: fadeIn 0.25s ease-out;
}

/* الخلفية المموّهة */
.modal-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(6px);
}

/* صندوق المودال */
.modal-text {
  position: relative;
  width: 90%;
  max-width: 640px;
  max-height: 90vh;
  background: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
}

/* رأس المودال */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(90deg, #6a11cb, #2575fc);
  padding: 1rem 1.5rem;
  color: #fff;
}
.modal-header h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
}
.modal-close {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 1.6rem;
  cursor: pointer;
  transition: transform 0.2s;
}
.modal-close:hover {
  transform: scale(1.2);
}

/* جسم المودال مع التمرير */
.attached-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}
.attached-text {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  line-height: 1.6;
  color: #333;
  font-family: 'Cairo', sans-serif;
}
/* شريط التمرير المخصص */
.attached-text::-webkit-scrollbar {
  width: 8px;
}
.attached-text::-webkit-scrollbar-track {
  background: transparent;
}
.attached-text::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

/* زر الرجوع العائم أسفل النص */
.modal-back-floating {
  position: sticky;
  bottom: 0;
  width: 100%;
  padding: 0.8rem;
  background: linear-gradient(90deg, #2575fc, #6a11cb);
  color: #fff;
  font-size: 1rem;
  text-align: center;
  border: none;
  cursor: pointer;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.2);
  transition: background 0.3s, transform 0.2s;
  z-index: 1;
}
.modal-back-floating:hover {
  background: linear-gradient(90deg, #1e65d1, #205bbf);
  transform: translateY(-2px);
}

/* تأثير فتح المودال */
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
</style>
