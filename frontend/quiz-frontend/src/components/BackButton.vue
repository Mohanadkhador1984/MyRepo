<!-- src/components/BackButton.vue -->
<template>
  <button
    class="go-back"
    @click="goBack"
    aria-label="رجوع"
    title="رجوع"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 20 20"
      fill="currentColor"
      class="icon-arrow"
    >
      <path
        fill-rule="evenodd"
        d="M12.293 16.293a1 1 0 010 1.414l-6-6a1 1 0 010-1.414l6-6a1 1 0 111.414 1.414L8.414 10l5.293 5.293a1 1 0 010 1.414z"
        clip-rule="evenodd"
      />
    </svg>
  </button>
</template>

<script>
export default {
  name: 'BackButton',
  emits: ['click'],
  methods: {
    goBack() {
      this.$emit('click')
    }
  }
}
</script>
