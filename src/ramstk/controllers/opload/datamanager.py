# -*- coding: utf-8 -*-
#
#       ramstk.controllers.opload.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Operating Load Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
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
        self._hardware_id: int = 0
        self._mode_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_opload_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_opload_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_opload")
        pub.subscribe(super().do_update, "request_update_opload")

        pub.subscribe(self.do_select_all, "selected_mechanism")

        pub.subscribe(self._do_insert_opload, "request_insert_opload")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the OpLoad data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected failure mode.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._revision_id = attributes["revision_id"]
        self._parent_id = attributes["mechanism_id"]
        self._hardware_id = attributes["hardware_id"]
        self._mode_id = attributes["mode_id"]

        for _opload in self.dao.do_select_all(
            RAMSTKOpLoad,
            key=["revision_id", "hardware_id", "mode_id", "mechanism_id"],
            value=[
                self._revision_id,
                self._hardware_id,
                self._mode_id,
                self._parent_id,
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

    def _do_insert_opload(self, parent_id: int) -> None:
        """Add a failure OpLoad.

        :param parent_id: a list containing the the failure Mode ID and the failure
            Mechanism ID the new OpLoad is associated with.
        :return: None
        :rtype: None
        """
        try:
            _opload = RAMSTKOpLoad()
            _opload.revision_id = self._revision_id
            _opload.hardware_id = self._hardware_id
            _opload.mode_id = self._mode_id
            _opload.mechanism_id = parent_id
            _opload.load_id = self.last_id + 1

            self.dao.do_insert(_opload)

            self.tree.create_node(
                tag="opload",
                identifier=_opload.load_id,
                parent=self._root,
                data={self._tag: _opload},
            )
            self.last_id = max(self.last_id, _opload.load_id)

            pub.sendMessage(
                "succeed_insert_opload",
                node_id=_opload.load_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_opload",
                error_message=_error.msg,
            )
