<!-- src/components/BackButton.vue -->
<template>
  <button
    class="floating-back-btn"
    @click="goBack"
    aria-label="رجوع"
    title="رجوع"
  >
    <i class="fas fa-arrow-left"></i>
    <span class="back-text">رجوع</span>
  </button>
</template>

<script>
export default {
  name: 'BackButton',
  emits: ['click'],
  methods: {
    goBack() {
      this.$emit('click')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.floating-back-btn {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  display: flex;
  align-items: center;
  background: #8b5cf6;
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 0.75rem 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  font-family: 'Cairo', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  z-index: 1001;
}

.floating-back-btn:hover {
  background: #7c3aed;
  transform: scale(1.05);
}

.floating-back-btn i {
  font-size: 1.25rem;
}

.back-text {
  margin-left: 0.5rem;
}
</style>
