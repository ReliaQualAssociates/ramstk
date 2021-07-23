# -*- coding: utf-8 -*-
#
#       ramstk.controllers.control.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Control Package Data Controller."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKControl


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the FMEA Control data manager."""

    _tag = "control"
    _root = 0

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a FMEA Control data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "control": [
                "revision_id",
                "hardware_id",
                "mode_id",
                "mechanism_id",
                "cause_id",
                "control_id",
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
        pub.subscribe(super().do_get_attributes, "request_get_control_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_control_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_control")
        pub.subscribe(super().do_update, "request_update_control")

        pub.subscribe(self.do_select_all, "selected_cause")
        pub.subscribe(self.do_get_tree, "request_get_control_tree")

        pub.subscribe(self._do_delete, "request_delete_control")
        pub.subscribe(self._do_insert_control, "request_insert_control")

    def do_get_tree(self) -> None:
        """Retrieve the FMEA Control treelib Tree.

        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_get_control_tree",
            tree=self.tree,
        )

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the FMEA Control data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected failure control.
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

        for _control in self.dao.do_select_all(
            RAMSTKControl,
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
                identifier=_control.control_id,
                parent=self._root,
                data={self._tag: _control},
            )
            self.last_id = self.dao.get_last_id("ramstk_control", "fld_control_id")

        pub.sendMessage(
            "succeed_retrieve_controls",
            tree=self.tree,
        )

    def _do_delete(self, node_id: int) -> None:
        """Remove a FMEA Control record.

        :param node_id: the node (Control record) ID to be removed from the RAMSTK
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
                "succeed_delete_control",
                tree=self.tree,
            )
        except (AttributeError, DataAccessError, NodeIDAbsentError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg: str = (
                "{1}: Attempted to delete non-existent Control ID {0}."
            ).format(str(node_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_delete_control",
                error_message=_error_msg,
            )

    def _do_insert_control(self) -> None:
        """Add a failure Control record.

        :return: None
        :rtype: None
        """
        try:
            _control = RAMSTKControl()
            _control.revision_id = self._revision_id
            _control.hardware_id = self._hardware_id
            _control.mode_id = self._mode_id
            _control.mechanism_id = self._mechanism_id
            _control.cause_id = self._parent_id
            _control.control_id = self.last_id + 1

            self.dao.do_insert(_control)

            self.tree.create_node(
                tag=self._tag,
                identifier=_control.control_id,
                parent=self._root,
                data={self._tag: _control},
            )

            self.last_id = self.dao.get_last_id("ramstk_control", "fld_control_id")

            pub.sendMessage(
                "succeed_insert_control",
                node_id=_control.control_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_control",
                error_message=_error.msg,
            )
