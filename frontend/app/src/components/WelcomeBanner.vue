<template>
    <v-card class="welcome-card" elevation="5">
      <div class="header">
        <v-avatar size="120" class="bot-avatar">
          <v-icon size="80" color="primary">mdi-robot-happy</v-icon>
        </v-avatar>
        <h1 class="text-h4 primary--text">Hello, I'm ScrapyBot!</h1>
      </div>
  
      <v-card-text class="content">
        <p class="text-body-1">
          I'm an intelligent chatbot designed to be your knowledge companion. Here's what I can of 
        </p>
        
        <v-list dense class="feature-list">
          <v-list-item v-for="(feature, i) in features" :key="i">
            <template v-slot:prepend>
              <v-icon color="success">mdi-check-circle</v-icon>
            </template>
            <v-list-item-title>{{ feature }}</v-list-item-title>
          </v-list-item>
        </v-list>
  
        <v-alert type="info" variant="tonal" class="my-4">
          <strong>Nota:</strong> Ask me anything about books or tech news!
        </v-alert>
      </v-card-text>
  
      <!-- Llamado a la acción -->
      <v-card-actions class="actions">
        <v-btn 
          color="primary" 
          large 
          @click="startChat"
          class="start-button"
        >
          <v-icon left>mdi-forum</v-icon>
          Comenzar a chatear
        </v-btn>
        
        <v-btn 
          variant="outlined" 
          color="secondary" 
          @click="viewSettings"
        >
          <v-icon left>mdi-cog</v-icon>
          Configuración
        </v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import router from '@/router';
  
  const features = ref([
    'Access to my extensive book database',
  'Up-to-date information from Hacker News',
  'Quick summaries of trending tech topics',
  ]);
  
  const startChat = () => {
    router.push('/chat');
  };
  
  const viewSettings = () => {
    alert("in develoment phase")
  };
  </script>
  
  <style scoped>
  .welcome-card {
    max-width: 600px;
    margin: 24px auto;
    padding: 24px;
    text-align: center;
  }
  
  .header {
    margin-bottom: 18px;
  }
  
  .bot-avatar {
    margin: 0 auto 12px;
    border: 3px solid rgb(var(--v-theme-primary));
  }
  
  .feature-list {
    background: transparent;
    text-align: left;
  }
  
  .actions {
    justify-content: center;
    gap: 12px;
    padding: 12px;
  }
  
  .start-button {
    min-width: 200px;
  }
  
  /* Efecto hover para interactividad */
  .v-btn:hover {
    transform: translateY(-2px);
    transition: transform 0.2s;
  }
  </style>