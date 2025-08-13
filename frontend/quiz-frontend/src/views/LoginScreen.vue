<!-- src/views/LoginScreen.vue -->
<template>
  <div class="login-screen">
    <h1>تسجيل الدخول</h1>
    <form @submit.prevent="doLogin">
      <input v-model="phone" type="text" placeholder="رقم الهاتف" required />
      <input v-model="password" type="password" placeholder="كلمة السر" required />
      <button type="submit">دخول</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { login } from '@/services/authService'

export default {
  name: 'LoginScreen',
  data() {
    return {
      phone: '',
      password: '',
      error: null
    }
  },
  methods: {
    async doLogin() {
      this.error = null
      try {
        // نحصل على access ونستخدمه مباشرة
        const { access } = await login(this.phone, this.password)
        if (access) {
          this.$router.push({ name: 'Quiz' })
        }
      } catch (err) {
        console.error('Login error:', err)
        this.error = err.response?.data?.detail || 'فشل تسجيل الدخول'
      }
    }
  }
}
</script>

<style scoped>
.error {
  color: red;
  margin-top: 1rem;
}
</style>
