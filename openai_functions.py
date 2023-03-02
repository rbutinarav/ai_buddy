#%%
def ai_complete(prompt='Hello', model='text-davinci-003', temperature=0.2, max_tokens=30, verbose=False):
    """
    Returns a string with the completion of the prompt
    """
    import openai
    
    #LOAD ENV VARIABLES (secrets)
    import streamlit as st
    openai.api_key = st.secrets["OPENAI_KEY"]

    response = openai.Completion.create(model=model, prompt=prompt, temperature=temperature, max_tokens=max_tokens)
    #print(type(response))  
    response_text = response['choices'][0]['text'] #parse text (prompt completion)
    if verbose == True:
        return prompt, response_text
    return response_text

def ai_model_list ():
    """
    Get the model list from openai
    """
    import os
    import openai
    from dotenv import load_dotenv

    #LOAD ENV VARIABLES - this is commented for use in streamlit
    #load_dotenv()
    #openai.api_key = os.getenv('OPENAI_KEY')

    #LOAD ENV VARIABLES - for streamlit
    import streamlit as st
    openai.api_key = st.secrets["OPENAI_KEY"]
    
    output = openai.Model.list()

    return (output)


#EXAMPLES
#print(ai_complete("Il migliore amico dell'uomo è", verbose=False))

#print(ai_model_list())

