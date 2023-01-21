##run this file to start the program
##will create an interative window with streamlit
##user will be able to chat with the bot, ask information
##the bot will answer searching for specific contents stored in a database
##made of documents indexed by OpenAI using embeddings


##print "hello world" on a web page with streamlit
# %%
import streamlit as st
from openai_functions import ai_complete #import ai_complete: returns a string with the completion of the prompt

# Initialize State on first run
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = ""
if "current_persona" not in st.session_state:
    st.session_state.current_persona = ""
if "previous_persona" not in st.session_state:
    st.session_state.previous_persona = ""
if "reset_history" not in st.session_state:
    st.session_state.reset_history = False
if "question" not in st.session_state:
    st.session_state.question = ""
if "question_box" not in st.session_state:
    st.session_state.question_box = ""

# Intialize other variables

question = st.empty()
current_persona = ""

#DEFINED FUNCTIONS
## this trigger OpenAI response
def openai_conversation(context, question):
    answer = ai_complete(context+question, max_tokens=100)
    return answer

#this print text on the web page with streamlit with the proper format for "\n"
def st_write(text):
    new_text=text.replace("\n", "  \n")
    st.write(new_text)
    return

#MAIN LOOP
st.title("Open AI chatbot")

#1.SELECT A PERSONA TO TALK TO
persona = st.sidebar.selectbox("Select a persona", ["", "Leonardo Da Vinci", "Albert Einstein", "Nelson Mandela", "Martin Luther King", "Jarvis"])

#check if the user has selected a new persona
if st.session_state.current_persona != persona:
    st.session_state.previous_persona = st.session_state.current_persona
    st.session_state.current_persona = persona
    #question = st.empty()

st.write("You are talking with", st.session_state.current_persona)
st.write("You were talking with", st.session_state.previous_persona)


#2.WANT TO SEE THE FULL CONVERSATION HISTORY?

#show_history= st.sidebar.checkbox("Show history", value=True)
conversation_reset = st.sidebar.button("Clear conversation")
save_conversation = st.sidebar.button("Save conversation")

if st.session_state.conversation_history != "":
    st_write(st.session_state.conversation_history)

if conversation_reset:
    st.session_state.conversation_history = ""
    st.experimental_rerun()

if save_conversation:
#save the conversation in a file adding Persona and time stamp to the name
    import datetime
    now = datetime.datetime.now()
    filename = "Conversation " + st.session_state.current_persona + " " + now.strftime("%Y-%m-%d_%H-%M") + ".txt"
#replace spaces with underscores
    filename = filename.replace(" ", "_")
    f = open("documents/"+filename, "w")
    f.write(st.session_state.conversation_history)
    f.close()
    st.write("Conversation saved in file", filename)

#3.HAS THE USER ASKED A QUESTION?

if st.session_state.current_persona != "":
    question = st.text_input("Have anything to ask?", key="question_box")
 
else:
    st.write("Please select a persona from the sidebar")

if persona != "" and question != "" and question != st.session_state.question:
    st.session_state.question = question
    if st.session_state.conversation_history == "":
        full_context = "You are talking with "+persona+"\n"+ "You: "
    else:
        full_context = st.session_state.conversation_history+"\n \n"+"You: "
    #st_write("FUll CONTEXT: "+full_context)
    full_question=question+"\n"+persona+": "
    answer=openai_conversation(context=full_context,question=full_question)
    #delete the first 1 characters of the answer
    answer=answer[1:]
    st_write(answer)

    #update the conversation history
    st.session_state.conversation_history = st.session_state.conversation_history + "\n \n" + "You: " + question + "\n" + persona + ": " + answer
    #st.write("CONVERSATION HISTORY: ", st.session_state.conversation_history)
    st.experimental_rerun()

    #version 2.1 test