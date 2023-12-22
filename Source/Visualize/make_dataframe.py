import pandas as pd
import pymongo

def make_dataframe():
    uri = "mongodb://dreamywanderer:fIheB7sQzEsjH3U6WXmOXoVP1Hj79V4Xom1pNV0uHNbNBal0Lx75X6fwSovFOxXFftvFAMsf5SGoACDboPqXRA==@dreamywanderer.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dreamywanderer@"
    client = pymongo.MongoClient(uri)
    NewsDataset = client['NewsDataset']
    VNFD = NewsDataset['VNFDPreprocessed']

    data = {}
    columns = list(VNFD.find()[0].keys())
    columns.remove('author')
    for col in columns:
        data[col] = []

    for doc in VNFD.find():
        for col in columns:
            data[col].append(doc[col])   
    
    df = pd.DataFrame(data).drop(['_id'], axis = 1)
    df['topic'] = df['topic'].str.get(0)
    return df