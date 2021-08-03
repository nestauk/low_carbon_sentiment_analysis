"""File: utils/buildhub/getters.py
Function to get the HTML for a web page.
"""

from low_carbon_sentiment_analysis import PROJECT_DIR, get_yaml_config

import requests
import time
from bs4 import BeautifulSoup

parameters = get_yaml_config(
    PROJECT_DIR / "low_carbon_sentiment_analysis/config/base.yaml"
)

wait = parameters["buildhub"]["wait"]


def request_sleep_soup(url, seconds=wait):
    # Requests the URL and returns an HTML soup,
    # waiting for a given number of seconds to avoid the site
    # being overloaded if numerous requests are made.
    page = requests.get(url)
    time.sleep(seconds)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
