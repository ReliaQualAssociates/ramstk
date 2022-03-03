# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.commondb_status_record.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKStatus Record Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKStatusRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent ramstk_status in the RAMSTK Common database."""

    __defaults__ = {
        "name": "Status Name",
        "description": "Status Decription",
        "status_type": "",
    }
    __tablename__ = "ramstk_status"
    __table_args__ = {"extend_existing": True}

    status_id = Column(
        "fld_status_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name = Column("fld_name", String(256), default=__defaults__["name"])
    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )
    status_type = Column(
        "fld_status_type", String(256), default=__defaults__["status_type"]
    )

    def get_attributes(self) -> Dict[str, Union[int, str]]:
        """Retrieve current values of the RAMSTKStatus data model attributes.

        :return: {status_id, name, description, status_type} pairs.
        :rtype: dict
        """
        return {
            "status_id": self.status_id,
            "name": self.name,
            "description": self.description,
            "status_type": self.status_type,
        }
