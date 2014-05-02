# coord_conversions.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 5/1/14
#
# Please see the license info in the root folder of this package.

"""
###########################################
coord_conversions.py
###########################################

Mission:
Provide code to convert start/stop coordinate pairs to and from specific conventions such as BED or GTF.

"""
__author__ = 'Gus Dunn'


def human_to_bed_chrom_start_stop(start, stop):
    """
    Returns a tuple containing chromosome coords in BED convention.

    :param start: first bp coordinate of subsequence (chromosome starts with 1 not 0).
    :param stop: last bp coordinate of subsequence (chromosome starts with 1 not 0).
    :return: bed_coords = (bed_start, bed_stop)
    """
    bed_start = start-1
    bed_stop = stop

    bed_coords = (bed_start, bed_stop)

    return bed_coords
