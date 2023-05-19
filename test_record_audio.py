from audio_functions import audio_recorder_st, wave_to_text, detect_language, wave_stream_to_text
import streamlit as st

#open and load the audio file
wave = audio_recorder_st()

#write the wave file to test.wav
with open("test.wav", "wb") as f:
    f.write(wave)

result = wave_to_text("test.wav", language="it-IT")
st.write(result)
