<!-- src/views/DeveloperPage.vue -->
<template>
  <div class="quiz-container auth-page">
    <h1>🛠️ صفحة المطور</h1>

    <div class="form-group">
      <input
        v-model="inputId"
        type="text"
        placeholder=" "
        required
      />
      <label>معرّف الجهاز</label>
    </div>

    <button
      class="btn btn-secondary"
      @click="generateCode"
      :disabled="!inputId"
    >
      توليد كود التفعيل
    </button>

    <div v-if="generatedCode" class="code-display">
      <p>كود التفعيل:</p>
      <code>{{ generatedCode }}</code>
    </div>

    <button
      class="btn btn-accent mt-6"
      @click="$router.push('/')"
    >
      العودة للواجهة
    </button>
  </div>
</template>

<script>
export default {
  name: 'DeveloperPage',
  data() {
    return {
      inputId: '',
      generatedCode: ''
    }
  },
  methods: {
    generateCode() {
      this.generatedCode = btoa(this.inputId).slice(0, 10)
    }
  }
}
</script>

<style scoped>
/* استخدام نفس تنسيق الصفحات السابقة */
.quiz-container {
  max-width: 480px;
  margin: 2rem auto;
  padding: 2rem;
}

.auth-page h1 {
  color: var(--primary);
  font-size: clamp(1.5rem, 4vw, 2rem);
  text-align: center;
  margin-bottom: var(--spacing);
}

/* حقول الإدخال */
.form-group {
  position: relative;
  margin-bottom: 1.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid var(--text-light);
  color: var(--text);
  font-size: 1rem;
  transition: border-color var(--transition);
}

.form-group input:focus {
  outline: none;
  border-bottom-color: var(--primary);
}

.form-group label {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
  pointer-events: none;
  transition: transform var(--transition), font-size var(--transition), color var(--transition);
}

.form-group input:focus + label,
.form-group input:not(:placeholder-shown) + label {
  transform: translateY(-160%) scale(0.85);
  color: var(--primary);
  font-size: 0.85rem;
}

/* زرول */
.btn {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition), transform var(--transition);
  margin-top: var(--spacing);
}

/* ثانوي */
.btn-secondary {
  background: var(--secondary);
  color: var(--text);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--primary);
  transform: translateY(-2px);
}

/* رابط العودة */
.btn-accent {
  background: var(--accent);
  color: var(--text);
}

.btn-accent:hover {
  background: var(--primary);
  transform: translateY(-2px);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* عرض الكود */
.code-display {
  margin-top: 1.5rem;
  text-align: center;
}

.code-display p {
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 0.5rem;
}

.code-display code {
  display: inline-block;
  background: rgba(255,255,255,0.1);
  color: var(--primary);
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-family: monospace;
  box-shadow: inset 0 0 8px rgba(0,0,0,0.4);
}
</style>
