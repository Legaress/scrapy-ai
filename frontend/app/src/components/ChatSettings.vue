<template>
    <v-card class="settings-card" elevation="3">
      <v-card-title class="primary white--text">
        <v-icon left>mdi-cog</v-icon>
        Configuración del Chatbot
      </v-card-title>
  
      <v-card-text>
        <!-- Selector de Modelo -->
        <v-select
          v-model="settings.selectedModel"
          :items="settings.availableModels"
          item-value="id"
          item-title="name"
          label="Modelo de IA"
          outlined
          dense
          class="mb-4"
        ></v-select>
  
        <!-- Tema Oscuro -->
        <v-switch
          v-model="settings.darkMode"
          label="Tema oscuro"
          color="primary"
          @change="applyTheme"
        ></v-switch>
  
        <!-- Tamaño de Fuente -->
        <v-slider
          v-model="settings.fontSize"
          label="Tamaño de texto"
          min="12"
          max="24"
          step="1"
          thumb-label
        ></v-slider>
  
        <!-- Sonidos -->
        <v-switch
          v-model="settings.enableSounds"
          label="Efectos de sonido"
          color="secondary"
        ></v-switch>
  
        <!-- Botón de Guardar -->
        <v-btn 
          color="primary" 
          block 
          class="mt-4"
          @click="saveSettings"
        >
          <v-icon left>mdi-content-save</v-icon>
          Guardar
        </v-btn>
      </v-card-text>
    </v-card>
  </template>
  
  <script setup>
  import { useSettingsStore } from '@/stores/settings';
  import { watch } from 'vue';
  
  const settings = useSettingsStore();
  
  // Aplicar tema oscuro globalmente
  const applyTheme = () => {
    document.documentElement.setAttribute(
      'data-theme', 
      settings.darkMode ? 'dark' : 'light'
    );
  };
  
  // Opcional: Persistencia automática
  watch(
    () => settings.$state,
    (state) => {
      localStorage.setItem('chatSettings', JSON.stringify(state));
    },
    { deep: true }
  );
  
  const saveSettings = () => {
    // Aquí podrías enviar a una API
    console.log('Configuración guardada:', settings.$state);
  };
  </script>
  
  <style scoped>
  .settings-card {
    max-width: 500px;
    margin: 0 auto;
  }
  
  /* Opcional: Estilos para tema oscuro */
  [data-theme="dark"] {
    background-color: #121212;
    color: #ffffff;
  }
  </style>