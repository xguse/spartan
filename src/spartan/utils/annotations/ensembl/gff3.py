# gff3 is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 5/3/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
gff3
=================================================
Purpose:
Handle parsing and storage of gff3 data
"""
from spartan.utils.annotations import intervals

__author__ = 'Gus Dunn'


class SimpleFeatureGFF3(intervals.SimpleFeature):

    def __init__(self, start, end, seqid=None, source=None, type=None,
                 score=None, strand=None, phase=None, attributes=None):
        # TODO: SimpleFeatureGFF3.__init__
        """
        Initializes `SimpleFeatureGFF3` object with the fields from a single GFF3 line.

        :param start:
        :param end:
        :param seqid:
        :param source:
        :param type:
        :param score:
        :param strand:
        :param phase:
        :param attributes:
        """
        pass

    def _parse_attributes(self, attributes):
        # TODO: SimpleFeatureGFF3._parse_attributes
        """
        Returns a `dict`-like object from the key/value data encoded in the attributes string.

        :param attributes: attributes string from a GFF3 line.
        """