# -*- coding: utf-8 -*-
#
#       ramstk.db.program.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Program Database Module."""

# Third Party Imports
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session

# RAMSTK Package Imports
from ramstk.models import (
    RAMSTKAllocationRecord,
    RAMSTKDesignElectricRecord,
    RAMSTKDesignMechanicRecord,
    RAMSTKEnvironmentRecord,
    RAMSTKFailureDefinitionRecord,
    RAMSTKHardwareRecord,
    RAMSTKMilHdbk217FRecord,
    RAMSTKMissionPhaseRecord,
    RAMSTKMissionRecord,
    RAMSTKNSWCRecord,
    RAMSTKReliabilityRecord,
    RAMSTKRevisionRecord,
    RAMSTKSimilarItemRecord,
)
from ramstk.models.programdb import (
    RAMSTKAction,
    RAMSTKCause,
    RAMSTKControl,
    RAMSTKFunction,
    RAMSTKHazardAnalysis,
    RAMSTKMechanism,
    RAMSTKMode,
    RAMSTKOpLoad,
    RAMSTKOpStress,
    RAMSTKProgramInfo,
    RAMSTKProgramStatus,
    RAMSTKRequirement,
    RAMSTKStakeholder,
    RAMSTKTestMethod,
    RAMSTKValidation,
)


def do_make_programdb_tables(engine: Engine) -> None:
    """Create all the tables in the RAMSTK Program database.

    :param engine: the SQLAlchemy database engine to use to create the program
        database tables.
    :type engine: :class:`sqlalchemy.engine.Engine`
    :return: None
    :rtype: None
    """
    RAMSTKRevisionRecord.__table__.create(bind=engine)
    RAMSTKProgramInfo.__table__.create(bind=engine)
    RAMSTKProgramStatus.__table__.create(bind=engine)
    RAMSTKMissionRecord.__table__.create(bind=engine)
    RAMSTKMissionPhaseRecord.__table__.create(bind=engine)
    RAMSTKEnvironmentRecord.__table__.create(bind=engine)
    RAMSTKFailureDefinitionRecord.__table__.create(bind=engine)

    RAMSTKFunction.__table__.create(bind=engine)
    RAMSTKHazardAnalysis.__table__.create(bind=engine)

    RAMSTKRequirement.__table__.create(bind=engine)
    RAMSTKStakeholder.__table__.create(bind=engine)

    RAMSTKHardwareRecord.__table__.create(bind=engine)
    RAMSTKAllocationRecord.__table__.create(bind=engine)
    RAMSTKDesignElectricRecord.__table__.create(bind=engine)
    RAMSTKDesignMechanicRecord.__table__.create(bind=engine)
    RAMSTKMilHdbk217FRecord.__table__.create(bind=engine)
    RAMSTKNSWCRecord.__table__.create(bind=engine)
    RAMSTKReliabilityRecord.__table__.create(bind=engine)
    RAMSTKSimilarItemRecord.__table__.create(bind=engine)
    RAMSTKMode.__table__.create(bind=engine)
    RAMSTKMechanism.__table__.create(bind=engine)
    RAMSTKCause.__table__.create(bind=engine)
    RAMSTKAction.__table__.create(bind=engine)
    RAMSTKControl.__table__.create(bind=engine)
    RAMSTKOpLoad.__table__.create(bind=engine)
    RAMSTKOpStress.__table__.create(bind=engine)
    RAMSTKTestMethod.__table__.create(bind=engine)

    RAMSTKValidation.__table__.create(bind=engine)


def do_create_program_db(engine: Engine, session: scoped_session) -> None:
    """Create and initialize a RAMSTK Program database.

    :param engine: the SQLAlchemy Engine connected to the database.
    :type engine: :class:`sqlalchemy.engine.Engine`
    :param session: the SQLAlchemy session to use when creating the database.
    :type session: :class:`sqlalchemy.orm.Session`
    :return: None
    :rtype: None
    """
    do_make_programdb_tables(engine)

    _record = RAMSTKProgramInfo()
    session.add(_record)

    _revision = RAMSTKRevisionRecord()
    session.add(_revision)
    session.commit()

    _mission = RAMSTKMissionRecord()
    _mission.revision_id = _revision.revision_id
    session.add(_mission)
    session.commit()

    _record = RAMSTKProgramStatus()
    _record.revision_id = _revision.revision_id
    session.add(_record)

    session.commit()
