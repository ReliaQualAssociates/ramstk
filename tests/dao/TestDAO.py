#!/usr/bin/env python -O
"""
This is the test class for testing the Environment class.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestEnvironment.py is part of The RTK Project
#
# All rights reserved.

import unittest

import os
import sys
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../.."))
sys.path.insert(0, os.path.abspath("../../.."))

import sqlite3

import rtk.dao.DAO as _dao
from rtk.dao.SQLite3 import Model as SQLite3


class TestSQLite3Model(unittest.TestCase):
    """
    Class for testing the SQLite3 model class.
    """

    def setUp(self):
        """
        Method to setup the test fixture for the Environment model class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self.DUT = _dao(_database)

    def test_create_sqlite3(self):
        """
        Method to test that the DAO creates an SQLite3 model and valid
        connection attribute.
        """

        self.assertTrue(isinstance(self.DUT, _dao))
        self.assertTrue(isinstance(self.DUT.model.connection,
                                   sqlite3.Connection))

    def test_execute(self):
        """
        Method to test that the DAO can execute an SQL query.
        """

        _query = "SELECT * FROM tbl_revisions"

        self.assertEqual(self.DUT.execute(_query)[1], 0)

    def test_get_next_id(self):
        """
        Tests that the next ID can be retrieved.
        """

        self.assertEqual(self.DUT.get_last_id('tbl_functions')[1], 0)
