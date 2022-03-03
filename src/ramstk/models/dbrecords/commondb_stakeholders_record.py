# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.commondb_stakeholders_record.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKStakeholders Record Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKStakeholdersRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent ramstk_stakeholders in the RAMSTK Common database."""

    __defaults__ = {
        "stakeholder": "Stakeholder",
    }
    __tablename__ = "ramstk_stakeholders"
    __table_args__ = {"extend_existing": True}

    stakeholders_id = Column(
        "fld_stakeholders_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    stakeholder = Column(
        "fld_stakeholder", String(512), default=__defaults__["stakeholder"]
    )

    def get_attributes(self) -> Dict[str, Union[int, str]]:
        """Retrieve current values of RAMSTKStakeholders data model attributes.

        :return: {stakeholders_id, stakeholder} pairs.
        :rtype: dict
        """
        return {
            "stakeholders_id": self.stakeholders_id,
            "stakeholder": self.stakeholder,
        }
