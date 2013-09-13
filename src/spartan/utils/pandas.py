import pandas as pd
import numpy as np



def stddf(df,axis=0,center='a'):
    """
    helper to unify an interface returning a standardized
    version of a dataframe along either axis.
    
    center is in ['a','m'] # a is mean; m is median
    """
    DF = pd.Dataframe
    if center == 'a':
        c_func = DF.mean
    elif center == 'm':
        c_func = DF.median
        
    if axis == 0:
        return (df - c_func(df,0)) / df.std()
    if axis == 1:
        return df.sub(c_func(df,1), axis=0).div(df.std(1), axis=0)

def get_correlation_matrix(dataframe,transpose=True):
    """
    simple help func. returns corr_mat
    """
    if transpose:
        corr_matrix = dataframe.T.corr()
    else:
        corr_matrix = dataframe.corr()

    return corr_matrix

def get_ranked_corrs_against_item(item_name,correlation_matrix):
    """
    returns a Series of correlation coeffs against ``item_name`` sorted so
    ``item_name`` is at the top
    """
    
    item_corrs = correlation_matrix[item_name].copy()
    
    item_corrs.sort(ascending=False)
    
    return item_corrs
