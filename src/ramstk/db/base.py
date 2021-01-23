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
import psycopg2  # type: ignore
from psycopg2 import sql  # type: ignore
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  # type: ignore
from pubsub import pub
# noinspection PyPackageRequirements
from sqlalchemy import create_engine, exc
# noinspection PyPackageRequirements,PyProtectedMember
from sqlalchemy.engine import Engine  # type: ignore
# noinspection PyPackageRequirements
from sqlalchemy.orm import query, scoped_session, sessionmaker  # type: ignore
from sqlalchemy.orm.exc import FlushError  # type: ignore

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError


def do_create_program_db(database: Dict[str, str], sql_file: TextIO) -> None:
    """Create a shiny new, unpopulated RAMSTK program database.

    :param database: a dict containing the database connection arguments.
    :param sql_file: the absolute path to the text file containing the
        SQL statements for creating a bare RAMSTK Program Database.
    :return: None
    :rtype: None
    """
    conn: Any = ''

    if database['dialect'] == 'sqlite':
        conn = sqlite3.connect(database['database'])
        conn.executescript(sql_file.read().strip())
    elif database['dialect'] == 'postgres':
        # Create the database.
        conn = psycopg2.connect(
            host=database['host'],
            dbname='postgres',
            user=database['user'],
            # deepcode ignore NoHardcodedPasswords:
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
        conn = psycopg2.connect(
            host=database['host'],
            dbname=database['database'],
            user=database['user'],
            # deepcode ignore NoHardcodedPasswords:
            password=database['password'])
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        conn.set_session(autocommit=True)

        cursor = conn.cursor()
        cursor.execute(sql_file.read())
        cursor.close()

    conn.close()


def do_open_session(database: str) -> Tuple[Engine, scoped_session]:
    """Create a session to be used with an instance of the BaseDatabase."""
    engine: Any = create_engine(database)
    # deepcode ignore missing~close~connect: engines are disposed
    engine.connect()

    return (engine,
            scoped_session(
                sessionmaker(autocommit=False, autoflush=False, bind=engine)))


# noinspection PyUnresolvedReferences
class BaseDatabase:
    """The BaseDatabase class."""

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
    engine: Engine = None  # type: ignore
    session: scoped_session = None  # type: ignore
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
        """Connect to the database.

        :param database: the connection information for the database to
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
        except TypeError as _error:
            raise DataAccessError('Unknown dialect or non-string value in '
                                  'database connection dict.') from _error

        if self.database != '':
            self.engine, self.session = do_open_session(self.database)

    def do_delete(self, item: object) -> None:
        """Delete a record from the RAMSTK Program database.

        :param item: the item to remove from the RAMSTK Program database.
        :type item: Object()
        :return: None
        :rtype: None
        """
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
            raise DataAccessError(_error_message) from _error
        except exc.ProgrammingError as _error:
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
            raise DataAccessError(_error_message) from _error

    def do_disconnect(self) -> None:
        """Close the current session.

        :return: None
        :rtype: None
        """
        self.session.close()
        self.engine.dispose()
        # noinspection PyTypeChecker
        self.session = None  # type: ignore
        self.database = ''

    def do_insert(self, record: object) -> None:
        """Add a new record to a database table.

        :param record: the object to add to the RAMSTK Program database.
        :return: None
        :rtype: None
        """
        try:
            self.session.add(record)
            self.session.commit()
        except (exc.IntegrityError, exc.StatementError) as _error:
            # This exception is raised when there is an error during
            # execution of a SQL statement.  These types of errors are
            # unlikely to be user errors as the programmer should ensure
            # everything is ready to insert.  Some situations that can raise
            # this exception are:
            #   1. Primary key violations.
            #   2. Non-date data supplied to date type fields.
            #   3. Foreign key violations.
            #   4. np.nan data supplied to any field type.
            #
            # With psycopg2, _error will have attributes pgcode and pgerror.
            # The first is a code associated with the error captured by
            # psycopg2 and the second is the original error message from the
            # database.  These should be used to generate the error message
            # to send to the client.  Error codes are defined in the
            # errorcodes.py file in the psycopg2 code base.
            self.session.rollback()
            print(_error.orig.pgerror)
            _error_message = (
                "do_insert: Database error when attempting to add a record.  "
                "Database returned:\n\t{0:s}".format(
                    str(_error.orig.pgerror.split(':')[2].strip())))
            pub.sendMessage(
                'fail_insert_record',
                error_message=_error_message,
            )
            raise DataAccessError(_error_message) from _error
        except FlushError as _error:
            self.session.rollback()
            _error_message = (
                "do_insert: Flush error when attempting to add records.  "
                "Database returned:\n\t{0:s}".format(str(_error)))
            pub.sendMessage(
                'fail_insert_record',
                error_message=_error_message,
            )
            raise DataAccessError(_error_message) from _error

    def do_insert_many(self, records: List[object]) -> None:
        """Add a group of new records to a database table.

        :param list records: the list of objects to add to the RAMSTK database.
        :return: None
        :rtype: None
        """
        for _record in records:
            self.do_insert(_record)

    def do_select_all(self, table, **kwargs) -> query.Query:
        """Select all records from the RAMSTK database for table.

        :param table: the database table object to select all from.
        :return: a list of table instances; one for each record.
        """
        _keys: List[str] = kwargs.get('key', None)
        _values: List[Any] = kwargs.get('value', None)
        _order: Any = kwargs.get('order', None)
        _all: bool = kwargs.get('_all', True)

        _filters = {}
        if _keys is not None:
            for _idx, _key in enumerate(_keys):
                _filters[_key] = _values[_idx]

        _results = self.session.query(table).filter_by(**_filters)
        if isinstance(_order, list):
            _results = _results.order_by(*_order)
        else:
            _results = _results.order_by(_order)

        if _all:
            _results = _results.all()
        else:
            _results = _results.first()

        return _results

    def do_update(self, record: object = None) -> None:
        """Update the RAMSTK database with any pending changes.

        :keyword record: the record to update in the database.
        :return: None
        :rtype: None
        """
        if record is not None:
            self.session.add(record)

        try:
            self.session.commit()
        except (exc.InvalidRequestError, exc.ProgrammingError) as _error:
            self.session.rollback()
            _error_message = (
                "There was an database error when attempting to update a "
                "record.  Faulty SQL statement was:\n\t{0:s}.\nParameters "
                "were:\n\t{1:s}.".format(
                    str(_error.statement),  # type: ignore
                    str(_error.params)))  # type: ignore
            pub.sendMessage('fail_update_record', error_message=_error_message)
            raise DataAccessError(_error_message) from _error

    def get_database_list(self, database: Dict[str, str]) -> List:
        """Retrieve the list of program databases available to RAMSTK.

        This method is used to create a user-selectable list of databases when
        using the postgresql or MariaDB (MySQL) backend.  SQLite3 simply uses
        an open file dialog.

        :param database: the connection information for the dialect's
            administrative database.
        :return: the list of databases available to RAMSTK for the selected
            dialect.
        :rtype: list
        """
        _databases = []

        if database['dialect'] == 'postgres':
            _query = (self.sqlstatements['select'].format('datname')
                      + self.sqlstatements['from'].format('pg_database;'))
            _database: str = ('postgresql+psycopg2://' + database['user'] + ':'
                              + database['password'] + '@' + database['host']
                              + ':' + database['port'] + '/'
                              + database['database'])
            # pylint: disable=unused-variable
            __, _session = do_open_session(_database)

            # Make list of available databases, but only those associated with
            # RAMSTK.
            for db in _session.execute(_query):
                if db[0] not in ['postgres', 'template0', 'template1']:
                    _databases.append(db[0])

        return _databases

    def get_last_id(self, table: str, id_column: str) -> Any:
        """Retrieve the last used value of the ID column.

        .. hint:: This method could be used to select the last used value from
            any column in a table.

        :param table: the name of the table to get the last ID from.
        :param id_column: the name of the field to use as the ID column.
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

        try:
            _last_id = self.session.execute(_sql_statement).first()[0]
        except (exc.ProgrammingError, TypeError):
            _last_id = 0

        return _last_id
