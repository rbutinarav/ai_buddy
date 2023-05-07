from azure_functions import uploadToBlobStorage, listBlobs, getBlob
import streamlit as st
import json

#input test with streamlit
#text = st.text_input("Enter text to load to blob storage")
#folder = st.text_input("Enter text folder where to store the text")
#uploadToBlobStorage(folder, "tests.txt", text)

#st.write(listBlobs(blob_path=folder, return_string=True))


folder_load = st.text_input("Enter text folder where to find the blob")

st.write(listBlobs(blob_path=folder_load))

text_load = st.text_input("Enter blob name to load from blob storage")

blob = getBlob(blob_path=folder_load, blob_name=text_load)
blob_json = json.loads(blob.content_as_text())


st.write(getBlob(blob_path=folder_load, blob_name=text_load))

name = blob_json["role"]

st.write ('role: ', name)