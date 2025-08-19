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
        {{ year }}
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
    }
  },
  methods: {
    select(year) {
      if (!this.isLocked(year)) this.$emit('select', year)
    },
    isLocked(year) {
      return this.lockedYears.includes(Number(year)) && !this.isActivated
    }
  }
}
</script>

<style scoped>
/* 1. خط عربي عصري */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

:root {
  --primary:   #c59e44;   /* ذهبي */
  --secondary: #001f3f;   /* أزرق داكن */
  --text:      #f5f5f5;   /* أبيض فاتح */
  --radius:    12px;
  --gap:       1.5rem;
  --padding:   2rem;
  --transition: 0.3s ease;
}

.year-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Tajawal', sans-serif;
  margin-bottom: 2rem;
}

.title {
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  color: var(--primary);
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
  margin-bottom: calc(var(--padding) / 1.5);
}

.years-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--gap);
  background: #000;
  border: 3px solid var(--primary);
  border-radius: var(--radius);
  padding: var(--padding);
  width: fit-content;
  max-width: 90vw;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
}

.year-button {
  position: relative;
  width: 100%;
  padding: 1.25rem 0;
  font-size: clamp(1rem, 2vw, 1.3rem);
  font-weight: 600;
  color: var(--text);
  background: var(--secondary);
  border: 2px solid var(--primary);
  border-radius: var(--radius);
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 
    background var(--transition), 
    transform var(--transition), 
    box-shadow var(--transition);
}

.year-button:hover:not(.locked),
.year-button:focus:not(.locked) {
  background: var(--primary);
  color: var(--secondary);
  transform: translateY(-2px) scale(1.03);
  box-shadow: 
    0 8px 24px rgba(0, 0, 0, 0.7), 
    0 0 20px var(--primary);
  outline: none;
}

.year-button.locked {
  background: #222;
  border-color: #555;
  color: #777;
  filter: grayscale(80%);
  cursor: not-allowed;
  box-shadow: none;
}

.lock-icon {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  font-size: 1.2rem;
  opacity: 0.8;
}
</style>
