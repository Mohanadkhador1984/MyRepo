<template>
  <div class="quiz-container">
    <!-- 1. Dropdown للتنقل بين الأسئلة -->
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

    <!-- 2. الملخص والعداد -->
    <div class="header-row">
      <div id="score-summary">
        صح: {{ score.correct }} | خطأ: {{ wrong }}
      </div>
      <div class="timer">
        <i class="timer-icon" /> {{ formattedTime }}
      </div>
    </div>

    <!-- 3. السؤال وزرّي النص والترجمة -->
    <h2 id="question">{{ current[`question_${lang}`] }}</h2>
    <div class="question-actions">
      <button
        v-if="hasText"
        class="open-text-btn"
        @click="openText"
        title="عرض النص المرفق"
      >
        <i class="fas fa-file-alt"></i>
      </button>
      <button
        class="lang-toggle-btn"
        @click="$emit('toggle-lang')"
        @mouseenter="showTooltip = true"
        @mouseleave="showTooltip = false"
        title="ترجمة"
      >
        <i class="fas fa-language"></i>
        <span v-if="showTooltip" class="tooltip">ترجمة</span>
      </button>
    </div>

    <!-- 4. خيارات الإجابة -->
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

    <!-- 5. أزرار التنقل -->
    <div class="nav-btns controls">
      <button
        class="prev-btn"
        @click="$emit('prev')"
        :disabled="currentIndex === 0"
      >
        السابق
      </button>
      <button
        class="next-btn"
        @click="$emit('next')"
      >
        {{ currentIndex === questions.length - 1
          ? 'إظهار النتيجة'
          : 'التالي' }}
      </button>
    </div>
  </div>

  <!-- 6. مودال النص المرفق -->
  <div
    id="text-screen"
    :class="{ active: showText }"
    @click.self="closeText"
  >
    <div class="modal-text">
      <button class="close-btn" @click="closeText">&times;</button>
      <div class="attached-text">
        <template v-for="(line, idx) in attachedLines" :key="idx">
          <p :class="idx % 2 === 0 ? 'en-line' : 'ar-line'">
            {{ line }}
          </p>
        </template>
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
      showText:    false,  // لإظهار/إخفاء المودال
      showTooltip: false   // للتحكم في التلميح على زر الترجمة
    };
  },

  computed: {
    // بناء خيارات الإجابة حسب اللغة
    answerOpts() {
      return [1, 2, 3, 4].map(i =>
        this.current[`answer${i}_${this.lang}`]
      );
    },

    // عدد الأخطاء
    wrong() {
      return Object.keys(this.answered).length - this.score.correct;
    },

    // هل هناك نص مرفق فعال؟
    hasText() {
      const txt = (
        this.current[`attached_text_${this.lang}`] ||
        this.current.attached_text ||
        ''
      ).trim();
      return txt.length > 0 && !/^[*_-\s]+$/.test(txt);
    },

    // هل أجيب على هذا السؤال؟
    isAnswered() {
      return this.answered[this.current.id] !== undefined;
    },

    // مؤشر الإجابة الصحيحة
    correctIndex() {
      return this.current.correct_answer - 1;
    },

    // حالة كل سؤال (✅ أو ❌ أو فراغ)
    statuses() {
      return this.questions.map(q => {
        const ans = this.answered[q.id];
        if (ans == null) return '';
        return ans === this.correctIndex ? '✅' : '❌';
      });
    },

    // ربط select بالتنقل بين الأسئلة
    selectedIndex: {
      get() {
        return this.currentIndex;
      },
      set(val) {
        this.$emit('jump', val);
      }
    },

    // تقسيم النص المرفق إلى أسطر منفصلة
    attachedLines() {
      const raw = (
        this.current[`attached_text_${this.lang}`] ||
        this.current.attached_text ||
        ''
      );
      return raw
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0);
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
