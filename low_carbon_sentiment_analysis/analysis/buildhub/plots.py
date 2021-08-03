"""File: analysis/buildhub/plots.py
Produces a histogram of BuildHub post sentiments.
"""

import matplotlib.pyplot as plt

from low_carbon_sentiment_analysis import PROJECT_DIR
from low_carbon_sentiment_analysis.getters.buildhub.read_from_file import read_posts

post_sentiments = read_posts()

polarities = [post["polarity"] for post in post_sentiments]

fig, ax = plt.subplots()
plt.hist(polarities, bins=50)
ax.set_title("Histogram of BuildHub post sentiments")
ax.set_xlabel("Post sentiment")
ax.set_ylabel("Frequency")

plt.savefig(PROJECT_DIR / "outputs/figures/all_buildhub_post_polarities.png")
