<template>
  <div class="quiz-container">
    <h1>اختر الاختبار</h1>
    <div class="year-selection">
      <button
        v-for="y in options"
        :key="y"
        @click="$emit('select', y)"
      >
        {{ y }}
      </button>
    </div>
  </div>
</template>
<script>
export default {
  name: 'YearSelector',
  props: { options: Array }
}
</script>
