"""File: analysis/buildhub/word_diffs.py
Calculates word co-occurrences in BuildHub posts.
"""

from low_carbon_sentiment_analysis.pipeline.clean_lemmatize import generate_clean_posts
from low_carbon_sentiment_analysis.utils.word_usage import word_prop_diff


post_sentiments = generate_clean_posts()

all_texts = [post["clean_text"] for post in post_sentiments]


# Identifying words that appear more frequently in posts mentioning problems
# than in other posts


def text_condition_problem(string):
    """Returns True if the input string uses words indicating a problem."""
    ls = string.lower()
    return (
        (("problem" in ls) & ("no problem" not in ls))
        | (" issue" in ls)
        | (" fault" in ls)
    )


problem_posts = [
    post for post in post_sentiments if text_condition_problem(post["text"])
]
problem_texts = [post["clean_text"] for post in problem_posts]
problem_diffs = word_prop_diff(all_texts, problem_texts, method=1)
alt_problem_diffs = word_prop_diff(all_texts, problem_texts, method=2)

for item in problem_diffs[0:30]:
    print(item, end="\n")
for item in alt_problem_diffs[0:30]:
    print(item, end="\n")


# Identifying words that appear more frequently in posts mentioning
# problems and causes than in other posts


def text_condition_cause(string):
    """Returns True if the input string mentions a cause."""
    ls = string.lower()
    return " cause" in ls


problem_cause_posts = [
    post
    for post in post_sentiments
    if (text_condition_problem(post["text"]) & text_condition_cause(post["text"]))
]
problem_cause_texts = [post["clean_text"] for post in problem_cause_posts]
problem_cause_diffs = word_prop_diff(all_texts, problem_cause_texts, method=1)
alt_problem_cause_diffs = word_prop_diff(all_texts, problem_cause_texts, method=2)

for item in problem_cause_diffs[0:30]:
    print(item, end="\n")
for item in alt_problem_cause_diffs[0:30]:
    print(item, end="\n")
