# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mode.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mode Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKMode


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Mode data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_mode_id"
    _db_tablename = "ramstk_mode"
    _tag = "mode"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Mode data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "mode": ["revision_id", "hardware_id", "mode_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mode_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mode_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_mode")
        pub.subscribe(super().do_update, "request_update_mode")

        pub.subscribe(self.do_select_all, "selected_revision")

        pub.subscribe(self._do_insert_mode, "request_insert_mode")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Mode data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            function or hardware item.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]
        self._parent_id = attributes["hardware_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _mode in self.dao.do_select_all(
            RAMSTKMode,
            key=["revision_id", "hardware_id"],
            value=[self._revision_id, self._parent_id],
        ):
            self.tree.create_node(
                tag=self._tag,
                identifier=_mode.mode_id,
                parent=self._root,
                data={self._tag: _mode},
            )
            self.last_id = _mode.mode_id

        pub.sendMessage(
            "succeed_retrieve_modes",
            tree=self.tree,
        )

    def _do_insert_mode(self) -> None:
        """Add a new failure mode.

        :return: None
        :rtype: None
        """
        try:
            _last_id: int = self.dao.get_last_id("ramstk_mode", "mode_id")
            _mode = RAMSTKMode()
            _mode.revision_id = self._revision_id
            _mode.hardware_id = self._parent_id
            _mode.mode_id = _last_id + 1

            self.dao.do_insert(_mode)

            self.tree.create_node(
                tag="mode",
                identifier=_mode.mode_id,
                parent=self._root,
                data={"mode": _mode},
            )

            self.last_id = max(self.last_id, _mode.mode_id)

            pub.sendMessage(
                "succeed_insert_mode",
                node_id=_mode.mode_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_mode",
                error_message=_error.msg,
            )
