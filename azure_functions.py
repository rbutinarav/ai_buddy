import dotenv
import os
import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
import azure.cognitiveservices.speech as speechsdk
import datetime

dotenv.load_dotenv()


def uploadToBlobStorage(blob_path, blob_name, file_contents):

    # load env variables from .env file
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    # add env variables from .secrets.toml file
    connection_string = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path+"/"+blob_name)

    # Upload the file contents directly to blob storage
    blob_client.upload_blob(file_contents, blob_type="BlockBlob", overwrite=True)



def listBlobs(blob_path, filter="", max_results=10, return_string=False):
    
    # load env variables from .env file
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    # add env variables from .secrets.toml file
    connection_string = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blob_list = container_client.list_blobs(prefix=blob_path)
    blob_path_filter = blob_path + "/" + filter

    filtered_list = [blob.name for blob in blob_list if blob.name.startswith(blob_path_filter)]

    #remove the path from the list
    filtered_list = [blob.split("/")[-1] for blob in filtered_list]

    filtered_list = filtered_list[:max_results]

    if return_string:
        filtered_list = ("\n".join(filtered_list))  ##not adding properly the new line

    return filtered_list


def getBlob(blob_path, blob_name):
    
    # load env variables from .env file
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    # add env variables from .secrets.toml file
    connection_string = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
   
    # Get the BlobClient for the specified blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path+"/"+blob_name)

    # Download the content of the blob
    try:
        blob_content = blob_client.download_blob()
    except:
        blob_content = False
        
    return blob_content


def text_to_speech(text, voicetype="it-IT-IsabellaNeural", ssml=False):
#this is the regular text to speech function, that unfortunately does not work with streamlit server
#so we made a modified version called text_to_speech_st
    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")

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


def detect_language(text):

    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    endpoint = os.getenv("AZURE_COGNITIVE_SERVICES_ENDPOINT")

    # Create the Text Analytics client
    client = TextAnalyticsClient(endpoint, AzureKeyCredential(subscription_key))

    # Perform language detection
    response = client.detect_language(documents=[text])[0]

    # Get the detected language
    detected_language = response.primary_language.iso6391_name

    return detected_language


def text_to_speech_st(text, voicetype="it-IT-IsabellaNeural"):
#modified version to first create a wave file and the play it to solve libraries issues with stramlit
    
    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")

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


def record_speech_to_text(language="it-IT"):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    # Does not work on streamlit server

    text =""

    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")
    
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

