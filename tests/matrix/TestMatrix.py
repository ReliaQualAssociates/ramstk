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
from datamodels.matrix.Matrix import Model
from dao import DAO
from dao import RTKMatrix

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
        self.dao.db_add([RTKMatrix(), ], self.session)

        self.DUT = Model(self.dao)

    @attr(all=True, unit=True)
    def test00_create(self):
        """
        (TestRevisionModel) __init__ should return a Revision model
        """

        self.assertTrue(isinstance(self.DUT, Model))
        self.assertTrue(isinstance(self.DUT.dao, DAO))
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.matrix_id, None)
        self.assertEqual(self.DUT.matrix_type, None)
        self.assertEqual(self.DUT.matrix, None)
        self.assertEqual(self.DUT.n_row, 1)
        self.assertEqual(self.DUT.n_col, 1)

    @attr(all=True, unit=True)
    def test01_select_all(self):
        """
        (TestMatrixModel): select_all() should return False on success.
        """

        self.assertFalse(self.DUT.select_all())

        self.assertTrue(isinstance(self.DUT.matrix, pd.DataFrame))
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.matrix_id, None)
        self.assertEqual(self.DUT.matrix_type, None)
        self.assertEqual(self.DUT.n_row, 1)
        self.assertEqual(self.DUT.n_col, 1)


class TestMatrixController(unittest.TestCase):
    """
    Class for testing the Matrix data controller class.
    """

    def setUp(self):

        self.DUT = Matrix()

    @attr(all=True, unit=False)
    def test01_create_controller(self):
        """
        (TestMatrix) __init__ should return instance of Matrix data controller
        """

        self.assertTrue(isinstance(self.DUT, Matrix))
        self.assertEqual(self.DUT._dao, None)           # pylint: disable=W0212
        self.assertEqual(self.DUT.dicMatrices, {})
