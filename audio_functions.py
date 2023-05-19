import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speechsdk
from audio_recorder_streamlit import audio_recorder
import datetime
from general_functions import get_env
import io

def record_speech_to_text(language="it-IT"):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    # Does not work on streamlit server

    text =""

    subscription_key = get_env("AZURE_COGNITIVE_SERVICES_KEY")
    region = get_env("AZURE_COGNITIVE_SERVICES_REGION")
    
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    #speech_config.speech_recognition_language="en-US"
    speech_config.speech_recognition_language=language

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = speech_recognition_result.text

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        text = ""

    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    return text


def audio_recorder_st(): #to be tested
    ##this works both locally and on streamlit server    
    audio_bytes = audio_recorder()
    return audio_bytes


def wave_to_text(wave_file, language="it-IT"): #to be tested
    text = ""
    
    subscription_key = get_env("AZURE_COGNITIVE_SERVICES_KEY")
    region = get_env("AZURE_COGNITIVE_SERVICES_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_recognition_language = language

    audio_config = speechsdk.audio.AudioConfig(filename=wave_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = speech_recognition_result.text

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        text = ""

    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    
    return text


def wave_stream_to_text(wave_stream, language="it-IT"): #to be tested
    text = ""
    
    subscription_key = get_env("AZURE_COGNITIVE_SERVICES_KEY")
    region = get_env("AZURE_COGNITIVE_SERVICES_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_recognition_language = language

    audio_config = speechsdk.audio.AudioConfig(stream=wave_stream)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = speech_recognition_result.text

    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        text = ""

    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    
    return text





def detect_language(text):

    subscription_key = get_env("AZURE_COGNITIVE_SERVICES_KEY")
    endpoint = get_env("AZURE_COGNITIVE_SERVICES_ENDPOINT")

    # Create the Text Analytics client
    client = TextAnalyticsClient(endpoint, AzureKeyCredential(subscription_key))

    # Perform language detection
    response = client.detect_language(documents=[text])[0]

    # Get the detected language
    detected_language = response.primary_language.iso6391_name

    return detected_language


def text_to_speech(text, voicetype="it-IT-IsabellaNeural", ssml=False):
#this is the regular text to speech function, that unfortunately does not work with streamlit server
#so we made a modified version called text_to_speech_st
    subscription_key = get_env("AZURE_COGNITIVE_SERVICES_KEY")
    region = get_env("AZURE_COGNITIVE_SERVICES_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voicetype

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    if ssml == False:
        result = speech_synthesizer.speak_text_async(text).get()
    else:
        result = speech_synthesizer.speak_ssml_async(text).get() ##currently not working properly

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Text-to-speech synthesis completed.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Text-to-speech synthesis was canceled.")


def text_to_speech_st(text, voicetype="it-IT-IsabellaNeural"):
#modified version to first create a wave file and the play it to solve libraries issues with stramlit
    
    subscription_key = get_env("AZURE_COGNITIVE_SERVICES_KEY")
    region = get_env("AZURE_COGNITIVE_SERVICES_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voicetype

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = speech_synthesizer.speak_text_async(text).get()
    stream = speechsdk.AudioDataStream(result)

    #create a date-time-stamped
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    #create a unique filename for audio file using datetime
    #filename = "audio_files/audio_file_"+timestamp+".wav"
    filename = "audio_file_"+timestamp+".wav"
    stream.save_to_wav_file(filename) #syncrhonously

    #play file
    st.audio (filename, format='audio/wav', start_time=0)
