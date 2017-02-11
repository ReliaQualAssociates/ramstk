#!/usr/bin/env python -O
"""
This is the test class for testing the Matrix class.
"""

# -*- coding: utf-8 -*-
#
#       tests.unit.TestMatrix.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

from datamodels.matrix.Matrix import Model, Matrix      # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2016 Andrew "weibullguy" Rowland'


class TestMatrixModel(unittest.TestCase):
    """
    Class for testing the Matrix model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Matrix model class.
        """

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test01_matrix_create(self):
        """
        (TestMatrix) __init__ should return instance of Matrix data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.dicRows, {})
        self.assertEqual(self.DUT.matrix_id, None)
        self.assertEqual(self.DUT.matrix_type, None)
        self.assertEqual(self.DUT.n_row, 1)
        self.assertEqual(self.DUT.n_col, 1)

    @attr(all=True, unit=True)
    def test02_set_attributes(self):
        """
        (TestMatrix) set_attributes should return a zero code and empty message on success
        """

        _values = (0, 0, 3, 10, 5)

        (_code, _msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_code, 0)
        self.assertEqual(_msg, '')

    @attr(all=True, unit=True)
    def test02a_set_attributes_wrong_type(self):
        """
        (TestMatrix) set_attributes should return a 10 error code when passed a wrong type
        """

        _values = (0, 0, 3, '', 5)

        (_code, _msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_code, 10)
        self.assertEqual(_msg, 'ERROR: Matrix Model - Converting one or more inputs to the correct data type.')

    @attr(all=True, unit=True)
    def test02b_set_attributes_missing(self):
        """
        (TestMatrix) set_attributes should return a 40 error code when passed too few values
        """

        _values = (0, 3, 5)

        (_code, _msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_code, 40)
        self.assertEqual(_msg, 'ERROR: Matrix Model - Insufficient input values.')

    @attr(all=True, unit=True)
    def test03_get_attributes(self):
        """
        (TestMatrix) get_attributes() should return a tuple of values
        """

        _values = (None, None, None, 1, 1)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test04_sanity(self):
        """
        (TestMatrix) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 3, 10, 5)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)


class TestMatrixController(unittest.TestCase):
    """
    Class for testing the Matrix data controller class.
    """

    def setUp(self):

        self.DUT = Matrix()

    @attr(all=True, unit=True)
    def test01_create_controller(self):
        """
        (TestMatrix) __init__ should return instance of Matrix data controller
        """

        self.assertTrue(isinstance(self.DUT, Matrix))
        self.assertEqual(self.DUT._dao, None)           # pylint: disable=W0212
        self.assertEqual(self.DUT.dicMatrices, {})
