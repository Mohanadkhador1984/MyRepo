<template>
  <div id="app">
    <!-- 1. NavBar + SideDrawer -->
    <NavBar @toggle-drawer="drawerOpen = !drawerOpen" />
    <SideDrawer
      :open="drawerOpen"
      @close="drawerOpen = false"
      @toggle-lang="toggleLanguage"
      @reset="resetQuiz"
    />

    <!-- 2. المحتوى الرئيسي أسفل الشريط -->
    <main class="app-main">
      <router-view />
      <InstallPrompt />
    </main>

   
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import SideDrawer from './components/SideDrawer.vue'
import InstallPrompt from './components/InstallPrompt.vue'


export default {
  name: 'App',
  components: {
    NavBar,
    SideDrawer,
    InstallPrompt
  },
  data() {
    return {
      drawerOpen: false
    }
  },
  methods: {
    toggleLanguage() {
      this.$emit('toggle-lang')
    },
    resetQuiz() {
      this.$emit('reset')
    }
  }
}
</script>

<style>
/*  رفع المحتوى أسفل شريط التنقل */
.app-main {
  margin-top: 4rem;               /* ارتفاع NavBar */
  margin-bottom: 3rem;            /* مساحة مخصصة للـ footer */
  min-height: calc(100vh - 7rem); /* يحسب 4rem nav + 3rem footer */
  padding: 1rem;
  box-sizing: border-box;
}

/* تصميم footer رابط صفحة المطوّر */
.dev-link {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3rem;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 -1px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.dev-link a {
  color: #2563EB;
  text-decoration: none;
  font-weight: bold;
}
</style>
