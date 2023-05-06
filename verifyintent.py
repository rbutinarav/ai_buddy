#let's detect if the user is asking something specific to be done
#we will use the intent classifier to detect the intent

import streamlit as st
import openai
from openai_functions import ai_complete

#authenticate to OpenAI
openai.api_key = st.secrets["OPENAI_KEY"]

#ask the user to input a question
question = st.text_input("Enter a question")

if question:
    #classify the intent
    #full_question = "Text: Play a song\nIntent: play_song\nText: what's the best food for my cat\nIntent: search_reviews\nText: How are you?\nIntent: other\nText: " + question
    
    full_question = "Detect if intent is: search_review, get_time, play_song, other.\n\What's the best food for my cat?\nIntent: search_review\n" + question + "\nIntent: "
    intent = ai_complete(full_question, verbose=False)
    st.write("Intent: ", intent)

  