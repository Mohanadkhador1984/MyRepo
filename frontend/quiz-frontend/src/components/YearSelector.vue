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
  props: { options: { type: Array, required: true } },
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
/* استخدام متغيرات جذّابة */
.year-selector {
  max-width: 800px;
  margin: 0 auto 2rem;
  padding: var(--spacing);
}

.title {
  color: var(--primary);
  font-size: clamp(1.5rem, 4vw, 2rem);
  margin-bottom: calc(var(--spacing) * 1.5);
  text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.years-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--spacing);
}

/* زر السنة */
.year-button {
  position: relative;
  background: var(--bg-card);
  color: var(--text-light);
  border: 2px solid var(--primary);
  padding: clamp(0.75rem, 2vw, 1rem) clamp(1rem, 3vw, 2rem);
  font-size: clamp(1rem, 1.5vw, 1.2rem);
  font-weight: 600;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition), transform var(--transition), box-shadow var(--transition);
  box-shadow: inset 0 0 10px rgba(0,0,0,0.4);
}

/* تأثير التحويم */
.year-button:hover:not(.locked) {
  background: var(--secondary);
  color: var(--text);
  transform: translateY(-3px) scale(1.03);
  box-shadow:
    0 4px 12px rgba(0,0,0,0.5),
    0 0 20px var(--primary);
}

/* الحالة المقفلة */
.year-button.locked {
  background: #222;
  border-color: #555;
  color: #777;
  cursor: not-allowed;
  box-shadow: none;
  filter: grayscale(80%);
}

/* أيقونة القفل */
.lock-icon {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 1.2rem;
  opacity: 0.8;
}
</style>
