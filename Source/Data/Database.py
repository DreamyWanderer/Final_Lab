import datetime
from pathlib import Path
import pymongo
import json

class NewsDatabase():
    """Manage communication with the MongoDB dabases that store the articles dataset.
    """    
    def __init__(self, uri: str, dbName: str, collectionName: str):
        """Initialize the database

        Args:
            uri (str): The URI to connect to the database
            dbName (str): The name of the database
            collectionName (str): The name of the collection
        """        
        self.client = pymongo.MongoClient(uri)
        self.NewsDataset = self.client[dbName]
        self.collection = self.NewsDataset[collectionName]

    def insertNews(self, news: dict):
        """Insert an article to the database

        Args:
            news (dict): The article
        """        
        self.collection.insert_one(news)

    def uploadDataset(self, datasetFile: str):
        """Upload a dataset to the database

        Args:
            datasetFile (str): The path to the dataset
        """        
        with open(datasetFile, 'r', encoding="utf-8") as file:
            dataset = json.load(file)
            for i, article in enumerate(dataset["dataset"]):
                self.insertNews(article)
                print("Uploaded", i, "/", len(dataset["dataset"]), "articles in", datasetFile, ".")