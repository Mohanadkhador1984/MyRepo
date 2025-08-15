<!-- src/views/ActivationPage.vue -->
<template>
  <div class="activation-page">
    <div class="activation-card">
      <h1>مرحبا بك في الاختبار</h1>

      <p class="label">كود جهازك</p>
      <div class="device-code-wrapper">
        <div class="device-code">{{ deviceId }}</div>
        <button class="action-btn copy-btn" @click="copyDeviceId">
          نسخ الكود
        </button>
      </div>

      <button class="action-btn whatsapp-btn" @click="sendWhatsApp">
        إرسال للمطور عبر واتساب
      </button>

      <div v-if="!isActivated" class="actions">
        <button class="btn free-btn" @click="enterFreeVersion">
          دخول مجاني
        </button>

        <input
          v-model="activationCode"
          placeholder="أدخل كود التفعيل"
          class="input-code"
        />
        <button class="btn activate-btn" @click="activate">
          تفعيل النسخة الكاملة
        </button>
        <p v-if="activationError" class="error-text">
          {{ activationError }}
        </p>
      </div>

      <div v-else class="actions">
        <p class="success-text">🎉 تم التفعيل بنجاح</p>
        <button class="btn full-btn" @click="enterFullVersion">
          دخول النسخة الكاملة
        </button>
      </div>

      <button class="dev-btn" @click="$router.push('/dev')">
        صفحة المطور
      </button>
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
      activationError: ''
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
      navigator.clipboard.writeText(this.deviceId)
        .then(() => alert('تم نسخ الكود'))
    },
    sendWhatsApp() {
      const msg = `رقم الجهاز: ${this.deviceId}`
      navigator.clipboard.writeText(this.deviceId)
      const url = `https://wa.me/0988131514?text=${encodeURIComponent(msg)}`
      window.open(url, '_blank')
    },
    enterFreeVersion() {
      this.$router.push({ name: 'QuizPage', query: { activated: false } })
    },
    enterFullVersion() {
      this.$router.push({ name: 'QuizPage', query: { activated: true } })
    },
    activate() {
      const validCode = btoa(this.deviceId).slice(0, 10)
      if (this.activationCode === validCode) {
        this.isActivated = true
        localStorage.setItem('activated', 'true')
        this.activationError = ''
      } else {
        this.activationError = 'كود التفعيل غير صحيح'
      }
    }
  }
}
</script>

<style scoped>
.activation-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-main);
  padding: var(--spacing);
}

.activation-card {
  background: var(--bg-card);
  border: 2px solid var(--primary);
  border-radius: var(--radius-lg);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7);
  max-width: 400px;
  width: 100%;
  padding: 2rem;
  text-align: center;
}

.activation-card h1 {
  color: var(--primary);
  font-size: clamp(1.5rem, 4vw, 2rem);
  margin-bottom: 1rem;
}

.label {
  color: var(--text-light);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.device-code-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.device-code {
  flex: 1;
  font-family: 'Courier New', monospace;
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem;
  border: 2px solid var(--primary);
  border-radius: var(--radius);
  color: var(--text);
  letter-spacing: 0.1rem;
}

.action-btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--transition), transform var(--transition);
  margin-bottom: var(--spacing);
}

.copy-btn {
  max-width: 120px;
  background: var(--accent);
  color: var(--text);
}

.copy-btn:hover {
  background: var(--primary);
  transform: translateY(-2px);
}

.whatsapp-btn {
  background: #25D366;
  color: #fff;
}

.whatsapp-btn:hover {
  background: #1DA851;
  transform: translateY(-2px);
}

.actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing);
  margin-top: var(--spacing);
}

.btn {
  padding: 0.75rem;
  font-size: 1rem;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background var(--transition), transform var(--transition);
}

.free-btn {
  background: var(--secondary);
  color: var(--text);
}

.free-btn:hover {
  background: var(--primary);
  transform: translateY(-2px);
}

.activate-btn {
  background: var(--accent);
  color: var(--text);
}

.activate-btn:hover {
  background: var(--primary);
  transform: translateY(-2px);
}

.full-btn {
  background: var(--primary);
  color: var(--secondary);
}

.full-btn:hover {
  background: var(--accent);
  transform: translateY(-2px);
}

.input-code {
  padding: 0.75rem;
  border: 2px solid var(--primary);
  border-radius: var(--radius);
  background: rgba(255,255,255,0.05);
  color: var(--text);
}

.error-text {
  color: var(--danger);
  font-size: 0.9rem;
}

.success-text {
  color: var(--success);
  font-size: 1rem;
  margin-bottom: var(--spacing);
}

.dev-btn {
  margin-top: var(--spacing);
  font-size: 0.8rem;
  color: var(--text-light);
  text-decoration: underline;
  background: transparent;
  border: none;
  cursor: pointer;
}

.dev-btn:hover {
  color: var(--primary);
}
</style>
