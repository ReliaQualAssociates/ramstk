#!/usr/bin/env python -O
"""
This is the test class for testing Revision module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       test_survival_data.py is part of The RTK Project
#
# All rights reserved.

import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(".."))

import numpy as np

import rtk.configuration as _conf
import rtk.utilities as _util
import rtk.sqlite as _sqlite
from rtk.function import Function


class TestFunction(unittest.TestCase):
    """
    Class to test Function module algorithms.
    """

    def setUp(self):
        """
        Setting up the Function class test fixtures.
        """

        # Read the configuration file.
        _util.read_configuration()

        _conf.MODE = 'developer'

        self.COMDB = _sqlite.SQLite3Interface(self)
        _database = _conf.SITE_DIR + '/' + _conf.RTK_COM_INFO[2] + '.rfb'
        self.ComCnx = self.COMDB.get_connection(_database)

        self.DB = _sqlite.SQLite3Interface(self)
        _database = _conf.PROG_DIR + '/TestDB.rtk'
        self.ProgCnx = self.DB.get_connection(_conf.RTK_PROG_INFO[2])

        self._DUT = Function(self)

    def test_function_create(self):
        """
        Test to ensure the current instance is of the Function class.
        """

        self.assertTrue(isinstance(self._DUT, Function))
        # self.assertEqual(_conf.RTK_MTIME, 10.0)
        # self.assertEqual(_conf.FRMULT, 1.0)

    def test_default_attribute_values(self):
        """
        Test to ensure default values for public attributes are correct.
        """

        self.assertEqual(self._DUT.revision_id, 0)
        self.assertEqual(self._DUT.function_id, 0)
        self.assertEqual(self._DUT.code, '')
        self.assertEqual(self._DUT.cost, 0.0)
        self.assertEqual(self._DUT.hazard_rate, 0.0)
        self.assertEqual(self._DUT.mission_hazard_rate, 0.0)
        self.assertEqual(self._DUT.mtbf, 0.0)
        self.assertEqual(self._DUT.mission_mtbf, 0.0)
        self.assertEqual(self._DUT.mpmt, 0.0)
        self.assertEqual(self._DUT.mcmt, 0.0)
        self.assertEqual(self._DUT.mttr, 0.0)
        self.assertEqual(self._DUT.mmt, 0.0)
        self.assertEqual(self._DUT.availability, 0.0)
        self.assertEqual(self._DUT.mission_availability, 0.0)
        self.assertEqual(self._DUT.remarks, '')
        self.assertEqual(self._DUT.n_modes, 0)
        self.assertEqual(self._DUT.n_parts, 0)
        self.assertEqual(self._DUT.parent_id, '')
        self.assertEqual(self._DUT.level, 0)
        self.assertEqual(self._DUT.safety_critical, 1)

    def test_calculate(self):
        """
        Test of the Function class calculations.
        """

        _results = self._DUT.calculate(None)

        self.assertEqual(_results, 1)

