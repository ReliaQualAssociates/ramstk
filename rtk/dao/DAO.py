#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.DAO.py is part of The RTK Project
#
# All rights reserved.

"""
The Data Access Object (DAO) Package.
"""

from datetime import date, timedelta

# Import the database models.
from SQLite3 import Model as SQLite3

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.engine.url import URL

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities

try:
    import RTKCommonDB
except ImportError:
    import dao.RTKCommonDB

# Import tables objects for the RTK Common database.
try:
    from dao.RTKUser import RTKUser
except ImportError:
    print "RTK ERROR: No module named dao.RTKUser"
try:
    from dao.RTKGroup import RTKGroup
except ImportError:
    print "RTK ERROR: No module named dao.RTKGroup"
try:
    from dao.RTKEnviron import RTKEnviron
except ImportError:
    print "RTK ERROR: No module named dao.RTKEnviron"
try:
    from dao.RTKModel import RTKModel
except ImportError:
    print "RTK ERROR: No module named dao.RTKModel"
try:
    from dao.RTKType import RTKType
except ImportError:
    print "RTK ERROR: No module named dao.RTKType"
try:
    from dao.RTKCategory import RTKCategory
except ImportError:
    print "RTK ERROR: No module named dao.RTKCategory"
try:
    from dao.RTKSubCategory import RTKSubCategory
except ImportError:
    print "RTK ERROR: No module named dao.RTKSubCategory"
try:
    from dao.RTKPhase import RTKPhase
except ImportError:
    print "RTK ERROR: No module named dao.RTKPhase"
try:
    from dao.RTKDistribution import RTKDistribution
except ImportError:
    print "RTK ERROR: No module named dao.RTKDistribution"
try:
    from dao.RTKManufacturer import RTKManufacturer
except ImportError:
    print "RTK ERROR: No module named dao.RTKManufacturer"
try:
    from dao.RTKUnit import RTKUnit
except ImportError:
    print "RTK ERROR: No module named dao.RTKUnit"
try:
    from dao.RTKMethod import RTKMethod
except ImportError:
    print "RTK ERROR: No module named dao.RTKMethod"
try:
    from dao.RTKCriticality import RTKCriticality
except ImportError:
    print "RTK ERROR: No module named dao.RTKCriticality"
try:
    from dao.RTKRPN import RTKRPN
except ImportError:
    print "RTK ERROR: No module named dao.RTKRPN"
try:
    from dao.RTKLevel import RTKLevel
except ImportError:
    print "RTK ERROR: No module named dao.RTKLevel"
try:
    from dao.RTKApplication import RTKApplication
except ImportError:
    print "RTK ERROR: No module named dao.RTKApplication"
try:
    from dao.RTKHazards import RTKHazards
except ImportError:
    print "RTK ERROR: No module named dao.RTKHazards"
try:
    from dao.RTKStakeholders import RTKStakeholders
except ImportError:
    print "RTK ERROR: No module named dao.RTKStakeholders"
try:
    from dao.RTKStatus import RTKStatus
except ImportError:
    print "RTK ERROR: No module named dao.RTKStatus"
try:
    from dao.RTKCondition import RTKCondition
except ImportError:
    print "RTK ERROR: No module named dao.RTKCondition"
try:
    from dao.RTKFailureMode import RTKFailureMode
except ImportError:
    print "RTK ERROR: No module named dao.RTKFailureMode"
try:
    from dao.RTKMeasurement import RTKMeasurement
except ImportError:
    print "RTK ERROR: No module named dao.RTKMeasurement"
try:
    from dao.RTKLoadHistory import RTKLoadHistory
except ImportError:
    print "RTK ERROR: No module named dao.RTKLoadHistory"

