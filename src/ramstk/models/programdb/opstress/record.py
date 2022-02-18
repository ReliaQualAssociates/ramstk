# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.RAMSTKOpStress.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2021 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKOpStress Table."""

# Third Party Imports
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord


class RAMSTKOpStressRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    """Class to represent table ramstk_op_stress in RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_op_load.
    """

    __defaults__ = {
        "description": "",
        "load_history": 0,
        "measurable_parameter": 0,
        "remarks": "",
    }
    __tablename__ = "ramstk_op_stress"
    __table_args__ = (
        ForeignKeyConstraint(
            [
                "fld_revision_id",
                "fld_hardware_id",
                "fld_mode_id",
                "fld_mechanism_id",
                "fld_opload_id",
            ],
            [
                "ramstk_op_load.fld_revision_id",
                "ramstk_op_load.fld_hardware_id",
                "ramstk_op_load.fld_mode_id",
                "ramstk_op_load.fld_mechanism_id",
                "ramstk_op_load.fld_opload_id",
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
    mechanism_id = Column("fld_mechanism_id", Integer, primary_key=True, nullable=False)
    opload_id = Column(
        "fld_opload_id", Integer, primary_key=True, nullable=False, unique=True
    )
    opstress_id = Column(
        "fld_opstress_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )
    load_history = Column(
        "fld_load_history", Integer, default=__defaults__["load_history"]
    )
    measurable_parameter = Column(
        "fld_measurable_parameter",
        Integer,
        default=__defaults__["measurable_parameter"],
    )
    remarks = Column("fld_remarks", String, default=__defaults__["remarks"])

    # Define the relationships to other tables in the RAMSTK Program database.
    op_load = relationship(  # type: ignore
        "RAMSTKOpLoadRecord",
        back_populates="op_stress",
    )

    is_mode = False
    is_mechanism = False
    is_opload = False
    is_opstress = True
    is_testmethod = False

    def get_attributes(self):
        """Retrieve the current values of the Op Stress data model attributes.

        :return: {opload_id, opstress_id, description, load_history,
                  measurable_parameter, remarks} pairs
        :rtype: tuple
        """
        return {
            "opload_id": self.opload_id,
            "opstress_id": self.opstress_id,
            "description": self.description,
            "load_history": self.load_history,
            "measurable_parameter": self.measurable_parameter,
            "remarks": self.remarks,
        }
