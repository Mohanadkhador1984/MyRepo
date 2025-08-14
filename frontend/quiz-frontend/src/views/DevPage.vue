<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-white p-4">
    <h1 class="text-xl font-bold mb-4">🛠️ صفحة المطور - توليد كود التفعيل</h1>
    <input
      v-model="inputId"
      placeholder="أدخل كود الجهاز"
      class="border w-full max-w-md px-4 py-2 rounded text-center"
    />
    <button
      @click="generateCode"
      class="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
    >
      توليد الكود
    </button>

    <div v-if="generatedCode" class="mt-4 text-green-600 font-mono text-center">
      كود التفعيل: {{ generatedCode }}
    </div>

    <button @click="$router.push('/')" class="mt-6 text-sm text-gray-500 underline">
      العودة للواجهة
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      inputId: '',
      generatedCode: '',
    }
  },
  methods: {
    generateCode() {
      if (!this.inputId) return
      this.generatedCode = btoa(this.inputId).slice(0, 10)
    }
  }
}
</script>