<template>
  <button class="floating-back-btn" @click="$emit('back')" aria-label="رجوع">
    <i class="fas fa-arrow-left"></i>
    <span class="label">رجوع</span>
  </button>
</template>

<script>
export default {
  name: 'FloatingBackButton'
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.floating-back-btn {
  position: fixed;
  bottom: calc(1.5rem + 1cm);
  left: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.6rem 1rem;
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  border: none;
  border-radius: 24px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
  color: #fff;
  font-family: 'Cairo', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.1s;
  z-index: 1001;
}

.floating-back-btn:hover {
  transform: scale(1.05);
}
.floating-back-btn:active {
  transform: scale(0.95);
}
.floating-back-btn i {
  pointer-events: none;
}
.floating-back-btn .label {
  pointer-events: none;
}
</style>
