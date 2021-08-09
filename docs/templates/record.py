# pylint: disable=duplicate-code
# -*- coding: utf-8 -*-
#
#       ramstk.models.<MODULE>.record.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKAction Table Module."""

# Standard Library Imports

# Third Party Imports
from sqlalchemy import Column, ForeignKeyConstraint, Integer, String
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord


class RAMSTK<MODULE>Record(RAMSTK_BASE, RAMSTKBaseRecord):
    """Class to represent a <MODULE> record in the RAMSTK Program database.

    This table shares a Many-to-One relationship with ramstk_cause.
    """

    __defaults__ = {}
    __tablename__ = "<MODULE>"
    __table_args__ = (
        ForeignKeyConstraint(
            [
            ],
            [
            ],
        ),
        {"extend_existing": True},
    )

    # Define the relationships to other tables in the RAMSTK Program database.

    def get_attributes(self):
        """Retrieve current values of the <MODULE> record attributes.

        :return: {} pairs.
        :rtype: dict
        """
        _attributes = {
            "<attribute>": self.<attribute>,
        }

        return _attributes
