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

def left_window_coords(win_size, original_left_bound):
    """
    Returns a `tuple` `(new_start, new_end)` left of original bound describing a window of length `win_size` (see
    note).

    Note: Converts any new value less than `1` to `1`.

    :param win_size: size of window to the left.
    :param original_left_bound:
    :return: new_coords
    """
    new_start = original_left_bound - win_size
    new_end = original_left_bound - 1

    if new_start < 1:
        new_start = 1
    if new_end < 1:
        new_end = 1

    new_coords = (new_start, new_end)

    return new_coords

def right_window_coords(win_size, original_right_bound):
    """
    Returns a `tuple` `(new_start, new_end)` right of original bound describing a window of length `win_size`.

    :param win_size: size of window to the right.
    :param original_right_bound:
    :return: new_coords
    """
    new_start = original_right_bound + 1
    new_end = original_right_bound + win_size

    new_coords = (new_start, new_end)

    return new_coords

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

    def __init__(self, start, end):

        """


        :param start: left most coordinate.
        :param end: right most coordinate.
        """

        assert isinstance(start, int)
        assert isinstance(end, int)
        self.start = min([start, end])
        self.end = max([start, end])

    def __len__(self):
        return interval_length(self.start, self.end)

    def __contains__(self, item):
        # TODO: SimpleFeature.__contains__(self, item)
        raise NotImplementedError()

    def __cmp__(self, other):
        # TODO: SimpleFeature.__cmp__
        """
        :param other: an interval/feature
        :returns int:
            * `-1` if `other` should sort to the right of `self`
            * `0` if `other` should sort exactly the same as `self`
            * `1` if `other` should sort to the left of `self`

        """
        raise NotImplementedError()

    def __eq__(self, other):
        # TODO: SimpleFeature.__eq__
        """
        Returns `True` if `other` perfectly overlaps this feature, `False` otherwise.
        :param other: an interval/feature
        """
        raise NotImplementedError()

    def __gt__(self, other):
        # TODO: SimpleFeature.__gt
        """
        Returns `True` if `other` falls to the right and does not overlap this feature, `False` otherwise.
        :param other: an interval/feature
        """
        raise NotImplementedError()

    def __ge__(self, other):
        # TODO: SimpleFeature.__ge
        """
        Returns `True` if `other` falls to the right even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        raise NotImplementedError()

    def __lt__(self, other):
        # TODO: SimpleFeature.__lt
        """
        Returns `True` if `other` falls to the left and does not overlap this feature, `False` otherwise.
        :param other: an interval/feature
        """
        raise NotImplementedError()

    def __le__(self, other):
        # TODO: SimpleFeature.__le
        """
        Returns `True` if `other` falls to the left even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        raise NotImplementedError()

    def get_flank(self, length):
        # TODO: SimpleFeature.flank
        raise NotImplementedError()

    def get_rflank(self, length):
        # TODO: SimpleFeature.rflank

        raise NotImplementedError()



        raise NotImplementedError()

    def get_lflank(self, length):
        # TODO: SimpleFeature.lflank
        raise NotImplementedError()
