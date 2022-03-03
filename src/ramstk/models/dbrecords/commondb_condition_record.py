# * coding: utf8 *
#
#       ramstk.models.dbrecords.commondb_condition_record.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Condition Record Model."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKConditionRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent ramstk_condition in RAMSTK Common database."""

    __defaults__ = {
        "description": "Condition Description",
        "condition_type": "",
    }
    __tablename__ = "ramstk_condition"
    __table_args__ = {"extend_existing": True}

    condition_id = Column(
        "fld_condition_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )
    condition_type = Column(
        "fld_condition_type",
        String(256),
        default=__defaults__["condition_type"],
    )

    def get_attributes(self):
        """Retrieve current values of RAMSTKCondition data model attributes.

        :return: {condition_id, description, condition_type} pairs
        :rtype: dict
        """
        return {
            "condition_id": self.condition_id,
            "description": self.description,
            "condition_type": self.condition_type,
        }
