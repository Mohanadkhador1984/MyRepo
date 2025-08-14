// src/services/authService.js
import { api } from '@/plugins/axios'

// تسجيل الدخول كما كان
export function login(phone, password) {
  return api.post('/accounts/login/', { phone, password })
}

// تفعيل الجهاز
export function activateDevice(code) {
  return api.post('/devices/activate/', { code })
}

// جلب قائمة أكواد التفعيل
export async function getActivationCodes() {
  const res = await api.get('/devices/activation-codes/')
  return res.data  // مفترض أن تكون مصفوفة [{ id, code }, …]
}

// إنشاء رمز تفعيل جديد
export async function createActivationCode() {
  const res = await api.post('/devices/activation-codes/')
  return res.data  // { id, code }
}
