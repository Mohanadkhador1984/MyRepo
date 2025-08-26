<!-- src/components/DevModal.vue -->
<template>
  <div class="dev-modal">
    <div class="overlay" @click="$emit('close')" />

    <div class="modal-box" role="dialog" aria-modal="true">
      <button class="close" @click="$emit('close')">&times;</button>

      <div v-if="!isAuthed">
        <h3>🛡️ حماية المطوّر</h3>
        <DevAuth @auth-success="onAuthSuccess" />
      </div>

      <div v-else>
        <DeveloperPage />
      </div>
    </div>
  </div>
</template>

<script>
import DevAuth from '@/views/DevAuth.vue';
import DeveloperPage from '@/views/DeveloperPage.vue';

export default {
  name: 'DevModal',
  components: { DevAuth, DeveloperPage },
  data() {
    return { isAuthed: localStorage.getItem('devAuth') === 'true' };
  },
  methods: {
    onAuthSuccess() {
      this.isAuthed = true;
    }
  }
}
</script>

<style scoped>
.dev-modal {
  position: fixed; inset: 0; z-index: 1001;
}
.overlay {
  position: absolute; inset: 0;
  background: rgba(0,0,0,0.7);
}
.modal-box {
  position: relative;
  max-width: 450px;
  margin: 5% auto;
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  text-align: center;
}
.close {
  position: absolute; top: .5rem; right: .75rem;
  background: none; border: none;
  font-size: 1.5rem; cursor: pointer;
  color: #555;
}
.modal-box h3 {
  margin-bottom: 1rem; color: #2563EB;
}
</style>
