import streamlit as st
from audio_recorder_streamlit import audio_recorder
import azure.cognitiveservices.speech as speechsdk
import os
import requests
import dotenv

dotenv.load_dotenv()

def speech_to_text():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")
    
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    #speech_config.speech_recognition_language="en-US"
    speech_config.speech_recognition_language="it-IT"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

#speech_to_text()

def speech_to_text_st():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"

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

def speech_play_audio():
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")

speech_play_audio



#st.write("Click the button below to transcribe the audio")
#if st.button("Transcribe"):
#    st.write("Transcribing...")
#    wav_to_text("audio_files/audio_file_2023-05-09-10-35-21.wav")
#    st.write("Done!")

