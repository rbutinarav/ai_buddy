import streamlit as st
from azure_functions import listBlobs, getBlob, uploadToBlobStorage
import json
import datetime

#backend functions

def create_user(user_name, user_email, user_full_name, user_password, user_role):  #user_name and email should match by design
    #create a json file, name of the json is the user_email
    user_dict = {"email": user_email, "full_name": user_full_name, "password": user_password, "role": user_role}
    user = json.dumps({user_name: user_dict})    
    #create a file with the user information
    uploadToBlobStorage("users", user_name+".json", str(user))

    return

def get_user(user_name):
    #get the user information from the json file
    user = getBlob("users", user_name+".json")
    #user_json = json.loads(user.content_as_text())
    #return user_json
    return user

def modify_user():
    return

def log_user_access(user_name, login_success):
    #create a json file, name of the json is the user_email + timestamp + login_success
    timestamp = datetime.datetime.now()
    #convert timestamp to string
    timestamp = timestamp.strftime("%Y%m%d%H%M%S")
    user_dict = {"user_name": user_name, "login_success": login_success, "timestamp": timestamp}
    blob_name = user_name + "_" + str(timestamp) + "_" + str(login_success) + ".json"
    user = json.dumps({user_name: user_dict})
    uploadToBlobStorage("logins", blob_name, str(user))
    return

## interactive function

def user_login():
    #ask for user name and password
    st.write("Welcome, please enter your credentials:")
    user_name=st.text_input("Enter user name")
    user_password=st.text_input("Enter user password")
    #add user button
    if st.button("Login"):
        #check if the user exists and the password is correct
        user = get_user(user_name)
        if user:
            user_json = json.loads(user.content_as_text())
            if user_json[user_name]["password"] == user_password:
                st.write("User logged in")
                log_user_access(user_name, "success")
            else:
                st.write("Wrong user or password")
                log_user_access(user_name, "fail")
    return

def add_user():
    return
