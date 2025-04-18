<script setup>
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
const message = ref('')

const sendMessage = () => {
  if (message.value && message.value.trim()) {
    chatStore.sendMessage(message.value)
    message.value = ''
  }
}
</script>

<template>
  <v-form @submit.prevent="sendMessage" class="message-input">
    <v-text-field
      v-model="message"
      label="Type your message"
      variant="outlined"
      clearable
      :loading="chatStore.isLoading"
      :disabled="chatStore.isLoading"
    >
      <template v-slot:append-inner>
        <v-btn
          icon="mdi-send"
          variant="text"
          type="submit"
          :disabled="!message || !message.trim() || chatStore.isLoading"
        ></v-btn>
      </template>
    </v-text-field>
  </v-form>
</template>

<style scoped>
.message-input {
  padding: 8px;
}
</style>