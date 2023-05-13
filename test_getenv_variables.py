from general_functions import get_env
import streamlit as st
#import dotenv
import os
import dotenv

dotenv.load_dotenv()

# load env variables from .env file
#container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
container_name = get_env("AZURE_STORAGE_CONTAINER_NAME")

# add env variables from .secrets.toml file
#connection_string = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
connection_string = get_env("AZURE_STORAGE_CONNECTION_STRING")


print (container_name)
print (connection_string)


