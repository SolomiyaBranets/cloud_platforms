# Project description

A pipeline that simulates a simple process of an AI business: A Webapp loads archived dataset with handwritten text from the object storage, unzips it and processes files one by one: the file itself it dumps to the object storage container and the name of the file sends to the Event Hub. Azure Function reads the Queue: it downloads the file from the Blob Container, predicts what is written on the image by sending a  request to Azure Cognitive Service and writes down the name of the file and the prediction result to the SQL Database. Services used: 2 compute services: Webapp and Azure Function, 1 storage service: Blob Container, 1 database: Azure SQL, 1 event service: Event Hub and 1 ML Service – Azure Cognitive Service. 

Here's the diagram:
![Diagram](https://github.com/SolomiyaBranets/cloud_platforms/blob/master/project/diagram.PNG)
