from azure.storage.blob import BlobServiceClient
import pandas as pd
import os
from azure.storage.blob import ContainerClient
from io import StringIO
from parameters.credentials import *


AZURE_STORAGE_CONNECTION_STRING = f"DefaultEndpointsProtocol=https;AccountName={STORAGEACCOUNTNAME};AccountKey={STORAGEACCOUNTKEY};EndpointSuffix=core.windows.net"


def read_data_from_azure(file_csv):
    connectionString = AZURE_STORAGE_CONNECTION_STRING
    containerName = CONTAINERNAME
    blobName = file_csv

    container_client = ContainerClient.from_connection_string(
         conn_str=connectionString,
         container_name=containerName
         )

    # Load blob as StorageStreamDownloader object
    downloaded_blob = container_client.download_blob(blobName)

    return pd.read_csv(StringIO(downloaded_blob.content_as_text()), sep=",")


def update_current_value(file_name_csv, df):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temporary_files/')
    container_name = "rawdata"
    file_name = file_name_csv
    filepath = os.path.join(local_path, file_name)

    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    df.to_csv(path_or_buf=filepath, index=False)
    with open(filepath, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    os.remove(local_path + "/" + file_name)


def update_savings_azure(file_csv, df):
    connectionString = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    containerName = "rawdata"
    file_name = file_csv

    container_client = ContainerClient.from_connection_string(
         conn_str=connectionString,
         container_name=containerName
         )

    # Load blob as StorageStreamDownloader object
    downloaded_blob = container_client.download_blob(file_name)

    pd_df = pd.read_csv(StringIO(downloaded_blob.content_as_text()))

    # concatenate with new investment
    new_df_invests = pd.concat([pd_df, df], ignore_index=True)

    # upload to azure
    update_current_value(file_name, new_df_invests)

    return
