import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    darkMode: false,
    selectedModel: 'gpt-3.5-turbo',
    availableModels: [
      { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo' },
      { id: 'gpt-4', name: 'GPT-4' },
      { id: 'claude-2', name: 'Claude 2' },
    ],
    fontSize: 14,
    enableSounds: true,
  }),
  actions: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode;
    },
    setModel(modelId) {
      this.selectedModel = modelId;
    },
  },
  persist: true, // Opcional: Usar plugin de persistencia para LocalStorage
}); 