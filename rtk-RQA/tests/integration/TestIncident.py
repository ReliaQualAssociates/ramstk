#!/usr/bin/env python -O
"""
This is the test class for testing Incident module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestIncident.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr
import numpy as np

import dao.DAO as _dao
from incident.Incident import Incident

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestIncidentController(unittest.TestCase):
    """
    Class for testing the Incident data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Incident class.
        """

        _database = '/tmp/tempdb.rtk'
        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Incident()

    @attr(all=True, integration=True)
    def test_request_incidents(self):
        """
        (TestIncident) request_tasks should return 0 on success
        """

        self.assertEqual(self.DUT.request_incidents(self._dao, 0)[1], 0)

    @attr(all=True, integration=True)
    def test_add_incident(self):
        """
        (TestIncident) add_task should return 0 on success
        """

        self.assertEqual(self.DUT.request_incidents(self._dao, 0)[1], 0)
        self.assertEqual(self.DUT.add_incident(0)[1], 0)

    @attr(all=True, integration=True)
    def test_save_incident(self):
        """
        (TestIncident) save_task returns 0 on success
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   5, 'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 1, 719163, True, 1, 719163, False, 1, 719164, False, 1,
                   719163, 3, 'Analysis', True)

        self.assertEqual(self.DUT.request_incidents(self._dao, 0)[1], 0)
        _incident = self.DUT.dicIncidents[min(self.DUT.dicIncidents.keys())]
        _incident.set_attributes(_values)

        (_results, _error_code) = self.DUT.save_incident(min(
                                                self.DUT.dicIncidents.keys()))

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)
