"""File: analysis/twitter/tweet_analysis.py
Various analysis of tweets.
"""

from low_carbon_sentiment_analysis.getters.twitter.tweet_getter import update_tweet_bank
from low_carbon_sentiment_analysis.pipeline.twitter.most_common_hashtags import (
    plot_hashtag_frequency,
)
from low_carbon_sentiment_analysis.pipeline.twitter.search_term_sentiment_plots import (
    plot_sentiment,
)
from low_carbon_sentiment_analysis.pipeline.twitter.tweet_word_diffs import (
    sentiment_words,
)


def perform_analysis(search_term):
    update_tweet_bank(search_term)
    search_term_no_spaces = search_term.replace(" ", "_")
    input_filename = search_term_no_spaces + "_tweet_bank.json"
    plot_hashtag_frequency(
        input_filename,
        lower_bound=3,
        graph_title="Most common hashtags in\n tweets mentioning '" + search_term + "'",
        output_filename=search_term_no_spaces + "_hashtag_frequency.png",
    )
    plot_sentiment(
        input_filename,
        histogram_bins=20,
        graph_title="Sentiments of tweets\n mentioning '" + search_term + "'",
        output_filename=search_term_no_spaces + "_sentiments_histogram.png",
    )
    print("Positively associated words:")
    for item in sentiment_words(input_filename, sentiment="positive"):
        print(item, end="\n")
    print("Negatively associated words:")
    for item in sentiment_words(input_filename, sentiment="negative"):
        print(item, end="\n")


# 'heat pump'
perform_analysis("heat pump")

# 'solar pv'
perform_analysis("solar pv")

plot_sentiment(
    "heat_pump_tweet_bank.json",
    histogram_bins=20,
    graph_title="Sentiments of tweets mentioning '"
    + "heat pump"
    + "',\nJuly 14th - 30th",
    output_filename="heat_pump" + "_sentiments_histogram.png",
)

plot_hashtag_frequency(
    "heat_pump_tweet_bank.json",
    lower_bound=3,
    graph_title="Most common hashtags in\n tweets mentioning '"
    + "heat pump"
    + "',\nJuly 14th - 30th",
    output_filename="heat_pump" + "_hashtag_frequency.png",
)
