<template>
  <div class="year-selector">
    <h2 class="title">اختر الاختبار</h2>
    <div class="years-grid">
      <button
        v-for="year in options"
        :key="year"
        :disabled="isLocked(year)"
        @click="select(year)"
        :class="['year-button', { locked: isLocked(year) }]"
      >
        <span class="year-text">{{ year }}</span>
        <span v-if="isLocked(year)" class="lock-icon">🔒</span>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'YearSelector',
  props: {
    options: {
      type: Array,
      required: true
    }
  },
  emits: ['select'],
  data() {
    return {
      lockedYears: [2022],
      isActivated: localStorage.getItem('activated') === 'true'
    };
  },
  methods: {
    select(year) {
      if (!this.isLocked(year)) {
        this.$emit('select', year);
      }
    },
    isLocked(year) {
      return this.lockedYears.includes(Number(year)) && !this.isActivated;
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

:root {
  --gold-light:    #ffe16a;
  --gold-med:      #c59e44;
  --gold-dark:     #b07f17;
  --gold-med-rgb:  197,158,68;
  --locked-bg:     rgba(0, 0, 0, 0.75);
  --locked-border: var(--gold-med);
  --white-soft:    #f5f5f5;
  --glass-bg:      rgba(255,255,255,0.08);
  --glass-border:  rgba(255,255,255,0.2);
  --radius:        20px;
  --gap:           2rem;
  --padding:       2.5rem;
  --transition:    0.4s ease-in-out;
}

/* إطار ذهبي متدرج حول الشاشة */
.year-selector {
  position: relative;
  padding: calc(var(--padding) + 12px);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: radial-gradient(circle at center, #111 0%, #000 75%);
  font-family: 'Tajawal', sans-serif;
  overflow: hidden;
  border: 12px solid transparent;
  border-image: conic-gradient(
    from 45deg,
    var(--gold-light),
    var(--gold-med),
    var(--gold-dark),
    var(--gold-med),
    var(--gold-light)
  ) 1;
  box-shadow:
    0 0 20px var(--gold-med),
    inset 0 0 30px rgba(0,0,0,0.6);
}

/* عنوان بتدرج ذهبي وشفافية */
.title {
  font-size: clamp(2.4rem, 6vw, 3.2rem);
  font-weight: 900;
  background: linear-gradient(90deg, var(--gold-light), var(--gold-med));
  -webkit-background-clip: text;
  color: transparent;
  margin-bottom: var(--gap);
  text-shadow: 0 2px 8px rgba(0,0,0,0.8);
}

/* حاوية الأزرار بزجاج ضبابي */
.years-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--gap);
  width: 90vw;
  max-width: 540px;
  padding: var(--padding);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  backdrop-filter: blur(14px);
  box-shadow:
    inset 0 0 36px rgba(255,255,255,0.1),
    0 10px 28px rgba(0,0,0,0.75);
}

/* تصميم الأزرار العامة */
.year-button {
  position: relative;
  padding: clamp(0.8rem, 3vw, 1.2rem) 0;
  font-size: clamp(1.1rem, 3vw, 1.4rem);
  font-weight: 700;
  color: var(--white-soft);
  background: linear-gradient(145deg, var(--gold-light), var(--gold-med));
  border: 2px solid transparent;
  border-image: conic-gradient(
    from 0deg,
    var(--gold-light),
    var(--gold-med),
    var(--gold-light)
  ) 1;
  border-radius: var(--radius);
  box-shadow:
    inset -3px -3px 12px rgba(255,255,255,0.3),
    inset 3px 3px 8px rgba(0,0,0,0.4),
    0 6px 20px rgba(0,0,0,0.8);
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition);
  overflow: hidden;
}

.year-button:hover:not(.locked),
.year-button:focus:not(.locked) {
  transform: translateY(-5px) scale(1.07);
  box-shadow:
    inset -3px -3px 12px rgba(255,255,255,0.35),
    inset 3px 3px 8px rgba(0,0,0,0.45),
    0 8px 24px rgba(0,0,0,0.85),
    0 0 16px var(--gold-light);
  outline: none;
}

/* أسلوب فاخر للأزرار المؤمَّنة */
.year-button.locked {
  background: var(--locked-bg);
  border: 2px solid var(--locked-border);
  color: var(--locked-border);
  box-shadow:
    inset 0 0 8px rgba(0,0,0,0.8),
    0 0 12px rgba(var(--gold-med-rgb),0.5);
  text-shadow: 0 0 3px var(--locked-border);
  backdrop-filter: blur(4px);
  cursor: not-allowed;
}

/* إخفاء نص السنة عند القفل */
.year-button.locked .year-text {
  visibility: hidden;
}

/* أيقونة قفل متوهجة ونابضة */
.year-button.locked .lock-icon {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%) scale(1);
  font-size: clamp(1.5rem, 4vw, 2rem);
  color: var(--gold-light);
  text-shadow:
    0 0 6px var(--gold-light),
    0 0 12px var(--gold-med);
  animation: pulseLock 2.5s ease-in-out infinite;
  opacity: 0.9;
}

@keyframes pulseLock {
  0%, 100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.9;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 0.6;
  }
}

/* تحسين للشاشات الصغيرة */
@media (max-width: 360px) {
  :root {
    --gap: 1.5rem;
    --padding: 1.5rem;
  }
  .title {
    margin-bottom: 1.5rem;
    font-size: clamp(2rem, 8vw, 2.6rem);
  }
}
</style>
