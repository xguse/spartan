# xls_to_csvs.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 06/20/14.
#
# Please see the license info in the root folder of this package.

"""
=================================================
xls_to_csvs.py
=================================================
Purpose:

"""

import docopt
from spartan.utils.spreadsheets import workbook_to_csv_files

__author__ = 'Gus Dunn'

usage = """
Usage:
xls_to_csvs XLS_FILE

Arguments:
  XLS_FILE     input xls file

Options:
  -h --help    show this

"""


def main():
    args = docopt.docopt(usage)

    workbook_to_csv_files(args['XLS_FILE'])
