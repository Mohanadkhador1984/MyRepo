<!-- src/views/DevAuth.vue -->
<template>
  <div class="auth-page">
    <div class="spinner" v-if="loading"></div>

    <div v-else>
      <input
        v-model="password"
        type="password"
        placeholder="أدخل كلمة مرور حسابك"
      />
      <button @click="login">🔐 دخول</button>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DevAuth',
  data() {
    return { password: '', error: '', loading: false };
  },
  methods: {
    async login() {
      this.error = ''; this.loading = true;
      await new Promise(r => setTimeout(r, 800)); // لمحاكاة التحقق
      this.loading = false;

      const secret = process.env.VUE_APP_DEV_PASSWORD;
      if (this.password === secret) {
        localStorage.setItem('devAuth', 'true');
        this.$emit('auth-success');
      } else {
        this.error = '❌ كلمة المرور غير صحيحة';
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  display: flex; flex-direction: column;
  align-items: center; gap: 1rem;
}
.auth-page input {
  width: 100%; padding: .5rem;
  border: 1px solid #ccc; border-radius: .25rem;
  font-size: 1rem;
}
.auth-page button {
  padding: .6rem 1.2rem; background: #2563EB;
  color: #fff; border: none; border-radius: .25rem;
  cursor: pointer; font-size: 1rem;
}
.error { color: #DC2626; font-size: .9rem; }
.spinner {
  width: 40px; height: 40px;
  border: 5px solid #f3f3f3; border-top: 5px solid #2563EB;
  border-radius: 50%; animation: spin 1s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
