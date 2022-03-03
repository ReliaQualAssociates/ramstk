# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.programdb_test_method_record.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKTestMethod Record Model."""

# Third Party Imports
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKTestMethodRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent table ramstk_test_method in RAMSTK Program database.

    This table shared a Many-to-One relationship with ramstk_op_stress.
    """

    __defaults__ = {
        "description": "",
        "boundary_conditions": "",
        "remarks": "",
    }
    __tablename__ = "ramstk_test_method"
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
    test_method_id = Column(
        "fld_test_method_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )
    boundary_conditions = Column(
        "fld_boundary_conditions",
        String(512),
        default=__defaults__["boundary_conditions"],
    )
    remarks = Column("fld_remarks", String, default=__defaults__["remarks"])

    # Define the relationships to other tables in the RAMSTK Program database.
    op_load: relationship = relationship(
        "RAMSTKOpLoadRecord",
        back_populates="test_method",
    )

    is_mode = False
    is_mechanism = False
    is_opload = False
    is_opstress = False
    is_testmethod = True

    def get_attributes(self):
        """Retrieve current values of RAMSTKTestMethod data model attributes.

        :return: {test_id, description, boundary_conditions, remarks} pairs
        :rtype: dict
        """
        return {
            "opload_id": self.opload_id,
            "test_method_id": self.test_method_id,
            "description": self.description,
            "boundary_conditions": self.boundary_conditions,
            "remarks": self.remarks,
        }
