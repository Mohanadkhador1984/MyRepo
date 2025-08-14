<!-- src/views/AdminScreen.vue -->
<template>
  <div class="login-page">
    <div class="login-card">
      <h2>🛠️ لوحة المدير</h2>

      <button @click="generateCode" :disabled="loading">
        <span v-if="!loading">➕ إنشاء رمز تفعيل</span>
        <span v-else><i class="spinner"></i> جاري الإنشاء...</span>
      </button>

      <ul class="code-list">
        <li v-for="code in codes" :key="code.id">
          <code>{{ code.code }}</code>
        </li>
      </ul>

      <button class="link-btn" @click="$router.push({ name: 'Quiz' })">
        ← العودة
      </button>
    </div>
  </div>
</template>

<script>
import { getActivationCodes, createActivationCode } from '@/services/authService'

export default {
  name: 'AdminScreen',
  data() {
    return {
      codes: [],
      loading: false
    }
  },
  async mounted() {
    this.codes = await getActivationCodes()
  },
  methods: {
    async generateCode() {
      this.loading = true
      try {
        const newCode = await createActivationCode()
        this.codes.unshift(newCode)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.code-list {
  list-style: none;
  padding: 0;
  margin-top: 1rem;
}

.code-list li {
  background: #333;
  margin-bottom: 0.5rem;
  padding: 0.5rem;
  border-radius: 4px;
}

.link-btn {
  margin-top: 1rem;
  background: none;
  border: none;
  color: #ffd700;
  cursor: pointer;
  text-decoration: underline;
  font-size: 0.9rem;
}
</style>
