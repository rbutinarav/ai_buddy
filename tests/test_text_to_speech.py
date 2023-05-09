import streamlit as st
import sys
from azure_functions import text_to_speech, detect_language, text_to_speech_st
from openai_functions import ai_complete


def assign_voice(persona, text):

    voices = {'Leonardo Da Vinci - English': 'en-US-GuyNeural', 'Leonardo Da Vinci - Italian': 'it-IT-DiegoNeural',
            'Albert Einstein - English': 'en-US-GuyNeural', 'Albert Einstein - Italian': 'it-IT-DiegoNeural',
            'Nelson Mandela - English': 'en-US-GuyNeural', 'Nelson Mandela - Italian': 'it-IT-DiegoNeural',
            'Jarvis - English': 'en-US-GuyNeural', 'Jarvis - Italian': 'it-IT-DiegoNeural',
            'Lady - English': 'en-US-AriaNeural', 'Lady - Italian': 'it-IT-IsabellaNeural'}

    available_voices = list(voices.keys())

    #detect language from the text
    language = detect_language(text)

    languages_dictionary = {'it': 'Italian', 'en': 'English'}
    language_long = languages_dictionary[language]

    assigned_voice = persona + " - " + language_long
    assigned_voice_id = voices[assigned_voice]

    return assigned_voice_id, language_long


#ask user to input text
text = st.text_input("Enter text")

#ask the user to select the persona from a list of available personas
persona = st.selectbox("Select persona", ['Leonardo Da Vinci', 'Albert Einstein', 'Nelson Mandela', 'Jarvis', 'Lady'])

assigned_voice_id, language_long = assign_voice(persona, text)
assigned_voice_id2 = assign_voice(persona, text)   

st.write ("Detected language: ", language_long)

assigned_voice = persona + " - " + language_long

st.write ("Assigned voice: ", assigned_voice)
st.write ("Assigned voice id: ", assigned_voice_id)
st.write ("Assigned voice id2: ", assigned_voice_id2)

#text_to_speech_dev(text, assigned_voice_id, use_speaker=True)
text_to_speech_st (text, assigned_voice_id)
#text_to_speech(text, assigned_voice_id)

#make a revised text appling SSML tags
#context = 'Please apply SSML tags to the text: '
#full_text = context + text
#markup_text = ai_complete(full_text, max_tokens=100, api_type="azure", engine = "chat")

#st.write (full_text, markup_text)

#text_to_speech("This should sound more natural, as I applied some markup tags to the text", assigned_voice_id)

#text_to_speech(markup_text, assigned_voice_id, ssml=True)
