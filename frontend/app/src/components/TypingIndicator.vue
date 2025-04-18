<script setup>
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
</script>

<template>
  <v-list-item v-if="chatStore.isLoading" class="typing-indicator">
    <template v-slot:prepend>
      <v-avatar color="secondary">
        <v-icon>mdi-robot</v-icon>
      </v-avatar>
    </template>
    
    <v-list-item-title>Bot is typing...</v-list-item-title>
    
    <v-list-item-subtitle>
      <v-progress-linear indeterminate color="secondary"></v-progress-linear>
    </v-list-item-subtitle>
  </v-list-item>
</template>

<style scoped>
.typing-indicator {
  opacity: 0.8;
}
</style>