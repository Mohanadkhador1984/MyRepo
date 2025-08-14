<!-- src/views/ActivationScreen.vue -->
<template>
  <div class="login-page">
    <div class="login-card">
      <h2>🔑 تفعيل جهازك</h2>

      <form @submit.prevent="doActivate">
        <div class="form-group">
          <input
            v-model="activationCode"
            type="text"
            placeholder=" "
            required
          />
          <label>رمز التفعيل</label>
        </div>

        <button type="submit" :disabled="loading">
          <span v-if="!loading">تفعيل</span>
          <span v-else><i class="spinner"></i> جاري التفعيل...</span>
        </button>

        <p v-if="error" class="error">⚠️ {{ error }}</p>
      </form>

      <button class="link-btn" @click="$router.push({ name: 'Login' })">
        ← العودة إلى شاشة الدخول
      </button>
    </div>
  </div>
</template>

<script>
import { activateDevice } from '@/services/authService'

export default {
  name: 'ActivationScreen',
  data() {
    return {
      activationCode: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async doActivate() {
      this.error   = null
      this.loading = true
      try {
        await activateDevice(this.activationCode)
        localStorage.setItem('device_code', this.activationCode)
        this.$router.push({ name: 'Quiz' })
      } catch (err) {
        this.error = err.response?.data?.detail || 'رمز التفعيل غير صحيح'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
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
