# spreadsheets.py is part of the 'spartan' package.
# It was written by Gus Dunn and was created on 6/19/14.
#
# Please see the license info in the root folder of this package.

"""
=================================================
spreadsheets.py
=================================================
Purpose:
Helper functions to open and manipulate excel-type spreadsheets.
"""

__author__ = 'Gus Dunn'


import csv
import os

import xlrd
import arrow

try:
    from sanitize import sanitize_path_fragment
except ImportError:
    raise ImportError('''For now you must install my fork of `sanitize`: You can do so with:
    `pip install git+ssh://git@github.com/xguse/sanitize.git@gus_mod#egg=sanitize` or manually downloading/installing
     the code at that url.''')


def sanitize_file_name(file_name):
    return sanitize_path_fragment(file_name, additional_illegal_characters=[u' '])


def get_workbook(workbook_path):
    return xlrd.open_workbook(workbook_path)


def get_worksheets(workbook):
    return workbook.sheets()


def get_rows(worksheet):
    """
    Returns a generator for cleaner iteration over `worksheet.row(row_i to row_N)`.

    :param worksheet: xlrd worksheet object
    """
    for i in range(worksheet.nrows):
        yield worksheet.row(i)


def get_row_values(worksheet):
    """
    Returns a generator for cleaner iteration over the `worksheet.row_values(row_i to row_N)`.

    :param worksheet: xlrd worksheet object
    """
    for i in range(worksheet.nrows):
        yield worksheet.row_values(i)


def worksheet_to_csv(worksheet, csv_path):
    """
    Writes data from `worksheet` in csv format to new file: `csv_path`.

    :param worksheet: xlrd sheet object
    :param csv_path: path to new csv file
    :return: `None`
    """
    csv_file = open(csv_path, 'wb')
    csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
    for row_values in get_row_values(worksheet):
        csv_writer.writerow(row_values)
    csv_file.close()


def workbook_to_csv_files(workbook_path):
    """
    Given a `workbook_path`, convert all worksheets to individual csv files with names
    constructed from the workbook name and worksheet names.

    :param workbook_path: path to the workbook (.xls file)
    """

    workbook_name = sanitize_file_name(os.path.basename(unicode(workbook_path)))
    workbook_dir = os.path.dirname(os.path.realpath(workbook_path))

    workbook = get_workbook(workbook_path)
    worksheets = get_worksheets(workbook)

    for worksheet in worksheets:
        # TODO: add code to test for sheets with same name and disambiguate if found

        worksheet_name = sanitize_file_name(worksheet.name)
        csv_path = "%s/%s--%s.csv" % (workbook_dir, workbook_name, worksheet_name)
        worksheet_to_csv(worksheet, csv_path)


def get_date(value, datemode):

    """
    Returns an `arrow` date object
    :param value: `xlrd` produced date float
    :param datemode: the datemode of the workbook
    """
    date_tuple = xlrd.xldate_as_tuple(value, datemode)
    return arrow.get(*date_tuple)