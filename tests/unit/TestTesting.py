#!/usr/bin/env python -O
"""
This is the test class for testing Testing module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.testing.TestTesting.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from testing.Testing import Model, Testing

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestTestingModel(unittest.TestCase):
    """
    Class for testing the Testing data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Testing class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_testing_create(self):
        """
        (TestTesting) __init__ should return a Testing model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.assembly_id, None)
        self.assertEqual(self.DUT.test_id, 0)
        self.assertEqual(self.DUT.name, '')
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.test_type, 0)
        self.assertEqual(self.DUT.attachment, '')
        self.assertEqual(self.DUT.cum_time, 0.0)
        self.assertEqual(self.DUT.cum_failures, 0)
        self.assertEqual(self.DUT.confidence, 0.75)
        self.assertEqual(self.DUT.consumer_risk, 0.0)
        self.assertEqual(self.DUT.producer_risk, 0.0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestTesting) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 1, 'Testing', 'Description', 2, 'Attachment', 40.2,
                   2.0, 0.6, 0.8, 0.9)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestTesting) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 0, 1, 'Testing', 'Description', 2, 'Attachment', 40.2,
                   2.0, 0.6, None, 0.9)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestTesting) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 0, 1, 'Testing', 'Description', 2, 'Attachment', 40.2,
                   2.0, 0.6, 0.8)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestTesting) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, 0, '', '', 0, '', 0.0, 0.0, 0.75, 0.0,
                          0.0))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestTesting) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 1, 'Testing', 'Description', 2, 'Attachment', 40.2,
                   2.0, 0.6, 0.8, 0.9)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)


class TestTestingController(unittest.TestCase):
    """
    Class for testing the Testing data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Testing class.
        """

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Testing()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestTesting) __init__ should create a Testing data controller
        """

        self.assertTrue(isinstance(self.DUT, Testing))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicTests, {})

    @attr(all=True, integration=True)
    def test_request_tests(self):
        """
        (TestTesting) request_inputs should return 0 on success
        """

        self.assertEqual(self.DUT.request_tests(self._dao, 0)[1], 0)
