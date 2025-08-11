<template>
  <div class="auth-container">
    <h2>إنشاء حساب</h2>
    <input v-model="username" placeholder="اسم المستخدم" />
    <input v-model="password" type="password" placeholder="كلمة المرور" />
    <button @click="doSignup">إنشاء حساب</button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { signup } from '@/services/authService'

export default {
  name: 'SignupScreen',
  data() {
    return { username: '', password: '', error: null }
  },
  methods: {
    async doSignup() {
      this.error = null
      try {
        await signup(this.username, this.password)
        this.$router.push({ name: 'Login' })
      } catch (err) {
        console.error('Signup error:', err)
        this.error = err.response?.data || 'فشل إنشاء الحساب'
      }
    }
  }
}
</script>

<style scoped>
.auth-container { display: flex; flex-direction: column; gap: 1rem; width: 300px; }
.error { color: red; }
</style>
