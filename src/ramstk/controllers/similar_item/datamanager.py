# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.similar_item.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Similar Item Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKSimilarItem


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Similar Item data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_similar_item"
    _tag = "similar_item"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Hardware data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "similar_item": ["revision_id", "hardware_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_similar_item_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_similar_item_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_similar_item")
        pub.subscribe(super().do_set_tree, "succeed_calculate_similar_item")
        pub.subscribe(super().do_update, "request_update_similar_item")

        pub.subscribe(self.do_select_all, "selected_revision")

        pub.subscribe(self._do_insert_similar_item, "request_insert_similar_item")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Similar Item data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _similar_item in self.dao.do_select_all(
            RAMSTKSimilarItem,
            key=["revision_id"],
            value=[self._revision_id],
            order=RAMSTKSimilarItem.parent_id,
        ):
            self.tree.create_node(
                tag="similar_item",
                identifier=_similar_item.hardware_id,
                parent=_similar_item.parent_id,
                data={"similar_item": _similar_item},
            )

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            "succeed_retrieve_similar_item",
            tree=self.tree,
        )

    def _do_insert_similar_item(self, hardware_id: int, parent_id: int = 0) -> None:
        """Add a new similar item record.

        :param hardware_id: the ID of the hardware item to associate the
            allocation record.
        :param parent_id: the parent allocation item's ID.
        :return: None
        :rtype: None
        """
        try:
            _similar_item = RAMSTKSimilarItem()
            _similar_item.revision_id = self._revision_id
            _similar_item.hardware_id = hardware_id
            _similar_item.parent_id = parent_id

            self.dao.do_insert(_similar_item)

            self.last_id = _similar_item.hardware_id

            self.tree.create_node(
                tag="similar_item",
                identifier=_similar_item.hardware_id,
                parent=parent_id,
                data={"similar_item": _similar_item},
            )

            pub.sendMessage(
                "succeed_insert_similar_item",
                node_id=self.last_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_similar_item",
                error_message=_error.msg,
            )
