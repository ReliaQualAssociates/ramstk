# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.programdb_mission_phase_record.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMissionPhase Record Model."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKMissionPhaseRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent ramstk_mission_phase in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mission. This table
    shares a One-to-Many relationship with ramstk_environment.
    """

    __defaults__ = {
        "description": "",
        "name": "",
        "phase_start": 0.0,
        "phase_end": 0.0,
    }
    __tablename__ = "ramstk_mission_phase"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fld_revision_id", "fld_mission_id"],
            [
                "ramstk_mission.fld_revision_id",
                "ramstk_mission.fld_mission_id",
            ],
        ),
        {"extend_existing": True},
    )

    revision_id = Column(
        "fld_revision_id",
        Integer,
        primary_key=True,
        nullable=False,
    )
    mission_id = Column(
        "fld_mission_id",
        Integer,
        primary_key=True,
        nullable=False,
    )
    mission_phase_id = Column(
        "fld_mission_phase_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    description = Column("fld_description", String, default=__defaults__["description"])
    name = Column("fld_name", String(256), default=__defaults__["name"])
    phase_start = Column("fld_phase_start", Float, default=__defaults__["phase_start"])
    phase_end = Column("fld_phase_end", Float, default=__defaults__["phase_end"])

    # Define the relationships to other tables in the RAMSTK Program database.
    mission: relationship = relationship(
        "RAMSTKMissionRecord",
        back_populates="phase",
    )
    environment: relationship = relationship(
        "RAMSTKEnvironmentRecord",
        back_populates="phase",
        cascade="all,delete",
    )

    def get_attributes(self):
        """Retrieve current values of the Mission Phase data model attributes.

        :return: value of instance attributes
        :rtype: tuple
        """
        return {
            "mission_id": self.mission_id,
            "mission_phase_id": self.mission_phase_id,
            "description": self.description,
            "name": self.name,
            "phase_start": self.phase_start,
            "phase_end": self.phase_end,
        }
