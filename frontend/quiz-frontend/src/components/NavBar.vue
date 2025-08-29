<!-- src/components/NavBar.vue -->
<template>
  <nav class="site-nav">
    <div class="nav-inner">
      <button class="nav-logo" @click="$router.push('/')">
        🏠
      </button>
      <h1 class="nav-title"> انكليزي بكالوريا </h1>
      <div class="nav-actions">
        <!-- ضع هنا أيقونات أو روابط إضافية حسب الحاجة -->
        <button class="nav-menu" @click="$emit('toggle-drawer')">☰</button>
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
.site-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4rem;               
  background-color: #000;   
  color: #fff;
  z-index: 1000;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5);
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-logo {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.5rem;
  cursor: pointer;
}

.nav-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin: 0;
}

.nav-actions button {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.5rem;
  cursor: pointer;
}
</style>
