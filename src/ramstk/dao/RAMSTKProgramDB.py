# -*- coding: utf-8 -*-
#
#       ramstk.dao.RAMSTKProgramDB.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKProgramDB File."""

# Import third party modules.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

RAMSTK_BASE = declarative_base()


def do_make_tables(engine):
    """Make all the tables in the RAMSTK Program database."""
    from ramstk.dao import (
        RAMSTKAction, RAMSTKAllocation, RAMSTKCause, RAMSTKControl,
        RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKEnvironment,
        RAMSTKFailureDefinition, RAMSTKFunction, RAMSTKGrowthTest,
        RAMSTKHardware, RAMSTKHazardAnalysis, RAMSTKIncident,
        RAMSTKIncidentAction, RAMSTKIncidentDetail, RAMSTKLoadHistory,
        RAMSTKMatrix, RAMSTKMechanism, RAMSTKMilHdbkF, RAMSTKMission,
        RAMSTKMissionPhase, RAMSTKMode, RAMSTKNSWC, RAMSTKOpLoad,
        RAMSTKOpStress, RAMSTKProgramInfo, RAMSTKProgramStatus,
        RAMSTKReliability, RAMSTKRequirement, RAMSTKRevision,
        RAMSTKSimilarItem, RAMSTKSoftware, RAMSTKSoftwareDevelopment,
        RAMSTKSoftwareReview, RAMSTKSoftwareTest, RAMSTKStakeholder,
        RAMSTKSurvival, RAMSTKSurvivalData, RAMSTKTest, RAMSTKTestMethod,
        RAMSTKUnits, RAMSTKValidation)

    RAMSTKAction.__table__.create(bind=engine)
    RAMSTKAllocation.__table__.create(bind=engine)
    RAMSTKCause.__table__.create(bind=engine)
    RAMSTKControl.__table__.create(bind=engine)
    RAMSTKDesignElectric.__table__.create(bind=engine)
    RAMSTKDesignMechanic.__table__.create(bind=engine)
    RAMSTKEnvironment.__table__.create(bind=engine)
    RAMSTKFailureDefinition.__table__.create(bind=engine)
    RAMSTKFunction.__table__.create(bind=engine)
    RAMSTKGrowthTest.__table__.create(bind=engine)
    RAMSTKHardware.__table__.create(bind=engine)
    RAMSTKHazardAnalysis.__table__.create(bind=engine)
    RAMSTKIncident.__table__.create(bind=engine)
    RAMSTKIncidentAction.__table__.create(bind=engine)
    RAMSTKIncidentDetail.__table__.create(bind=engine)
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
    RAMSTKSoftware.__table__.create(bind=engine)
    RAMSTKSoftwareDevelopment.__table__.create(bind=engine)
    RAMSTKSoftwareReview.__table__.create(bind=engine)
    RAMSTKSoftwareTest.__table__.create(bind=engine)
    RAMSTKStakeholder.__table__.create(bind=engine)
    RAMSTKSurvival.__table__.create(bind=engine)
    RAMSTKSurvivalData.__table__.create(bind=engine)
    RAMSTKTest.__table__.create(bind=engine)
    RAMSTKTestMethod.__table__.create(bind=engine)
    RAMSTKUnits.__table__.create(bind=engine)
    RAMSTKValidation.__table__.create(bind=engine)

    return None


