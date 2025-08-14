<!-- src/views/ActivationPage.vue -->
<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
    <div class="bg-white p-6 rounded shadow max-w-md w-full">
      <h1 class="text-xl font-bold text-center mb-4">مرحبا بك في الاختبار</h1>

      <p class="text-sm text-gray-600 mb-1">كود جهازك:</p>
      <div class="bg-gray-200 px-4 py-2 rounded text-center text-sm font-mono mb-4">
        {{ deviceId }}
      </div>

      <!-- زر النسخة المجانية يظهر فقط إذا لم يُفعّل الجهاز -->
      <button
        v-if="!isActivated"
        @click="enterFreeVersion"
        class="w-full bg-blue-600 text-white py-2 rounded mb-4"
      >
        الدخول للنسخة المجانية
      </button>

      <!-- حقول التفعيل تظهر فقط إذا لم يُفعّل الجهاز -->
      <div v-if="!isActivated">
        <input
          v-model="activationCode"
          placeholder="أدخل كود التفعيل"
          class="w-full border rounded px-3 py-2 mb-2"
        />
        <button
          @click="activate"
          class="w-full bg-green-600 text-white py-2 rounded mb-2"
        >
          تفعيل النسخة الكاملة
        </button>
        <p v-if="activationError" class="text-red-600 text-sm">
          {{ activationError }}
        </p>
      </div>

      <!-- رسالة النجاح وزر النسخة الكاملة بعد التفعيل -->
      <div v-else>
        <p class="text-green-600 text-sm mb-4">🎉 تم التفعيل بنجاح</p>
        <button
          @click="enterFullVersion"
          class="w-full bg-purple-600 text-white py-2 rounded"
        >
          الدخول للنسخة الكاملة
        </button>
      </div>

      <button
        @click="$router.push('/dev')"
        class="mt-6 text-xs text-gray-500 underline hover:text-gray-800"
      >
        صفحة المطور (توليد كود التفعيل)
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      deviceId: '',
      activationCode: '',
      isActivated: false,
      activationError: ''
    }
  },
  mounted() {
    // جلب UUID المخزن أو إنشاؤه
    let stored = localStorage.getItem('device_uuid')
    if (!stored) {
      stored = crypto.randomUUID()
      localStorage.setItem('device_uuid', stored)
    }
    this.deviceId = stored
    // قراءة حالة التفعيل
    this.isActivated = localStorage.getItem('activated') === 'true'
  },
  methods: {
    enterFreeVersion() {
      // نسخة مجانية (بدون تمكين الميزات المدفوعة)
      this.$router.push({
        name: 'QuizPage',
        query: { activated: false }
      })
    },
    enterFullVersion() {
      // نسخة كاملة (بعد التفعيل)
      this.$router.push({
        name: 'QuizPage',
        query: { activated: true }
      })
    },
    activate() {
      // محاكاة تحقق من الكود (بناءً على Base64)
      const validCode = btoa(this.deviceId).slice(0, 10)
      if (this.activationCode === validCode) {
        this.isActivated = true
        localStorage.setItem('activated', 'true')
        this.activationError = ''
      } else {
        this.activationError = 'كود التفعيل غير صحيح'
      }
    }
  }
}
</script>

<style scoped>
.input-code {
  width: 100%;
  max-width: 300px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
  text-align: center;
}

.btn-activate {
  width: 100%;
  background-color: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-activate:hover {
  background-color: #059669;
}

.text-red-600 {
  color: #dc2626;
}

.text-green-600 {
  color: #16a34a;
}
</style>
