# Final Project - [Course] Big Data in Use

## Information

- Name project: **Fake News Detection in Big Data Scenario**
- Group: Allin
- Instructor: PhD. Nguyễn Ngọc Thảo
- Department: Computer Science

## About repository

This repository contains propsal, tasks, descriptions, source code and other related resources for this course.

## System requirement

## Development Guideline

### Microsoft Azure MongoDB

#### Set up connection

Use following code snippet:

```[Python]
uri = "mongodb://dreamywanderer:fIheB7sQzEsjH3U6WXmOXoVP1Hj79V4Xom1pNV0uHNbNBal0Lx75X6fwSovFOxXFftvFAMsf5SGoACDboPqXRA==@dreamywanderer.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@dreamywanderer@"

client = pymongo.MongoClient(uri)
NewsDataset = client['NewsDataset']
```

#### List of Database

- `NewsDataset`: Contains collections of multiple original (raw) dataset. Each dataset belongs to a collection:
  - `VNFD`: VNFD dataset.
- ``: Contains collections of multiple processed dataset.

### Dataset

#### General dataset scheme

Every crawled dataset before pushed to database need to convert to json with features described in `Document/denineScheme.md`.

#### VNFD

Download VNFD dataset. Extract the folder `Fake_Real_Dataset` and put into `Dataset\Raw\VNFD`. Run `VNFD.py` to push those data to MongoDB. However, due to the inconsistency of scheme of the dataset, we need to change keys suitably in `VNFD.py`.

### Github Commit Message

Try to follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) and choose type of commits from [here](https://www.conventionalcommits.org/en/v1.0.0/) when you do a commit. This will help set up the standard and is more easy to follow the repository.

### Misc

I suggest you install CoPilot of Github (Mircrosoft) for quicker coding in some cubersome, tedious or boring tasks.
