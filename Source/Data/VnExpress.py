from calendar import c
from newsplease import NewsPlease
from bs4 import BeautifulSoup
from pathlib import Path
from Source.Data.DatasetBuilder import IDatasetBuilder
import os
import time
import json

import requests

""" article = NewsPlease.from_url(
    'https://vnexpress.net/mon-no-cuoc-doi-cua-nguoi-dan-ba-buon-tien-gia-4679635.html')
with open("demo.json", 'w', encoding="utf-8") as file:
    json.dump(article.get_serializable_dict(), file, indent=4, ensure_ascii=False) """

class VnExpressDatasetBuilder(IDatasetBuilder):
    """The class used to build a dataset from VnExpress news website.

    The `urlRoot` should be a page lists articles belong to a topic.
    For example, the `urlRoot` of topic "Thế giới" is (in defined date range):
    https://vnexpress.net/category/day/cateid/1001002/fromdate/1701363600/todate/1702832399/.
    """      
    def getArticleURLs(self):
        """Get list of URLs from urlRoot
        """
        listURLs = []
        numPage = 1

        for year in range(self.dateRange[0][2], self.dateRange[1][2] + 1): #type: ignore
            for month in range(self.dateRange[0][1], self.dateRange[1][1] + 1): #type: ignore
                listUrlInMonth = []
                numPage = 1

                while (True):
                    try:
                        fromDay = self._getUnixEpoch(year, month, self.dateRange[0][0]) #type: ignore
                        toDay = self._getUnixEpoch(year, month, self.dateRange[1][0]) #type: ignore
                        urlRootLv2 = self.urlRoot + f"/fromdate/{fromDay}/todate/{toDay}/page/{numPage}"

                        response = requests.get(urlRootLv2)
                        soup = BeautifulSoup(response.text, 'lxml')

                        # Get all class="title_news" in the tag with id="automation_TV0".
                        # Then for each found tag, get the a tag inside it and get the href attribute.
                        listURLsLv2 = [tag.a["href"] for tag in soup.find(id="automation_TV0").find_all(class_="title-news")] # type: ignore
                        listUrlInMonth.extend(listURLsLv2)

                        print("Crawled", len(listUrlInMonth), "articles in", self.nameTopic, "in", month, "/", year, ".")
                        
                        if len(listUrlInMonth) >= self.numArticlesEachMonth:
                            listURLs.extend(listUrlInMonth[:self.numArticlesEachMonth])
                            break
                        else:
                            numPage += 1
                    except:
                        print("Error when crawling", self.nameTopic, "in", month, "/", year, ".")
                        break

        return listURLs