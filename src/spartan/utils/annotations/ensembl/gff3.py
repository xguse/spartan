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
from copy import deepcopy

from spartan.utils.annotations import intervals
from spartan.utils.misc import Bunch

__author__ = 'Gus Dunn'


def convert_strand(strand):
    """

    :param strand:
    """
    strand_dict = {'+': 1,
                   '-': -1,
                   '1': 1,
                   '-1': -1,
                   '.': 1}

    return strand_dict[strand]


class SimpleFeatureGFF3(intervals.SimpleFeature):

    def __init__(self, gff3_data):
        # TODO: SimpleFeatureGFF3.__init__
        """
        Initializes `SimpleFeatureGFF3` object with the fields from a single GFF3 line.

        :param gff3_data: either a single gff3 file line or a dict of proper information.
        """
        self.data = Bunch()
        if isinstance(gff3_data, str):
            fields = gff3_data.rstrip('\n').split('\t')

            self.data.seqid = fields[0]
            self.data.source = fields[1]
            self.data.type = fields[2]
            self.data.start = int(fields[3])
            self.data.end = int(fields[4])
            self.data.score = fields[5]
            self.data.strand = convert_strand(fields[6])
            self.data.phase = fields[7]
            self.data.attributes = self.parse_attributes(fields[8])
        elif isinstance(gff3_data, dict):
            # NOTE: in this case you will need to have pre-parsed the `attributes` data if included.
            for k, v in gff3_data.iteritems():
                self.data.__setattr__(k, v)

    @staticmethod
    def parse_attributes(self, attributes):
        # TODO: SimpleFeatureGFF3._parse_attributes
        """
        Returns a `dict`-like object `Bunch` from the key/value data encoded in the attributes string.

        :param attributes: attributes string from a GFF3 line.
        """
        attrib_pairs = attributes.split(';')

        attrib_bunch = Bunch()

        for key_val in attrib_pairs:
            try:
                k, v = key_val.split('=')
                attrib_bunch[k] = v
            except ValueError:
                try:
                    attrib_bunch['unnamed'].append(key_val)
                except KeyError:
                    attrib_bunch['unnamed'] = [key_val]

        return attrib_bunch

    def get_upstream(self, length):
        # TODO: !! TEST gff3.SimpleFeatureGFF3.get_upstream()
        """
        Return new `SimpleFeatureGFF3` representing `length` upstream of current feature.
        :param length:
        :return: SimpleFeatureGFF3
        """
        if self.data.strand > 0:
            new_coords = intervals.left_window_coords(length, self.data.start)
        else:
            new_coords = intervals.right_window_coords(length, self.data.end)

        new_feature_data = deepcopy(dict(self.data))

        new_feature_data['start'] = new_coords[0]
        new_feature_data['end'] = new_coords[1]

        new_feature_obj = SimpleFeatureGFF3(new_feature_data)

        return new_feature_obj


    def get_downstream(self, length):
        """
        Return new `SimpleFeatureGFF3` representing `length` downstream of current feature.
        :param length:
        :return: SimpleFeatureGFF3
        """
        raise NotImplementedError()

def parse_gff3(gff3_path):
    """

    :param gff3_path:
    """

    gff3_lines = open(gff3_path, 'rU')

    for line in gff3_lines:
        if line.startswith('#'):
            continue
        else:
            yield SimpleFeatureGFF3(line)
