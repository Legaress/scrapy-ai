<script setup>
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
const message = ref('')

const sendMessage = () => {
  console.log("Submit")
  if (message.value && message.value.trim()) {
    chatStore.sendMessage(message.value)
    message.value = ''
  }
}
</script>

<template>
    <v-text-field
    @keydown.enter="sendMessage"
      class="message-input"
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
          :loading="chatStore.isLoading"
          @click.prevent="sendMessage"
        ></v-btn>
      </template>
    </v-text-field>
</template>

<style scoped>
.message-input {
  width: 100%;
  padding: 8px;
}
</style>