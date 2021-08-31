from azure.storage.blob import BlobServiceClient
import os
from flask import Flask
import zipfile
import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

app = Flask(__name__)

connect_str = "..."
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
os.mkdir("./data2")
os.mkdir("./data2/images")
blob_client = blob_service_client.get_blob_client(container='images', blob='images_zipped.zip')

with open('./data2/images_zipped.zip', "wb") as download_file:
    download_file.write(blob_client.download_blob().readall())

with zipfile.ZipFile('./data2/images_zipped.zip', 'r') as zip_ref:
    zip_ref.extractall('./data2/images/')

loop = asyncio.get_event_loop()

@app.route("/doit")
def hello():
    async def run():
        # create a producer client to send messages to the event hub
        # specify connection string to your event hubs namespace and
            # the event hub name
        producer = EventHubProducerClient.from_connection_string(conn_str="...")
        async with producer:
            # create a batch
            event_data_batch = await producer.create_batch()

            for i in os.listdir('./data2/images/'):
                blob_client = blob_service_client.get_blob_client(container='images', blob=i)
                upload_file_path = './data2/images/'+i

                # Upload the created file to storage
                with open(upload_file_path, "rb") as data:
                    blob_client.upload_blob(data)

                # add events to the batch
                event_data_batch.add(EventData(i))

            # send the batch of events to the event hub
            await producer.send_batch(event_data_batch)          
    

    loop.run_until_complete(run())

    return "unzipped and sent to blob and hub"