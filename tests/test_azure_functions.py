from azure_functions import uploadToBlobStorage, listBlobs, getBlob
from user_auth import create_user, get_user, modify_user, user_login, add_user
import streamlit as st
import json

#input test with streamlit
#text = st.text_input("Enter text to load to blob storage")
#folder = st.text_input("Enter text folder where to store the text")
#uploadToBlobStorage(folder, "tests.txt", text)

#st.write(listBlobs(blob_path=folder, return_string=True))


#folder_load = st.text_input("Enter text folder where to find the blob")

#st.write(listBlobs(blob_path=folder_load))

#text_load = st.text_input("Enter blob name to load from blob storage")

#blob = getBlob(blob_path=folder_load, blob_name=text_load)
#blob_json = json.loads(blob.content_as_text())


#st.write(getBlob(blob_path=folder_load, blob_name=text_load))

#name = blob_json["role"]

#st.write ('role: ', name)

#ask for user name, email, password and role
name=st.text_input("Enter user name")
full_name=st.text_input("Enter user full name")
email=st.text_input("Enter user email")
password=st.text_input("Enter user password")
role=st.text_input("Enter user role")

#add user button
if st.button("Add user"):
    create_user(name, email, full_name, password, role)
    st.write("User added")

#check if user has been added
if st.button("Check user"):
    user = get_user(name)
    st.write("User: ", user)


#ask for user name, email, password and role
#name=st.text_input("Enter user name")
#email=st.text_input("Enter user email")

#check if user exists
#if st.button("Check user"):
#    user = get_user(name)

st.write(user)

user_json = json.loads(user.content_as_text())
st.write(user_json)
#st.write(user[name]["password"])