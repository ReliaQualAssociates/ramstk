# -*- coding: utf-8 -*-
#
#       ramstk.controllers.function.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Function Package Data Model."""

# Standard Library Imports
import inspect
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib.exceptions import NodeIDAbsentError

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKFunction


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Function data manager.

    This class manages the function data from the RAMSTKFunction and
    RAMSTKHazardAnalysis data models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_function_id"
    _db_tablename = "ramstk_function"
    _tag = "function"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Function data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {"function": ["revision_id", "function_id"]}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_function_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_function_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_function")
        pub.subscribe(super().do_update, "request_update_function")

        pub.subscribe(self.do_select_all, "selected_revision")

        pub.subscribe(self._do_insert_function, "request_insert_function")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Function data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Function.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _function in self.dao.do_select_all(
            RAMSTKFunction,
            key=["revision_id"],
            value=[self._revision_id],
            order=RAMSTKFunction.function_id,
        ):

            self.tree.create_node(
                tag=self._tag,
                identifier=_function.function_id,
                parent=_function.parent_id,
                data={self._tag: _function},
            )

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            "succeed_retrieve_functions",
            tree=self.tree,
        )

    def _do_insert_function(self, parent_id: int = 0) -> None:
        """Add a new function as child of the parent ID function.

        :param parent_id: the parent (function) ID of the function to
            insert the child.  Default is to add a top-level function.
        :return: None
        :rtype: None
        """
        _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore

        try:
            _last_id = self.dao.get_last_id("ramstk_function", "function_id")

            _function = RAMSTKFunction()
            _function.revision_id = self._revision_id
            _function.function_id = _last_id + 1
            _function.name = "New Function"
            _function.parent_id = parent_id

            self.dao.do_insert(_function)

            self.last_id = _function.function_id

            self.tree.create_node(
                tag=self._tag,
                identifier=_function.function_id,
                parent=_function.parent_id,
                data={self._tag: _function},
            )

            pub.sendMessage(
                "succeed_insert_function",
                node_id=self.last_id,
                tree=self.tree,
            )
        except NodeIDAbsentError:
            _error_msg: str = (
                "{1}: Attempted to insert child function under "
                "non-existent function ID {0}."
            ).format(str(parent_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_insert_function",
                error_message=_error_msg,
            )
        except DataAccessError:
            _error_msg = (
                "{1}: A database error occurred when attempting to "
                "add a child function to parent function ID "
                "{0}."
            ).format(str(parent_id), _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
            pub.sendMessage(
                "fail_insert_function",
                error_message=_error_msg,
            )
