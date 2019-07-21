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
from sqlalchemy import MetaData, create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKAction, RAMSTKAllocation, RAMSTKCause,
    RAMSTKControl, RAMSTKDesignElectric, RAMSTKDesignMechanic,
    RAMSTKEnvironment, RAMSTKFailureDefinition, RAMSTKFunction,
    RAMSTKHardware, RAMSTKHazardAnalysis, RAMSTKMatrix,
    RAMSTKMechanism, RAMSTKMilHdbkF, RAMSTKMission, RAMSTKMissionPhase,
    RAMSTKMode, RAMSTKReliability, RAMSTKRevision, RAMSTKSimilarItem
)

# RAMSTK Local Imports
from .commondb import (
    RAMSTKRPN, RAMSTKCategory, RAMSTKCondition, RAMSTKFailureMode, RAMSTKGroup,
    RAMSTKHazards, RAMSTKLoadHistory, RAMSTKManufacturer, RAMSTKMeasurement,
    RAMSTKMethod, RAMSTKModel, RAMSTKSiteInfo, RAMSTKStakeholders,
    RAMSTKStatus, RAMSTKSubCategory, RAMSTKType, RAMSTKUser
)
from .programdb import (
    RAMSTKGrowthTest, RAMSTKIncident, RAMSTKIncidentAction,
    RAMSTKIncidentDetail, RAMSTKOpLoad, RAMSTKOpStress, RAMSTKProgramInfo,
    RAMSTKProgramStatus, RAMSTKRequirement, RAMSTKSoftware,
    RAMSTKSoftwareDevelopment, RAMSTKSoftwareReview, RAMSTKSoftwareTest,
    RAMSTKStakeholder, RAMSTKSurvival, RAMSTKSurvivalData, RAMSTKTest,
    RAMSTKTestMethod, RAMSTKUnits, RAMSTKValidation
)
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


# pylint: disable=too-many-statements, too-many-locals
def do_create_test_database(database):
    """
    Create a new RAMSTK Program test database.

    :param str database: the RFC1738 URL path to the database to connect
                         with.
    :return: False if successful or True if an error occurs.
    :rtype: bool
    """
    # Create and populate the RAMSTK Program test database.
    engine = create_engine(database, echo=False)
    session = scoped_session(sessionmaker())

    session.remove()
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    # Create all the tables in the RAMSTK Program database.
    do_make_programdb_tables(engine)

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

        _hazardanalysis = RAMSTKHazardAnalysis()
        _hazardanalysis.revision_id = _revision.revision_id
        _hazardanalysis.function_id = _function.function_id
        session.add(_hazardanalysis)

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
        _action.action_recommended = bytes(
            ("Test Functional FMEA Recommended "
             "Action #{0:d} for Cause ID {1:d}").format(i, _cause.cause_id),
            'utf-8',
        )
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
    session.add(_mode)
    session.commit()

    # Build a Hardware FMEA for the system.
    _mechanism = RAMSTKMechanism()
    _mechanism.mode_id = _mode.mode_id
    _mechanism.description = ('Test Failure Mechanism #1 for Mode ID '
                              '{0:d}').format(_mode.mode_id)
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
    _action.action_recommended = bytes(
        'Test FMEA Recommended Action #1 for Cause ID {0:d}'.format(
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
        _matrix.value = 2
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
        self.RAMSTK_SESSION.close_all()
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
        except IOError:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print("IOError")
            _return = True
        except exc.OperationalError:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print("OperationalError")
            _return = True
        except exc.DBAPIError:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print("DBAPIError")
            _return = True
        except exc.SQLAlchemyError:
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            print("SQLAlchemyError")
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
                else:
                    # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
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
            # ISSUE: See issue #238 at https://github.com/ReliaQualAssociates/ramstk/issues/238
            self.session.rollback()
            _error_code = 1
            _msg = (
                "RAMSTK ERROR: Updating the RAMSTK Program database failed "
                "with error: {0:s}.").format(_error)

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
