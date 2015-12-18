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
from datamodels.matrix.Matrix import *

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestMatrixModel(unittest.TestCase):
    """
    Class for testing the Matrix model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Matrix model class.
        """

        self.DUT = Model(0, 0)

    @attr(all=True, unit=True)
    def test_matrix_create(self):
        """
        (TestMatrix) __init__ should return instance of Matrix data model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.dicCells, {})
        self.assertEqual(self.DUT.matrix_id, 0)
        self.assertEqual(self.DUT.matrix_type, 0)
        self.assertEqual(self.DUT.n_row, 0)
        self.assertEqual(self.DUT.n_col, 0)

    @attr(all=True, unit=True)
    def test_set_attributes(self):
        """
        (TestMatrix)
        """

        pass

    @attr(all=True, unit=True)
    def test_get_attributes(self):
        """
        (TestMatrix)
        """

        pass

class TestMatrixController(unittest.TestCase):
    """
    Class for testing the Matrix data controller class.
    """

    def setUp(self):

        _database = '/home/andrew/Analyses/RTK/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Matrix()
        self.DUT._dao = self._dao

        self.query = "SELECT fld_matrix_id, fld_row_id, fld_col_id, fld_value \
                      FROM rtk_matrices \
                      WHERE fld_revision_id=0"

    @attr(all=True, unit=True, integration=True)
    def test_create_controller(self):
        """
        (TestMatrix) __init__ should return instance of Matrix data controller
        """

        self.assertTrue(isinstance(self.DUT, Matrix))

        self.assertEqual(self.DUT._dao, self._dao)
        self.assertEqual(self.DUT.dicMatrices, {})

    @attr(all=True, integration=True)
    def test_request_matrix(self):
        """
        (TestMatrix) request_matrix should return False on success
        """

        self.assertFalse(self.DUT.request_matrix(0, self.query, 0))

    @attr(all=True, integration=True)
    def test_request_matrix_no_matrix_id(self):
        """
        (TestMatrix) request_matrix should raise ParentError with no Matrix ID
        """

        self.assertRaises(ParentError, self.DUT.request_matrix, None,
                          self.query, 0)

    @unittest.expectedFailure
    @attr(all=True, integration=True)
    def test_request_rows(self):
        """
        (TestMatrix) request_rows should return dictionary on success
        """

        self.DUT.request_matrix(0, self.query, 0)
        self.assertEqual(self.DUT.request_rows(0, 0),
                         {0: [-1, 0, 0], 1: [1, 1, 0]})

    @attr(all=True, integration=True)
    def test_request_rows_no_matrix(self):
        """
        (TestMatrix) request_rows should return an empty dict when the requested Matrix does not exist
        """

        self.assertEqual(self.DUT.request_rows(0, 1), {})

    @attr(all=True, integration=True)
    def test_add_row(self):
        """
        (TestMatrix) add_row should return (True, 0) on success
        """

        self.DUT.request_matrix(0, self.query, 0)
        self.DUT.request_rows(0, 0)
        self.assertEqual(self.DUT.add_row(0, 0, 0, 2), (True, 0))

    @attr(all=True, integration=True)
    def test_delete_row(self):
        """
        (TestMatrix) delete_row should return (True, 0) on success
        """

        self.DUT.request_matrix(0, self.query, 0)
        self.DUT.request_rows(0, 0)
        self.DUT.add_row(0, 0, 0, 2)
        self.assertEqual(self.DUT.delete_row(0, 0, 2), (True, 0))

    @attr(all=True, integration=True)
    def test_save_matrix(self):
        """
        (TestMatrix) save_matrix should return (True, 0) on success
        """

        self.DUT.request_matrix(0, self.query, 0)
        _matrix = self.DUT.dicMatrices[0][0]
        self.assertEqual(self.DUT.save_matrix(_matrix), (True, 0))
