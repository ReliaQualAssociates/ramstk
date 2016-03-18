#!/usr/bin/env python -O
"""
This is the test package for testing RTK.
"""

# -*- coding: utf-8 -*-
#
#       tests.integration.__init__.py is part of The RTK Project
#
# All rights reserved.
import sys
import os
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import sqlite3

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2016 Andrew "weibullguy" Rowland'


def setUp():

    _database = '/tmp/tempdb.rtk'

    _connection =sqlite3.connect(_database)
    _cursor = _connection.cursor()

    # Create the temporary database.
    _sqlfile = open('/home/andrew/projects/RTK/devtools/mkTestDB.sql', 'r')
    for _query in _sqlfile.read().split(';'):
        try:
            _cursor.execute(_query)
        except Exception as e:
            print _database + ': ' + str(e)
            print _query
            _cursor.close()
            raise

    _connection.commit()

    # Clean up.
    _sqlfile.close()
    _cursor.close()
    _connection.close()

def tearDown():

    _database = '/tmp/tempdb.rtk'

    if os.path.isfile(_database):
        os.remove(_database)
