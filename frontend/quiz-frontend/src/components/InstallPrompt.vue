<template>
  <div v-if="visible" class="install-wrapper">

    <!-- زر التثبيت الفخم -->
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
      title="أضف للتطبيق"
    >
      <i class="fas fa-plus-square"></i>
    </div>

    <!-- نافذة الإرشادات اليدوية -->
    <transition name="fade">
      <div
        v-if="showManual"
        class="manual-popup"
      >
        <p>لإضافة التطبيق إلى شاشتك الرئيسية:</p>
        <ol>
          <li>اضغط ⋮ أو ⋯ في المتصفح</li>
          <li>اختر "Add to Home screen"</li>
        </ol>
        <button class="close-btn" @click="showManual = false">
          إغلاق
        </button>
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
  if (!deferredPrompt.value) return
  deferredPrompt.value.prompt()
  deferredPrompt.value.userChoice.then(choice => {
    console.log('User choice:', choice.outcome)
    visible.value = false
    deferredPrompt.value = null
  })
}

onMounted(() => {
  // 1) أسرع التقاط للحدث قبل انتهاء التحميل
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault()
    deferredPrompt.value = e
    canPrompt.value      = true
    visible.value        = true
  })

  // 2) بعد 800ms إذا لم يظهر الزر القياسي نعرض البديل
  setTimeout(() => {
    if (!canPrompt.value) {
      visible.value = true
    }
  }, 800)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.install-wrapper {
  position: fixed;
  left: 50%;
  bottom: 2cm; /* يرتفع 2 سم عن أسفل الشاشة */
  transform: translateX(-50%);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 1) زر التثبيت فخم ونابض */
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

/* 2) الأيقونة البديلة للمتصفحات القديمة */
.fallback-icon {
  font-size: 2.4rem;
  color: #32a852;
  cursor: pointer;
  animation: pulseIcon 2s ease-in-out infinite;
  text-shadow: 0 0 6px rgba(50,168,82,0.6);
}

/* 3) نافذة الإرشادات اليدوية */
.manual-popup {
  position: absolute;
  bottom: 4cm; /* فوق الزر بمسافة */
  left: 50%;
  transform: translateX(-50%);
  background: #ffffff;
  color: #333;
  border-radius: 8px;
  padding: 1rem 1.2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  width: 240px;
  text-align: right;
  font-size: 0.9rem;
}
.manual-popup p {
  margin: 0 0 0.5rem;
}
.manual-popup ol {
  margin: 0 0 0.8rem;
  padding-left: 1.2rem;
}
.close-btn {
  background: #e0e0e0;
  border: none;
  color: #555;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}
.close-btn:hover {
  background: #ccc;
}

/* 4) تأثير Fade */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 5) Pulse animations */
@keyframes pulseButton {
  0%,100% { transform: scale(1); }
  50%     { transform: scale(1.06); }
}
@keyframes pulseIcon {
  0%,100% { opacity: 1; transform: scale(1); }
  50%     { opacity: 0.6; transform: scale(1.2); }
}
</style>
