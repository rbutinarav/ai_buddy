import streamlit as st
import sys
from azure_functions import text_to_speech, detect_language, text_to_speech_dev
from azure_functions_dev import text_to_speech_dev
from openai_functions import ai_complete

#ask user to input text
text = st.text_input("Enter text")

#ask user to select a voice from a list of available voices
#make a dictionary of available voices
#for each combination of persona and language, there is a voice
#list of available personas: Leonardo Da Vinci, Albert Einstein, Nelson Mandela, Jarvis
#list of available languages: English, Italian
#list of available voices: Leonardo Da Vinci - English, Leonardo Da Vinci - Italian, Albert Einstein - English, Albert Einstein - Italian, Nelson Mandela - English, Nelson Mandela - Italian, Jarvis - English, Jarvis - Italian

#make a new dictionary taking this list of available voices
#it-IT-IsabellaNeural (Female)
#it-IT-DiegoNeural (Male)
#en-US-AriaNeural (Female)
#en-US-GuyNeural (Male)
#en-US-JennyNeural (Female)
voices = {'Leonardo Da Vinci - English': 'en-US-GuyNeural', 'Leonardo Da Vinci - Italian': 'it-IT-DiegoNeural',
          'Albert Einstein - English': 'en-US-GuyNeural', 'Albert Einstein - Italian': 'it-IT-DiegoNeural',
          'Nelson Mandela - English': 'en-US-GuyNeural', 'Nelson Mandela - Italian': 'it-IT-DiegoNeural',
          'Jarvis - English': 'en-US-GuyNeural', 'Jarvis - Italian': 'it-IT-DiegoNeural',
          'Lady - English': 'en-US-AriaNeural', 'Lady - Italian': 'it-IT-IsabellaNeural'}

#make a new

#make a list of available voices
available_voices = list(voices.keys())

#ask the user to select the persona from a list of available personas
persona = st.selectbox("Select persona", ['Leonardo Da Vinci', 'Albert Einstein', 'Nelson Mandela', 'Jarvis', 'Lady'])

#detect language from the text
language = detect_language(text)

languages_dictionary = {'it': 'Italian', 'en': 'English'}
language_long = languages_dictionary[language]

st.write ("Detected language: ", language_long)

assigned_voice = persona + " - " + language_long
assigned_voice_id = voices[assigned_voice]

st.write ("Assigned voice: ", assigned_voice)
st.write ("Assigned voice id: ", assigned_voice_id)

#text_to_speech_dev(text, assigned_voice_id, use_speaker=True)
text_to_speech_dev (text, assigned_voice_id, use_speaker=False)
text_to_speech(text, assigned_voice_id)

#make a revised text appling SSML tags
#context = 'Please apply SSML tags to the text: '
#full_text = context + text
#markup_text = ai_complete(full_text, max_tokens=100, api_type="azure", engine = "chat")

#st.write (full_text, markup_text)

#text_to_speech("This should sound more natural, as I applied some markup tags to the text", assigned_voice_id)

#text_to_speech(markup_text, assigned_voice_id, ssml=True)





