"""File: getters/read_from_file.py
Reads BuildHub posts from file.
"""

import json
from low_carbon_sentiment_analysis import PROJECT_DIR


def read_posts(filename=PROJECT_DIR / "outputs/data/buildhub/buildhub_posts.json"):
    with open(filename) as f:
        posts = json.load(f)
    return posts
