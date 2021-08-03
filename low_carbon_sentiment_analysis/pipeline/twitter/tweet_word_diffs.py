"""File: analysis/twitter/tweet_word_diffs.py
Finds words the appear proportionally more often in tweets of a certain sentiment.
"""

from low_carbon_sentiment_analysis.utils.word_usage import word_prop_diff
from low_carbon_sentiment_analysis.pipeline.clean_lemmatize import clean_and_lemmatize
from low_carbon_sentiment_analysis.pipeline.twitter.tweet_analyser import analyse_tweets

from low_carbon_sentiment_analysis import PROJECT_DIR, get_yaml_config

parameters = get_yaml_config(
    PROJECT_DIR / "low_carbon_sentiment_analysis/config/base.yaml"
)

neg_param = parameters["sentiment"]["neg_param"]
pos_param = parameters["sentiment"]["pos_param"]


def sentiment_words(input_file, sentiment="positive"):
    #
    tweets_and_sentiments = analyse_tweets(input_file)
    #
    for tweet in tweets_and_sentiments:
        tweet["important_text"] = clean_and_lemmatize(tweet["clean_text"])
    #
    all_tweets = [tweet["important_text"] for tweet in tweets_and_sentiments]
    #
    pos_tweets = [
        tweet["important_text"]
        for tweet in tweets_and_sentiments
        if tweet["polarity"] >= pos_param
    ]
    neg_tweets = [
        tweet["important_text"]
        for tweet in tweets_and_sentiments
        if tweet["polarity"] <= neg_param
    ]
    #
    if sentiment == "positive":
        return word_prop_diff(all_tweets, pos_tweets, 10)
    if sentiment == "negative":
        return word_prop_diff(all_tweets, neg_tweets, 10)
