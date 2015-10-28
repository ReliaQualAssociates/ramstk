#!/usr/bin/env python -O
"""
This is the test class for testing Dataset module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       tests.survival.TestDataset.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr
import numpy as np

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from survival.Dataset import Model


class TestDatasetModel(unittest.TestCase):
    """
    Class for testing the Dataset data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Dataset class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_create(self):
        """
        (TestDataset) __init__ should return an Dataset model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.dicRecords, {})
        self.assertEqual(self.DUT.survival_id, None)
        self.assertEqual(self.DUT.dataset_id, None)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestDataset) set_attributes should return a 0 error code on success
        """

        _values = (0, 1)
        _records = [[0, 6, 729263, 0.0, 100.0, 0, 1, 100.0, 2, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', ''],
                    [1, 6, 729363, 100.0, 328.0, 0, 1, 228.0, 4, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', '']]

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestDataset) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, None)
        _records = [[0, 6, 729263, 0.0, 100.0, 0, 1, 100.0, 2, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', ''],
                    [1, 6, 729363, 100.0, 328.0, 0, 1, 228.0, 4, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', '']]

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestDataset) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0)
        _records = [[0, 6, 729263, 0.0, 100.0, 0, 1, 100.0, 2, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', ''],
                    [1, 6, 729363, 100.0, 328.0, 0, 1, 228.0, 4, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', '']]

        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 1000)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestDataset) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(), (None, None, {}))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestDataset) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 1)
        _records = [[0, 6, 729263, 0.0, 100.0, 0, 1, 100.0, 2, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', ''],
                    [1, 6, 729363, 100.0, 328.0, 0, 1, 228.0, 4, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', '']]

        _results = (0, 1, {0: [6, 729263, 0.0, 100.0, 0, 1, 100.0, 2, 0,
                               719163, 1, 719163, 1, 0.0, 0.0, 0.0, 0, 0, 0,
                               '', '', ''],
                           1: [6, 729363, 100.0, 328.0, 0, 1, 228.0, 4, 0,
                               719163, 1, 719163, 1, 0.0, 0.0, 0.0, 0, 0, 0,
                               '', '', '']})

        self.DUT.set_attributes(_values)
        self.DUT.load_records(_records)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _results)

    @attr(all=True, unit=True)
    def test_calculate_tbf(self):
        """
        (TestDataset) calculate_tbf should return False on success with the current record's tbf = 238.0
        """

        _values = (0, 1)
        _records = [[0, 6, 729263, 100.0, 100.0, 0, 1, 100.0, 2, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', ''],
                    [1, 6, 729363, 338.0, 338.0, 0, 1, 0.0, 4, 0, 719163, 1,
                     719163, 1, 0.0, 0.0, 0.0, 0, 0, 0, '', '', '']]

        self.DUT.set_attributes(_values)
        self.DUT.load_records(_records)
        self.assertFalse(self.DUT.calculate_tbf(0, 1))

        self.assertEqual(self.DUT.dicRecords[1][6], 238.0)
