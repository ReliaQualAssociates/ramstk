# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.commondb_hazards_record.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKHazard Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKHazardsRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent ramstk_hazard in the RAMSTK Common database."""

    __defaults__ = {
        "hazard_category": "Hazard Category",
        "hazard_subcategory": "Hazard Subcategory",
    }
    __tablename__ = "ramstk_hazards"
    __table_args__ = {"extend_existing": True}

    hazard_id = Column(
        "fld_hazard_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    hazard_category = Column(
        "fld_hazard_category", String(512), default="Hazard Category"
    )
    hazard_subcategory = Column(
        "fld_hazard_subcategory", String(512), default="Hazard Subcategory"
    )

    def get_attributes(self):
        """Retrieve current values of the RAMSTKHazard data model attributes.

        :return: {hazard_id, category, subcategory} pairs
        :rtype: tuple
        """
        return {
            "hazard_id": self.hazard_id,
            "hazard_category": self.hazard_category,
            "hazard_subcategory": self.hazard_subcategory,
        }
