#!/usr/bin/env python
"""
Provides the class and methods for interfacing with a SQLite3 database backend.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       sqlite3.py is part of The RTK Project
#
# All rights reserved.

try:
    import sqlite3
    HASSQLITE3 = True
except ImportError:
    HASSQLITE3 = False


class SQLite3Interface(object):
    """
    The SQLite3Interface class is used to represent an SQLite3 database
    connection.
    """

    def __init__(self, application):
        """
        Initializes the SQLite3 interface class.

        @param application: the current instance of the RTK application.
        """

        self._version = None
        self._app = application
        self._is_closed = True

    def get_connection(self, database):
        """
        Opens a connections to a database.

        :param STR database: the absolute path to the database to be opened.
        """
# TODO: Make the connection object an instance attribute.
        cnx = sqlite3.connect(database, isolation_level=None)

        self._is_closed = False

        return cnx

    def execute_query(self, query, values, cnx, commit=False):
        """
        Executes a query on the SQLite database and returns the results.

        :param str query: the query to execute.
        :param tuple values: a typle containing the values to insert into the
                             query.
        :param sqlite3.connect cnx: the connection to use when executing the
                                    query.
        :param boolean commit: whether or not to commit the results.
        :return: results of the query, True if a commit query, and False if an
                 error is encountered.
        :rtype: list of tuples or boolean
        """
# TODO: Revise to eliminate the values parameter.
# TODO: Return the error code and process locally in the calling module.
        with cnx:
            _cursor = cnx.cursor()

            try:
                if values is None:
                    _cursor.execute(query)
                else:
                    _cursor.execute(query, values)

                if not commit:
                    try:
                        _results = _cursor.fetchall()
                    except sqlite3.Error, _error:
                        _err_code = self._error_handler(_error)
                        try:
                            self._app.debug_log.error(_error)
                            self._app.debug_log.error(query)
                        except AttributeError:
                            pass
                        _results = False
                else:
                    try:
                        cnx.commit()
                        _results = True
                    except sqlite3.Error, _error:
                        _err_code = self._error_handler(_error)
                        cnx.rollback()
                        try:
                            self._app.debug_log.error(_error.args[0])
                            self._app.debug_log.error(query)
                        except AttributeError:
                            pass
                        _results = False

            except sqlite3.Error, _error:
                _err_code = self._error_handler(_error)
                try:
                    self._app.debug_log.error(_error)
                    self._app.debug_log.error(query)
                except AttributeError:
                    pass
                _results = False

            _cursor.close()

        return _results

    def _error_handler(self, msg):
        """
        Method to handle SQLite3 errors and return actionable error codes.

        :param str msg: the error message to parse.
        :return: _err_code
        :rtype: int
        """

        _err_code = 0
        if "PRIMARY KEY must be unique" in msg[0]:      # Primary key not unique.
            _err_code = 1555
        else:
            print msg[0]

        return _err_code
