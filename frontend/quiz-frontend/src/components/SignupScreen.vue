<template>
  <div class="signup-screen">
    <h2>إنشاء حساب جديد</h2>
    <input v-model="phone" placeholder="رقم الهاتف" type="tel"/>
    <input v-model="password" placeholder="كلمة السر" type="password"/>
    <button @click="doSignup" :disabled="loading">
      {{ loading ? 'جاري الإنشاء…' : 'إنشاء حساب' }}
    </button>
    <p v-if="error" class="error">{{ error }}</p>
    <p>لديك حساب؟ <router-link to="/">الدخول</router-link></p>
  </div>
</template>

<script>
import { ref } from 'vue'
import { register } from '@/services/authService'

export default {
  name: 'SignupScreen',
  setup(_, { router }) {
    const phone = ref('')
    const password = ref('')
    const loading = ref(false)
    const error = ref('')

    async function doSignup() {
      error.value = ''
      loading.value = true
      try {
        await register(phone.value, password.value)
        router.push({ name:'Start' })
      } catch (e) {
        error.value = e.response?.data?.detail || 'فشل إنشاء الحساب'
      } finally {
        loading.value = false
      }
    }

    return { phone, password, loading, error, doSignup }
  }
}
</script>

<style scoped>
.signup-screen { max-width:400px; margin:2rem auto; text-align:center }
input, button { width:100%; padding:0.5rem; margin-bottom:0.5rem; }
.error { color:red; }
</style>
