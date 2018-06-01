# -*- coding: utf-8 -*-
#
#       rtk.dao.RTKProgramDB.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""RTKProgramDB File."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

RTK_BASE = declarative_base()

# This file contains all the dictionaries defining the default fields for each
# of the tables in the RTK Program database.
RTK_RPNS = {
    0: ('None', 'No effect.', 'severity', 1),
    1: ('Very Minor', 'System operable with minimal interference.', 'severity',
        2),
    2: ('Minor', 'System operable with some degradation of '
        'performance.', 'severity', 3),
    3: ('Very Low', 'System operable with significant degradation of '
        'performance.', 'severity', 4),
    4: ('Low', 'System inoperable without damage.', 'severity', 5),
    5: ('Moderate', 'System inoperable with minor damage.', 'severity', 6),
    6: ('High', 'System inoperable with system damage.', 'severity', 7),
    7: ('Very High', 'System inoperable with destructive failure '
        'without compromising safety.', 'severity', 8),
    8: ('Hazardous, with warning',
        'Failure effects safe system operation with warning.', 'severity', 9),
    9:
    ('Hazardous, without warning',
     'Failure effects safe system operation without warning.', 'severity', 10),
    10: ('Remote', 'Failure rate is 1 in 1,500,000.', 'occurrence', 1),
    11: ('Very Low', 'Failure rate is 1 in 150,000.', 'occurrence', 2),
    12: ('Low', 'Failure rate is 1 in 15,000', 'occurrence', 3),
    13: ('Moderately Low', 'Failure rate is 1 in 2000.', 'occurrence', 4),
    14: ('Moderate', 'Failure rate is 1 in 400.', 'occurrence', 5),
    15: ('Moderately High', 'Failure rate is 1 in 80.', 'occurrence', 6),
    16: ('High', 'Failure rate is 1 in 20.', 'occurrence', 7),
    17: ('Very High', 'Failure rate is 1 in 8.', 'occurrence', 8),
    18: ('Extremely High', 'Failure rate is 1 in 3.', 'occurrence', 9),
    19: ('Dangerously High', 'Failure rate is > 1 in 2.', 'occurrence', 10),
    20: ('Almost Certain',
         'Design control will almost certainly detect a potential '
         'mechanism/cause and subsequent failure mode.', 'detection', 1),
    21: ('Very High', 'Very high chance the existing design controls '
         'will or can detect a potential mechanism/cause and '
         'subsequent failure mode.', 'detection', 2),
    22: ('High', 'High chance the existing design controls will or '
         'can detect a potential mechanism/cause and subsequent '
         'failure mode.', 'detection', 3),
    23: ('Moderately High', 'Moderately high chance the existing '
         'design controls will or can detect a potential '
         'mechanism/cause and subsequent failure mode.', 'detection', 4),
    24: ('Moderate', 'Moderate chance the existing design controls '
         'will or can detect a potential mechanism/cause and '
         'subsequent failure mode.', 'detection', 5),
    25: ('Low', 'Low chance the existing design controls will or can '
         'detect a potential mechanism/cause and subsequent failure '
         'mode.', 'detection', 6),
    26: ('Very Low', 'Very low chance the existing design controls '
         'will or can detect a potential mechanism/cause and '
         'subsequent failure mode.', 'detection', 7),
    27: ('Remote', 'Remote chance the existing design controls will '
         'or can detect a potential mechanism/cause and subsequent '
         'failure mode.', 'detection', 8),
    28: ('Very Remote', 'Very remote chance the existing design '
         'controls will or can detect a potential mechanism/cause and '
         'subsequent failure mode.', 'detection', 9),
    29: ('Absolute Uncertainty', 'Existing design controls will not '
         'or cannot detect a potential mechanism/cause and subsequent '
         'failure mode; there is no design control.', 'detection', 10)
}


