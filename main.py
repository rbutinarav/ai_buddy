import datetime
import streamlit as st
from openai_functions import ai_complete
from azure_functions import uploadToBlobStorage, listBlobs, text_to_speech, text_to_speech_st, detect_language, record_speech_to_text
from user_auth import user_login
from general_functions import get_env

# Define functions
def initialize_state():
    session_vars = [
        "conversation_history", "current_persona", "previous_persona",
        "reset_history", "question", "question_box", "load_document",
        "user_name", "login_success"
    ]
    for var in session_vars:
        if var not in st.session_state:
            st.session_state[var] = ""

def save_conversation():
    now = datetime.datetime.now()
    filename = f"Conversation_{st.session_state.current_persona}_{now.strftime('%Y-%m-%d_%H-%M')}.txt"
    uploadToBlobStorage("conversations",filename,st.session_state.conversation_history)
    st.write("Conversation saved in file", filename)

def handle_conversation_reset():
    if st.sidebar.button("Clear conversation"):
        st.session_state.conversation_history = ""
        st.experimental_rerun()

def handle_save_conversation():
    if st.sidebar.button("Save conversation"):
        save_conversation()

def handle_load_documents():
    if st.sidebar.button("Load documents"):
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            uploaded_file_name = uploaded_file.name
            with open(uploaded_file_name, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            uploadToBlobStorage(uploaded_file_name, uploaded_file_name)
            st.write("File uploaded to the server")
            st.session_state.load_document = False
        else:
            st.session_state.load_document = True

def handle_review_documents():
    if st.sidebar.button("List documents"):
        st.write("These are the last 50 conversations:\n",listBlobs(("conversations"), "", 50)) #currently not sorting by date

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

    return assigned_voice_id


# Initialize State
initialize_state()

def main():

    st.title("AI Buddy")

    #if environment variable AUTH = NO, bypass user login
    if get_env("LOGIN") == "NO":
        st.session_state.login_success = True
        st.session_state.user_name = "Guest" 
        st.write ("No login")
       
    #check if user is logged in

    if st.session_state.login_success == '':
        user_name, login_success = user_login()
        if login_success:
            st.session_state.login_success = login_success
            st.session_state.user_name = user_name
            st.write(user_name, "-", login_success)
            #rerun app
            st.experimental_rerun()
    
    elif st.session_state.login_success:
        st.write('Welcome: ', st.session_state.user_name)

        persona = st.sidebar.selectbox("Select a persona", ["", "Leonardo Da Vinci", "Albert Einstein", "Nelson Mandela", "Martin Luther King", "Jarvis", "Lady"])

        # Add a checkbox control to enable or disable voice
        use_voice = st.sidebar.checkbox("Use voice", value=False)
        use_voice_st = st.sidebar.checkbox("User voice st", value=False)
        listen = st.sidebar.checkbox("Listen", value=False)
        #add a sidebar.selectbox to choose the language
        if listen:
            language = st.sidebar.selectbox("Spoken language:",["English", "Italiano"])
            languages = {'English': 'en-US', 'Italiano': 'it-IT'}
            #assign a language code
            language_id = languages[language]


        context = f"This is a conversation between Me and {persona}."
        conversation_history = st.session_state.conversation_history

        if st.session_state.current_persona != persona:
            st.session_state.previous_persona = st.session_state.current_persona
            st.session_state.current_persona = persona

        if st.session_state.current_persona:
            st.write(f"You are talking with {st.session_state.current_persona}")
        else:
            st.write("Please select a persona from the sidebar")

        handle_conversation_reset()
        handle_save_conversation()

        if st.session_state.conversation_history != "":
            st.write(st.session_state.conversation_history)

        if st.session_state.current_persona:
            if listen:
                question = ""
                while question == "":
                    question = record_speech_to_text(language=language_id)

            else:
                question = st.text_input("Have anything to ask?", key="question_box")

            if persona != "" and question != "" and question != st.session_state.question:
                st.session_state.question = question

                prompt = f"{context}\n\n{conversation_history}\n\nMe: {question}\n\n"
                
                answer = ai_complete(prompt, max_tokens=100, temperature=0.7)

                answer_1 = answer.split("Me:")[0]
    
                # Update the conversation history
                st.session_state.conversation_history += f"\n\nMe: {question}\n\n{answer_1}"

                #st.write ("\n\nMe: ",question,"\n\n",answer_1)

                if use_voice:
                    #drop the {persona} from the answer
                    answer_2 = answer_1.split(": ")[1]
                    voice_type = assign_voice(persona, answer_2)
                    text_to_speech(answer_2, voice_type)
                    st.experimental_rerun()
                
                if use_voice_st:
                    #drop the {persona} from the answer
                    answer_2 = answer_1.split(": ")[1]
                    voice_type = assign_voice(persona, answer_2)
                    text_to_speech_st(answer_2, voice_type)
                
                else:
                    st.experimental_rerun()

        # Handle file uploading and document reviewing for Jarvis persona
        if st.session_state.current_persona == "Jarvis":
            st.write("Remember you can upload documents to the server and I will index them for you.")
            handle_load_documents()
            st.write("Remember you can also browse the documents already uploaded to the server.")
            handle_review_documents()


if __name__ == "__main__":
    main()