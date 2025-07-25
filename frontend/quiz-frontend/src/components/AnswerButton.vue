<template>
  <button
    :disabled="disabled"
    :class="{ correct: isCorrect, wrong: isWrong }"
    @click="$emit('select')"
  >
    {{ text }}
  </button>
</template>
<script>
export default {
  name: 'AnswerButton',
  props: {
    text: String,
    disabled: Boolean,
    isCorrect: Boolean,
    isWrong: Boolean
  }
}
</script>
<style scoped>
.correct { background: var(--success-color) !important; }
.wrong   { background: var(--danger-color) !important; }
</style>
