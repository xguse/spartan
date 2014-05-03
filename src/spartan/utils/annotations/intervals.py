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

def detect_1D_overlap(coords1,coords2):
    # TODO: understand and convert detect_1D_overlap() yo useful code

    """Returns TRUE if coords1 overlaps with coords2.
    """
    coords1[0],coords1[1] = int(coords1[0]),int(coords1[1])
    coords2[0],coords2[1] = int(coords2[0]),int(coords2[1])
    # +++ Validate Usr Input +++
    assert (len(coords1)==2) and (len(coords2)==2), \
           "** ERROR: coords1 and coords2 must be lists of length 2! **"
    # +++ Sort Coords +++
    coords1.sort()
    coords2.sort()
    # +++ Classify Coords +++
    if (coords1[1]-coords1[0]) <= (coords2[1]-coords2[0]):
        shorter = coords1
        longer  = coords2
    else:
        shorter = coords2
        longer  = coords1
    # +++  +++
    lEdge = (shorter[0]-longer[0] >= 0) and (shorter[0]-longer[1] <= 0)
    rEdge = (shorter[1]-longer[0] >= 0) and (shorter[1]-longer[1] <= 0)
    # -- did we get a hit? --
    return (lEdge or rEdge)

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
        # TODO: SimpleFeature.__contains__(self, item)
        pass

    def __cmp__(self, other):
        # TODO: SimpleFeature.__cmp__
        """
        :param other: an interval/feature
        :returns int:
            * `-1` if `other` should sort to the right of `self`
            * `0` if `other` should sort exactly the same as `self`
            * `1` if `other` should sort to the left of `self`

        """
        pass

    def __eq__(self, other):
        # TODO: SimpleFeature.__eq__
        """
        Returns `True` if `other` perfectly overlaps this feature, `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def __gt__(self, other):
        # TODO: SimpleFeature.__gt
        """
        Returns `True` if `other` falls to the right and does not overlap this feature, `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def __ge__(self, other):
        # TODO: SimpleFeature.__ge
        """
        Returns `True` if `other` falls to the right even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def __lt__(self, other):
        # TODO: SimpleFeature.__lt
        """
        Returns `True` if `other` falls to the left and does not overlap this feature, `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def __le__(self, other):
        # TODO: SimpleFeature.__le
        """
        Returns `True` if `other` falls to the left even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        pass

    def flank(self, length):
        # TODO: SimpleFeature.flank
        pass

    def rflank(self, length):
        # TODO: SimpleFeature.rflank
        pass

    def lflank(self, length):
        # TODO: SimpleFeature.lflank
        pass