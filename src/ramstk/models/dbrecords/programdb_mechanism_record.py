# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.programdb_mechanism_record.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKMechanism Record Model."""

# Third Party Imports
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKMechanismRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent table ramstk_mechanism in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_mode. This table
    shares a One-to-Many relationship with ramstk_cause. This table shares a One-
    to-Many relationship with ramstk_op_load.
    """

    __defaults__ = {
        "description": "",
        "pof_include": 1,
        "rpn": 0,
        "rpn_detection": 10,
        "rpn_detection_new": 10,
        "rpn_new": 0,
        "rpn_occurrence": 10,
        "rpn_occurrence_new": 10,
    }
    __tablename__ = "ramstk_mechanism"
    __table_args__ = (
        ForeignKeyConstraint(
            ["fld_revision_id", "fld_hardware_id", "fld_mode_id"],
            [
                "ramstk_mode.fld_revision_id",
                "ramstk_mode.fld_hardware_id",
                "ramstk_mode.fld_mode_id",
            ],
        ),
        {"extend_existing": True},
    )

    revision_id = Column("fld_revision_id", Integer, primary_key=True, nullable=False)
    hardware_id = Column(
        "fld_hardware_id",
        Integer,
        primary_key=True,
        default=-1,
        nullable=False,
    )
    mode_id = Column("fld_mode_id", Integer, primary_key=True, nullable=False)
    mechanism_id = Column(
        "fld_mechanism_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
        unique=True,
    )

    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )
    pof_include = Column(
        "fld_pof_include", Integer, default=__defaults__["pof_include"]
    )
    rpn = Column("fld_rpn", Integer, default=__defaults__["rpn"])
    rpn_detection = Column(
        "fld_rpn_detection", Integer, default=__defaults__["rpn_detection"]
    )
    rpn_detection_new = Column(
        "fld_rpn_detection_new",
        Integer,
        default=__defaults__["rpn_detection_new"],
    )
    rpn_new = Column("fld_rpn_new", Integer, default=__defaults__["rpn_new"])
    rpn_occurrence = Column(
        "fld_rpn_occurrence", Integer, default=__defaults__["rpn_occurrence"]
    )
    rpn_occurrence_new = Column(
        "fld_rpn_occurrence_new",
        Integer,
        default=__defaults__["rpn_occurrence_new"],
    )

    # Define the relationships to other tables in the RAMSTK Program database.
    mode: relationship = relationship(
        "RAMSTKModeRecord",
        back_populates="mechanism",
    )
    cause: relationship = relationship(
        "RAMSTKCauseRecord",
        back_populates="mechanism",
        cascade="all,delete",
    )
    op_load: relationship = relationship(
        "RAMSTKOpLoadRecord",
        back_populates="mechanism",
        cascade="all,delete",
    )

    is_mode = False
    is_mechanism = True
    is_cause = False
    is_control = False
    is_action = False
    is_opload = False
    is_opstress = False
    is_testmethod = False

    def get_attributes(self):
        """Retrieve the current values of the Mechanism data model attributes.

        :return: {mode_id, mechanism_id, description, pof_include, rpn,
                  rpn_detection, rpn_detection_new, rpn_new, rpn_occurrence,
                  rpn_occurrence_new} pairs
        :rtype: dict
        """
        return {
            "mode_id": self.mode_id,
            "mechanism_id": self.mechanism_id,
            "description": self.description,
            "pof_include": self.pof_include,
            "rpn": self.rpn,
            "rpn_detection": self.rpn_detection,
            "rpn_detection_new": self.rpn_detection_new,
            "rpn_new": self.rpn_new,
            "rpn_occurrence": self.rpn_occurrence,
            "rpn_occurrence_new": self.rpn_occurrence_new,
        }
