# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.commondb_subcategory_table.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""SubCategory Table Model."""

# Standard Library Imports
from typing import Type

# RAMSTK Local Imports
from ..dbrecords import RAMSTKSubCategoryRecord
from .basetable import RAMSTKBaseTable


class RAMSTKSubCategoryTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Option data manager."""

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_subcategory_id"
    _db_tablename = "ramstk_subcategory"
    _select_msg = "request_get_subcategory"
    _tag = "subcategory"

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKBaseTable.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "category_id",
            "subcategory_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKSubCategoryRecord] = RAMSTKSubCategoryRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "subcategory_id"

        # Subscribe to PyPubSub messages.
