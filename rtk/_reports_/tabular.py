#!/usr/bin/env python
"""
Contains functions for creating analysis reports.
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

import sys
from os import name

import xlwt


def simple_tabular_report(data, f_format=1):
    """
    Function to create a simple report of tabular information.  Simple, in this
    case, means reports with one or more rows of one or more columns of
    information.  All rows have the same number of columns of data.  Formatting
    is minimal.

    :param dic data: the tabular data to print to the report.  Key is the index
                     of the row to print, value is a list of the data for each
                     column.  The first record is the list of column headings.
    :param int f_format: the file format for the report.
                         * 1 = comma separated variable
                         * 2 = tab delimited
                         * 3 = Excel
                         * 4 = pdf
    """

    _n_records = len(data.keys())
    _n_fields = len(data[0])

    if format == 3:
        # Define the decorator font (headers, footers, etc.)
        _fntDecorator = xlwt.Font()
        _fntDecorator.name = 'Arial'
        _fntDecorator.bold = True

        # Define the font for the content (data).
        _fntContent = xlwt.Font()
        _fntContent.name = 'Arial'
        _fntContent.bold = False

        _styDecorator = xlwt.XFStyle()
        _styDecorator.font = _fntDecorator

        _styContent = xlwt.XFStyle()
        _styContent.font = _fntContent

        _wb = xlwt.Workbook()
        _ws = _wb.add_sheet(data[1][0])

        for j in range(_n_fields):
            _ws.write(5, j, data[0][j], _styDecorator)

        for i in 1, range(_n_records):
            for j in range(_n_fields):
                try:
                    _row = i + 5
                    _col = j
                    _ws.write(_row, _col, data[i][j], _styContent)
                except TypeError:
                    print _row, _col

        _wb.save('/home/andrew/RTKTestOutput.xls')

    return False
