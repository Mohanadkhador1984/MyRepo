<!-- src/components/SideDrawer.vue -->
<template>
  <transition name="fade">
    <div v-if="open" class="drawer-backdrop" @click.self="$emit('close')">
      <transition name="slide">
        <aside
          class="side-drawer"
          role="navigation"
          aria-label="أهلا وسهلا بكم"
        >
          <!-- Header -->
          <header class="drawer-header">
            <h2>أهلا وسهلا بكم</h2>
            <button class="btn close-btn" aria-label="إغلاق" @click="$emit('close')">
              <i class="fas fa-times"></i>
            </button>
          </header>

          <!-- Home -->
          <nav class="drawer-nav">
            <router-link to="/" class="drawer-item" @click="$emit('close')">
              <i class="fas fa-home"></i>
              <span>الصفحة الرئيسية</span>
            </router-link>

            <hr/>

            <!-- تواصل مع المطوّر -->
            <section class="section">
              <p class="section-title">تواصل مع المطوّر</p>
              <div class="social-grid">
                <button class="social-btn whatsapp" @click="contactWhatsApp">
                  <i class="fab fa-whatsapp"></i>
                  <span>واتساب</span>
                </button>
                <button class="social-btn sms" @click="contactSMS">
                  <i class="fas fa-sms"></i>
                  <span>رسالة نصية</span>
                </button>
                <button class="social-btn telegram" @click="contactTelegram">
                  <i class="fab fa-telegram-plane"></i>
                  <span>تليجرام</span>
                </button>
              </div>
            </section>

            <hr/>

            <!-- مشاركة التطبيق -->
            <section class="section">
              <p class="section-title">مشاركة التطبيق</p>
              <div class="social-grid">
                <button class="social-btn whatsapp" @click="shareWhatsApp">
                  <i class="fab fa-whatsapp"></i>
                  <span>واتساب</span>
                </button>
                <button class="social-btn messenger" @click="shareMessenger">
                  <i class="fab fa-facebook-messenger"></i>
                  <span>مسنجر</span>
                </button>
                <button class="social-btn telegram" @click="shareTelegram">
                  <i class="fab fa-telegram-plane"></i>
                  <span>تليجرام</span>
                </button>
              </div>
            </section>

            <hr class="divider" />

            <!-- زر صفحة المطوّر -->
            <button
              type="button"
              class="drawer-item dev-btn"
              @click="devModalOpen = true"
            >
              <i class="fas fa-user-shield"></i>
              <span>أعمالنا  </span>
            </button>
          </nav>
        </aside>
      </transition>
    </div>
  </transition>

  <!-- نافذة صفحة المطوّر -->
  <DevModal
    v-if="devModalOpen"
    @close="devModalOpen = false"
  />
</template>

<script>
import DevModal from './DevModal.vue'

export default {
  name: 'SideDrawer',
  components: { DevModal },
  props: {
    open: { type: Boolean, required: true }
  },
  data() {
    return {
      devModalOpen: false,
      devPhone: '0953447860',
      telegramUser: 'YourTelegramUsername',
      appUrl: window.location.origin,
      shareText: 'جرب هذا التطبيق الرائع!'
    }
  },
  methods: {
    contactWhatsApp() {
      const url = `https://wa.me/${this.devPhone}`
      window.open(url, '_blank')
    },
    contactSMS() {
      const url = `sms:${this.devPhone}?body=${encodeURIComponent('مرحباً')}`
      window.open(url)
    },
    contactTelegram() {
      const url = `https://t.me/${this.telegramUser}`
      window.open(url, '_blank')
    },
    shareWhatsApp() {
      const url = `https://wa.me/?text=${encodeURIComponent(this.shareText + ' ' + this.appUrl)}`
      window.open(url, '_blank')
    },
    shareMessenger() {
      const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(this.appUrl)}`
      window.open(url, '_blank')
    },
    shareTelegram() {
      const url = `https://t.me/share/url?url=${encodeURIComponent(this.appUrl)}&text=${encodeURIComponent(this.shareText)}`
      window.open(url, '_blank')
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600&display=swap');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css');

/* Backdrop fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: flex-start;
  z-index: 2000;
}

/* Drawer slide */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
.slide-enter-to,
.slide-leave-from {
  transform: translateX(0);
}

.side-drawer {
  width: 320px;
  max-width: 85%;
  background: #fff;
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding: 1rem;
  box-shadow: 4px 0 12px rgba(0,0,0,0.2);
  font-family: 'Cairo', sans-serif;
}

/* Header */
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.drawer-header h2 {
  margin: 0;
  font-size: 1.3rem;
  color: #333;
}
.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #555;
  cursor: pointer;
}
.close-btn:hover {
  color: #000;
}

/* Nav link */
.drawer-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.drawer-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.6rem 0.4rem;
  border-radius: 6px;
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.2s, transform 0.2s;
  background: none;
  border: none;
  cursor: pointer;
}
.drawer-item i {
  width: 24px;
  text-align: center;
}
.drawer-item:hover {
  background: #f0f0f0;
}

/* Sections */
.divider {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 1rem 0;
}
.section-title {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #444;
}
.social-grid {
  display: flex;
  gap: 0.6rem;
}

/* Buttons */
.social-btn {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #4e54c8, #8f94fb);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 0.5rem;
  font-size: 0.95rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.social-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

/* Individual colors */
.whatsapp { background: #25D366; }
.sms      { background: #007bff; }
.telegram { background: #0088cc; }
.messenger{ background: #0084FF; }

/* زر المطور */
.dev-btn {
  margin-top: 0.5rem;
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
</style>
