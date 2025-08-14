// src/plugins/axios.js

import axios from 'axios'

// أنشئ instance إذا احتجت تهيئة منفصلة
export const api = axios.create({
  baseURL: 'http://localhost:8000',   // عدّل حسب الخلفية
})

// إضافة الهيدر للجهاز لو مرّرت deviceId عند التسطيب
export default {
  install(app, options = {}) {
    if (options.deviceId) {
      api.defaults.headers.common['Device-Id'] = options.deviceId
    }
    // تُثبت api تحت this.$api أو globalProperties.$api
    app.config.globalProperties.$api = api
  }
}
