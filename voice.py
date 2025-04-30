# import os
import base64
# import threading
import requests
import numpy as np
import torch
import pyaudio
import soundfile as sf
import whisper
from faster_whisper import WhisperModel
from inference import generate_cloned_voice  

# ========== Config ========== 
MODEL_SIZE = "base.en"
DEVICE = "cpu"
LLM_ENDPOINT = "http://localhost:11434/api/generate"
INPUT_FILE = "input.wav"
OUTPUT_FILE = "output.wav"
REFERENCE_AUDIO = "reference_audio/vb.wav"

# ========== Initialization ========== 
whisper_model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type="int8")
audio_interface = pyaudio.PyAudio()

# ========== Audio Recording ========== 
def record_audio(filename=INPUT_FILE, duration=5):
    """Records audio from microphone and saves to file."""
    RATE, CHUNK = 22050, 1024
    FORMAT, CHANNELS = pyaudio.paInt16, 1

    stream = audio_interface.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = [
        np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        for _ in range(int(RATE / CHUNK * duration))
    ]

    stream.stop_stream()
    stream.close()

    raw_audio_data = np.hstack(frames)
    sf.write(filename, raw_audio_data, RATE)

# ========== Transcription ========== 
def transcribe_with_whisper(audio_file_path):
    """Transcribes audio using Whisper."""
    model = whisper.load_model("base.en")
    result = model.transcribe(audio_file_path)
    return result["text"]

# ========== LLM Querying ========== 
def query_ollama(prompt):
    """Sends prompt to local LLM API and returns the response."""
    prompt = f"""provide a detailed answer to the following question: {prompt}"""

    response = requests.post(
        LLM_ENDPOINT,
        json={
            "model": "vitalik-buterin-agent",
            "prompt": prompt,
            "stream": False,
            "max_tokens": 100
        }
    )

    if response.ok:
        return response.json().get("response", "").strip()

    return "Sorry, I couldn't process that."

# ========== Record and transcribe ========== 
def record_and_transcribe():
    """Records audio and returns transcribed text."""
    try:
        record_audio()
        return transcribe_with_whisper(INPUT_FILE)
    except Exception as e:
        print(f"Recording/transcription error: {str(e)}")
        return None

# ========== LLM Response ========== 
def generate_response(prompt):
    """Generates a response from the LLM."""
    try:
        return query_ollama(prompt)
    except Exception as e:
        print(f"LLM error: {str(e)}")
        return "Sorry, I encountered an error processing your request."

# ========== Audio to Base64 ========== 
def get_audio_base64():
    """Encodes the generated audio file as a base64 string."""
    try:
        with open(OUTPUT_FILE, "rb") as f:
            audio_bytes = f.read()
        return base64.b64encode(audio_bytes).decode()
    except Exception as e:
        print(f"Error reading audio file: {str(e)}")
        return None

# ========== Voice Synthesis ========== 
def synthesize_voice(text):
    """Synthesizes speech from text using cloned voice."""
    try:
        generate_cloned_voice(text, REFERENCE_AUDIO, OUTPUT_FILE)
        return True
    except Exception as e:
        print(f"Voice synthesis error: {str(e)}")
        return False

# ========== Play Audio ========== 
def play_audio():
    """Plays the generated audio file."""
    try:
        data, samplerate = sf.read(OUTPUT_FILE, dtype='int16')
        stream = audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=samplerate,
            output=True
        )
        stream.write(data.tobytes())
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Audio play error: {str(e)}")

# ========== Main Voice chat Loop ========== 
def voice_chat_start():
    print("Voice chat started. Speak to interact.")
    while True:
        record_audio()
        user_text = transcribe_with_whisper(INPUT_FILE)

        if not user_text.strip():
            continue

        print(f"User said: {user_text}")

        ai_reply = query_ollama(user_text)

        if synthesize_voice(ai_reply):
            play_audio()

        return user_text, ai_reply
