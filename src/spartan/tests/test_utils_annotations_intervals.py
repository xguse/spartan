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

test_intervals = []
test_intervals.append(i.Interval(1, 9))
test_intervals.append(i.Interval(5, 6))
test_intervals.append(i.Interval(12, 14))
test_intervals.append(i.Interval(14, 15))
test_intervals.append(i.Interval(17, 20))

a,b,c,d,e,f = test_intervals

class TestIntervalLength():
    """
    tests i.raw_interval_length
    """
 
    def test_150_200(self):
        assert i.raw_interval_length(150, 200)  == 51

    def test_150_150(self):
        assert i.raw_interval_length(150, 150) == 1


class TestGrowInterval():
    """
    tests i.grow
    """

    pass


class TestInterval():
    """
    tests i.Interval()
    """

    def test_interval_a_in_b(self):
        assert (a in b) == False

    def test_interval_b_in_a(self):
        assert (a in b) == True

    def test_interval_a_in_b(self):
        assert (a in b) == False


