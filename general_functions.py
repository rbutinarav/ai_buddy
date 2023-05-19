import pandas as pd
import streamlit as st
import os
import dotenv


def get_env(env_name):
    dotenv.load_dotenv()
    env_value = os.getenv(env_name)
    if env_value is None:
        env_value = st.secrets[env_name]    
    return env_value
    





