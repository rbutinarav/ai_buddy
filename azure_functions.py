import streamlit as st
from azure.storage.blob import BlobServiceClient
from general_functions import get_env


def uploadToBlobStorage(blob_path, blob_name, file_contents):

    # load env variables from .env file
    container_name = get_env("AZURE_STORAGE_CONTAINER_NAME")

    # add env variables from .secrets.toml file
    connection_string = get_env("AZURE_STORAGE_CONNECTION_STRING")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path+"/"+blob_name)

    # Upload the file contents directly to blob storage
    blob_client.upload_blob(file_contents, blob_type="BlockBlob", overwrite=True)



def listBlobs(blob_path, filter="", max_results=10, return_string=False):
    
    # load env variables from .env file
    container_name = get_env("AZURE_STORAGE_CONTAINER_NAME")

    # add env variables from .secrets.toml file
    connection_string = get_env("AZURE_STORAGE_CONNECTION_STRING")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    blob_list = container_client.list_blobs(prefix=blob_path)
    blob_path_filter = blob_path + "/" + filter

    filtered_list = [blob.name for blob in blob_list if blob.name.startswith(blob_path_filter)]

    #remove the path from the list
    filtered_list = [blob.split("/")[-1] for blob in filtered_list]

    filtered_list = filtered_list[:max_results]

    if return_string:
        filtered_list = ("\n".join(filtered_list))  ##not adding properly the new line

    return filtered_list


def getBlob(blob_path, blob_name):
    
    # load env variables from .env file
    container_name = get_env("AZURE_STORAGE_CONTAINER_NAME")

    # add env variables from .secrets.toml file
    connection_string = get_env("AZURE_STORAGE_CONNECTION_STRING")

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
   
    # Get the BlobClient for the specified blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_path+"/"+blob_name)

    # Download the content of the blob
    try:
        blob_content = blob_client.download_blob()
    except:
        blob_content = False
        
    return blob_content