# Import RTK Program database table objects.
from dao.RTKAction import RTKAction
from dao.RTKAllocation import RTKAllocation
from dao.RTKCause import RTKCause
from dao.RTKControl import RTKControl
from dao.RTKDesignElectric import RTKDesignElectric
from dao.RTKDesignMechanic import RTKDesignMechanic
from dao.RTKEnvironment import RTKEnvironment
from dao.RTKFailureDefinition import RTKFailureDefinition
from dao.RTKFunction import RTKFunction
from dao.RTKGrowthTest import RTKGrowthTest
from dao.RTKHardware import RTKHardware
from dao.RTKHazardAnalysis import RTKHazardAnalysis
from dao.RTKIncident import RTKIncident
from dao.RTKIncidentAction import RTKIncidentAction
from dao.RTKIncidentDetail import RTKIncidentDetail
from dao.RTKMatrix import RTKMatrix
from dao.RTKMechanism import RTKMechanism
from dao.RTKMilHdbkF import RTKMilHdbkF
from dao.RTKMission import RTKMission
from dao.RTKMissionPhase import RTKMissionPhase
from dao.RTKMode import RTKMode
from dao.RTKNSWC import RTKNSWC
from dao.RTKOpLoad import RTKOpLoad
from dao.RTKOpStress import RTKOpStress
from dao.RTKReliability import RTKReliability
from dao.RTKRequirement import RTKRequirement
from dao.RTKRevision import RTKRevision
from dao.RTKSimilarItem import RTKSimilarItem
from dao.RTKSoftware import RTKSoftware
from dao.RTKSoftwareDevelopment import RTKSoftwareDevelopment
from dao.RTKSoftwareReview import RTKSoftwareReview
from dao.RTKSoftwareTest import RTKSoftwareTest
from dao.RTKStakeholder import RTKStakeholder
from dao.RTKSurvival import RTKSurvival
from dao.RTKSurvivalData import RTKSurvivalData
from dao.RTKTest import RTKTest
from dao.RTKTestMethod import RTKTestMethod
from dao.RTKValidation import RTKValidation

