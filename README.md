# Final Project - [Course] Big Data in Use

**This project is only for educational purpose only. It by no mean can be used for more serious, high accuracy expectation scenarios without further modification of used methods and existing codebase.**

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
  - `VnExpress`: VnExpress dataset.
  - `FakeVN`: FakeVN dataset.
  - `VNFDPreprocessed`: The preprocessed VNFD dataset.

### Dataset

#### General dataset scheme

Every crawled dataset before pushed to database need to convert to json with features described in [`Document/denineScheme.md`](./Document/datasetScheme.md).

#### Specification of each Dataset

There are $3$ datasets we are going to use in this project as training/EDA data.

1. VNFD
2. VnExpress
3. FakeVN

The specification of each above dataset is described in file [`Document/datasetDetail`](./Document/datasetDetail.md).

### Github Commit Message

Try to follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) and choose type of commits from [here](https://www.conventionalcommits.org/en/v1.0.0/) when you do a commit. This will help set up the standard and is more easy to follow the repository.

### Misc

I suggest you install CoPilot of Github (Mircrosoft) for quicker coding in some cubersome, tedious or boring tasks.
