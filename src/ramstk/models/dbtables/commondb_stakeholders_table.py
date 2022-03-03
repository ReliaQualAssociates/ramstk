# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.stakeholders.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholders Table Model."""

# Standard Library Imports
from typing import Type

# RAMSTK Local Imports
from ..dbrecords import RAMSTKStakeholdersRecord
from .basetable import RAMSTKBaseTable


class RAMSTKStakeholdersTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Option data manager."""

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_stakeholders_id"
    _db_tablename = "ramstk_stakeholders"
    _select_msg = "request_get_stakeholders"
    _tag = "stakeholders"

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKBaseTable.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "stakeholders_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKStakeholdersRecord] = RAMSTKStakeholdersRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "stakeholders_id"

        # Subscribe to PyPubSub messages.
