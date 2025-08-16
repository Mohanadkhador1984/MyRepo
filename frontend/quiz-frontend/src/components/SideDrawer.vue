<!-- src/components/SideDrawer.vue -->
<template>
  <transition name="slide-drawer">
    <div
      v-if="open"
      class="drawer-wrapper"
      @keydown.esc="$emit('close')"
      tabindex="0"
    >
      <!-- Overlay -->
      <div class="drawer-overlay" @click="$emit('close')" />

      <!-- Side Drawer -->
      <aside
        class="side-drawer"
        role="navigation"
        aria-label="القائمة الجانبية"
      >
        <header class="drawer-header">
          <h2 class="drawer-title">القائمة</h2>
          <button
            class="close-btn"
            aria-label="إغلاق"
            @click="$emit('close')"
          >
            <i class="fas fa-times"></i>
          </button>
        </header>

        <nav class="drawer-nav">
          <router-link to="/" class="drawer-item">
            <div class="icon-wrap">
              <i class="fas fa-home"></i>
            </div>
            <span class="label">الرئيسية</span>
          </router-link>

          <router-link to="/profile" class="drawer-item">
            <div class="icon-wrap">
              <i class="fas fa-user"></i>
            </div>
            <span class="label">حسابي الشخصي</span>
          </router-link>

          <a
            href="https://facebook.com/YourPage"
            target="_blank"
            rel="noopener"
            class="drawer-item"
          >
            <div class="icon-wrap">
              <i class="fab fa-facebook-f"></i>
            </div>
            <span class="label">فيسبوك</span>
          </a>

          <router-link to="/dev" class="drawer-item">
            <div class="icon-wrap">
              <i class="fas fa-tools"></i>
            </div>
            <span class="label">حساب المطور</span>
          </router-link>

          <a
            href="https://wa.me/0953447860"
            target="_blank"
            rel="noopener"
            class="drawer-item"
          >
            <div class="icon-wrap whatsapp">
              <i class="fab fa-whatsapp"></i>
            </div>
            <div class="label-group">
              <span class="label">واتساب</span>
              <span class="sub-label">0953447860</span>
            </div>
          </a>

          <a
            href="https://myrepo-29.onrender.com"
            target="_blank"
            rel="noopener"
            class="drawer-item"
          >
            <div class="icon-wrap">
              <i class="fas fa-share-alt"></i>
            </div>
            <span class="label">دعوة الأصدقاء</span>
          </a>

          <hr class="divider" />

          <button class="drawer-item" @click="$emit('toggle-lang')">
            <div class="icon-wrap">
              <i class="fas fa-globe"></i>
            </div>
            <span class="label">تغيير اللغة</span>
          </button>

          <button class="drawer-item" @click="$emit('reset')">
            <div class="icon-wrap">
              <i class="fas fa-redo-alt"></i>
            </div>
            <span class="label">إعادة الاختبار</span>
          </button>
        </nav>
      </aside>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'SideDrawer',
  props: {
    open: { type: Boolean, required: true }
  }
}
</script>

<style scoped>
/* Theme Variables */
:root {
  --drawer-bg: #1f2029;
  --overlay-bg: rgba(0, 0, 0, 0.6);
  --text-color: #e4e6f0;
  --accent: #8b5cf6;
  --hover-bg: rgba(139, 92, 246, 0.15);
  --divider-color: rgba(255, 255, 255, 0.1);
}

/* Import fonts & icons */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

.drawer-wrapper {
  position: fixed;
  inset: 0;
  display: flex;
  justify-content: flex-end;
  z-index: 1000;
  outline: none;
}

.drawer-overlay {
  position: absolute;
  top: 4rem; /* below navbar */
  left: 0; right: 0; bottom: 0;
  background: var(--overlay-bg);
  backdrop-filter: blur(6px);
}

.side-drawer {
  position: relative;
  top: 4rem;
  width: 280px;
  height: calc(100% - 4rem);
  background: var(--drawer-bg);
  color: var(--text-color);
  font-family: 'Cairo', sans-serif;
  box-shadow: -12px 0 32px rgba(0, 0, 0, 0.8);
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Header */
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid var(--divider-color);
}

.drawer-title {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

/* Close Button */
.close-btn {
  background: transparent;
  border: none;
  color: var(--text-color);
  font-size: 1.2rem;
  width: 32px;
  height: 32px;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s, transform 0.1s;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: scale(1.1);
}

/* Navigation & Items */
.drawer-nav {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
}

.drawer-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  color: var(--text-color);
  border-radius: 6px;
  transition: background 0.25s, color 0.25s, padding-left 0.25s;
  font-weight: 500;
}

.drawer-item:hover {
  background: var(--hover-bg);
  padding-left: 1.75rem;
}

.drawer-item:active {
  background: rgba(139, 92, 246, 0.25);
}

/* Icon Wrap */
.icon-wrap {
  width: 36px;
  height: 36px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.25s, transform 0.25s;
}

.drawer-item:hover .icon-wrap {
  background: rgba(139, 92, 246, 0.2);
  transform: scale(1.05);
}

.icon-wrap.whatsapp {
  background: rgba(37, 211, 102, 0.1);
}

.drawer-item:hover .icon-wrap.whatsapp {
  background: rgba(37, 211, 102, 0.2);
}

/* Icon */
.icon-wrap i {
  color: var(--accent);
  font-size: 1.1rem;
}

/* Labels */
.label {
  flex-grow: 1;
  font-size: 1rem;
}

.label-group {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.sub-label {
  font-size: 0.85rem;
  color: #a1a6b0;
  margin-top: 2px;
}

/* Divider */
.divider {
  border: none;
  height: 1px;
  margin: 0.75rem 1.5rem;
  background: var(--divider-color);
}

/* Slide Animation */
.slide-drawer-enter-active,
.slide-drawer-leave-active {
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}
.slide-drawer-enter-from,
.slide-drawer-leave-to {
  transform: translateX(100%);
}
.slide-drawer-enter-to,
.slide-drawer-leave-from {
  transform: translateX(0);
}

/* Scrollbar */
.drawer-nav::-webkit-scrollbar {
  width: 6px;
}
.drawer-nav::-webkit-scrollbar-track {
  background: transparent;
}
.drawer-nav::-webkit-scrollbar-thumb {
  background-color: rgba(255,255,255,0.2);
  border-radius: 3px;
}
</style>
