<template>
  <div class="activation-page">
    <div class="card">

      <!-- اسم التطبيق -->
      <div class="app-header">بكالوريا إنجليزي</div>

      <!-- شاشة البداية -->
      <div v-if="currentScreen === 'start'" class="screen screen-start">
        <h1 class="title">🎓 أهلاً بك في الاختبار</h1>
        <p class="subtitle">يرجى تفعيل حسابك أو تجربة النسخة المجانية</p>
        <div class="button-group two-col">
          <button class="btn activate-btn" @click="currentScreen = 'activation'">
            🔐 تفعيل الحساب
          </button>
          <button class="btn free-btn" @click="enterFreeVersion">
            {{ freeBtnText }}
          </button>
        </div>
      </div>

      <!-- شاشة التفعيل -->
      <div v-else-if="currentScreen === 'activation'" class="screen screen-activation">
        <h2 class="title">🔑 تفعيل النسخة الكاملة</h2>
        <p class="subtitle">
          انسخ رقم جهازك وأرسله للمطور، ثم أدخل كود التفعيل
        </p>

        <!-- رقم الجهاز مع Tooltip -->
        <div class="section tooltip-wrapper">
          <label class="label">رقم الجهاز</label>
          <div class="device-code">{{ deviceId }}</div>
          <button
      :class="['btn copy-btn', { copied }]"
      @click="copyDeviceId"
    >
      {{ copied ? '✅ تم النسخ وجاهز للإرسال' : '📋 نسخ الرقم' }}
    </button>
          <div class="tooltip">
            انقر هنا لنسخ الرقم التسلسلي تلقائيًا ويصبح جاهزًا للإرسال
          </div>
        </div>

        <!-- أزرار التواصل -->
        <div class="section">
          <label class="label">أرسل للمطور عبر:</label>
          <div class="social-group">
            <button class="btn social whatsapp-btn" @click="sendWhatsApp">
              <i class="fab fa-whatsapp"></i>
            </button>
            <button class="btn social messenger-btn" @click="sendMessenger">
              <i class="fab fa-facebook-messenger"></i>
            </button>
          </div>
        </div>

        <!-- حقل كود التفعيل -->
        <div class="section activation-frame">
          <label class="label">كود التفعيل</label>
          <div class="activation-panel">
            <input
              v-model="activationCode"
              type="text"
              placeholder="أدخل الكود هنا"
              class="activation-input"
              autofocus
            />
            <button
              class="btn activation-btn"
              :class="{ success: activationSuccess }"
              @click="activate"
            >
              <i class="fas fa-key"></i>
              تفعيل
            </button>
          </div>
          <p v-if="activationError" class="error-text">{{ activationError }}</p>
        </div>

        <!-- زر العودة -->
        <div class="button-group one-col">
          <button class="btn return-btn" @click="currentScreen = 'start'">
            🔙 العودة
          </button>
        </div>
      </div>

      <!-- شاشة النجاح -->
      <div v-else-if="currentScreen === 'success'" class="screen screen-success">
        <h1 class="title">🎉 تم التفعيل بنجاح</h1>
        <p class="subtitle">يمكنك الآن استخدام جميع الميزات الكاملة!</p>
        <button class="btn free-btn" @click="enterFreeVersion">
          🚀 تجربة النسخة الكاملة
        </button>
      </div>

    </div>

    <!-- زر المساعدة العائم -->
    <button class="floating-help" @click="showHelp = true">
      ❓
    </button>

    <!-- نافذة المساعدة -->
    <div v-if="showHelp" class="help-modal" @click.self="showHelp = false">
      <div class="help-box">
        <h2>📘 خطوات التفعيل</h2>
        <ul>
          <li>1️⃣ انسخ رقم جهازك.</li>
          <li>2️⃣ أرسله للمطور عبر واتساب أو ماسنجر.</li>
          <li>3️⃣ أدخل كود التفعيل هنا واضغط “تفعيل”.</li>
        </ul>
        <button class="btn close-btn" @click="showHelp = false">
          إغلاق
        </button>
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
      activationError: '',
      activationSuccess: false,
      showHelp: false,
      copied: false,
      currentScreen: 'start'
    }
  },
  computed: {
    freeBtnText() {
      return this.activationSuccess
        ? '🎁 تجربة النسخة الكاملة'
        : '🎁 النسخة المجانية'
    }
  },
  mounted() {
    let id = localStorage.getItem('device_uuid')
    if (!id) {
      id = crypto.randomUUID()
      localStorage.setItem('device_uuid', id)
    }
    this.deviceId = id

    if (localStorage.getItem('activated') === 'true') {
      this.activationSuccess = true
      this.currentScreen = 'success'
    }
  },
  methods: {
    copyDeviceId() {
      navigator.clipboard.writeText(this.deviceId).then(() => {
        this.copied = true
        // إعادة الزر إلى حالته الأصلية بعد 3 ثواني
        setTimeout(() => {
          this.copied = false
        }, 3000)
      })
    },
    sendWhatsApp() {
      const msg = `🔑 رقم الجهاز: ${this.deviceId}`
      window.open(
        `https://wa.me/0953447860?text=${encodeURIComponent(msg)}`,
        '_blank'
      )
    },
    sendMessenger() {
      const msg = `🔑 رقم الجهاز: ${this.deviceId}`
      window.open(
        `https://m.me/devAccount?text=${encodeURIComponent(msg)}`,
        '_blank'
      )
    },
    activate() {
      const valid = btoa(this.deviceId).slice(0, 10)
      if (this.activationCode === valid) {
        localStorage.setItem('activated', 'true')
        this.activationSuccess = true
        this.currentScreen = 'success'
      } else {
        this.activationError = '❌ كود التفعيل غير صحيح'
      }
    },
    enterFreeVersion() {
      this.$router.push({
        name: 'QuizPage',
        query: { activated: this.activationSuccess }
      })
    }
  }
}
</script>

