#!/usr/bin/env python
"""
Provides the class and methods for interfacing with a MySQL database backend.
"""

# -*- coding: utf-8 -*-
#
#       mysql.py is part of The RTK Project
#
#       Copyright 2007-2013 Andrew "Weibullguy" Rowland <darowland@ieee.org>
#
# All rights reserved.

try:
    import MySQLdb
    has_mysqldb = True
except ImportError:
    has_mysqldb = False

# Import other RTK modules.
import Configuration as _conf
import Utilities as _util

class MySQLInterface:

    def __init__(self, application):

        self._version = None
        self._app = application

    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++
    # This function checks whether the version of python-mysqldb is greater
    # than or equal to the version that's passed to it.  Note that the tuple
    # only checks the major, minor, and sub versions; the sub-sub version is
    # weird, so we only check for 'final' versions.
    #
    # Inputs:
    #       1. self - the MySQLInterface class.
    #       2. v    - the version of python-mysqlbd we're using.
    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++
    def _mysqldb_gt_or_eq(self, v):

        ver = MySQLdb.version_info
        if ver[0] < v[0] or ver[1] < v[1] or ver[2] < v[2]:
            return False
        return True

    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++
    # This function simply checks whether we have the python-mysqldb module.
    #
    # Inputs:
    #       1. self - the MySQLInterface class.
    # +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++ +++++
    def get_supported_schemes(self):

        global has_mysqldb
        if has_mysqldb:
            return [ ('mysql', 1) ]
        else:
            return []

    def get_connection(self, mysql_info):

        """ Opens a connections to a database.

            Keyword Arguments:
            mysql_info -- list containing MySQL login information.
                          [0] - MySQL host
                          [1] - MySQL port
                          [2] - MySQL database
                          [3] - MySQL user
                          [4] - MySQL user password
        """

        # Check the port being used for the MySQL database.
        if mysql_info[1] is None:
            mysql_info[1] = 3306

        # Check the password.
        if mysql_info[4] is None:
            mysql_info[4] = ''

        # Make the connection to the database.
        if (self._mysqldb_gt_or_eq((1, 2, 1))):
            if(mysql_info[2] is None):
                cnx = MySQLdb.connect(host=mysql_info[0],
                                      user=mysql_info[3],
                                      passwd=mysql_info[4],
                                      charset='utf8')
            else:
                cnx = MySQLdb.connect(host=mysql_info[0],
                                      db=mysql_info[2],
                                      user=mysql_info[3],
                                      passwd=mysql_info[4],
                                      charset='utf8')
        else:
            cnx = MySQLdb.connect(host=mysql_info[0],
                                  port=mysql_info[1],
                                  db=mysql_info[2],
                                  user=mysql_info[3],
                                  passwd=mysql_info[4],
                                  use_unicode=True)
            self._set_character_set(cnx, 'utf8')

        self._is_closed = False

        return cnx

    def get_cursor(self, cnx):

        """ Retrieves a cursor from the open database.

            Keyword Arguments:
            cnx -- an open connection.

        """

        cursor = cnx.cursor()
        return cursor

    def execute_query(self, query, values, cnx, commit=False):

        """ Executes a query on the MySQL database and returns the results.

            Keyword Arguments:
            query  -- the query to execute.
            cnx    -- the connection to use when executing the query.
            commit -- whether or not to commit the results.
            values -- a typle containing the values to insert into the query.
        """

        if(values is not None):
            query = query % values

        cur = self.get_cursor(cnx)

        try:
            cur.execute(query)

            if not commit:
                try:
                    results = cur.fetchall()
                except:
                    self._app._log.error("mysql.py: MySQL error:")
                    self._app._log.error(repr(e))
                    _util.rtk_error(repr(e[1]))
                    results = False
            else:
                try:
                    cnx.commit()
                    results = True
                except:
                    self._app._log.error("mysql.py: MySQL error:")
                    self._app._log.error(repr(e))
                    _util.rtk_error(repr(e[1]))
                    results = False

        except MySQLdb.IntegrityError, e:
            self._app._log.error("mysql.py: MySQL integrity error:")
            self._app._log.error(repr(e))
            _util.rtk_error(repr(e[1]))
            results = False
        except MySQLdb.OperationalError, e:
            self._app._log.error("mysql.py: MySQL operational error:")
            self._app._log.error(repr(e))
            _util.rtk_error(repr(e[1]))
            results = False
        except MySQLdb.Error, e:
            self._app._log.error("mysql.py: MySQL error:")
            self._app._log.error(repr(e))
            _util.rtk_error(repr(e[1]))
            results = False
        except MySQLdb.Warning, e:
            self._app._log.error("mysql.py: MySQL warning:")
            self._app._log.error(repr(e))
            _util.rtk_error(repr(e[1]))
            results = False

        cur.close()

        return(results)
