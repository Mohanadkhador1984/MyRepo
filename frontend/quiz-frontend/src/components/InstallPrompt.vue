<!-- src/components/InstallCTA.vue -->
<template>
  <div v-if="!installed" class="install-wrapper" @click.self="hideManual">

    <!-- 1. زر التثبيت الفاخر -->
    <button
      v-if="canPrompt"
      class="install-btn"
      :disabled="installing"
      @click.stop="onInstallClick"
    >
      <span v-if="!installing">📥 تثبيت التطبيق</span>
      <span v-else class="spinner"></span>
    </button>

    <!-- 2. أيقونة التنويه للمتصفحات غير المدعومة -->
    <button
      v-else-if="!installing"
      class="fallback-btn"
      @click.stop="showManual = true"
      title="أضف للتطبيق / Add to Home Screen"
    >
      <i class="fas fa-bell"></i>
    </button>

    <!-- 3. نافذة الشرح التفصيلي (بالونوسيوني ـ Balloon) -->
    <transition name="fade-scale">
      <div
        v-if="showManual"
        class="manual-popup"
        @click.stop
      >
        <button class="close-btn" @click="hideManual">
          <i class="fas fa-times"></i>
        </button>
        <h3 class="popup-title">كيفية تثبيت التطبيق</h3>
        <p class="popup-text">
          لتثبيت التطبيق:
          <br />
          اضغط زر القائمة (⋮) في متصفحك
          <br />
          ثم اختر <strong>إضافة إلى الشاشة الرئيسية</strong>
        </p>
        <p class="popup-text en">
          To install the app:
          <br />
          Press the menu button (⋮) in your browser
          <br />
          then select <strong>Add to Home Screen</strong>
        </p>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const deferredPrompt = ref(null)
const canPrompt      = ref(false)
const installing     = ref(false)
const installed      = ref(false)
const showManual     = ref(false)

function detectInstalled() {
  if (
    window.matchMedia('(display-mode: standalone)').matches ||
    window.navigator.standalone === true
  ) {
    installed.value = true
  }
}

function onInstallClick() {
  if (!deferredPrompt.value) return
  installing.value = true
  deferredPrompt.value.prompt()
  deferredPrompt.value.userChoice.then(({ outcome }) => {
    installing.value = false
    if (outcome === 'accepted') installed.value = true
    deferredPrompt.value = null
  })
}

function onAppInstalled() {
  installed.value = true
}

function hideManual() {
  showManual.value = false
}

onMounted(() => {
  detectInstalled()
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault()
    deferredPrompt.value = e
    canPrompt.value      = true
  })
  window.addEventListener('appinstalled', onAppInstalled)

  // بعد 800ms، إن لم يظهر beforeinstallprompt
  setTimeout(() => {
    if (!canPrompt.value && !installed.value) {
      showManual.value = false
      canPrompt.value  = false
    }
  }, 800)
})

onBeforeUnmount(() => {
  window.removeEventListener('appinstalled', onAppInstalled)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* كامل الشاشة لالتقاط النقرات */
.install-wrapper {
  position: fixed;
  inset: 0;
  z-index: 10000;
  pointer-events: auto;
  display: flex;
  align-items: flex-end; /* زر في الأسفل */
  padding: 2cm;         /* يرفع 2 سم من الأسفل ولليسار */
}

/* زر التثبيت */
.install-btn {
  background: linear-gradient(135deg, #4e54c8, #8f94fb);
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 0.8rem 1.8rem;
  font-size: 1rem;
  font-weight: 600;
  box-shadow: 0 6px 18px rgba(0,0,0,0.2);
  cursor: pointer;
  animation: pulse 1.8s ease-in-out infinite;
  transition: transform 0.2s, box-shadow 0.2s;
}
.install-btn:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 10px 28px rgba(0,0,0,0.3);
}
.install-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}
.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* زر التنويه */
.fallback-btn {
  background: rgba(255,255,255,0.9);
  border: 2px solid #4e54c8;
  color: #4e54c8;
  border-radius: 50%;
  padding: 0.5rem;
  font-size: 1.6rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  animation: pulse 2s ease-in-out infinite;
}
.fallback-btn:hover {
  transform: scale(1.1);
}

/* Balloony glass popup في وسط الشاشة */
.manual-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(8px);
  border-radius: 24px;
  padding: 1.5rem;
  box-shadow: 0 12px 32px rgba(0,0,0,0.2);
  color: #333;
  text-align: center;
  pointer-events: auto;
}
/* ذيل البالون */
.manual-popup::after {
  content: '';
  position: absolute;
  bottom: -16px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 8px;
  border-style: solid;
  border-color: rgba(255,255,255,0.9) transparent transparent transparent;
}

/* Close button */
.close-btn {
  position: absolute;
  top: 0.8rem;
  right: 0.8rem;
  background: transparent;
  border: none;
  color: #666;
  font-size: 1rem;
  cursor: pointer;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #000;
}

/* Popup content */
.popup-title {
  margin: 0 0 0.8rem;
  font-size: 1.1rem;
  font-weight: 600;
}
.popup-text {
  margin: 0.4rem 0;
  font-size: 0.95rem;
  line-height: 1.4;
}
.popup-text.en {
  margin-top: 1rem;
  color: #555;
}

/* Animations */
@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes pulse {
  0%,100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Fade & scale transition */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-scale-enter-from {
  opacity: 0; transform: scale(0.9);
}
.fade-scale-leave-to {
  opacity: 0; transform: scale(0.9);
}
</style>
