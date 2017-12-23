#!/usr/bin/env python -O
"""
This is the test class for testing reporting functions.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       test_analysis_reports.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import unittest
import os
import sys
import pandas as pd

sys.path.insert(
    0,
    dirname(dirname(dirname(__file__))) + "/rtk",
)

from rtk._reports_.tabular import ExcelReport


class TestAnalysisReports(unittest.TestCase):

    xcloutfile = '/home/andrew/RTKTestOutput.xls'

    data = pd.DataFrame(
        [['Example Sub-System 1', 0.00036
          ], ['No changes', 1.0], ['No changes', 1.0], ['No changes', 1.0],
         ['No changes', 1.0], ['No changes', 1.0], ['No changes', 1.0]],
        columns=['Assembly', 'Failure Intensity'])

    metadata = pd.DataFrame(
        [(0, 'Test Metadata', 100.0, '2014-01-01')],
        columns=['Test Output ID', 'Test', 'Test Time', 'Report Date'])

    def setUp(self):
        """
        Setting up the analysis reports test fixtures.
        """

        self._DUT = ExcelReport(self.xcloutfile, engine='xlwt')

    def test_create_excel_writer(self):
        """
        Test that the tabular report __init__ function returns an instance
        of ExcelReport.
        """

        self.assertTrue(isinstance(self._DUT, ExcelReport))

    def test_write_title(self):
        """
        Test that the ExcelReport class can write the report title to file.
        """

        self.assertFalse(
            self._DUT.write_title("Test Report", 'Sheet 1', srow=0, scol=0))
        self._DUT.book.save(self.xcloutfile)

    def test_write_metadata(self):
        """
        Test that the ExcelReport class can write the metadata to file.
        """

        self.assertFalse(
            self._DUT.write_metadata(self.metadata, 'Sheet 1', srow=3, scol=0))
        self._DUT.book.save(self.xcloutfile)

    def test_write_content(self):
        """
        Test that the ExcelReport class can write the contents to file.
        """

        self.assertFalse(
            self._DUT.write_content(self.data, 'Sheet 1', srow=12, scol=0))
        self._DUT.book.save(self.xcloutfile)