def create_program_db(**kwargs):
    """Create and populate a RTK Program database."""
    from rtk.dao import (
        RTKAction, RTKAllocation, RTKCause, RTKControl, RTKDesignElectric,
        RTKDesignMechanic, RTKEnvironment, RTKFailureDefinition, RTKFunction,
        RTKGrowthTest, RTKHardware, RTKHazardAnalysis, RTKIncident,
        RTKIncidentAction, RTKIncidentDetail, RTKLoadHistory, RTKMatrix,
        RTKMechanism, RTKMilHdbkF, RTKMission, RTKMissionPhase, RTKMode,
        RTKNSWC, RTKOpLoad, RTKOpStress, RTKProgramInfo, RTKProgramStatus,
        RTKReliability, RTKRequirement, RTKRevision, RTKRPN, RTKSimilarItem,
        RTKSoftware, RTKSoftwareDevelopment, RTKSoftwareReview,
        RTKSoftwareTest, RTKStakeholder, RTKSurvival, RTKSurvivalData, RTKTest,
        RTKTestMethod, RTKUnits, RTKValidation)

    uri = kwargs['database']

    # Create and populate the RTK Program test database.
    engine = create_engine(uri, echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the RTK Program database.
    RTKAction.__table__.create(bind=engine)
    RTKAllocation.__table__.create(bind=engine)
    RTKCause.__table__.create(bind=engine)
    RTKControl.__table__.create(bind=engine)
    RTKDesignElectric.__table__.create(bind=engine)
    RTKDesignMechanic.__table__.create(bind=engine)
    RTKEnvironment.__table__.create(bind=engine)
    RTKFailureDefinition.__table__.create(bind=engine)
    RTKFunction.__table__.create(bind=engine)
    RTKGrowthTest.__table__.create(bind=engine)
    RTKHardware.__table__.create(bind=engine)
    RTKHazardAnalysis.__table__.create(bind=engine)
    RTKIncident.__table__.create(bind=engine)
    RTKIncidentAction.__table__.create(bind=engine)
    RTKIncidentDetail.__table__.create(bind=engine)
    RTKLoadHistory.__table__.create(bind=engine)
    RTKMatrix.__table__.create(bind=engine)
    RTKMechanism.__table__.create(bind=engine)
    RTKMilHdbkF.__table__.create(bind=engine)
    RTKMission.__table__.create(bind=engine)
    RTKMissionPhase.__table__.create(bind=engine)
    RTKMode.__table__.create(bind=engine)
    RTKNSWC.__table__.create(bind=engine)
    RTKOpLoad.__table__.create(bind=engine)
    RTKOpStress.__table__.create(bind=engine)
    RTKProgramInfo.__table__.create(bind=engine)
    RTKProgramStatus.__table__.create(bind=engine)
    RTKReliability.__table__.create(bind=engine)
    RTKRequirement.__table__.create(bind=engine)
    RTKRevision.__table__.create(bind=engine)
    RTKRPN.__table__.create(bind=engine)
    RTKSimilarItem.__table__.create(bind=engine)
    RTKSoftware.__table__.create(bind=engine)
    RTKSoftwareDevelopment.__table__.create(bind=engine)
    RTKSoftwareReview.__table__.create(bind=engine)
    RTKSoftwareTest.__table__.create(bind=engine)
    RTKStakeholder.__table__.create(bind=engine)
    RTKSurvival.__table__.create(bind=engine)
    RTKSurvivalData.__table__.create(bind=engine)
    RTKTest.__table__.create(bind=engine)
    RTKTestMethod.__table__.create(bind=engine)
    RTKUnits.__table__.create(bind=engine)
    RTKValidation.__table__.create(bind=engine)

    # Add an entry for the Program Information.
    _record = RTKProgramInfo()
    session.add(_record)

    _revision = RTKRevision()
    session.add(_revision)
    session.commit()

    _mission = RTKMission()
    _mission.revision_id = _revision.revision_id
    session.add(_mission)
    session.commit()

    _phase = RTKMissionPhase()
    _phase.mission_id = _mission.mission_id
    session.add(_phase)
    session.commit()

    _record = RTKEnvironment()
    _record.phase_id = _phase.phase_id
    session.add(_record)

    _system = RTKHardware()
    _system.revision_id = _revision.revision_id
    _system.description = "Test System"
    _system.ref_des = "S1"
    _system.comp_ref_des = "S1"
    session.add(_system)
    session.commit()

    _record = RTKReliability()
    _record.hardware_id = _system.hardware_id
    session.add(_record)
    _record = RTKMilHdbkF()
    _record.hardware_id = _system.hardware_id
    session.add(_record)
    _record = RTKNSWC()
    _record.hardware_id = _system.hardware_id
    session.add(_record)
    _record = RTKDesignElectric()
    _record.hardware_id = _system.hardware_id
    session.add(_record)
    _record = RTKDesignMechanic()
    _record.hardware_id = _system.hardware_id
    session.add(_record)
    _record = RTKAllocation()
    _record.revision_id = _revision.revision_id
    _record.hardware_id = _system.hardware_id
    _record.parent_id = 0
    session.add(_record)

    _record = RTKProgramStatus()
    _record.revision_id = _revision.revision_id
    session.add(_record)

    session.commit()

    return None


def do_create_test_database(database):
    """
    Create a new RTK Program test database.

    :param str database: the RFC1738 URL path to the database to connect
                         with.
    :return: False if successful or True if an error occurs.
    :rtype: bool
    """
    from rtk.dao import (
        RTKAction, RTKAllocation, RTKCause, RTKControl, RTKDesignElectric,
        RTKDesignMechanic, RTKEnvironment, RTKFailureDefinition, RTKFunction,
        RTKGrowthTest, RTKHardware, RTKHazardAnalysis, RTKIncident,
        RTKIncidentAction, RTKIncidentDetail, RTKLoadHistory, RTKMatrix,
        RTKMechanism, RTKMilHdbkF, RTKMission, RTKMissionPhase, RTKMode,
        RTKNSWC, RTKOpLoad, RTKOpStress, RTKProgramInfo, RTKProgramStatus,
        RTKReliability, RTKRequirement, RTKRevision, RTKRPN, RTKSimilarItem,
        RTKSoftware, RTKSoftwareDevelopment, RTKSoftwareReview,
        RTKSoftwareTest, RTKStakeholder, RTKSurvival, RTKSurvivalData, RTKTest,
        RTKTestMethod, RTKUnits, RTKValidation)

    # Create and populate the RTK Program test database.
    engine = create_engine(database, echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the RTK Program database.
    RTKAction.__table__.create(bind=engine)
    RTKAllocation.__table__.create(bind=engine)
    RTKCause.__table__.create(bind=engine)
    RTKControl.__table__.create(bind=engine)
    RTKDesignElectric.__table__.create(bind=engine)
    RTKDesignMechanic.__table__.create(bind=engine)
    RTKEnvironment.__table__.create(bind=engine)
    RTKFailureDefinition.__table__.create(bind=engine)
    RTKFunction.__table__.create(bind=engine)
    RTKGrowthTest.__table__.create(bind=engine)
    RTKHardware.__table__.create(bind=engine)
    RTKHazardAnalysis.__table__.create(bind=engine)
    RTKIncident.__table__.create(bind=engine)
    RTKIncidentAction.__table__.create(bind=engine)
    RTKIncidentDetail.__table__.create(bind=engine)
    RTKLoadHistory.__table__.create(bind=engine)
    RTKMatrix.__table__.create(bind=engine)
    RTKMechanism.__table__.create(bind=engine)
    RTKMilHdbkF.__table__.create(bind=engine)
    RTKMission.__table__.create(bind=engine)
    RTKMissionPhase.__table__.create(bind=engine)
    RTKMode.__table__.create(bind=engine)
    RTKNSWC.__table__.create(bind=engine)
    RTKOpLoad.__table__.create(bind=engine)
    RTKOpStress.__table__.create(bind=engine)
    RTKProgramInfo.__table__.create(bind=engine)
    RTKProgramStatus.__table__.create(bind=engine)
    RTKReliability.__table__.create(bind=engine)
    RTKRequirement.__table__.create(bind=engine)
    RTKRevision.__table__.create(bind=engine)
    RTKRPN.__table__.create(bind=engine)
    RTKSimilarItem.__table__.create(bind=engine)
    RTKSoftware.__table__.create(bind=engine)
    RTKSoftwareDevelopment.__table__.create(bind=engine)
    RTKSoftwareReview.__table__.create(bind=engine)
    RTKSoftwareTest.__table__.create(bind=engine)
    RTKStakeholder.__table__.create(bind=engine)
    RTKSurvival.__table__.create(bind=engine)
    RTKSurvivalData.__table__.create(bind=engine)
    RTKTest.__table__.create(bind=engine)
    RTKTestMethod.__table__.create(bind=engine)
    RTKUnits.__table__.create(bind=engine)
    RTKValidation.__table__.create(bind=engine)

    _program_info = RTKProgramInfo()
    _program_info.revision_prefix = "REV"
    _program_info.revision_next_id = 0
    session.add(_program_info)

    _revision = RTKRevision()
    _revision.revision_id = 1
    _revision.name = 'Test Revision'
    session.add(_revision)
    session.commit()

    _definition = RTKFailureDefinition()
    _definition.revision_id = _revision.revision_id
    _definition.definition = 'Failure Definition'

    _mission = RTKMission()
    _mission.revision_id = _revision.revision_id
    _mission.mission_id = 1
    _mission.description = "Test Mission"
    session.add(_definition)
    session.add(_mission)
    session.commit()

    _phase = RTKMissionPhase()
    _phase.mission_id = _mission.mission_id
    _phase.phase_id = 1
    _phase.description = "Test Mission Phase 1"
    session.add(_phase)
    session.commit()

    _environment = RTKEnvironment()
    _environment.phase_id = _phase.phase_id
    session.add(_environment)

    _program_status = RTKProgramStatus()
    _program_status.revision_id = _revision.revision_id
    session.add(_program_status)

    _dic_rows = {}
    for i in [1, 2, 3]:
        _function = RTKFunction()
        _function.revision_id = _revision.revision_id
        _function.function_code = "FUNC-000{0:d}".format(i)
        session.add(_function)
        session.commit()

        _mode = RTKMode()
        _mode.function_id = _function.function_id
        _mode.hardware_id = -1
        _mode.description = (
        "Test Functional Failure Mode #{0:d}").format(i)
        session.add(_mode)
        session.commit()

        _cause = RTKCause()
        _cause.mode_id = _mode.mode_id
        _cause.mechanism_id = -1
        _cause.description = ("Test Functional FMEA Cause "
                  "#{0:d} for Mode ID {1:d}").format(
                      i, _mode.mode_id)
        session.add(_cause)
        session.commit()

        _control = RTKControl()
        _control.cause_id = _cause.cause_id
        _control.description = (
        "Test Functional FMEA Control #{0:d} for Cause ID {1:d}"
        ).format(i, _cause.cause_id)
        _action = RTKAction()
        _action.cause_id = _cause.cause_id
        _action.action_recommended = (
        "Test Functional FMEA Recommended "
        "Action #{0:d} for Cause ID {1:d}").format(i, _cause.cause_id)
        session.add(_control)
        session.add(_action)
        _dic_rows[i] = _function.function_id
        session.commit()

    _requirement = RTKRequirement()
    _requirement.revision_id = _revision.revision_id
    _requirement.requirement_code = 'REL-0001'
    _stakeholder = RTKStakeholder()
    _stakeholder.revision_id = _revision.revision_id
    _stakeholder.description = 'Test Stakeholder Input'
    session.add(_requirement)
    session.add(_stakeholder)
    session.commit()

    _system = RTKHardware()
    _system.revision_id = _revision.revision_id
    _system.hardware_id = 1
    _system.description = "Test System"
    _system.ref_des = "S1"
    _system.comp_ref_des = "S1"
    session.add(_system)
    session.commit()

    _reliability = RTKReliability()
    _reliability.hardware_id = _system.hardware_id
    _mil_hdbk_217 = RTKMilHdbkF()
    _mil_hdbk_217.hardware_id = _system.hardware_id
    _nswc = RTKNSWC()
    _nswc.hardware_id = _system.hardware_id
    _design_electric = RTKDesignElectric()
    _design_electric.hardware_id = _system.hardware_id
    _design_mechanic = RTKDesignMechanic()
    _design_mechanic.hardware_id = _system.hardware_id
    _allocation = RTKAllocation()
    _allocation.revision_id = _revision.revision_id
    _allocation.hardware_id = _system.hardware_id
    _allocation.parent_id = 0
    _similaritem = RTKSimilarItem()
    _similaritem.revision_id = _revision.revision_id
    _similaritem.hardware_id = _system.hardware_id
    _similaritem.parent_id = 0
    _hazardanalysis = RTKHazardAnalysis()
    _hazardanalysis.revision_id = _revision.revision_id
    _hazardanalysis.hardware_id = _system.hardware_id
    _mode = RTKMode()
    _mode.function_id = -1
    _mode.hardware_id = _system.hardware_id
    _mode.description = 'System Test Failure Mode'
    session.add(_reliability)
    session.add(_mil_hdbk_217)
    session.add(_nswc)
    session.add(_design_electric)
    session.add(_design_mechanic)
    session.add(_allocation)
    session.add(_similaritem)
    session.add(_hazardanalysis)
    session.add(_mode)
    session.commit()

    # Build a Hardware FMEA for the system.
    _mechanism = RTKMechanism()
    _mechanism.mode_id = _mode.mode_id
    _mechanism.description = 'Test Failure Mechanism #1 for Mode ID {0:d}'.format(
        _mode.mode_id)
    session.add(_mechanism)
    session.commit()
    _cause = RTKCause()
    _cause.mode_id = _mode.mode_id
    _cause.mechanism_id = _mechanism.mechanism_id
    _cause.description = 'Test Failure Cause #1 for Mechanism ID {0:d}'.format(
        _mechanism.mechanism_id)
    session.add(_cause)
    session.commit()
    _control = RTKControl()
    _control.cause_id = _cause.cause_id
    _control.description = 'Test FMEA Control #1 for Cause ID {0:d}'.format(
        _cause.cause_id)
    _action = RTKAction()
    _action.cause_id = _cause.cause_id
    _action.action_recommended = 'Test FMEA Recommended Action #1 for Cause ID {0:d}'.format(
        _cause.cause_id)

    # Build the PoF for the system.
    _opload = RTKOpLoad()
    _opload.mechanism_id = _mechanism.mechanism_id
    _opload.description = 'Test Operating Load'
    session.add(_control)
    session.add(_action)
    session.add(_opload)
    session.commit()
    _opstress = RTKOpStress()
    _opstress.load_id = _opload.load_id
    _opstress.description = 'Test Operating Stress'
    session.add(_opstress)
    session.commit()
    _testmethod = RTKTestMethod()
    _testmethod.stress_id = _opstress.stress_id
    _testmethod.description = 'Test Test Method'
    session.add(_testmethod)

    # Create a dictionary to use for creating X_hrdwr and hrdwr_X matrices.
    # Key is row or column ID; value is row item or column item ID.
    _dic_cols = {1: _system.hardware_id}
    for i in [1, 2, 3, 4]:
        _subsystem = RTKHardware()
        _subsystem.revision_id = _revision.revision_id
        _subsystem.hardware_id = i + 1
        _subsystem.parent_id = _system.hardware_id
        _subsystem.ref_des = "SS{0:d}".format(i)
        _subsystem.comp_ref_des = "S1:SS{0:d}".format(i)
        _subsystem.description = "Test Sub-System {0:d}".format(i)
        session.add(_subsystem)
        session.commit()
        _dic_cols[i + 1] = _subsystem.hardware_id

        if i == 1:
            for j in [5, 6, 7]:
                _assembly = RTKHardware()
                _assembly.revision_id = _revision.revision_id
                _assembly.hardware_id = j + 1
                _assembly.parent_id = _subsystem.hardware_id
                _assembly.ref_des = "A{0:d}".format(j - 4)
                _assembly.comp_ref_des = "S1:SS1:A{0:d}".format(j - 4)
                _assembly.description = "Test Assembly {0:d}".format(j - 4)
                session.add(_assembly)
                _dic_cols[j + 1] = _assembly.hardware_id
    session.commit()

    for i in [1, 2, 3, 4]:
        _allocation = RTKAllocation()
        _allocation.revision_id = _revision.revision_id
        _allocation.hardware_id = i + 1
        _allocation.parent_id = _system.hardware_id
        _similaritem = RTKSimilarItem()
        _similaritem.revision_id = _revision.revision_id
        _similaritem.hardware_id = i + 1
        _similaritem.parent_id = _system.hardware_id
        _hazardanalysis = RTKHazardAnalysis()
        _hazardanalysis.revision_id = _revision.revision_id
        _hazardanalysis.hardware_id = i + 1
        _reliability = RTKReliability()
        _reliability.hardware_id = i + 1
        _mil_hdbk_217 = RTKMilHdbkF()
        _mil_hdbk_217.hardware_id = i + 1
        _nswc = RTKNSWC()
        _nswc.hardware_id = i + 1
        _design_electric = RTKDesignElectric()
        _design_electric.hardware_id = i + 1
        _design_mechanic = RTKDesignMechanic()
        _design_mechanic.hardware_id = i + 1
        session.add(_allocation)
        session.add(_similaritem)
        session.add(_hazardanalysis)
        session.add(_reliability)
        session.add(_mil_hdbk_217)
        session.add(_nswc)
        session.add(_design_electric)
        session.add(_design_mechanic)

    for i in [5, 6, 7]:
        _allocation = RTKAllocation()
        _allocation.revision_id = _revision.revision_id
        _allocation.hardware_id = i + 1
        _allocation.parent_id = 2
        _similaritem = RTKSimilarItem()
        _similaritem.revision_id = _revision.revision_id
        _similaritem.hardware_id = i + 1
        _similaritem.parent_id = 2
        _hazardanalysis = RTKHazardAnalysis()
        _hazardanalysis.revision_id = _revision.revision_id
        _hazardanalysis.hardware_id = i + 1

        _reliability = RTKReliability()
        _reliability.hardware_id = i + 1
        _mil_hdbk_217 = RTKMilHdbkF()
        _mil_hdbk_217.hardware_id = i + 1
        _nswc = RTKNSWC()
        _nswc.hardware_id = i + 1
        _design_electric = RTKDesignElectric()
        _design_electric.hardware_id = i + 1
        _design_mechanic = RTKDesignMechanic()
        _design_mechanic.hardware_id = i + 1
        session.add(_allocation)
        session.add(_similaritem)
        session.add(_hazardanalysis)
        session.add(_reliability)
        session.add(_mil_hdbk_217)
        session.add(_nswc)
        session.add(_design_electric)
        session.add(_design_mechanic)
    session.commit()

    for _ckey in _dic_cols:
        _matrix = RTKMatrix()
        _matrix.revision_id = _revision.revision_id
        _matrix.matrix_id = 2
        _matrix.matrix_type = 'rqrmnt_hrdwr'
        _matrix.column_id = _ckey
        _matrix.column_item_id = _dic_cols[_ckey]
        _matrix.row_id = _ckey
        _matrix.row_item_id = 1
        session.add(_matrix)
        for _rkey in _dic_rows:
            _matrix = RTKMatrix()
            _matrix.revision_id = _revision.revision_id
            _matrix.matrix_id = 1
            _matrix.matrix_type = 'fnctn_hrdwr'
            _matrix.column_id = _ckey
            _matrix.column_item_id = _dic_cols[_ckey]
            _matrix.row_id = _ckey
            _matrix.row_item_id = _dic_rows[_rkey]
            session.add(_matrix)
    session.commit()

    _validation = RTKValidation()
    _validation.revision_id = _revision.revision_id
    _validation.description = 'Test Validation'
    session.add(_validation)
    session.commit()

    for _ckey in _dic_cols:
        _matrix = RTKMatrix()
        _matrix.revision_id = _revision.revision_id
        _matrix.matrix_id = 3
        _matrix.matrix_type = 'hrdwr_rqrmnt'
        _matrix.column_id = 1
        _matrix.column_item_id = 1
        _matrix.row_id = _ckey
        _matrix.row_item_id = _dic_cols[_ckey]
        session.add(_matrix)
        _matrix = RTKMatrix()
        _matrix.revision_id = _revision.revision_id
        _matrix.matrix_id = 4
        _matrix.matrix_type = 'hrdwr_vldtn'
        _matrix.column_id = 1
        _matrix.column_item_id = 1
        _matrix.row_id = _ckey
        _matrix.row_item_id = _dic_cols[_ckey]
        session.add(_matrix)
    session.commit()

    return False
