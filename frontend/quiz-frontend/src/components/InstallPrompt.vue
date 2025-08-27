<!-- src/components/InstallCTA.vue -->
<template>
  <div v-if="!installed" class="install-wrapper" @click.self="hideManual">

    <!-- 1. زر التثبيت الفخم -->
    <button
      v-if="canPrompt"
      class="install-btn"
      :disabled="installing"
      @click="onInstallClick"
    >
      <span v-if="!installing">📥 تثبيت التطبيق</span>
      <span v-else class="spinner"></span>
    </button>

    <!-- 2. زر التنويه للمتصفحات القديمة -->
    <button
      v-else-if="!installing"
      class="fallback-btn"
      @click="showManual = true"
      title="أضف للتطبيق / Add to Home Screen"
    >
      <i class="fas fa-bell"></i>
    </button>

    <!-- 3. النافذة المنبثقة الشفافة الفاخرة -->
    <transition name="fade">
      <div v-if="showManual" class="manual-popup">
        <button class="close-btn" @click="showManual = false">
          <i class="fas fa-times"></i>
        </button>
        <h3 class="popup-title">كيفية إضافة التطبيق</h3>
        <p class="popup-text">
          اضغط على ⋮ في شريط المتصفح ثم اختر
          <strong>"Add to Home Screen"</strong>
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
  if (window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true) {
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

  // إذا لم نرَ قبل 800ms، نظهر الfallback-icon
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

.install-wrapper {
  position: fixed;
  left: 2cm;
  bottom: 2cm;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* زر التثبيت الفاخر */
.install-btn {
  background: linear-gradient(135deg, #f1c40f, #e67e22);
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 0.8rem 1.8rem;
  font-size: 1rem;
  font-weight: 600;
  box-shadow: 0 6px 18px rgba(0,0,0,0.25);
  cursor: pointer;
  animation: pulse 1.8s ease-in-out infinite;
  transition: transform 0.2s, box-shadow 0.2s;
}
.install-btn:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 10px 28px rgba(0,0,0,0.3);
}
.install-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}
/* دوار التحميل */
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
  background: #fff;
  border: 2px solid #f1c40f;
  color: #f1c40f;
  border-radius: 50%;
  padding: 0.5rem;
  font-size: 1.6rem;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  animation: pulse 2s ease-in-out infinite;
  transition: transform 0.2s;
}
.fallback-btn:hover {
  transform: scale(1.1);
}

/* النافذة المنبثقة */
.manual-popup {
  position: absolute;
  left: 2cm;
  bottom: 5.5cm;
  width: 260px;
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  padding: 1rem 1.2rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.25);
  color: #fff;
  overflow: hidden;
}
/* إطار ذهبي */
.manual-popup::before {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  background: linear-gradient(135deg, #f1c40f, #e67e22);
  z-index: -1;
  filter: blur(6px);
  animation: glow 3s ease-in-out infinite alternate;
}

/* زر الإغلاق */
.close-btn {
  position: absolute;
  top: 0.6rem;
  left: 0.6rem;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 1.1rem;
  cursor: pointer;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #e67e22;
}

/* العنوان والنص */
.popup-title {
  margin: 0 0 0.6rem;
  font-size: 1rem;
  font-weight: 600;
}
.popup-text {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

/* أنيميشنات */
@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes pulse {
  0%,100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}
@keyframes glow {
  from { opacity: 0.6; }
  to { opacity: 1; }
}

/* انتقال fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-enter-from {
  opacity: 0; transform: translateY(10px);
}
.fade-leave-to {
  opacity: 0; transform: translateY(10px);
}
</style>
