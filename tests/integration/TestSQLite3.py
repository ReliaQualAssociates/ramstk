#!/usr/bin/env python -O
"""
This is the test class for testing the Environment class.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.unit.TestDAO.py is part of The RTK Project
#
# All rights reserved.
import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import sqlite3

import unittest
from nose.plugins.attrib import attr

import dao.DAO as _dao

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'


class TestSQLite3Model(unittest.TestCase):
    """
    Class for testing the SQLite3 model class.
    """

    def setUp(self):
        """
        (TestSQLite3) setup the test fixture for the SQLite3 model class
        """

        _database = '/tmp/tempdb.rtk'
        self.DUT = _dao(_database)

    @attr(all=True, integration=True)
    def test_create_sqlite3(self):
        """
        (TestSQLite3) SQLite3 __init__() should return an sqlite3.Connection
        """

        self.assertTrue(isinstance(self.DUT, _dao))
        self.assertTrue(isinstance(self.DUT.model.connection,
                                   sqlite3.Connection))

    @attr(all=True, integration=True)
    def test_execute(self):
        """
        (TestSQLite3) execute should return 0 when an SQL query is successfully executed
        """

        _query = "SELECT * FROM tbl_revisions"

        self.assertEqual(self.DUT.execute(_query)[1], 0)

    @attr(all=True, integration=True)
    def test_get_next_id(self):
        """
        (TestSQLite3) Tests that the next ID can be retrieved.
        """

        self.assertEqual(self.DUT.get_last_id('tbl_functions')[1], 0)
