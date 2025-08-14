<!-- src/components/ActivationForm.vue -->
<template>
  <form class="activation-form" @submit.prevent="handleActivate">
    <p>معرّف جهازك: <code>{{ props.deviceId }}</code></p>

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

    <button type="submit" :disabled="actLoading">
      <span v-if="!actLoading">تفعيل</span>
      <span v-else><i class="spinner"></i> جاري التفعيل…</span>
    </button>

    <p v-if="actError" class="error">⚠️ {{ actError }}</p>
  </form>
</template>

<script setup>
// تعطيل قواعد lint للخط التالي فقط
// eslint-disable-next-line vue/no-setup-props-destructure, no-undef
const props = defineProps({ deviceId: String })

import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { activateDevice } from '@/services/authService'

const router         = useRouter()
const activationCode = ref('')
const actLoading     = ref(false)
const actError       = ref('')

async function handleActivate() {
  actError.value   = ''
  actLoading.value = true

  try {
    await activateDevice(activationCode.value)
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
.activation-form p code {
  background: #333;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  color: #fff;
}

.activation-form .form-group {
  position: relative;
  margin: 1rem 0;
}

.activation-form input {
  width: 100%;
  padding: 0.75rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid #555;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.activation-form input:focus {
  outline: none;
  border-color: #ffd700;
}

.activation-form label {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  transform: translateY(-50%);
  color: #aaa;
  transition: 0.3s ease;
  pointer-events: none;
}

.activation-form input:focus + label,
.activation-form input:not(:placeholder-shown) + label {
  transform: translateY(-160%) scale(0.85);
  font-size: 0.85rem;
  color: #ffd700;
}

button[type='submit'] {
  width: 100%;
  padding: 0.75rem;
  background: #ffd700;
  color: #0f0f0f;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
  margin-top: 0.5rem;
}

button[type='submit']:hover:not(:disabled) {
  background: #e6c200;
}

button[type='submit']:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #0f0f0f;
  border-top: 2px solid rgba(0, 0, 0, 0.4);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error {
  color: #f87171;
  margin-top: 0.5rem;
  font-size: 0.95rem;
}
</style>
