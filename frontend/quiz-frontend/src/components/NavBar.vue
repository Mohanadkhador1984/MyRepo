<!-- src/components/NavBar.vue -->
<template>
  <nav class="site-nav">
    <div class="nav-inner">
      <button class="nav-logo" @click="$router.push('/')">
        🏠
      </button>

      <h1 class="nav-title">انكليزي بكالوريا</h1>

      <div class="nav-actions">
        <button class="nav-menu" @click="$emit('toggle-drawer')">
          ☰
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
}
</script>

<style scoped>
/* 1. Import custom Arabic font */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

/* 2. Color variables: deep black + gold accent */
:root {
  --bg-start:  #000000;
  --bg-end:    #111111;
  --accent:    #FFD700;
  --text-main: #FFFFFF;
  --shadow:    rgba(0, 0, 0, 0.7);
}

/* 3. Nav container: pure black gradient, soft glow & border */
.site-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4rem;
  background: linear-gradient(90deg, var(--bg-start), var(--bg-end));
  color: var(--text-main);
  font-family: 'Cairo', sans-serif;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 12px var(--shadow);
  border-bottom: 2px solid var(--accent);
  overflow: hidden;
  z-index: 1000;
}

/* 4. Subtle shimmer overlay across the bar */
.site-nav::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 200%; height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.05),
    transparent
  );
  animation: shimmer 3s infinite ease-in-out;
  pointer-events: none;
}

/* 5. Inner layout */
.nav-inner {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

/* 6. Logo & menu icons */
.nav-logo,
.nav-menu {
  background: none;
  border: none;
  color: var(--text-main);
  font-size: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s ease, color 0.3s ease, text-shadow 0.3s ease;
}

.nav-logo:hover,
.nav-menu:hover {
  transform: scale(1.1);
  color: var(--accent);
  text-shadow: 0 0 8px rgba(255, 215, 0, 0.7);
}

/* 7. Title with animated underline */
.nav-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  position: relative;
}

.nav-title::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--accent),
    transparent
  );
  animation: slide-underline 3s infinite ease-in-out;
}

/* 8. Keyframes */
@keyframes shimmer {
  0%   { transform: translateX(-100%); }
  100% { transform: translateX(100%);  }
}

@keyframes slide-underline {
  0%,100% { transform: translateX(-100%); }
  50%     { transform: translateX(0);     }
}
</style>
