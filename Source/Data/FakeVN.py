from bs4 import BeautifulSoup
from Source.Data.DatasetBuilder import IDatasetBuilder
from pathlib import Path
from abc import ABC, abstractmethod
import os
import requests

class DatasetBuilderPageNumberNoDateLimit(IDatasetBuilder, ABC):
    """Work with news website that usses page numbering to navigate between pages. Does not limit
    number of crawled articles by date range or per month. 

    You can limit total number of crawled articles by setting `numArticlesEachMonth` in constructor.
    """

    @abstractmethod
    def _getURLRootv2(self, **kwag) -> str:
        pass

    def _getListURLsLv2(self, **kwag) -> list:
        return []

    def getArticleURLs(self):
        """Get list of URLs from urlRoot
        """
        listURLs = []
        numPage = 1

        while (True):
            try:
                urlRootLv2: str = self._getURLRootv2(page=numPage)

                response = requests.get(urlRootLv2)
                self._soup = BeautifulSoup(response.text, 'lxml')

                listURLsLv2 = self._getListURLsLv2()
                listURLs += listURLsLv2

                print("Crawled", len(listURLsLv2), "articles in", self.nameTopic, "from page", numPage, ".")

                if len(listURLs) >= self.numArticlesEachMonth or len(listURLsLv2) == 0:
                    break
                else:
                    numPage += 1
            except:
                print("Error when crawling", self.nameTopic, "from page", numPage, ".")
                break

        return listURLs

class Thoibao_deDatasetBuilder(DatasetBuilderPageNumberNoDateLimit):

    def _getURLRootv2(self, **kwag) -> str:
        return self.urlRoot + f"/page/{kwag['page']}"
    
    def _getListURLsLv2(self, **kwag) -> list:
        return [article.find("a")["href"] for article in 
                self._soup.find("div", {"id": "content"}).find_all("article")] # type: ignore

class BBCDatasetBuilder(DatasetBuilderPageNumberNoDateLimit):

    def _getURLRootv2(self, **kwag) -> str:
        return f"{self.urlRoot}?page={kwag['page']}"
    
    def _getListURLsLv2(self, **kwag) -> list:
        return [li.find("a")["href"] for li in 
                self._soup.find("ul", {"data-testid": "topic-promos"}).find_all("li")]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(os.getcwd())

    """ fakeVN = Thoibao_deDatasetBuilder("https://thoibao.de/blog/category/phap-luat-doi-song", "Pháp luật", 20,
                                  Path("../../Dataset/Raw/FakeVN/data_4.json"), 1)
    fakeVN.buildDataset() """

    """ fakeVN = BBCDatasetBuilder("https://www.bbc.com/vietnamese/topics/ckdxnx1k7zxt", "Thể thao", 1000000,
                                  Path("../../Dataset/Raw/FakeVN/data_8.json"), 1)
    fakeVN.buildDataset() """

    # Remove time in date from data_1 to data_8
    for i in range(1, 9):
        fakeVN = BBCDatasetBuilder("https://www.bbc.com/vietnamese/topics/ckdxnx1k7zxt", "Thể thao", 1000000,
                                  Path(f"../../Dataset/Raw/FakeVN/data_{i}.json"), 1)
        fakeVN.removeTimeInDataset()
        print("Done", i)