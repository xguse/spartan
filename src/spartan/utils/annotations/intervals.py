# intervals.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 5/3/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
test_intervals.py
=================================================
Purpose:
This code is intended to provide the "base" interval representation for `spartan`.

"""

from spartan.utils.misc import Bunch

__author__ = 'Gus Dunn'

from collections import deque
import pybedtools as pbt

import spartan.utils.errors as e


# class Interval(pbt.Interval):
class Interval(object):
    """
    Represents a single, strandless, start/end interval.
    """

    def __init__(self, start, end):

        """
        :param start: left most coordinate.
        :param end: right most coordinate.
        """
        assert isinstance(start, int)
        assert isinstance(end, int)

        try:
            assert start <= end
        except AssertionError:
            raise e.NonsenseInterval

        self.start = start
        self.end = end


    def __str__(self):
        return "%s-%s" % (self.start, self.end)

    def __repr__(self):
        return "Interval(%s, %s)" % (self.start, self.end)

    def __len__(self):
        return raw_interval_length(self.start, self.end)

    def __contains__(self, other):
        
        try:
            # do this if `other` is an Interval obj
            if (self.start <= other.start) and (self.end >= other.end):
                return True
            else:
                return False
        
        except AttributeError:
            if isinstance(other, int):
                # do this if `other` is an integer
                if (self.start <= other) and (self.end >= other):
                    return True
                else:
                    return False

    def __add__(self, other):
        """
        Returns a single merged new Interval object if overlap is detected, two new objects with original values
        otherwise.

        :param other: Another Interval object
        """

        if self.overlaps(other):
            new_start = min(self.start, other.start)
            new_end = max(self.end, other.end)
            return Interval(new_start, new_end)

        else:
            return Interval(self.start, self.end), Interval(other.start, other.end)


    def __sub__(self, other):
        """
        Returns portion of self NOT overlapped by other as new Interval Object(s).

        :param other: Another Interval object
        """
        return_intervals = []

        try:
            return_intervals.append(Interval(self.start, other.start))
        except e.NonsenseInterval:
            pass

        try:
            return_intervals.append(Interval(other.end, self.end))
        except e.NonsenseInterval:
            pass

        return return_intervals







    def __cmp__(self, other):
        """
        :param other: an interval/feature
        :returns int:
            * `-1` if `other` should sort to the right of `self`
            * `0` if `other` should sort exactly the same as `self`
            * `1` if `other` should sort to the left of `self`

        """
        self.start = self.start
        other.start = other.start

        if self.start < other.start:
            return -1

        if self.start == other.start:
            return 0

        if self.start > other.start:
            return 1

    def __eq__(self, other):
        """
        Returns `True` if `other` perfectly overlaps this feature, `False` otherwise.
        :param other: an interval/feature
        """
        self.start = self.start
        other.start = other.start
        self.end = self.end
        other.end = other.end

        if (self.start == other.start) and (self.end == other.end):
            return True
        else:
            return False

    def __gt__(self, other):
        """
        Returns `True` if `other` falls to the right even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        if self.end > other.end:
            return True
        else:
            return False


    def __lt__(self, other):
        """
        Returns `True` if `other` falls to the left even if `other` overlaps this feature,
        `False` otherwise.
        :param other: an interval/feature
        """
        if self.start < other.start:
            return True
        else:
            return False


    def grow(self, grow_by, add_to="both"):
        """
        Returns new Interval obj after growing the Interval at either
        the ``left``, ``right``, or ``both`` ends by ``grow_by`` amount.
    
        :param grow_by: number of bases to grow the edges of the interval
        :param add_to: {"left", "right", "both"}
        :return: (new_start, new_end)
        """
    
        assert isinstance(self.start, int)
        assert isinstance(self.end, int)

        if add_to == "both":
            grow_left = True
            grow_right = True
        elif add_to == "left":
            grow_left = True
            grow_right = False
        elif add_to == "right":
            grow_left = False
            grow_right = True
        else:
            raise e.InvalidOptionError(wrong_value=add_to,
                                       option_name="add_to",
                                       valid_values=('both', 'left', 'right'))
    
        merge_these = []
    
        if grow_left:
            merge_these.append(self.left_window(grow_by))
    
        if grow_right:
            merge_these.append(self.right_window(grow_by))
    
        merged = self.merge(merge_these)
    
        if len(merged) == 1:
            return merged
        else:
            msg = "`grow` should return a single new interval. Check your input then check the code. Would " \
                  "have returned: %s" % (str(merged))
            raise e.SanityCheckError(msg)
       
    def merge(self, intervals):
        """
        Returns a list of Interval objects (sorted from left to right by `start` bound) after overlapping test_intervals
        have been combined.
    
        :param intervals: iterable of Interval objs
        """
        # to_merge = sorted(deque(intervals + self))
        #
        #  = deck.popleft()
        #
        # while 1:
        #     merging = merged[-1]
        #     if merging.


    
    def left_window(self, win_size):
        """
        Returns a new Interval obj left of original bound describing a window of length `win_size` (see
        note).
    
        Note: Converts any new value less than `1` to `1`.
    
        :param win_size: size of window to the left.
        """
        new_start = self.start - win_size
        new_end = self.start - 1
    
        if new_start < 1:
            new_start = 1
        if new_end < 1:
            new_end = 1
    
        new_interval = Interval(new_start, new_end)
    
        return new_interval
    
    def right_window(self, win_size):
        """
        Returns a new Interval obj right of original bound describing a window of length `win_size`.
    
        :param win_size: size of window to the right.
        """
        new_start = self.end + 1
        new_end = self.end + win_size

        new_interval = Interval(new_start, new_end)

        return new_interval


    def overlaps(self, other):
        """
        Returns `True` if `self` overlaps with `other`.
        :param self: `list` of two `int` numbers representing **start**, **end** coordinates of a feature
        :param other: `list` of two `int` numbers representing **start**, **end** coordinates of a feature
        """

        # An overlap exists if the left-sorted interval contains the start of the right-sorted interval.

        left_interval, right_interval = sorted([self, other])

        if right_interval.start in left_interval:
            return True
        else:
            return False

#### Helper functions ####
def raw_interval_length(start, end):
    return end - start + 1




##########################


class SimpleFeature(object):




    def get_flank(self, length):
        # TODO: SimpleFeature.flank
        raise NotImplementedError()

    def get_rflank(self, length):
        # TODO: SimpleFeature.rflank

        raise NotImplementedError()

    def get_lflank(self, length):
        # TODO: SimpleFeature.lflank
        raise NotImplementedError()
