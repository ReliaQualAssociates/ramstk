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

import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(".."))

from rtk._reports_.tabular import *


class TestAnalysisReports(unittest.TestCase):

    xcloutfile = '/home/andrew/RTKTestOutput'

    data = {0: ['Assembly', 'Failure Intensity',
                'Design Change Description', 'Design Factor',
                'Manufacturing Change Description', 'Manufacturing Factor',
                'Operation Change Description', 'Operation Factor',
                'Loads/Stresses Change Description', 'Loading Factor',
                'Serviceability Change Description', 'Serviceability Factor',
                'Supply Chain Change Description', 'Supply Chain Factor'],
            1: ['Example Sub-System 1', 0.00036,
                'No changes', 1.0,
                'No changes', 1.0,
                'No changes', 1.0,
                'No changes', 1.0,
                'No changes', 1.0,
                'No changes', 1.0]}

    metadata = {'Assembly:': 'Example Sub-System 1',
                'Report Date:': '2014-06-28'}

    def test_tabular_report_data_only(self):
        """
        Test of the simple tabular report generation function
        passing only data.
        """

        self.assertFalse(simple_tabular_report(self.data,
                                               self.xcloutfile + '1.xls',
                                               f_format=3))

    def test_tabular_report_data_metadata(self):
        """
        Test of the simple tabular report generation function
        passing data and metadata.
        """

        self.assertFalse(simple_tabular_report(self.data,
                                               self.xcloutfile + '2.xls',
                                               metadata=self.metadata,
                                               f_format=3))

    def test_tabular_report_data_metadata_title(self):
        """
        Test of the simple tabular report generation function
        passing data, metadata, and a title.
        """

        self.assertFalse(simple_tabular_report(self.data,
                                               self.xcloutfile + '3.xls',
                                               metadata=self.metadata,
                                               title='Test Report',
                                               f_format=3))
