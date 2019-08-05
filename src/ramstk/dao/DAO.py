# -*- coding: utf-8 -*-
#
#       ramstk.dao.DAO.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Data Access Object (DAO) Package."""

# Standard Library Imports
import gettext

# Third Party Imports
from sqlalchemy import MetaData, create_engine, event, exc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError
from ramstk.models.commondb import (
    RAMSTKRPN, RAMSTKCategory, RAMSTKCondition, RAMSTKFailureMode, RAMSTKGroup,
    RAMSTKHazards, RAMSTKLoadHistory, RAMSTKManufacturer, RAMSTKMeasurement,
    RAMSTKMethod, RAMSTKModel, RAMSTKSiteInfo, RAMSTKStakeholders,
    RAMSTKStatus, RAMSTKSubCategory, RAMSTKType, RAMSTKUser
)
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKAction, RAMSTKAllocation, RAMSTKCause, RAMSTKControl,
    RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKEnvironment,
    RAMSTKFailureDefinition, RAMSTKFunction, RAMSTKHardware,
    RAMSTKHazardAnalysis, RAMSTKMatrix, RAMSTKMechanism, RAMSTKMilHdbkF,
    RAMSTKMission, RAMSTKMissionPhase, RAMSTKMode, RAMSTKOpLoad,
    RAMSTKOpStress, RAMSTKProgramInfo, RAMSTKProgramStatus,
    RAMSTKReliability, RAMSTKRequirement, RAMSTKRevision, RAMSTKSimilarItem,
    RAMSTKStakeholder, RAMSTKTestMethod, RAMSTKValidation
)

# RAMSTK Local Imports
from .RAMSTKCommonDB import (
    RAMSTK_CATEGORIES, RAMSTK_CONDITIONS, RAMSTK_FAILURE_MODES,
    RAMSTK_GROUPS, RAMSTK_HAZARDS, RAMSTK_HISTORIES, RAMSTK_MANUFACTURERS,
    RAMSTK_MEASUREMENTS, RAMSTK_METHODS, RAMSTK_MODELS, RAMSTK_RPNS,
    RAMSTK_STAKEHOLDERS, RAMSTK_STATUSES, RAMSTK_SUBCATEGORIES, RAMSTK_TYPES
)

# Add localization support.
_ = gettext.gettext


