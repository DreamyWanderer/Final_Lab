import pymongo

uri = "mongodb://dreamywanderer:fIheB7sQzEsjH3U6WXmOXoVP1Hj79V4Xom1pNV0uHNbNBal0Lx75X6fwSovFOxXFftvFAMsf5SGoACDboPqXRA==@dreamywanderer.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dreamywanderer@"

client = pymongo.MongoClient(uri)
NewsDataset = client['NewsDataset']

# Get name of all existing collections in the NewsDataset
print(NewsDataset.list_collection_names())

# Print all documents in the collection VNFD
VNFD = NewsDataset['VNFD']
""" for doc in VNFD.find():
    print(doc) """
