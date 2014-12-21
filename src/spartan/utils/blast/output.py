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


def filter_for_argot(path, protein_names):
    """
    Yields lines from `path` that represent blast results for any protein listed in `protein_names` as strings.
    """

    names = set(protein_names)

    with open(path, 'rU') as blast_file:
        for line in blast_file:
            if line.split()[0] in names:
                yield line
