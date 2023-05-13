import pandas as pd
import json
import wave
import pyaudio
import streamlit as st
import os
import dotenv

def json_to_df (file_name):
    # Opening JSON file
    json_file = open(file_name)
    json_dict = json.load(json_file)
    json_df=pd.DataFrame(json_dict)
    #for i in json_dict:
    #    print(i['prompt'])
    # Closing file
    json_file.close()
    return json_df


def play_wav_file(wav_file):   #this function has to be tested
    CHUNK = 1024
    wf = wave.open(wav_file, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()


def get_env(env_name):
    dotenv.load_dotenv()
    #env_value = os.getenv(env_name)
    env_value = os.getenv(env_name)
    if env_value is None:
        #try .streamlit/secrets.toml file
        env_value = st.secrets[env_name]    
    return env_value
    





