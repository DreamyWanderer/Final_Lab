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

This is the Vietnamese news dataset contains both credible and uncredible samples. Although size of the dataset is really small, the dataset is checked manually for their credibility so this dataset has higher quality in label's accuracy. However, most of websites has been removed, so the images cannot be retrived.

Download VNFD dataset. Extract the folder `Fake_Real_Dataset` and put into `Dataset\Raw\VNFD`. Run `VNFD.py` to push those data to MongoDB. However, due to the inconsistency of scheme of the dataset, we need to change keys suitably in `VNFD.py`.

#### VnExpress.net

This is the main source for credible Vietnamese news dataset, with following properties:

- Every general topic have at least 1 article.
- For each general topic and for each month of each year: there are at least $10$ articles. The years taken is $2020$ - $2023$. So in total, there are at least $6240$ articles (In fact it is less since some articles is missied when crawling).
- For each month: retrieving articles published from $1$-st to $28$-th day until $10$ articles have been colleced.
- We assume that all articles taken from `VnExpress.net` are credible.

#### FakeVN

The dataset of uncredible Vietnamese articles. The creation of this dataset is rolling. This is taken from:

- <https://danlambaovn.blogspot.com/>
- <https://thoibao.online/> (Need VPN)
- <https://thoibao.de/> (Need VPN)
- <https://kenh14.vn/>
- <https://mangxahoi.net/> (Need VPN)
- <https://danviet.vn/> (Mixed)
- <https://tintuconline.com.vn/> (Need VPN)

Assigning general topics to above articles manually is impossible. So we fine-tune the model *mT5* on VnExpreses.net dataset for extracting general topics from Vietnamese text and applying to FakeVN.

### Github Commit Message

Try to follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) and choose type of commits from [here](https://www.conventionalcommits.org/en/v1.0.0/) when you do a commit. This will help set up the standard and is more easy to follow the repository.

### Misc

I suggest you install CoPilot of Github (Mircrosoft) for quicker coding in some cubersome, tedious or boring tasks.
