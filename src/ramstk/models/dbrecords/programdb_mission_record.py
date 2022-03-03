# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.programdb_mission_record.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMission Record Model."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKMissionRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent ramstk_mission table in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_revision. This table
    shares a One-to-Many relationship with ramstk_mission_phase.
    """

    __defaults__ = {
        "description": "",
        "mission_time": 0.0,
        "time_units": "hours",
    }
    __tablename__ = "ramstk_mission"
    __table_args__ = (
        UniqueConstraint(
            "fld_revision_id", "fld_mission_id", name="ramstk_mission_ukey"
        ),
        {"extend_existing": True},
    )

    revision_id = Column(
        "fld_revision_id",
        Integer,
        ForeignKey("ramstk_revision.fld_revision_id", ondelete="CASCADE"),
        nullable=False,
    )
    mission_id = Column(
        "fld_mission_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column("fld_description", String, default=__defaults__["description"])
    mission_time = Column(
        "fld_mission_time", Float, default=__defaults__["mission_time"]
    )
    time_units = Column(
        "fld_time_units", String(256), default=__defaults__["time_units"]
    )

    # Define the relationships to other tables in the RAMSTK Program database.
    phase = relationship(  # type: ignore
        "RAMSTKMissionPhaseRecord",
        back_populates="mission",
        cascade="all,delete",
    )

    def get_attributes(self):
        """Retrieve current values of the RAMSTKMission data model attributes.

        :return: (revision_id, mission_id, description, mission_time,
                  time_units)
        :rtype: tuple
        """
        return {
            "revision_id": self.revision_id,
            "mission_id": self.mission_id,
            "description": self.description,
            "mission_time": self.mission_time,
            "time_units": self.time_units,
        }
