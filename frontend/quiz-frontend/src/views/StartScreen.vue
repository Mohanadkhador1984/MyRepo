<template>
  <div class="start-screen">
    <div class="login-card">
      <h2>تسجيل الدخول / إنشاء حساب</h2>

      <!-- نموذج الدخول -->
      <LoginForm />

      <p class="switch">
        لا تملك حساباً؟ <router-link to="/signup">إنشاء حساب</router-link>
      </p>

      <hr/>

      <!-- نموذج التفعيل -->
      <h3>تفعيل النسخة الكاملة</h3>
      <ActivationForm :device-id="deviceId" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LoginForm from '@/components/LoginForm.vue'
import ActivationForm from '@/components/ActivationForm.vue'

const deviceId = ref(localStorage.getItem('device_uuid') || '')
</script>

<style scoped>
.start-screen {
  min-height: 100vh;
  background-color: #0f0f0f;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', sans-serif;
  padding: 1rem;
}

.login-card {
  background: #1a1a1a;
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  width: 100%;
  color: #ffd700;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
  text-align: center;
}

.login-card h2 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #ffd700;
}

.login-card h3 {
  font-size: 1.2rem;
  margin: 1.5rem 0 1rem;
  color: #ffd700;
}

.switch {
  margin: 1rem 0;
  color: #ccc;
}

.switch a {
  color: #ffd700;
  text-decoration: none;
}

.switch a:hover {
  text-decoration: underline;
}

hr {
  border: none;
  height: 1px;
  background: #333;
  margin: 1.5rem 0;
}
</style>
