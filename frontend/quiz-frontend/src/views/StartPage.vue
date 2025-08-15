<template>
  <div class="activation-page">
    <div class="main-card">
      <!-- شاشة البداية -->
      <template v-if="currentScreen === 'start'">
        <h1 class="title">🎓 مرحبًا بك في الاختبار</h1>
        <p class="subtitle">يرجى تفعيل حسابك أو تجربة النسخة المجانية</p>
        <div class="button-group">
          <button class="btn activate-btn" @click="currentScreen = 'activation'">🔐 تفعيل الحساب</button>
          <button class="btn free-btn" @click="enterFreeVersion">🎁 تجربة النسخة المجانية</button>
        </div>
      </template>

      <!-- شاشة التفعيل -->
      <template v-else-if="currentScreen === 'activation'">
        <h2 class="title">🔑 تفعيل النسخة الكاملة</h2>
        <p class="subtitle">انسخ الكود وأرسله للمطور</p>

        <div class="section-card">
          <p class="label">رقم الجهاز:</p>
          <div class="device-code">{{ deviceId }}</div>
          <button class="btn copy-btn" @click="copyDeviceId">📋 نسخ الكود</button>
        </div>

        <div class="section-card">
          <p class="label">إرسال الكود للمطور:</p>
          <div class="button-group">
            <button class="btn whatsapp-btn" @click="sendWhatsApp">📱 واتساب</button>
            <button class="btn dev-btn" @click="sendMessenger">💬 ماسنجر</button>
          </div>
        </div>

        <div class="section-card">
          <p class="label">أدخل كود التفعيل:</p>
          <input v-model="activationCode" placeholder="مثال: X1Y2Z3ABC" class="input-code" />
          <button class="btn activate-btn" @click="activate">✅ تفعيل</button>
          <p v-if="activationError" class="error-text">{{ activationError }}</p>
        </div>

        <div class="button-group mt-4">
          <button class="btn dev-btn" @click="currentScreen = 'developer'">🧑‍💻 تواصل مع المطور</button>
          <button class="btn free-btn" @click="currentScreen = 'start'">🔙 العودة</button>
        </div>
      </template>

      <!-- شاشة المطور -->
      <template v-else-if="currentScreen === 'developer'">
        <h2 class="title">🧑‍💻 المطور</h2>
        <p class="subtitle">للحصول على كود التفعيل تواصل معنا:</p>
        <div class="section-card text-right text-sm leading-7">
          <ul>
            <li>📱 واتساب: <a class="text-green-400 underline" href="https://wa.me/0988131514" target="_blank">0988131514</a></li>
            <li>💬 ماسنجر: <a class="text-blue-400 underline" href="https://m.me/devAccount" target="_blank">صفحة المطور</a></li>
            <li>📧 بريد: <span class="text-gray-300">dev@example.com</span></li>
          </ul>
        </div>
        <div class="button-group mt-4">
          <button class="btn activate-btn" @click="currentScreen = 'activation'">🔙 العودة للتفعيل</button>
        </div>
      </template>

      <!-- شاشة النجاح -->
      <template v-else-if="currentScreen === 'success'">
        <h1 class="title">🎉 تم التفعيل بنجاح</h1>
        <p class="success-text">يمكنك الآن استخدام النسخة الكاملة</p>
        <button class="btn free-btn mt-6" @click="enterFreeVersion">🚀 ابدأ الآن</button>
      </template>
    </div>

    <!-- زر المساعدة -->
    <button class="floating-help" @click="showHelp = true">❓</button>

    <!-- نافذة المساعدة -->
    <div v-if="showHelp" class="help-modal" @click.self="showHelp = false">
      <div class="help-box">
        <h2>📘 خطوات التفعيل</h2>
        <ul>
          <li>1️⃣ انسخ رقم الجهاز.</li>
          <li>2️⃣ أرسله للمطور عبر واتساب أو ماسنجر.</li>
          <li>3️⃣ أدخل كود التفعيل عند استلامه.</li>
        </ul>
        <button class="btn close-btn" @click="showHelp = false">إغلاق</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActivationPage',
  data() {
    return {
      deviceId: '',
      activationCode: '',
      isActivated: false,
      activationError: '',
      showHelp: false,
      currentScreen: 'start', // start, activation, developer, success
    }
  },
  mounted() {
    let stored = localStorage.getItem('device_uuid')
    if (!stored) {
      stored = crypto.randomUUID()
      localStorage.setItem('device_uuid', stored)
    }
    this.deviceId = stored
    this.isActivated = localStorage.getItem('activated') === 'true'
    if (this.isActivated) {
      this.currentScreen = 'success'
    }
  },
  methods: {
    copyDeviceId() {
      navigator.clipboard.writeText(this.deviceId).then(() => alert('تم نسخ الكود'))
    },
    sendWhatsApp() {
      const msg = `رقم الجهاز: ${this.deviceId}`
      window.open(`https://wa.me/0988131514?text=${encodeURIComponent(msg)}`, '_blank')
    },
    sendMessenger() {
      const msg = `رقم الجهاز: ${this.deviceId}`
      window.open(`https://m.me/devAccount?text=${encodeURIComponent(msg)}`, '_blank')
    },
    enterFreeVersion() {
      this.$router.push({ name: 'QuizPage', query: { activated: false } })
    },
    activate() {
      const validCode = btoa(this.deviceId).slice(0, 10)
      if (this.activationCode === validCode) {
        this.isActivated = true
        localStorage.setItem('activated', 'true')
        this.activationError = ''
        this.currentScreen = 'success'
      } else {
        this.activationError = '❌ كود التفعيل غير صحيح'
      }
    },
  },
}
</script>

