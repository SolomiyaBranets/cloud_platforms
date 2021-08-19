# Project description

A pipeline that simulates a simple process of an AI business: A Container loads archived MNIST dataset from the object storage, unzips it and processes files one by one: the file itself it dumps to the object storage container and the name of the file sens to the Queue. Azure Function reads the Queue: it downloads the file from the Blob Container, predicts which number is written on the image using open-source ml model and writes down the name of the file and the prediction result to the Database - then it drops the file from memory and procedes with the next one. Services used: 2 compute services: Container and Azure Function, 1 storage service: Blob Container, 1 database: Azure SQL and 1 event service: Event Hub.
To simplify the project, Azure Storage Table can be used instead of the Azure SQL and Azure Storage Queue can be used instead of Event Hub - please, let me know if that's fine. 

Here's the diagram:
![Diagram](https://github.com/SolomiyaBranets/cloud_platforms/blob/master/project/diagram.PNG)
