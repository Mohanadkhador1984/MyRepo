<!-- src/views/DeveloperPage.vue -->
<template>
  <div class="dev-wrapper">
    <div class="dev-card">
      <!-- Header -->
      <div class="dev-header">
        <i class="fas fa-cogs header-icon"></i>
        <h2 class="header-title">🎛️ لوحة المطوّر</h2>
      </div>

      <!-- Device ID Section -->
      <div class="section">
        <label class="section-label">معرّف الجهاز:</label>
        <div class="code-block">
          <code>{{ deviceId }}</code>
          <button class="copy-btn" @click="copyDeviceId" title="نسخ المعرّف">
            <i class="fas fa-copy"></i>
          </button>
        </div>
      </div>

      <!-- Generate Button -->
      <div class="section center">
        <button class="gen-btn" @click="generateCode">
          <i class="fas fa-key btn-icon"></i>
          توليد كود التفعيل
        </button>
      </div>

      <!-- Activation Code Result -->
      <div v-if="activationCode" class="section">
        <label class="section-label">كود التفعيل:</label>
        <div class="code-block">
          <code>{{ activationCode }}</code>
          <button class="copy-btn" @click="copyActivationCode" title="نسخ الكود">
            <i class="fas fa-copy"></i>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeveloperPage',
  data() {
    // جلب أو إنشاء Device UUID ثابت
    let id = localStorage.getItem('device_uuid')
    if (!id) {
      id = crypto.randomUUID()
      localStorage.setItem('device_uuid', id)
    }
    return {
      deviceId: id,
      activationCode: ''
    }
  },
  methods: {
    generateCode() {
      // توليد الكود باقتطاع أول 10 أحرف من Base64
      this.activationCode = btoa(this.deviceId).slice(0, 10)
    },
    copyDeviceId() {
      navigator.clipboard.writeText(this.deviceId)
    },
    copyActivationCode() {
      navigator.clipboard.writeText(this.activationCode)
    }
  }
}
</script>

<style scoped>
/* Container & Card */
.dev-wrapper {
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
  background: #f0f2f5;
  min-height: calc(100vh - 4rem);
}

.dev-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  max-width: 480px;
  width: 100%;
  padding: 1.5rem;
  font-family: 'Cairo', sans-serif;
  color: #333;
}

/* Header */
.dev-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.header-icon {
  font-size: 1.6rem;
  color: #2563eb;
}

.header-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2563eb;
  margin: 0;
}

/* Sections */
.section {
  margin-bottom: 1rem;
}

.section-label {
  display: block;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  color: #555;
}

.center {
  text-align: center;
}

/* Code Block */
.code-block {
  position: relative;
  display: flex;
  align-items: center;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 0.6rem 0.75rem;
  font-family: monospace;
  font-size: 0.95rem;
  overflow-x: auto;
}

.code-block code {
  flex: 1;
  word-break: break-all;
}

/* Copy Button */
.copy-btn {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  margin-left: 0.5rem;
  font-size: 1.1rem;
  transition: color 0.2s;
}

.copy-btn:hover {
  color: #374151;
}

/* Generate Button */
.gen-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.7rem 1.4rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(34, 197, 94, 0.3);
  transition: transform 0.2s, box-shadow 0.2s;
}

.gen-btn .btn-icon {
  font-size: 1.2rem;
}

.gen-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(34, 197, 94, 0.4);
}

/* Result Styling */
.result code {
  color: #2563eb;
  font-weight: 600;
}
</style>
