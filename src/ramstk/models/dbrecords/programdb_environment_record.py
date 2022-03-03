# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.programdb_environment_record.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKEnvironment Record Model."""

# Third Party Imports
from sqlalchemy import Column, Float, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKEnvironmentRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent ramstk_environment table in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mission_phase.
    """

    __defaults__ = {
        "name": "Condition Name",
        "units": "Units",
        "minimum": 0.0,
        "maximum": 0.0,
        "mean": 0.0,
        "variance": 0.0,
        "ramp_rate": 0.0,
        "low_dwell_time": 0.0,
        "high_dwell_time": 0.0,
    }
    __tablename__ = "ramstk_environment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fld_revision_id", "fld_mission_id", "fld_mission_phase_id"],
            [
                "ramstk_mission_phase.fld_revision_id",
                "ramstk_mission_phase.fld_mission_id",
                "ramstk_mission_phase.fld_mission_phase_id",
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
    mission_id = Column("fld_mission_id", Integer, primary_key=True, nullable=False)
    mission_phase_id = Column(
        "fld_mission_phase_id", Integer, primary_key=True, nullable=False
    )
    environment_id = Column(
        "fld_environment_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    name = Column("fld_name", String(256), default=__defaults__["name"])
    units = Column("fld_units", String(128), default=__defaults__["units"])
    minimum = Column("fld_minimum", Float, default=__defaults__["minimum"])
    maximum = Column("fld_maximum", Float, default=__defaults__["maximum"])
    mean = Column("fld_mean", Float, default=__defaults__["mean"])
    variance = Column("fld_variance", Float, default=__defaults__["variance"])
    ramp_rate = Column("fld_ramp_rate", Float, default=__defaults__["ramp_rate"])
    low_dwell_time = Column(
        "fld_low_dwell_time", Float, default=__defaults__["low_dwell_time"]
    )
    high_dwell_time = Column(
        "fld_high_dwell_time", Float, default=__defaults__["high_dwell_time"]
    )

    # Define the relationships to other tables in the RAMSTK Program database.
    phase: relationship = relationship(  # type: ignore
        "RAMSTKMissionPhaseRecord",
        back_populates="environment",
    )

    def get_attributes(self):
        """Retrieve current values of RAMSTKEnvironment data model attributes.

        :return: {mission_phase_id, environment_id, name, units, minimum,
                  maximum, mean, variance, ramp_rate, low_dwell_time,
                  high_dwell_time} pairs.
        :rtype: dict
        """
        return {
            "mission_phase_id": self.mission_phase_id,
            "environment_id": self.environment_id,
            "name": self.name,
            "units": self.units,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "mean": self.mean,
            "variance": self.variance,
            "ramp_rate": self.ramp_rate,
            "low_dwell_time": self.low_dwell_time,
            "high_dwell_time": self.high_dwell_time,
        }
