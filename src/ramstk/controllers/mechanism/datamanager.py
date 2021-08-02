# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mechanism.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Mechanism Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKMechanism


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Mechanism data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_mechanism_id"
    _db_tablename = "ramstk_mechanism"
    _tag = "mechanism"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Mechanism data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
            "hardware_id": 0,
            "mode_id": 0,
        }
        self._pkey = {
            "mechanism": ["revision_id", "hardware_id", "mode_id", "mechanism_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKMechanism] = RAMSTKMechanism

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mechanism_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mechanism_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_mechanism")
        pub.subscribe(super().do_update, "request_update_mechanism")

        pub.subscribe(self.do_select_all, "selected_mode")

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
        _new_record.mechanism_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self._db_id_colname.replace("fld_", ""))

        _new_record.set_attributes(attributes)

        return _new_record

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Mechanism data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            failure mode.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._fkey["revision_id"] = attributes["revision_id"]
        self._fkey["hardware_id"] = attributes["hardware_id"]
        self._fkey["mode_id"] = attributes["mode_id"]

        for _mechanism in self.dao.do_select_all(
            RAMSTKMechanism,
            key=["revision_id", "hardware_id", "mode_id"],
            value=[
                self._fkey["revision_id"],
                self._fkey["hardware_id"],
                self._fkey["mode_id"],
            ],
        ):
            self.tree.create_node(
                tag="mechanism",
                identifier=_mechanism.mechanism_id,
                parent=self._parent_id,
                data={"mechanism": _mechanism},
            )
            self.last_id = _mechanism.mechanism_id

        pub.sendMessage(
            "succeed_retrieve_mechanisms",
            tree=self.tree,
        )
