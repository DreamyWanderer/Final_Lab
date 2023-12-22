from wordcloud import WordCloud
import matplotlib.pyplot as plt

def visualize_frequency_words(news_df, col_name, title = ''):
    words_df = [] 
    news_df[col_name].apply(lambda x: words_df.extend(x))
    wordcloud = WordCloud(background_color="white").generate(' '.join(words_df))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(title)
    plt.show()