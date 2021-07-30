# -*- coding: utf-8 -*-
#
#       ramstk.controllers.action.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Action Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKAction


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the FMEA Action data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_tablename = "ramstk_action"
    _id_col = "fld_action_id"
    _select_msg = "selected_cause"
    _tag = "action"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a FMEA Action data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
            "hardware_id": 0,
            "mode_id": 0,
            "mechanism_id": 0,
            "cause_id": 0,
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record = RAMSTKAction

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.last_id = 0
        self.pkey: str = "action_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_insert_action, "request_insert_action")

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
