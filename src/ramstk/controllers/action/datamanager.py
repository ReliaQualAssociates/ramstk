# -*- coding: utf-8 -*-
#
#       ramstk.controllers.action.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Action Package Data Controller."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKAction


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the FMEA Action data manager."""

    _tag = "action"
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a FMEA Action data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "action": [
                "revision_id",
                "hardware_id",
                "mode_id",
                "mechanism_id",
                "cause_id",
                "action_id",
            ],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id: int = 0
        self._mode_id: int = 0
        self._mechanism_id: int = 0
        self._cause_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_action_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_action_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_action")
        pub.subscribe(super().do_update, "request_update_action")

        pub.subscribe(self.do_select_all, "selected_cause")

        pub.subscribe(self._do_delete, "request_delete_action")
        pub.subscribe(self._do_insert_action, "request_insert_action")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the FMEA Action data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected failure action.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._revision_id = attributes["revision_id"]
        self._hardware_id = attributes["hardware_id"]
        self._mode_id = attributes["mode_id"]
        self._mechanism_id = attributes["mechanism_id"]
        self._parent_id = attributes["cause_id"]

        for _action in self.dao.do_select_all(
            RAMSTKAction,
            key=["revision_id", "hardware_id", "mode_id", "mechanism_id", "cause_id"],
            value=[
                self._revision_id,
                self._hardware_id,
                self._mode_id,
                self._mechanism_id,
                self._parent_id,
            ],
        ):
            self.tree.create_node(
                tag=self._tag,
                identifier=_action.action_id,
                parent=self._root,
                data={self._tag: _action},
            )
            self.last_id = self.dao.get_last_id("ramstk_action", "fld_action_id")

        pub.sendMessage(
            "succeed_retrieve_actions",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a FMEA Action record.

        :param node_id: the node (Action record) ID to be removed from the RAMSTK
            Program database.
        :return: None
        :rtype: None
        """
        try:
            _table = list(self.tree.get_node(node_id).data.keys())[0]

            super().do_delete(node_id, _table)

            self.tree.remove_node(node_id)
            self.last_id = max(self.tree.nodes.keys())

            pub.sendMessage(
                "succeed_delete_action",
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent Action ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_action",
                error_message=_error_msg,
            )

    def _do_insert_action(self) -> None:
        """Add a failure Action record.

        :return: None
        :rtype: None
        """
        try:
            _action = RAMSTKAction()
            _action.revision_id = self._revision_id
            _action.hardware_id = self._hardware_id
            _action.mode_id = self._mode_id
            _action.mechanism_id = self._mechanism_id
            _action.cause_id = self._parent_id
            _action.action_id = self.last_id + 1

            self.dao.do_insert(_action)

            self.tree.create_node(
                tag=self._tag,
                identifier=_action.action_id,
                parent=self._root,
                data={self._tag: _action},
            )

            self.last_id = self.dao.get_last_id("ramstk_action", "fld_action_id")

            pub.sendMessage(
                "succeed_insert_action",
                node_id=_action.action_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_action",
                error_message=_error.msg,
            )
