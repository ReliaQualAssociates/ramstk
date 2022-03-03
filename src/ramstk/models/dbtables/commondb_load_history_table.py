# -*- coding: utf-8 -*-
#
#       ramstk.models.commondb.load_history.table.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Load History Table Model."""

# Standard Library Imports
from typing import Type

# RAMSTK Local Imports
from ..dbrecords import RAMSTKLoadHistoryRecord
from .basetable import RAMSTKBaseTable


class RAMSTKLoadHistoryTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Load History table model."""

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_history_id"
    _db_tablename = "ramstk_load_history"
    _select_msg = "request_get_load_history"
    _tag = "load_history"

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKBaseTable.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "history_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKLoadHistoryRecord] = RAMSTKLoadHistoryRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "history_id"

        # Subscribe to PyPubSub messages.
