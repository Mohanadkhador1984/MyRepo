<template>
  <button 
    v-if="showBtn" 
    @click="installApp" 
    class="install-btn"
  >
    📲 تثبيت التطبيق
  </button>
</template>

<script>
export default {
  data() {
    return {
      deferredPrompt: null,
      showBtn: false
    }
  },
  mounted() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showBtn = true;
    });
  },
  methods: {
    async installApp() {
      if (!this.deferredPrompt) return;
      this.deferredPrompt.prompt();
      const choice = await this.deferredPrompt.userChoice;
      console.log('Install outcome:', choice.outcome);
      this.deferredPrompt = null;
      this.showBtn = false;
    }
  }
}
</script>

<style>
.install-btn {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  background: #4a90e2;
  color: #fff;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  z-index: 1000;
}
</style>
