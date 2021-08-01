# -*- coding: utf-8 -*-
#
#       ramstk.controllers.stakeholder.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Stakeholder Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKStakeholder


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Stakeholder data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_stakeholder_id"
    _db_tablename = "ramstk_stakeholder"
    _tag = "stakeholder"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Stakeholder data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {"stakeholder": ["revision_id", "stakeholder_id"]}

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_stakeholder_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_stakeholder_attributes")
        pub.subscribe(super().do_set_attributes, "lvw_editing_stakeholder")
        pub.subscribe(super().do_update, "request_update_stakeholder")

        pub.subscribe(self.do_select_all, "selected_revision")

        pub.subscribe(self._do_insert_stakeholder, "request_insert_stakeholder")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Stakeholder data from the RAMSTK Program database.

        :param attributes: the attributes dict for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _stakeholder in self.dao.do_select_all(
            RAMSTKStakeholder,
            key=["revision_id"],
            value=[self._revision_id],
            order=RAMSTKStakeholder.stakeholder_id,
        ):
            _data_package = {"stakeholder": _stakeholder}

            self.tree.create_node(
                tag="stakeholder",
                identifier=_stakeholder.stakeholder_id,
                parent=self._root,
                data=_data_package,
            )

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            "succeed_retrieve_stakeholders",
            tree=self.tree,
        )

    def _do_insert_stakeholder(self) -> None:
        """Add a new stakeholder.

        :return: None
        :rtype: None
        """
        try:
            _stakeholder = RAMSTKStakeholder()
            _stakeholder.revision_id = self._revision_id
            _stakeholder.stakeholder_id = self.last_id + 1
            _stakeholder.description = "New Stakeholder Input"

            self.dao.do_insert(_stakeholder)

            self.last_id = _stakeholder.stakeholder_id
            self.tree.create_node(
                tag="stakeholder",
                identifier=self.last_id,
                parent=0,
                data={"stakeholder": _stakeholder},
            )

            pub.sendMessage(
                "succeed_insert_stakeholder",
                node_id=self.last_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_stakeholder",
                error_message=_error.msg,
            )
