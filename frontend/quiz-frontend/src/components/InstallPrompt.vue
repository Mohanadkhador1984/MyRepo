<!-- eslint-disable vue/no-parsing-error -->
<template>
  <div class="install-wrapper">
    <!-- زر التثبيت الرسمي (المتصفحات الداعمة لـ PWA) -->
    <button
      v-if="showInstallBtn"
      class="install-btn"
      @click="installApp"
    >
      📲 تثبيت التطبيق
    </button>

    <!-- أيقونة بديلة في حال المتصفح قديم أو لم يصلنا beforeinstallprompt -->
    <div
      v-else-if="showFallback"
      class="fallback-btn"
      @click="showManual = true"
      title="اضغط هنا لمعرفة طريقة الإضافة"
    >
      <i class="fas fa-info-circle"></i>
    </div>

    <!-- صندوق الإرشادات اليدوية يظهر عند الضغط على الأيقونة البديلة -->
    <transition name="fade-scale">
      <div
        v-if="showManual"
        ref="manualRef"
        class="manual-popup"
      >
        <button class="close-btn" @click="hideManual">
          <i class="fas fa-times"></i>
        </button>
        <h3 class="popup-title">كيفية إضافة التطبيق للشاشة الرئيسية</h3>
        <p class="popup-text">
          1. اضغط زر القائمة (⋮) في متصفحك<br>
          2. اختر <strong>إضافة إلى الشاشة الرئيسية</strong>
        </p>
        <p class="popup-text en">
          1. Tap the menu button (⋮) in your browser<br>
          2. Select <strong>Add to Home Screen</strong>
        </p>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const deferredPrompt = ref(null)
const showInstallBtn = ref(false)
const showFallback   = ref(false)
const showManual     = ref(false)
const manualRef      = ref(null)

function installApp() {
  if (!deferredPrompt.value) return
  deferredPrompt.value.prompt()

  // استخدمنا 'choice' بالكامل حتى لا يظهر خطأ no-unused-vars
  deferredPrompt.value.userChoice.then(choice => {
    console.log('Install outcome:', choice.outcome)
    deferredPrompt.value = null
    showInstallBtn.value = false
  })
}

function hideManual() {
  showManual.value = false
}

function handleClickOutside(e) {
  if (
    showManual.value &&
    manualRef.value &&
    !manualRef.value.contains(e.target)
  ) {
    hideManual()
  }
}

onMounted(() => {
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault()
    deferredPrompt.value = e
    showInstallBtn.value = true
  })

  // بعد 800ms إذا لم يصلنا beforeinstallprompt، نظهر أيقونة fallback
  setTimeout(() => {
    if (!showInstallBtn.value) {
      showFallback.value = true
    }
  }, 800)

  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.install-wrapper {
  position: fixed;
  bottom: 2cm;
  left: 2cm;
  z-index: 10000;
}

/* زر التثبيت */
.install-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: .8rem 1.8rem;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(37,99,235,0.3);
  cursor: pointer;
  pointer-events: auto;
  animation: pulse 1.6s ease-in-out infinite;
  transition: transform .2s, box-shadow .2s;
}
.install-btn:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 12px 32px rgba(37,99,235,0.5);
}
.install-btn:disabled {
  opacity: .7;
  cursor: wait;
}

/* أيقونة fallback */
.fallback-btn {
  font-size: 2rem;
  color: #2563eb;
  background: rgba(255,255,255,0.9);
  border-radius: 50%;
  padding: .4rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  cursor: pointer;
  pointer-events: auto;
  animation: pulse 2s ease-in-out infinite;
}

/* صندوق التعليمات */
.manual-popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 300px;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(8px);
  border-radius: 24px;
  padding: 1.2rem 1rem;
  box-shadow: 0 12px 32px rgba(0,0,0,0.2);
  text-align: center;
}
.manual-popup::after {
  content: "";
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  border: 12px solid transparent;
  border-top-color: rgba(255,255,255,0.9);
}
.close-btn {
  position: absolute;
  top: .6rem;
  right: .6rem;
  background: none;
  border: none;
  font-size: 1rem;
  color: #666;
  cursor: pointer;
}
.close-btn:hover {
  color: #333;
}
.popup-title {
  margin: 0 0 .6rem;
  font-size: 1.1rem;
  font-weight: 600;
}
.popup-text {
  margin: .4rem 0;
  font-size: .95rem;
  line-height: 1.4;
}
.popup-text.en {
  margin-top: .8rem;
  color: #555;
  font-style: italic;
}

@keyframes pulse {
  0%,100% { transform: scale(1); }
  50%     { transform: scale(1.05); }
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity .3s ease, transform .3s ease;
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
