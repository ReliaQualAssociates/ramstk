# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.allocation.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Allocation Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKAllocation


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Allocation data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_allocation"
    _select_msg = "selected_revision"
    _tag = "allocation"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Allocation data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
        }
        self._pkey = {
            "allocation": ["revision_id", "hardware_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKAllocation] = RAMSTKAllocation

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_allocation_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_allocation_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_allocation")
        pub.subscribe(super().do_set_tree, "succeed_calculate_allocation")
        pub.subscribe(super().do_update, "request_update_allocation")

        pub.subscribe(self.do_set_all_attributes, "succeed_calculate_allocation_goals")

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
        _new_record.revision_id = self._fkey["revision_id"]
        _new_record.parent_id = attributes["parent_id"]
        _new_record.hardware_id = attributes["hardware_id"]

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self.pkey)

        _new_record.set_attributes(attributes)

        return _new_record

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the record associated with the Module ID.

        This is a helper function to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the allocation
            item.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            super().do_set_attributes(
                node_id=[attributes["hardware_id"], -1],
                package={_key: attributes[_key]},
            )
