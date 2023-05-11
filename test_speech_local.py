import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import os
import dotenv
import time
from openai_functions import ai_complete

dotenv.load_dotenv()

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
    return text


def listen_continuous_speech(language="it-IT"):
    subscription_key = st.secrets["AZURE_COGNITIVE_SERVICES_KEY"]
    region = os.getenv("AZURE_COGNITIVE_SERVICES_REGION")

    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_recognition_language = language

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)




#inizialized state
if "text" not in st.session_state:
    st.session_state["text"] = ""

st.write(st.session_state["text"])

text = record_speech_to_text()

context = "This is conversation with a friendly bot, ironic and a little crazy, it likes to tease and have fun."
full_prompt = context + st.session_state["text"] + '\n Me:' + text

answer = ai_complete(full_prompt, temperature=1)

st.session_state["text"] = st.session_state["text"] + text + "\n Me:" + answer


#run again the experiment
st.experimental_rerun()



