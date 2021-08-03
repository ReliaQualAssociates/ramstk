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
from ramstk.models.programdb import RAMSTKAction


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the FMEA Action data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_action_id"
    _db_tablename = "ramstk_action"
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
        self._record: RAMSTKAction = RAMSTKAction

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

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = self._fkey["revision_id"]
        _new_record.hardware_id = self._fkey["hardware_id"]
        _new_record.mode_id = self._fkey["mode_id"]
        _new_record.mechanism_id = self._fkey["mechanism_id"]
        _new_record.cause_id = self._fkey["cause_id"]
        _new_record.action_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self._db_id_colname.replace("fld_", ""))

        _new_record.set_attributes(attributes)

        return _new_record

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the FMEA Action data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected failure action.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._fkey["revision_id"] = attributes["revision_id"]
        self._fkey["hardware_id"] = attributes["hardware_id"]
        self._fkey["mode_id"] = attributes["mode_id"]
        self._fkey["mechanism_id"] = attributes["mechanism_id"]
        self._fkey["cause_id"] = attributes["cause_id"]

        for _action in self.dao.do_select_all(
            RAMSTKAction,
            key=["revision_id", "hardware_id", "mode_id", "mechanism_id", "cause_id"],
            value=[
                self._fkey["revision_id"],
                self._fkey["hardware_id"],
                self._fkey["mode_id"],
                self._fkey["mechanism_id"],
                self._fkey["cause_id"],
            ],
        ):
            self.tree.create_node(
                tag=self._tag,
                identifier=_action.action_id,
                parent=self._parent_id,
                data={self._tag: _action},
            )
            self.last_id = self.dao.get_last_id("ramstk_action", "fld_action_id")

        pub.sendMessage(
            "succeed_retrieve_actions",
            tree=self.tree,
        )
