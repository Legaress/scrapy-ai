<script setup>
import MessageList from '@/components/MessageList.vue'
import MessageInput from '@/components/MessageInput.vue'
import TypingIndicator from '@/components/TypingIndicator.vue'
import { useChatStore } from '@/stores/chat'
import { onMounted, ref } from 'vue'

const chatStore = useChatStore()
const messageListRef = ref(null)

// Auto-scroll to bottom when new messages arrive
onMounted(() => {
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
})
</script>

<template>
  <v-card class="chat-container" elevation="4">
    <v-card-title class="d-flex align-center">
      <v-icon icon="mdi-robot" class="mr-2"></v-icon>
      Chatbot Assistant
    </v-card-title>
    
    <v-divider></v-divider>
    
    <v-card-text class="messages-container" ref="messageListRef">
      <MessageList :messages="chatStore.displayedMessages" />
      <TypingIndicator />
    </v-card-text>
    
    <v-divider></v-divider>
    
    <v-card-actions>
      <MessageInput />
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.chat-container {
  width: 100%;
  max-width: 800px;
  height: 70vh;
  display: flex;
  flex-direction: column;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 0;
}
</style>