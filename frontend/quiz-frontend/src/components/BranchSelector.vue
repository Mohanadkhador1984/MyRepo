<template>
  <div class="quiz-container">
    <h1>اختر الفرع</h1>
    <div class="year-selection">
      <button @click="$emit('select', 'A')">أدبي</button>
      <button @click="$emit('select', 'B')">علمي</button>
    </div>
  </div>
</template>
<script>
export default { name: 'BranchSelector' }
</script>
