#!/usr/bin/env python -O
"""
This is the test class for testing Incident module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestIncident.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr
import numpy as np

from incident.Incident import Model, Incident

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestIncidentModel(unittest.TestCase):
    """
    Class for testing the Incident data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Incident class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestIncident) __init__ should return an Incident model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.incident_id, None)
        self.assertEqual(self.DUT.incident_category, 0)
        self.assertEqual(self.DUT.incident_type, 0)
        self.assertEqual(self.DUT.short_description, '')
        self.assertEqual(self.DUT.detail_description, '')
        self.assertEqual(self.DUT.criticality, 0)
        self.assertEqual(self.DUT.detection_method, 0)
        self.assertEqual(self.DUT.remarks, '')
        self.assertEqual(self.DUT.status, 0)
        self.assertEqual(self.DUT.test, '')
        self.assertEqual(self.DUT.test_case, '')
        self.assertEqual(self.DUT.execution_time, 0.0)
        self.assertEqual(self.DUT.unit_id, 0)
        self.assertEqual(self.DUT.cost, 0.0)
        self.assertEqual(self.DUT.incident_age, 0.0)
        self.assertEqual(self.DUT.hardware_id, 0)
        self.assertEqual(self.DUT.software_id, 0)
        self.assertEqual(self.DUT.request_by, 0)
        self.assertEqual(self.DUT.request_date, 0)
        self.assertEqual(self.DUT.reviewed, False)
        self.assertEqual(self.DUT.review_by, 0)
        self.assertEqual(self.DUT.review_date, 0)
        self.assertEqual(self.DUT.approved, False)
        self.assertEqual(self.DUT.approve_by, 0)
        self.assertEqual(self.DUT.approve_date, 0)
        self.assertEqual(self.DUT.closed, False)
        self.assertEqual(self.DUT.close_by, 0)
        self.assertEqual(self.DUT.close_date, 0)
        self.assertEqual(self.DUT.life_cycle, 0)
        self.assertEqual(self.DUT.analysis, '')
        self.assertEqual(self.DUT.accepted, False)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestIncident) set_attributes should return a 0 error code on success
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   5, 'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 0, 719163, True, 0, 719163, False, 0, 719164, False, 0,
                   719163, 3, 'Analysis', True)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestIncident) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 0, 719163, True, 0, 719163, False, 0, 719164, False, 0,
                   719163, 'Design', 'Analysis', True)

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestIncident) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   5, 'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 0, 719163, True, 0, 719163, False, 0, 719164, False, 0,
                   719163, 3, 'Analysis')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestIncident) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, 0, 0, '', '', 0, 0, '', 0, '', '', 0.0,
                          0, 0.0, 0.0, 0, 0, 0, 0, False, 0, 0, False, 0, 0,
                          False, 0, 0, 0, '', False))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestIncident) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 1, 2, 3, 'Short Description', 'Detailed Description', 4,
                   5, 'Remarks', 6, 'Test', 'Test Case', 7.0, 8, 9.0, 10.0, 11,
                   12, 0, 719163, True, 0, 719163, False, 0, 719164, False, 0,
                   719163, 3, 'Analysis', True)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)


class TestIncidentController(unittest.TestCase):
    """
    Class for testing the Incident data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Incident class.
        """

        self.DUT = Incident()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestIncident) __init__ should create a Incident data controller
        """

        self.assertTrue(isinstance(self.DUT, Incident))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicIncidents, {})
