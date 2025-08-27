<template>
  <div v-if="!installed" class="install-wrapper">

    <!-- 1. Fancy Install Button -->
    <button
      v-if="canPrompt"
      class="install-btn"
      :disabled="installing"
      @click="onInstallClick"
    >
      <span v-if="!installing">📥 تثبيت التطبيق</span>
      <span v-else class="spinner"></span>
    </button>

    <!-- 2. Fallback + Icon for old browsers -->
    <div
      v-else-if="!installing"
      class="fallback-icon"
      @click="showManual = true"
      title="أضف للتطبيق / Add to Home Screen"
    >
      <i class="fas fa-plus-circle"></i>
    </div>

    <!-- 3. Manual Glassmorphic Popup -->
    <transition name="fade-slide">
      <div
        v-if="showManual && !installed"
        class="manual-popup"
      >
        <button class="close-btn" @click="showManual = false">
          <i class="fas fa-times"></i>
        </button>
        <h3 class="popup-title">
          إضافة للتطبيق  
          <span class="en">/ Add to Home Screen</span>
        </h3>
        <ul class="popup-steps">
          <li>
            <i class="fas fa-ellipsis-h step-icon"></i>
            اضغط ⋮ في شريط المتصفح  
            <span class="en">Tap ⋮ in your browser</span>
          </li>
          <li>
            <i class="fas fa-plus step-icon"></i>
            اختر “Add to Home screen”  
            <span class="en">Select “Add to Home screen”</span>
          </li>
        </ul>
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

function onInstallClick() {
  if (!deferredPrompt.value) return
  installing.value = true
  deferredPrompt.value.prompt()
  deferredPrompt.value.userChoice.then(({ outcome }) => {
    installing.value = false
    showManual.value = false
    if (outcome === 'accepted') {
      installed.value = true
    }
    deferredPrompt.value = null
  })
}

// Called when PWA is installed via system UI
function onAppInstalled() {
  installed.value = true
}

function detectInstalled() {
  // Chrome, Edge, etc.
  if (window.matchMedia('(display-mode: standalone)').matches) {
    installed.value = true
  }
  // Safari iOS
  if (window.navigator.standalone === true) {
    installed.value = true
  }
}

onMounted(() => {
  detectInstalled()
  window.addEventListener('appinstalled', onAppInstalled)
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault()
    deferredPrompt.value = e
    canPrompt.value      = true
  })

  // If no beforeinstallprompt after 800ms → show fallback
  setTimeout(() => {
    if (!canPrompt.value && !installed.value) {
      showManual.value = false // don't auto-open manual popup
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
  /* نلغي التحويل لأننا نقوم بضبط الإحداثيات يدوياً */
  transform: none;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 2) Gradient pulsating button */
.install-btn {
  background: linear-gradient(135deg, #6b21a8, #9333ea);
  color: #fff;
  border: none;
  border-radius: 100px;
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
  cursor: pointer;
  animation: pulse 1.6s ease-in-out infinite;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s, box-shadow 0.2s;
}
.install-btn:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 12px 24px rgba(0,0,0,0.3);
}
.install-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}
/* Spinner inside button */
.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

/* 3) Fallback icon pulsating */
.fallback-icon {
  font-size: 2.2rem;
  color: #9333ea;
  cursor: pointer;
  animation: pulse 2s ease-in-out infinite;
  text-shadow: 0 0 6px rgba(147,51,234,0.6);
}

/* 4) Manual glassmorphic popup */
.manual-popup {
  position: absolute;
  bottom: 5.5cm;
  left: 50%;
  transform: translateX(-50%);
  width: 280px;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  padding: 1.4rem 1.2rem;
  text-align: right;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  overflow: hidden;
}
/* Animated gradient border */
.manual-popup::before {
  content: '';
  position: absolute;
  top: -2px; left: -2px; right: -2px; bottom: -2px;
  background: conic-gradient(from 0deg, #9333ea, #6b21a8, #9333ea);
  border-radius: inherit;
  z-index: -1;
  filter: blur(8px);
  animation: rotateBorder 5s linear infinite;
}

/* Close button */
.close-btn {
  position: absolute;
  top: 0.6rem; left: 0.6rem;
  background: transparent;
  border: none;
  color: #555;
  font-size: 1.1rem;
  cursor: pointer;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #000;
}

/* Popup title */
.popup-title {
  margin: 0 0 1rem;
  font-size: 1rem;
  font-weight: 600;
  color: #222;
}
.popup-title .en {
  display: block;
  font-size: 0.85rem;
  color: #555;
  margin-top: 0.2rem;
}

/* Steps list */
.popup-steps {
  list-style: none;
  padding: 0;
  margin: 0;
}
.popup-steps li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #333;
}
.step-icon {
  font-size: 1.2rem;
  color: #9333ea;
  margin-left: 0.6rem;
  margin-top: 2px;
}

/* Animations */
@keyframes pulse {
  0%,100% { transform: scale(1); }
  50%     { transform: scale(1.05); }
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
@keyframes rotateBorder {
  to { transform: rotate(360deg); }
}

/* Fade-slide transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from {
  opacity: 0; transform: translateY(10px);
}
.fade-slide-leave-to {
  opacity: 0; transform: translateY(10px);
}
</style>
