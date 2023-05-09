import streamlit as st
from audio_recorder_streamlit import audio_recorder
import azure.cognitiveservices.speech as speechsdk
import os
import dotenv

dotenv.load_dotenv()

def record_speech_to_text_st():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    # Does not work on streamlit server

    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")
    
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    #speech_config.speech_recognition_language="en-US"
    speech_config.speech_recognition_language="it-IT"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    #show a button with "click to record your voice"
    voice_record = st.button("Click to record your voice")
    if voice_record:
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            text = speech_recognition_result.text
            st.write ("Recognized: {}".format(text))
            #print("Recognized: {}".format(speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            st.write("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
            #print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


def speech_to_text(audio_file, language="it-IT"):
    subscription_key = os.getenv("AZURE_COGNITIVE_SERVICES_KEY")
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")
    
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_recognition_language=language

    audio_config = speechsdk.AudioConfig(filename=audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = speech_recognition_result.text
    
    else:
        text = ""

    return text



audio_bytes = audio_recorder()
#plays back audio recorded
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
#converts audio to text
#write audio_bytes to a file called "speech.wav"
if audio_bytes is not None:
    with open("speech.wav", "wb") as f:
        f.write(audio_bytes)

    text = speech_to_text("speech.wav")
    st.write('This is what you said: ', text)
