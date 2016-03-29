#!/usr/bin/env python -O
"""
This is the test class for testing the Matrix class.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.TestMatrix.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao                                      # pylint: disable=E0401
from datamodels.matrix.Matrix import Matrix, ParentError    # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2016 Andrew "weibullguy" Rowland'


class TestMatrixController(unittest.TestCase):
    """
    Class for testing the Matrix data controller class.
    """

    def setUp(self):

        _database = '/tmp/tempdb.rtk'

        self._dao = _dao(_database)
        self._dao.execute("PRAGMA foreign_keys = ON", commit=False)

        self.DUT = Matrix()

    @attr(all=True, integration=True)
    def test0_request_matrix(self):
        """
        (TestMatrix) request_matrix should return a tuple of lists and a 0 error code on success
        """

        (_results, _error_code) = self.DUT.request_matrix(self._dao, 0,
                                                          [0, 1, 2])

        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT._dao, self._dao)      # pylint: disable=W0212

        # Check that the Hardware and Software matrices were created and the
        # Testing matrix was not.  Then check the correct column headers are
        # created for the Hardware and Software matrices.
        self.assertEqual(self.DUT.dicMatrices.keys(), [0, 1, 2])
        _matrix = self.DUT.dicMatrices[0]
        self.assertEqual(_matrix.lstColumnHeaders, [u'System', u'Sub-System 1',
                                                    u'Sub-System 2',
                                                    u'Sub-System 3',
                                                    u'Assembly 11',
                                                    u'Assembly 12',
                                                    u'Sub-System 4',
                                                    u'Sub-Assembly 121',
                                                    u'Sub-Assembly 111',
                                                    u'Sub-Assembly 122'])
        _matrix = self.DUT.dicMatrices[1]
        self.assertEqual(_matrix.lstColumnHeaders, ['System Software'])

    @attr(all=True, integration=True)
    def test1_request_matrix_no_matrix_id(self):
        """
        (TestMatrix) request_matrix should raise ParentError with no Matrix ID
        """

        self.assertRaises(ParentError, self.DUT.request_matrix, self._dao,
                          None, [0])

    @attr(all=True, integration=True)
    def test2_add_row(self):
        """
        (TestMatrix) add_row should return (True, 0) on success
        """

        self.DUT.request_matrix(self._dao, 0, [0])

        (_results, _error_code) = self.DUT.add_row(0, -1, 900)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test3_delete_row(self):
        """
        (TestMatrix) delete_row should return (True, 0) on success
        """

        self.DUT.request_matrix(self._dao, 0, [0])
        self.DUT.add_row(0, -1, 900)
        _row_id = self.DUT.dicMatrices[0].n_row - 1

        (_results, _error_code) = self.DUT.delete_row(0, _row_id)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test4_add_column(self):
        """
        (TestMatrix) add_column should return a list of tuples on success
        """

        self.DUT.request_matrix(self._dao, 0, [0])

        _error_codes = self.DUT.add_column(0)
        self.assertEqual(_error_codes,
                         [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
                          (6, 0), (7, 0), (8, 0), (9, 0)])

    @attr(all=True, integration=True)
    def test5_delete_column(self):
        """
        (TestMatrix) delete_column should return (True, 0) on success
        """

        self.DUT.request_matrix(self._dao, 0, [0])
        self.DUT.add_column(0)
        _col_id = self.DUT.dicMatrices[0].n_col - 1

        (_results, _error_code) = self.DUT.delete_column(0, _col_id)
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test6_save_matrix(self):
        """
        (TestMatrix) save_matrix should return False on success
        """

        self.DUT.request_matrix(self._dao, 0, [0])

        self.assertFalse(self.DUT.save_matrix(0))