<style scoped>
/* ===== أساسي ===== */
.activation-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(160deg, #0f172a, #1e293b);
  padding: 1rem;
  font-family: 'Tajawal', sans-serif;
  color: #fff;
}

/* ===== البطاقة ===== */
.card {
  width: 100%;
  max-width: 450px;
  padding: 2rem 1.5rem;
  background: rgba(30, 41, 59, 0.9);
  border-radius: 1rem;
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(6px);
  text-align: center;
  animation: popIn 0.6s ease-out both;
}
@keyframes popIn {
  from { opacity: 0; transform: scale(0.9); }
  to   { opacity: 1; transform: scale(1); }
}

/* ===== اسم التطبيق ===== */
.app-header {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #facc15;
}

/* ===== العناوين ===== */
.title {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: #38bdf8;
}
.subtitle {
  font-size: 1rem;
  margin-bottom: 1.5rem;
  color: #cbd5e1;
}

/* ===== button groups ===== */
.button-group {
  display: grid;
  gap: 0.75rem;
}
.two-col { grid-template-columns: repeat(2, 1fr); }
.one-col { grid-template-columns: 1fr; }

/* ===== buttons ===== */
.btn {
  padding: 0.75rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn:hover { transform: translateY(-3px); }

/* تفعيل الحساب */
.activate-btn {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: #fff;
  box-shadow: 0 6px 16px rgba(34,197,94,0.4);
}

/* free / full */
.free-btn {
  background: linear-gradient(135deg, #facc15, #eab308);
  color: #1e293b;
  box-shadow: 0 6px 16px rgba(234,179,8,0.4);
}

/* العودة */
.return-btn {
  background: linear-gradient(135deg, #7c3aed, #9333ea);
  color: #fff;
  box-shadow: 0 6px 16px rgba(124,58,237,0.4);
}

/* ===== Device Code ===== */
.section { text-align: right; margin-bottom: 1.5rem; }
.label { font-size: 0.95rem; color: #94a3b8; margin-bottom: 0.5rem; }
.device-code {
  padding: 0.75rem;
  background: #273141;
  border: 1px dashed #38bdf8;
  border-radius: 0.5rem;
  font-family: monospace;
  overflow-x: auto;
  position: relative;
}
.device-code::before {
  content: '';
  position: absolute; top:0; left:-100%;
  width:100%; height:100%;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.15), transparent);
  animation: shine 2s infinite;
}
@keyframes shine {
  0% { left: -100%; } 50% { left: 100%; } 100% { left:100%; }
}

/* ===== Tooltip ===== */
.tooltip-wrapper { position: relative; }


.copy-btn {
  width: 100%;
  margin-top: 0.75rem;
  background: linear-gradient(135deg, #facc15, #eab308);
  color: #1e293b;
  box-shadow: 0 6px 16px rgba(234,179,8,0.4);
  transition: background 0.3s, transform 0.2s, box-shadow 0.2s;
}

/* تأثير Hover عادي */
.copy-btn:hover {
  transform: translateY(-3px);
}

/* الزر بعد النسخ */
.copy-btn.copied {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: #fff;
  box-shadow: 0 6px 16px rgba(34,197,94,0.4);
}


.tooltip {
  position: absolute;
  bottom: 140%;
  left: 50%;
  transform: translateX(-50%);
  background: #ffc107;
  color: #1e1e1e;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s;
}
.tooltip::before {
  content: '';
  position: absolute;
  top: 100%; left: 50%;
  transform: translateX(-50%);
  border-width: 6px; border-style: solid;
  border-color: #ffc107 transparent transparent transparent;
}
.tooltip-wrapper:hover .tooltip {
  opacity: 1;
  visibility: visible;
}

/* ===== Social Buttons ===== */
.social-group {
  display: flex; justify-content: center; gap: 1rem;
}
.btn.social {
  width: 50px; height: 50px;
  border-radius: 50%;
  font-size: 1.4rem;
  display: grid; place-items: center;
  transition: transform 0.3s;
}
.whatsapp-btn {
  background: radial-gradient(circle at 30%30%, #25d366, #128c7e);
  box-shadow: 0 6px 16px rgba(37,211,102,0.4);
}
.messenger-btn {
  background: radial-gradient(circle at 30%30%, #0084ff, #0063d1);
  box-shadow: 0 6px 16px rgba(0,132,255,0.4);
}
.btn.social:hover {
  transform: translateY(-4px) scale(1.1);
}

/* ===== Activation Input ===== */
.activation-frame {
  border: 2px solid #38bdf8;
  border-radius: 0.75rem;
  padding: 1rem;
  animation: pulseBorder 3s infinite;
}
@keyframes pulseBorder {
  0%,100% { border-color: #38bdf8; }
  50%     { border-color: #a78bfa; }
}
.activation-panel { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.activation-input {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #38bdf8;
  border-radius: 0.5rem;
  background: transparent;
  color: #fff;
  font-size: 1rem;
  caret-color: #ffeb3b;
  /* animation: blinkCaret 1s steps(1) infinite; */
}
@keyframes blinkCaret {
  0%,50% { opacity: 1; }
  51%,100% { opacity: 0; }
}

/* ===== Floating Help ===== */
.floating-help {
  position: fixed; bottom:1.5rem; right:1.5rem;
  width:3rem; height:3rem;
  background:#38bdf8; color:#fff;
  border:none; border-radius:50%;
  font-size:1.5rem; cursor:pointer;
  box-shadow:0 4px 12px rgba(0,0,0,0.3);
  transition:transform 0.3s; z-index:10;
}
.floating-help:hover { transform:scale(1.2); }

/* ===== Help Modal ===== */
.help-modal {
  position:fixed; inset:0;
  background:rgba(0,0,0,0.7);
  display:flex; align-items:center; justify-content:center;
  z-index:20;
}
.help-box {
  background:rgba(30,41,59,0.95);
  padding:1.5rem; border-radius:1rem;
  max-width:350px; width:90%;
  text-align:right; animation:popIn 0.4s both;
}
.close-btn {
  margin-top:1rem; background:#ef4444; color:#fff;
}

/* ===== Mobile ===== */
@media (max-width: 480px) {
  .card { padding:1.5rem 1rem; margin:0 0.5rem; }
  .app-header { font-size:1.2rem; }
  .title { font-size:1.6rem; }
  .subtitle { font-size:0.9rem; }
  .two-col { grid-template-columns: 1fr; }
  .activation-panel { flex-direction: column; }
  .activation-input { animation: none; }
  .btn, .return-btn, .copy-btn { font-size:0.95rem; padding:0.65rem; }
  .btn.social { width:45px; height:45px; font-size:1.2rem; }
  .floating-help { width:2.5rem; height:2.5rem; font-size:1.25rem; }
}
</style>



<style scoped>
/* === Toast Styles === */
.toast {
  position: fixed;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.95);
  color: #1e293b;
  padding: 1rem 1.5rem;
  border-radius: 0.75rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  font-size: 0.95rem;
  text-align: center;
  line-height: 1.4;
  z-index: 100;
  pointer-events: none;
}

/* حركة الظهور والاختفاء */
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.4s, transform 0.4s;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}
.toast-fade-enter-to,
.toast-fade-leave-from {
  opacity: 1;
  transform: translate(-50%, 0);
}

/* === Responsive Adjustments === */
@media (max-width: 480px) {
  .toast {
    bottom: 1rem;
    padding: 0.75rem 1rem;
    font-size: 0.85rem;
  }
}
</style>