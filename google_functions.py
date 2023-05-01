import dotenv
import os
import streamlit as st
import requests
import io
from pydub import AudioSegment
from pydub.playback import play

dotenv.load_dotenv()


def text_to_speech(text = "Hello World!", languageCode = "en-US", name = "en-US-Wavenet-A", action="stream", audioEncoding = "MP3"):

    # Set up authentication
    api_key = st.secrets["GOOGLE_API_KEY"]

    # Set up the API endpoint URL
    url = os.getenv("GOOGLE_COGNITIVE_SERVICES_ENDPOINT") # "https://texttospeech.googleapis.com/v1/text:synthesize"

    # Set up the request headers
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    }

    # Set up the request data
    data = {
    "input": {"text": text},
    "voice": {"languageCode": languageCode, "name": name},
    "audioConfig": {"audioEncoding": audioEncoding},
    }

    # Make the API request
    response = requests.post(url, headers=headers, json=data)

    # Get the binary audio data from the response
    audio_data = io.BytesIO(response.content)

    if action == "stream":
        # Load the audio data into a PyDub AudioSegment object
        audio_segment = AudioSegment.from_file(audio_data, format="mp3")

        # Play the audio using PyDub
        play(audio_segment)

    elif action == "save":
        # Save the audio data to an MP3 file
        with open("audio.mp3", "wb") as audio_file:
            audio_file.write(audio_data.read())
        st.write("Audio saved to audio.mp3")

##CURRENTLY NO GOOGLE SECRETS HAVE BEEN PROVIEDED, FUNCTION IS NOT WORKING





    