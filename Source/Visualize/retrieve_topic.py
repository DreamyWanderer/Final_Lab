from gensim import corpora
from gensim.models import LdaModel
from nltk.tokenize import word_tokenize
import warnings
warnings.filterwarnings("ignore")

def retrieve_topic(content):
    dictionary = corpora.Dictionary([content])
    corpus = [dictionary.doc2bow(content)]
    lda_model = LdaModel(corpus, num_topics=1, id2word=dictionary)
    topics = lda_model.show_topic(0)
    topics = [topic[0] for topic in topics]
    return topics