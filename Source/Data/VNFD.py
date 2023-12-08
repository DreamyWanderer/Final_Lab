import glob
import os
import pymongo
import json

URI = "mongodb://dreamywanderer:fIheB7sQzEsjH3U6WXmOXoVP1Hj79V4Xom1pNV0uHNbNBal0Lx75X6fwSovFOxXFftvFAMsf5SGoACDboPqXRA==@dreamywanderer.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dreamywanderer@"

def connectToMongoDB():

    client = pymongo.MongoClient(URI)
    NewsDataset = client["NewsDataset"]

    return NewsDataset
 
def insertNews(NewsDataset, news):

    vnfd = NewsDataset["VNFD"]
    vnfd.insert_one(news)

def parseNews(pathJSON):

    with open(pathJSON, "r", encoding="utf-8") as file:
        news = json.load(file)

    standardNews = {}
    
    # Get suitable key from JSON file before running this script
    try:
        standardNews["title"] = news["title"]
        standardNews["content"] = news["text"]
        standardNews["url"] = news["url"]
        standardNews["label"] = 1 if pathJSON.split("\\")[-3] == "Fake" else 0 
        standardNews["imageURL"] = news["image_url"]
        standardNews["domain"] = news["source_domain"]
        standardNews["topic"] = None
        standardNews["author"] = news["authors"]
        standardNews["date"] = news["date_publish"]
    except:
        print("Error in parsing " + pathJSON)
        return None

    return standardNews

def uploadRawNews(NewsDataset):

    # CAUTION: Empty the collection before uploading
    """ VNFD = NewsDataset["VNFD"]
    VNFD.delete_many({}) """

    directory = r"Dataset\Raw\VFND\Fake_Real_Dataset\Real"
    
    for file in glob.glob(os.path.join(directory, "**/*.json"), recursive=True):
        news = parseNews(file)
        if (news != None):
            insertNews(NewsDataset, news)

        print("Uploaded " + file)

def main():

    NewsDataset = connectToMongoDB()
    uploadRawNews(NewsDataset)

if __name__ == "__main__":
    main()