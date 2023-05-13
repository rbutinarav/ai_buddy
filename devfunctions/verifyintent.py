#let's detect if the user is asking something specific to be done
#we will use the intent classifier to detect the intent

from openai_functions import ai_complete

def get_intent(text):
    intents = {[]}