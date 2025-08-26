<template>
  <div class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded-lg shadow-lg w-80 space-y-4 text-center">
      <h3 class="text-xl font-bold">تفعيل النسخة</h3>
      <input
        v-model="deviceCode"
        placeholder="أدخل رمز التفعيل"
        class="w-full border px-3 py-2 rounded"
      />
      <button
        @click="activate"
        class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
      >
        تفعيل
      </button>
      <p v-if="error" class="text-red-500">{{ error }}</p>
      <button
        @click="$emit('close')"
        class="mt-2 text-sm text-gray-500 hover:underline"
      >
        إلغاء
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ActivationModal',
  emits: ['activated', 'close'],
  setup(_, { emit }) {
    const deviceCode = ref('')
    const error      = ref('')

    function activate() {
      if (deviceCode.value === '864777mmm1984') {
        emit('activated', deviceCode.value)
      } else {
        error.value = 'رمز التفعيل غير صحيح'
      }
    }

    return { deviceCode, error, activate }
  }
}
</script>
