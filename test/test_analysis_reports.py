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

    def test_tabular_report(self):
        """
        Test of the simple tabular report generation function.
        """

        _data = {0: ['Assembly', 'Failure Intensity',
                     'Design Change Description', 'Design Factor',
                     'Manufacturing Change Description', 'Manufacturing Factor',
                     'Operation Change Description', 'Operation Factor'],
                 1: ['Example Sub-System 1', 0.00036,
                     'No changes', 1.0,
                     'No changes', 1.0,
                     'No changes', 1.0]}

        self.assertFalse(simple_tabular_report(_data, f_format=3))

