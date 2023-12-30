from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import seaborn as sns

def calculate_tfidf(documents):
    # Create a TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    # tfidf_matrix = vectorizer.fit_transform([' '.join(document) for document in documents])
    document_texts = [' '.join(doc) for doc in documents]

    # Get feature names (terms)
    # feature_names = vectorizer.get_feature_names_out()
    tfidf_matrix = tfidf_vectorizer.fit_transform(document_texts)

    # Get feature names (terms)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Convert TF-IDF matrix to a dense DataFrame for readability
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

    return tfidf_df
def visualize_tfidf(tfidf_df, ax, title):
    sns.heatmap(tfidf_df.sample(n=100), cmap='viridis', annot=False, cbar=True, ax=ax)
    ax.set_title(title)

def cal_TypeTokenRatio(words):
    """
    Calculate the Type-Token Ratio (TTR) of a given text.

    Parameters:
    - text (str): The input text.

    Returns:
    - ttr (float): The Type-Token Ratio.
    """

    # Calculate the total number of tokens
    total_tokens = len(words)

    # Calculate the number of unique words (types)
    unique_words = set(words)
    total_types = len(unique_words)

    # Calculate the Type-Token Ratio (TTR)
    ttr = total_types / total_tokens

    return ttr



import re

def count_clauses(sentence):
    # Define patterns for common Vietnamese clause structures
    clause_patterns = [
        r'\b[A-Za-zÀ-Ỹà-ỹ]+\s*[,;:]+\s+[A-Za-zÀ-Ỹà-ỹ]+',  # Subject-verb/object with punctuation separator
        r'\b[A-Za-zÀ-Ỹà-ỹ]+\s+[A-Za-zÀ-Ỹà-ỹ]+\s*[,;:]+\s+[A-Za-zÀ-Ỹà-ỹ]+',  # Subject-verb-object with punctuation separator
        r'\b[A-Za-zÀ-Ỹà-ỹ]+\s+[A-Za-zÀ-Ỹà-ỹ]+\s+(và|hoặc|hay|cùng)\s+[A-Za-zÀ-Ỹà-ỹ]+',  # Subject-verb and coordinating conjunction
        r'\b[A-Za-zÀ-Ỹà-ỹ]+\s+[A-Za-zÀ-Ỹà-ỹ]+\s+và\s+[A-Za-zÀ-Ỹà-ỹ]+',  # Subject-verb and "và" (and) conjunction
        # Add more patterns as needed based on your requirements and language characteristics
    ]

    count = 0
    for pattern in clause_patterns:
        matches = re.findall(pattern, sentence, flags=re.UNICODE)
        count += len(matches)

    return count


def cal_syntactic_complexity(content):
    sentences = content.split('. ')
    total_sentences = len(sentences)
    total_words = 0
    total_clauses = 0
    syntactic_structures = set()

    for sentence in sentences:
        words = sentence.split()
        total_words += len(words)

        clause_count = count_clauses(sentence)
        total_clauses += clause_count

        # Identify and store the syntactic structures used in the sentence
        syntactic_structures.add(sentence)  # Example: Store the whole sentence as a syntactic structure

    average_sentence_length = total_words / total_sentences
    average_clause_length = total_words / total_clauses
    unique_syntactic_structures = len(syntactic_structures)

    syntactic_complexity = {
        'average_sentence_length': average_sentence_length,
        'average_clause_length': average_clause_length,
        'unique_syntactic_structures': unique_syntactic_structures
    }

    return syntactic_complexity



def count_syllables_vietnamese(word):
    vowels = 'aeiouy'
    syllables = 0
    prev_char = None

    for char in word:
        if char in vowels:
            if prev_char is None or prev_char not in vowels:
                syllables += 1
        prev_char = char

    return syllables
def cal_readability(words):
    total_syllables = 0

    for word in words:
        syllables = count_syllables_vietnamese(word)  # Replace with your preferred method for counting syllables in Vietnamese
        total_syllables += syllables

    average_syllables_per_word = total_syllables / len(words)

    return average_syllables_per_word