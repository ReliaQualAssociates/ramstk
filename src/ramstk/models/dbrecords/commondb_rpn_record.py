# -*- coding: utf-8 -*-
#
#       ramstk.models.dbrecords.commondb_rpn_record.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKRPN Record Model."""

# Standard Library Imports
from typing import Dict, Union

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Local Imports
from .. import RAMSTK_BASE
from .baserecord import RAMSTKBaseRecord


class RAMSTKRPNRecord(RAMSTK_BASE, RAMSTKBaseRecord):  # type: ignore
    """Class to represent table ramstk_rpn in the RAMSTK Common database."""

    __defaults__ = {
        "name": "RPN Name",
        "description": "RPN Description",
        "rpn_type": "",
        "value": 0,
    }
    __tablename__ = "ramstk_rpn"
    __table_args__ = {"extend_existing": True}

    rpn_id = Column(
        "fld_rpn_id",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name = Column("fld_name", String(512), default=__defaults__["name"])
    description = Column(
        "fld_description", String(512), default=__defaults__["description"]
    )
    rpn_type = Column("fld_rpn_type", String(256), default=__defaults__["rpn_type"])
    value = Column("fld_value", Integer, default=__defaults__["value"])

    def get_attributes(self) -> Dict[str, Union[int, str]]:
        """Retrieve the current values of the RAMSTKRPN data model attributes.

        :return: {}rpn_id, name, description, rpn_type, value} key:value pairs
        :rtype: dict
        """
        return {
            "rpn_id": self.rpn_id,
            "name": self.name,
            "description": self.description,
            "rpn_type": self.rpn_type,
            "value": self.value,
        }
