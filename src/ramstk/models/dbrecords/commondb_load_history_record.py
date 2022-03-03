# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.commondb_load_history_record.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Load History Table Model."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKLoadHistoryRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent the table ramstk_load_history."""

    __defaults__ = {
        "description": "Load History Description",
    }
    __tablename__ = "ramstk_load_history"
    __table_args__ = {"extend_existing": True}

    history_id = Column(
        "fld_history_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )

    def get_attributes(self):
        """Retrieve current values of RAMSTKLoadHistory data model attributes.

        :return: {load_history_id, description} pairs
        :rtype: dict
        """
        return {
            "history_id": self.history_id,
            "description": self.description,
        }
