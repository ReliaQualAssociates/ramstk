# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.preferences.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Preferences Package Data Model."""

# Standard Library Imports
from typing import Dict, List, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKProgramInfo


class DataManager(RAMSTKDataManager):
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
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.
        self._pkey: Dict[str, List[str]] = {
            "preference": ["revision_id"],
        }

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKProgramInfo] = RAMSTKProgramInfo

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "revision_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_preference_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_preference_attributes")
        pub.subscribe(super().do_update, "request_update_preference")
