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
      <aside class="side-drawer" role="navigation" aria-label="القائمة الجانبية">
        <header class="drawer-header">
          <h2 class="drawer-title">القائمة</h2>
          <button
            type="button"
            class="close-btn"
            aria-label="إغلاق"
            @click="$emit('close')"
          >
            <i class="fas fa-times"></i>
          </button>
        </header>

        <nav class="drawer-nav">
          <router-link to="/" class="drawer-item">
            <i class="fas fa-home"></i>
            <span>الصفحة الرئيسية</span>
          </router-link>

          <router-link to="/about" class="drawer-item">
            <i class="fas fa-info-circle"></i>
            <span>من نحن</span>
          </router-link>

          <a
            href="https://facebook.com/YourPage"
            target="_blank"
            rel="noopener"
            class="drawer-item"
          >
            <i class="fab fa-facebook-f"></i>
            <span>فيسبوك</span>
          </a>

          <a
            href="https://wa.me/0953447860"
            target="_blank"
            rel="noopener"
            class="drawer-item"
          >
            <i class="fab fa-whatsapp"></i>
            <span>واتساب</span>
          </a>

          <a
            href="https://t.me/YourChannel"
            target="_blank"
            rel="noopener"
            class="drawer-item"
          >
            <i class="fab fa-telegram-plane"></i>
            <span>تليجرام</span>
          </a>

          <hr class="divider" />

          <button
            type="button"
            class="drawer-item share-btn"
            @click="shareApp"
          >
            <i class="fas fa-share-alt"></i>
            <span>مشاركة التطبيق</span>
          </button>

          <!-- زر صفحة المطور -->
          <button
            type="button"
            class="drawer-item dev-btn"
            @click="devModalOpen = true"
          >
            <i class="fas fa-user-shield"></i>
            <span>صفحة المطوّر</span>
          </button>
        </nav>
      </aside>

      <!-- النافذة المنبثقة لصفحة المطور -->
      <DevModal
        v-if="devModalOpen"
        @close="devModalOpen = false"
      />
    </div>
  </transition>
</template>

<script>
import DevModal from '@/components/DevModal.vue';

export default {
  name: 'SideDrawer',
  components: { DevModal },
  props: {
    open: { type: Boolean, required: true }
  },
  data() {
    return {
      appUrl: 'https://myrepo-29.onrender.com',
      shareTitle: 'تطبيق مفيد',
      devModalOpen: false
    };
  },
  methods: {
    async shareApp() {
      if (navigator.share) {
        try {
          await navigator.share({
            title: this.shareTitle,
            text: 'جرب هذا التطبيق وسيُسعدك:',
            url: this.appUrl
          });
        } catch (err) {
          // المستخدم ألغى أو فشل
        }
      } else {
        try {
          await navigator.clipboard.writeText(this.appUrl);
          alert('تم نسخ رابط التطبيق إلى الحافظة');
        } catch {
          prompt('انسخ الرابط يدوياً:', this.appUrl);
        }
      }
    }
  }
};
</script>

<style scoped>
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
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
}

.side-drawer {
  position: relative;
  width: 300px;
  max-width: 85%;
  height: 100%;
  background: #1f2733;
  border-left: 6px solid #ff4081;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  color: #ececec;
  font-family: 'Cairo', sans-serif;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.6rem;
  background: #252f3a;
}

.drawer-title {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.close-btn:hover {
  transform: rotate(90deg);
  color: #e74c3c;
}

.drawer-nav {
  flex: 1;
  overflow-y: auto;
  padding: 0.8rem 0;
}

.drawer-item {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  padding: 0.8rem 1.6rem;
  color: inherit;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: background 0.2s, transform 0.2s;
}

.drawer-item i {
  width: 24px;
  text-align: center;
  font-size: 1.1rem;
}

.drawer-item span {
  flex: 1;
}

.drawer-item:hover {
  background: #303b47;
  transform: translateX(4px);
}

.divider {
  margin: 1rem 1.6rem;
  border: none;
  border-top: 1px solid #3b4550;
}

.share-btn {
  background: linear-gradient(45deg, #e91e63, #ff4081);
  color: #fff;
  border-radius: 30px;
}

.share-btn:hover {
  background: linear-gradient(45deg, #ff4081, #e91e63);
  box-shadow: 0 6px 16px rgba(233, 30, 99, 0.4);
  transform: scale(1.05);
}

/* زر المطور */
.dev-btn {
  background: #424a57;
  color: #facc15;
  border-radius: 8px;
}

.dev-btn i {
  color: #facc15;
}

.dev-btn:hover {
  background: #535c6a;
  transform: translateX(4px) scale(1.02);
}

/* Slide animation */
.slide-drawer-enter-active,
.slide-drawer-leave-active {
  transition: transform 0.3s ease;
}

.slide-drawer-enter-from,
.slide-drawer-leave-to {
  transform: translateX(100%);
}

.slide-drawer-enter-to,
.slide-drawer-leave-from {
  transform: translateX(0);
}

/* Custom scrollbar */
.drawer-nav::-webkit-scrollbar {
  width: 6px;
}

.drawer-nav::-webkit-scrollbar-thumb {
  background: #555;
  border-radius: 3px;
}
</style>
