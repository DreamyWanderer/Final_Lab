# Specification of Dataset

## VNFD

This is the Vietnamese news dataset contains both credible and uncredible samples. Although size of the dataset is really small, the dataset is checked manually for their credibility so this dataset has higher quality in label's accuracy. However, most of websites has been removed, so the images cannot be retrived.

The process of converting original VNFD dataset to ours standard dataset scheme and then publishing it in Database is not straightforward. So I will not describe it here.

## VnExpress

This is the main source for credible Vietnamese news dataset, with following properties:

- Every general topic have at least 1 article.
- For each general topic and for each month of each year: there are at least $10$ articles. The years taken is $2020$ - $2023$. So in total, there are at least $6240$ articles (In fact it is less since some articles is missied when crawling).
- For each month: retrieving articles published from $1$-st to $28$-th day until $10$ articles have been colleced.
- We assume that all articles taken from `VnExpress.net` are credible.

## FakeVN

The dataset of uncredible Vietnamese articles. Due to the scarity of existing fake news, we cannot guarantee that the published date of articles belong to the same range of year like VnExpress dataset. There are about $3000$ colleced samples.

This is taken from:

- <https://danlambaovn.blogspot.com/> (Not crawled yet).
- ~~<https://thoibao.online/> (Need VPN)~~ (Cannot retrieve content by `news-please`)
- <https://thoibao.de/> (Need VPN)
- <https://kenh14.vn/> (Not crawled yet)
- <https://tintuconline.com.vn/> (Need VPN) (Cannot crawled yet, quite difficult)
- <https://www.bbc.com/vietnamese>

For some of news sources, assigning general topics to articles manually is impossible. So we fine-tune the model *mT5* on VnExpreses.net dataset for extracting general topics from Vietnamese text and applying to FakeVN.