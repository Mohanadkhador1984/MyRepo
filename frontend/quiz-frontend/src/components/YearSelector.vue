<!-- src/components/YearSelector.vue -->
<template>
  <div class="year-selector">
    <button
      v-for="year in options"
      :key="year"
      type="button"
      class="year-btn"
      :disabled="disabled"
      @click="$emit('select', year)"
    >
      {{ year }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'YearSelector',
  props: {
    options: {
      type: Array,
      required: true
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.year-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin: 1rem 0;
}

.year-btn {
  padding: 0.6rem 1.2rem;
  background-color: #D4AF37; /* ذهبي */
  color: #111;              /* نص داكن */
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
}

.year-btn:hover:not(:disabled) {
  background-color: #C4A62A;
  transform: translateY(-1px);
}

.year-btn[disabled] {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #999;
}
</style>
