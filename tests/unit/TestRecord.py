#!/usr/bin/env python -O
"""
This is the test class for testing Record module algorithms and models.
"""

# -*- coding: utf-8 -*-
#
#       tests.survival.TestRecord.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from survival.Record import Model, Record

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'


class TestRecordModel(unittest.TestCase):
    """
    Class for testing the dataset Record data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the dataset Record class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestRecord) __init__ should return a Record model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.survival_id, 0)
        self.assertEqual(self.DUT.assembly_id, 0)
        self.assertEqual(self.DUT.failure_date, 719163)
        self.assertEqual(self.DUT.left_interval, 0.0)
        self.assertEqual(self.DUT.right_interval, 0.0)
        self.assertEqual(self.DUT.status, 0)
        self.assertEqual(self.DUT.n_failures, 0)
        self.assertEqual(self.DUT.interarrival_time, 0.0)
        self.assertEqual(self.DUT.mode_type, 0)
        self.assertEqual(self.DUT.nevada_chart, 0)
        self.assertEqual(self.DUT.ship_date, 719163)
        self.assertEqual(self.DUT.return_date, 719163)
        self.assertEqual(self.DUT.user_float_1, 0.0)
        self.assertEqual(self.DUT.user_float_2, 0.0)
        self.assertEqual(self.DUT.user_float_3, 0.0)
        self.assertEqual(self.DUT.user_integer_1, 0)
        self.assertEqual(self.DUT.user_integer_2, 0)
        self.assertEqual(self.DUT.user_integer_3, 0)
        self.assertEqual(self.DUT.user_string_1, '')
        self.assertEqual(self.DUT.user_string_2, '')
        self.assertEqual(self.DUT.user_string_3, '')

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestRecord) set_attributes should return a 0 error code on success
        """

        _values = (0, 1, 719163, 3.0, 4.0, 5, 6, 7.0, 8, 9, 719163, 719163,
                   12.0, 13.0, 14.0, 15, 16, 17, "User String 1",
                   "User String 2", 'User String 3')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestRecord) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 1, 719163, 3.0, 4.0, 5, 6, None, 8, 9, 719163, 719163,
                   12.0, 13.0, 14.0, 15, 16, 17, "User String 1",
                   "User String 2", 'User String 3')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestRecord) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 1, 719163, 3.0, 4.0, 5, 6, 7.0, 8, 9, 719163, 719163,
                   12.0, 13.0, 14.0, 15, 16, 17, "User String 1",
                   'User String 3')

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestRecord) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (0, 0, 719163, 0.0, 0.0, 0, 0, 0.0, 0, 0, 719163,
                          719163, 0.0, 0.0, 0.0, 0, 0, 0, '', '', ''))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestRecord) get_attributes(set_attributes(values)) == values
        """

        _values = (0, '1', 719163, 3.0, 4.0, 5, 6, 7.0, 8, 9, 719163, 719163,
                   12.0, 13.0, 14.0, 15, 16, 17, "User String 1",
                   "User String 2", 'User String 3')

        self.DUT.set_attributes(_values)
        self.assertEqual(self.DUT.get_attributes(), _values)


class TestRecordController(unittest.TestCase):
    """
    Class for testing the Record data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Record class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Record()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestRecord) __init__ should create a Record data controller
        """

        self.assertTrue(isinstance(self.DUT, Record))
