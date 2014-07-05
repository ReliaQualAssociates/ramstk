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


def simple_tabular_report(data, filename, metadata=None, title=None, f_format=1):
    """
    Function to create a simple report of tabular information.  Simple, in this
    case, means reports with one or more rows of one or more columns of
    information.  All rows have the same number of columns of data.  Formatting
    is minimal.

    :param dic data: the tabular data to print to the report.  Key is the index
                     of the row to print, value is a list of the data for each
                     column.  The first record is the list of column headings.
    :pram str filename: the full path to the file to save the report to.
    :param dic metadata: metadata to print to the report.  This can be any
                         information describing the reported output (e.g.,
                         hardware assembly the report is applicable to, the
                         date the report was generated, system revision the
                         report is applicable to, etc.).  Key is the
                         description of the metadata, value is the metadata
                         itself.  Keys will be printed in bold with their
                         associated value printed to the immediate right.
    :param str title: the title of the report.
    :param int f_format: the file format for the report.
                         * 1 = comma separated variable
                         * 2 = tab delimited
                         * 3 = Excel
                         * 4 = pdf
    """

    _n_records = len(data.keys())
    _n_fields = len(data[0])

    if f_format == 3:
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

        # Define the title font (headers, footers, etc.)
        _fntTitle = xlwt.Font()
        _fntTitle.name = 'Arial'
        _fntTitle.bold = True
        _fntTitle.height = 0x0190

        # Define the decorator font (headers, footers, etc.)
        _fntDecorator = xlwt.Font()
        _fntDecorator.name = 'Arial'
        _fntDecorator.bold = True
        _fntDecorator.height = 0x00F0

        _alnHeaders = xlwt.Alignment()
        _alnHeaders.horz = xlwt.Alignment.HORZ_CENTER
        _alnHeaders.vert = xlwt.Alignment.VERT_CENTER
        _alnHeaders.wrap = xlwt.Alignment.WRAP_AT_RIGHT

        # Define the font for the content (data).
        _fntContent = xlwt.Font()
        _fntContent.name = 'Arial'
        _fntContent.bold = False
        _fntContent.height = 0x00F0

        _styTitle = xlwt.XFStyle()
        _styTitle.font = _fntTitle

        _styDecorator = xlwt.XFStyle()
        _styDecorator.font = _fntDecorator

        _styHeaders = xlwt.XFStyle()
        _styHeaders.font = _fntDecorator
        _styHeaders.alignment = _alnHeaders

        _styContent = xlwt.XFStyle()
        _styContent.font = _fntContent

        # Create the workbook and one worksheet.
        _wb = xlwt.Workbook()

        # Initialize the row and columns variables.
        _row = 0
        _col = 0

        # Print the title if one was passed.
        if title is not None:
            _ws = _wb.add_sheet(title)
            _ws.write(_row, _col, title, _styTitle)
        else:
            _ws = _wb.add_sheet('RTK Report')
        _row += 2

        # Print the metadata if any was passed.
        if metadata is not None:
            for key in metadata.keys():
                _ws.write(_row, _col, key, _styDecorator)
                _ws.write(_row, _col+1, metadata[key], _styContent)
                _row += 1
        _row += 1

        # Print the data if any was passed.
        for key in data.keys():
            i = 0
            for j in range(len(data[key])):
                if key == 0:
                    _ws.write(_row, _col+j, data[key][j], _styHeaders)
                else:
                    _ws.write(_row, _col+j, data[key][j], _styContent)
            i += 1
            _row += 1

        _wb.save(filename)

    return False
