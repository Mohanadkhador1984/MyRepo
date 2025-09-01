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
        <span class="year-content">
          <span class="year-text">{{ year }}</span>
          <span v-if="isLocked(year)" class="lock-icon">🔒</span>
        </span>
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
  --gold-light: #ffe16a;
  --gold-med: #c59e44;
  --gold-dark: #b07f17;
  --gold-med-rgb: 197,158,68;
  --locked-bg: rgba(0, 0, 0, 0.8);
  --locked-border: var(--gold-med);
  --white-soft: #f5f5f5;
  --glass-bg: rgba(255, 255, 255, 0.05);
  --glass-border: rgba(255, 255, 255, 0.15);
  --radius: 20px;
  --gap: 2rem;
  --padding: 3rem;
  --transition: 0.35s ease-in-out;
}

.year-selector {
  position: relative;
  padding: calc(var(--padding) + 10px);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
  font-family: 'Tajawal', sans-serif;
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
    inset 0 0 30px rgba(255, 255, 255, 0.05),
    0 0 30px var(--gold-med);
  overflow: hidden;
}

.title {
  font-size: clamp(2.5rem, 6vw, 3.5rem);
  font-weight: 900;
  background: linear-gradient(90deg, var(--gold-light), var(--gold-med));
  -webkit-background-clip: text;
  color: transparent;
  margin-bottom: var(--gap);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
}

.years-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--gap);
  width: 90vw;
  max-width: 600px;
  padding: var(--padding);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  backdrop-filter: blur(12px);
  box-shadow:
    inset 0 0 36px rgba(255, 255, 255, 0.08),
    0 10px 30px rgba(0, 0, 0, 0.7);
}

.year-button {
  position: relative;
  padding: clamp(1rem, 3vw, 1.4rem) 0;
  font-size: clamp(1.2rem, 3vw, 1.6rem);
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
    inset -3px -3px 12px rgba(255,255,255,0.25),
    inset 3px 3px 8px rgba(0,0,0,0.4),
    0 6px 20px rgba(0,0,0,0.8);
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition);
  overflow: hidden;
}

.year-button:hover:not(.locked),
.year-button:focus:not(.locked) {
  transform: translateY(-6px) scale(1.05);
  box-shadow:
    inset -3px -3px 12px rgba(255,255,255,0.3),
    inset 3px 3px 10px rgba(0,0,0,0.45),
    0 8px 22px rgba(0,0,0,0.9),
    0 0 14px var(--gold-light);
  outline: none;
}

.year-button.locked {
  background: var(--locked-bg);
  border: 2px solid var(--locked-border);
  color: var(--locked-border);
  box-shadow:
    inset 0 0 8px rgba(0, 0, 0, 0.8),
    0 0 12px rgba(var(--gold-med-rgb), 0.4);
  text-shadow: 0 0 3px var(--locked-border);
  cursor: not-allowed;
}

.year-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.lock-icon {
  font-size: 1.4rem;
  color: var(--gold-light);
  animation: pulseLock 2.5s ease-in-out infinite;
  text-shadow:
    0 0 6px var(--gold-light),
    0 0 8px var(--gold-med);
}

@keyframes pulseLock {
  0%, 100% {
    transform: scale(1);
    opacity: 0.9;
  }
  50% {
    transform: scale(1.2);
    opacity: 0.6;
  }
}

@media (max-width: 360px) {
  :root {
    --gap: 1.2rem;
    --padding: 1.5rem;
  }

  .title {
    font-size: clamp(2rem, 8vw, 2.6rem);
  }
}
</style>