from azure_functions import uploadToBlobStorage, listBlobs, getBlob
from user_auth import create_user, get_user, modify_user, user_login, add_user
import streamlit as st
import json

#user_login()
#user_name = user_login()
#initialize st.session_state.login_success
if "login_success" not in st.session_state:
    st.session_state.login_success = None
if st.session_state.login_success is None:
    user_name, login_success = user_login()
    if login_success:
        st.session_state.login_success = login_success
        st.session_state.user_name = user_name
        st.write(user_name, "-", login_success)
        #rerun app
        st.experimental_rerun()
    
elif st.session_state.login_success:
    st.write('The app continues... only if login is successful')

elif not st.session_state.login_success == False:
    st.write('Login uccessful')
