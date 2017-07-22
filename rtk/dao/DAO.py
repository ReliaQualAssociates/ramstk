#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.dao.DAO.py is part of The RTK Project
#
# All rights reserved.

"""
The Data Access Object (DAO) Package.
"""

import gettext

from treelib import Tree

# Import the database models.
from SQLite3 import Model as SQLite3

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_database

# Import other RTK modules.
try:
    import Configuration as Configuration
except ImportError:
    import rtk.Configuration as Configuration
try:
    import Utilities as Utilities
except ImportError:
    import rtk.Utilities as Utilities

import RTKCommonDB

# Import tables objects for the RTK Common database.
from RTKUser import RTKUser
from RTKGroup import RTKGroup
from RTKEnviron import RTKEnviron
from RTKModel import RTKModel
from RTKType import RTKType
from RTKCategory import RTKCategory
from RTKSubCategory import RTKSubCategory
from RTKPhase import RTKPhase
from RTKDistribution import RTKDistribution
from RTKManufacturer import RTKManufacturer
from RTKUnit import RTKUnit
from RTKMethod import RTKMethod
from RTKCriticality import RTKCriticality
from RTKRPN import RTKRPN
from RTKLevel import RTKLevel
from RTKApplication import RTKApplication
from RTKHazards import RTKHazards
from RTKStakeholders import RTKStakeholders
from RTKStatus import RTKStatus
from RTKCondition import RTKCondition
from RTKFailureMode import RTKFailureMode
from RTKMeasurement import RTKMeasurement
from RTKLoadHistory import RTKLoadHistory

# Import RTK Program database table objects.
from RTKAction import RTKAction
from RTKAllocation import RTKAllocation
from RTKCause import RTKCause
from RTKControl import RTKControl
from RTKDesignElectric import RTKDesignElectric
from RTKDesignMechanic import RTKDesignMechanic
from RTKEnvironment import RTKEnvironment
from RTKFailureDefinition import RTKFailureDefinition
from RTKFunction import RTKFunction
from RTKGrowthTest import RTKGrowthTest
from RTKHardware import RTKHardware
from RTKHazardAnalysis import RTKHazardAnalysis
from RTKIncident import RTKIncident
from RTKIncidentAction import RTKIncidentAction
from RTKIncidentDetail import RTKIncidentDetail
from RTKMatrix import RTKMatrix
from RTKMechanism import RTKMechanism
from RTKMilHdbkF import RTKMilHdbkF
from RTKMission import RTKMission
from RTKMissionPhase import RTKMissionPhase
from RTKMode import RTKMode
from RTKNSWC import RTKNSWC
from RTKOpLoad import RTKOpLoad
from RTKOpStress import RTKOpStress
from RTKReliability import RTKReliability
from RTKRequirement import RTKRequirement
from RTKRevision import RTKRevision
from RTKSimilarItem import RTKSimilarItem
from RTKSoftware import RTKSoftware
from RTKSoftwareDevelopment import RTKSoftwareDevelopment
from RTKSoftwareReview import RTKSoftwareReview
from RTKSoftwareTest import RTKSoftwareTest
from RTKStakeholder import RTKStakeholder
from RTKSurvival import RTKSurvival
from RTKSurvivalData import RTKSurvivalData
from RTKTest import RTKTest
from RTKTestMethod import RTKTestMethod
from RTKValidation import RTKValidation

Base = declarative_base()

