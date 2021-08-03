"""
"""

import preprocessor as pp  # https://pypi.org/project/tweet-preprocessor/
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import json

from low_carbon_sentiment_analysis import PROJECT_DIR

pp.set_options(pp.OPT.URL, pp.OPT.MENTION, pp.OPT.RESERVED, pp.OPT.NUMBER)


def clean_tweets(input_file):
    with open(PROJECT_DIR / "outputs/data/twitter" / input_file, "r") as filepath:
        tweet_list = json.load(filepath)
    # drops retweets and cleans the rest
    for tweet in tweet_list:
        text = tweet["full_text"]
        if text.startswith("RT @"):
            tweet_list.drop(tweet)
        else:
            tweet["clean_text"] = pp.clean(text)
    return tweet_list


def analyse_tweets(input_file):
    tweet_list = clean_tweets(input_file)
    analyzer = SentimentIntensityAnalyzer()
    for tweet in tweet_list:
        sentence_list = tokenize.sent_tokenize(tweet["clean_text"])
        if len(sentence_list) > 0:  # if no text, skip - also avoids div by 0
            total_sentiment = 0.0
            for sentence in sentence_list:  # calculate the mean sentiment
                sentence_sentiment = analyzer.polarity_scores(sentence)
                total_sentiment += sentence_sentiment["compound"]
            tweet["polarity"] = total_sentiment / len(sentence_list)
        else:
            tweet["polarity"] = 0.0
    tweet_list_sorted = sorted(
        tweet_list, key=lambda tweet: tweet["polarity"], reverse=True
    )
    return tweet_list_sorted
