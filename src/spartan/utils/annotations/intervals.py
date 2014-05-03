# intervals.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 5/3/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
intervals.py
=================================================
Purpose:
This code is intended to provide the "base" interval representation for `spartan`.

"""
__author__ = 'Gus Dunn'


#### Helper functions ####
def interval_length(start, end):
    return end - start + 1


##########################

class CompoundFeature(object):
    def __init__(self):
        pass




class SimpleFeature(object):

    def __init__(self, start, end, seqid=None):

        """


        :param start: left most coordinate.
        :param end: right most coordinate.
        :param seqid: ID of the sequence that this interval is annotated on.
        :param name:
        """

        assert isinstance(start, int)
        assert isinstance(end, int)
        self.start = min([start, end])
        self.end = max([start, end])
        self.seqid = seqid

    def __len__(self):
        return interval_length(self.start, self.end)

    def __contains__(self, item):
        pass

    def __cmp__(self, other):
        """
        :param other: an interval/feature
        :returns int:
            * `-1` if `other` should sort to the right of `self`
            * `0` if `other` should sort exactly the same as `self`
            * `1` if `other` should sort to the left of `self`

        """
        pass

    def __eq__(self, other):
        """
        Returns `True` if `other` perfectly overlaps this feature, `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def __gt__(self, other):
        """
        Returns `True` if `other` falls to the right and does not overlap this feature, `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def __ge__(self, other):
        """
        Returns `True` if `other` falls to the right even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def __lt__(self, other):
        """
        Returns `True` if `other` falls to the left and does not overlap this feature, `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def __le__(self, other):
        """
        Returns `True` if `other` falls to the left even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def flank(self, length):
        pass

    def rflank(self, length):
        pass

    def lflank(self, length):
        pass