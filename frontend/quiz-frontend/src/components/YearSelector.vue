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
/* استيراد خط عربي عصري */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

:root {
  --primary:    #c59e44;    /* ذهبي */
  --secondary:  #001f3f;    /* أزرق داكن */
  --text-light: #f5f5f5;    /* أبيض فاتح */
  --radius:     12px;
  --gap:        1rem;
  --padding:    1.5rem;
  --transition: 0.3s ease;
}

.year-selector {
  font-family: 'Tajawal', sans-serif;
  text-align: center;
  padding: var(--padding) 0;
}

.title {
  font-size: clamp(1.8rem, 5vw, 2.4rem);
  color: var(--primary);
  margin-bottom: var(--gap);
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.6);
}

/* شبكة الأزرار: جدولية واستجابة تامة على الهاتف */
.years-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: var(--gap);
  margin: 0 auto;
  padding: var(--padding);
  background: #000;
  border: 3px solid var(--primary);
  border-radius: var(--radius);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);

  /* تشغل 90% من عرض الشاشة على الهواتف */
  width: 90vw;
  max-width: 480px;
}

/* زر السنة */
.year-button {
  position: relative;
  width: 100%;
  padding: 1rem 0;
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  font-weight: 600;
  color: var(--text-light);
  background: var(--secondary);
  border: 2px solid var(--primary);
  border-radius: var(--radius);
  cursor: pointer;
  transition:
    background var(--transition),
    transform var(--transition),
    box-shadow var(--transition);
  display: flex;
  justify-content: center;
  align-items: center;
}

.year-button:hover:not(.locked),
.year-button:focus:not(.locked) {
  background: var(--primary);
  color: var(--secondary);
  transform: translateY(-3px) scale(1.03);
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
  top: 0.5rem;
  right: 0.5rem;
  font-size: 1.2rem;
  opacity: 0.8;
}
</style>
