def uploadToBlobStorage(file_path,file_name):

    #import the libraries for managing the azure blob storage
    from azure.storage.blob import BlobServiceClient

    #load env variables from .env file
    import dotenv
    import os
    dotenv.load_dotenv()
    container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

    #add env variables from .secrets.toml file
    import streamlit
    #storage_account_key = streamlit.secrets["AZURE_STORAGE_KEY"]
    connection_string = streamlit.secrets["AZURE_STORAGE_CONNECTION_STRING"]

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

#uploadToBlobStorage("azure_functions.py","azure_functions.py")
