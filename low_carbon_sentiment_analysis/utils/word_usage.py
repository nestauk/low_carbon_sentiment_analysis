"""File: utils/word_usage.py
Functions to analyse word frequency and co-occurrence.
"""

import math


def word_count(list):
    """Given a list of documents, return a list of (word, frequency) tuples
    ordered by decreasing frequency for each word appearing in the documents.
    """
    counts = dict()
    for str in list:
        words = str.split()
        for word in words:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts


def word_prop_diff(posts_set, posts_subset, lower_bound=10, method=2):
    """For a set of documents, and a particular subset of the documents,
    return the words that appear proportionally more often in the subset
    than in its complement.

    Method 1 is simply the difference between the proportions of documents in
    the subset and its complement which contain a given word. Method 2 uses
    the z test statistic for the comparison of two binomial distributions as
    this may be a better option for low frequency words. Any words appearing
    less often in the subset than the lower bound are excluded.
    """
    props = dict()
    #
    for str in posts_set:
        words = str.split()
        for word in list(set(words)):
            if word in props.keys():
                props[word]["all_num"] += 1
            else:
                props[word] = {"all_num": 1}
    #
    for str in posts_subset:
        words = str.split()
        for word in list(set(words)):
            if "subset_num" in props[word].keys():
                props[word]["subset_num"] += 1
            else:
                props[word]["subset_num"] = 1
    #
    all_total = len(posts_set)
    subset_total = len(posts_subset)
    #
    for word in props.keys():
        item = props[word]
        if "subset_num" not in item.keys():
            item["subset_num"] = 0
        n_0 = all_total - subset_total
        n_1 = subset_total
        p_0 = (item["all_num"] - item["subset_num"]) / n_0
        p_1 = item["subset_num"] / n_1
        if method == 1:
            # metric is the difference between the proportions
            item["metric"] = p_0 - p_1
        if method == 2:
            p = (n_0 * p_0 + n_1 * p_1) / (n_0 + n_1)
            # metric is the z-test statistic
            item["metric"] = (p_0 - p_1) / math.sqrt(p * (1 - p) * (1 / n_0 + 1 / n_1))
    #
    props_filtered = {
        key: value
        for (key, value) in props.items()
        if value["subset_num"] >= lower_bound
    }
    #
    props_sorted = sorted(props_filtered.items(), key=lambda item: item[1]["metric"])
    return props_sorted
