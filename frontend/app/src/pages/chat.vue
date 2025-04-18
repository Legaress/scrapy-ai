<script setup>
import ChatContainer from '@/components/ChatContainer.vue'
</script>

<template>
  <v-app>
    <v-main>
      <v-container class="d-flex justify-center align-center fill-height">
        <ChatContainer />
      </v-container>
    </v-main>
  </v-app>
</template>

<style>
html, body, #app {
  height: 100%;
}
</style>
  