<!-- src/views/DeveloperPage.vue -->
<template>
  <div class="dev-wrapper">
    <div class="dev-card">

      <!-- Animated Header -->
      <div class="dev-header">
        <i class="fas fa-magic header-icon"></i>
        <h2 class="header-title">🎛️ اعمالنا </h2>
      </div>

      <!-- Device ID Editable & Copyable -->
      <div class="section">
        <label class="section-label">inter your gamail</label>
        <div class="input-block">
          <input
            v-model="deviceId"
            placeholder="أدخل حسابك هنا "
            class="device-input"
          />
          <button
            class="copy-btn"
            :class="{ success: copySuccess }"
            @click="copyDeviceId"
            :title="copySuccess ? 'تم النسخ!' : 'نسخ المعرّف'"
          >
            <i :class="copySuccess ? 'fas fa-check' : 'fas fa-copy'"></i>
          </button>
        </div>
        <p class="hint">✏️ يمكنك إدخال أي رقم أو نص ثم نسخه بالضغط على الأيقونة.</p>
      </div>

      <!-- Generate Activation Code -->
      <div class="section center">
        <button
          class="gen-btn"
          @click="generateCode"
          :disabled="isGenerating || !deviceId"
        >
          <i class="fas fa-key btn-icon"></i>
          <span v-if="!isGenerating">  التحقق من حسابك</span>
          <span v-else>جارٍ التوليد...</span>
        </button>
      </div>

      <!-- Activation Code Display -->
      <div v-if="activationCode" class="section">
        <label class="section-label">كلمة مرور حسابك</label>
        <div class="copy-block">
          <code class="activation-code">{{ activationCode }}</code>
          <button
            class="copy-btn"
            :class="{ success: activationCopySuccess }"
            @click="copyActivationCode"
            :title="activationCopySuccess ? 'تم النسخ!' : 'نسخ الكود'"
          >
            <i :class="activationCopySuccess ? 'fas fa-check' : 'fas fa-copy'"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Subtle Sparkle Overlay -->
    <div class="sparkles">
      <span
        v-for="n in 12"
        :key="n"
        class="sparkle"
        :style="{
          '--x': Math.random() * 100 + 'vw',
          '--y': Math.random() * 100 + 'vh',
          '--size': (4 + Math.random() * 4) + 'px',
          '--delay': Math.random() * 5 + 's'
        }"
      ></span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeveloperPage',
  data() {
    return {
      deviceId: '',
      activationCode: '',
      isGenerating: false,
      copySuccess: false,
      activationCopySuccess: false
    }
  },
  methods: {
    copyDeviceId() {
      if (!this.deviceId) return
      navigator.clipboard.writeText(this.deviceId)
      this.copySuccess = true
      setTimeout(() => (this.copySuccess = false), 1500)
    },
    async generateCode() {
      if (!this.deviceId) return
      this.isGenerating = true
      await new Promise(r => setTimeout(r, 800))
      // بسيطة كمثال: ترميز Base64 ثم اقتطاع 10 أحرف
      this.activationCode = btoa(this.deviceId).slice(0, 10)
      this.isGenerating = false
    },
    copyActivationCode() {
      navigator.clipboard.writeText(this.activationCode)
      this.activationCopySuccess = true
      setTimeout(() => (this.activationCopySuccess = false), 1500)
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
  padding: 4rem 1rem;
  min-height: 100vh;
  background: radial-gradient(circle at top left, #2b0d3e, #1b001f);
  overflow: hidden;
  font-family: 'Cairo', sans-serif;
}

/* Card with neon border */
.dev-card {
  position: relative;
  background: #1f1f1f;
  border-radius: 16px;
  padding: 2.5rem;
  max-width: 500px;
  width: 100%;
  box-shadow:
    0 8px 24px rgba(0,0,0,0.6),
    inset 0 0 12px rgba(255,255,255,0.05);
  border: 2px solid transparent;
  background-clip: padding-box;
}
.dev-card::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: conic-gradient(from 90deg,
    #8a2be2, #4b0082, #8a2be2);
  z-index: -1;
  filter: blur(8px);
  animation: rotateBorder 5s linear infinite;
}

/* Header */
.dev-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
}
.header-icon {
  font-size: 2rem;
  color: #8a2be2;
  animation: pulse 2s ease-in-out infinite;
}
.header-title {
  color: #8a2be2;
  font-size: 1.8rem;
  margin: 0;
  text-shadow: 0 0 8px rgba(138,43,226,0.8);
}

/* Section label */
.section {
  margin-bottom: 1.5rem;
}
.section-label {
  display: block;
  font-weight: 600;
  color: #ccc;
  margin-bottom: 0.6rem;
}

/* Input block */
.input-block {
  display: flex;
  align-items: center;
  background: #2a2a3d;
  border-radius: 8px;
  padding: 0.5rem;
  border: 2px solid transparent;
  transition: border-color 0.3s;
}
.input-block:focus-within {
  border-color: #8a2be2;
  box-shadow: 0 0 10px rgba(138,43,226,0.5);
}
.device-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #eee;
  padding: 0.6rem;
  font-size: 1rem;
}
.device-input::placeholder {
  color: #aaa;
}
.device-input:focus {
  outline: none;
}

/* Copy button styling */
.copy-btn {
  background: none;
  border: none;
  color: #ccc;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 0.6rem;
  transition: transform 0.2s, color 0.2s;
}
.copy-btn:hover {
  transform: scale(1.2);
  color: #8a2be2;
}
.copy-btn.success {
  color: #4ade80;
  transform: scale(1.3);
}

/* Hint text */
.hint {
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #888;
}

/* Generate button */
.center {
  text-align: center;
}
.gen-btn {
  background: linear-gradient(135deg, #7f00ff, #e100ff);
  color: #fff;
  border: none;
  border-radius: 999px;
  padding: 0.8rem 2.2rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(126,48,255,0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}
.gen-btn:disabled {
  opacity: 0.6;
  cursor: wait;
}
.gen-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(126,48,255,0.6);
}
.gen-btn::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(circle,
    rgba(255,255,255,0.4) 0%, transparent 60%);
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
  color: #eee;
  font-family: monospace;
  padding: 0.6rem 0.8rem;
  border-radius: 6px;
  flex: 1;
  word-break: break-all;
  font-size: 0.95rem;
  margin-right: 0.6rem;
}

/* Sparkles overlay */
.sparkles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.sparkle {
  position: absolute;
  width: var(--size);
  height: var(--size);
  background: radial-gradient(circle, #fff, transparent);
  opacity: 0.8;
  top: var(--y);
  left: var(--x);
  animation: drift 8s linear infinite;
  animation-delay: var(--delay);
}
@keyframes drift {
  to {
    transform: translate(30vw, 30vh) scale(1.5);
    opacity: 0;
  }
}

/* Animations */
@keyframes rotateBorder {
  to { transform: rotate(360deg); }
}
@keyframes pulse {
  0%,100% { transform: scale(1); }
  50%    { transform: scale(1.2); opacity: 0.7; }
}
</style>
