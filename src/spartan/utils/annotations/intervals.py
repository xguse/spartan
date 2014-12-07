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
__author__ = 'Gus Dunn'

import ipdb

import itertools
import operator

import pybedtools as pbt

import spartan.utils.errors as e


# class Interval(pbt.Interval):
class Interval(object):
    """
    Represents a single, strandless, start/end interval.
    """

    def __init__(self, start, end, seq=None, one_to_zero=False):

        """
        If ``one_to_zero``, conversion from 1-based(closed) to 0-based(half-open) will be performed.
        :param start: left most coordinate.
        :param end: right most coordinate.
        """
        assert isinstance(start, int)
        assert isinstance(end, int)

        try:
            assert start <= end
        except AssertionError:
            raise e.NonsenseInterval

        if seq is not None:
            self.seq = seq
        else:
            self.seq = 'unnamed'

        if one_to_zero:
            self.start = start - 1
            self.end = end

        else:
            self.start = start
            self.end = end

        self._range = frozenset(self.range())

    def __str__(self):
        return "%s-%s" % (self.start, self.end)

    def __repr__(self):
        return "Interval(%s, %s)" % (self.start, self.end)

    def __len__(self):
        return self.end - self.start

    def __contains__(self, other):
        """
        Returns `True` if `other` is completely contained within `self`, `False` otherwise.
        """
        try:
            # do this if `other` is an Interval obj
            return self._range >= other._range
        
        except AttributeError:
            if isinstance(other, int):
                # do this if `other` is an integer
                return other in self._range
            else:
                raise e.InvalidOptionError(wrong_value=other,
                                           option_name='other',
                                           valid_values=[type(self).__name__, type(1).__name__])

    def __add__(self, other):
        """
        Returns a single merged new Interval object if overlap is detected, ``None`` otherwise.

        :param other: Another Interval object
        """

        if self.overlaps(other):
            new_start = min(self.start, other.start)
            new_end = max(self.end, other.end)
            return Interval(new_start, new_end)

        else:
            return None


    def __sub__(self, other):
        """
        Returns portion(s) of self NOT overlapped by other as new Interval Object(s) as long as other overlaps self
        SOMEWHERE; returns ``None`` otherwise.

        :param other: Another Interval object
        """
        return_intervals = []

        if self.overlaps(other):
            try:
                return_intervals.append(Interval(self.start, other.start))
            except e.NonsenseInterval:
                pass

            try:
                return_intervals.append(Interval(other.end, self.end))
            except e.NonsenseInterval:
                pass

            return return_intervals

        else:
            return None


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

    def range(self):
        """
        Returns ``range(self.start, self.end)``
        """
        return range(self.start, self.end)

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
    
        merged = list(self.merge(merge_these))
    
        if len(merged) == 1:
            return merged[0]
        else:
            msg = "`grow` should return a single new interval. Check your input then check the code. Would " \
                  "have returned: %s" % (str(merged))
            raise e.SanityCheckError(msg)
       
    def merge(self, intervals):
        """
        Returns a generator of Interval objects (sorted from left to right by `start` bound) after overlapping
        test_intervals
        have been combined.
    
        :param intervals: iterable of Interval objs
        """
        _range = operator.attrgetter('_range')

        assert isinstance(intervals, list)
        intervals.append(self)

        merged_positions = set()
        merged_positions.update(*map(_range,intervals))

        new_intervals = intervals_from_positions(sorted(list(merged_positions))) # returns generator
        return new_intervals


    def separation(self, other):
        """
        Returns the genomic distance separating the two Intervals if on the same seq, `None` otherwise.
        :param other: Interval obj
        """
        #TODO: finish coding separation method

        assert self.seq == other.seq
        intervals = [self, other]
        left, right = sorted(intervals)

        sep = right.start - left.end

        if sep > 0:
            return sep
        else:
            return 0


    
    def left_window(self, win_size):
        """
        Returns a new Interval obj left of original bound describing a window of length `win_size` (see
        note).
    
        Note: Converts any new value less than `1` to `1`.
    
        :param win_size: size of window to the left.
        """
        new_start = self.start - win_size
        new_end = self.start
    
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
        new_start = self.end
        new_end = self.end + win_size

        new_interval = Interval(new_start, new_end)

        return new_interval


    def overlaps(self, other):
        """
        Returns `True` if `self` overlaps with `other`.
        :param self: `list` of two `int` numbers representing **start**, **end** coordinates of a feature
        :param other: `list` of two `int` numbers representing **start**, **end** coordinates of a feature
        """

        # any intersection of the ._range sets is an overlap.
        if self._range.intersection(other._range):
            return True
        else:
            return False


#### Helper functions ####
def intervals_from_positions(positions, one_to_zero=False):
    """
    Returns a generator of `Interval` objects initialized based on groups of any contiguous ranges of numbers found
    in the `positions` list.

    """

    positions.sort()
    pos_lists = get_contiguous_integers(positions)

    for plist in pos_lists:
        start = plist[0]
        end = start + len(plist) # use the start + len bc of the half-open nature of range definitions.
        yield Interval(start=start, end=end, one_to_zero=one_to_zero)


def get_contiguous_integers(integer_list):
    """
    Returns a generator of lists containing contiguous numbers.
    """
    for k, g in itertools.groupby(enumerate(integer_list), lambda (i, x): i - x):
        yield map(operator.itemgetter(1), g)




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
