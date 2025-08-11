// src/services/authService.js
import axios from 'axios'

const API_URL = '/api/auth/'

export function login(phone, password) {
  return axios
    .post(`${API_URL}login/`, { phone, password })
    .then(({ data }) => {
      // حفظ التوكنات بأسماء ثابتة
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)

      // إعداد هيدر Authorization للجلسات اللاحقة
      axios.defaults.headers.common['Authorization'] = `Bearer ${data.access}`

      return data
    })
}

export function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  delete axios.defaults.headers.common['Authorization']
}
