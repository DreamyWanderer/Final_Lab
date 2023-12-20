# Dataset Scheme

## General Features of All Dataset

1. Title (`title`)
2. Text Content (`content`)
3. URL (`url`)
4. Label ($1$: Fake - $0$: Credible) (`label`)

    If possible, we can collect following features as well:

5. URL/List of URLs of images of collected news (Do not download images yet due to storage space limitation) (`imageURL`)
6. Domain of URL (or name of news website) (`domain`)
7. List of Topics of text content (can collect from given keywords, tags) (`topic`)
8. List of Authors (`author`)
9. Date news created (`date`)

For any empty field: set `null`

Each colleted news will be saved as a document with above features. The features may be changed in the future.

## About `topic` field

Beside using topic extraction tools later, we try to define a predefined scope of **general topics**. It means each of news sample has at least $1$ value in `topic` list field, and the first one is that general topic. We establish this general `topic` to avoid the case that all dataset does not have common `topic` values which can make EDA meaningless. Certainly each news sample still has other values in `topic`, which is can be considered specific topics.

The following is the list of general topics (build from VnExpress.net):

- Thời sự
- Thế giới
- Kinh tế
- Bất động sản
- Khoa học
- Giải trí
- Thể thao
- Pháp luật
- Giáo dục
- Sức khỏe
- Đời sống
- Du lịch
- Số hóa (Công nghệ)
