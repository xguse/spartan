import collections

import pandas as pd
import numpy as np

import seaborn as sns

from spartan.utils import errors as e


def confusion_matrix_to_pandas(cm, labels):
    """Returns a pandas dataframe.

    It is created from the confusion matrix stored in `cm` with rows and columns
    labeled with `labels`.
    """
    return pd.DataFrame(data=cm, index=labels, columns=labels)


def normalize_confusion_matrix(cm):

    try:
        return cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    except ValueError as exc:
        if "Shape of passed values is" in exc:
            raise e.SpartanError()

    return cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


def plot_confusion_matrix(cm, labels=None, cmap='Blues', title=None, norm=False, context=None, annot=True):

    if labels is None:
        labels = True

    if isinstance(labels, collections.Iterable) and not isinstance(labels,str):
        labels = [label.title() for label in labels]

    if norm:
        cm = normalize_confusion_matrix(cm)

    if title is None:
        if norm:
            title = "Normalized Confusion Matrix"
        else:
            title = "Confusion Matrix"

    if context is None:
        context = sns.plotting_context("notebook", font_scale=1.5)

    with context:
        ax = sns.heatmap(cm,
                         xticklabels=labels,
                         yticklabels=labels,
                         cmap=cmap,
                         annot=annot
                        )
        ax.set_title(title)
