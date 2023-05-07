import streamlit as st
from azure_functions import listBlobs, getBlob, uploadToBlobStorage


#backend functions

def create_user(user_name, user_email, user_password, user_role):
    #create a json file with the user information, one level json
    user = {user_name: {"email": user_email, "password": user_password, "role": user_role}}
        
    #create a file with the user information
    uploadToBlobStorage("users", user_name+".json", str(user))

    return

def get_user():
    return

def modify_user():
    return

## interactive function

def user_login():
    return

def add_user():
    return
