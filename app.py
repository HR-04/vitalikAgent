import streamlit as st
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.llms import Ollama
import base64
import voice


# ---------- Page Config ----------
st.set_page_config(
    page_title="Vitalik Agent",
    page_icon="🧠",
    layout="wide"
)

# ---------- Utilities ----------
def create_avatar(text, bg_color, text_color=(255, 255, 255)):
    img = Image.new('RGB', (200, 200), color=bg_color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)  # Get the bounding box
    text_width = bbox[2] - bbox[0]  # Calculate width
    text_height = bbox[3] - bbox[1]  # Calculate height
    draw.text(((200 - text_width) / 2, (200 - text_height) / 2), text, fill=text_color, font=font)
    return img

def pil_to_base64(img):
    import io
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# ---------- Load/Create Avatars ----------
def load_avatar(path, fallback_text, bg_color):
    try:
        img = Image.open(path)
    except:
        img = create_avatar(fallback_text, bg_color)
    return pil_to_base64(img)

eth_logo_base64 = load_avatar("img/eth.png", "ETH", (78, 42, 132))
user_logo_base64 = load_avatar("img/user.png", "USER", (73, 109, 137))

# Vitalik image for sidebar
try:
    vitalik_img = Image.open("img/vk3.jpg").resize((650, 400))
except:
    vitalik_img = create_avatar("VB", (46, 125, 50))
vitalik_img_base64 = pil_to_base64(vitalik_img)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        f'<div style="display: flex; justify-content: center; margin-bottom: 20px;">'
        f'<img src="data:image/png;base64,{vitalik_img_base64}" '
        f'style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover;"></div>',
        unsafe_allow_html=True
    )
    st.markdown("<h2 style='text-align: center; font-size: 20px;'>Vitalik Buterin</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; color: #666; font-size: 14px; line-height: 1.6;'>Ethereum Co-Founder and visionary behind the Ethereum blockchain. "
        "Shaping the future of decentralized applications and crypto-economics.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True, key="new_chat_button"):
        st.session_state.chat_history[st.session_state.current_chat] = st.session_state.messages.copy()
        st.session_state.current_chat = str(datetime.now().timestamp())
        st.session_state.messages = []
        StreamlitChatMessageHistory(key="langchain_messages").clear()
        st.session_state.chat_history = {}
        st.rerun()

    st.divider()

    voice_button = st.button("🎤   Voice Chat", key="voice_chat_button", use_container_width=True)
    if "is_listening" not in st.session_state:
        st.session_state.is_listening = False
    if voice_button:
        st.session_state.is_listening = not st.session_state.is_listening
        st.success("Voice Chat is now Active" if st.session_state.is_listening else "Voice Chat is now Inactive")

# ---------- Session State Init ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_chat" not in st.session_state:
    st.session_state.current_chat = str(datetime.now().timestamp())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {st.session_state.current_chat: []}

msgs = StreamlitChatMessageHistory(key="langchain_messages")

# ---------- LLM & Prompt ----------
llm = Ollama(model="vitalik-buterin-agent", temperature=0.7)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are Vitalik Buterin, co-founder of Ethereum. Respond to questions as Vitalik would, "
        "with technical depth, visionary thinking, and occasional humor. Focus on blockchain technology, "
        "Ethereum's roadmap, decentralization, and crypto-economics."
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}")
])

chain = prompt | llm
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="history"
)

# ---------- Main Display ----------
st.title("Vitalik Agent 🧠")
st.markdown("Your Co-founder, Co-thinker and conscience. Designed to build Civilization")

for message in st.session_state.messages:
    if message["role"] == "user":
        _, col = st.columns([0.7, 0.3])
        with col:
            with st.chat_message("user", avatar=f"data:image/png;base64,{user_logo_base64}"):
                st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar=f"data:image/png;base64,{eth_logo_base64}") :
            st.write(message["content"])
            if "latency" in message:
                st.caption(f"Response time: {message['latency']} ms")

# ---------- Voice Chat ----------
if st.session_state.is_listening:
    try:
        user_text = voice.record_and_transcribe()
    except Exception as e:
        st.error(f"Recording error: {str(e)}")
        user_text = None

    if user_text:
        st.session_state.messages.append({"role": "user", "content": user_text})
        msgs.add_user_message(user_text)

        _, col = st.columns([0.7, 0.3])
        with col:
            with st.chat_message("user", avatar=f"data:image/png;base64,{user_logo_base64}") :
                st.write(user_text)

        with st.chat_message("assistant", avatar=f"data:image/png;base64,{eth_logo_base64}") :
            with st.status("Vitalik Thinking 💭...", expanded=False) as status:
                start_time = time.time()
                try:
                    ai_reply = voice.generate_response(user_text)
                    latency = int((time.time() - start_time) * 1000)
                    voice.synthesize_voice(ai_reply)
                except Exception as e:
                    ai_reply = f"Error generating response: {str(e)}"
                    latency = 0

                st.session_state.messages.append({
                    "role": "assistant", "content": ai_reply, "latency": latency
                })
                msgs.add_ai_message(ai_reply)
                st.markdown(ai_reply)
                st.caption(f"Response time: {latency} ms")
                status.update(label="Thinking complete", state="complete", expanded=True)

                audio_base64 = voice.get_audio_base64()
                if audio_base64:
                    st.markdown(
                        f'<audio autoplay="true"><source src="data:audio/wav;base64,{audio_base64}" type="audio/wav"></audio>',
                        unsafe_allow_html=True
                    )

# ---------- Text ChatBot ----------
if prompt := st.chat_input("Ask me Anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    msgs.add_user_message(prompt)

    _, col = st.columns([0.7, 0.3])
    with col:
        with st.chat_message("user", avatar=f"data:image/png;base64,{user_logo_base64}") :
            st.write(prompt)

    with st.chat_message("assistant", avatar=f"data:image/png;base64,{eth_logo_base64}") :

        with st.status("Vitalik Thinking 💭...", expanded=True) as status:
            start_time = time.time()
            try:
                response = chain_with_history.invoke(
                    {"question": prompt},
                    config={"configurable": {"session_id": "any"}}
                )
                latency = int((time.time() - start_time) * 1000)
            except Exception as e:
                response = f"Error getting response: {str(e)}"
                latency = 0

            status.update(label="Thinking complete", state="complete", expanded=False)
        st.markdown(response)
        st.caption(f"Response time: {latency} ms")

        st.session_state.messages.append({
            "role": "assistant", "content": response, "latency": latency
        })
        msgs.add_ai_message(response)
