<template>
  <div class="activation-page">
    <div class="main-card">
      <h1 class="title">🎓 مرحبًا بك في الاختبار</h1>
      <p class="subtitle">فضلاً قم بتفعيل حسابك أو جرّب النسخة المجانية</p>

      <!-- بطاقة فرعية -->
      <div class="sub-card">
        <p class="label">رقم الجهاز:</p>
        <div class="device-code">{{ deviceId }}</div>
        <button class="btn small-btn copy-btn" @click="copyDeviceId">📋 نسخ الكود</button>

        <div v-if="!isActivated" class="activation-area">
          <input v-model="activationCode" placeholder="أدخل كود التفعيل" class="input-code" />
          <button class="btn activate-btn" @click="activate">✅ تفعيل النسخة</button>
          <p v-if="activationError" class="error-text">{{ activationError }}</p>
        </div>
        <div v-else class="success-text">
          🎉 تم تفعيل النسخة الكاملة بنجاح
        </div>
      </div>

      <!-- أزرار عامة -->
      <div class="button-group">
        <button class="btn free-btn" @click="enterFreeVersion">🎁 دخول النسخة المجانية</button>
        <button class="btn whatsapp-btn" @click="sendWhatsApp">📱 إرسال للمطور عبر واتساب</button>
        <button class="btn dev-btn" @click="$router.push('/dev')">🧑‍💻 صفحة المطور</button>
      </div>
    </div>

    <!-- زر عائم للمساعدة -->
    <button class="floating-help" @click="showHelp = true">❓</button>

    <!-- نافذة المساعدة -->
    <div v-if="showHelp" class="help-modal" @click.self="showHelp = false">
      <div class="help-box">
        <h2>📘 كيفية التفعيل</h2>
        <ul>
          <li>📋 انسخ رقم الجهاز من الشاشة.</li>
          <li>📲 أرسله للمطور عبر واتساب.</li>
          <li>🔐 ستحصل على كود تفعيل خاص بك.</li>
          <li>✅ أدخل الكود واضغط "تفعيل النسخة".</li>
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
      showHelp: false
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
  },
  methods: {
    copyDeviceId() {
      navigator.clipboard.writeText(this.deviceId).then(() => alert('تم نسخ الكود'))
    },
    sendWhatsApp() {
      const msg = `رقم الجهاز: ${this.deviceId}`
      const url = `https://wa.me/0988131514?text=${encodeURIComponent(msg)}`
      window.open(url, '_blank')
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
      } else {
        this.activationError = '❌ كود التفعيل غير صحيح'
      }
    }
  }
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
  position: relative;
  font-family: 'Tajawal', sans-serif;
  color: #fff;
  direction: rtl;
}

.main-card {
  background: #1e293b;
  border-radius: 1rem;
  padding: 2rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
  text-align: center;
}

.title {
  font-size: 1.8rem;
  color: #38bdf8;
}

.subtitle {
  margin-bottom: 1.5rem;
  color: #cbd5e1;
}

.sub-card {
  background: #0f172a;
  border: 2px solid #38bdf8;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.label {
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.device-code {
  background: #1e293b;
  padding: 1rem;
  border-radius: 0.75rem;
  font-family: monospace;
  font-size: 1.1rem;
  word-break: break-all;
  margin-bottom: 0.5rem;
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
  margin-bottom: 1rem;
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

.small-btn {
  font-size: 0.9rem;
  margin-bottom: 1rem;
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
  background: #475569;
  color: #f1f5f9;
}

.dev-btn:hover {
  background: #334155;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activation-area {
  margin-top: 1rem;
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
  background: rgba(0, 0, 0, 0.8);
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