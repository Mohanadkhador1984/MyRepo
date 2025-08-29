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
/* Arabic font for elegance */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');

/* 1. Nav container: deep black with soft glow & shimmer overlay */
.site-nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 4rem;
  background-color: #000;
  font-family: 'Cairo', sans-serif;
  color: #fff;
  display: flex;
  align-items: center;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
  overflow: hidden;
  z-index: 1000;
}

/* Moving shimmer haze for a magical vibe */
.site-nav::before {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.03), transparent 70%);
  mix-blend-mode: overlay;
  animation: shimmer-nav 10s infinite linear;
  pointer-events: none;
}

/* Layout of inner content */
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

/* 2. Logo & menu icons: scale + glow on hover */
.nav-logo,
.nav-menu {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s ease, text-shadow 0.3s ease;
}

.nav-logo:hover,
.nav-menu:hover {
  transform: scale(1.2);
  text-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
}

/* 3. Title with subtle animated underline */
.nav-title {
  font-size: 1.25rem;
  font-weight: 700;
  position: relative;
  margin: 0;
}

.nav-title::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, rgba(255,255,255,0.2), rgba(255,255,255,0.8));
  background-size: 200% 100%;
  animation: slide-underline 5s infinite linear;
}

/* Keyframes */
@keyframes shimmer-nav {
  0%   { transform: translate(-50%, -50%) scale(1);    }
  50%  { transform: translate(10%, 10%)   scale(1.1);  }
  100% { transform: translate(-50%, -50%) scale(1);    }
}

@keyframes slide-underline {
  0%   { background-position: 0% 0; }
  100% { background-position: 200% 0; }
}
</style>
