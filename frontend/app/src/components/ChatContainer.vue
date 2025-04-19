<script setup>
import MessageList from '@/components/MessageList.vue'
import MessageInput from '@/components/MessageInput.vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()

</script>

<template>
  <v-card class="chat-container" elevation="4">
    <v-card-title class="d-flex align-center pa-4">
      <v-avatar color="primary" size="40" class="mr-3">
        <v-icon icon="mdi-robot" size="24"></v-icon>
      </v-avatar>
      <div class="d-flex flex-column">
        <div class="text-h6">ScrapyBot Assistant</div>
        <div class="text-caption text-medium-emphasis">Always here to help</div>
      </div>
      <v-spacer />
      <v-chip 
        v-if="chatStore.isLoading"
        color="info"
        size="small"
        class="ml-2"
        prepend-icon="mdi-connection"
      >
        Connecting...
      </v-chip>
    </v-card-title>
    
    <v-divider />
    
    <v-card-text class="messages-container">
      <MessageList />
    </v-card-text>
    
    <v-divider />
    
    <v-card-actions class="pa-4">
      <MessageInput />
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.chat-container {
  max-width: 800px;
  width: 100%;
  height: 96vh;
  display: flex;
  flex-direction: column;
  background-color: rgb(var(--v-theme-background));
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 0;
  background-color: rgb(var(--v-theme-surface));
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
}

/* Custom scrollbar styling */
.messages-container::-webkit-scrollbar {
  width: 8px;
}

.messages-container::-webkit-scrollbar-track {
  background: rgba(var(--v-theme-on-surface), 0.05);
  border-radius: 4px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.3);
  border-radius: 4px;
}

.messages-container::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.5);
}
</style>