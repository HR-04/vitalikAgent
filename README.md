
# 🧠 **Vitalik Agent** – AI-Powered Chatbot Emulating Vitalik Buterin

**Vitalik Agent** is a cutting-edge, AI-powered chatbot designed to mimic the distinct personality, speech style, and voice of **Vitalik Buterin**, co-founder of Ethereum. This interactive agent enables users to engage in both **text** and **voice** conversations, providing insightful and thought-provoking responses on topics related to **blockchain**, **Ethereum**, and more—just as Vitalik would.


## Key Features

### 💬 **Text Interaction**  
Engage in detailed conversations with the **Vitalik Agent** through text. Receive insightful answers that reflect Vitalik’s deep technical expertise, visionary thinking, and passion for decentralized technologies.

### 🎤 **Voice Interaction**  
Experience an ultra-realistic voice model that emulates Vitalik’s tone and speaking style. Hear responses in real-time, delivered by a high-fidelity TTS (Text-to-Speech) model, for an authentic, immersive interaction.

### ⚡ **Real-Time Communication**  
Whether through **text** or **voice**, Vitalik Agent responds instantly with synchronized speech and text, making interactions seamless and dynamic.

---

## Key Deliverables

### 1. **Vitalik Text Persona (LLM Layer)**  
- Powered by a fine-tuned **Llama3.1:8b** model that replicates Vitalik’s reasoning, speech patterns, and technical depth.  
- Trained on a diverse range of **Vitalik's public content**—including blog posts, tweets, interviews, and talks.

### 2. **Voice Model (TTS)**  
- Utilizes the **OpenVoice TTS** system to create a realistic voice model that perfectly captures Vitalik’s distinctive tone and cadence.  
- The system ensures near-instant voice responses with **ultra-low latency** (under 1 second).

### 3. **Speech-to-Text (STT)**  
- Integrates **Whisper** for fast and accurate speech recognition, providing real-time transcription of voice inputs.

### 4. **Frontend Chat Interface**  
- An intuitive, minimalist **Streamlit**-based interface that allows easy text or voice input.  
- **Mic Input + Live Transcription:** Speak directly to the agent and see your speech transcribed in real-time.  
- **Vitalik-Like Text Output:** Receive responses crafted in Vitalik’s signature style.  
- **Synchronized Voice Output (TTS):** Enjoy listening to responses spoken in Vitalik’s unique voice.

---

## Tech Stack

- **Streamlit** for UI development  
- **Whisper** for Speech-to-Text (STT)  
- **OpenVoice** for Text-to-Speech (TTS)  
- **Unsloth** for model fine-tuning

---

## Installation Instructions

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HR-04/vitalikAgent.git
   cd vitalik-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. [Download the necessary model checkpoints and place them in the `checkpoints_v2` directory](https://drive.google.com/drive/folders/1P1tlKkx7WbnR2CVVNIu7DW3MIiL3zb1R?usp=drive_link)

4. **Download the Vitalik Buterin model** for interaction:  
   [Download the Vitalik Model here](https://ollama.com/Harini_4623/Vitalik_Buterin)

5. **Configure device** for either **CPU** or **GPU**.

### Running the Application

Launch the application with:
```bash
streamlit run app.py
```

Then, navigate to **http://localhost:8501** in your browser to begin interacting with the **Vitalik Buterin Agent**.

---

## Interaction Modes

### 🎤 **Voice Chat**  
- Tap the **🎤 Voice Chat** button to speak directly to the agent.  
- The system will capture your speech, transcribe it, and respond in **Vitalik’s voice**.

### 💬 **Text Chat**  
- Type your questions into the input box for detailed, text-based responses.

---

## License

This project is licensed under the **MIT License**. For more details, see the [LICENSE](LICENSE) file.

---

**Unlock the insights of Ethereum’s co-founder, powered by AI. Engage with the Vitalik Agent now!**
