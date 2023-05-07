from azure_functions import uploadToBlobStorage, listBlobs, getBlob
from user_auth import create_user, get_user, modify_user, user_login, add_user
import streamlit as st
import json

st.write("This app is still experimental, if you need a user_id, please contact the administrator: roberto.butinar@gmail.com")

user_name=st.text_input("Enter user name")
user_password=st.text_input("Enter user password")
#add user button
if st.button("Login"):
    #check if the user exists and the password is correct
    user = get_user(user_name)

    if user:
        st.write(user)
    
    else:
        st.write("User not found")