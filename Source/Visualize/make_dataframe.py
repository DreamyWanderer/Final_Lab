import pandas as pd
# from Source.Data import VNFD
import pymongo

def make_dataframe():
    uri = "mongodb://dreamywanderer:fIheB7sQzEsjH3U6WXmOXoVP1Hj79V4Xom1pNV0uHNbNBal0Lx75X6fwSovFOxXFftvFAMsf5SGoACDboPqXRA==@dreamywanderer.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dreamywanderer@"
    client = pymongo.MongoClient(uri)
    NewsDataset = client['NewsDataset']
    VNFD = NewsDataset['VNFDPreprocessed']

    data = {}
    columns = list(VNFD.find()[0].keys())
    for col in columns:
        data[col] = []

    for doc in VNFD.find():
        for col in columns:
            data[col].append(doc[col])   
    
    df = pd.DataFrame(data).drop(['_id'], axis = 1)
    df['topic'] = df['topic'].str.get(0)
    return df

def make_raw_dataframe():
    uri = "mongodb://dreamywanderer:fIheB7sQzEsjH3U6WXmOXoVP1Hj79V4Xom1pNV0uHNbNBal0Lx75X6fwSovFOxXFftvFAMsf5SGoACDboPqXRA==@dreamywanderer.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dreamywanderer@"
    client = pymongo.MongoClient(uri)
    NewsDataset = client['NewsDataset']
#     VNFD`: VNFD dataset.
#   - `VnExpress`: VnExpress dataset.
#   - `FakeVN`: FakeVN dataset.
    
    VNFD = NewsDataset['VNFD']
    VnExpress = NewsDataset['VnExpress']
    FakeVN = NewsDataset['FakeVN']

    # Return df that contain for all collections
    df = pd.DataFrame()
    for collection in [VNFD, VnExpress, FakeVN]:
        data = {}
        columns = list(collection.find()[0].keys())
        for col in columns:
            data[col] = []

        for doc in collection.find():
            for col in columns:
                data[col].append(doc[col])   
        df = df.append(pd.DataFrame(data).drop(['_id'], axis = 1))
    df['topic'] = df['topic'].str.get(0)
    return df
    