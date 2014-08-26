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
from rtk.revision import Revision


class TestRevision(unittest.TestCase):
    """
    Class to test Revision module algorithms.
    """

    def setUp(self):
        """
        Setting up the Revision class test fixtures.
        """

        # Read the configuration file.
        _util.read_configuration()

        _conf.MODE = 'developer'

        self.COMDB = _sqlite.SQLite3Interface(self)
        _database = _conf.SITE_DIR + '/' + _conf.RTK_COM_INFO[2] + '.rfb'
        self.ComCnx = self.COMDB.get_connection(_database)

        self.DB = _sqlite.SQLite3Interface(self)
        self.ProgCnx = self.DB.get_connection(_conf.RTK_PROG_INFO[2])

        self._revision = Revision(self)

    def test_revision_create(self):
        """
        Test to ensure the current instance is of the Revision class.
        """

        self.assertTrue(isinstance(self._revision, Revision))
        # self.assertEqual(_conf.RTK_MTIME, 10.0)
        # self.assertEqual(_conf.FRMULT, 1.0)

    def test_default_attribute_values(self):
        """
        Test to ensure default values for public attributes are correct.
        """

        self.assertEqual(self._revision.revision_id, 0)
        self.assertEqual(self._revision.name, '')
        self.assertEqual(self._revision.n_parts, 0)
        self.assertEqual(self._revision.cost, 0.0)
        self.assertEqual(self._revision.cost_per_failure, 0.0)
        self.assertEqual(self._revision.cost_per_hour, 0.0)
        self.assertEqual(self._revision.active_hazard_rate, 0.0)
        self.assertEqual(self._revision.dormant_hazard_rate, 0.0)
        self.assertEqual(self._revision.software_hazard_rate, 0.0)
        self.assertEqual(self._revision.hazard_rate, 0.0)
        self.assertEqual(self._revision.mission_hazard_rate, 0.0)
        self.assertEqual(self._revision.mtbf, 0.0)
        self.assertEqual(self._revision.mission_mtbf, 0.0)
        self.assertEqual(self._revision.reliability, 0.0)
        self.assertEqual(self._revision.mission_reliability, 0.0)
        self.assertEqual(self._revision.mpmt, 0.0)
        self.assertEqual(self._revision.mcmt, 0.0)
        self.assertEqual(self._revision.mttr, 0.0)
        self.assertEqual(self._revision.mmt, 0.0)
        self.assertEqual(self._revision.availability, 0.0)
        self.assertEqual(self._revision.mission_availability, 0.0)
        self.assertEqual(self._revision.remarks, '')
        self.assertEqual(self._revision.code, '')
        self.assertEqual(self._revision.program_time, 0.0)
        self.assertEqual(self._revision.program_time_se, 0.0)
        self.assertEqual(self._revision.program_cost, 0.0)
        self.assertEqual(self._revision.program_cost_se, 0.0)

    def test_reliability_calculations(self):
        """
        Test to ensure no errors are raised when calculating the revision
        and that the results are correct within seven decimal places.
        """

        self.assertEqual(self._revision.calculate(None), False)
        self.assertEqual(self._revision.cost, 199.03)
        self.assertEqual(self._revision.active_hazard_rate, 0.0000542)
        self.assertEqual(self._revision.dormant_hazard_rate, 0.00000342)
        self.assertEqual(self._revision.software_hazard_rate, 0.00142)
        self.assertEqual(self._revision.n_parts, 112)
        self.assertEqual(self._revision.mission_hazard_rate, 0.0014542)
        self.assertEqual(self._revision.mpmt, 20.0)
        self.assertAlmostEqual(self._revision.mcmt, 2.099958)
        self.assertAlmostEqual(self._revision.mttr, 2.3999981)
        self.assertAlmostEqual(self._revision.mmt, 11.1994624)
        self.assertEqual(self._revision.hazard_rate, 0.00147762)
        self.assertAlmostEqual(self._revision.mtbf, 676.7639853)
        self.assertAlmostEqual(self._revision.mission_mtbf, 687.66332)
        self.assertAlmostEqual(self._revision.reliability, 0.9853324)
        self.assertAlmostEqual(self._revision.mission_reliability, 0.9855632)
        self.assertAlmostEqual(self._revision.availability, 0.9964662)
        self.assertAlmostEqual(self._revision.mission_availability, 0.9965221)
        self.assertAlmostEqual(self._revision.cost_per_failure, 0.2940907)
        self.assertEqual(self._revision.cost_per_hour, 19.903)
