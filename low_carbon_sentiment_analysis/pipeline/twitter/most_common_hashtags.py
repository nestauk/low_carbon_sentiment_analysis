"""File: analysis/twitter/most_common_hashtags.py
Plots a bar chart of the most common hashtags used in tweets for a given search term.
"""

import matplotlib.pyplot as plt

from low_carbon_sentiment_analysis.pipeline.twitter.tweet_analyser import clean_tweets
from low_carbon_sentiment_analysis.utils.word_usage import word_count
from low_carbon_sentiment_analysis.utils.text_fixers import remove_punctuation
from low_carbon_sentiment_analysis import PROJECT_DIR


def extract_and_count_hashtags(input_filename):
    """Counts hashtags in tweets.
    Returns a list of (hashtag, frequency) tuples.
    """
    tweets_and_sentiments = clean_tweets(input_filename)
    # Make lowercase and remove punctuation, other than apostrophes and hashes
    tweet_texts = [tweet["clean_text"].lower() for tweet in tweets_and_sentiments]
    text_no_punct = [
        remove_punctuation(text, except_for=["'", "#"]) for text in tweet_texts
    ]
    # Count words, filter to hashtags
    wc = word_count(text_no_punct)
    hashtag_frequencies = [item for item in wc if item[0].startswith("#")]
    #
    return hashtag_frequencies


def plot_hashtag_frequency(input_filename, lower_bound, graph_title, output_filename):
    """Plots a bar chart showing the most used hashtags for a
    particular search term. Only shows hashtags used more than
    the lower bound. Saves figure in outputs folder.
    """
    hashtag_frequencies = extract_and_count_hashtags(input_filename)
    # Drop any that are less frequent than the lower bound
    common_hashtag_frequencies = [
        item for item in hashtag_frequencies if item[1] >= lower_bound
    ]
    hashtags = [item[0] for item in common_hashtag_frequencies]
    hashtags.reverse()
    frequencies = [item[1] for item in common_hashtag_frequencies]
    frequencies.reverse()
    #
    fig, ax = plt.subplots()
    plt.barh(hashtags, frequencies)
    ax.set_title(graph_title)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Hashtag")
    plt.tight_layout()
    plt.savefig(PROJECT_DIR / "outputs/figures" / output_filename)
