#!/usr/bin/env python -O
"""
This is the test class for testing the Matrix class.
"""

# -*- coding: utf-8 -*-
#
#       tests.datamodels.TestMatrix.py is part of The RTK Project
#
# All rights reserved.

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao
from datamodels.matrix.Matrix import Model, Matrix, ParentError, NoMatrixError

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
    def test_matrix_create(self):
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
    def test_set_attributes(self):
        """
        (TestMatrix) set_attributes should return a zero code and empty message on success
        """

        _values = (0, 0, 3, 10, 5)

        (_code, _msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_code, 0)
        self.assertEqual(_msg, '')

    @attr(all=True, unit=True)
    def test_set_attributes_wrong_type(self):
        """
        (TestMatrix) set_attributes should return a 10 error code when passed a wrong type
        """

        _values = (0, 0, 3, '', 5)

        (_code, _msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_code, 10)
        self.assertEqual(_msg, 'ERROR: Matrix Model - Converting one or more inputs to the correct data type.')

    @attr(all=True, unit=True)
    def test_set_attributes_missing(self):
        """
        (TestMatrix) set_attributes should return a 40 error code when passed too few values
        """

        _values = (0, 3, 5)

        (_code, _msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_code, 40)
        self.assertEqual(_msg, 'ERROR: Matrix Model - Insufficient input values.')

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMatrix) get_attributes() should return a tuple of values
        """

        _values = (None, None, None, 1, 1)

        self.assertEqual(self.DUT.get_attributes(), _values)

    @attr(all=True, unit=True)
    def test_sanity(self):
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

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Matrix()

    @attr(all=True, unit=True)
    def test_create_controller(self):
        """
        (TestMatrix) __init__ should return instance of Matrix data controller
        """

        self.assertTrue(isinstance(self.DUT, Matrix))

        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT.dicMatrices, {})

    @attr(all=True, integration=True)
    def test_request_matrix(self):
        """
        (TestMatrix) request_matrix should return a tuple of lists and a 0 error code on success
        """

        (_results, _error_code) = self.DUT.request_matrix(self._dao, 0)
        self.assertEqual(_error_code, 0)

        self.assertEqual(self.DUT._dao, self._dao)

    @attr(all=True, integration=True)
    def test_request_matrix_no_matrix_id(self):
        """
        (TestMatrix) request_matrix should raise ParentError with no Matrix ID
        """

        self.assertRaises(ParentError, self.DUT.request_matrix, self._dao,
                          None)

    @attr(all=True, integration=True)
    def test_add_row(self):
        """
        (TestMatrix) add_row should return (True, 0) on success
        """

        self.DUT.request_matrix(self._dao, 0)

        (_results,
         _error_code) = self.DUT.add_row(0, -1, 900)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_row(self):
        """
        (TestMatrix) delete_row should return (True, 0) on success
        """

        self.DUT.request_matrix(self._dao, 0)
        self.DUT.add_row(0, -1, 900)
        _row_id = self.DUT.dicMatrices[0].n_row - 1

        (_results, _error_code) = self.DUT.delete_row(0, _row_id)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_add_column(self):
        """
        (TestMatrix) add_column should return (True, 0) on success
        """

        self.DUT.request_matrix(self._dao, 0)

        (_results,
         _error_code) = self.DUT.add_column(0)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_column(self):
        """
        (TestMatrix) delete_column should return (True, 0) on success
        """

        self.DUT.request_matrix(self._dao, 0)
        self.DUT.add_column(0)
        _col_id = self.DUT.dicMatrices[0].n_col - 1

        (_results, _error_code) = self.DUT.delete_column(0, _col_id)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_matrix(self):
        """
        (TestMatrix) save_matrix should return False on success
        """

        self.DUT.request_matrix(self._dao, 0)

        self.assertFalse(self.DUT.save_matrix(0))
