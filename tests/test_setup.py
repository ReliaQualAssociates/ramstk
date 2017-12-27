#!/usr/bin/env python -O
# -*- coding: utf-8 -*-
#
#       tests.test_setup.py is part of The RTK Project
#
# All rights reserved.
"""
This is the test package for testing RTK.
"""

import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database

sys.path.insert(0,
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '../rtk/')))

# pylint: disable=import-error, wrong-import-position
import Configuration
import Utilities

# Import the RTK Common database table objects.
import dao.RTKCommonDB
from dao import RTKSiteInfo, RTKUser, RTKGroup, RTKEnviron, RTKModel, \
    RTKType, RTKCategory, RTKSubCategory, RTKPhase, RTKDistribution, \
    RTKManufacturer, RTKUnit, RTKMethod, RTKCriticality, RTKRPN, RTKLevel, \
    RTKApplication, RTKHazards, RTKStakeholders, RTKStatus, RTKCondition, \
    RTKFailureMode, RTKMeasurement, RTKLoadHistory

# Import the RTK Program database table objects.
from dao import RTKAction, RTKAllocation, RTKCause, RTKControl, \
    RTKDesignElectric, RTKDesignMechanic, RTKEnvironment, \
    RTKFailureDefinition, RTKFunction, RTKGrowthTest, RTKHardware, \
    RTKHazardAnalysis, RTKIncident, RTKIncidentAction, RTKIncidentDetail, \
    RTKMatrix, RTKMechanism, RTKMilHdbkF, RTKMission, RTKMissionPhase, \
    RTKMode, RTKNSWC, RTKOpLoad, RTKOpStress, RTKProgramInfo, \
    RTKProgramStatus, RTKReliability, RTKRequirement, RTKRevision, \
    RTKSimilarItem, RTKSoftware, RTKSoftwareDevelopment, RTKSoftwareReview, \
    RTKSoftwareTest, RTKStakeholder, RTKSurvival, RTKSurvivalData, RTKTest, \
    RTKTestMethod, RTKValidation

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 - 2017 Andrew "weibullguy" Rowland'


