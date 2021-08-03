"""File: pipeline/clean_lemmatize.py
Functions to clean and lemmatize posts.
"""

from nltk.corpus import stopwords

from low_carbon_sentiment_analysis.utils.text_fixers import (
    remove_words,
    collapse_list_to_string,
    remove_punctuation,
    lemmatize_text,
)
from low_carbon_sentiment_analysis.getters.buildhub.read_from_file import read_posts


def clean_and_lemmatize(text):
    # Performs the following actions on a string:
    # makes lowercase, removes punctuation,
    # removes nltk stopwords, and lemmatizes words.
    stop = stopwords.words("english")
    #
    lt = text.lower()
    lt_clean = [remove_punctuation(word) for word in lt.split()]
    lt_nostop = remove_words(lt_clean, stop)
    lt_str = collapse_list_to_string(lt_nostop)
    lt_lemma = lemmatize_text(lt_str)
    lt_lemma_string = collapse_list_to_string(lt_lemma)
    #
    return lt_lemma_string


def generate_clean_posts():
    """Returns a list of dictionaries, each of which is a BuildHub post
    with associated cleaned/lemmatized text.
    """
    post_sentiments = read_posts()
    #
    for post in post_sentiments:
        post["clean_text"] = clean_and_lemmatize(post["text"])
    #
    return post_sentiments
