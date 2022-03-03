# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.commondb_model_record.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKModel Record Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKModelRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent ramstk_model in the RAMSTK Common database."""

    __defaults__ = {
        "description": "Model Description",
        "model_type": 0,
    }
    __tablename__ = "ramstk_model"
    __table_args__ = {"extend_existing": True}

    model_id = Column(
        "fld_model_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )
    model_type = Column(
        "fld_model_type", String(256), default=__defaults__["model_type"]
    )

    def get_attributes(self) -> Dict[str, Union[int, str]]:
        """Retrieve current values of the RAMSTKModel data model attributes.

        :return: {model_id, description, model_type} pairs.
        :rtype: dict
        """
        return {
            "model_id": self.model_id,
            "description": self.description,
            "model_type": self.model_type,
        }
