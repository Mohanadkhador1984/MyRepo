<template>
  <div class="quiz-container">
    <div class="welcome">مرحبا بك في تطبيق بكالوريا إنكليزي</div>
    <div class="year-selection">
      <button @click="$emit('select','A')">أدبي</button>
      <button @click="$emit('select','B')">علمي</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BranchSelector'
}
</script>

<style scoped>
/* 1. متغيرات فاخرة */
:root {
  --primary:     #c59e44;
  --secondary:   #001f3f;
  --text-light:  #f5f5f5;
  --bg-dark:     #000;
  --radius:      16px;
  --transition:  0.3s ease-in-out;
}

/* 2. خلفية غنية بنمط متدرج مركزي + مركز المحتوى */
.quiz-container {
  display: grid;
  place-items: center;
  min-height: 100vh;
  padding: clamp(1rem, 5vw, 2rem);
  background: radial-gradient(circle at top left, #111 0%, var(--bg-dark) 90%);
  font-family: 'Tajawal', sans-serif;
  text-align: center;
  box-sizing: border-box;
}

/* 3. عنوان ترحيبي بتدرج ذهبي وظلال ناعمة */
.welcome {
  font-size: clamp(1.8rem, 6vw, 2.4rem);
  color: var(--primary);
  font-weight: 700;
  margin-bottom: clamp(2rem, 8vw, 3.5rem);
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
  line-height: 1.2;
}

/* 4. حاوية الأزرار مع إطار لامع وتأثير Shimmer */
.year-selection {
  position: relative;
  width: 100%;
  max-width: 380px;
  padding: clamp(1rem, 5vw, 2rem);
  background: rgba(0, 0, 0, 0.8);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7);
}

/* خطوط متحركة تلمع على الحد */
.year-selection::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    45deg,
    transparent 40%,
    rgba(197, 158, 68, 0.5),
    transparent 60%
  );
  animation: shimmer 4s linear infinite;
  pointer-events: none;
}

@keyframes shimmer {
  0%   { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(50%, 50%) rotate(360deg); }
}

/* 5. الأزرار بعرض كامل الحاوية وحشوة ديناميكية */
.year-selection button {
  width: 100%;
  padding: clamp(0.75rem, 4vw, 1rem) 0;
  margin-bottom: clamp(0.75rem, 4vw, 1rem);
  font-size: clamp(1rem, 4vw, 1.25rem);
  font-weight: 600;
  color: var(--text-light);
  background: radial-gradient(circle at center, var(--secondary) 0%, #001f3f 80%);
  border: none;
  border-radius: var(--radius);
  box-shadow:
    inset 0 0 0 2px var(--primary),
    0 4px 12px rgba(0, 0, 0, 0.8);
  cursor: pointer;
  transition: transform var(--transition), box-shadow var(--transition);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 6. تأثير التفاعل الفاخر */
.year-selection button:hover,
.year-selection button:focus {
  transform: translateY(-3px) scale(1.04);
  box-shadow:
    inset 0 0 0 3px var(--primary),
    0 6px 18px rgba(0, 0, 0, 0.9);
  outline: none;
}

/* 7. تحسين إضافي لأصغر الشاشات */
@media (max-width: 320px) {
  .welcome {
    font-size: clamp(1.6rem, 8vw, 2rem);
    margin-bottom: 2rem;
  }
  .year-selection {
    padding: 1rem;
  }
  .year-selection button {
    font-size: clamp(0.9rem, 5vw, 1.1rem);
    padding: 0.6rem 0;
    margin-bottom: 0.6rem;
  }
}
</style>
