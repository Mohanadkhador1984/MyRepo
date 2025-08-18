<template>
  <button class="floating-back-btn" @click="$emit('back')">
    <i class="fas fa-arrow-left"></i>
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
  /* ارتفع 1 سم أعلى من موقعه الحالي */
  bottom: calc(1.5rem + 1.1cm);
  left: 1.5rem;
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  border: none;
  border-radius: 50%;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-family: 'Cairo', sans-serif;
  font-weight: 600;
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.1s;
  z-index: 1001;
}


.floating-back-btn:hover {
  transform: scale(1.1);
}

.floating-back-btn:active {
  transform: scale(0.95);
}

.floating-back-btn i {
  pointer-events: none;
}
</style>
