import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axiosPlugin from './plugins/axios'

// أنماط
import './assets/styles/global.css'
import './assets/styles/quiz.css'

// توليد UUID للجهاز
const DEVICE_KEY = 'device_uuid'
if (!localStorage.getItem(DEVICE_KEY)) {
  const uuid = crypto.randomUUID?.() ||
    'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
      const r = Math.random() * 16 | 0
      const v = c === 'x' ? r : (r & 0x3 | 0x8)
      return v.toString(16)
    })
  localStorage.setItem(DEVICE_KEY, uuid)
}

// إنشاء التطبيق
const app = createApp(App)

// حدث PWA
let deferredPrompt = null
window.addEventListener('beforeinstallprompt', e => {
  e.preventDefault()
  deferredPrompt = e
  app.config.globalProperties.$deferredPrompt = deferredPrompt
})

// تركيب الإضافات
app.use(router)
app.use(axiosPlugin, {
  deviceId: localStorage.getItem(DEVICE_KEY)
})

// devTools
app.config.devtools = process.env.NODE_ENV !== 'production'

// Service Worker
if (process.env.NODE_ENV === 'production' && 'serviceWorker' in navigator) {
  import('./registerServiceWorker')
    .then(() => console.log('SW registered'))
    .catch(err => console.warn('SW failed:', err))
}

// تشغيل التطبيق
app.mount('#app')