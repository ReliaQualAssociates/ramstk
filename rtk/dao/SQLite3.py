#!/usr/bin/env python
"""
############################
SQLite3 Package Data Module
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.dao.SQLite3.py is part of The RTK Project
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

try:
    import sqlite3
    HASSQLITE3 = True
except ImportError:
    HASSQLITE3 = False

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


def error_handler(message):
    """
    Method to handle SQLite3 errors and return actionable error codes.

    :param str message: the error message to parse.
    :return: _err_code
    :rtype: int
    """

    _error_code = 0

    if "PRIMARY KEY must be unique" in message[0]:  # Primary key not unique.
        _error_code = 1555
    elif "syntax error" in message[0]:              # Syntax error in SQL statement.
        _error_code = 78
    elif "database is locked" in message[0]:        # Database is locked.
        _error_code = 5
    elif "foreign key constraint failed" in message[0]:
        _error_code = 787
    else:
        print "Unhandled error in SQLite3.py: {0:s}".format(message)
        _error_code = message[0]

    return _error_code


class Model(object):
    """
    This is the SQLite3 data access model.
    """

    def __init__(self):
        """
        Method to initialize an instance of the SQLite3 model.
        """

        self.connection = None

    def connect(self, database):
        """
        Method to connect to a database.

        :param str database: the full path to the database to connect to.
        """
        
        self.connection = sqlite3.connect(database, isolation_level=None)

    def execute(self, query, commit=False):
        """
        Method to execute a query against the database.

        :param str query: the SQL query to execute.
        :keyword bool commit: indicates whether or not to commit query.
        :return: (_results, _error_code); the results of the query and the
                                          error code produced.
        :rtype: tuple
        """

        _error_code = 0
        _last_id = -1

        with self.connection:
            _cursor = self.connection.cursor()

            try:
                _cursor.execute(query)

                if not commit:
                    try:
                        _results = _cursor.fetchall()
                    except sqlite3.Error, _error:
                        _error_code = error_handler(_error)
                        _results = False
                else:
                    try:
                        _cursor.execute("SELECT last_insert_rowid()")
                        _last_id = _cursor.fetchall()[0][0]
                        self.connection.commit()
                        _results = True
                    except sqlite3.Error, _error:
                        _error_code = error_handler(_error)
                        self.connection.rollback()
                        _results = False

            except sqlite3.Error, _error:
                _error_code = error_handler(_error)
                _results = False

            _cursor.close()

        return(_results, _error_code, _last_id)

    def get_last_id(self, table):
        """
        Retrieves the last value to be used in the autoincrement field for the
        passed table.

        :param str table: the name of the table to get the next value.
        :return: (_last_id, _error_code)
        :rtype: tuple
        """

        _error_code = 0

        _query = "SELECT seq \
                  FROM sqlite_sequence \
                  WHERE name='{0:s}'".format(table)

        with self.connection:
            _cursor = self.connection.cursor()
            _cursor.execute(_query)
            try:
                _last_id = _cursor.fetchall()
                _last_id = _last_id[0][0]
            except sqlite3.Error, _error:
                _error_code = error_handler(_error)
                _last_id = -1
            except IndexError:
                _last_id = -1

        _cursor.close()

        return(_last_id, _error_code)
