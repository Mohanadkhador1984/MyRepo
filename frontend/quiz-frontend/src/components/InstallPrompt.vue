<template>
  <div v-if="visible" class="install-wrapper">

    <!-- زر تثبيت التطبيق (كما كان) -->
    <button
      v-if="canPrompt"
      class="install-btn"
      @click="onInstallClick"
    >
      📥 تثبيت التطبيق
    </button>

    <!-- أيقونة بديلة للمتصفحات القديمة -->
    <div
      v-else
      class="fallback-icon"
      @click="showManual = true"
      title="أضف للتطبيق / Add to Home Screen"
    >
      <i class="fas fa-plus-square"></i>
    </div>

    <!-- نافذة الإرشادات اليدوية الفاخرة -->
    <transition name="fade-slide">
      <div
        v-if="showManual"
        class="manual-popup fancy"
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
import { ref, onMounted } from 'vue'

const deferredPrompt = ref(null)
const canPrompt      = ref(false)
const visible        = ref(false)
const showManual     = ref(false)

function onInstallClick() {
  deferredPrompt.value.prompt()
  deferredPrompt.value.userChoice.then(() => {
    visible.value = false
    deferredPrompt.value = null
  })
}

onMounted(() => {
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault()
    deferredPrompt.value = e
    canPrompt.value      = true
    visible.value        = true
  })

  setTimeout(() => {
    if (!canPrompt.value) visible.value = true
  }, 800)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* Wrapper */
.install-wrapper {
  position: fixed;
  left: 50%;
  bottom: 2cm;
  transform: translateX(-50%);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* زر التثبيت */
.install-btn {
  background: linear-gradient(135deg, #32a852, #28a745);
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  animation: pulseButton 1.8s ease-in-out infinite;
  transition: transform 0.2s, box-shadow 0.2s;
}
.install-btn:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 12px 24px rgba(0,0,0,0.3);
}

/* أيقونة البديل */
.fallback-icon {
  font-size: 2.4rem;
  color: #32a852;
  cursor: pointer;
  animation: pulseIcon 2s ease-in-out infinite;
  text-shadow: 0 0 6px rgba(50,168,82,0.6);
}

/* نافذة الإرشادات */
.manual-popup.fancy {
  position: absolute;
  bottom: 5.5cm;
  left: 50%;
  transform: translateX(-50%);
  width: 280px;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1.4rem 1.2rem;
  text-align: right;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  overflow: hidden;
}

/* إطار متدرّج متحرك */
.manual-popup.fancy::before {
  content: '';
  position: absolute;
  top: -2px; left: -2px; right: -2px; bottom: -2px;
  background: conic-gradient(from 0deg, #f9d423, #ff4e50, #f9d423);
  border-radius: inherit;
  z-index: -1;
  filter: blur(8px);
  animation: rotateBorder 4s linear infinite;
}

/* Close button */
.close-btn {
  position: absolute;
  top: 0.6rem; left: 0.6rem;
  background: none;
  border: none;
  color: #555;
  font-size: 1.1rem;
  cursor: pointer;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #000;
}

/* العنوان */
.popup-title {
  margin: 0 0 0.8rem;
  font-size: 1.05rem;
  font-weight: 600;
  color: #222;
}
.popup-title .en {
  display: block;
  font-size: 0.85rem;
  color: #555;
  margin-top: 0.2rem;
}

/* خطوات الإرشاد */
.popup-steps {
  list-style: none;
  padding: 0;
  margin: 0;
}
.popup-steps li {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.8rem;
  font-size: 0.9rem;
  color: #333;
}
.step-icon {
  font-size: 1.3rem;
  color: #28a745;
  margin-left: 0.6rem;
  margin-top: 2px;
}

/* أنيميشن الحافة */
@keyframes rotateBorder {
  to { transform: rotate(360deg); }
}

/* نبضات */
@keyframes pulseButton {
  0%,100% { transform: scale(1); }
  50% { transform: scale(1.06); }
}
@keyframes pulseIcon {
  0%,100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.2); }
}

/* Fade-slide تأثير دخول */
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
