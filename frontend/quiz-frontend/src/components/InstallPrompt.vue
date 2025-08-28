<!-- src/components/InstallAndInfo.vue -->
<template>
  <div v-if="showInstallBtn || showInfoBtn" class="actions-container">

    <!-- زر التثبيت الدائري -->
    <button
      v-if="showInstallBtn"
      class="install-circle-btn"
      @click="promptInstall"
      aria-label="تثبيت التطبيق"
    >
      <svg
        class="install-icon"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="M12 5v10m0 0l-3-3m3 3l3-3" />
        <path d="M4 17h16" />
      </svg>
    </button>

    <!-- زر التعجب -->
    <button
      v-if="showInfoBtn"
      class="info-btn"
      @click="openPopup"
      aria-label="تعليمات التثبيت"
    >
      ❗
    </button>

    <!-- نافذة التعليمات المنبثقة -->
    <transition name="fade-scale">
      <div
        v-if="showPopup"
        class="popup-backdrop"
        @click.self="closePopup"
      >
        <div class="popup-card">
          <button
            class="close-btn"
            @click="closePopup"
            aria-label="إغلاق"
          >
            ×
          </button>
          <h3 class="popup-title">كيفية إضافة التطبيق</h3>
          <p class="popup-text">
            1. اضغط زر القائمة (⋮) في متصفحك<br>
            2. اختر إضافة إلى الشاشة الرئيسية
          </p>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const deferredPrompt = ref(null)
const showInstallBtn  = ref(false)
const showInfoBtn     = ref(true)
const showPopup       = ref(false)

// التقاط حدث beforeinstallprompt
onMounted(() => {
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault()
    deferredPrompt.value = e
    showInstallBtn.value  = true
  })
})

function promptInstall() {
  if (!deferredPrompt.value) return
  deferredPrompt.value.prompt()
  deferredPrompt.value.userChoice.then(choice => {
    if (choice.outcome === 'accepted') {
      showInstallBtn.value = false
    }
    deferredPrompt.value = null
  })
}

function openPopup() {
  showPopup.value = true
}

function closePopup() {
  showPopup.value  = false
  showInfoBtn.value = false
}
</script>

<style scoped>
.actions-container {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  z-index: 10000;
}

/* زر التثبيت الدائري */
.install-circle-btn {
  width: 3.6rem;
  height: 3.6rem;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #36d1dc 0%, #5b86e5 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.install-circle-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

/* أيقونة السهم داخل زر التثبيت */
.install-icon {
  width: 1.6rem;
  height: 1.6rem;
  color: #fff;
}

/* زر التعجب */
.info-btn {
  width: 3.6rem;
  height: 3.6rem;
  font-size: 1.5rem;
  background: radial-gradient(circle, #ffd54f, #ffb300);
  color: #fff;
  border: none;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.info-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(0,0,0,0.3);
}

/* خلفية ونسق النافذة المنبثقة */
.popup-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10001;
}
.popup-card {
  position: relative;
  background: #fff;
  border-radius: 12px;
  padding: 1.5rem 1.2rem;
  width: 300px;
  text-align: center;
  box-shadow: 0 12px 32px rgba(0,0,0,0.2);
}
.close-btn {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #666;
}
.close-btn:hover {
  color: #333;
}
.popup-title {
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
  color: #333;
}
.popup-text {
  font-size: 0.95rem;
  color: #555;
  line-height: 1.5;
}

/* تأثير دخول/خروج */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
