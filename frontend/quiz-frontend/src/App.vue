<template>
  <div id="app">
    <router-view/>
    <InstallPrompt/>
  </div>
</template>

<script>
import InstallPrompt from './components/InstallPrompt.vue';

export default {
  name: 'App',
  components: { InstallPrompt }
}
</script>
