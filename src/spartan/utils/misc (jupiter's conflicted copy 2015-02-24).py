# *****************************************************************************
#  misc.py (part of the spartan package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#  Licensed under the GNU General Public License 3.0 license.
# ******************************************************************************

"""
####################
misc.py
####################
Code facilitating random aspects of this package.
"""
import os
import sys
import inspect
import smtplib
import base64
import time
import re


class Tristate(object):
    def __init__(self, value=None):
        number_map = {True: 1, False: 0, None: None}
        if any(value is v for v in (True, False, None)):
            self.value = value
            self.__value = number_map[self.value]
        else:
            raise ValueError("Tristate value must be True, False, or None")

    def __eq__(self, other):
        return self.value is other

    def __ne__(self, other):
        return self.value is not other

    def __bool__(self):  # Python 3: __bool__()
        raise TypeError("Tristate value may not be used as implicit Boolean")

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Tristate(%s)" % self.value

    def __add__(self, other):
        if isinstance(other, Tristate):
            try:
                return other.__value + self.__value
            except TypeError as exc:
                if "'NoneType' and 'int'" in exc.message:
                    pass
                elif "'int' and 'NoneType'" in exc.message:
                    pass
                else:
                    raise exc

                return other.__value
        else:
            try:
                return other + self.__value
            except TypeError as exc:
                if "'NoneType' and 'int'" in exc.message:
                    pass
                elif "'int' and 'NoneType'" in exc.message:
                    pass
                else:
                    raise exc

                return other

    __radd__ = __add__


def split_stream(stream, divisor):
    """
    Yields stream items grouped into tuples with length `divisor` including the remainder.
    """

    group = []

    for item in stream:
        group.append(item)

        if len(group) == divisor:
            yield_me = tuple(group[:])
            group = []
            yield yield_me

    yield group


def get_version_number(path_to_setup):
    """
    Provides access to current version info contained in setup.py
    """
    
    setup_path = path_to_setup
    with open(setup_path, 'rb') as f:
        match = re.search(
            '\s*[\'"]?version[\'"]?\s*[=:]\s*[\'"]?([^\'",]+)[\'"]?',
            f.read().decode('utf-8'), re.I)

    if match:
        version_string = match.group(1)
        return version_string

    else:
        print(("No version definition found in ", setup_path))


class Bunch(dict):
    """
    A dict like class to facilitate setting and access to tree-like data.  Allows access to dictionary keys through 'dot' notation: "yourDict.key = value".
    """
    def __init__(self, *args, **kwds):
        super(Bunch,self).__init__(*args,**kwds)
        self.__dict__ = self


def bunchify(dict_tree):
    """
    Traverses a dictionary tree and converts all sub-dictionaries to Bunch() objects.
    """
    for k,v in dict_tree.items():
        if type(v) == type({}):
            dict_tree[k] = bunchify(dict_tree[k])
    return Bunch(dict_tree)


def whoami():
    """
    Returns the name of the currently active function.
    """
    return inspect.stack()[1][3]


def get_time():
    """
    Return system time formatted as 'YYYY:MM:DD-hh:mm:ss'.
    """
    t = time.localtime()
    return time.strftime('%Y.%m.%d-%H:%M:%S',t)
        

def uniques(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]


def slidingWindow(sequence, winSize, step=1):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable."""

    # Verify the inputs
    try: it = iter(sequence)
    except TypeError:
        raise Exception("**ERROR** sequence must be iterable.")
    if not ((type(winSize) == type(0)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > winSize:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if winSize > len(sequence):
        raise Exception("**ERROR** winSize must not be larger than sequence length.")

    # Pre-compute number of chunks to emit
    numOfChunks = ((len(sequence)-winSize)/step)+1

    # Do the work
    for i in range(0,numOfChunks*step,step):
        yield sequence[i:i+winSize]


def fold_seq(seq, lineLen=70):
    return [seq[i:i+lineLen] for i in range(0, len(seq), lineLen)]
