#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.unit.TestMatrix.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
This is the test class for testing the Matrix class.
"""

import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

import unittest
from nose.plugins.attrib import attr

from sqlalchemy.orm import scoped_session
from treelib import Tree
import pandas as pd

import Utilities as Utilities
from Configuration import Configuration
from datamodels import RTKDataMatrix
from dao import DAO
from dao import RTKMatrix
from dao import RTKFunction, RTKHardware

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'


class TestMatrixModel(unittest.TestCase):
    """
    Class for testing the Matrix model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Matrix class.
        """

        self.Configuration = Configuration()

        self.Configuration.RTK_BACKEND = 'sqlite'
        self.Configuration.RTK_PROG_INFO = {'host'    : 'localhost',
                                            'socket'  : 3306,
                                            'database': '/tmp/TestDB.rtk',
                                            'user'    : '',
                                            'password': ''}

        self.Configuration.DEBUG_LOG = \
            Utilities.create_logger("RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
        self.Configuration.USER_LOG = \
            Utilities.create_logger("RTK.user", 'INFO', '/tmp/RTK_user.log')

        # Create a data access object and connect to a test database.
        self.dao = DAO()
        _database = self.Configuration.RTK_BACKEND + ':///' + \
                    self.Configuration.RTK_PROG_INFO['database']
        self.dao.db_connect(_database)

        self.dao.RTK_SESSION.configure(bind=self.dao.engine, autoflush=False,
                                       expire_on_commit=False)
        self.session = scoped_session(self.dao.RTK_SESSION)

        self.DUT = RTKDataMatrix(self.dao, RTKFunction, RTKHardware)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestRevisionModel) __init__ should return a Revision model
        """

        self.assertTrue(isinstance(self.DUT, RTKDataMatrix))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT.dic_column_hdrs, {})
        self.assertEqual(self.DUT.dic_row_hdrs, {})
        self.assertEqual(self.DUT.dtf_matrix, None)
        self.assertEqual(self.DUT.n_row, 1)
        self.assertEqual(self.DUT.n_col, 1)

    @attr(all=True, unit=True)
    def test01_select_all(self):
        """
        (TestMatrixModel): select_all() should return False on success.
        """

        self.assertFalse(self.DUT.select_all(1, 1, 1, 1, 5, 6))

        self.assertTrue(isinstance(self.DUT.dtf_matrix, pd.DataFrame))
        self.assertEqual(self.DUT.dic_column_hdrs,
                         {1: u'S1', 2: u'S1:SS1', 3: u'S1:SS2'})
        self.assertEqual(self.DUT.dic_row_hdrs,
                         {1: u'PRESS-001', 2: u'FLOW-001', 3: u'TEMP-001'})
        self.assertEqual(self.DUT.n_row, 3)
        self.assertEqual(self.DUT.n_col, 3)

    @attr(all=True, unit=True)
    def test02_select(self):
        """
        (TestMatrixModel): select() should return an integer on success.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        _cell = self.DUT.dtf_matrix[2][2]

        self.assertEqual(_cell, 1)

    @attr(all=True, unit=True)
    def test03a_insert_row(self):
        """
        (TestMatrixModel): insert() should return False on successfully inserting a row.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        _error_code, _msg = self.DUT.insert(6, 'TEMP-001A', row=True)

        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_row, 4)
        self.assertEqual(self.DUT.n_col, 3)
        self.assertEqual(self.DUT.dtf_matrix[1][6], 0)

    @attr(all=True, unit=True)
    def test03b_insert_column(self):
        """
        (TestMatrixModel): insert() should return False on successfully inserting a column.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        _error_code, _msg = self.DUT.insert(4, 'S1:SS1:A1', row=False)

        self.assertEqual(_error_code, 0)
        self.assertEqual(self.DUT.n_row, 3)
        self.assertEqual(self.DUT.n_col, 4)
        self.assertEqual(self.DUT.dtf_matrix[4][1], 0)

    @attr(all=True, unit=True)
    def test04a_delete_row(self):
        """
        (TestMatrixModel): delete() should return False on successfully deleting a row.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        _error_code, _msg = self.DUT.delete(3, row=True)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Removing a row or column from ' \
                               'the matrix.')
        self.assertEqual(self.DUT.n_row, 2)
        self.assertEqual(self.DUT.n_col, 3)

    @attr(all=True, unit=True)
    def test04b_delete_non_existent_row(self):
        """
        (TestMatrixModel): delete() should return True when attempting to delete a non-existent row.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        _error_code, _msg = self.DUT.delete(22, row=True)

        self.assertEqual(_error_code, 6)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to drop non-existent ' \
                               'row 22 from the matrix.')
        self.assertEqual(self.DUT.n_row, 3)
        self.assertEqual(self.DUT.n_col, 3)

    @attr(all=True, unit=True)
    def test04c_delete_column(self):
        """
        (TestMatrixModel): delete() should return False on successfully deleting a column.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        _error_code, _msg = self.DUT.delete(2, row=False)

        self.assertEqual(_error_code, 0)
        self.assertEqual(_msg, 'RTK SUCCESS: Removing a row or column from ' \
                               'the matrix.')
        self.assertEqual(self.DUT.n_row, 3)
        self.assertEqual(self.DUT.n_col, 2)

    @attr(all=True, unit=True)
    def test04d_delete_non_existent_column(self):
        """
        (TestMatrixModel): delete() should return True when attempting to delete a non-existent column.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        _error_code, _msg = self.DUT.delete(400, row=False)

        self.assertEqual(_error_code, 6)
        self.assertEqual(_msg, 'RTK ERROR: Attempted to drop non-existent ' \
                               'column 400 from the matrix.')
        self.assertEqual(self.DUT.n_row, 3)
        self.assertEqual(self.DUT.n_col, 3)

    @attr(all=True, unit=True)
    def test05a_update(self):
        """
        (TestMatrixModel): update() should return a zero error code on success.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        (_error_code, _msg) = self.DUT.update(1, 1)

        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test05b_update_non_existent_matrix(self):
        """
        (TestMatrixModel): update() should return a non-zero error code when attempting to update a non-existent matrix.
        """

        self.DUT.select_all(1, 1, 1, 1, 5, 6)

        (_error_code, _msg) = self.DUT.update(1, 3)

        self.assertEqual(_error_code, 0)