# pylint: disable=too-many-locals
def do_create_common_db(**kwargs):
    """Create and populate the RAMSTK Common database."""
    import os
    from datetime import date, timedelta

    __test = kwargs['test']
    uri = kwargs['database']

    _cwd = os.getcwd()
    try:
        license_file = open(_cwd + '/license.key', 'r')
        _license_key = license_file.read()[0]
        _expire_date = license_file.read()[1]
        license_file.close()
    except IOError:
        _license_key = '0000'
        _expire_date = date.today() + timedelta(days=30)

    # Create and populate the RAMSTK Common test database.
    engine = create_engine(uri, echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    do_make_commondb_tables(engine)

    # Add the product key and expiration date to the site info table.
    _site_info = RAMSTKSiteInfo()
    _site_info.product_key = _license_key
    _site_info.expire_on = _expire_date
    session.add(_site_info)

    for __, _value in list(RAMSTK_CATEGORIES.items()):
        _record = RAMSTKCategory()
        _record.name = _value[0]
        _record.description = _value[1]
        _record.cat_type = _value[2]
        _record.value = _value[3]
        _record.harsh_ir_limit = _value[4]
        _record.mild_ir_limit = _value[5]
        _record.harsh_pr_limit = _value[6]
        _record.mild_pr_limit = _value[7]
        _record.harsh_vr_limit = _value[8]
        _record.mild_vr_limit = _value[9]
        _record.harsh_deltat_limit = _value[10]
        _record.mild_deltat_limit = _value[11]
        _record.harsh_maxt_limit = _value[12]
        _record.mild_maxt_limit = _value[13]
        session.add(_record)

    for __, _value in enumerate(RAMSTK_SUBCATEGORIES):
        _record = RAMSTKSubCategory()
        _record.category_id = _value[0]
        _record.description = _value[2]
        session.add(_record)

    # Default failure modes.
    for _ckey in RAMSTK_FAILURE_MODES:
        _record = RAMSTKFailureMode()
        _record.category_id = _ckey
        for _skey in RAMSTK_FAILURE_MODES[_ckey]:
            _record.subcategory_id = _skey
            for _mkey in RAMSTK_FAILURE_MODES[_ckey][_skey]:
                _record.mode_id = _mkey
                _record.description = RAMSTK_FAILURE_MODES[_ckey][_skey][
                    _mkey][0]
                _record.mode_ratio = RAMSTK_FAILURE_MODES[_ckey][_skey][_mkey][
                    1]
                _record.source = RAMSTK_FAILURE_MODES[_ckey][_skey][_mkey][2]
                session.add(_record)

    # Environmental conditions, operating conditions and load histories for
    # PoF analysis.
    for __, _value in list(RAMSTK_CONDITIONS.items()):
        _record = RAMSTKCondition()
        _record.description = _value[0]
        _record.cond_type = _value[1]
        session.add(_record)
    for __, _value in list(RAMSTK_HISTORIES.items()):
        _record = RAMSTKLoadHistory()
        _record.description = _value[0]
        session.add(_record)

    # Workgroups and affinity groups.
    for __, _value in list(RAMSTK_GROUPS.items()):
        _record = RAMSTKGroup()
        _record.description = _value[0]
        _record.group_type = _value[1]
        session.add(_record)

    # Hazards for hazard analysis.
    for __, _value in list(RAMSTK_HAZARDS.items()):
        _record = RAMSTKHazards()
        _record.category = _value[0]
        _record.subcategory = _value[1]
        session.add(_record)

    # Manufacturers.
    for __, _value in list(RAMSTK_MANUFACTURERS.items()):
        _record = RAMSTKManufacturer()
        _record.description = _value[0]
        _record.location = _value[1]
        _record.cage_code = _value[2]
        session.add(_record)

    # Units of measure, damage measurements.
    for __, _value in list(RAMSTK_MEASUREMENTS.items()):
        _record = RAMSTKMeasurement()
        _record.code = _value[0]
        _record.description = _value[1]
        _record.measurement_type = _value[2]
        session.add(_record)

    # Detection methods for incident reports.
    for __, _value in list(RAMSTK_METHODS.items()):
        _record = RAMSTKMethod()
        _record.name = _value[0]
        _record.description = _value[1]
        _record.method_type = _value[2]
        session.add(_record)

    # Damage models.
    for __, _value in list(RAMSTK_MODELS.items()):
        _record = RAMSTKModel()
        _record.description = _value[0]
        _record.model_type = _value[1]
        session.add(_record)

    # This table needs to be moved to the RAMSTK Program database.
    for __, _value in list(RAMSTK_RPNS.items()):
        _record = RAMSTKRPN()
        _record.name = _value[0]
        _record.description = _value[1]
        _record.rpn_type = _value[2]
        _record.value = _value[3]
        session.add(_record)

    # Stakeholders.
    for __, _value in list(RAMSTK_STAKEHOLDERS.items()):
        _record = RAMSTKStakeholders()
        _record.stakeholder = _value[0]
        session.add(_record)

    # Action and incident statuses.
    for __, _value in list(RAMSTK_STATUSES.items()):
        _record = RAMSTKStatus()
        _record.name = _value[0]
        _record.description = _value[1]
        _record.status_type = _value[2]
        session.add(_record)

    # Incident, requirement, and validation types.
    for __, _value in list(RAMSTK_TYPES.items()):
        _record = RAMSTKType()
        _record.code = _value[0]
        _record.description = _value[1]
        _record.type_type = _value[2]
        session.add(_record)

    _user = RAMSTKUser()
    if not __test:
        _yn = input(
            _("Would you like to add a RAMSTK Administrator? ([y]/n): "),
        ) or 'y'

        if _yn.lower() == 'y':
            _user.user_lname = input(
                _("Enter the RAMSTK Administrator's last name (surname): "), )
            _user.user_fname = input(
                _("Enter the RAMSTK Administrator's first name (given name): "
                  ), )
            _user.user_email = input(
                _("Enter the RAMSTK Administrator's e-mail address: "), )
            _user.user_phone = input(
                _("Enter the RAMSTK Administrator's phone number: "), )
            _user.user_group_id = '1'
    else:
        _user.user_lname = 'Tester'
        _user.user_fname = 'Johnny'
        _user.user_email = 'tester.johnny@reliaqual.com'
        _user.user_phone = '+1.269.867.5309'
        _user.user_group_id = '1'
    session.add(_user)

    session.commit()


def do_create_program_db(**kwargs):
    """Create and initialize a RAMSTK Program database."""
    uri = kwargs['database']

    # Create and populate the RAMSTK Program test database.
    engine = create_engine(uri, echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the RAMSTK Program database.
    do_make_programdb_tables(engine)

    # Add an entry for the Program Information.
    _record = RAMSTKProgramInfo()
    session.add(_record)

    _revision = RAMSTKRevision()
    session.add(_revision)
    session.commit()

    _mission = RAMSTKMission()
    _mission.revision_id = _revision.revision_id
    session.add(_mission)
    session.commit()

    _record = RAMSTKProgramStatus()
    _record.revision_id = _revision.revision_id
    session.add(_record)

    session.commit()


# pylint: disable=too-many-locals
def do_make_programdb_tables(engine):
    """Make all the tables in the RAMSTK Program database."""
    RAMSTKAction.__table__.create(bind=engine)
    RAMSTKAllocation.__table__.create(bind=engine)
    RAMSTKCause.__table__.create(bind=engine)
    RAMSTKControl.__table__.create(bind=engine)
    RAMSTKDesignElectric.__table__.create(bind=engine)
    RAMSTKDesignMechanic.__table__.create(bind=engine)
    RAMSTKEnvironment.__table__.create(bind=engine)
    RAMSTKFailureDefinition.__table__.create(bind=engine)
    RAMSTKFunction.__table__.create(bind=engine)
    RAMSTKHardware.__table__.create(bind=engine)
    RAMSTKHazardAnalysis.__table__.create(bind=engine)
    RAMSTKLoadHistory.__table__.create(bind=engine)
    RAMSTKMatrix.__table__.create(bind=engine)
    RAMSTKMechanism.__table__.create(bind=engine)
    RAMSTKMilHdbkF.__table__.create(bind=engine)
    RAMSTKMission.__table__.create(bind=engine)
    RAMSTKMissionPhase.__table__.create(bind=engine)
    RAMSTKMode.__table__.create(bind=engine)
    RAMSTKNSWC.__table__.create(bind=engine)
    RAMSTKOpLoad.__table__.create(bind=engine)
    RAMSTKOpStress.__table__.create(bind=engine)
    RAMSTKProgramInfo.__table__.create(bind=engine)
    RAMSTKProgramStatus.__table__.create(bind=engine)
    RAMSTKReliability.__table__.create(bind=engine)
    RAMSTKRequirement.__table__.create(bind=engine)
    RAMSTKRevision.__table__.create(bind=engine)
    RAMSTKSimilarItem.__table__.create(bind=engine)
    RAMSTKStakeholder.__table__.create(bind=engine)
    RAMSTKTestMethod.__table__.create(bind=engine)
    RAMSTKValidation.__table__.create(bind=engine)


def do_make_commondb_tables(engine):
    """Make all the tables in the RAMSTK Common database."""
    RAMSTKSiteInfo.__table__.create(bind=engine)
    RAMSTKCategory.__table__.create(bind=engine)
    RAMSTKCondition.__table__.create(bind=engine)
    RAMSTKFailureMode.__table__.create(bind=engine)
    RAMSTKGroup.__table__.create(bind=engine)
    RAMSTKHazards.__table__.create(bind=engine)
    RAMSTKLoadHistory.__table__.create(bind=engine)
    RAMSTKManufacturer.__table__.create(bind=engine)
    RAMSTKMeasurement.__table__.create(bind=engine)
    RAMSTKMethod.__table__.create(bind=engine)
    RAMSTKModel.__table__.create(bind=engine)
    RAMSTKRPN.__table__.create(bind=engine)
    RAMSTKStakeholders.__table__.create(bind=engine)
    RAMSTKStatus.__table__.create(bind=engine)
    RAMSTKSubCategory.__table__.create(bind=engine)
    RAMSTKType.__table__.create(bind=engine)
    RAMSTKUser.__table__.create(bind=engine)


class DAO():
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

    @staticmethod
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def db_connect(self, database):
        """
        Connect to the database using settings from the configuration file.

        :param str database: the absolute path to the database to connect to.
        :return: None
        :rtype: None
        """
        self.database = database
        self.engine = create_engine(self.database, echo=False)
        self.metadata = MetaData(self.engine)

        self.session = self.RAMSTK_SESSION(
            bind=self.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
        )

    def db_close(self):
        """
        Close the current session.

        :return: None
        :rtype: None
        """
        self.session.close()
        self.engine.dispose()
        self.session = None
        self.engine = None
        self.metadata = None
        self.database = None

    def _db_table_create(self, table):
        """
        Check if the passed table exists and create it if not.

        :param table: the table to check for.
        :return: None
        :rtype: None
        """
        if not self.engine.dialect.has_table(
                self.engine.connect(),
                str(table),
        ):
            table.create(bind=self.engine)

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
            return do_create_common_db(database=database, test=_test)
        except (
                IOError,
                exc.SQLAlchemyError,
                exc.DBAPIError,
                exc.OperationalError,
        ) as _error:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            return True
        except ArgumentError:  # pylint: disable=undefined-variable # noqa
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print("Bad common database URI: {0:s}".format(database))
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
        _return = False

        try:
            do_create_program_db(database=database)
        except IOError as _error:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print(_error)
            _return = True
        except exc.OperationalError as _error:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print(_error)
            _return = True
        except exc.DBAPIError as _error:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print(_error)
            _return = True
        except exc.SQLAlchemyError as _error:
            _error = '{0:s}'.format(str(_error))
            print(_error)
            if 'Invalid SQLite URL' in _error:
                _return = True
        except ArgumentError:  # pylint: disable=undefined-variable  # noqa
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print("Bad program database URI: {0:s}".format(database))
            _return = True

        return _return

    def db_add(self, item, session=None):
        """
        Add a new item to the RAMSTK Program database.

        :param item: the object to add to the RAMSTK Program database.
        :return: (_error_code, _msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Adding one or more items to the RAMSTK " \
               "Program database."

        for _item in item:
            try:
                self.session.add(_item)
                self.session.commit()
            except (exc.SQLAlchemyError, exc.DBAPIError) as error:
                _error = '{0:s}'.format(str(error))
                self.session.rollback()
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
                elif 'NOT NULL constraint failed' in _error:
                    _error_code = 5
                    _msg = ('RAMSTK ERROR: One or more fields with a NOT NULL '
                            'constraint were provided with a None value.')
                elif 'database is locked' in _error:
                    _error_code = 6
                    _msg = ('RAMSTK ERROR: The data base is locked and cannot '
                            'be written to.')
                elif 'FOREIGN KEY constraint failed' in _error:
                    _error_code = 7
                    _msg = ('RAMSTK ERROR: A foreign key constraint failed '
                            'when attempting to add an item to the database.')
                else:
                    # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
                    print(_error)
                    _error_code = 1
                    _msg = (
                        'RAMSTK ERROR: Adding one or more items to the RAMSTK '
                        'Program database.')
                raise DataAccessError(_msg)
            except ValueError as _error:
                _error_code = 4
                _msg = ('RAMSTK ERROR: Date field did not contain Python '
                        'date object: {0:s}').format(_error)
                raise DataAccessError(_msg)

        return _error_code, _msg

    def db_update(self, session=None):
        """
        Update the RAMSTK Program database with any pending changes.

        :return: (_error_code, _Msg); the error code and associated error
            message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RAMSTK SUCCESS: Updating the RAMSTK Program database."

        try:
            self.session.commit()
        except (exc.SQLAlchemyError, exc.DBAPIError) as _error:
            print(_error)
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            self.session.rollback()
            _error_code = 1
            _msg = (
                "RAMSTK ERROR: Updating the RAMSTK Program database failed "
                "with error: {0:s}.").format(str(_error))

        return _error_code, _msg

    def db_delete(self, item, session=None):
        """
        Delete a record from the RAMSTK Program database.

        :param item: the item to remove from the RAMSTK Program database.
        :type item: Object()
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = ("RAMSTK SUCCESS: Deleting an item from the RAMSTK Program "
                "database.")

        self.session.execute("PRAGMA foreign_keys=ON")
        try:
            self.session.delete(item)
            self.session.commit()
        except (exc.SQLAlchemyError, exc.DBAPIError) as _error:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            self.session.rollback()
            _error_code = 1
            _msg = ("RAMSTK ERROR: Deleting an item from the RAMSTK Program "
                    "database with error: {0:s}.").format(str(_error))

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

    # TODO: Implement a DAO.db_last_id() method to retrieve the value of the last ID from the database.
    @property
    def db_last_id(self):
        """
        Retrieve the value of the last ID column from a table in the database.

        :return: _last_id; the last value of the ID column.
        :rtype: int
        """
        _last_id = 0

        return _last_id
