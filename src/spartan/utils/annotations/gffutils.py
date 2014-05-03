# gffutils.py is part of the 'spartan' package.
# It was written by Gus Dunn
# and was created on 5/1/14
#
# Please see the license info in the root folder of this package.


"""
##############################################
gffutils.py
##############################################

"""
import os

from sqlite3 import OperationalError

import gffutils

__author__ = 'Gus Dunn'


def load_genes(gff3_path):

    """
    Tries to load a gffutils database file first,
    if this fails, tries to create one,
    finally if the file is empty after it all, deletes the file.

    :param gff3_path: path to a gff3 file
    :return: gffutils database connection
    """
    gff3_db_path = gff3_path+'.db'

    try:
        db = gffutils.FeatureDB(gff3_db_path)
        return db
    except OperationalError:
        db = gffutils.create_db(gff3_path, dbfn=gff3_db_path, force=True, keep_order=False, merge_strategy='merge')

        return db
    finally:
        fstat = os.stat(gff3_db_path)

        if fstat.st_size == 0:
            os.remove(gff3_db_path)
        else:
            pass