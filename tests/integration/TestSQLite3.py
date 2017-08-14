#!/usr/bin/env python -O
"""
This is the test class for testing the Environment class.
"""

# -*- coding: utf-8 -*-
#
#       rtk.tests.unit.TestDAO.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys
from os.path import dirname

sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk", )

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
    def test01_create_sqlite3(self):
        """
        (TestSQLite3) SQLite3 __init__() should return an sqlite3.Connection
        """

        self.assertTrue(isinstance(self.DUT, _dao))
        self.assertTrue(isinstance(self.DUT.model.connection,
                                   sqlite3.Connection))

    @attr(all=True, integration=True)
    def test02_execute(self):
        """
        (TestSQLite3) execute should return 0 when an SQL query is successfully executed
        """

        _query = "SELECT * FROM tbl_revisions"

        self.assertEqual(self.DUT.execute(_query)[1], 0)

    @attr(all=True, integration=True)
    def test03_get_next_id(self):
        """
        (TestSQLite3) Tests that the next ID can be retrieved.
        """

        self.assertEqual(self.DUT.get_last_id('tbl_functions')[1], 0)
