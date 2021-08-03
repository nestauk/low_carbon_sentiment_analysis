"""File: analysis/twitter/tweet_getter.py
Functions to fetch tweets for a given search term
and update the bank of tweets corresponding to that term.
"""

import tweepy
from dotenv import load_dotenv, find_dotenv
import os
import json

from low_carbon_sentiment_analysis.utils.date_formatting import today_date_numeric
from low_carbon_sentiment_analysis import PROJECT_DIR, get_yaml_config

parameters = get_yaml_config(
    PROJECT_DIR / "low_carbon_sentiment_analysis/config/base.yaml"
)

uk_geocode = parameters["twitter"]["uk_geocode"]
number_of_tweets = parameters["twitter"]["number_of_tweets"]


def get_tweets(
    search_term, search_geocode=uk_geocode, number_of_tweets=number_of_tweets
):
    """Returns a list of ids, dates and tweet texts for a search.
    Only tweets from the last 7 days are accessible.
    """
    load_dotenv(find_dotenv())
    #
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_SECRET_KEY")
    #
    auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
    #
    api = tweepy.API(auth)
    #
    tweets = tweepy.Cursor(
        api.search,
        q=search_term,
        lang="en",
        geocode=search_geocode,
        result_type="recent",
        tweet_mode="extended",
    ).items(number_of_tweets)
    #
    tweet_list = []
    #
    for tweet in tweets:
        if not tweet.full_text.startswith("RT @"):
            info = {
                "id": tweet.id,
                "date": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "full_text": tweet.full_text,
            }
            tweet_list.append(info)
    #
    return tweet_list


def update_tweet_bank(search_term):
    """Saves a json file of search results in outputs/data/twitter/weekly
    and updates the bank of tweets for that search term in
    outputs/data/twitter (or creates the bank if it does not exist).
    """
    last_week_tweets = get_tweets(search_term)
    numeric_date = today_date_numeric()
    week_filename = numeric_date + "_" + search_term.replace(" ", "_") + "_tweets.json"
    #
    with open(
        PROJECT_DIR / "outputs/data/twitter/weekly" / week_filename, "w"
    ) as outfile:
        json.dump(last_week_tweets, outfile, ensure_ascii=False, indent=2)
    #
    all_filename = search_term.replace(" ", "_") + "_tweet_bank.json"
    # If the bank exists, open it; otherwise, start with an empty list
    try:
        with open(PROJECT_DIR / "outputs/data/twitter" / all_filename, "r") as filepath:
            all_tweets = json.load(filepath)
    except:
        all_tweets = []
    #
    # Form a list of all tweets
    extended_list = last_week_tweets + all_tweets
    # Remove duplicates - the tweets are dicts so we can't just use set()
    # Instead, form a dictionary of ids to tweets - this removes any duplicates
    # Then just take the values of this dict as a list
    id_to_tweet_dict = {tweet["id"]: tweet for tweet in extended_list}
    unique_tweet_list = list(id_to_tweet_dict.values())
    #
    with open(PROJECT_DIR / "outputs/data/twitter" / all_filename, "w") as filepath:
        json.dump(unique_tweet_list, filepath, indent=2)