# Add localization support.
_ = gettext.gettext

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
    session = None

    def __init__(self, database, db_type=0):
        """
        Method to initialize an instance of the DAO controller.

        :param str database: the full path of the database to connect to.
        :keyword int db_type: the type of database to connect to.  Options are:
                              * SQLite3 = 0 (default)
                              * MySQL/MariaDB = 1
        """

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.tree = Tree()          # TODO: Consider moving this to the Component class.

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
        self.metadata = MetaData(self.engine)

        return False

    def db_create_common(self, database, session):
        """
        Method to create a new RTK Program database.

        :param str database: the absolute path to the database to create.
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Common database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        create_database(database)

        RTKUser.__table__.create(bind=self.engine)
        RTKGroup.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.groups.keys():
            _group = RTKGroup()
            _group.group_id = _key
            self.db_add([_group, ], session)
            session.commit()
            _group.set_attributes(RTKCommonDB.groups[_key])
            session.commit()

        RTKEnviron.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.environs.keys():
            _environ = RTKEnviron()
            _environ.environ_id = _key
            self.db_add([_environ, ], session)
            session.commit()
            _environ.set_attributes(RTKCommonDB.environs[_key])
            session.commit()

        RTKModel.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.models.keys():
            _model = RTKModel()
            _model.model_id = _key
            self.db_add([_model, ], session)
            session.commit()
            _model.set_attributes(RTKCommonDB.models[_key])
            session.commit()

        RTKType.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.types.keys():
            _type = RTKType()
            _type.type_id = _key
            self.db_add([_type, ], session)
            session.commit()
            _type.set_attributes(RTKCommonDB.types[_key])
            session.commit()

        RTKCategory.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.categories.keys():
            _category = RTKCategory()
            _category.category_id = _key
            self.db_add([_category, ], session)
            session.commit()
            _category.set_attributes(RTKCommonDB.categories[_key])
            session.commit()

        RTKSubCategory.__table__.create(bind=self.engine)
        RTKFailureMode.__table__.create(bind=self.engine)

        RTKPhase.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.phases.keys():
            _phase = RTKPhase()
            _phase.phase_id = _key
            self.db_add([_phase, ], session)
            session.commit()
            _phase.set_attributes(RTKCommonDB.phases[_key])
            session.commit()

        RTKDistribution.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.distributions.keys():
            _distribution = RTKDistribution()
            _distribution.distribution_id = _key
            self.db_add([_distribution, ], session)
            session.commit()
            _distribution.set_attributes(RTKCommonDB.distributions[_key])
            session.commit()

        RTKManufacturer.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.manufacturers.keys():
            _manufacturer = RTKManufacturer()
            _manufacturer.manufacturer_id = _key
            self.db_add([_manufacturer, ], session)
            session.commit()
            _manufacturer.set_attributes(RTKCommonDB.manufacturers[_key])
            session.commit()

        RTKUnit.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.units.keys():
            _unit = RTKUnit()
            _unit.unit_id = _key
            self.db_add([_unit, ], session)
            session.commit()
            _unit.set_attributes(RTKCommonDB.units[_key])
            session.commit()

        RTKMethod.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.methods.keys():
            _method = RTKMethod()
            _method.method_id = _key
            self.db_add([_method, ], session)
            session.commit()
            _method.set_attributes(RTKCommonDB.methods[_key])
            session.commit()

        RTKCriticality.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.criticalitys.keys():
            _criticality = RTKCriticality()
            _criticality.criticality_id = _key
            self.db_add([_criticality, ], session)
            session.commit()
            _criticality.set_attributes(RTKCommonDB.criticalitys[_key])
            session.commit()

        RTKRPN.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.rpns.keys():
            _rpn = RTKRPN()
            _rpn.rpn_id = _key
            self.db_add([_rpn, ], session)
            session.commit()
            _rpn.set_attributes(RTKCommonDB.rpns[_key])
            session.commit()

        RTKLevel.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.levels.keys():
            _level = RTKLevel()
            _level.level_id = _key
            self.db_add([_level, ], session)
            session.commit()
            _level.set_attributes(RTKCommonDB.levels[_key])
            session.commit()

        RTKApplication.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.applications.keys():
            _application = RTKApplication()
            _application.application_id = _key
            self.db_add([_application, ], session)
            session.commit()
            _application.set_attributes(RTKCommonDB.applications[_key])
            session.commit()

        RTKHazards.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.hazards.keys():
            _hazard = RTKHazards()
            _hazard.hazard_id = _key
            self.db_add([_hazard, ], session)
            session.commit()
            _hazard.set_attributes(RTKCommonDB.hazards[_key])
            session.commit()

        RTKStakeholders.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.stakeholders.keys():
            _stakeholder = RTKStakeholders()
            _stakeholder.stakeholders_id = _key
            self.db_add([_stakeholder, ], session)
            session.commit()
            _stakeholder.set_attributes(RTKCommonDB.stakeholders[_key])
            session.commit()

        RTKStatus.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.statuses.keys():
            _status = RTKStatus()
            _status.status_id = _key
            self.db_add([_status, ], session)
            session.commit()
            _status.set_attributes(RTKCommonDB.statuses[_key])
            session.commit()

        RTKCondition.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.conditions.keys():
            _condition = RTKCondition()
            _condition.condition_id = _key
            self.db_add([_condition, ], session)
            session.commit()
            _condition.set_attributes(RTKCommonDB.conditions[_key])
            session.commit()

        RTKMeasurement.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.measurements.keys():
            _measurement = RTKMeasurement()
            _measurement.measurement_id = _key
            self.db_add([_measurement, ], session)
            session.commit()
            _measurement.set_attributes(RTKCommonDB.measurements[_key])
            session.commit()

        RTKLoadHistory.__table__.create(bind=self.engine)
        for _key in RTKCommonDB.historys.keys():
            _history = RTKLoadHistory()
            _history.history_id = _key
            self.db_add([_history, ], session)
            session.commit()
            _history.set_attributes(RTKCommonDB.historys[_key])
            session.commit()

        return False

    def db_create_program(self, database, session):
        """
        Method to create a new RTK Program database.

        :param str database: the absolute path to the database to create.
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """

        create_database(database)

        RTKRevision.__table__.create(bind=self.engine)
        _revision = RTKRevision()
        _revision.revision_id = 1
        _revision.description = _(u"Initial Revision")
        self.db_add([_revision, ], session)
        session.commit()

        RTKMission.__table__.create(bind=self.engine)
        _mission = RTKMission()
        _mission.revision_id = _revision.revision_id
        _mission.mission_id = 1
        _mission.description = _(u"Default Mission")
        self.db_add([_mission, ], session)
        session.commit()

        RTKMissionPhase.__table__.create(bind=self.engine)
        _phase = RTKMissionPhase()
        _phase.mission_id = _mission.mission_id
        _phase.phase_id = 1
        _phase.description = _(u"Default Mission Phase 1")
        self.db_add([_phase, ], session)
        session.commit()

        RTKEnvironment.__table__.create(bind=self.engine)
        RTKFailureDefinition.__table__.create(bind=self.engine)
        RTKFunction.__table__.create(bind=self.engine)
        RTKRequirement.__table__.create(bind=self.engine)
        RTKStakeholder.__table__.create(bind=self.engine)
        RTKMatrix.__table__.create(bind=self.engine)
        RTKHardware.__table__.create(bind=self.engine)
        _hardware = RTKHardware()
        _hardware.revision_id = _revision.revision_id
        _hardware.hardware_id = 1
        _hardware.description = _(u"System")
        self.db_add([_hardware, ], session)
        session.commit()

        RTKAllocation.__table__.create(bind=self.engine)
        _allocation = RTKAllocation()
        _allocation.hardware_id = _hardware.hardware_id

        RTKHazardAnalysis.__table__.create(bind=self.engine)
        _hazard = RTKHazardAnalysis()
        _hazard.hardware_id = _hardware.hardware_id

        RTKSimilarItem.__table__.create(bind=self.engine)
        _similar_item = RTKSimilarItem()
        _similar_item.hardware_id = _hardware.hardware_id

        RTKReliability.__table__.create(bind=self.engine)
        _reliability = RTKReliability()
        _reliability.hardware_id = _hardware.hardware_id
        self.db_add([_allocation, _hazard, _similar_item, _reliability],
                    session)
        session.commit()

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
        _software = RTKSoftware()
        _software.revision_id = _revision.revision_id
        _software.software_id = 1
        _software.description = _(u"System Software")
        self.db_add([_software, ], session)
        session.commit()

        RTKSoftwareDevelopment.__table__.create(bind=self.engine)
        for i in range(43):
            _sw_development = RTKSoftwareDevelopment()
            _sw_development.software_id = _software.software_id
            _sw_development.question_id = i
            self.db_add([_sw_development, ], session)
        session.commit()

        RTKSoftwareReview.__table__.create(bind=self.engine)
        for i in range(50):
            _sw_review = RTKSoftwareReview()
            _sw_review.software_id = _software.software_id
            _sw_review.question_id = i
            _sw_review.type = 'SRR'
            self.db_add([_sw_review, ], session)
        for i in range(38):
            _sw_review = RTKSoftwareReview()
            _sw_review.software_id = _software.software_id
            _sw_review.question_id = i
            _sw_review.type = 'PDR'
            self.db_add([_sw_review, ], session)
        for i in range(35):
            _sw_review = RTKSoftwareReview()
            _sw_review.software_id = _software.software_id
            _sw_review.question_id = i
            _sw_review.type = 'CDR'
            self.db_add([_sw_review, ], session)
        for i in range(24):
            _sw_review = RTKSoftwareReview()
            _sw_review.software_id = _software.software_id
            _sw_review.question_id = i
            _sw_review.type = 'TRR'
            self.db_add([_sw_review, ], session)
        session.commit()

        RTKSoftwareTest.__table__.create(bind=self.engine)
        for i in range(21):
            _sw_test = RTKSoftwareTest()
            _sw_test.software_id = _software.software_id
            _sw_test.technique_id = i
            self.db_add([_sw_test, ], session)
        session.commit()

        RTKValidation.__table__.create(bind=self.engine)
        RTKIncident.__table__.create(bind=self.engine)
        RTKIncidentDetail.__table__.create(bind=self.engine)
        RTKIncidentAction.__table__.create(bind=self.engine)
        RTKTest.__table__.create(bind=self.engine)
        RTKGrowthTest.__table__.create(bind=self.engine)
        RTKSurvival.__table__.create(bind=self.engine)
        RTKSurvivalData.__table__.create(bind=self.engine)

        return False

    def db_add(self, item, session):
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

        for _item in item:
            try:
                session.add(_item)
                session.commit()
            except:
                session.rollback()
                _error_code = 1003
                _msg = "RTK ERROR: Adding one or more items to the RTK " \
                       "Program database."

        return _error_code, _msg

    def db_update(self, session):
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
        except:
            session.rollback()
            _error_code = 1004
            _msg = "RTK ERROR: Updating the RTK Program database."

        return _error_code, _msg

    def db_delete(self, item, session):
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
        except:
            session.rollback()
            _error_code = 1005
            _msg = "RTK ERROR: Deleting an item from the RTK Program database."

        return _error_code, _msg

    def db_query(self, query, session):
        """
        Method to exceute an SQL query against the connected database.

        :param str query: the SQL query to execute
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return:
        :rtype: str
        """

        return session.execute(query)

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

    def db_load_globals(self, session):
        """
        Method to load all the global Configuration variables from the RTK
        Site database.

        :param session: the SQLAlchemy scoped_session to use for querying the
                        RTK Common database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # ------------------------------------------------------------------- #
        # Build the component category, component subcategory, failure modes  #
        # tree.                                                               #
        # ------------------------------------------------------------------- #
        self.tree.create_node('Components', -1)
        for _category in session.query(RTKCategory).\
                filter(RTKCategory.type == 'hardware').all():
            self.tree.create_node(_category.name, _category.category_id,
                                  parent=-1,
                                  data=_category.get_attributes()[1:])

        for _subcategory in session.query(RTKSubCategory).\
                filter(RTKSubCategory.category_id == _category.category_id).\
                all():
            # We need to create a unique identifer for each subcategory because
            # we can't have two nodes in the tree with the same ID, but we can
            # have a category and subcategory with the same ID in the database.
            # This simple method garantees a unique ID for the subcategory for
            # the tree.
            _identifier = str(_subcategory.category_id) + \
                          str(_subcategory.subcategory_id)
            self.tree.create_node(_subcategory.description, _identifier,
                                  parent=_subcategory.category_id,
                                  data=_subcategory.get_attributes()[2:])

        for _mode in session.query(RTKFailureMode).all():
            # We need to create a unique identifer for each mode because
            # we can't have two nodes in the tree with the same ID, but we can
            # have a category, subcategory, and/or mode with the same ID in the
            # database.  This simple method garantees a unique ID for the mode
            # for the tree.  For the same reason we have to create the parent
            # ID.
            _identifier = str(_mode.category_id) + \
                          str(_mode.subcategory_id) + \
                          str(_mode.mode_id)
            _parent = str(_mode.category_id) + \
                      str(_mode.subcategory_id)
            self.tree.create_node(_mode.description, _identifier,
                                  parent=_parent,
                                  data=_mode.get_attributes()[3:])

        for _stakeholder in session.query(RTKStakeholders).all():
            Configuration.RTK_STAKEHOLDERS[_stakeholder.stakeholders_id] = \
                _stakeholder.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKCategory.                                 #
        # ------------------------------------------------------------------- #
        for _category in session.query(RTKCategory).\
                filter(RTKCategory.category_id == 'action').all():
            Configuration.RTK_ACTION_CATEGORY[_category.category_id] = \
                _category.get_attributes()[1:]

        for _category in session.query(RTKCategory).\
                filter(RTKCategory.type == 'incident').all():
            Configuration.RTK_INCIDENT_CATEGORY[_category.category_id] = \
                _category.get_attributes()[1:]

        for _severity in session.query(RTKCategory).\
                filter(RTKCategory.type == 'risk').all():
             Configuration.RTK_SEVERITY[_severity.category_id] = \
                 _severity.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKEnviron.                                  #
        # ------------------------------------------------------------------- #
        for _environ in session.query(RTKEnviron).\
                filter(RTKEnviron.type == 'active').all():
            Configuration.RTK_ACTIVE_ENVIRONMENTS[_environ.environ_id] = \
                _environ.get_attributes()[1:]

        for _environ in session.query(RTKEnviron).\
                filter(RTKEnviron.type == 'dormant').all():
            Configuration.RTK_DORMANT_ENVIRONMENTS[_environ.environ_id] = \
                _environ.get_attributes()[1:]

        for _environ in session.query(RTKEnviron).\
                filter(RTKEnviron.type == 'development').all():
            Configuration.RTK_SW_DEV_ENVIRONMENTS[_environ.environ_id] = \
                _environ.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKGroup.                                    #
        # ------------------------------------------------------------------- #
        for _group in session.query(RTKGroup).\
                filter(RTKGroup.type == 'affinity').all():
            Configuration.RTK_AFFINITY_GROUPS[_group.group_id] = \
                _group.get_attributes()[1:]

        for _group in session.query(RTKGroup).\
                filter(RTKGroup.type == 'workgroup').all():
            Configuration.RTK_WORKGROUPS[_group.group_id] = \
                _group.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKLevel.                                    #
        # ------------------------------------------------------------------- #
        for _level in session.query(RTKLevel).\
                filter(RTKLevel.type == 'probability').all():
            Configuration.RTK_FAILURE_PROBABILITY[_level.level_id] = \
                _level.get_attributes()[1:]

        for _level in session.query(RTKLevel).\
                filter(RTKLevel.type == 'software').all():
            Configuration.RTK_SW_LEVELS[_level.level_id] = \
                _level.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RTKMethod.                               #
        # ------------------------------------------------------------------- #
        for _method in session.query(RTKMethod).\
                filter(RTKMethod.type == 'detection').all():
            Configuration.RTK_DETECTION_METHODS[_method.method_id] = \
                _method.get_attributes[1:]

        for _method in session.query(RTKMethod).\
                filter(RTKMethod.type == 'test').all():
            Configuration.RTK_SW_TEST_METHODS[_method.method_id] = \
                _method.get_attributes[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKModel.                                    #
        # ------------------------------------------------------------------- #
        for _model in session.query(RTKModel).\
                filter(RTKModel.type == 'allocation').all():
            Configuration.RTK_ALLOCATION_MODELS[_model.model_id] = \
                _model.get_attributes()[1:]
        for _model in session.query(RTKModel).\
                filter(RTKModel.type == 'rprediction').all():
            Configuration.RTK_HR_MODEL[_model.model_id] = \
                _model.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load the dictionaries from RTKPhase.                                #
        # ------------------------------------------------------------------- #
        for _phase in session.query(RTKPhase).\
                filter(RTKPhase.type == 'lifecycle').all():
            Configuration.RTK_LIFECYCLE[_phase.phase_id] = \
                _phase.get_atrributes()[1:]

        for _phase in session.query(RTKPhase).\
                filter(RTKPhase.type == 'development').all():
            Configuration.RTK_SW_DEV_PHASES[_phase.phase_id] = \
                _phase.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKRPN.                                      #
        # ------------------------------------------------------------------- #
        for _rpn in session.query(RTKRPN).\
                filter(RTKRPN.type == 'detection').all():
            Configuration.RTK_RPN_DETECTION[_rpn.rpn_id] = \
                _rpn.get_attributes()[1:]

        for _rpn in session.query(RTKRPN).\
                filter(RTKRPN.type == 'occurrence').all():
            Configuration.RTK_RPN_OCCURRENCE[_rpn.rpn_id] = \
                _rpn.get_attributes()[1:]

        for _rpn in session.query(RTKRPN). \
                filter(RTKRPN.type == 'severity').all():
            Configuration.RTK_RPN_SEVERITY[_rpn.rpn_id] = \
                _rpn.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKStatus.                                   #
        # ------------------------------------------------------------------- #
        for _status in session.query(RTKStatus).\
                filter(RTKStatus.type == 'action').all():
            Configuration.RTK_ACTION_STATUS[_status.status_id] = \
                _status.get_attributes()[1:]

        for _status in session.query(RTKStatus).\
                filter(RTKStatus.type == 'incident').all():
            Configuration.RTK_INCIDENT_STATUS[_status.status_id] = \
                _status.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from RTKType.                                     #
        # ------------------------------------------------------------------- #
        Configuration.RTK_CONTROL_TYPES = [_(u"Prevention"), _(u"Detection")]

        for _type in session.query(RTKType). \
                filter(RTKType.type == 'cost').all():
            Configuration.RTK_COST_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        for _type in session.query(RTKType).\
                filter(RTKType.type == 'mtbf').all():
            Configuration.RTK_HR_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        for _type in session.query(RTKType).\
                filter(RTKType.type == 'incident').all():
            Configuration.RTK_INCIDENT_TYPE[_type.type_id] = \
                _type.get_attributes[1:]

        for _type in session.query(RTKType).\
                filter(RTKType.type == 'mttr').all():
            Configuration.RTK_MTTR_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        for _type in session.query(RTKType).\
                filter(RTKType.type == 'requirement').all():
            Configuration.RTK_REQUIREMENT_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        for _type in session.query(RTKType).\
                filter(RTKType.type == 'validation').all():
            Configuration.RTK_VALIDATION_TYPE[_type.type_id] = \
                _type.get_attributes()[1:]

        # ------------------------------------------------------------------- #
        # Load dictionaries from tables not requiring a filter.               #
        # ------------------------------------------------------------------- #
        for _application in session.query(RTKApplication).all():
            Configuration.RTK_SW_APPLICATION[_application.application_id] = \
                _application.get_attributes()[1:]

        for _crit in session.query(RTKCriticality).all():
            Configuration.RTK_CRITICALITY[_crit.criticality_id] = \
                _crit.get_attributes()[1:]

        for _dist in session.query(RTKDistribution).all():
            Configuration.RTK_S_DIST[_dist.distribution_id] = \
                _dist.get_attributes()[1:]

        for _hazard in session.query(RTKHazards).all():
            Configuration.RTK_HAZARDS[_hazard.hazard_id] = \
                _hazard.get_attributes()[1:]

        for _manufacturer in session.query(RTKManufacturer).all():
            Configuration.RTK_MANUFACTURERS[_manufacturer.manufacturer_id] = \
            _manufacturer.get_attributes()[1:]

        for _unit in session.query(RTKUnit).\
                filter(RTKUnit.type == 'measurement').all():
            Configuration.RTK_MEASUREMENT_UNITS[_unit.unit_id] = \
                _unit.get_attributes()[1:]

        for _user in session.query(RTKUser).all():
            Configuration.RTK_USERS[_user.user_id] = \
                _user.get_attributes()[1:]

        return _return
