<template>
  <v-app>
    <v-main>
      <router-view />
    </v-main>
    
    <!-- Dev Tools (only visible in development) -->
    <DevTools />
  </v-app>
</template>

<script>
import DevTools from '@/components/DevTools.vue'

export default {
  name: 'App',
  components: {
    DevTools
  }
}
</script>
