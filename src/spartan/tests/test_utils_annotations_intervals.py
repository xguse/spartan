# test_utils_annotations_intervals.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 11/26/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
test_utils_annotations_intervals.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

from spartan.utils.annotations import intervals as i


class TestIntervalLength():
    """
    tests i.interval_length
    """
 
    def test_150_200(self):
        assert i.interval_length(150, 200)  == 51

    def test_150_150(self):
        assert i.interval_length(150, 150) == 1


class TestGrowInterval():
    """
    tests i.grow_interval
    """

    pass


