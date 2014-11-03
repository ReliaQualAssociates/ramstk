#!/usr/bin/env python -O
"""
This is the test class for testing Revision module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestRevision.py is part of The RTK Project
#
# All rights reserved.

import unittest

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from revision.Revision import Model, Revision


class TestRevisionModel(unittest.TestCase):
    """
    Class for testing the Revision model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision class.
        """

        _database = '/home/andrew/Analyses/RTK/AGCO/AxialCombine/AxialCombine.rtk'
        self._dao = _dao(_database)

        self.DUT = Model()

        self.good_values = (0, 1, 50.0, 'days', 'Test Mission')
        self.bad_values = (0, 'days', 'Test Mission', 1, 50.0)

        self._reliability_inputs = (0.005, 0.0000065, 0.0000065, 0.0045)
        self._availability_inputs = (1.25, 2.86, 3.18, 2.06)
        self._cost_inputs = 100.00
        self._mission_time = 10.0
        self._hr_multiplier = [1.0, 1000000]

    def test_revision_create(self):
        """
        Method to test the creation of a Revision class instance and default
        values for public attributes are correct.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.n_parts, 0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.cost_per_failure, 0.0)
        self.assertEqual(self.DUT.cost_per_hour, 0.0)
        self.assertEqual(self.DUT.active_hazard_rate, 0.0)
        self.assertEqual(self.DUT.dormant_hazard_rate, 0.0)
        self.assertEqual(self.DUT.software_hazard_rate, 0.0)
        self.assertEqual(self.DUT.hazard_rate, 0.0)
        self.assertEqual(self.DUT.mission_hazard_rate, 0.0)
        self.assertEqual(self.DUT.mtbf, 0.0)
        self.assertEqual(self.DUT.mission_mtbf, 0.0)
        self.assertEqual(self.DUT.reliability, 0.0)
        self.assertEqual(self.DUT.mission_reliability, 0.0)
        self.assertEqual(self.DUT.mpmt, 0.0)
        self.assertEqual(self.DUT.mcmt, 0.0)
        self.assertEqual(self.DUT.mttr, 0.0)
        self.assertEqual(self.DUT.mmt, 0.0)
        self.assertEqual(self.DUT.availability, 0.0)
        self.assertEqual(self.DUT.mission_availability, 0.0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.code, '')
        self.assertEqual(self.DUT.program_time, 0.0)
        self.assertEqual(self.DUT.program_time_se, 0.0)
        self.assertEqual(self.DUT.program_cost, 0.0)
        self.assertEqual(self.DUT.program_cost_se, 0.0)

    def test_calculate_reliability(self):
        """
        Test of Revision reliability calculations.
        """

        self.DUT.calculate_reliability(self._reliability_inputs,
                                       self._mission_time,
                                       self._hr_multiplier[0])
        self.assertAlmostEqual(self.DUT.hazard_rate, 0.005013)
        self.assertAlmostEqual(self.DUT.mtbf, 199.4813485)
        self.assertAlmostEqual(self.DUT.mission_mtbf, 222.2222222)
        self.assertAlmostEqual(self.DUT.reliability, 0.9511058)
        self.assertAlmostEqual(self.DUT.mission_reliability, 0.9559975)

    def test_calculate_availability(self):
        """
        Test of Revision availability calculations.
        """

        self.DUT.mtbf = 199.4813485
        self.DUT.mission_mtbf = 222.2222222

        self.DUT.calculate_availability(self._availability_inputs)
        self.assertAlmostEqual(self.DUT.availability, 0.9984261)
        self.assertAlmostEqual(self.DUT.mission_availability, 0.9985869)

    def test_calculate_costs(self):
        """
        Test of Revision cost calculations.
        """

        self.DUT.hazard_rate = 0.005013

        self.DUT.calculate_costs(self._cost_inputs, self._mission_time)
        self.assertEqual(self.DUT.cost, 100.0)
        self.assertAlmostEqual(self.DUT.cost_per_failure, 0.5013)
        self.assertAlmostEqual(self.DUT.cost_per_hour, 10.0)


class TestRevisionController(unittest.TestCase):
    """
    Class for testing the Revision data controller class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Revision class.
        """

        _database = '/home/andrew/Analyses/RTK/AGCO/AxialCombine/AxialCombine.rtk'
        self._dao = _dao(_database)

        self.DUT = Revision()

    def test_request_revisions(self):
        """
        Method to test the request for revisions.
        """

        self.assertEqual(self.DUT.request_revisions(self._dao)[1], 0)
