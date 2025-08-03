import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles/quiz.css'
import './assets/styles/global.css'
import './registerServiceWorker'

const app = createApp(App)
app.use(router).mount('#app')
app.config.devtools = true

// تسجيل SW فقط في البناء النهائي
// بعد `app.mount('#app')`
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    console.log('⏳ Registering SW…');
    navigator.serviceWorker
      .register('/service-worker.js')
      .then(reg => console.log('✅ SW registered, scope=', reg.scope))
      .catch(err => console.error('❌ SW registration failed:', err));
  });
}


