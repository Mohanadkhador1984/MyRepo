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
/* 1. استيراد خط عربي عصري */
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');

/* 2. ألوان أساسية */
:root {
  --primary:   #c59e44;   /* ذهبي */
  --secondary: #001f3f;   /* أزرق داكن */
  --light:     #f5f5f5;   /* أبيض فاتح */
}



/* 4. ترحيب كبير بنص ذهبي وظل خفيف */
.welcome {
  font-size: 2.0rem;
  font-weight: 700;
  color: var(--primary);
  text-shadow: 0 3px 8px rgba(0, 0, 0, 0.6);
  margin-bottom: 3.5rem;
  line-height: 1.2;
}

/* 5. العنوان الفرعي بنص أبيض وحجم متناسق */
.subtitle {
  font-size: 1.5rem;
  font-weight: 200;
  color: var(--light);
  margin-bottom: 2rem;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.5);
}

/* 6. الصندوق الأسود حول الأزرار */
.year-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem 3rem;
  background: #000;
  border: 3px solid var(--primary);
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
}

/* 7. أزرار كبيرة وواضحة */
.year-selection button {
  width: 260px;
  padding: 1rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--light);
  background: var(--secondary);
  border: 2px solid var(--primary);
  border-radius: 12px;
  transition: background 0.3s, transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 8. تأثير المرور والتفاعل */
.year-selection button:hover,
.year-selection button:focus {
  background: var(--primary);
  color: var(--secondary);
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7);
  outline: none;
}
</style>
