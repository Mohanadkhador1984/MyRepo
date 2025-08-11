<template>
  <div class="start-container">
    <h1>مرحبًا بك في Quiz App</h1>
    <button @click="$router.push({ name: 'Login' })"  class="btn">تسجيل الدخول</button>
    <button @click="$router.push({ name: 'Signup' })" class="btn">إنشاء حساب</button>
  </div>
</template>

<script>
export default { name: 'StartScreen' }
</script>

<style scoped>
.start-container {
  display: flex; flex-direction: column; align-items: center;
  gap: 1.5rem; margin-top: 5rem;
}
.btn {
  padding: .75rem 1.5rem; background: #42b983; color: white;
  border: none; border-radius: 4px; cursor: pointer;
}
.btn:hover { background: #369b6f; }
</style>