<style scoped>
.activation-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #0f172a, #1e293b);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  font-family: 'Tajawal', sans-serif;
  color: #fff;
  direction: rtl;
}
.main-card {
  background: #1e293b;
  border-radius: 1rem;
  padding: 2rem;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  text-align: center;
}
.title {
  font-size: 1.6rem;
  color: #38bdf8;
  margin-bottom: 0.5rem;
}
.subtitle {
  margin-bottom: 1.5rem;
  color: #cbd5e1;
  font-size: 0.95rem;
}
.section-card {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 0.75rem;
  padding: 1.25rem;
  margin-bottom: 1rem;
}
.label {
  color: #94a3b8;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  text-align: right;
}
.device-code {
  background: #1e293b;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-family: monospace;
  font-size: 1rem;
  word-break: break-all;
  border: 1px dashed #38bdf8;
  color: #f8fafc;
}
.input-code {
  border: none;
  padding: 0.75rem;
  width: 100%;
  border-radius: 0.5rem;
  background: #334155;
  color: #fff;
  margin-top: 0.5rem;
}
.btn {
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: 0.3s;
  width: 100%;
}
.copy-btn {
  background: #38bdf8;
  color: #0f172a;
}
.copy-btn:hover {
  background: #0ea5e9;
}
.activate-btn {
  background: #22c55e;
  color: #fff;
}
.activate-btn:hover {
  background: #16a34a;
}
.free-btn {
  background: #f59e0b;
  color: #0f172a;
}
.free-btn:hover {
  background: #d97706;
}
.whatsapp-btn {
  background: #25d366;
  color: #0f172a;
}
.whatsapp-btn:hover {
  background: #1da851;
}
.dev-btn {
  background: #3b82f6;
  color: white;
}
.dev-btn:hover {
  background: #2563eb;
}
.button-group {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.error-text {
  color: #f87171;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}
.success-text {
  color: #4ade80;
  font-weight: bold;
  margin-top: 1rem;
}
.floating-help {
  position: fixed;
  bottom: 1.5rem;
  left: 1.5rem;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #0ea5e9;
  color: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  z-index: 1000;
}
.help-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
.help-box {
  background: #1e293b;
  padding: 2rem;
  border-radius: 1rem;
  max-width: 350px;
  width: 90%;
  text-align: right;
  color: #fff;
}
.help-box h2 {
  margin-bottom: 1rem;
  color: #38bdf8;
}
.help-box ul {
  list-style: none;
  padding: 0;
}
.help-box li {
  margin-bottom: 0.75rem;
  font-size: 1rem;
}
.close-btn {
  background: #ef4444;
  margin-top: 1rem;
  color: white;
}
</style>