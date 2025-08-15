<!-- src/components/ActivationForm.vue -->
<template>
  <div class="quiz-container auth-page">
    <h1>تفعيل الجهاز</h1>

    <p class="label">
      معرّف جهازك:
      <code class="device-code">{{ props.deviceId }}</code>
    </p>

    <div class="device-actions">
      <button class="btn btn-accent" @click="copyDeviceId">
        نسخ المعرّف
      </button>
      <button class="btn btn-success" @click="sendWhatsApp">
        إرسال عبر واتساب
      </button>
    </div>

    <form class="activation-form" @submit.prevent="handleActivate">
      <div class="form-group">
        <input
          id="activationCode"
          v-model="activationCode"
          type="text"
          placeholder=" "
          required
        />
        <label for="activationCode">رمز التفعيل</label>
      </div>

      <button
        type="submit"
        class="btn btn-primary"
        :disabled="actLoading"
      >
        <template v-if="!actLoading">تفعيل</template>
        <template v-else><i class="spinner"></i> جاري التفعيل…</template>
      </button>

      <p v-if="actError" class="error-text">⚠️ {{ actError }}</p>
    </form>
  </div>
</template>

<script setup>
// eslint-disable-next-line vue/no-setup-props-destructure
const props = defineProps({ deviceId: String })

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { activateDevice } from '@/services/authService'

const router       = useRouter()
const activationCode = ref('')
const actLoading     = ref(false)
const actError       = ref('')

function copyDeviceId() {
  navigator.clipboard.writeText(props.deviceId)
    .then(() => alert('تم نسخ المعرّف'))
}

function sendWhatsApp() {
  const msg = `رقم الجهاز: ${props.deviceId}`
  const url = `https://wa.me/0988131514?text=${encodeURIComponent(msg)}`
  window.open(url, '_blank')
}

async function handleActivate() {
  actError.value   = ''
  actLoading.value = true
  try {
    await activateDevice({ code: activationCode.value, deviceId: props.deviceId })
    localStorage.setItem('device_code', activationCode.value)
    router.push({ name: 'Quiz' })
  } catch (e) {
    actError.value = e.response?.data?.detail || 'رمز التفعيل غير صحيح'
  } finally {
    actLoading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  margin: 2rem auto;
  width: 100%;
  max-width: 420px;
}

.quiz-container {
  padding: 2rem;
}

/* العنوان */
h1 {
  color: var(--primary);
  font-size: clamp(1.5rem, 5vw, 2rem);
  margin-bottom: 1rem;
  text-align: center;
}

/* الوسم والمعرّف */
.label {
  color: var(--text-light);
  margin-bottom: 1rem;
  font-weight: 500;
  text-align: center;
}

.device-code {
  display: inline-block;
  background: rgba(255,255,255,0.1);
  padding: 0.5rem 1rem;
  border: 2px solid var(--primary);
  border-radius: var(--radius);
  color: var(--text);
  font-family: monospace;
  margin-top: 0.5rem;
}

/* أزرار نسخ وواتساب */
.device-actions {
  display: flex;
  gap: var(--spacing);
  justify-content: center;
  margin-bottom: 2rem;
}

.btn {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: transform var(--transition), background var(--transition);
}

.btn:hover {
  transform: translateY(-2px);
}

.btn-primary {
  background: var(--primary);
  color: var(--secondary);
  width: 100%;
  margin-bottom: var(--spacing);
}

.btn-accent {
  background: var(--accent);
  color: var(--text);
}

.btn-success {
  background: var(--success);
  color: var(--text);
}

/* نموذج التفعيل */
.activation-form .form-group {
  position: relative;
  margin-bottom: 1.5rem;
}

.activation-form input {
  width: 100%;
  padding: 0.75rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid var(--text-light);
  color: var(--text);
  font-size: 1rem;
  transition: border-color var(--transition);
}

.activation-form input:focus {
  outline: none;
  border-bottom-color: var(--primary);
}

.activation-form label {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-light);
  pointer-events: none;
  transition: transform var(--transition), color var(--transition), font-size var(--transition);
}

.activation-form input:focus + label,
.activation-form input:not(:placeholder-shown) + label {
  transform: translateY(-160%) scale(0.85);
  color: var(--primary);
  font-size: 0.85rem;
}

/* سبينر */
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--secondary);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  vertical-align: middle;
  margin-right: 0.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* رسالة الخطأ */
.error-text {
  color: var(--danger);
  font-size: 0.9rem;
  margin-top: 1rem;
  text-align: center;
}
</style>
