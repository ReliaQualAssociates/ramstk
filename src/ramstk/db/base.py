# -*- coding: utf-8 -*-
#
#       ramstk.db.base.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Base Database Module."""

# Standard Library Imports
import sqlite3
from typing import Any, Dict, List, TextIO, Tuple

# Third Party Imports
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pubsub import pub
from sqlalchemy import and_, create_engine, exc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError


def do_open_session(database: str) -> Tuple[Engine, scoped_session]:
    """Create a session to be used with an instance of the BaseDatabase."""
    engine = create_engine(database)
    engine.connect()

    return (engine,
            scoped_session(
                sessionmaker(autocommit=False, autoflush=False, bind=engine)))


class BaseDatabase():
    """This is the BaseDatabase class."""

    # Define public class dict attributes.
    cxnargs: Dict[str, str] = {
        'dialect': '',
        'user': '',
        'password': '',
        'host': '',
        'port': '',
        'dbname': ''
    }

    # Define public class scalar attributes.
    engine: Engine = None
    session: scoped_session = None
    database: str = ''
    sqlstatements: Dict[str, str] = {
        'select': 'SELECT {0:s} ',
        'from': 'FROM {0:s} ',
        'order': 'ORDER BY {0:s} DESC LIMIT 1'
    }

    def __init__(self) -> None:
        """Initialize an instance of the BaseDatabase."""

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

    def do_connect(self, database: Dict) -> None:
        """
        Connect to the database.

        :param dict database: the connection information for the database to
            connect to.
        :return: None
        :rtype: None
        :raise: sqlalchemy.exc.OperationalError if passed an invalid database
            URL.
        :raise: sqlalchemy.exc.ArgumentError if passed a database URL with
            an unknown/unsupported SQL dialect.
        """
        self.cxnargs['dialect'] = database['dialect']
        self.cxnargs['user'] = database['user']
        self.cxnargs['password'] = database['password']
        self.cxnargs['host'] = database['host']
        self.cxnargs['port'] = database['port']
        self.cxnargs['dbname'] = database['database']

        try:
            if self.cxnargs['dialect'] == 'sqlite':
                self.database = 'sqlite:///' + self.cxnargs['dbname']
            elif self.cxnargs['dialect'] == 'postgres':
                self.database = ('postgresql+psycopg2://'
                                 + self.cxnargs['user'] + ':'
                                 + self.cxnargs['password'] + '@'
                                 + self.cxnargs['host'] + ':'
                                 + self.cxnargs['port'] + '/'
                                 + self.cxnargs['dbname'])
            else:
                raise DataAccessError('Unknown database dialect in database '
                                      'connection dict.')
        except TypeError:
            raise DataAccessError('Unknown dialect or non-string value in '
                                  'database connection dict.')

        if self.database != '':
            self.engine, self.session = do_open_session(self.database)

    @staticmethod
    def do_create_program_db(database: Dict, sql_file: TextIO) -> None:
        """
        Create a shiny new, unpopulated RAMSTK program database.

        :param str database: the absolute path to the database to connect to.
        :param dict sql_file: a dict containing the database connection
            arguments.
        :return: None
        :rtype: None
        """
        if database['dialect'] == 'sqlite':
            conn = sqlite3.connect(database['database'])
            conn.executescript(sql_file.read().strip())
        elif database['dialect'] == 'postgres':
            # Create the database.
            conn = psycopg2.connect(host=database['host'],
                                    dbname='postgres',
                                    user=database['user'],
                                    password=database['password'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

            cursor = conn.cursor()
            cursor.execute(
                sql.SQL('DROP DATABASE IF EXISTS {}').format(
                    sql.Identifier(database['database'])))
            cursor.execute(
                sql.SQL('CREATE DATABASE {}').format(
                    sql.Identifier(database['database'])))
            cursor.close()
            conn.close()

            # Populate the database.
            conn = psycopg2.connect(host=database['host'],
                                    dbname=database['database'],
                                    user=database['user'],
                                    password=database['password'])
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            conn.set_session(autocommit=True)

            cursor = conn.cursor()
            cursor.execute(sql_file.read())
            cursor.close()

        conn.close()

    def do_delete(self, item: object) -> None:
        """
        Delete a record from the RAMSTK Program database.

        :param item: the item to remove from the RAMSTK Program database.
        :type item: Object()
        :return: None
        :rtype: None
        """
        if self.cxnargs['dialect'] == 'sqlite':
            self.session.execute(
                "PRAGMA foreign_keys=ON")

        try:
            self.session.delete(item)
            self.session.commit()
        except exc.InvalidRequestError as _error:
            # This exception generally corresponds to runtime state errors.
            # These types of errors are unlikely to be user errors and will
            # most likely be the result of a corrupted database.  Some
            # situations that can raise this exception are:
            #   1. Attempting to delete a record from a non-existent table.
            self.session.rollback()
            _error_message = (
                "There was an database error when attempting to delete a "
                "record.  Error returned from database was:\n\t{0:s}.".format(
                    str(_error)))
            pub.sendMessage('fail_delete_record', error_message=_error_message)
            raise DataAccessError(_error_message)
        except exc.OperationalError as _error:
            # This exception is raised when there is an error during
            # execution of a SQL statement.  These types of errors are
            # unlikely to be user errors and will most likely be the result of
            # a corrupted database.  Some situations that can raise this
            # exception are:
            #   1. Foreign key exists, but foreign table does not.
            self.session.rollback()
            _error_message = (
                "There was an database error when attempting to delete a "
                "record.  Error returned from database was:\n\t{0:s}.".format(
                    str(_error.orig)))
            pub.sendMessage('fail_delete_record', error_message=_error_message)
            raise DataAccessError(_error_message)

    def do_disconnect(self) -> None:
        """
        Close the current session.

        :return: None
        :rtype: None
        """
        self.session.close()
        self.session = None
        self.database = ''

    def do_insert(self, record: object) -> None:
        """
        Add a new record to a database table.

        :param record: the object to add to the RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            self.session.add(record)
            self.session.commit()
        except exc.StatementError as _error:
            # This exception is raised when there is an error during
            # execution of a SQL statement.  These types of errors are
            # unlikely to be user errors as the programmer should ensure
            # everything is ready to insert.  Some situations that can raise
            # this exception are:
            #   1. Primary key violations.
            #   2. Non-date data supplied to date type fields.
            #   3. Foreign key violations.
            #   4. np.nan data suppled to any field type.
            self.session.rollback()
            _error_message = (
                "There was an database error when attempting to add a "
                "record.  Faulty SQL statement was:\n\t{0:s}.\nParameters "
                "were:\n\t{1:s}.".format(str(_error.statement),
                                         str(_error.params)))
            pub.sendMessage('fail_insert_record', error_message=_error_message)
            raise DataAccessError(_error_message)

    def do_insert_many(self, records: List[object]) -> None:
        """
        Add a group of new records to a database table.

        :param list records: the list of objects to add to the RAMSTK database.
        :return: None
        :rtype: None
        """
        for _record in records:
            self.do_insert(_record)

    def do_select_all(self, table, key=None, value=None, order=None,
                      _all=True) -> None:
        """
        Select all records from the RAMSTK database for table.

        :param table: the database table object to select all from.
        :keyword key: the index key in the table.
        :keyword value: the value of the index key.
        :keyword order: the field to order returned results.
        :keyword _all: whether to return all records or only the first record.
        :return: a list of table instances; one for each record.
        """
        _results = []
        if isinstance(key, list):
            _results = self.session.query(table).filter(
                and_(key[0] == value[0],
                     key[1] == value[1]))
        else:
            _results = self.session.query(table).filter(key == value)

        if order is not None:
            _results = _results.order_by(order)

        if _all:
            _results = _results.all()
        else:
            _results = _results.first()

        return _results

    def do_update(self, record=None) -> None:
        """
        Update the RAMSTK database with any pending changes.

        :keyword record: the record to update in the database.
        :return: None
        :rtype: None
        """
        if not record is None:
            self.session.add(record)

        self.session.commit()

    def get_last_id(self, table: str, id_column: str) -> Any:
        """
        Retrieve the last used value of the ID column.

        .. hint:: This method could be used to select the last used value from
            any column in a table.

        :param str table: the name of the table to get the last ID from.
        :param str id_column: the name of the field to use as the ID column.
        :return: _last_id; the last used value of the ID column.
        :rtype: int
        :raise: :class:`sqlalchemy.exc.OperationalError` if passed an unknown
            table or unknown column name.
        """
        # This ensures the column name is prefixed with fld_ in case the
        # table's attribute name was passed instead.
        if id_column[0:4] != 'fld_':
            id_column = 'fld_' + id_column

        _sql_statement = self.sqlstatements['select'].format(
            id_column) + self.sqlstatements['from'].format(
                table) + self.sqlstatements['order'].format(id_column)

        return self.session.execute(_sql_statement).first()[0]
