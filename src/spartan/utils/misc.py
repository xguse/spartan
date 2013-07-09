#*****************************************************************************
#  misc.py (part of the spartan package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#  Licensed under the GNU General Public License 3.0 license.
#******************************************************************************

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

from collections import defaultdict


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
        print("No version definition found in ", setup_path)


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
    for k,v in dict_tree.iteritems():
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