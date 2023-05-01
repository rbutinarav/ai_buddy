import dotenv
import os
import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import azure.cognitiveservices.speech as speechsdk
import azure.cognitiveservices.speech.audio as audio

dotenv.load_dotenv()


def uploadToBlobStorage(file_path,file_name):

    #import the libraries for managing the azure blob storage
    from azure.storage.blob import BlobServiceClient

    #load env variables from .env file
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    #add env variables from .secrets.toml file
    import streamlit
    #storage_account_key = streamlit.secrets["AZURE_STORAGE_KEY"]
    connection_string = streamlit.secrets["AZURE_STORAGE_CONNECTION_STRING"]

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

#uploadToBlobStorage("azure_functions.py","azure_functions.py")


def listBlobs():
    #import the libraries for managing the azure blob storage


    #load env variables from .env file
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    #add env variables from .secrets.toml file
    import streamlit
    #storage_account_key = streamlit.secrets["AZURE_STORAGE_KEY"]
    connection_string = streamlit.secrets["AZURE_STORAGE_CONNECTION_STRING"]

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blob_list = container_client.list_blobs()
    for blob in blob_list:
        st.write("t" + blob.name)


def text_to_speech(text, voicetype="it-IT-IsabellaNeural"):
    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
 
    speech_config.speech_synthesis_voice_name = voicetype

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Text-to-speech synthesis completed.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Text-to-speech synthesis was canceled.")




def text_to_speech_audio(text, voicetype="it-IT-IsabellaNeural"):
    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_synthesis_voice_name = voicetype

    audio_config = audio.AudioOutputConfig(use_default_speaker=True)

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Text-to-speech synthesis completed.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Text-to-speech synthesis was canceled.")
       


def detect_language(text):

    dotenv.load_dotenv()
    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    endpoint = os.getenv("AZURE_COGNITIVE_SERVICES_ENDPOINT")

    # Create the Text Analytics client
    client = TextAnalyticsClient(endpoint, AzureKeyCredential(subscription_key))

    # Perform language detection
    response = client.detect_language(documents=[text])[0]

    # Get the detected language
    detected_language = response.primary_language.iso6391_name

    return detected_language


text_to_speech_audio("Ciao, come stai?")
text_to_speech("Ciao, come stai?")



    