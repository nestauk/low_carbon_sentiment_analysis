"""File: analysis/twitter/search_term_sentiment_plots.py
Plots a histogram of the sentiment of tweets.
"""

from low_carbon_sentiment_analysis import PROJECT_DIR
from low_carbon_sentiment_analysis.pipeline.twitter.tweet_analyser import analyse_tweets

import matplotlib.pyplot as plt


def plot_sentiment(input_path, histogram_bins, graph_title, output_filename):
    """Plots tweet sentiments as a histogram and saves in outputs/plots."""
    tweets_and_sentiments = analyse_tweets(input_path)
    #
    sentiments = [tweet["polarity"] for tweet in tweets_and_sentiments]
    #
    fig, ax = plt.subplots()
    plt.hist(sentiments, bins=histogram_bins)
    ax.set_title(graph_title)
    ax.set_xlabel("Tweet sentiment")
    ax.set_ylabel("Frequency")
    ax.set_xlim([-1, 1])
    #
    plt.savefig(PROJECT_DIR / "outputs/figures" / output_filename)
