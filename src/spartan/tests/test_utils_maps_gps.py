# test_utils_maps_gps.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 2/2/15.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
test_utils_maps_gps.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

import munch as m

from spartan.utils.maps import gps as t



if __name__ == "__main__":

    c = t.load_gps_coords('/home/gus/Dropbox/repos/git/spartan/testing/gps/gps_no_traces.tsv')

    all_mean = c.mean()
    UWA_mean = c.mean(trace='UWA')
    KTC_mean = c.mean(trace='KTC')
    NGO_mean = c.mean(trace='NGO')

    all_median = c.median()
    UWA_median = c.median(trace='UWA')
    KTC_median = c.median(trace='KTC')
    NGO_median = c.median(trace='NGO')
