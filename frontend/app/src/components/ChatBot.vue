<template>
    <v-card class="chatbot-wrapper" elevation="3">
      <!-- Header del Chat -->
      <v-toolbar color="primary" dark dense>
        <v-icon left>mdi-robot</v-icon>
        <v-toolbar-title>Asistente Virtual</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn
          icon
          @click="goToSettings"
          class="settings-btn"
        >
          <v-icon>mdi-cog</v-icon>
        </v-btn>
      </v-toolbar>
  
      <!-- Área de Mensajes -->
      <v-card-text class="message-area" ref="messageArea">
        <div 
          v-for="(msg, index) in chatStore.messages" 
          :key="index" 
          :class="['message', msg.sender]"
        >
          <v-avatar v-if="msg.sender === 'bot'" size="32" color="blue" class="mr-2">
            <v-icon dark>mdi-robot</v-icon>
          </v-avatar>
          <div class="message-content">
            <div class="text-bubble">{{ msg.text }}</div>
            <div class="message-timestamp">{{ formatTimestamp(msg.timestamp) }}</div>
          </div>
          <v-avatar v-if="msg.sender === 'user'" size="32" color="green" class="ml-2">
            <v-icon dark>mdi-account</v-icon>
          </v-avatar>
        </div>

        <!-- Indicador de escritura -->
        <div v-if="chatStore.isTyping" class="message bot">
          <v-avatar size="32" color="blue" class="mr-2">
            <v-icon dark>mdi-robot</v-icon>
          </v-avatar>
          <div class="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </v-card-text>
  
      <!-- Input de Mensaje -->
      <v-card-actions>
        <v-text-field
          v-model="userMessage"
          label="Escribe tu mensaje..."
          outlined
          dense
          hide-details
          @keyup.enter="sendMessage"
          class="flex-grow-1 mx-2"
          :disabled="chatStore.isLoading"
          :error-messages="chatStore.errorMessage"
          @input="chatStore.clearError"
        ></v-text-field>
        <v-btn 
          icon 
          color="primary" 
          @click="sendMessage"
          :disabled="!userMessage.trim() || chatStore.isLoading"
          :loading="chatStore.isLoading"
        >
          <v-icon>mdi-send</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick, watch } from 'vue';
  import { useChatStore } from '@/stores/chat';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const chatStore = useChatStore();
  const userMessage = ref('');
  const messageArea = ref(null);
  
  // Función para formatear la hora
  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };
  
  // Función para hacer scroll al último mensaje
  const scrollToBottom = async () => {
    await nextTick();
    if (messageArea.value) {
      messageArea.value.scrollTop = messageArea.value.scrollHeight;
    }
  };
  
  // Observar cambios en los mensajes para hacer scroll
  watch(() => chatStore.messages, () => {
    scrollToBottom();
  });
  
  // Enviar mensaje
  const sendMessage = async () => {
    if (!userMessage.value.trim() || chatStore.isLoading) return;
  
    const userMsg = userMessage.value;
    userMessage.value = '';
    
    await chatStore.sendMessage(userMsg);
  };
  
  // Scroll inicial
  onMounted(() => {
    scrollToBottom();
  });
  
  // Función para navegar a la página de configuración
  const goToSettings = () => {
    router.push('/settings');
  };
  </script>
  
  <style scoped>
  .chatbot-wrapper {
    width: 100%;
    max-width: 600px;
    height: 75vh;
    margin: 1rem auto;
    display: flex;
    flex-direction: column;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
  }
  
  .chatbot-wrapper:hover {
    box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
  }
  
  .message-area {
    flex-grow: 1;
    overflow-y: auto;
    background-color: #f8f9fa;
    padding: 20px;
    scroll-behavior: smooth;
    background-image: linear-gradient(rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.9)),
      url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }
  
  .message {
    display: flex;
    margin-bottom: 16px;
    align-items: flex-start;
    animation: fadeIn 0.3s ease-out;
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
  
  .message.user {
    justify-content: flex-end;
  }
  
  .message-content {
    display: flex;
    flex-direction: column;
    max-width: 75%;
    transition: all 0.2s ease;
  }
  
  .message-content:hover {
    transform: translateY(-1px);
  }
  
  .text-bubble {
    padding: 12px 16px;
    border-radius: 20px;
    word-wrap: break-word;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
  }
  
  .bot .text-bubble {
    background-color: white;
    color: #2c3e50;
    border: 1px solid #e9ecef;
    border-top-left-radius: 4px;
  }
  
  .bot .text-bubble:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .user .text-bubble {
    background: linear-gradient(135deg, #1976d2, #1565c0);
    color: white;
    border-top-right-radius: 4px;
  }
  
  .user .text-bubble:hover {
    background: linear-gradient(135deg, #1565c0, #0d47a1);
  }
  
  .message-timestamp {
    font-size: 0.7rem;
    color: #6c757d;
    margin-top: 4px;
    text-align: right;
    opacity: 0.8;
  }
  
  .typing-indicator {
    background-color: white;
    padding: 12px 16px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border: 1px solid #e9ecef;
    border-top-left-radius: 4px;
  }
  
  .typing-indicator span {
    width: 8px;
    height: 8px;
    background-color: #1976d2;
    border-radius: 50%;
    animation: typing 1.2s infinite ease-in-out;
    opacity: 0.7;
  }
  
  .typing-indicator span:nth-child(2) {
    animation-delay: 0.2s;
  }
  
  .typing-indicator span:nth-child(3) {
    animation-delay: 0.4s;
  }
  
  @keyframes typing {
    0%, 100% {
      transform: translateY(0) scale(1);
      opacity: 0.7;
    }
    50% {
      transform: translateY(-4px) scale(1.1);
      opacity: 1;
    }
  }
  
  /* Custom scrollbar */
  .message-area::-webkit-scrollbar {
    width: 6px;
  }
  
  .message-area::-webkit-scrollbar-track {
    background: transparent;
  }
  
  .message-area::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
  }
  
  .message-area::-webkit-scrollbar-thumb:hover {
    background-color: rgba(0, 0, 0, 0.2);
  }
  
  /* Input field styling */
  :deep(.v-text-field) {
    .v-field__input {
      padding: 12px 16px;
      font-size: 0.95rem;
    }
    
    .v-field__outline {
      border-radius: 24px;
    }
    
    &:hover .v-field__outline {
      opacity: 0.8;
    }
  }
  
  /* Send button styling */
  :deep(.v-btn) {
    transition: all 0.2s ease;
    
    &:hover:not(:disabled) {
      transform: scale(1.1);
    }
    
    &:active:not(:disabled) {
      transform: scale(0.95);
    }
  }
  
  /* Settings button styling */
  .settings-btn {
    transition: all 0.2s ease;
  }
  
  .settings-btn:hover {
    transform: rotate(30deg);
  }
  
  @media (max-width: 600px) {
    .chatbot-wrapper {
      height: 85vh;
      margin: 0;
      border-radius: 0;
    }
    
    .message-content {
      max-width: 85%;
    }
    
    .text-bubble {
      padding: 10px 14px;
    }
  }
  </style>