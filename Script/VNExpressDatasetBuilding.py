"""Crawling Vietnamese news articles from multiples websites and save them to a dataset.
"""

import os
import sys
# Add the root folder of project to sys.path for relative importing when running this script directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import argparse
from pathlib import Path

from Source.Data.VnExpress import VnExpressDatasetBuilder

r"""
python -m Source.Script.VnExpressDatasetBuilding "https://vnexpress.net/category/day/cateid/1003231" "Du lịch" 10 "../../Dataset/Raw/VnExpress/data_1.json" 0 "((1, 1, 2020), (28, 12, 2023)) --buildDataset
"""

parser = argparse.ArgumentParser()
parser.add_argument("urlRoot", help="The root URL that directly contains the list of articles we want to crawl")
parser.add_argument("nameTopic", help="The name of topic of urlRoot")
parser.add_argument("numArticlesEachMonth", help="The number of articles we want to crawl each month")
parser.add_argument("resultFile", help="The path to save the result")
parser.add_argument("label", help="The label will be assigned to whole dataset")
parser.add_argument("dateRange", help="The date range we want to crawl. The format is ((day, month, year), (day, month, year)). Day 31 and 30 may not exist in some months and cause error. If not specified, the class should crawl all suitable articles.")
parser.add_argument("--buildDataset", help="Crawl and build dataset from scratch", action="store_true")
parser.add_argument("--removeTime", help="Remove time from date information in dataset. This method should only be called after the dataset is built and you do not want to keep the time information in date anymore. If the format of `date` field in dataset is not 'date time', you have to modify this method.", action="store_true")
args = parser.parse_args()

# Crawling data
urlRoot = args.urlRoot
nameTopic = args.nameTopic
numArticlesEachMonth = int(args.numArticlesEachMonth)
resultFile = Path(args.resultFile)
label = int(args.label)
dateRange = eval(args.dateRange)

builder = VnExpressDatasetBuilder(urlRoot, nameTopic, numArticlesEachMonth, resultFile, label, dateRange)
if args.buildDataset:
    builder.buildDataset()

if args.removeTime:
    for i in range(1, 14):
        builder = VnExpressDatasetBuilder(urlRoot, nameTopic, numArticlesEachMonth, resultFile, label, dateRange)
        builder.removeTimeInDataset()
        print("Removed time in data", i)