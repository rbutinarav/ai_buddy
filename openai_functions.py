#%%
def ai_complete(prompt='Hello', model='text-davinci-003', engine="gpt-35-turbo", temperature=0.7, max_tokens=30, verbose=False, api_type="azure"):
    """
    Returns a string with the completion of the prompt
    engine must match the deployment name on Azure
    engine="gpt-35-turbo" is more verbose and conversational
    engine="chat" is more concise and factual - chat should be renamed in text-davinci-003
    """
    import openai
    import streamlit as st
    
    import os
    
    from dotenv import load_dotenv
    load_dotenv()
    
    if api_type == "azure":
        openai.api_type = "azure"
        openai.api_key = st.secrets["AZURE_OPENAI_KEY"]
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai.api_version = "2023-03-15-preview"   

        response_json = openai.Completion.create(engine=engine, prompt=prompt, temperature=temperature, max_tokens=max_tokens) #this works with Azure OpenAI
 
 
    else :    
        openai.api_key = st.secrets["OPENAI_KEY"]
        response_json = openai.Completion.create(model=model, prompt=prompt, temperature=temperature, max_tokens=max_tokens) #this works with OpenAI
    
    response_text = response_json['choices'][0]['text'] #parse text (prompt completion)

    if verbose == True:
        return prompt, response_text
    return response_text




