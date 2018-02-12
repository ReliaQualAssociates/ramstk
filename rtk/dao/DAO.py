# -*- coding: utf-8 -*-
#
#       rtk.dao.DAO.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
The Data Access Object (DAO) Package.
"""

import gettext

from sqlalchemy import create_engine, exc, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database

# Import other RTK modules.
import rtk.dao.RTKCommonDB

# Import tables objects for the RTK Common database.
from .RTKUser import RTKUser
from .RTKGroup import RTKGroup
from .RTKEnviron import RTKEnviron
from .RTKModel import RTKModel
from .RTKType import RTKType
from .RTKCategory import RTKCategory
from .RTKSubCategory import RTKSubCategory
from .RTKPhase import RTKPhase
from .RTKDistribution import RTKDistribution
from .RTKManufacturer import RTKManufacturer
from .RTKUnit import RTKUnit
from .RTKMethod import RTKMethod
from .RTKCriticality import RTKCriticality
from .RTKRPN import RTKRPN
from .RTKLevel import RTKLevel
from .RTKApplication import RTKApplication
from .RTKHazards import RTKHazards
from .RTKStakeholders import RTKStakeholders
from .RTKStatus import RTKStatus
from .RTKCondition import RTKCondition
from .RTKFailureMode import RTKFailureMode
from .RTKMeasurement import RTKMeasurement
from .RTKLoadHistory import RTKLoadHistory

# Import RTK Program database table objects.
from .RTKAction import RTKAction
from .RTKAllocation import RTKAllocation
from .RTKCause import RTKCause
from .RTKControl import RTKControl
from .RTKDesignElectric import RTKDesignElectric
from .RTKDesignMechanic import RTKDesignMechanic
from .RTKEnvironment import RTKEnvironment
from .RTKFailureDefinition import RTKFailureDefinition
from .RTKFunction import RTKFunction
from .RTKGrowthTest import RTKGrowthTest
from .RTKHardware import RTKHardware
from .RTKHazardAnalysis import RTKHazardAnalysis
from .RTKIncident import RTKIncident
from .RTKIncidentAction import RTKIncidentAction
from .RTKIncidentDetail import RTKIncidentDetail
from .RTKMatrix import RTKMatrix
from .RTKMechanism import RTKMechanism
from .RTKMilHdbkF import RTKMilHdbkF
from .RTKMission import RTKMission
from .RTKMissionPhase import RTKMissionPhase
from .RTKMode import RTKMode
from .RTKNSWC import RTKNSWC
from .RTKOpLoad import RTKOpLoad
from .RTKOpStress import RTKOpStress
from .RTKProgramInfo import RTKProgramInfo
from .RTKReliability import RTKReliability  
from .RTKRequirement import RTKRequirement
from .RTKRevision import RTKRevision
from .RTKSimilarItem import RTKSimilarItem
from .RTKSoftware import RTKSoftware
from .RTKSoftwareDevelopment import RTKSoftwareDevelopment
from .RTKSoftwareReview import RTKSoftwareReview
from .RTKSoftwareTest import RTKSoftwareTest
from .RTKStakeholder import RTKStakeholder
from .RTKSurvival import RTKSurvival
from .RTKSurvivalData import RTKSurvivalData
from .RTKTest import RTKTest
from .RTKTestMethod import RTKTestMethod
from .RTKValidation import RTKValidation

RTK_BASE = declarative_base()

# Add localization support.
_ = gettext.gettext

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class DAO(object):
    """
    This is the data access controller class.
    """

    RTK_SESSION = sessionmaker()

    # Define public class scalar attributes.
    engine = None
    metadata = None
    session = None

    def __init__(self):
        """
        Method to initialize an instance of the DAO controller.
        """

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

    def db_connect(self, database):
        """
        Method to perform database connection using database settings from
        the configuration file.

        :param str database: the absolute path to the database to connect to.
        :return: False if successful, True if an error occurs.
        :rtype: bool
        """

        self.engine = create_engine(database, echo=False)
        self.metadata = MetaData(self.engine)

        self.session = self.RTK_SESSION(
            bind=self.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        return False

    def _db_table_create(self, table):
        """
        Method to check if the passed table exists and create it if not.

        :param table: the table to check for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        if not self.engine.dialect.has_table(self.engine.connect(),
                                             str(table)):
            table.create(bind=self.engine)

        return _return

    def db_create_common(self, database, session):  # pylint: disable=R0914
        """
        Method to create a new RTK Program database.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Common database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        try:
            create_database(database)
        except IOError:
            return True

        self._db_table_create(RTKUser.__table__)
        self._db_table_create(RTKGroup.__table__)
        for _key in RTKCommonDB.RTK_GROUPS:
            _group = RTKGroup()
            _group.group_id = _key
            self.db_add([
                _group,
            ], session)
            session.commit()
            _group.set_attributes(RTKCommonDB.RTK_GROUPS[_key])
            session.commit()

        self._db_table_create(RTKEnviron.__table__)
        for _key in RTKCommonDB.RTK_ENVIRONS:
            _environ = RTKEnviron()
            _environ.environ_id = _key
            self.db_add([
                _environ,
            ], session)
            session.commit()
            _environ.set_attributes(RTKCommonDB.RTK_ENVIRONS[_key])
            session.commit()

        self._db_table_create(RTKModel.__table__)
        for _key in RTKCommonDB.RTK_MODELS:
            _model = RTKModel()
            _model.model_id = _key
            self.db_add([
                _model,
            ], session)
            session.commit()
            _model.set_attributes(RTKCommonDB.RTK_MODELS[_key])
            session.commit()

        self._db_table_create(RTKType.__table__)
        for _key in RTKCommonDB.RTK_TYPES:
            _type = RTKType()
            _type.type_id = _key
            self.db_add([
                _type,
            ], session)
            session.commit()
            _type.set_attributes(RTKCommonDB.RTK_TYPES[_key])
            session.commit()

        self._db_table_create(RTKCategory.__table__)
        for _key in RTKCommonDB.RTK_CATEGORIES:
            _category = RTKCategory()
            _category.category_id = _key
            self.db_add([
                _category,
            ], session)
            session.commit()
            _category.set_attributes(RTKCommonDB.RTK_CATEGORIES[_key])
            session.commit()

        self._db_table_create(RTKSubCategory.__table__)
        self._db_table_create(RTKFailureMode.__table__)

        self._db_table_create(RTKPhase.__table__)
        for _key in RTKCommonDB.RTK_PHASES:
            _phase = RTKPhase()
            _phase.phase_id = _key
            self.db_add([
                _phase,
            ], session)
            session.commit()
            _phase.set_attributes(RTKCommonDB.RTK_PHASES[_key])
            session.commit()

        self._db_table_create(RTKDistribution.__table__)
        for _key in RTKCommonDB.RTK_DISTRIBUTIONS:
            _distribution = RTKDistribution()
            _distribution.distribution_id = _key
            self.db_add([
                _distribution,
            ], session)
            session.commit()
            _distribution.set_attributes(RTKCommonDB.RTK_DISTRIBUTIONS[_key])
            session.commit()

        self._db_table_create(RTKManufacturer.__table__)
        for _key in RTKCommonDB.RTK_MANUFACTURERS:
            _manufacturer = RTKManufacturer()
            _manufacturer.manufacturer_id = _key
            self.db_add([
                _manufacturer,
            ], session)
            session.commit()
            _manufacturer.set_attributes(RTKCommonDB.RTK_MANUFACTURERS[_key])
            session.commit()

        self._db_table_create(RTKUnit.__table__)
        for _key in RTKCommonDB.RTK_UNITS:
            _unit = RTKUnit()
            _unit.unit_id = _key
            self.db_add([
                _unit,
            ], session)
            session.commit()
            _unit.set_attributes(RTKCommonDB.RTK_UNITS[_key])
            session.commit()

        self._db_table_create(RTKMethod.__table__)
        for _key in RTKCommonDB.RTK_METHODS:
            _method = RTKMethod()
            _method.method_id = _key
            self.db_add([
                _method,
            ], session)
            session.commit()
            _method.set_attributes(RTKCommonDB.RTK_METHODS[_key])
            session.commit()

        self._db_table_create(RTKCriticality.__table__)
        for _key in RTKCommonDB.RTK_CRITICALITIES:
            _criticality = RTKCriticality()
            _criticality.criticality_id = _key
            self.db_add([
                _criticality,
            ], session)
            session.commit()
            _criticality.set_attributes(RTKCommonDB.RTK_CRITICALITIES[_key])
            session.commit()

        self._db_table_create(RTKRPN.__table__)
        for _key in RTKCommonDB.RTK_RPNS:
            _rpn = RTKRPN()
            _rpn.rpn_id = _key
            self.db_add([
                _rpn,
            ], session)
            session.commit()
            _rpn.set_attributes(RTKCommonDB.RTK_RPNS[_key])
            session.commit()

        self._db_table_create(RTKLevel.__table__)
        for _key in RTKCommonDB.RTK_LEVELS:
            _level = RTKLevel()
            _level.level_id = _key
            self.db_add([
                _level,
            ], session)
            session.commit()
            _level.set_attributes(RTKCommonDB.RTK_LEVELS[_key])
            session.commit()

        self._db_table_create(RTKApplication.__table__)
        for _key in RTKCommonDB.RTK_APPLICATIONS:
            _application = RTKApplication()
            _application.application_id = _key
            self.db_add([
                _application,
            ], session)
            session.commit()
            _application.set_attributes(RTKCommonDB.RTK_APPLICATIONS[_key])
            session.commit()

        self._db_table_create(RTKHazards.__table__)
        for _key in RTKCommonDB.RTK_HAZARDS:
            _hazard = RTKHazards()
            _hazard.hazard_id = _key
            self.db_add([
                _hazard,
            ], session)
            session.commit()
            _hazard.set_attributes(RTKCommonDB.RTK_HAZARDS[_key])
            session.commit()

        self._db_table_create(RTKStakeholders.__table__)
        for _key in RTKCommonDB.RTK_STAKEHOLDERS:
            _stakeholder = RTKStakeholders()
            _stakeholder.stakeholders_id = _key
            self.db_add([
                _stakeholder,
            ], session)
            session.commit()
            _stakeholder.set_attributes(RTKCommonDB.RTK_STAKEHOLDERS[_key])
            session.commit()

        self._db_table_create(RTKStatus.__table__)
        for _key in RTKCommonDB.RTK_STATUSES:
            _status = RTKStatus()
            _status.status_id = _key
            self.db_add([
                _status,
            ], session)
            session.commit()
            _status.set_attributes(RTKCommonDB.RTK_STATUSES[_key])
            session.commit()

        self._db_table_create(RTKCondition.__table__)
        for _key in RTKCommonDB.RTK_CONDITIONS:
            _condition = RTKCondition()
            _condition.condition_id = _key
            self.db_add([
                _condition,
            ], session)
            session.commit()
            _condition.set_attributes(RTKCommonDB.RTK_CONDITIONS[_key])
            session.commit()

        self._db_table_create(RTKMeasurement.__table__)
        for _key in RTKCommonDB.RTK_MEASUREMENTS:
            _measurement = RTKMeasurement()
            _measurement.measurement_id = _key
            self.db_add([
                _measurement,
            ], session)
            session.commit()
            _measurement.set_attributes(RTKCommonDB.RTK_MEASUREMENTS[_key])
            session.commit()

        self._db_table_create(RTKLoadHistory.__table__)
        for _key in RTKCommonDB.RTK_HISTORIES:
            _history = RTKLoadHistory()
            _history.history_id = _key
            self.db_add([
                _history,
            ], session)
            session.commit()
            _history.set_attributes(RTKCommonDB.RTK_HISTORIES[_key])
            session.commit()

        return False

    def db_create_program(self, database, session):
        """
        Method to create a new RTK Program database.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        try:
            create_database(database)
        except IOError:
            return True

        self._db_table_create(RTKProgramInfo.__table__)

        self._db_table_create(RTKRevision.__table__)
        _revision = RTKRevision()
        _revision.revision_id = 1
        _revision.description = _(u"Initial Revision")
        self.db_add([
            _revision,
        ], session)
        session.commit()

        self._db_table_create(RTKMission.__table__)
        _mission = RTKMission()
        _mission.revision_id = _revision.revision_id
        _mission.mission_id = 1
        _mission.description = _(u"Default Mission")
        self.db_add([
            _mission,
        ], session)
        session.commit()

        self._db_table_create(RTKMissionPhase.__table__)
        _phase = RTKMissionPhase()
        _phase.mission_id = _mission.mission_id
        _phase.phase_id = 1
        _phase.description = _(u"Default Mission Phase 1")
        self.db_add([
            _phase,
        ], session)
        session.commit()

        self._db_table_create(RTKEnvironment.__table__)
        self._db_table_create(RTKFailureDefinition.__table__)
        self._db_table_create(RTKFunction.__table__)
        self._db_table_create(RTKRequirement.__table__)
        self._db_table_create(RTKStakeholder.__table__)
        self._db_table_create(RTKMatrix.__table__)

        self._db_table_create(RTKHardware.__table__)
        _hardware = RTKHardware()
        _hardware.revision_id = _revision.revision_id
        _hardware.hardware_id = 1
        _hardware.description = _(u"System")
        self.db_add([
            _hardware,
        ], session)
        session.commit()

        self._db_table_create(RTKAllocation.__table__)
        _allocation = RTKAllocation()
        _allocation.hardware_id = _hardware.hardware_id

        self._db_table_create(RTKHazardAnalysis.__table__)
        _hazard = RTKHazardAnalysis()
        _hazard.hardware_id = _hardware.hardware_id

        self._db_table_create(RTKSimilarItem.__table__)
        _similar_item = RTKSimilarItem()
        _similar_item.hardware_id = _hardware.hardware_id

        self._db_table_create(RTKReliability.__table__)
        _reliability = RTKReliability()
        _reliability.hardware_id = _hardware.hardware_id
        self.db_add([_allocation, _hazard, _similar_item, _reliability],
                    session)
        session.commit()

        self._db_table_create(RTKMilHdbkF.__table__)
        self._db_table_create(RTKNSWC.__table__)
        self._db_table_create(RTKDesignElectric.__table__)
        self._db_table_create(RTKDesignMechanic.__table__)
        self._db_table_create(RTKMode.__table__)
        self._db_table_create(RTKMechanism.__table__)
        self._db_table_create(RTKCause.__table__)
        self._db_table_create(RTKControl.__table__)
        self._db_table_create(RTKAction.__table__)
        self._db_table_create(RTKOpLoad.__table__)
        self._db_table_create(RTKOpStress.__table__)
        self._db_table_create(RTKTestMethod.__table__)

        self._db_table_create(RTKSoftware.__table__)
        _software = RTKSoftware()
        _software.revision_id = _revision.revision_id
        _software.software_id = 1
        _software.description = _(u"System Software")
        self.db_add([
            _software,
        ], session)
        session.commit()

        self._db_table_create(RTKSoftwareDevelopment.__table__)
        for i in range(43):
            _sw_development = RTKSoftwareDevelopment()
            _sw_development.software_id = _software.software_id
            _sw_development.question_id = i
            self.db_add([
                _sw_development,
            ], session)
        session.commit()

        self._db_table_create(RTKSoftwareReview.__table__)
        for i in range(50):
            _sw_review = RTKSoftwareReview()
            _sw_review.software_id = _software.software_id
            _sw_review.question_id = i
            _sw_review.type = 'SRR'
            self.db_add([
                _sw_review,
            ], session)
        for i in range(38):
            _sw_review = RTKSoftwareReview()
            _sw_review.software_id = _software.software_id
            _sw_review.question_id = i
            _sw_review.type = 'PDR'
            self.db_add([
                _sw_review,
            ], session)
        for i in range(35):
            _sw_review = RTKSoftwareReview()
            _sw_review.software_id = _software.software_id
            _sw_review.question_id = i
            _sw_review.type = 'CDR'
            self.db_add([
                _sw_review,
            ], session)
        for i in range(24):
            _sw_review = RTKSoftwareReview()
            _sw_review.software_id = _software.software_id
            _sw_review.question_id = i
            _sw_review.type = 'TRR'
            self.db_add([
                _sw_review,
            ], session)
        session.commit()

        self._db_table_create(RTKSoftwareTest.__table__)
        for i in range(21):
            _sw_test = RTKSoftwareTest()
            _sw_test.software_id = _software.software_id
            _sw_test.technique_id = i
            self.db_add([
                _sw_test,
            ], session)
        session.commit()

        self._db_table_create(RTKValidation.__table__)
        self._db_table_create(RTKIncident.__table__)
        self._db_table_create(RTKIncidentDetail.__table__)
        self._db_table_create(RTKIncidentAction.__table__)
        self._db_table_create(RTKTest.__table__)
        self._db_table_create(RTKGrowthTest.__table__)
        self._db_table_create(RTKSurvival.__table__)
        self._db_table_create(RTKSurvivalData.__table__)

        return False

    @staticmethod
    def db_add(item, session):
        """
        Method to add a new item to the RTK Program database.

        :param item: the object to add to the RTK Program database.
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Adding one or more items to the RTK Program " \
               "database."
        # TODO: Determine if the add_many option can work with Foreign Keys.
        for _item in item:
            try:
                session.add(_item)
                session.commit()
            except (exc.SQLAlchemyError, exc.DBAPIError) as error:
                print error
                session.rollback()
                _error_code = 1003
                _msg = "RTK ERROR: Adding one or more items to the RTK " \
                       "Program database."

        return _error_code, _msg

    @staticmethod
    def db_update(session):
        """
        Method to update the RTK Program database with any pending changes.

        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Updating the RTK Program database."

        try:
            session.commit()
        except (exc.SQLAlchemyError, exc.DBAPIError) as error:
            print error
            session.rollback()
            _error_code = 1004
            _msg = "RTK ERROR: Updating the RTK Program database."

        return _error_code, _msg

    @staticmethod
    def db_delete(item, session):
        """
        Method to delete a record from the RTK Program database.

        :param item: the item to remove from the RTK Program database.
        :type item: Object()
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """

        _error_code = 0
        _msg = "RTK SUCCESS: Deleting an item from the RTK Program database."

        try:
            session.delete(item)
            session.commit()
        except(exc.SQLAlchemyError, exc.DBAPIError) as error:
            print error
            session.rollback()
            _error_code = 1005
            _msg = "RTK ERROR: Deleting an item from the RTK Program database."

        return _error_code, _msg

    @staticmethod
    def db_query(query, session):
        """
        Method to exceute an SQL query against the connected database.

        :param str query: the SQL query string to execute
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return:
        :rtype: str
        """

        return session.execute(query)

    @property
    def db_last_id(self):
        """
        Method to retrieve the value of the last ID column from a table in the
        RTK Program database.

        :return: _last_id; the last value of the ID column.
        :rtype: int
        """
        # TODO: Write the db_last_id method if needed, else remove from file.
        _last_id = 0

        return _last_id
