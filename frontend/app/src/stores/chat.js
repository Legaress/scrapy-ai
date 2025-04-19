import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  // Computed property for reversed messages (to show newest at bottom)
  const displayedMessages = computed(() => [...messages.value])

  // Add a new message to the chat
  const addMessage = (message) => {
    messages.value.push(message)
  }

  const getBotResponse = async (userMessage) => {
    isLoading.value = true
    
    try {
      const url = import.meta.env.VITE_N8N_ENDPOINT;
      const response = await fetch(
          url,
          {
              headers: {
                  "Content-Type": "application/json"
              },
              method: "POST",
              body: JSON.stringify({ 'question': userMessage.text })
          }
      );
      
      const data = await response.json()
         
      addMessage({
        id: Date.now(),
        text: data.output,
        sender: 'bot',
        timestamp: new Date().toISOString()
      })
    } catch (err) {
      error.value = 'Failed to get bot response'
      console.error('Error:', err)
    } finally {
      isLoading.value = false
    }
  }

  // Send a message (user)
  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return
    
    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: 'user',
      timestamp: new Date().toISOString()
    }
    
    addMessage(userMessage)
    await getBotResponse(userMessage)
  }

  return {
    messages,
    displayedMessages,
    isLoading,
    error,
    sendMessage,
    addMessage
  }
})