Base = declarative_base()

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class DAO(object):
    """
    This is the data access controller class.

    :ivar model: an instance of the database class selected for data access.
    """

    # Define public class scalar attributes.
    engine = None
    metadata = None
    session = scoped_session(sessionmaker())

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
        :param bool commit: indicates whether or not to commit query.
        :return: (_results, _error_code); the results of the query and the
                                          error code produced.
        :rtype: tuple
        """

        (_results, _error_code, _last_id) = self.model.execute(query, commit)

        return _results, _error_code, _last_id

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

    def db_connect(self, database):
        """
        Method to perform database connection using database settings from
        the configuration file.

        :param str database: the absolute path to the database to connect to.
        :return: False if successful, True if an error occurs.
        :rtype: bool
        """

        self.engine = create_engine(database, echo=False)

        self.session.remove()
        self.session.configure(bind=self.engine, autoflush=False,
                               expire_on_commit=False)
        self.metadata = MetaData(self.engine)

        #if not database_exists(database):
        #    self.db_create_common(database)

        return False

    def db_create_common(self, database):
        """
        Method to create a new RTK Program database.

        :param str database: the absolute path to the database to create.
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        create_database(database)

        RTKUser.__table__.create(bind=self.engine)
        RTKGroup.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.groups.keys():
            _group = RTKGroup()
            self.db_add(_group)
            self.session.commit()
            _group.set_attributes(RTKCommonDB.groups[_key])
            self.session.commit()

        RTKEnviron.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.environs.keys():
            _environ = RTKEnviron()
            self.db_add(_environ)
            self.session.commit()
            _environ.set_attributes(RTKCommonDB.environs[_key])
            self.session.commit()

        RTKModel.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.models.keys():
            _model = RTKModel()
            self.db_add(_model)
            self.session.commit()
            _model.set_attributes(RTKCommonDB.models[_key])
            self.session.commit()

        RTKType.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.types.keys():
            _type = RTKType()
            self.db_add(_type)
            self.session.commit()
            _type.set_attributes(RTKCommonDB.types[_key])
            self.session.commit()

        RTKCategory.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.categories.keys():
            _category = RTKCategory()
            self.db_add(_category)
            self.session.commit()
            _category.set_attributes(RTKCommonDB.categories[_key])
            self.session.commit()

        RTKSubCategory.__table__.create(bind=self.engine)
        RTKFailureMode.__table__.create(bind=self.engine)

        RTKPhase.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.phases.keys():
            _phase = RTKPhase()
            self.db_add(_phase)
            self.session.commit()
            _phase.set_attributes(RTKCommonDB.phases[_key])
            self.session.commit()

        RTKDistribution.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.distributions.keys():
            _distribution = RTKDistribution()
            self.db_add(_distribution)
            self.session.commit()
            _distribution.set_attributes(RTKCommonDB.distributions[_key])
            self.session.commit()

        RTKManufacturer.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.manufacturers.keys():
            _manufacturer = RTKManufacturer()
            self.db_add(_manufacturer)
            self.session.commit()
            _manufacturer.set_attributes(RTKCommonDB.manufacturers[_key])
            self.session.commit()

        RTKUnit.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.units.keys():
            _unit = RTKUnit()
            self.db_add(_unit)
            self.session.commit()
            _unit.set_attributes(RTKCommonDB.units[_key])
            self.session.commit()

        RTKMethod.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.methods.keys():
            _method = RTKMethod()
            self.db_add(_method)
            self.session.commit()
            _method.set_attributes(RTKCommonDB.methods[_key])
            self.session.commit()

        RTKCriticality.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.criticalitys.keys():
            _criticality = RTKCriticality()
            self.db_add(_criticality)
            self.session.commit()
            _criticality.set_attributes(RTKCommonDB.criticalitys[_key])
            self.session.commit()

        RTKRPN.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.rpns.keys():
            _rpn = RTKRPN()
            self.db_add(_rpn)
            self.session.commit()
            _rpn.set_attributes(RTKCommonDB.rpns[_key])
            self.session.commit()

        RTKLevel.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.levels.keys():
            _level = RTKLevel()
            self.db_add(_level)
            self.session.commit()
            _level.set_attributes(RTKCommonDB.levels[_key])
            self.session.commit()

        RTKApplication.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.applications.keys():
            _application = RTKApplication()
            self.db_add(_application)
            self.session.commit()
            _application.set_attributes(RTKCommonDB.applications[_key])
            self.session.commit()

        RTKHazards.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.hazards.keys():
            _hazard = RTKHazards()
            self.db_add(_hazard)
            self.session.commit()
            _hazard.set_attributes(RTKCommonDB.hazards[_key])
            self.session.commit()

        RTKStakeholders.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.stakeholders.keys():
            _stakeholder = RTKStakeholders()
            self.db_add(_stakeholder)
            self.session.commit()
            _stakeholder.set_attributes(RTKCommonDB.stakeholders[_key])
            self.session.commit()

        RTKStatus.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.statuses.keys():
            _status = RTKStatus()
            self.db_add(_status)
            self.session.commit()
            _status.set_attributes(RTKCommonDB.statuses[_key])
            self.session.commit()

        RTKCondition.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.conditions.keys():
            _condition = RTKCondition()
            self.db_add(_condition)
            self.session.commit()
            _condition.set_attributes(RTKCommonDB.conditions[_key])
            self.session.commit()

        RTKMeasurement.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.measurements.keys():
            _measurement = RTKMeasurement()
            self.db_add(_measurement)
            self.session.commit()
            _measurement.set_attributes(RTKCommonDB.measurements[_key])
            self.session.commit()

        RTKLoadHistory.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.historys.keys():
            _history = RTKLoadHistory()
            self.db_add(_history)
            self.session.commit()
            _history.set_attributes(RTKCommonDB.historys[_key])
            self.session.commit()

        return False

    def db_create(self, database):
        """
        Method to create a new RTK Program database.

        :param str database: the absolute path to the database to create.
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        create_database(database)

        RTKRevision.__table__.create(bind=self.engine)
        RTKMission.__table__.create(bind=self.engine)
        RTKMissionPhase.__table__.create(bind=self.engine)
        RTKEnvironment.__table__.create(bind=self.engine)
        RTKFailureDefinition.__table__.create(bind=self.engine)
        RTKFunction.__table__.create(bind=self.engine)
        RTKRequirement.__table__.create(bind=self.engine)
        RTKStakeholder.__table__.create(bind=self.engine)
        RTKMatrix.__table__.create(bind=self.engine)
        RTKHardware.__table__.create(bind=self.engine)
        RTKAllocation.__table__.create(bind=self.engine)
        RTKHazardAnalysis.__table__.create(bind=self.engine)
        RTKSimilarItem.__table__.create(bind=self.engine)
        RTKReliability.__table__.create(bind=self.engine)
        RTKMilHdbkF.__table__.create(bind=self.engine)
        RTKNSWC.__table__.create(bind=self.engine)
        RTKDesignElectric.__table__.create(bind=self.engine)
        RTKDesignMechanic.__table__.create(bind=self.engine)
        RTKMode.__table__.create(bind=self.engine)
        RTKMechanism.__table__.create(bind=self.engine)
        RTKCause.__table__.create(bind=self.engine)
        RTKControl.__table__.create(bind=self.engine)
        RTKAction.__table__.create(bind=self.engine)
        RTKOpLoad.__table__.create(bind=self.engine)
        RTKOpStress.__table__.create(bind=self.engine)
        RTKTestMethod.__table__.create(bind=self.engine)
        RTKSoftware.__table__.create(bind=self.engine)
        RTKSoftwareDevelopment.__table__.create(bind=self.engine)
        RTKSoftwareReview.__table__.create(bind=self.engine)
        RTKSoftwareTest.__table__.create(bind=self.engine)
        RTKValidation.__table__.create(bind=self.engine)
        RTKIncident.__table__.create(bind=self.engine)
        RTKIncidentDetail.__table__.create(bind=self.engine)
        RTKIncidentAction.__table__.create(bind=self.engine)
        RTKTest.__table__.create(bind=self.engine)
        RTKGrowthTest.__table__.create(bind=self.engine)
        RTKSurvival.__table__.create(bind=self.engine)
        RTKSurvivalData.__table__.create(bind=self.engine)

        return False

    def db_add(self, item):
        """
        Method to add a new item to the RTK Program database.

        :param item: the object to add to the RTK Program database.
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "SUCCESS: Adding an item to the RTK Program database."

        try:
            if isinstance(item, list):
                self.session.add_all(item)
            else:
                self.session.add(item)
            self.session.commit()
        except:
            self.session.rollback()
            _error_code = 1003
            _msg = "ERROR: Adding an item to the RTK Program database."

        return _error_code, _msg

    def db_update(self):
        """
        Method to update the RTK Program database with any pending changes.

        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "SUCCESS: Updating the RTK Program database."

        try:
            self.session.commit()
        except:
            self.session.rollback()
            _error_code = 1004
            _msg = "ERROR: Updating the RTK Program database."

        return _error_code, _msg

    def db_delete(self, item):
        """
        Method to delete a record from the RTK Program database.

        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "SUCCESS: Deleting an item from the RTK Program database."

        try:
            self.session.delete(item)
            self.session.commit()
        except:
            self.session.rollback()
            _error_code = 1005
            _msg = "ERROR: Deleting an item from the RTK Program database."

        return _error_code, _msg

    def db_query(self, query):
        """
        Method to exceute an SQL query against the connected database.

        :param str query: the SQL query to execute
        :return:
        :rtype: str
        """

        return self.session.execute(query)

    def db_last_id(self):
        """
        Method to retrieve the value of the last ID column from a table in the
        RTK Program database.

        :return: _last_id; the last value of the ID column.
        :rtype: int
        """

        _last_id = 0

        return _last_id
