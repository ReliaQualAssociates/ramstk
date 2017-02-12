#!/usr/bin/env python
"""
Contains classes for creating analysis reports.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tabular.py is part of The RTK Project
#
# All rights reserved.

import xlwt


class ExcelReport(object):
    """
    This class is used to write reports to Excel.
    """

    # Set the font size with the height property.  Some common values
    # below:
    # Points    Decimal Value   Hex Value
    #   10           200          0x00C8
    #   12           240          0x00F0
    #   14           280          0x0118
    #   16           320          0x0140
    #   20           400          0x0190
    #   24           480          0x01E0
    #   32           640          0x0280

    def __init__(self, outfile, engine='xlwt'):
        """
        Method to initialize an instance of the ExcelWriter class.

        :param str outfile: the absolute path to the Excel file to write the
                            report to.
        :param str engine: the python module to use to write to Excel.
                           * xlwt for Excel 2003 (*.xls)
                           * openpyxl for Excel 2007 and 2010 (*.xlsx)
        """

        self.sheets = {}
        self.path = outfile

        if engine == 'xlwt':
            self.book = xlwt.Workbook()

            # Define some default styles.
            _font = xlwt.Font()
            _font.name = 'Arial'
            _font.bold = True
            _font.height = 0x0190
            self._styTitle = xlwt.XFStyle()
            self._styTitle.font = _font

            _font = xlwt.Font()
            _font.name = 'Arial'
            _font.bold = True
            _font.height = 0x00F0
            self._styHeaders = xlwt.XFStyle()
            self._styHeaders.font = _font

    def _get_worksheet(self, sheet_name):
        """
        Method to get the worksheet object from the dictionary of worksheets.

        :param str sheet_name: the name of the worksheet object to retrieve.
        :return: _worksheet
        :rtype: xlwt.Worksheet
        """

        if sheet_name in self.sheets:
            _worksheet = self.sheets[sheet_name]
        else:
            _worksheet = self.book.add_sheet(sheet_name)
            self.sheets[sheet_name] = _worksheet

        return _worksheet

    def write_title(self, title, sheet_name, style=None, srow=0, scol=0):
        """
        Method to write a title to the worksheet.

        :param str title: the title to write to the worksheet.
        :param str sheet_name: the name of the worksheet to write to.
        :param xlwt.Style style: font and other formatting information.
        :param int srow: the starting row in the worksheet.
        :param int scol: the starting column in the worksheet.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if style is None:
            style = self._styTitle

        _worksheet = self._get_worksheet(sheet_name)
        _worksheet.write(srow, scol, title, style)

        return False

    def write_metadata(self, metadata, sheet_name, style=None, srow=0, scol=0):
        """
        Method to write metadata to the worksheet.  Metadata is information
        describing the contents of the report.  For example, a mission profile
        report might contain the following metadata:

        Mission ID  1
        Mission New Mission 1
        Mission Time    10
        Report Date 2014-07-16

        :param pandas.DataFram metadata: a pandas.DataFrame() containing the
                                         metadata.  DataFrame columns are used
                                         as the row headings in the output
                                         file.
        :param str sheet_name: the name of the worksheet to write to.
        :param xlwt.Style style: font and other formatting information.
        :param int srow: the starting row in the worksheet.
        :param int scol: the starting column in the worksheet.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if style is None:
            style = self._styHeaders

        _worksheet = self._get_worksheet(sheet_name)
        for _col in metadata.columns.values.tolist():
            _worksheet.write(srow, scol, _col, style)
            _worksheet.write(srow, scol + 1, metadata[_col][0])
            srow += 1

        return False

    def write_content(self, content, sheet_name, style=None, srow=0, scol=0):
        """
        Method to write the report content to the worksheet.

        :param pandas.DataFram conent: a pandas.DataFrame() containing the
                                       content.  DataFrame columns are used
                                       as the column headings in the output
                                       file.  Each row in the data frame is
                                       written on a row in the output file.
        :param str sheet_name: the name of the worksheet to write to.
        :param xlwt.Style style: font and other formatting information.
        :param int srow: the starting row in the worksheet.
        :param int scol: the starting column in the worksheet.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if style is None:
            style = self._styHeaders

        _worksheet = self._get_worksheet(sheet_name)
        for _col in content.columns.values.tolist():
            _worksheet.write(srow, scol, _col, style)
            i = srow + 1
            for _row in content[_col].index.tolist():
                _worksheet.write(i, scol, content[_col][_row])
                i += 1
            scol += 1

        return False

    def close(self):
        """
        Method to save the output file.
        """

        self.book.save(self.path)
