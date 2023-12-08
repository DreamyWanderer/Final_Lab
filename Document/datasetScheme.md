# Dataset Scheme

## General Features of All Dataset

1. Title (`title`)
2. Text Content (`content`)
3. URL (`url`)
4. Label ($1$: Fake - $0$: Credible) (`label`)

    If possible, we can collect following features as well:

5. URL/List of URLs of images of collected news (Do not download images yet due to storage space limitation) (`imageURL`)
6. Domain of URL (or name of news website) (`domain`)
7. Topic/List of Topics of text content (can collect from given keywords, tags) (`topic`)
8. Author/List of Authors (`author`)
9. Date news created (`date`)

Each colleted news will be saved as a document with above features. The features may be changed in the future.
