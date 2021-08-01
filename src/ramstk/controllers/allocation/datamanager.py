# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.allocation.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Allocation Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

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
    _tag = "allocation"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Allocation data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {"revision_id": 0, "hardware_id": 0}
        self._pkey = {
            "allocation": ["revision_id", "hardware_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: RAMSTKAllocation = RAMSTKAllocation

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_allocation_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_allocation_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_allocation")
        pub.subscribe(super().do_set_tree, "succeed_calculate_allocation")
        pub.subscribe(super().do_update, "request_update_allocation")

        pub.subscribe(self.do_select_all, "selected_revision")
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
        _new_record.parent_id = self._parent_id
        _new_record.hardware_id = attributes["hardware_id"]

        for _key in self._fkey.items():
            attributes.pop(_key[0])

        _new_record.set_attributes(attributes)

        return _new_record

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve the Allocation BoM data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._fkey["revision_id"] = attributes["revision_id"]
        self._fkey["hardware_id"] = attributes["hardware_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _allocation in self.dao.do_select_all(
            RAMSTKAllocation,
            key=["revision_id"],
            value=[self._fkey["revision_id"]],
            order=RAMSTKAllocation.parent_id,
        ):

            self.tree.create_node(
                tag="allocation",
                identifier=_allocation.hardware_id,
                parent=_allocation.parent_id,
                data={"allocation": _allocation},
            )

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            "succeed_retrieve_allocation",
            tree=self.tree,
        )

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
