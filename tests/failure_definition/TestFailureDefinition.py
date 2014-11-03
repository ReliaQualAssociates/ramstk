#!/usr/bin/env python -O
"""
This is the test class for testing Failure Definition module algorithms and
models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestFailureDefinition.py is part of The RTK Project
#
# All rights reserved.

import unittest

# We add this to ensure the imports within the rtk packages will work.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao

from failure_definition.FailureDefinition import Model, FailureDefinition


class TestFailureDefinitionModel(unittest.TestCase):
    """
    Class for testing the Failure Definition model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Failure Definition class.
        """

        self.DUT = Model()

        self._good_values = (0, 1, 'Test Definition')
        self._bad_values = (0, 'Test Definition', 1)

    def test_mission_create(self):
        """
        Method to test the creation of a Failure Definition model instance and
        default values for public attributes are correct.
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.definition_id, 0)
        self.assertEqual(self.DUT.definition, '')

    def test_set_attributes(self):
        """
        Test that attributes can be set.
        """

        self.assertFalse(self.DUT.set_attributes(self._good_values))
        self.assertTrue(self.DUT.set_attributes(self._bad_values))

    def test_get_attributes(self):
        """
        Test that attributes can be retrieved.
        """

        self.assertEqual(self.DUT.get_attributes(), (0, 0, ''))


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):

        _database = '/home/andrew/Analyses/RTK/AGCO/AxialCombine/AxialCombine.rtk'
        self._dao = _dao(_database)

        self.DUT = FailureDefinition()
        self.DUT._dao = self._dao

    def test_create_controller(self):
        """
        Test the creation of a Failure Definition data controller instance.
        """

        self.assertEqual(self.DUT.dicDefinitions, {})

    @unittest.skip("Skipping: Only run during database testing.")
    def test_request_definitions(self):
        """
        Test that Failure Definitions can be loaded from a Project database.
        """

        self.assertFalse(self.DUT.request_profile())

    @unittest.skip("Skipping: Only run during database testing.")
    def test_add_definition(self):
        """
        Test that a failure definition can be added to the Revision.
        """

        (_results, _error_code, _last_id) = self.DUT.add_mission(0)
        self.assertEqual(_error_code, 0)
        #self.assertTrue(isinstance(self.DUT.dicMissions[_last_id], Mission))

    @unittest.skip("Skipping: Only run during database testing.")
    def test_save_definition(self):
        """
        Test that a Failure Definition can be saved to the database.
        """

        self.assertEqual(self.DUT._save_mission(), ([], 0))

    @unittest.skip("Skipping: Only run during database testing.")
    def test_delete_mission(self):
        """
        Test that a failure definition can be deleted from the Revision.
        """

        _n = len(self.DUT.dicMissions)

        self.assertEqual(self.DUT.delete_mission(_n - 1), ([], 0))
        self.assertTrue(self.DUT.delete_mission(_n))
