# -*- coding: utf-8 -*-
#
#       ramstk.controllers.test_method.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test Method Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKTestMethod


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Test Method data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_test_id"
    _db_tablename = "ramstk_test_method"
    _tag = "test_method"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Test Method data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "test_method": [
                "revision_id",
                "hardware_id",
                "mode_id",
                "mechanism_id",
                "load_id",
                "test_id",
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
        pub.subscribe(super().do_get_attributes, "request_get_test_method_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_test_method_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_test_method")
        pub.subscribe(super().do_update, "request_update_test_method")

        pub.subscribe(self.do_select_all, "selected_load")

        pub.subscribe(self._do_insert_test_method, "request_insert_test_method")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Test Method data from the RAMSTK Program database.

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

        for _test_method in self.dao.do_select_all(
            RAMSTKTestMethod,
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
                tag="test_method",
                identifier=_test_method.test_id,
                parent=self._root,
                data={self._tag: _test_method},
            )
            self.last_id = self.dao.get_last_id("ramstk_test_method", "fld_test_id")

        pub.sendMessage(
            "succeed_retrieve_test_methods",
            tree=self.tree,
        )

    def _do_insert_test_method(self, parent_id: int) -> None:
        """Add a failure Test Method.

        :param parent_id: the operating load ID the failure Test Method is associated
            with.
        :return: None
        :rtype: None
        """
        try:
            _test_method = RAMSTKTestMethod()
            _test_method.revision_id = self._revision_id
            _test_method.hardware_id = self._hardware_id
            _test_method.mode_id = self._mode_id
            _test_method.mechanism_id = self._mechanism_id
            _test_method.load_id = parent_id
            _test_method.test_id = self.last_id + 1

            self.dao.do_insert(_test_method)

            self.tree.create_node(
                tag="test_method",
                identifier=_test_method.test_id,
                parent=self._root,
                data={self._tag: _test_method},
            )

            self.last_id = max(self.last_id, _test_method.test_id)

            pub.sendMessage(
                "succeed_insert_test_method",
                node_id=_test_method.test_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_test_method",
                error_message=_error.msg,
            )
