"""File: analysis/buildhub/text_fixers.py
Functions to clean and lemmatize text.
"""

import nltk
import string
from nltk.corpus import wordnet


def remove_words(text_data, list_of_words_to_remove):
    # For a given list of words, returns all words that are
    # not in a specified list of words to remove.
    return [item for item in text_data if item not in list_of_words_to_remove]


def collapse_list_to_string(string_list):
    # Joins a list of strings into a single string.
    return " ".join(string_list)


def remove_punctuation(s, except_for=["'"]):
    # Removes all punctuation from a string other than a specified list.
    punctuation_to_replace = string.punctuation
    for punct in except_for:
        punctuation_to_replace = punctuation_to_replace.replace(punct, "")
    s = s.translate(str.maketrans("", "", punctuation_to_replace))
    return s


def get_wordnet_pos(pos_tag):
    # Maps POS tag to wordnet word type.
    # Defaults to noun if POS tag is empty.
    if pos_tag.startswith("J"):
        return wordnet.ADJ
    elif pos_tag.startswith("V"):
        return wordnet.VERB
    elif pos_tag.startswith("N"):
        return wordnet.NOUN
    elif pos_tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmatize_text(text):
    # Lemmatizes a list of words.
    tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokenized = tokenizer.tokenize(text)
    return [
        lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag))
        for (word, tag) in nltk.pos_tag(tokenized)
    ]
