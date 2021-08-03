"""File: getters/scrapers.py
Functions for scraping BuildHub posts.
Ideally minimise usage as this makes lots of requests to the site.
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import json

from low_carbon_sentiment_analysis import PROJECT_DIR
from low_carbon_sentiment_analysis.utils.buildhub.requests import request_sleep_soup

MAIN_URL = "https://forum.buildhub.org.uk/forum/119-air-source-heat-pumps-ashp/"


def get_all_page_urls(main_url=MAIN_URL):
    """Gets page URLs from the main page."""
    soup = request_sleep_soup(main_url)
    last_page_number = int(soup.find(class_="ipsPagination_last").a["data-page"])
    #
    page_urls = []
    for i in range(last_page_number):
        page_urls.append(main_url + "page/" + str(i + 1) + "/")
    #
    return page_urls


def get_all_thread_urls(page_urls):
    """Gets thread URLs from a list of page URLs."""
    thread_urls = []
    for page_url in page_urls:
        soup = request_sleep_soup(page_url)
        threads = soup.main.find_all("span", class_="ipsType_break ipsContained")
        #
        for thread in threads:
            thread_urls.append(thread.a["href"])
    #
    return thread_urls


# get thread subpage URLs from thread page URLs
def get_all_thread_page_urls(thread_urls):
    """Gets all thread page URLs from a list of thread URLs."""
    thread_page_urls = []
    for thread_url in thread_urls:
        soup = request_sleep_soup(thread_url)
        if soup.find(class_="ipsPagination_last") is not None:
            last_thread_page_number = int(
                soup.find(class_="ipsPagination_last").a["data-page"]
            )
            for i in range(last_thread_page_number):
                thread_page_urls.append(thread_url + "page/" + str(i + 1) + "/")
        else:
            thread_page_urls.append(thread_url)
        #
    return thread_page_urls


def analyse_posts(thread_page_urls):
    """Gets all posts from a list of thread page URLs,
    cleans them and analyses their sentiment.
    """
    analyzer = SentimentIntensityAnalyzer()
    posts_list = []
    for thread_page_url in thread_page_urls:
        soup = request_sleep_soup(thread_page_url)
        for blockquote in soup("blockquote"):
            blockquote.decompose()
        for edited_by in soup.find_all(
            class_="ipsType_reset ipsType_medium ipsType_light"
        ):
            edited_by.decompose()
        posts = soup.find_all(
            "div", class_="ipsType_normal ipsType_richText ipsContained"
        )
        for post in posts:
            clean_post = (
                post.text.replace("\n", " ")
                .replace("\t", " ")
                .replace("\xa0", " ")
                .strip()
            )
            #
            sentence_list = tokenize.sent_tokenize(clean_post)
            if len(sentence_list) > 0:  # if no text, skip - also avoids div by 0
                total_sentiment = 0.0
                for sentence in sentence_list:
                    vs = analyzer.polarity_scores(sentence)
                    total_sentiment += vs["compound"]
                post_sentiment = total_sentiment / len(sentence_list)
                #
                posts_list.append({"text": clean_post, "polarity": post_sentiment})
    #
    posts_list_sorted = sorted(
        posts_list, key=lambda post: post["polarity"], reverse=True
    )
    #
    return posts_list_sorted


def get_and_analyse_all_posts():
    """Function to perform all scraping and sentiment analysis.
    Saves output in outputs/data.
    """
    page_urls = get_all_page_urls()
    thread_urls = get_all_thread_urls(page_urls)
    thread_page_urls = get_all_thread_page_urls(thread_urls)
    post_sentiments = analyse_posts(thread_page_urls)
    #
    with open(
        PROJECT_DIR / "outputs/data/buildhub/buildhub_posts.json", "w"
    ) as outfile:
        json.dump(post_sentiments, outfile, ensure_ascii=False)
