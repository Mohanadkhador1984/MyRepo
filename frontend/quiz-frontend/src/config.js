// src/config.js
const API_URL =
  process.env.VUE_APP_API_URL ||       // Vue-CLI
  'http://localhost:8000';              // قيمة افتراضية إن لم يُعرف المتغير

export default {
  baseURL: `${API_URL}/api/`
};
