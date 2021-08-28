# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.models.programdb.program_info.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Preferences Package Data Model."""

# Standard Library Imports
from typing import Type

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable, RAMSTKProgramInfoRecord


class RAMSTKProgramInfoTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Options data manager.

    This class manages the user-configurable Preferences and Options data from
    the Site and Program databases.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_revision_id"
    _db_tablename = "ramstk_program_info"
    _select_msg = "request_program_preferences"
    _tag = "preference"

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKBaseTable.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKProgramInfoRecord] = RAMSTKProgramInfoRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "revision_id"

        # Subscribe to PyPubSub messages.
