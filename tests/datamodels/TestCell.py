#!/usr/bin/env python -O
"""
This is the test class for testing the Cell class.
"""

# -*- coding: utf-8 -*-
#
#       tests.datamodels.TestCell.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from datamodels.cell.Cell import Model

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestCellModel(unittest.TestCase):
    """
    Class for testing the Cell model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Cell model class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_control_create(self):
        """
        (TestCell) __init__ should return instance of Cell data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.row_id, None)
        self.assertEqual(self.DUT.col_id, None)
        self.assertEqual(self.DUT.value, None)

    @attr(all=True, unit=True)
    def test_set_good_attributes(self):
        """
        (TestCell) set_attributes should return 0 with good inputs
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((1, 2, -1))
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_set_attributes_missing_index(self):
        """
        (TestCell) set_attributes should return 40 with missing input(s)
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((20, -1))
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestCell) set_attributes should return 10 with wrong data type
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((0, None, 'Test Cell'))
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_value(self):
        """
        (TestCell) set_attributes should return 10 with bad value
        """

        (_error_code,
         _error_msg) = self.DUT.set_attributes((1, 'Test Cause', 2))
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestCell) get_attributes should return good values
        """

        self.assertEqual(self.DUT.get_attributes(), (None, None, None))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestCell) get_attributes(set_attributes(values)) == values
        """

        values = (4, 10, 1)

        self.DUT.set_attributes(values)
        result = self.DUT.get_attributes()
        self.assertEqual(result, values)
