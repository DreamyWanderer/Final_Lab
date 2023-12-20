"""Upload all raw dataset to Microsoft Azure MongoDB databases"""

import os
import sys
from unicodedata import name
# Add the root folder of project to sys.path for relative importing when running this script directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from Source.Data.Database import NewsDatabase

uri = "mongodb://dreamywanderer:fIheB7sQzEsjH3U6WXmOXoVP1Hj79V4Xom1pNV0uHNbNBal0Lx75X6fwSovFOxXFftvFAMsf5SGoACDboPqXRA==@dreamywanderer.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dreamywanderer@"
nameDatabase = "NewsDataset"
nameCOllection = "FakeVN"
listDatasetFile = [f"Dataset//Raw//FakeVN//data_{i}.json" for i in range(7, 9)]

database = NewsDatabase(uri, nameDatabase, nameCOllection)
for datasetFile in listDatasetFile:
    database.uploadDataset(datasetFile)
    print("Uploaded", datasetFile)