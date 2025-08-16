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

    <!-- 2. رفع المحتوى أسفل الشريط -->
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
      // بدّل هنا بين 'ar' و 'en' أو استدعي ميثود من المكون الحالي
      this.$emit('toggle-lang')
    },
    resetQuiz() {
      // مثلاً: أرسل حدث للمكون QuizPage عبر bus أو استخدم vuex
      this.$emit('reset')
    }
  }
}
</script>

<style>
/* ارفع محتوى التطبيق أسفل شريط التنقل الثابت */
.app-main {
  margin-top: 4rem;               /* يساوي ارتفاع NavBar */
  min-height: calc(100vh - 4rem);
  padding: 1rem;
  box-sizing: border-box;
}
</style>
