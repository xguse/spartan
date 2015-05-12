# output.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 12/21/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
output.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

from spartan.utils import errors as e


def protein_name_from_argot_search(line, group_map):
    if line.startswith('#'):
        raise e.IgnoreThisError('Comment line')

    try:
        return group_map[line.split()[0]]
    except IndexError:
        raise e.IgnoreThisError('wonky line: %s' % line)

