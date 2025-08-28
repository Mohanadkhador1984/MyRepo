<!-- src/components/InstallCTA.vue -->
<template>
  <div>

    <!-- 1) زر التثبيت الرسمي (إذا دعم المتصفح beforeinstallprompt) -->
    <button
      v-if="showInstallBtn"
      class="install-btn"
      @click="installApp"
    >
      📲 تثبيت التطبيق
    </button>

    <!-- 
      2) علامة التعجب (❗) كبديل لزر التثبيت في المتصفحات القديمة أو إذا لم يصل beforeinstallprompt 
         تُعلم المستخدم بكيفية إضافة التطبيق للشاشة الرئيسية 
    -->
    <div
      v-else-if="showFallback"
      class="fallback-btn"
      @click="openManual"
      title="اضغط هنا لمعرفة كيفية الإضافة"
    >
      ❗
    </div>

    <!--
      3) صندوق الإرشادات المنبثق بشكل “balloon” 
         يظهر عند النقر على علامة التعجب ويختفي عند النقر خارجه
    -->
    <transition name="fade-scale">
      <div
        v-if="showManual"
        ref="manualRef"
        class="manual-popup"
      >
        <!-- زر الإغلاق -->
        <button class="close-btn" @click="hideManual">✖</button>

        <!-- عنوان الشرح -->
        <h3 class="popup-title">كيفية إضافة التطبيق</h3>

        <!-- خطوات الإضافة بالعربية -->
        <p class="popup-text">
          1. اضغط زر القائمة (⋮) في متصفحك<br />
          2. اختر <strong>إضافة إلى الشاشة الرئيسية</strong>
        </p>

        <!-- نفس الشرح بالإنجليزية -->
        <p class="popup-text en">
          1. Tap the menu button (⋮) in your browser<br />
          2. Select <strong>Add to Home Screen</strong>
        </p>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

/* 
  متغيرات الحالة:
  - showInstallBtn: عند دعم PWA prompt
  - showFallback: عند عدم دعم prompt (المتصفحات القديمة)
  - showManual: عند فتح صندوق الإرشادات
*/
const deferredPrompt  = ref(null)
const showInstallBtn = ref(false)
const showFallback   = ref(false)
const showManual     = ref(false)
const manualRef      = ref(null)

/*
  عرض مربع الإرشادات وإخفاء علامة التعجب
*/
function openManual() {
  showManual.value = true
  showFallback.value = false
}

/*
  إخفاء مربع الإرشادات وعلامة التعجب
*/
function hideManual() {
  showManual.value = false
  showFallback.value = false
}

/*
  تنفيذ تثبيت PWA عند النقر على زر التثبيت
*/
function installApp() {
  if (!deferredPrompt.value) return
  deferredPrompt.value.prompt()
  deferredPrompt.value.userChoice.then(choice => {
    console.log('Install outcome:', choice.outcome)
    // بعد التثبيت أو الرفض نخفي الزر
    showInstallBtn.value = false
    deferredPrompt.value = null
  })
}

/*
  إخفاء صندوق الإرشادات عند النقر خارج العنصر
*/
function onDocumentClick(e) {
  if (
    showManual.value &&
    manualRef.value &&
    !manualRef.value.contains(e.target)
  ) {
    hideManual()
  }
}

onMounted(() => {
  // التقاط حدث beforeinstallprompt للمتصفحات الحديثة
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault()
    deferredPrompt.value = e
    showInstallBtn.value = true
  })

  // إذا لم يصلنا beforeinstallprompt خلال 800ms → عرض علامة التعجب
  setTimeout(() => {
    if (!showInstallBtn.value) {
      showFallback.value = true
    }
  }, 800)

  // الاستماع للنقرات في المستند لكشف النقر خارج صندوق الإرشادات
  document.addEventListener('click', onDocumentClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', onDocumentClick)
})
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* موضع الأزرار: 2 سم عن اليسار والأسفل */
.install-btn,
.fallback-btn {
  position: fixed;
  bottom: 2cm;
  left: 2cm;
  pointer-events: auto;
  z-index: 10000;
}

/* 1) زر التثبيت بتدرج أزرق فاخر */
.install-btn {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: .8rem 1.8rem;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(37,99,235,0.3);
  cursor: pointer;
  animation: pulse 1.6s ease-in-out infinite;
  transition: transform .2s, box-shadow .2s;
}
.install-btn:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 12px 32px rgba(37,99,235,0.5);
}

/* Spinner أثناء انتظار userChoice */
.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin .8s linear infinite;
}

/* 2) علامة التعجب كبديل */
.fallback-btn {
  font-size: 1.8rem;
  background: rgba(255,255,255,0.9);
  border-radius: 50%;
  padding: .3rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  cursor: pointer;
  animation: pulse 2s ease-in-out infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 3) صندوق الإرشادات المنبثق بشكل بالوني */
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
  z-index: 10001;
}
/* ذيل البالون */
.manual-popup::after {
  content: "";
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  border: 12px solid transparent;
  border-top-color: rgba(255,255,255,0.9);
}

/* زر الإغلاق */
.close-btn {
  position: absolute;
  top: .6rem;
  right: .6rem;
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
}
.close-btn:hover {
  color: #333;
}

/* نصوص الشرح */
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

/* أنيميشنات */
@keyframes pulse {
  0%,100% { transform: scale(1); }
  50%     { transform: scale(1.05); }
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* انتقال صندوق التعليمات */
.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity .3s, transform .3s;
}
.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style>
