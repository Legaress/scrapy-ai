<script setup>
import { computed } from 'vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()

const props = defineProps({
  messages: {
    type: Array,
    required: true,
    default: () => []
  }
})

const formattedMessages = computed(() => {
  if (!props.messages) return []
  return props.messages.map(msg => ({
    ...msg,
    time: new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }))
})
</script>

<template>
  <v-list lines="two" class="message-list">
    <template v-for="message in formattedMessages" :key="message.id">
      <v-list-item
        :class="{
          'user-message': message.sender === 'user',
          'bot-message': message.sender === 'bot'
        }"
      >
        <template v-slot:prepend>
          <v-avatar :color="message.sender === 'user' ? 'primary' : 'secondary'">
            <v-icon v-if="message.sender === 'user'">mdi-account</v-icon>
            <v-icon v-else>mdi-robot</v-icon>
          </v-avatar>
        </template>

        <v-list-item-title>
          {{ message.sender === 'user' ? 'You' : 'Bot' }}
        </v-list-item-title>
        
        <v-list-item-subtitle>
          {{ message.text }}
        </v-list-item-subtitle>

        <template v-slot:append>
          <span class="text-caption text-grey">{{ message.time }}</span>
        </template>
      </v-list-item>
      <v-divider></v-divider>
    </template>
  </v-list>
</template>

<style scoped>
.message-list {
  height: 100%;
  overflow-y: auto;
}

.user-message {
  text-align: right;
}

.bot-message {
  text-align: left;
}
</style>