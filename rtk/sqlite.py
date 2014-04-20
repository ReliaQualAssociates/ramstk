#!/usr/bin/env python
""" Provides the class and methods for interfacing with a SQLite3
    database backend.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

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


class SQLite3Interface:

    """
    The SQLite3Interface class is used to represent an SQLite3 database
    connection.
    """

    def __init__(self, application):

        """
        Initializes the SQLite3 interface class.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._version = None
        self._app = application
        self._is_closed = True

    def get_connection(self, database):

        """
        Opens a connections to a database.

        Keyword Arguments:
        sqlite_info -- list containing SQLite login information.
                       [0] -
                       [1] -
                       [2] - SQLite3 database
                       [3] - SQLite3 user
                       [4] - SQLite3 user password
        """

        cnx = sqlite3.connect(database, isolation_level=None)

        self._is_closed = False

        return(cnx)

    def execute_query(self, query, values, cnx, commit=False):
        """
        Executes a query on the SQLite database and returns the results.

        @param string query: the query to execute.
        @param tuple values: a typle containing the values to insert into the
                             query.
        @param cnx: the connection to use when executing the query.
        @param boolean commit: whether or not to commit the results.
        """
#TODO: Revise to eliminate the values parameter.
        cur = cnx.cursor()

        try:
            if values is None:
                cur.execute(query)
            else:
                cur.execute(query, values)

            if not commit:
                try:
                    results = cur.fetchall()
                except sqlite3.Error, e:
                    self._app.debug_log.error(e)
                    self._app.debug_log.error(query)
                    results = False
            else:
                try:
                    cnx.commit()
                    results = True
                except sqlite3.Error, e:
                    self._app.debug_log.error(e)
                    self._app.debug_log.error(query)
                    results = False

        except sqlite3.Error, e:
            self._app.debug_log.error(e)
            self._app.debug_log.error(query)
            results = False

        cur.close()

        return results
