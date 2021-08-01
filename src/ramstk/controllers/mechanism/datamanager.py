# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mechanism.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Mechanism Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
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
        self._pkey = {
            "mechanism": ["revision_id", "hardware_id", "mode_id", "mechanism_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mechanism_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mechanism_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_mechanism")
        pub.subscribe(super().do_update, "request_update_mechanism")

        pub.subscribe(self.do_select_all, "selected_mode")

        pub.subscribe(self._do_insert_mechanism, "request_insert_mechanism")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Mechanism data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected
            failure mode.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._revision_id = attributes["revision_id"]
        self._hardware_id = attributes["hardware_id"]
        self._parent_id = attributes["mode_id"]

        for _mechanism in self.dao.do_select_all(
            RAMSTKMechanism,
            key=["revision_id", "hardware_id", "mode_id"],
            value=[self._revision_id, self._hardware_id, self._parent_id],
        ):
            self.tree.create_node(
                tag="mechanism",
                identifier=_mechanism.mechanism_id,
                parent=self._root,
                data={"mechanism": _mechanism},
            )
            self.last_id = _mechanism.mechanism_id

        pub.sendMessage(
            "succeed_retrieve_mechanisms",
            tree=self.tree,
        )

    def _do_insert_mechanism(self) -> None:
        """Add a failure Mechanism.

        :return: None
        :rtype: None
        """
        try:
            _mechanism = RAMSTKMechanism()
            _mechanism.revision_id = self._revision_id
            _mechanism.hardware_id = self._hardware_id
            _mechanism.mode_id = self._parent_id
            _mechanism.mechanism_id = self.last_id + 1

            self.dao.do_insert(_mechanism)

            self.tree.create_node(
                tag=self._tag,
                identifier=_mechanism.mechanism_id,
                parent=self._root,
                data={self._tag: _mechanism},
            )

            self.last_id = max(self.last_id, _mechanism.mechanism_id)

            pub.sendMessage(
                "succeed_insert_{}".format(self._tag),
                node_id=_mechanism.mechanism_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_{}".format(self._tag),
                error_message=_error.msg,
            )