def create_program_db(**kwargs):
    """Create and populate a RAMSTK Program database."""
    from ramstk.dao import (RAMSTKMission, RAMSTKProgramInfo,
                            RAMSTKProgramStatus, RAMSTKRevision)

    uri = kwargs['database']

    # Create and populate the RAMSTK Program test database.
    engine = create_engine(uri, echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the RAMSTK Program database.
    do_make_tables(engine)

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

    return None


def do_create_test_database(database):
    """
    Create a new RAMSTK Program test database.

    :param str database: the RFC1738 URL path to the database to connect
                         with.
    :return: False if successful or True if an error occurs.
    :rtype: bool
    """
    from ramstk.dao import (
        RAMSTKAction, RAMSTKAllocation, RAMSTKCause, RAMSTKControl,
        RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKEnvironment,
        RAMSTKFailureDefinition, RAMSTKFunction, RAMSTKGrowthTest,
        RAMSTKHardware, RAMSTKHazardAnalysis, RAMSTKIncident,
        RAMSTKIncidentAction, RAMSTKIncidentDetail, RAMSTKLoadHistory,
        RAMSTKMatrix, RAMSTKMechanism, RAMSTKMilHdbkF, RAMSTKMission,
        RAMSTKMissionPhase, RAMSTKMode, RAMSTKNSWC, RAMSTKOpLoad,
        RAMSTKOpStress, RAMSTKProgramInfo, RAMSTKProgramStatus,
        RAMSTKReliability, RAMSTKRequirement, RAMSTKRevision,
        RAMSTKSimilarItem, RAMSTKSoftware, RAMSTKSoftwareDevelopment,
        RAMSTKSoftwareReview, RAMSTKSoftwareTest, RAMSTKStakeholder,
        RAMSTKSurvival, RAMSTKSurvivalData, RAMSTKTest, RAMSTKTestMethod,
        RAMSTKUnits, RAMSTKValidation)

    # Create and populate the RAMSTK Program test database.
    engine = create_engine(database, echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the RAMSTK Program database.
    do_make_tables(engine)

    _program_info = RAMSTKProgramInfo()
    _program_info.revision_prefix = "REV"
    _program_info.revision_next_id = 0
    session.add(_program_info)

    _revision = RAMSTKRevision()
    _revision.revision_id = 1
    _revision.name = 'Test Revision'
    session.add(_revision)
    session.commit()

    _definition = RAMSTKFailureDefinition()
    _definition.revision_id = _revision.revision_id
    _definition.definition = b'Failure Definition'

    _mission = RAMSTKMission()
    _mission.revision_id = _revision.revision_id
    _mission.mission_id = 1
    _mission.description = b'Test Mission'
    session.add(_definition)
    session.add(_mission)
    session.commit()

    _phase = RAMSTKMissionPhase()
    _phase.mission_id = _mission.mission_id
    _phase.phase_id = 1
    _phase.description = b'Test Mission Phase 1'
    session.add(_phase)
    session.commit()

    _environment = RAMSTKEnvironment()
    _environment.phase_id = _phase.phase_id
    session.add(_environment)

    _program_status = RAMSTKProgramStatus()
    _program_status.revision_id = _revision.revision_id
    session.add(_program_status)

    _dic_rows = {}
    for i in [1, 2, 3]:
        _function = RAMSTKFunction()
        _function.revision_id = _revision.revision_id
        _function.function_code = "FUNC-000{0:d}".format(i)
        session.add(_function)
        session.commit()

        _mode = RAMSTKMode()
        _mode.function_id = _function.function_id
        _mode.hardware_id = -1
        _mode.description = ("Test Functional Failure Mode #{0:d}").format(i)
        session.add(_mode)
        session.commit()

        _cause = RAMSTKCause()
        _cause.mode_id = _mode.mode_id
        _cause.mechanism_id = -1
        _cause.description = ("Test Functional FMEA Cause "
                              "#{0:d} for Mode ID {1:d}").format(
                                  i, _mode.mode_id)
        session.add(_cause)
        session.commit()

        _control = RAMSTKControl()
        _control.cause_id = _cause.cause_id
        _control.description = (
            "Test Functional FMEA Control #{0:d} for Cause ID {1:d}").format(
                i, _cause.cause_id)
        _action = RAMSTKAction()
        _action.cause_id = _cause.cause_id
        _action.action_recommended = bytes((
            "Test Functional FMEA Recommended "
            "Action #{0:d} for Cause ID {1:d}").format(i, _cause.cause_id), 'utf-8')
        session.add(_control)
        session.add(_action)
        _dic_rows[i] = _function.function_id
        session.commit()

    _requirement = RAMSTKRequirement()
    _requirement.revision_id = _revision.revision_id
    _requirement.requirement_code = 'REL-0001'
    _stakeholder = RAMSTKStakeholder()
    _stakeholder.revision_id = _revision.revision_id
    _stakeholder.description = b'Test Stakeholder Input'
    session.add(_requirement)
    session.add(_stakeholder)
    session.commit()

    _system = RAMSTKHardware()
    _system.revision_id = _revision.revision_id
    _system.hardware_id = 1
    _system.description = "Test System"
    _system.ref_des = "S1"
    _system.comp_ref_des = "S1"
    session.add(_system)
    session.commit()

    _reliability = RAMSTKReliability()
    _reliability.hardware_id = _system.hardware_id
    _mil_hdbk_217 = RAMSTKMilHdbkF()
    _mil_hdbk_217.hardware_id = _system.hardware_id
    _nswc = RAMSTKNSWC()
    _nswc.hardware_id = _system.hardware_id
    _design_electric = RAMSTKDesignElectric()
    _design_electric.hardware_id = _system.hardware_id
    _design_mechanic = RAMSTKDesignMechanic()
    _design_mechanic.hardware_id = _system.hardware_id
    _allocation = RAMSTKAllocation()
    _allocation.revision_id = _revision.revision_id
    _allocation.hardware_id = _system.hardware_id
    _allocation.parent_id = 0
    _similaritem = RAMSTKSimilarItem()
    _similaritem.revision_id = _revision.revision_id
    _similaritem.hardware_id = _system.hardware_id
    _similaritem.parent_id = 0
    _hazardanalysis = RAMSTKHazardAnalysis()
    _hazardanalysis.revision_id = _revision.revision_id
    _hazardanalysis.hardware_id = _system.hardware_id
    _mode = RAMSTKMode()
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
    _mechanism = RAMSTKMechanism()
    _mechanism.mode_id = _mode.mode_id
    _mechanism.description = 'Test Failure Mechanism #1 for Mode ID {0:d}'.format(
        _mode.mode_id)
    session.add(_mechanism)
    session.commit()
    _cause = RAMSTKCause()
    _cause.mode_id = _mode.mode_id
    _cause.mechanism_id = _mechanism.mechanism_id
    _cause.description = 'Test Failure Cause #1 for Mechanism ID {0:d}'.format(
        _mechanism.mechanism_id)
    session.add(_cause)
    session.commit()
    _control = RAMSTKControl()
    _control.cause_id = _cause.cause_id
    _control.description = 'Test FMEA Control #1 for Cause ID {0:d}'.format(
        _cause.cause_id)
    _action = RAMSTKAction()
    _action.cause_id = _cause.cause_id
    _action.action_recommended = bytes('Test FMEA Recommended Action #1 for Cause ID {0:d}'.format(
        _cause.cause_id), 'utf-8')

    # Build the PoF for the system.
    _opload = RAMSTKOpLoad()
    _opload.mechanism_id = _mechanism.mechanism_id
    _opload.description = 'Test Operating Load'
    session.add(_control)
    session.add(_action)
    session.add(_opload)
    session.commit()
    _opstress = RAMSTKOpStress()
    _opstress.load_id = _opload.load_id
    _opstress.description = 'Test Operating Stress'
    session.add(_opstress)
    _testmethod = RAMSTKTestMethod()
    _testmethod.load_id = _opload.load_id
    _testmethod.description = 'Test Test Method'
    session.add(_testmethod)
    session.commit()

    # Create a dictionary to use for creating X_hrdwr and hrdwr_X matrices.
    # Key is row or column ID; value is row item or column item ID.
    _dic_cols = {1: _system.hardware_id}
    for i in [1, 2, 3, 4]:
        _subsystem = RAMSTKHardware()
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
                _assembly = RAMSTKHardware()
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
        _allocation = RAMSTKAllocation()
        _allocation.revision_id = _revision.revision_id
        _allocation.hardware_id = i + 1
        _allocation.parent_id = _system.hardware_id
        _similaritem = RAMSTKSimilarItem()
        _similaritem.revision_id = _revision.revision_id
        _similaritem.hardware_id = i + 1
        _similaritem.parent_id = _system.hardware_id
        _hazardanalysis = RAMSTKHazardAnalysis()
        _hazardanalysis.revision_id = _revision.revision_id
        _hazardanalysis.hardware_id = i + 1
        _reliability = RAMSTKReliability()
        _reliability.hardware_id = i + 1
        _mil_hdbk_217 = RAMSTKMilHdbkF()
        _mil_hdbk_217.hardware_id = i + 1
        _nswc = RAMSTKNSWC()
        _nswc.hardware_id = i + 1
        _design_electric = RAMSTKDesignElectric()
        _design_electric.hardware_id = i + 1
        _design_mechanic = RAMSTKDesignMechanic()
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
        _allocation = RAMSTKAllocation()
        _allocation.revision_id = _revision.revision_id
        _allocation.hardware_id = i + 1
        _allocation.parent_id = 2
        _similaritem = RAMSTKSimilarItem()
        _similaritem.revision_id = _revision.revision_id
        _similaritem.hardware_id = i + 1
        _similaritem.parent_id = 2
        _hazardanalysis = RAMSTKHazardAnalysis()
        _hazardanalysis.revision_id = _revision.revision_id
        _hazardanalysis.hardware_id = i + 1

        _reliability = RAMSTKReliability()
        _reliability.hardware_id = i + 1
        _mil_hdbk_217 = RAMSTKMilHdbkF()
        _mil_hdbk_217.hardware_id = i + 1
        _nswc = RAMSTKNSWC()
        _nswc.hardware_id = i + 1
        _design_electric = RAMSTKDesignElectric()
        _design_electric.hardware_id = i + 1
        _design_mechanic = RAMSTKDesignMechanic()
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
        _matrix = RAMSTKMatrix()
        _matrix.revision_id = _revision.revision_id
        _matrix.matrix_id = 2
        _matrix.matrix_type = 'rqrmnt_hrdwr'
        _matrix.column_id = _ckey
        _matrix.column_item_id = _dic_cols[_ckey]
        _matrix.row_id = _ckey
        _matrix.row_item_id = 1
        session.add(_matrix)
        for _rkey in _dic_rows:
            _matrix = RAMSTKMatrix()
            _matrix.revision_id = _revision.revision_id
            _matrix.matrix_id = 1
            _matrix.matrix_type = 'fnctn_hrdwr'
            _matrix.column_id = _ckey
            _matrix.column_item_id = _dic_cols[_ckey]
            _matrix.row_id = _ckey
            _matrix.row_item_id = _dic_rows[_rkey]
            session.add(_matrix)
    session.commit()

    _validation = RAMSTKValidation()
    _validation.revision_id = _revision.revision_id
    _validation.description = b'Test Validation'
    session.add(_validation)
    session.commit()

    for _ckey in _dic_cols:
        _matrix = RAMSTKMatrix()
        _matrix.revision_id = _revision.revision_id
        _matrix.matrix_id = 3
        _matrix.matrix_type = 'hrdwr_rqrmnt'
        _matrix.column_id = 1
        _matrix.column_item_id = 1
        _matrix.row_id = _ckey
        _matrix.row_item_id = _dic_cols[_ckey]
        session.add(_matrix)
        _matrix = RAMSTKMatrix()
        _matrix.revision_id = _revision.revision_id
        _matrix.matrix_id = 4
        _matrix.matrix_type = 'hrdwr_vldtn'
        _matrix.column_id = 1
        _matrix.column_item_id = 1
        _matrix.row_id = _ckey
        _matrix.row_item_id = _dic_cols[_ckey]
        session.add(_matrix)
        _matrix = RAMSTKMatrix()
        _matrix.revision_id = _revision.revision_id
        _matrix.matrix_id = 5
        _matrix.matrix_type = 'vldtn_hrdwr'
        _matrix.column_id = _ckey
        _matrix.column_item_id = _dic_cols[_ckey]
        _matrix.row_id = 1
        _matrix.row_item_id = 1
        session.add(_matrix)
    session.commit()

    return False
