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
from collections import defaultdict

import networkx as nx
import pyfasta

from spartan.utils.annotations import intervals
from spartan.utils.misc import Bunch

__author__ = 'Gus Dunn'

##### helper functions #####


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


def parse_gff3(gff3_path):
    """

    :param gff3_path:
    """

    gff3_lines = open(gff3_path, 'rU')

    for line_no, data in enumerate(gff3_lines):
        if data.startswith('#'):
            continue
        else:
            feature = SimpleFeatureGFF3(data)
            feature.line_no = line_no + 1  # to correct for python vs file index
            yield feature

#############################


class GFF3(object):
    def __init__(self, gff3_path, fasta_path=False):

        self.gff3_path = gff3_path
        self.fasta_path = fasta_path
        self.parents_graph = nx.Graph()
        self.feature_db = dict()
        self.common_to_uniq_id = dict()
        self.uniq_to_common = dict()
        self.seqids = set()
        self.types = set()
        self.sources = set()

        self.install_gff3_features_from_file(self.gff3_path)

        if fasta_path:
            self.install_fasta_access()

    def install_gff3_features_from_file(self, gff3_path):
        features = parse_gff3(self.gff3_path)

        for feature in features:
            # add feature to feature_db
            self.set_feature_uniq_id(feature)
            feature.gff3_container = self  # provide access to the gff obj by the feature
            self.feature_db[feature.uniq_id] = feature

            try:
                self.common_to_uniq_id[feature.data.attributes.ID] = feature.uniq_id
            except AttributeError:
                pass

            try:
                self.uniq_to_common[feature.uniq_id] = feature.data.attributes.ID
            except AttributeError:
                pass

            # record the range of occurrences for certain fields
            self.seqids.add(feature.data.seqid)
            self.types.add(feature.data.type)
            self.sources.add(feature.data.source)

        # add parent:child relationships to parent_graph
        for uid, feat in self.feature_db.iteritems():
            try:
                p = self.common_to_uniq_id[feat.data.attributes.Parent]
                self.parents_graph.add_edge(uid, p)
            except AttributeError:
                pass

    def set_feature_uniq_id(self, feature):
        try:
            u_id = '%s:%s:%s:%s:%s:%s:%s' % (feature.line_no, feature.data.seqid, feature.data.type,
                                             feature.data.start, feature.data.end, feature.data.strand,
                                             feature.data .attributes.ID)
        except AttributeError:
            u_id = '%s:%s:%s:%s:%s:%s' % (feature.line_no, feature.data.seqid, feature.data.type, feature.data.start,
                                          feature.data.end, feature.data.strand)
        feature.uniq_id = u_id

    def install_fasta_access(self):
        self.fasta_db = pyfasta.Fasta(self.fasta_path, flatten_inplace=True)


class SimpleFeatureGFF3(intervals.SimpleFeature):

    def __init__(self, gff3_data, start=None, end=None):
        """
            Initializes `SimpleFeatureGFF3` object with the fields from a single GFF3 line.

            :param gff3_data: either a single gff3 file line or a dict of proper information.
            """
        super(SimpleFeatureGFF3, self).__init__(start, end)
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

        self.parents = defaultdict(list)
        self.children = defaultdict(list)

    #@staticmethod # TODO: is this useful?
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
                    attrib_bunch['unnamed_attributes'].append(key_val)
                except KeyError:
                    attrib_bunch['unnamed_attributes'] = [key_val]

        return attrib_bunch

    def get_range(self):
        return self.data.start, self.data.end

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
        new_feature_data['source'] = 'spartan_derived'
        new_feature_data['type'] = 'upstream_region'

        new_feature_obj = SimpleFeatureGFF3(new_feature_data)

        return new_feature_obj


    def get_downstream(self, length):
        """
        Return new `SimpleFeatureGFF3` representing `length` downstream of current feature.
        :param length:
        :return: SimpleFeatureGFF3
        """
        if self.data.strand > 0:
            new_coords = intervals.right_window_coords(length, self.data.end)
        else:
            new_coords = intervals.left_window_coords(length, self.data.start)

        new_feature_data = deepcopy(dict(self.data))

        new_feature_data['start'] = new_coords[0]
        new_feature_data['end'] = new_coords[1]
        new_feature_data['source'] = 'spartan_derived'
        new_feature_data['type'] = 'downstream_region'

        new_feature_obj = SimpleFeatureGFF3(new_feature_data)

        return new_feature_obj

    def get_parent_ID(self):
        """


        :return: `ID` of parent feature
        """
        return self.data.attributes.Parent

    def set_parent_ID(self, ID):
        self.data.attributes.Parent = ID

    def get_dna_sequence(self):
        try:
            vitals = self.get_vitals()

            return self.gff3_container.fasta_db.sequence({'chr': vitals.seqid,
                                                          'start': vitals.start, 'stop': vitals.end,
                                                          'strand': vitals.strand})
        except:
            raise

    def get_vitals(self):

        vitals = Bunch()
        vitals.seqid = self.data.seqid
        vitals.start = self.data.start
        vitals.end = self.data.end
        vitals.strand = self.data.strand
        return vitals