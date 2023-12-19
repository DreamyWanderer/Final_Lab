from typing import Optional
from newsplease import NewsPlease
from bs4 import BeautifulSoup
from pathlib import Path
from abc import ABC, abstractmethod
from Source.Data.Database import NewsDatabase
import os
import time
import json

class IDatasetBuilder(ABC):
    """The class used to build a dataset from a specific news website.
    This class assumes that aLL articles from this website are in the same ground truth label.
    DatasetBuilder uses `BeautifulSoup` to crawl URLs of articles from a specific urlRoot, then it uses
    `news-please` to crawl the content of each article and save it to a json file.

    To implement this interface, you need to implement the:
    - `getArticleURLs` method to let the class know how to crawl URLs of articles you want to collect.

    The `urlRoot` should be a page lists articles belong to a topic.
    For example, the `urlRoot` of topic "Thế giới" is (in defined date range):
    https://vnexpress.net/category/day/cateid/1001002/fromdate/1701363600/todate/1702832399/.
    """    
    def __init__(self, urlRoot: str, nameTopic: str, numArticlesEachMonth: int, 
                 resultFile: Path, label: int, dateRange: Optional[tuple] = None):
        """
        Args:
            urlRoot (str): The root URL that directly contains the list of articles we want to crawl
            nameTopic (str): The name of topic of urlRoot
            dateRange (tuple): The date range we want to crawl. The format is ((day, month, year), (day, month, year)). Day 31 and 30 may not exist in some months and cause error. If not specified,
            the class should crawl all suitable articles.
            numArticlesEachMonth (int): The number of articles we want to crawl each month in the year range
            resultFile (Path): The path to save the result
            label (int): The label will be assigned to whole dataset
        """        
        self.urlRoot = urlRoot
        self.nameTopic = nameTopic
        self.dateRange = dateRange
        self.numArticlesEachMonth = numArticlesEachMonth
        self.resultFile = resultFile
        self.label = label

    def _getUnixEpoch(self, year: int, month: int, day: int):
        """Convert date to Unix Epoch Second. This is just a helper function often used to get Unix Epoch Second
        for using in URL.

        Args:
            year (int): Year
            month (int): Month
            day (int): Day

        Returns:
            int: Timestamp
        """        
        return int(time.mktime(time.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")))
    
    def removeTimeInDataset(self):
        """Remove time from date information in dataset. 
        This method should only be called after the dataset is built and you do not want to keep the time information in date anymore.

        If the format of `date` field in dataset is not "date time", you have to modify this method.
        """        
        print(self.resultFile)
        with open(self.resultFile, 'r', encoding="utf-8") as file:
            dataset = json.load(file)
            for article in dataset["dataset"]:
                article["date"] = article["date"].split(" ")[0]
        
        with open(self.resultFile, 'w', encoding="utf-8") as file:
            json.dump(dataset, file, indent=4, ensure_ascii=False)
        
    def convertToStandardDataScheme(self, article: dict):
        """Convert the data scheme of an article to the standard scheme

        Args:
            article (dict): The data scheme of the article

        Returns:
            dict: The standard data scheme of the article
        """        
        tmpArticle = {}
        tmpArticle["title"] = article["title"]
        tmpArticle["content"] = article["maintext"]
        tmpArticle["url"] = article["url"]
        tmpArticle["label"] = self.label
        tmpArticle["imageURL"] = article["image_url"]
        tmpArticle["domain"] = article["source_domain"]
        tmpArticle["topic"] = [self.nameTopic]
        tmpArticle["date"] = article["date_publish"]

        return tmpArticle
        
    def buildDataset(self):
        """Build dataset from list of URLs
        """   
        listURLs = self.getArticleURLs()
        if (listURLs is None) or (len(listURLs) == 0):
            print("Error when crawling", self.nameTopic)
            return
        listArticle = {
            "dataset": []
        }

        with open(self.resultFile, 'w+', encoding="utf-8") as file:
            # Get the index of url in listURLs and the url itself
            for i, url in enumerate(listURLs):
                try:
                    article = NewsPlease.from_url(url)
                    if article is not None:
                        article = self.convertToStandardDataScheme(article.get_serializable_dict())
                        listArticle["dataset"].append(article)

                        print("Crawled", i, "/", len(listURLs), "articles in", self.nameTopic, ".")
                    else: 
                        print("Error when crawling", url)
                except:
                    print("Error when crawling", url)
                    continue
            
            json.dump(listArticle, file, indent=4, ensure_ascii=False)

    @abstractmethod
    def getArticleURLs(self):
        """Get list of URLs from urlRoot
        """
        pass