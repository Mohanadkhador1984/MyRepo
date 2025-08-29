<template>
  <div class="quiz-container">
    <div class="welcome">تطبيق إنكليزي بكالوريا</div>
    <div class="year-selection">
      <button @click="$emit('select','A')">أدبي</button>
      <button @click="$emit('select','B')">علمي</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BranchSelector'
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');

:root {
  --primary:     #c59e44;
  --secondary:   #001f3f;
  --text-light:  #f5f5f5;
  --bg-dark:     #000;
  --radius:      16px;
  --transition:  0.3s ease-in-out;
}

/* خلفية ذات نمط فاخر ولمعة */
.quiz-container {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: clamp(1rem, 5vw, 2rem);
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
  font-family: 'Tajawal', sans-serif;
  text-align: center;
  box-sizing: border-box;
  position: relative;
  overflow: hidden;
}

/* تأثير لمعة متحركة في الخلفية */
.quiz-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 40%,
    rgba(197, 158, 68, 0.08),
    transparent 60%
  );
  animation: shimmer-bg 8s linear infinite;
  z-index: 0;
  pointer-events: none;
}

@keyframes shimmer-bg {
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* العنوان الذهبي */
.welcome {
  font-size: clamp(2rem, 6vw, 2.6rem);
  color: var(--primary);
  font-weight: 900;
  margin-bottom: clamp(2rem, 8vw, 3rem);
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
  z-index: 1;
}

/* حاوية الأزرار */
.year-selection {
  position: relative;
  width: 100%;
  max-width: 400px;
  padding: clamp(1rem, 5vw, 2rem);
  background: rgba(0, 0, 0, 0.85);
  border-radius: var(--radius);
  box-shadow:
    0 8px 30px rgba(0, 0, 0, 0.8),
    inset 0 0 10px rgba(255, 255, 255, 0.05);
  z-index: 1;
}

/* لمعة ذهبية متحركة داخل الحاوية */
.year-selection::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    60deg,
    transparent 45%,
    rgba(197, 158, 68, 0.12),
    transparent 55%
  );
  animation: shimmer-box 6s linear infinite;
  pointer-events: none;
  z-index: 0;
}

@keyframes shimmer-box {
  0%   { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

/* زر أنيق حديث */
.year-selection button {
  width: 100%;
  padding: clamp(0.8rem, 4vw, 1.2rem) 0;
  margin-bottom: clamp(1rem, 5vw, 1.5rem);
  font-size: clamp(1.1rem, 4vw, 1.4rem);
  font-weight: 700;
  color: var(--text-light);
  background: linear-gradient(145deg, #002b5c, #001f3f);
  border: 2px solid var(--primary);
  border-radius: var(--radius);
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.05),
    0 6px 20px rgba(0, 0, 0, 0.7);
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition);
  position: relative;
  z-index: 1;
}

/* تأثير النبض والضوء */
.year-selection button:hover,
.year-selection button:focus {
  transform: translateY(-3px) scale(1.03);
  box-shadow:
    0 0 10px var(--primary),
    0 8px 24px rgba(0, 0, 0, 0.9);
  outline: none;
}

/* تحسين إضافي للأجهزة الصغيرة */
@media (max-width: 360px) {
  .welcome {
    font-size: clamp(1.6rem, 8vw, 2.2rem);
    margin-bottom: 2rem;
  }
  .year-selection {
    padding: 1rem;
  }
  .year-selection button {
    font-size: clamp(1rem, 5vw, 1.2rem);
    padding: 0.6rem 0;
    margin-bottom: 0.8rem;
  }
}
</style>