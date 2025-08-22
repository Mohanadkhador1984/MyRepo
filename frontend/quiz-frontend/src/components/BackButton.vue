<template>
  <button
    class="floating-back-btn"
    @click="handleBack"
    aria-label="رجوع"
  >
    <i class="fas fa-arrow-left"></i>
    <span class="label">إغلاق</span>
  </button>
</template>

<script>
export default {
  name: 'FloatingBackButton',
  methods: {
    handleBack() {
      // لو نحن داخل شاشة الامتحان (يمكن استبدال "ExamScreen" بالاسم الفعلي للمسار)
      if (this.$route.name === 'ExamScreen' || this.$route.path.startsWith('/exam')) {
        const confirmed = window.confirm('هل أنت متأكد من الخروج من الامتحان؟ سيتم فقدان التقدم الحالي.');
        if (confirmed) {
          this.$emit('back');
        }
      } else {
        this.$emit('back');
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* زر ثابت في الأسفل بنفس موضعك السابق */
.floating-back-btn {
  position: fixed;
  bottom: calc(1.5rem + 1.5cm);
  left: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 0.9rem;
  background: #6c63ff;
  border: 2px solid #5048e5;
  border-radius: 24px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  color: #fff;
  font-family: 'Cairo', sans-serif;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: transform 0.15s ease, background 0.3s ease;
  z-index: 1001;
  
}

.floating-back-btn:hover {
  background: #5048e5;
  transform: translateY(-2px);
}

.floating-back-btn:active {
  transform: translateY(1px) scale(0.97);
}

.floating-back-btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(81, 72, 229, 0.5);
}

.floating-back-btn i {
  pointer-events: none;
  font-size: 1.2rem;
}

.floating-back-btn .label {
  pointer-events: none;
  white-space: nowrap;
}
</style>
