import { defineStore } from 'pinia';

export const useChatStore = defineStore('chat', {
    id: 'chat',
    state: () => ({
        messages: [
            { 
                text: '¡Hola! ¿En qué puedo ayudarte hoy?', 
                sender: 'bot',
                timestamp: new Date()
            }
        ],
        isLoading: false,
        isTyping: false,
        errorMessage: '',
    }),

    actions: {
        async clearMessages() {
            this.messages = [
                { 
                    text: '¡Hola! ¿En qué puedo ayudarte hoy?', 
                    sender: 'bot',
                    timestamp: new Date()
                }
            ];
            this.isLoading = false;
            this.isTyping = false;
            this.errorMessage = '';

            const url = import.meta.env.VITE_FLOWISE_API + import.meta.env.VITE_FLOWISE_ENDPOINT_CHATMESSAGE + import.meta.env.VITE_CHATFLOW_ID;
            const token = import.meta.env.VITE_FLOWISE_TOKEN;
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                  "Authorization": token
                },
            });
            const data = await response.json();
            return data;
        },
        
        addMessage(text, sender, timestamp = new Date()) {
            this.messages.push({
                text,
                sender,
                timestamp,
            });
        },

        async sendMessage(userMessage) {
            if (!userMessage.trim() || this.isLoading) return;
            
            // Add user message
            this.addMessage(userMessage, 'user');
            
            try {
                this.isLoading = true;
                this.isTyping = true;
                
                // Simulate typing delay
                await new Promise(resolve => setTimeout(resolve, 800));
                
                const url = import.meta.env.VITE_N8N_API + import.meta.env.VITE_N8N_ENDPOINT;
                const token = import.meta.env.VITE_N8N_TOKEN;
                const response = await fetch(
                    url,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`,
                            "Content-Type": "application/json"
                        },
                        method: "POST",
                        body: JSON.stringify({ message: userMessage })
                    }
                );
                
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                
                const result = await response.json();
                
                // Add bot response
                this.addMessage(result.response || 'Lo siento, no pude procesar tu mensaje.', 'bot');
                
                return result;
            } catch (error) {
                console.error('Error sending message:', error);
                this.errorMessage = 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta de nuevo.';
                return { error: true, message: error.message };
            } finally {
                this.isLoading = false;
                this.isTyping = false;
            }
        },

        clearError() {
            this.errorMessage = '';
        },
    },
});