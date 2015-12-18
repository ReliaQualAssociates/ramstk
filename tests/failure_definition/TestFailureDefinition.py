#!/usr/bin/env python -O
"""
This is the test class for testing Failure Definition module algorithms and
models.
"""

# -*- coding: utf-8 -*-
#
#       tests.failure_definition.TestFailureDefinition.py is part of The RTK
#       Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from failure_definition.FailureDefinition import Model, FailureDefinition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestFailureDefinitionModel(unittest.TestCase):
    """
    Class for testing the Failure Definition model class.
    """

    def setUp(self):
        """
        (TestFailureDefinition) Method to setup the test fixture for the Failure Definition class.
        """

        self.DUT = Model()

        self._good_values = (0, 1, 'Test Definition')
        self._bad_values = (0, 'Test Definition', 1)

    @attr(all=True, unit=True)
    def test_definition_create(self):
        """
        (TestFailureDefinition) __init__ should return instance of a FailureDefition data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, 0)
        self.assertEqual(self.DUT.definition_id, 0)
        self.assertEqual(self.DUT.definition, '')

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        (TestFailureDefinition) set_attributes should return 0 with good inputs
        """

        _values = (0, 1, 'Definition')

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestFailureDefinition) set_attributes should return 40 with missing input(s)
        """

        _values = (0, 1)

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestFailureDefinition) set_attributes should return 10 with wrong data type
        """

        _values = (0, None, 'Definition')

        (_error_code, _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestFailureDefinition) get_attributes should return good values
        """

        self.assertEqual(self.DUT.get_attributes(), (0, 0, ''))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestFailureDefinition) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 1, 'Definition')

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)


class TestUsageProfileController(unittest.TestCase):
    """
    Class for testing the Usage Profile controller class.
    """

    def setUp(self):

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = FailureDefinition()
        self.DUT._dao = self._dao

    @attr(all=True, unit=True)
    def test_create_controller(self):
        """
        (TestFailureDefinition) Test the creation of a Failure Definition data controller instance.
        """

        self.assertTrue(isinstance(self.DUT, FailureDefinition))

        self.assertEqual(self.DUT.dicDefinitions, {})

    @attr(all=True, integration=True)
    def test_request_definitions(self):
        """
        (TestFailureDefinition) request_definitions should return a list of definitions and an error code of 0 on success
        """

        (_results, _error_code) = self.DUT.request_definitions(0, self._dao)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_add_definition(self):
        """
        (TestFailureDefinition) add_definition should return
        """

        (_results, _error_code, _last_id) = self.DUT.add_definition(0)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_definition(self):
        """
        (TestFailureDefinition) save_definition should return True on success
        """

        self.DUT.request_definitions(0, self._dao)

        (_results, _error_code) = self.DUT.save_definitions(0)
        self.assertTrue(_results)

    @attr(all=True, integration=True)
    def test_delete_definition(self):
        """
        (TestFailureDefinition) delete_definition should return a 0 error code on success
        """

        self.DUT.request_definitions(0, self._dao)

        _n = max(self.DUT.dicDefinitions.keys())

        (_results, _error_code) = self.DUT.delete_definition(0, _n)
        self.assertEqual(_error_code, 0)
