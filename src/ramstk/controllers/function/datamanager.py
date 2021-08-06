# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKFunction


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Function data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_function_id"
    _db_tablename = "ramstk_function"
    _select_msg = "selected_revision"
    _tag = "function"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Function data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {"function": ["revision_id", "function_id"]}

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "function_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKFunction] = RAMSTKFunction

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "function_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_function_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_function_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_function")
        pub.subscribe(super().do_update, "request_update_function")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes["parent_id"]

        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.function_id = self.last_id + 1
        _new_record.parent_id = attributes["parent_id"]

        return _new_record
