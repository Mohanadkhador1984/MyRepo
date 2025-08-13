<template>
  <div class="auth">
    <div class="card">
      <h2>إنشاء حساب</h2>
      <div class="step">خطوة {{ step }} من 3</div>
      <form @submit.prevent="onSubmit">
        <!-- STEP 1 -->
        <div v-if="step===1" class="field">
          <label>رقم الجوال</label>
          <input v-model="phone" type="tel" required placeholder="05XXXXXXXX" />
        </div>
        <!-- STEP 2 -->
        <div v-else-if="step===2" class="field">
          <label>رمز التحقق</label>
          <input v-model="otp" type="text" required placeholder="XXXXXX" />
        </div>
        <!-- STEP 3 -->
        <div v-else class="field">
          <label>الاسم الكامل</label>
          <input v-model="name" type="text" required placeholder="اسمك الكامل" />
          <label>كلمة المرور</label>
          <input v-model="password" type="password" required placeholder="••••••••" />
        </div>
        <button :disabled="loading">
          <span v-if="!loading">
            {{ step<3 ? 'التالي' : 'إنشاء الحساب' }}
          </span>
          <span v-else>
            <i class="spinner"></i> جاري المعالجة...
          </span>
        </button>
      </form>
      <p class="switch">
        لديك حساب؟
        <router-link to="/login">دخول</router-link>
      </p>
    </div>
  </div>
</template>

<script>
const wait = ms => new Promise(r => setTimeout(r, ms))

export default {
  name: 'SignupScreen',
  data: () => ({
    step: 1, loading: false,
    phone: '', otp: '', name: '', password: ''
  }),
  methods: {
    async onSubmit() {
      this.loading = true
      try {
        if (this.step === 1) {
          await Promise.all([
            this.$axios.post('/api/send-otp',{ phone:this.phone }),
            wait(500)
          ])
          this.step = 2
        }
        else if (this.step === 2) {
          await Promise.all([
            this.$axios.post('/api/verify-otp',{ phone:this.phone, otp:this.otp }),
            wait(500)
          ])
          this.step = 3
        }
        else {
          await Promise.all([
            this.$axios.post('/api/signup',{
              phone:this.phone,
              name:this.name,
              password:this.password
            }),
            wait(500)
          ])
          this.$toast.success('تم إنشاء الحساب')
          this.$router.push({ name:'Login' })
        }
      } catch (e) {
        this.$toast.error(e.response?.data?.message || 'خطأ في العملية')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.auth {
  display: flex; justify-content: center; align-items: center;
  min-height: 100vh;
}
.card {
  background: #fff; padding: 2rem; border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1); width: 320px;
}
.step {
  margin-bottom: 1rem; color: #4f46e5; font-weight: bold;
}
.field + .field { margin-top: 1rem }
button {
  width: 100%; padding: .75rem; margin-top: 1.5rem;
  background: #4f46e5; color: #fff; border:none;
  border-radius:4px; font-size:1rem; cursor:pointer;
  transition: background .2s;
}
button:disabled { opacity:.6; cursor:not-allowed }
.spinner {
  border: 2px solid #fff; border-top: 2px solid rgba(255,255,255,0.3);
  border-radius:50%; width:16px; height:16px;
  animation: spin .8s linear infinite;
}
@keyframes spin { to{ transform:rotate(360deg) } }
.switch {
  text-align: center; margin-top:1rem;
}
</style>
