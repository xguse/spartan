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

from spartan.utils.misc import Bunch

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


def detect_overlap(coords1, coords2):
    """
    Returns `True` if `coords1` overlaps with `coords2`.
    :param coords1: `list` of two `int` numbers representing **start**, **end** coordinates of a feature
    :param coords2: `list` of two `int` numbers representing **start**, **end** coordinates of a feature
    """
    coords1[0], coords1[1] = int(coords1[0]), int(coords1[1])
    coords2[0], coords2[1] = int(coords2[0]), int(coords2[1])

    # +++ Sort Coords +++
    coords1.sort()
    coords2.sort()
    # +++ Classify Coords +++
    if (coords1[1]-coords1[0]) <= (coords2[1]-coords2[0]):
        shorter = coords1
        longer = coords2
    else:
        shorter = coords2
        longer = coords1
    # +++  +++
    left_edge = (shorter[0]-longer[0] >= 0) and (shorter[0]-longer[1] <= 0)
    right_edge = (shorter[1]-longer[0] >= 0) and (shorter[1]-longer[1] <= 0)
    # -- did we get a hit? --
    return left_edge or right_edge

##########################


class SimpleFeature(object):

    def __init__(self, start, end):

        """


        :param start: left most coordinate.
        :param end: right most coordinate.
        """
        self.data = Bunch()

        start = int(start)
        end = int(end)

        self.data.start = min([start, end])
        self.data.end = max([start, end])

    def __str__(self):
        return "%s-%s" % (self.data.start, self.data.end)

    def __len__(self):
        return interval_length(self.data.start, self.data.end)

    def __contains__(self, other):
        s_start = self.data.start
        o_start = other.data.start
        s_end = self.data.end
        o_end = other.data.end

        if (s_start <= o_start) and (s_end >= o_end):
            return True
        else:
            return False

    def __cmp__(self, other):
        """
        :param other: an interval/feature
        :returns int:
            * `-1` if `other` should sort to the right of `self`
            * `0` if `other` should sort exactly the same as `self`
            * `1` if `other` should sort to the left of `self`

        """
        s_start = self.data.start
        o_start = other.data.start

        if s_start < o_start:
            return -1

        if s_start == o_start:
            return 0

        if s_start > o_start:
            return 1

    def __eq__(self, other):
        """
        Returns `True` if `other` perfectly overlaps this feature, `False` otherwise.
        :param other: an interval/feature
        """
        s_start = self.data.start
        o_start = other.data.start
        s_end = self.data.end
        o_end = other.data.end

        if (s_start == o_start) and (s_end == o_end):
            return True
        else:
            return False

    def __gt__(self, other):
        """
        Returns `True` if `other` falls to the right even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        if self.data.end > other.data.end:
            return True
        else:
            return False


    def __lt__(self, other):
        """
        Returns `True` if `other` falls to the left even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        if self.data.start < other.data.start:
            return True
        else:
            return False

    def has_overlap(self, other):
        return detect_overlap(coords1=[self.data.start, self.data.end],
                              coords2=[other.data.start, other.data.end])

    def get_flank(self, length):
        # TODO: SimpleFeature.flank
        raise NotImplementedError()

    def get_rflank(self, length):
        # TODO: SimpleFeature.rflank

        raise NotImplementedError()

    def get_lflank(self, length):
        # TODO: SimpleFeature.lflank
        raise NotImplementedError()
