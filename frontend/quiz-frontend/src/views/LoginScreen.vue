<template>
  <div class="login-page">
    <div class="login-card">
      <h2>👋 مرحباً بعودتك</h2>

      <form ref="loginForm" @submit.prevent="doLogin">
        <!-- رقم الجوال -->
        <div class="form-group">
          <input
            id="phone"
            v-model="phone"
            type="tel"
            placeholder=" "
            autocomplete="tel"
            required
          />
          <label for="phone">📱 05XXXXXXXX</label>
        </div>

        <!-- كلمة المرور -->
        <div class="form-group password-wrapper">
          <input
            :type="showPassword ? 'text' : 'password'"
            id="password"
            v-model="password"
            placeholder=" "
            autocomplete="current-password"
            required
          />
          <label for="password">🔒 كلمة السر</label>
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
          <input id="remember" v-model="rememberMe" type="checkbox" />
          <label for="remember">💡 تذكرني</label>
        </div>

        <!-- زر الدخول -->
        <button type="submit" :disabled="loading">
          <span v-if="!loading">🚪 دخول</span>
          <span v-else><i class="spinner"></i> جاري المعالجة...</span>
        </button>

        <p v-if="error" class="error">⚠️ {{ error }}</p>
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
      } catch {
        // المستخدم رفض أو Credential API غير مدعوم
      }
    }

    // 2) LocalStorage احتياطي
    if (!this.phone && localStorage.remember_phone) {
      this.phone = localStorage.remember_phone
      this.password = localStorage.remember_pass
      this.rememberMe = true
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword
    },
    async doLogin() {
      this.error = null
      this.loading = true
      try {
        const resp = await login(this.phone, this.password)
        const data = resp.data ?? resp
        const token = data.access || data.access_token || data.token
        if (!token) throw new Error('استجابة غير متوقعة من السيرفر')
        localStorage.setItem('access_token', token)

        // Credential Management API
        if (navigator.credentials?.store && this.rememberMe) {
          try {
            const cred = await navigator.credentials.create({
              password: {
                id: this.phone,
                password: this.password,
                name: 'MyApp'
              }
            })
            await navigator.credentials.store(cred)
          } catch {
            // فشل تخزين凭据
          }
        }

        // Local storage احتياطي
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
  min-height: 100vh;
  background-color: #0f0f0f;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', sans-serif;
  padding: 1rem;
}

.login-card {
  background: #1a1a1a;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  width: 100%;
  color: #ffd700;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
  text-align: center;
}

.login-card h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #ffd700;
}

.form-group {
  position: relative;
  margin: 1.5rem 0;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid #555;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #ffd700;
}

.form-group label {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  transform: translateY(-50%);
  color: #aaa;
  transition: 0.3s ease;
  pointer-events: none;
}

.form-group input:focus + label,
.form-group input:not(:placeholder-shown) + label {
  transform: translateY(-160%) scale(0.85);
  font-size: 0.85rem;
  color: #ffd700;
}

.password-wrapper .toggle-visibility {
  position: absolute;
  top: 50%;
  right: 0.75rem;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #ffd700;
  cursor: pointer;
}

.form-remember {
  display: flex;
  align-items: center;
  justify-content: start;
  margin: 1rem 0;
  font-size: 0.9rem;
  color: #ccc;
}

.form-remember input {
  margin-right: 0.5rem;
}

button[type='submit'] {
  width: 100%;
  padding: 0.75rem;
  background: #ffd700;
  color: #0f0f0f;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

button[type='submit']:hover:not(:disabled) {
  background: #e6c200;
}

button[type='submit']:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #0f0f0f;
  border-top: 2px solid rgba(0, 0, 0, 0.4);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error {
  color: #f87171;
  margin-top: 1rem;
  font-size: 0.95rem;
}
</style>