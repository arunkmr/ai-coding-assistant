<template>
  <div class="chat-container">
    
    <!-- Messages -->
    <div class="messages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="msg.role"
      >
        {{ msg.text }}
      </div>

      <div v-if="loading" class="loading">
        AI is thinking...
      </div>
    </div>

    <!-- Input Box -->
    <div class="input-box">
      <textarea
        v-model="userInput"
        placeholder="Ask something..."
        @keydown.enter.prevent="sendMessage"
      ></textarea>

      <button @click="sendMessage" :disabled="loading">
        Send
      </button>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      userInput: "",
      messages: [],
      loading: false,
    };
  },

  methods: {
    async sendMessage() {
      if (!this.userInput.trim()) return;

      const userMessage = this.userInput;

      // 1. Push user message
      this.messages.push({
        role: "user",
        text: userMessage,
      });

      this.userInput = "";
      this.loading = true;

      try {
        // 2. Call backend
        const response = await axios.post(
          "http://localhost:8000/chat",
          {
            message: userMessage,
          }
        );

        // 3. Push AI response
        this.messages.push({
          role: "ai",
          text: response.data.response,
        });

      } catch (err) {
        this.messages.push({
          role: "ai",
          text: "Error connecting to server",
        });
      }

      this.loading = false;
    },
  },
};
</script>
<style scoped>
.chat-container {
  width: 700px;
  height: 80vh;
  margin: 20px auto;
  border: 1px solid #ccc;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  background: white;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user {
  background: #d1e7ff;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 10px;
  text-align: right;
}

.ai {
  background: #f1f1f1;
  padding: 10px;
  border-radius: 10px;
  text-align: left;
  white-space: pre-wrap;
  line-height: 1.5;
}

.loading {
  color: gray;
  font-style: italic;
}

.input-box {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ccc;
  gap: 10px;
}

textarea {
  flex: 1;
  height: 60px;
  padding: 10px;
  resize: none;
  border-radius: 8px;
  border: 1px solid #ccc;
}

button {
  width: 100px;
  border: none;
  border-radius: 8px;
  background: #007bff;
  color: white;
  cursor: pointer;
}

button:disabled {
  background: gray;
}
</style>