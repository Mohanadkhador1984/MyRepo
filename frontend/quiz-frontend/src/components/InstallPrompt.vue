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

    <!-- زر التعجب الفخم -->
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

          <div class="popup-content">
            <div class="arabic-steps">
              <h4>الخطوات بالعربية</h4>
              <ol>
                <li>اضغط زر القائمة (⋮) في متصفحك.</li>
                <li>اختر "إضافة إلى الشاشة الرئيسية".</li>
              </ol>
            </div>

            <div class="english-steps">
              <h4>Steps in English</h4>
              <ol>
                <li>Tap the menu button (⋮) in your browser.</li>
                <li>Select “Add to Home Screen.”</li>
              </ol>
            </div>
          </div>
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
  showPopup.value   = false
  showInfoBtn.value = false
}
</script>

<style scoped>
/* حاوية الأزرار على اليسار وفوق */
.actions-container {
  position: fixed;
  bottom: 4rem;
  left: 2rem;
  display: flex;
  gap: 1.2rem;
  align-items: center;
  z-index: 10000;
}

/* زر التثبيت */
.install-circle-btn {
  width: 4rem;
  height: 4rem;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #36d1dc 0%, #5b86e5 100%);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25),
              inset 0 0 8px rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.install-circle-btn:hover {
  transform: scale(1.15) rotate(-2deg);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3),
              inset 0 0 12px rgba(255, 255, 255, 0.3);
}

/* أيقونة التثبيت */
.install-icon {
  width: 1.8rem;
  height: 1.8rem;
  color: #fff;
}

/* زر التعجب الذهبي */
.info-btn {
  width: 4rem;
  height: 4rem;
  font-size: 1.8rem;
  border: none;
  border-radius: 50%;
  background: linear-gradient(45deg, #f39c12, #f1c40f);
  color: #fff;
  box-shadow: 0 0 12px rgba(243, 156, 18, 0.6),
              0 4px 16px rgba(0, 0, 0, 0.25);
  animation: pulse 2.5s infinite ease-in-out;
  cursor: pointer;
  transition: transform 0.2s;
}
.info-btn:hover {
  transform: scale(1.2);
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 0 12px rgba(243, 156, 18, 0.8); }
  50%      { box-shadow: 0 0 24px rgba(243, 156, 18, 0.4); }
}

/* خلفية النافذة المنبثقة */
.popup-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10001;
}

/* بطاقة النافذة المنبثقة وفخامة النص */
.popup-card {
  position: relative;
  background: #fff;
  border: 2px solid #d4af37;
  border-radius: 16px;
  padding: 1.6rem 1.4rem;
  width: 320px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
  font-family: 'Arial', sans-serif;
  color: #333;            /* نص واضح */
  line-height: 1.6;       /* مسافة أسطر مريحة */
  overflow: hidden;
}

/* زخرفة ذهبية صغيرة فوق البطاقة */
.popup-card::before {
  content: "";
  position: absolute;
  width: 12px;
  height: 12px;
  background: #d4af37;
  transform: rotate(45deg);
  top: -6px;
  right: calc(50% - 6px);
}

/* زر الإغلاق */
.close-btn {
  position: absolute;
  top: 0.6rem;
  right: 0.6rem;
  background: none;
  border: none;
  font-size: 1.3rem;
  color: #666;
  cursor: pointer;
  transition: color 0.2s;
}
.close-btn:hover {
  color: #333;
}

/* عنوان النافذة */
.popup-title {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: #d4af37;
  text-transform: uppercase;
  letter-spacing: 1px;
}

/* محتوى التعليمات مع نص مرئي */
.popup-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.popup-content ol {
  margin: 0;
  padding-left: 1.2rem;
  color: #333;
  font-size: 0.95rem;
  font-weight: 500;
}

/* تنسيق أقسام اللغة */
.arabic-steps {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 0.8rem;
  direction: rtl;
  text-align: right;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.05);
}
.english-steps {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 0.8rem;
  direction: ltr;
  text-align: left;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.05);
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
```