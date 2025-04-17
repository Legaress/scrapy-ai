<template>
    <v-card class="welcome-card" elevation="5">
      <!-- Encabezado con logo/avatar -->
      <div class="header">
        <v-avatar size="120" class="bot-avatar">
          <!-- Opcional: ícono si no hay imagen -->
          <v-icon v-if="!avatarLoaded" size="80" color="primary">mdi-robot-happy</v-icon>
        </v-avatar>
        <h1 class="text-h4 primary--text">¡Hola, soy AsistBot!</h1>
      </div>
  
      <!-- Cuerpo informativo -->
      <v-card-text class="content">
        <p class="text-body-1">
          Soy un chatbot inteligente creado como parte del <strong>proceso de evaluación técnica</strong> 
          para [Nombre de la Empresa]. Mi objetivo es demostrar habilidades en:
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
          <strong>Nota:</strong> Este proyecto utiliza Vue 3, Vuetify, Pinia y Vue Router.
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
  
  const avatarLoaded = ref(true); // Cambiar a false si no hay imagen
  const features = ref([
    'Vue 3 Composition API',
    'Integración con APIs de IA',
    'Diseño responsive con Vuetify',
    'Gestión de estado con Pinia',
    'Enrutamiento con Vue Router',
    'Personalización completa'
  ]);
  
  const startChat = () => {
    router.push('/chat');
  };
  
  const viewSettings = () => {
    router.push('/settings');
  };
  </script>
  
  <style scoped>
  .welcome-card {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    text-align: center;
  }
  
  .header {
    margin-bottom: 1.5rem;
  }
  
  .bot-avatar {
    margin: 0 auto 1rem;
    border: 3px solid rgb(var(--v-theme-primary));
  }
  
  .feature-list {
    background: transparent;
    text-align: left;
  }
  
  .actions {
    justify-content: center;
    gap: 12px;
    padding: 1rem;
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