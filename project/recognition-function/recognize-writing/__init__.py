from typing import List
import logging
import pyodbc


import azure.functions as func

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
import time
from azure.storage.blob import BlobServiceClient


def main(events: List[func.EventHubEvent]):

    logging.info('started')

    subscription_key = "f6c66acc36124cdb9dd39651a35b7b67"
    endpoint = "https://ocr-api-cloud-platforms.cognitiveservices.azure.com/"
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    connect_str = "..."
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    local_path = "./images"

    server = 'mysqlserver-cloud-images.database.windows.net'
    database = 'images-recognition-result-db'
    username = 'azureuser'
    password = '...'   
    driver= '{ODBC Driver 17 for SQL Server}'

    if not os.path.exists(local_path): 
        os.mkdir(directory)

    connection = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = connection.cursor()

        
    for event in events:
        logging.info('Python EventHub trigger processed an event: %s',
                        event.get_body().decode('utf-8'))
        file_name = str(event.get_body().decode('utf-8'))

        cursor.execute("INSERT INTO dbo.recognition_results_test (image_name, result) VALUES ('"'{file_name}'"', '"'{final_result}'"')".format(file_name = file_name, final_result = file_name))
        connection.commit()

        try:
            # download image from blob store
            blob_client = blob_service_client.get_blob_client(container='images', blob=file_name)
            
            with open('./images/'+file_name, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

            # predict what was written
            read_image = open('./images/'+file_name, "rb")

            read_response = computervision_client.read_in_stream(read_image, raw=True)
            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]

            while True:
                read_result = computervision_client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            final_result = ''
            # Print the detected text, line by line
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        final_result += line.text + ' '
        except: final_result = "error"

        cursor.execute("INSERT INTO dbo.recognition_results2 (image_name, result) VALUES ('"'{file_name}'"', '"'{final_result}'"')".format(file_name = file_name, final_result = final_result))
        connection.commit()

        logging.info(final_result)