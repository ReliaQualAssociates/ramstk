# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_program_info_table.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKProgramInfo Table Model."""

# Standard Library Imports
from typing import Dict, Type, Union

# RAMSTK Local Imports
from ..dbrecords import RAMSTKProgramInfoRecord
from .basetable import RAMSTKBaseTable


class RAMSTKProgramInfoTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Program Info table model."""

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

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKProgramInfo table model instance."""
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
