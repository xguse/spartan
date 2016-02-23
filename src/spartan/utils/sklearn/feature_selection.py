# feature_selection is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 1/25/16.
#
# Please see the license info in the root folder of this package.

"""
Purpose:

=================================================
feature_selection
=================================================
"""
from collections import defaultdict
import math

import numpy as np

import pandas as pd


__author__ = 'Gus Dunn'


def consensus_top10pct_feature_selection(X, y, clf, names=None, iters=100):
    """Runs classifier iters times and keeps track of which features
    (and their mean scores) end up in the top 10%.
    Returns (Counter, mean_retained_features)
    """

    # Validations
    if names is None:
        try:
            names = X.columns.values
        except AttributeError:
            raise Exception('If X is not a Dataframe, you must supply a value for "names".')

    # Bizness starts
    feat_score_db = defaultdict(list)

    i = 0

    while 1:
        if i >= iters:
            break

        try:
            clf.fit(X, y)

            # get first 10% of features
            named_scores = sorted(zip(map(lambda x: round(x, 4), clf.scores_), names), reverse=True)

            first_10pct = named_scores[:int(math.ceil(len(named_scores) / 100 * 10))]

            for f_score, f_name in first_10pct:
                feat_score_db[f_name].append(f_score)

            i += 1

        except ValueError as exc:
            msg = 'This solver needs samples of at least 2 classes'
            if msg in exc[0]:
                continue
            else:
                raise

    return feat_score_db


def process_retained_features(retained, thresh=1, iters=10):
    stable_features = dict()
    stable_features["feature_names"] = []
    stable_features["avg_score"] = []
    stable_features["retention_rate"] = []

    for feature, scores in retained.items():

        if len(scores) >= thresh:
            stable_features["feature_names"].append(feature)
            stable_features["avg_score"].append(np.mean(scores))
            stable_features["retention_rate"].append(len(scores) / iters)

    return pd.DataFrame(stable_features)
