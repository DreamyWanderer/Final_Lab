from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


def cal_TypeTokenRatio(text):
    """
    Calculate the Type-Token Ratio (TTR) of a given text.

    Parameters:
    - text (str): The input text.

    Returns:
    - ttr (float): The Type-Token Ratio.
    """
    # Tokenize the text into words
    words = text.split()

    # Calculate the total number of tokens
    total_tokens = len(words)

    # Calculate the number of unique words (types)
    unique_words = set(words)
    total_types = len(unique_words)

    # Calculate the Type-Token Ratio (TTR)
    ttr = total_types / total_tokens

    return ttr


def calculate_tfidf(documents):
    # Create a TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the documents
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Get feature names (terms)
    feature_names = vectorizer.get_feature_names_out()

    # Create a DataFrame to store the result
    result_df = pd.DataFrame(columns=['document', 'term', 'tfidf'])

    # Extract TF-IDF values and populate the DataFrame
    for i, doc in enumerate(documents):
        feature_index = tfidf_matrix[i, :].nonzero()[1]
        tfidf_scores = zip(feature_index, [tfidf_matrix[i, x] for x in feature_index])
        for term_index, tfidf in tfidf_scores:
            result_df = result_df.append({
                'document': f'doc{i + 1}',
                'term': feature_names[term_index],
                'tfidf': tfidf
            }, ignore_index=True)

    return result_df

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

def cal_readability(content):
    words = content.split()
    total_syllables = 0

    for word in words:
        syllables = count_syllables_vietnamese(word)  # Replace with your preferred method for counting syllables in Vietnamese
        total_syllables += syllables

    average_syllables_per_word = total_syllables / len(words)

    return average_syllables_per_word

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



