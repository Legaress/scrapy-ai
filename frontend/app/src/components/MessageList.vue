<script setup>
import { useChatStore } from '@/stores/chat'
import VueMarkdown from 'vue-markdown-render'
import { useGoTo } from 'vuetify'

const chatStore = useChatStore()
const myUseGoTo = useGoTo()

const scrollToBottom = () => {
  nextTick(() => {
    myUseGoTo(document.querySelector(".bottom"),{ container: '.message-list'})
  })
}

watch(
  () => chatStore.displayedMessages,
  () => {
    scrollToBottom()
  },
  { 
    deep: true,
    flush: 'post' // Ensures watcher runs after DOM updates
  }
)

</script>

<template>
  <div class="message-list">
    <div v-for="message in chatStore.displayedMessages" 
         :key="message.id" 
         class="message-wrapper"
         :class="{ 'user-message-wrapper': message.sender === 'user' }">

      <v-avatar 
          v-if="message.sender !== 'user'"
          :size="32" 
          color="primary" 
          class="message-avatar"
        > 
        <v-icon>mdi-robot</v-icon>
      </v-avatar>
      
      <div class="message-bubble"
          :class="{
            'user-message': message.sender === 'user',
            'bot-message': message.sender !== 'user'}">
        <div class="message-content">
          <vue-markdown :source="message.text" />
        </div>
      </div>
    </div>

    <span class="bottom"></span>
  </div>
</template>

<style scoped>
.message-list {
  height: 100%;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message-wrapper {
  display: flex;
  width: 100%;
  align-items: flex-start;
  gap: 8px;
  font-weight: 500;
}

.user-message-wrapper {
  justify-content: flex-end;

}

.message-bubble {
  border-radius: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
  animation: fadeIn 0.3s ease-out;
  color: #f8faff
}

.bot-message {
  background-color: rgb(var(--v-theme-primary),0.3);
  padding: 8px 16px 8px 24px;
}

.user-message {
  background-color: rgb(var(--v-theme-secondary),0.3);
  padding: 8px 24px 8px 16px;
}

.message-avatar {
  flex-shrink: 0;
}

.message-content {
  line-height: 1.5;
  word-break: break-word;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>