def _create_common_database():

    # Create and populate the RTK Common test database.
    engine = create_engine('sqlite:////tmp/TestCommonDB.rtk', echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    RTKSiteInfo.__table__.create(bind=engine)
    RTKUser.__table__.create(bind=engine)
    RTKGroup.__table__.create(bind=engine)
    RTKEnviron.__table__.create(bind=engine)
    RTKModel.__table__.create(bind=engine)
    RTKType.__table__.create(bind=engine)
    RTKCategory.__table__.create(bind=engine)
    RTKSubCategory.__table__.create(bind=engine)
    RTKPhase.__table__.create(bind=engine)
    RTKDistribution.__table__.create(bind=engine)
    RTKManufacturer.__table__.create(bind=engine)
    RTKUnit.__table__.create(bind=engine)
    RTKMethod.__table__.create(bind=engine)
    RTKCriticality.__table__.create(bind=engine)
    RTKRPN.__table__.create(bind=engine)
    RTKLevel.__table__.create(bind=engine)
    RTKApplication.__table__.create(bind=engine)
    RTKHazards.__table__.create(bind=engine)
    RTKStakeholders.__table__.create(bind=engine)
    RTKStatus.__table__.create(bind=engine)
    RTKCondition.__table__.create(bind=engine)
    RTKFailureMode.__table__.create(bind=engine)
    RTKMeasurement.__table__.create(bind=engine)
    RTKLoadHistory.__table__.create(bind=engine)

    # Add an entry to each table.  These are used as the DUT in each test
    # file.
    _site_info = RTKSiteInfo()
    _site_info.product_key = '9490059723f3a743fb961d092d3283422f4f2d13'
    session.add(_site_info)
    session.add(RTKUser())

    _group = RTKGroup()
    _group.description = 'Engineering, Systems'
    _group.group_type = 'workgroup'
    session.add(_group)

    _group = RTKGroup()
    _group.description = 'Engineering, Reliability'
    _group.group_type = 'workgroup'
    session.add(_group)

    _group = RTKGroup()
    _group.description = 'Engineering, Design Services'
    _group.group_type = 'workgroup'
    session.add(_group)

    session.add(RTKEnviron())
    session.add(RTKModel())
    _type = RTKType()
    _type.code = 'STMD'
    _type.description = 'State/Mode Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    _type = RTKType()
    _type.code = 'FUNC'
    _type.description = 'Functional Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    _type = RTKType()
    _type.code = 'PERF'
    _type.description = 'Performance Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    _type = RTKType()
    _type.code = 'EXIN'
    _type.description = 'External Interface Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    _type = RTKType()
    _type.code = 'ENVT'
    _type.description = 'Environmental Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    _type = RTKType()
    _type.code = 'RESC'
    _type.description = 'Resource Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    _type = RTKType()
    _type.code = 'PHYS'
    _type.description = 'Physical Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    _type = RTKType()
    _type.code = 'QUAL'
    _type.description = 'Quality Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    _type = RTKType()
    _type.code = 'DSGN'
    _type.description = 'Design Requirement'
    _type.type_type = 'requirement'
    session.add(_type)

    session.add(RTKPhase())
    session.add(RTKDistribution())
    session.add(RTKManufacturer())
    session.add(RTKUnit())
    session.add(RTKMethod())
    session.add(RTKCriticality())
    session.add(RTKRPN())
    session.add(RTKLevel())
    session.add(RTKApplication())
    session.add(RTKHazards())
    session.add(RTKStakeholders())
    session.add(RTKStatus())
    session.add(RTKCondition())
    session.add(RTKMeasurement())
    session.add(RTKLoadHistory())
    session.commit()

    for _key in dao.RTKCommonDB.RTK_CATEGORIES.keys():
        _category = RTKCategory()
        _category.category_id = _key
        session.add(_category)
        _category.set_attributes(dao.RTKCommonDB.RTK_CATEGORIES[_key])
    session.commit()

    _subcategory = RTKSubCategory()
    _subcategory.category_id = 9
    session.add(_subcategory)
    session.commit()
    _failuremode = RTKFailureMode()
    _failuremode.category_id = 9
    _failuremode.subcategory_id = _subcategory.subcategory_id
    session.add(_failuremode)
    session.commit()


def _create_program_database():
    bcolors = {
        'HEADER': '\033[35m',
        'OKBLUE': '\033[34m',
        'OKGREEN': '\033[32m',
        'WARNING': '\033[33m',
        'FAIL': '\033[31m',
        'ENDC': '\033[0m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m'
    }

    print "\n" + bcolors['OKBLUE'] + bcolors['BOLD'] + \
          "  Creating RTK Program test database...." + bcolors['ENDC'] + "\n"

    # Create the RTK Program test database.
    create_database('sqlite:////tmp/TestDB.rtk')

    engine = create_engine('sqlite:////tmp/TestDB.rtk', echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the RTK Program test database.
    RTKRevision.__table__.create(bind=engine)
    RTKMission.__table__.create(bind=engine)
    RTKMissionPhase.__table__.create(bind=engine)
    RTKEnvironment.__table__.create(bind=engine)
    RTKFailureDefinition.__table__.create(bind=engine)
    RTKFunction.__table__.create(bind=engine)
    RTKRequirement.__table__.create(bind=engine)
    RTKStakeholder.__table__.create(bind=engine)
    RTKMatrix.__table__.create(bind=engine)
    RTKHardware.__table__.create(bind=engine)
    RTKAllocation.__table__.create(bind=engine)
    RTKHazardAnalysis.__table__.create(bind=engine)
    RTKSimilarItem.__table__.create(bind=engine)
    RTKReliability.__table__.create(bind=engine)
    RTKMilHdbkF.__table__.create(bind=engine)
    RTKNSWC.__table__.create(bind=engine)
    RTKDesignElectric.__table__.create(bind=engine)
    RTKDesignMechanic.__table__.create(bind=engine)
    RTKMode.__table__.create(bind=engine)
    RTKMechanism.__table__.create(bind=engine)
    RTKCause.__table__.create(bind=engine)
    RTKControl.__table__.create(bind=engine)
    RTKAction.__table__.create(bind=engine)
    RTKOpLoad.__table__.create(bind=engine)
    RTKOpStress.__table__.create(bind=engine)
    RTKProgramInfo.__table__.create(bind=engine)
    RTKProgramStatus.__table__.create(bind=engine)
    RTKTestMethod.__table__.create(bind=engine)
    RTKSoftware.__table__.create(bind=engine)
    RTKSoftwareDevelopment.__table__.create(bind=engine)
    RTKSoftwareReview.__table__.create(bind=engine)
    RTKSoftwareTest.__table__.create(bind=engine)
    RTKValidation.__table__.create(bind=engine)
    RTKIncident.__table__.create(bind=engine)
    RTKIncidentDetail.__table__.create(bind=engine)
    RTKIncidentAction.__table__.create(bind=engine)
    RTKTest.__table__.create(bind=engine)
    RTKGrowthTest.__table__.create(bind=engine)
    RTKSurvival.__table__.create(bind=engine)
    RTKSurvivalData.__table__.create(bind=engine)

    _program = RTKProgramInfo()
    _program.revision_prefix = 'REV'
    session.add(_program)
    session.commit()

    _revision = RTKRevision()
    _revision.revision_id = 1
    session.add(_revision)
    session.commit()

    # Create tables that have Revision ID as a Foreign Key.
    _program_status = RTKProgramStatus()
    _program_status.revision_id = _revision.revision_id
    session.add(_program_status)

    _mission = RTKMission()
    _mission.revision_id = _revision.revision_id
    _mission.description = 'Test Mission Description'
    session.add(_mission)

    _failure_definition = RTKFailureDefinition()
    _failure_definition.revision_id = _revision.revision_id
    session.add(_failure_definition)

    _function = RTKFunction()
    _function.revision_id = _revision.revision_id
    _function.function_code = 'PRESS-001'
    session.add(_function)

    _function = RTKFunction()
    _function.revision_id = _revision.revision_id
    _function.function_code = 'FLOW-001'
    session.add(_function)

    _function = RTKFunction()
    _function.revision_id = _revision.revision_id
    _function.function_code = 'TEMP-001'
    session.add(_function)

    _requirement = RTKRequirement()
    _requirement.revision_id = _revision.revision_id
    _requirement.requirement_code = 'REL-0001'
    session.add(_requirement)

    _requirement = RTKRequirement()
    _requirement.revision_id = _revision.revision_id
    _requirement.requirement_code = 'PERF-0001'
    session.add(_requirement)

    _stakeholder = RTKStakeholder()
    _stakeholder.revision_id = _revision.revision_id
    session.add(_stakeholder)

    # Add Hardware items to the RTK Program database.
    _hardware_id = _build_hardware_bom(session, _revision.revision_id)

    # Add Incidents to the RTK Program database.
    _incident = RTKIncident()
    _incident.revision_id = _revision.revision_id
    session.add(_incident)

    _software = RTKSoftware()
    _software.revision_id = _revision.revision_id
    session.add(_software)

    _test = RTKTest()
    _test.revision_id = _revision.revision_id
    session.add(_test)

    _survival = RTKSurvival()
    _survival.revision_id = _revision.revision_id
    session.add(_survival)

    _validation = RTKValidation()
    _validation.revision_id = _revision.revision_id
    _validation.description = 'Test Validation Task'
    session.add(_validation)

    session.commit()

    # Create tables that have Hardware ID as a Foreign Key.
    _allocation = RTKAllocation()
    _allocation.hardware_id = _hardware_id
    session.add(_allocation)

    _hazard_analysis = RTKHazardAnalysis()
    _hazard_analysis.hardware_id = _hardware_id
    session.add(_hazard_analysis)

    _similar_item = RTKSimilarItem()
    _similar_item.hardware_id = _hardware_id
    session.add(_similar_item)

    # Create test Function:Hardware matrix
    for _row in [1, 2, 3]:
        for _column in [1, 2, 3]:
            _matrix = RTKMatrix()
            _matrix.revision_id = _revision.revision_id
            _matrix.matrix_id = 1
            _matrix.matrix_type = 'fnctn_hrdwr'
            _matrix.row_item_id = _row
            _matrix.column_item_id = _column
            session.add(_matrix)

    # Create test Requirement:Hardware matrix
    for _row in [1, 2]:
        for _column in [1, 2, 3]:
            _matrix = RTKMatrix()
            _matrix.revision_id = _revision.revision_id
            _matrix.matrix_id = 11
            _matrix.matrix_type = 'rqrmnt_hrdwr'
            _matrix.row_item_id = _row
            _matrix.column_item_id = _column
            session.add(_matrix)

    # Create test Hardware:Validation matrix
    for _row in [1, 2, 3]:
        _matrix = RTKMatrix()
        _matrix.revision_id = _revision.revision_id
        _matrix.matrix_id = 22
        _matrix.matrix_type = 'hrdwr_vldtn'
        _matrix.row_item_id = _row
        _matrix.column_item_id = 1
        session.add(_matrix)

    session.commit()

    # Create tables that have other than Revision ID or Hardware ID as a
    # Foreign Key or have o Foreign Key.
    _phase = RTKMissionPhase()
    _phase.mission_id = _mission.mission_id
    _phase.description = 'Test Mission Phase'
    session.add(_phase)
    session.commit()

    _environment = RTKEnvironment()
    _environment.phase_id = _phase.phase_id
    _environment.name = 'Test Environmental Condition'
    session.add(_environment)
    session.commit()

    _mode = RTKMode()
    _mode.function_id = _function.function_id
    _mode.hardware_id = _hardware_id
    _mode.description = 'Test Failure Mode #1'
    session.add(_mode)
    session.commit()

    _mechanism = RTKMechanism()
    _mechanism.mode_id = _mode.mode_id
    _mechanism.description = 'Test Failure Mechanism #1'
    session.add(_mechanism)
    session.commit()

    _cause = RTKCause()
    _cause.mechanism_id = _mechanism.mechanism_id
    _cause.description = 'Test Failure Cause #1'
    session.add(_cause)
    session.commit()

    _control = RTKControl()
    _control.mode_id = _mode.mode_id
    _control.cause_id = _cause.cause_id
    _control.description = 'Test Control for Failure Cause #1'
    session.add(_control)
    session.commit()

    _action = RTKAction()
    _action.mode_id = _mode.mode_id
    _action.cause_id = _cause.cause_id
    _action.action_recommended = 'Recommended action for Failure Cause #1'
    session.add(_action)
    session.commit()

    _op_load = RTKOpLoad()
    _op_load.mechanism_id = _mechanism.mechanism_id
    session.add(_op_load)

    _software_development = RTKSoftwareDevelopment()
    _software_development.software_id = _software.software_id
    session.add(_software_development)

    _software_review = RTKSoftwareReview()
    _software_review.software_id = _software.software_id
    session.add(_software_review)

    _software_test = RTKSoftwareTest()
    _software_test.software_id = _software.software_id
    session.add(_software_test)

    _incident_action = RTKIncidentAction()
    _incident_action.incident_id = _incident.incident_id
    session.add(_incident_action)

    _incident_detail = RTKIncidentDetail()
    _incident_detail.incident_id = _incident.incident_id
    session.add(_incident_detail)

    _growth_test = RTKGrowthTest()
    _growth_test.test_id = _test.test_id
    session.add(_growth_test)

    _survival_data = RTKSurvivalData()
    _survival_data.survival_id = _survival.survival_id
    session.add(_survival_data)

    session.commit()

    _op_stress = RTKOpStress()
    _op_stress.load_id = _op_load.load_id
    session.add(_op_stress)

    session.commit()

    _test_method = RTKTestMethod()
    _test_method.stress_id = _op_stress.stress_id
    session.add(_test_method)

    session.commit()


def _build_hardware_bom(session, revision_id):
    """
    Build a Hardware BoM in the test database.

    :param session:
    :param int revision_id:
    """
    _hardware = RTKHardware()
    _hardware.revision_id = revision_id
    _hardware.ref_des = 'S1'
    session.add(_hardware)
    session.commit()
    _parent_id = _hardware.hardware_id

    _entity = RTKDesignElectric()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKDesignMechanic()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKMilHdbkF()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKNSWC()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKReliability()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _hardware = RTKHardware()
    _hardware.parent_id = _parent_id
    _hardware.revision_id = revision_id
    _hardware.ref_des = 'SS1'
    session.add(_hardware)
    session.commit()

    _entity = RTKDesignElectric()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKDesignMechanic()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKMilHdbkF()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKNSWC()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKReliability()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _hardware = RTKHardware()
    _hardware.parent_id = _parent_id
    _hardware.revision_id = revision_id
    _hardware.ref_des = 'SS2'
    session.add(_hardware)
    session.commit()

    _entity = RTKDesignElectric()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKDesignMechanic()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKMilHdbkF()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKNSWC()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)

    _entity = RTKReliability()
    _entity.hardware_id = _hardware.hardware_id
    session.add(_entity)
    session.commit()

    return _hardware.hardware_id

def setUp():

    # Clean up from previous runs.
    print "Cleaning up logs and databases from previous run."

    if os.path.isfile('/tmp/RTK_debug.log'):
        os.remove('/tmp/RTK_debug.log')

    if os.path.isfile('/tmp/RTK_user.log'):
        os.remove('/tmp/RTK_user.log')

    if os.path.isfile('/tmp/TestDB.rtk'):
        os.remove('/tmp/TestDB.rtk')

    if os.path.isfile('/tmp/TestCommonDB.rtk'):
        os.remove('/tmp/TestCommonDB.rtk')

    _create_common_database()
    _create_program_database()

    Configuration.RTK_HR_MULTIPLIER = 1.0
    Configuration.RTK_DEBUG_LOG = Utilities.create_logger(
        "RTK.debug", 'DEBUG', '/tmp/RTK_debug.log')
    Configuration.RTK_USER_LOG = Utilities.create_logger(
        "RTK.user", 'INFO', '/tmp/RTK_user.log')


def tearDown():

    #if os.path.isfile('/tmp/TestDB.rtk'):
    #    os.remove('/tmp/TestDB.rtk')

    #if os.path.isfile('/tmp/TestCommonDB.rtk'):
    #    os.remove('/tmp/TestCommonDB.rtk')
    pass
