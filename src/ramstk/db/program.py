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
from ramstk.models.programdb import (
    RAMSTKNSWC, RAMSTKAction, RAMSTKAllocation, RAMSTKCause, RAMSTKControl,
    RAMSTKDesignElectric, RAMSTKDesignMechanic, RAMSTKEnvironment,
    RAMSTKFailureDefinition, RAMSTKFunction, RAMSTKHardware,
    RAMSTKHazardAnalysis, RAMSTKMechanism, RAMSTKMilHdbkF, RAMSTKMission,
    RAMSTKMissionPhase, RAMSTKMode, RAMSTKOpLoad, RAMSTKOpStress,
    RAMSTKProgramInfo, RAMSTKProgramStatus, RAMSTKReliability,
    RAMSTKRequirement, RAMSTKRevision, RAMSTKSimilarItem,
    RAMSTKStakeholder, RAMSTKTestMethod, RAMSTKValidation
)


def do_make_programdb_tables(engine: Engine) -> None:
    """Create all the tables in the RAMSTK Program database.

    :param engine: the SQLAlchemy database engine to use to create the program
        database tables.
    :type engine: :class:`sqlalchemy.engine.Engine`
    :return: None
    :rtype: None
    """
    RAMSTKRevision.__table__.create(bind=engine)
    RAMSTKProgramInfo.__table__.create(bind=engine)
    RAMSTKProgramStatus.__table__.create(bind=engine)
    RAMSTKMission.__table__.create(bind=engine)
    RAMSTKMissionPhase.__table__.create(bind=engine)
    RAMSTKEnvironment.__table__.create(bind=engine)
    RAMSTKFailureDefinition.__table__.create(bind=engine)

    RAMSTKFunction.__table__.create(bind=engine)
    RAMSTKHazardAnalysis.__table__.create(bind=engine)

    RAMSTKRequirement.__table__.create(bind=engine)
    RAMSTKStakeholder.__table__.create(bind=engine)

    RAMSTKHardware.__table__.create(bind=engine)
    RAMSTKAllocation.__table__.create(bind=engine)
    RAMSTKDesignElectric.__table__.create(bind=engine)
    RAMSTKDesignMechanic.__table__.create(bind=engine)
    RAMSTKMilHdbkF.__table__.create(bind=engine)
    RAMSTKNSWC.__table__.create(bind=engine)
    RAMSTKReliability.__table__.create(bind=engine)
    RAMSTKSimilarItem.__table__.create(bind=engine)
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
