# -*- coding: utf-8 -*-
#
#       ramstk.dao.DAO.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Data Access Object (DAO) Package."""

import gettext

from sqlalchemy import create_engine, exc, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Import tables objects for the RAMSTK Common database.
from .RAMSTKCommonDB import create_common_db
from .RAMSTKProgramDB import create_program_db

RAMSTK_BASE = declarative_base()

# Add localization support.
_ = gettext.gettext

__author__ = 'Doyle Rowland'
__email__ = 'doyle.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Doyle "weibullguy" Rowland'


class DAO(object):
    """This is the data access controller class."""

    RAMSTK_SESSION = sessionmaker()

    # Define public class scalar attributes.
    engine = None
    metadata = None
    session = None
    database = None

    def __init__(self):
        """Initialize an instance of the DAO controller."""

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

    def db_connect(self, database):
        """
        Connect to the database using settings from the configuration file.

        :param str database: the absolute path to the database to connect to.
        :return: False if successful, True if an error occurs.
        :rtype: bool
        """
        self.database = database
        self.engine = create_engine(self.database, echo=False)
        self.metadata = MetaData(self.engine)

        self.session = self.RAMSTK_SESSION(
            bind=self.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        return False

    def db_close(self):
        """
        Close the current session.

        :return: False if successful, True if an error occurs.
        :rtype: bool
        """
        self.session.close()
        self.RAMSTK_SESSION.close_all()
        self.engine.dispose()
        self.session = None
        self.engine = None
        self.metadata = None
        self.database = None

        return False

    def _db_table_create(self, table):
        """
        Check if the passed table exists and create it if not.

        :param table: the table to check for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self.engine.dialect.has_table(self.engine.connect(),
                                             str(table)):
            table.create(bind=self.engine)

        return _return

    @staticmethod
    def db_create_common(database, **kwargs):
        """
        Create a new RAMSTK Common database.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """
        _test = kwargs['test']
        try:
            return create_common_db(database=database, test=_test)
        except (IOError, exc.SQLAlchemyError, exc.DBAPIError,
                exc.OperationalError):
            return True
        except ArgumentError:  # pylint: disable=undefined-variable # noqa
            print "Bad common database URI: {0:s}".format(database)
            return True

    @staticmethod
    def db_create_program(database):
        """
        Create a new RAMSTK Program database.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """
        try:
            return create_program_db(database=database)
        except IOError:
            print "IOError"
            return True
        except exc.SQLAlchemyError:
            print "SQLAlchemyError"
            return True
        except exc.DBAPIError:
            print "DBAPIError"
            return True
        except exc.OperationalError:
            print "OperationalError"
            return True
        except ArgumentError:  # pylint: disable=undefined-variable  # noqa
            print "Bad program database URI: {0:s}".format(database)
            return True

    @staticmethod
    def db_add(item, session):
        """
        Add a new item to the RAMSTK Program database.

        :param item: the object to add to the RAMSTK Program database.
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RAMSTK Program database.
        :type session: :class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Adding one or more items to the RAMSTK Program " \
               "database."
        # TODO: Determine if the add_many option can work with Foreign Keys.
        for _item in item:
            try:
                session.add(_item)
                session.commit()
            except (exc.SQLAlchemyError, exc.DBAPIError) as error:
                _error = '{0:s}'.format(error)
                session.rollback()
                if 'Could not locate a bind' in _error:
                    _error_code = 2
                    _msg = ('RAMSTK ERROR: No database open when attempting '
                            'to insert record.')
                elif ('PRIMARY KEY must be unique' in _error) or (
                        'UNIQUE constraint failed:' in _error):
                    _error_code = 3
                    _msg = ('RAMSTK ERROR: Primary key error: '
                            '{0:s}').format(_error)
                elif 'Date type only accepts Python date objects as input' in _error:
                    _error_code = 4
                    _msg = ('RAMSTK ERROR: Date field did not contain Python '
                            'date object: {0:s}').format(_error)
                else:
                    print _error
                    _error_code = 1
                    _msg = (
                        'RAMSTK ERROR: Adding one or more items to the RAMSTK '
                        'Program database.')
            except ValueError as _error:
                _error_code = 4
                _msg = ('RAMSTK ERROR: Date field did not contain Python '
                        'date object: {0:s}').format(_error)

        return _error_code, _msg

    @staticmethod
    def db_update(session):
        """
        Update the RAMSTK Program database with any pending changes.

        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RAMSTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating the RAMSTK Program database."

        try:
            session.commit()
        except (exc.SQLAlchemyError, exc.DBAPIError) as error:
            print error
            session.rollback()
            _error_code = 1
            _msg = "RAMSTK ERROR: Updating the RAMSTK Program database."

        return _error_code, _msg

    @staticmethod
    def db_delete(item, session):
        """
        Delete a record from the RAMSTK Program database.

        :param item: the item to remove from the RAMSTK Program database.
        :type item: Object()
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RAMSTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Deleting an item from the RAMSTK Program database."

        try:
            session.delete(item)
            session.commit()
        except (exc.SQLAlchemyError, exc.DBAPIError) as error:
            print error
            session.rollback()
            _error_code = 1
            _msg = "RAMSTK ERROR: Deleting an item from the RAMSTK Program database."

        return _error_code, _msg

    @staticmethod
    def db_query(query, session=None):
        """
        Execute an SQL query against the connected database.

        :param str query: the SQL query string to execute
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RAMSTK Program database.
        :type session: :class:`sqlalchemy.orm.scoped_session`
        :return:
        :rtype: str
        """
        return session.execute(query)

    @property
    def db_last_id(self):
        """
        Retrieve the value of the last ID column from a table in the database.

        :return: _last_id; the last value of the ID column.
        :rtype: int
        """
        _last_id = 0
        # TODO: Write the db_last_id method if needed, else remove from file.
        return _last_id
