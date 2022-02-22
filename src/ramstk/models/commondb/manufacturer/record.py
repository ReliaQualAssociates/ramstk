# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.manufacturer.record.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Manufacturer Record Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord


class RAMSTKManufacturerRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    """Class to represent ramstk_manufacturer in the RAMSTK Common database."""

    __defaults__ = {
        "description": "Manufacturer Description",
        "location": "unknown",
        "cage_code": "CAGE Code",
    }
    __tablename__ = "ramstk_manufacturer"
    __table_args__ = {"extend_existing": True}

    manufacturer_id = Column(
        "fld_manufacturer_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )
    location = Column("fld_location", String(512), default=__defaults__["location"])
    cage_code = Column("fld_cage_code", String(512), default=__defaults__["cage_code"])

    def get_attributes(self) -> Dict[str, Union[int, str]]:
        """Retrieve current values of RAMSTKManufacturer data model attributes.

        :return: {manufacturer_id, description, location, cage_code} pairs
        :rtype: dict
        """
        return {
            "manufacturer_id": self.manufacturer_id,
            "description": self.description,
            "location": self.location,
            "cage_code": self.cage_code,
        }
