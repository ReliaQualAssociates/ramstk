# -*- coding: utf-8 -*-
#
#       ramstk.models.options.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Options Package Data Model."""

# Standard Library Imports
from typing import Type

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable
from ramstk.models.commondb import RAMSTKSiteInfo


class DataManager(RAMSTKBaseTable):
    """Contain the attributes and methods of the Option data manager."""

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_site_id"
    _db_tablename = "ramstk_site_info"
    _tag = "option"

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKBaseTable.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_id_columns = [
            "site_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKSiteInfo] = RAMSTKSiteInfo

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "site_id"

        # Subscribe to PyPubSub messages.
