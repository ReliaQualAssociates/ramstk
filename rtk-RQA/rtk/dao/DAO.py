#!/usr/bin/env python
"""
The DAO Package.
"""

# -*- coding: utf-8 -*-
#
#       rtk.dao.DAO.py is part of The RTK Project
#
# All rights reserved.

# Import the database models.
from SQLite3 import Model as SQLite3

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class DAO(object):
    """
    This is the data access controller class.

    :ivar model: an instance of the database class selected for data access.
    """

    def __init__(self, database, db_type=0):
        """
        Method to initialize an instance of the DAO controller.

        :param str database: the full path of the database to connect to.
        :keyword int db_type: the type of database to connect to.  Options are:
                              * SQLite3 = 0 (default)
                              * MySQL/MariaDB = 1
        """

        if db_type == 0:
            self.model = SQLite3()
        elif db_type == 1:
            pass

        self.model.connect(database)

    def execute(self, query, commit=False):
        """
        Method to execute the passed query.

        :param str query: the SQL query to execute.
        :keyword bool commit: indicates whether or not to commit query.
        :return: (_results, _error_code); the results of the query and the
                                          error code produced.
        :rtype: tuple
        """

        (_results, _error_code, _last_id) = self.model.execute(query, commit)

        return(_results, _error_code, _last_id)

    def get_last_id(self, table):
        """
        Retrieves the next value to be used in the autoincrement field for the
        passed table.

        :param str table: the name of the table to get the next value.
        :return: _next_id
        :rtype: int
        """

        _last_id = self.model.get_last_id(table)

        return _last_id

    def close(self):
        """
        Method to close the database connection.
        """

        self.model.connection.close()
