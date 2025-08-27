<!-- src/views/DeveloperPage.vue -->
<template>
  <div class="dev-wrapper">
    <div class="dev-card">
      <!-- Animated Header -->
      <div class="dev-header">
        <i class="fas fa-magic header-icon"></i>
        <h2 class="header-title">🎛️ لوحة المطوّر</h2>
      </div>

      <!-- Device ID Editable & Copyable -->
      <div class="section">
        <label class="section-label">معرّف الجهاز:</label>
        <div class="input-block">
          <input
            v-model="deviceId"
            @blur="saveDeviceId"
            class="device-input"
          />
          <button class="copy-btn" @click="copyDeviceId" title="نسخ المعرّف">
            <i class="fas fa-copy"></i>
          </button>
        </div>
        <p class="hint">✏️ يمكنك تحرير المعرّف ثم الضغط خارجه للحفظ.</p>
      </div>

      <!-- Generate Activation Code -->
      <div class="section center">
        <button
          class="gen-btn"
          @click="generateCode"
          :disabled="isGenerating"
        >
          <i class="fas fa-key btn-icon"></i>
          <span v-if="!isGenerating">توليد كود التفعيل</span>
          <span v-else>جارٍ التوليد...</span>
        </button>
      </div>

      <!-- Activation Code Display -->
      <div v-if="activationCode" class="section">
        <label class="section-label">كود التفعيل:</label>
        <div class="copy-block">
          <code class="activation-code">{{ activationCode }}</code>
          <button class="copy-btn" @click="copyActivationCode" title="نسخ الكود">
            <i class="fas fa-copy"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Subtle Sparkle Overlay -->
    <div class="sparkles">
      <span v-for="n in 12" :key="n" class="sparkle"></span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeveloperPage',
  data() {
    let id = localStorage.getItem('device_uuid')
    if (!id) {
      id = crypto.randomUUID()
      localStorage.setItem('device_uuid', id)
    }
    return {
      deviceId: id,
      activationCode: '',
      isGenerating: false
    }
  },
  methods: {
    saveDeviceId() {
      localStorage.setItem('device_uuid', this.deviceId)
    },
    copyDeviceId() {
      navigator.clipboard.writeText(this.deviceId)
    },
    async generateCode() {
      this.isGenerating = true
      // لمسة سحرية: انتظر لحظات قبل العرض
      await new Promise(r => setTimeout(r, 800))
      this.activationCode = btoa(this.deviceId).slice(0, 10)
      this.isGenerating = false
    },
    copyActivationCode() {
      navigator.clipboard.writeText(this.activationCode)
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* Wrapper with animated gradient background */
.dev-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 1rem;
  min-height: 100vh;
  background: linear-gradient(135deg, #1e1e35, #2a2545);
  overflow: hidden;
  font-family: 'Cairo', sans-serif;
}

.dev-card {
  position: relative;
  background: #1f1f1f;
  border-radius: 16px;
  padding: 2rem;
  max-width: 480px;
  width: 100%;
  box-shadow: 
    0 8px 24px rgba(0,0,0,0.6),
    inset 0 0 12px rgba(255,255,255,0.05);
  border: 2px solid transparent;
  background-clip: padding-box;
}

/* Animated gradient border */
.dev-card::before {
  content: '';
  position: absolute;
  top: -2px; left: -2px; right: -2px; bottom: -2px;
  background: conic-gradient(
    from 0deg,
    #ffd700, #c59e44, #ffd700, #b07f17, #ffd700
  );
  z-index: -1;
  filter: blur(8px);
  animation: rotateBorder 6s linear infinite;
}

@keyframes rotateBorder {
  to { transform: rotate(360deg); }
}

/* Header */
.dev-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}
.header-icon {
  font-size: 1.8rem;
  color: #ffd700;
  animation: sparkle 2s ease-in-out infinite;
}
@keyframes sparkle {
  0%,100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.3); opacity: 0.7; }
}
.header-title {
  color: #ffd700;
  font-size: 1.6rem;
  margin: 0;
  text-shadow: 0 0 6px rgba(255,215,0,0.8);
}

/* Sections */
.section {
  margin-bottom: 1.5rem;
}
.section-label {
  display: block;
  font-weight: 600;
  color: #ddd;
  margin-bottom: 0.5rem;
}

/* Editable Input Block */
.input-block {
  display: flex;
  align-items: center;
  background: #2a2a3d;
  border-radius: 8px;
  padding: 0.5rem;
}
.device-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #f5f5f5;
  padding: 0.5rem;
  font-size: 1rem;
}
.device-input:focus {
  outline: none;
}
.copy-btn {
  background: none;
  border: none;
  color: #ffd700;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 0.5rem;
  transition: transform 0.2s;
}
.copy-btn:hover {
  transform: scale(1.2);
}

/* Hint text */
.hint {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #aaa;
}

/* Generate Button */
.center {
  text-align: center;
}
.gen-btn {
  background: linear-gradient(45deg, #22c55e, #16a34a);
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 0 6px 16px rgba(34,197,94,0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}
.gen-btn:disabled {
  opacity: 0.6;
  cursor: wait;
}
.gen-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(34,197,94,0.6);
}
/* Inner shine */
.gen-btn::before {
  content: '';
  position: absolute; top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.5) 0%, transparent 60%);
  transform: translateX(-100%) rotate(45deg);
  transition: transform 0.7s ease-in-out;
}
.gen-btn:hover::before {
  transform: translateX(100%) rotate(45deg);
}

/* Activation Code Block */
.copy-block {
  display: flex;
  align-items: center;
}
.activation-code {
  background: #2a2a3d;
  color: #f5f5f5;
  font-family: monospace;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  flex: 1;
  word-break: break-all;
  font-size: 0.95rem;
  margin-right: 0.5rem;
}

/* Sparkles overlay */
.sparkles {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
}
.sparkle {
  position: absolute;
  width: 6px; height: 6px;
  background: radial-gradient(circle, #fff, transparent);
  opacity: 0.8;
  animation: drift 8s linear infinite;
}
@keyframes drift {
  from { transform: translate(var(--x), var(--y)) scale(0.5); opacity: 0.8; }
  to   { transform: translate(calc(var(--x) + 50vw), calc(var(--y) + 50vh)) scale(1.5); opacity: 0; }
}
.sparkle:nth-child(odd) { animation-duration: 10s; }
.sparkle:nth-child(2n) { animation-duration: 12s; }
.sparkle:nth-child(3n) { animation-duration: 8s; }
.sparkle:nth-child(4n) { animation-duration: 14s; }
</style>
