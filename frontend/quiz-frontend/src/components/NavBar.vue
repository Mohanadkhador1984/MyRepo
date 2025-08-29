<template>
  <nav class="navbar">
    <div class="navbar-container">
      <button class="navbar-logo" @click="$router.push('/')">
        <span class="logo-icon">📘</span>
        <span class="logo-text">English Bac</span>
      </button>

      <h1 class="navbar-title">انكليزي بكالوريا</h1>

      <div class="navbar-actions">
        <button class="icon-button" @click="$emit('search')" title="بحث">🔍</button>
        <button class="icon-button" @click="$emit('profile')" title="الملف الشخصي">👤</button>
        <button class="menu-button" @click="$emit('toggle-drawer')" title="القائمة">☰</button>
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
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4.5rem;
  background: linear-gradient(to right, #0f0f0f, #1f1f1f);
  color: #fff;
  z-index: 1000;
  display: flex;
  align-items: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.8);
  font-family: 'Segoe UI', Roboto, Tahoma, sans-serif;
  padding: 0 1rem;
  backdrop-filter: blur(6px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.navbar-container {
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-logo {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  cursor: pointer;
  color: #facc15;
  font-weight: bold;
  font-size: 1.25rem;
  transition: all 0.3s ease;
}

.navbar-logo:hover {
  transform: scale(1.08);
  color: #fde68a;
}

.logo-icon {
  font-size: 1.8rem;
  margin-right: 0.4rem;
  filter: drop-shadow(0 0 4px #facc15);
}

.logo-text {
  font-size: 1.1rem;
  letter-spacing: 1px;
  color: #fef3c7;
}

.navbar-title {
  color: #e0e7ff;
  font-size: 1.6rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.05);
  flex: 1;
  text-align: center;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.icon-button,
.menu-button {
  background: none;
  border: none;
  font-size: 1.6rem;
  color: #f3f4f6;
  cursor: pointer;
  transition: all 0.3s ease;
}

.icon-button:hover,
.menu-button:hover {
  color: #facc15;
  transform: scale(1.2);
  text-shadow: 0 0 4px #facc15;
}

/* Responsive */
@media (max-width: 640px) {
  .navbar-title {
    font-size: 1.1rem;
  }

  .logo-text {
    display: none;
  }

  .logo-icon {
    font-size: 1.5rem;
  }

  .icon-button,
  .menu-button {
    font-size: 1.4rem;
  }
}
</style>