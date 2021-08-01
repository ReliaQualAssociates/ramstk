# -*- coding: utf-8 -*-
#
#       ramstk.controllers.opstress.datamanager.py is part of The RAMSTK Project
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
from ramstk.models.programdb import RAMSTKOpStress


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the OpStress data manager.

    This class manages the OpStress data from the RAMSTKOpStress data model.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_stress_id"
    _db_tablename = "ramstk_op_stress"
    _tag = "opstress"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a OpStress data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "opstress": [
                "revision_id",
                "hardware_id",
                "mode_id",
                "mechanism_id",
                "load_id",
                "stress_id",
            ],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id: int = 0
        self._mode_id: int = 0
        self._mechanism_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_opstress_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_opstress_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_opstress")
        pub.subscribe(super().do_update, "request_update_opstress")

        pub.subscribe(self.do_select_all, "selected_load")

        pub.subscribe(self._do_insert_opstress, "request_insert_opstress")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the OpStress data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            failure mode.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._revision_id = attributes["revision_id"]
        self._hardware_id = attributes["hardware_id"]
        self._mode_id = attributes["mode_id"]
        self._mechanism_id = attributes["mechanism_id"]
        self._parent_id = attributes["load_id"]

        for _opstress in self.dao.do_select_all(
            RAMSTKOpStress,
            key=["revision_id", "hardware_id", "mode_id", "mechanism_id", "load_id"],
            value=[
                self._revision_id,
                self._hardware_id,
                self._mode_id,
                self._mechanism_id,
                self._parent_id,
            ],
        ):
            self.tree.create_node(
                tag="opstress",
                identifier=_opstress.stress_id,
                parent=self._root,
                data={self._tag: _opstress},
            )
            self.last_id = self.dao.get_last_id("ramstk_op_stress", "fld_stress_id")

        pub.sendMessage(
            "succeed_retrieve_opstresss",
            tree=self.tree,
        )

    def _do_insert_opstress(self, parent_id: int) -> None:
        """Add a failure OpStress.

        :param parent_id: a list containing the the failure Mode ID and the failure
            Mechanism ID the new OpStress is associated with.
        :return: None
        :rtype: None
        """
        try:
            _opstress = RAMSTKOpStress()
            _opstress.revision_id = self._revision_id
            _opstress.hardware_id = self._hardware_id
            _opstress.mode_id = self._mode_id
            _opstress.mechanism_id = self._mechanism_id
            _opstress.load_id = parent_id
            _opstress.stress_id = self.last_id + 1

            self.dao.do_insert(_opstress)

            self.tree.create_node(
                tag="opstress",
                identifier=_opstress.stress_id,
                parent=self._root,
                data={self._tag: _opstress},
            )
            self.last_id = max(self.last_id, _opstress.stress_id)

            pub.sendMessage(
                "succeed_insert_opstress",
                node_id=_opstress.stress_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_opstress",
                error_message=_error.msg,
            )
