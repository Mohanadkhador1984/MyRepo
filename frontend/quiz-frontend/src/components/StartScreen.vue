<template>
  <div class="start">
    <h1>مرحبًا بك في Quiz App</h1>
    <div class="buttons">
      <router-link to="/login"  class="btn">دخول</router-link>
      <router-link to="/signup" class="btn outline">إنشاء حساب</router-link>
    </div>
  </div>
</template>

<script>
export default { name: 'StartScreen' }
</script>

<style scoped>
.start {
  text-align: center;
  padding: 4rem 1rem;
}
.buttons {
  margin-top: 2rem;
}
.btn {
  display: inline-block;
  margin: 0 .5rem;
  padding: .75rem 1.5rem;
  background: #4f46e5;
  color: #fff;
  border-radius: 4px;
  text-decoration: none;
  transition: background .2s;
}
.btn:hover { background: #4338ca }
.btn.outline {
  background: transparent;
  border: 2px solid #4f46e5;
  color: #4f46e5;
}
.btn.outline:hover {
  background: #4f46e5;
  color: #fff;
}
</style>
