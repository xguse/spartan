# pandas_helpers.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 1/25/16.
#
# Please see the license info in the root folder of this package.

"""
Purpose:

=================================================
pandas_helpers.py
=================================================
"""
__author__ = 'Gus Dunn'

import pandas as pd


def repandasify(array, y_names, X_names=None):
    """Converts numpy array into pandas dataframe using provided index and column names."""
    df = pd.DataFrame(data=array, index=y_names, columns=X_names)
    return df
