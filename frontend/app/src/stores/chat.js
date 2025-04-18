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

  // Simulate bot response
  const getBotResponse = async (userMessage) => {
    isLoading.value = true
    
    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      const responses = [
        "I understand what you're saying.",
        "That's an interesting point!",
        "Could you elaborate on that?",
        "I'm still learning, but I'll do my best to help.",
        "Thanks for sharing that with me!"
      ]
      
      const randomResponse = responses[Math.floor(Math.random() * responses.length)]
      
      addMessage({
        id: Date.now(),
        text: randomResponse,
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