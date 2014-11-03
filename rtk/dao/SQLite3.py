#!/usr/bin/env python
"""
The SQLite3 Package.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       SQLite3.py is part of The RTK Project
#
# All rights reserved.

try:
    import sqlite3
    HASSQLITE3 = True
except ImportError:
    HASSQLITE3 = False


def error_handler(message):
    """
    Method to handle SQLite3 errors and return actionable error codes.

    :param str msg: the error message to parse.
    :return: _err_code
    :rtype: int
    """

    _error_code = 0

    if "PRIMARY KEY must be unique" in message[0]:  # Primary key not unique.
        _error_code = 1555
    elif "syntax error" in message[0]:      # Syntax error in SQL statement.
        _error_code = 78
    else:
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

        pass

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

    def _get_last_id(self, cursor):
        """
        Method to retrieve the last value used in the autoincrement field.
        """

        _query = "SELECT seq FROM sqlite_sequence"
