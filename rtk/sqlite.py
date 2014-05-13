#!/usr/bin/env python
""" Provides the class and methods for interfacing with a SQLite3
    database backend.
"""

__author__ = 'Andrew Rowland'
__email = 'andrew.rowland@reliaqual.com'
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

        @param database: the absolute path to the database to be opened.
        """
# TODO: Make the connection object an instance attribute.
        cnx = sqlite3.connect(database, isolation_level=None)

        self._is_closed = False

        return cnx

    def execute_query(self, query, values, cnx, commit=False):
        """
        Executes a query on the SQLite database and returns the results.

        @param query: the query to execute.
        @type query: string
        @param values: a typle containing the values to insert into the query.
        @type values: tuple
        @param cnx: the connection to use when executing the query.
        @type cnx: SQLite3 connection
        @param commit: whether or not to commit the results.
        @type commit: boolean
        """
# TODO: Revise to eliminate the values parameter.
# TODO: Return the error message and process locally in the calling module.
        with cnx:
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
                        self._app.debug_log.error(e.args[0])
                        self._app.debug_log.error(query)
                        results = False

            except sqlite3.Error, e:
                self._app.debug_log.error(e)
                self._app.debug_log.error(query)
                results = False

            cur.close()

        return results
