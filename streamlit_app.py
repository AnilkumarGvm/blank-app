# pip install streamlit
# pip install audio-recorder-streamlit
# pip install openai

import os
import io
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from openai import OpenAI
from dotenv import load_dotenv
import wave

load_dotenv()  # take environment variables from .env.
API_KEY = os.getenv('API_KEY')

# def record_voice(output_filename, record_seconds, rate=44100):
#     print("Recording...")
#     # Record audio
#     audio_data = sd.rec(int(record_seconds * rate), samplerate=rate, channels=2, dtype='int16')
#     sd.wait()  # Wait for the recording to finish
#     print("Recording finished.")
#     # Save the recorded audio to a WAV file
#     write(output_filename, rate, audio_data)

def transcribe_text_to_voice(audio_location):
    client = OpenAI(api_key=API_KEY)
    audio_file= open(audio_location, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

def chat_completion_call(text):
    client = OpenAI(api_key=API_KEY)
    messages = [{"role": "user", "content": text}]
    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=messages)
    return response.choices[0].message.content


def text_to_speech_ai(speech_file_path, api_response):
    client = OpenAI(api_key=API_KEY)
    response = client.audio.speech.create(model="tts-1",voice="nova",input=api_response)
    response.stream_to_file(speech_file_path)



st.title("🧑‍💻 Gvm Voice Assistant Online 💬 ")

"""
Hi🤖 just click on the voice recorder and let me know how I can help you today?
"""

audio_data = audio_recorder()

audio_location = "audio/audio_file.wav"
# st.write(f"Audio data length: {len(audio_data) if audio_data else 0}")
# record_voice(audio_location, 5)
# if 1==1:
if audio_data:
    # st.write(f"Audio data length: {len(audio_data) if audio_data else 0}")
    # ##Save the Recorded File
    st.audio(audio_data, format="audio/wav")  # Play the recorded audio
    
    # # Convert the audio_data from bytes to raw format
    # audio_buffer = io.BytesIO(audio_data)
    # audio_bytes = audio_buffer.read()
    
    with open(audio_location, "wb") as wf:
        # wf.setnchannels(1)  # Mono audio
        # wf.setsampwidth(2)  # 16-bit audio
        # wf.setframerate(44100)  # Sampling rate
        # wf.writeframes(audio_bytes)
        wf.write(audio_data)
    
    #Transcribe the saved file to text
    text = transcribe_text_to_voice(audio_location)
    st.write(text)
    print(text)

    #Use API to get an AI response
    api_response = chat_completion_call(text)
    st.write(api_response)
    print(api_response)

    # Read out the text response using tts
    speech_file_path = 'audio/audio_response.mp3'
    text_to_speech_ai(speech_file_path, api_response)
    st.audio(speech_file_path)