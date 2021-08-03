# -*- coding: utf-8 -*-
#
#       ramstk.controllers.opload.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Operating Load Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKOpLoad


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the OpLoad data manager.

    This class manages the OpLoad data from the RAMSTKOpLoad data model.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_load_id"
    _db_tablename = "ramstk_opload"
    _tag = "opload"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a OpLoad data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
            "hardware_id": 0,
            "mode_id": 0,
            "mechanism_id": 0,
        }
        self._pkey = {
            "opload": [
                "revision_id",
                "hardware_id",
                "mode_id",
                "mechanism_id",
                "load_id",
            ],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKOpLoad] = RAMSTKOpLoad

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_opload_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_opload_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_opload")
        pub.subscribe(super().do_update, "request_update_opload")

        pub.subscribe(self.do_select_all, "selected_mechanism")

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
        _new_record.load_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self._db_id_colname.replace("fld_", ""))

        _new_record.set_attributes(attributes)

        return _new_record

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the OpLoad data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected failure mode.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._fkey["revision_id"] = attributes["revision_id"]
        self._fkey["hardware_id"] = attributes["hardware_id"]
        self._fkey["mode_id"] = attributes["mode_id"]
        self._fkey["mechanism_id"] = attributes["mechanism_id"]

        for _opload in self.dao.do_select_all(
            RAMSTKOpLoad,
            key=["revision_id", "hardware_id", "mode_id", "mechanism_id"],
            value=[
                self._fkey["revision_id"],
                self._fkey["hardware_id"],
                self._fkey["mode_id"],
                self._fkey["mechanism_id"],
            ],
        ):
            self.tree.create_node(
                tag="opload",
                identifier=_opload.load_id,
                parent=self._root,
                data={self._tag: _opload},
            )
            self.last_id = self.dao.get_last_id("ramstk_op_load", "fld_load_id")

        pub.sendMessage(
            "succeed_retrieve_oploads",
            tree=self.tree,
        )
