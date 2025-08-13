<!-- src/views/LoginScreen.vue -->
<template>
  <div class="login-page">
    <div class="login-card">
      <h2>مرحباً بعودتك</h2>

      <form ref="loginForm" @submit.prevent="doLogin">
        <!-- رقم الجوال مع Floating Label -->
        <div class="form-group">
          <input
            id="phone"
            v-model="phone"
            type="tel"
            placeholder=" "
            autocomplete="tel"
            required
          />
          <label for="phone">05XXXXXXXX</label>
        </div>

        <!-- كلمة المرور مع Floating Label + أيقونة الإظهار -->
        <div class="form-group password-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            id="password"
            v-model="password"
            placeholder=" "
            autocomplete="current-password"
            required
          />
          <label for="password">كلمة السر</label>
          <button
            type="button"
            class="toggle-visibility"
            @click="togglePassword"
            :aria-label="showPassword ? 'إخفاء كلمة السر' : 'إظهار كلمة السر'"
          >
            {{ showPassword ? '🙈' : '👁️' }}
          </button>
        </div>

        <!-- تذكرني -->
        <div class="form-remember">
          <input
            id="remember"
            v-model="rememberMe"
            type="checkbox"
          />
          <label for="remember">تذكرني</label>
        </div>

        <!-- زر الدخول مع Spinner -->
        <button type="submit" :disabled="loading">
          <span v-if="!loading">دخول</span>
          <span v-else><i class="spinner"></i> جاري المعالجة...</span>
        </button>

        <!-- رسالة الخطأ -->
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
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
      rememberMe: false,
      showPassword: false,
      loading: false,
      error: null
    }
  },
  async mounted() {
    // 1) Credential Management API
    if (navigator.credentials?.get) {
      try {
        const cred = await navigator.credentials.get({ password: true })
        if (cred) {
          this.phone = cred.id || ''
          this.password = cred.password || ''
          this.rememberMe = true
        }
      } catch { /* رفض المستخدم أو غير مدعوم */ }
    }

    // 2) LocalStorage احتياطي
    if (!this.phone && localStorage.remember_phone) {
      this.phone      = localStorage.remember_phone
      this.password   = localStorage.remember_pass
      this.rememberMe = true
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    async doLogin() {
      this.error   = null
      this.loading = true

      try {
        const resp  = await login(this.phone, this.password)
        const data  = resp.data ?? resp
        const token = data.access || data.access_token || data.token

        if (!token) {
          throw new Error('استجابة غير متوقعة من السيرفر')
        }

        localStorage.setItem('access_token', token)

        // تذكير Credential Management API
        if (navigator.credentials?.store && this.rememberMe) {
          try {
            const cred = await navigator.credentials.create({
              password: { id: this.phone, password: this.password, name: 'MyApp' }
            })
            await navigator.credentials.store(cred)
          } catch { /* فشل تخزين */ }
        }

        // تخزين احتياطي
        if (this.rememberMe) {
          localStorage.setItem('remember_phone', this.phone)
          localStorage.setItem('remember_pass', this.password)
        } else {
          localStorage.removeItem('remember_phone')
          localStorage.removeItem('remember_pass')
        }

        this.$router.push({ name: 'Quiz' })
      } catch (err) {
        this.error =
          err.response?.data?.detail ||
          err.response?.data?.message ||
          err.message ||
          'فشل تسجيل الدخول'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  max-width: 360px;
  margin: 2rem auto;
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 8px;
  text-align: center;
  font-family: 'Inter', sans-serif;
  background: #fff;
}

.login-card h2 {
  margin-bottom: 1.5rem;
  color: #4f46e5;
  font-size: 1.5rem;
}

.form-group {
  position: relative;
  margin: 1rem 0;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-bottom: 2px solid #ccc;
  background: transparent;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #4f46e5;
}

.form-group label {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  transform: translateY(-50%);
  color: #9ca3af;
  pointer-events: none;
  transition: transform 0.2s, font-size 0.2s;
}

.form-group input:focus + label,
.form-group input:not(:placeholder-shown) + label {
  transform: translateY(-150%) scale(0.85);
  font-size: 0.85rem;
  color: #4f46e5;
}

.password-wrapper .toggle-visibility {
  position: absolute;
  top: 50%;
  right: 0.75rem;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.1rem;
  cursor: pointer;
}

.form-remember {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1rem 0;
}

.form-remember input {
  margin-right: 0.5rem;
}

button[type="submit"] {
  width: 100%;
  padding: 0.75rem;
  background: #4f46e5;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

button[type="submit"]:hover:not(:disabled) {
  background: #4338ca;
}

button[type="submit"]:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #fff;
  border-top: 2px solid rgba(255,255,255,0.4);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  color: #dc2626;
  margin-top: 1rem;
  font-size: 0.95rem;
}
</style>
