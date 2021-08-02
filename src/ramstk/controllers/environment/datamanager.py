# -*- coding: utf-8 -*-
#
#       ramstk.controllers.environment.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Environment Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKEnvironment


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Environment data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_environment_id"
    _db_tablename = "ramstk_environment"
    _tag = "environment"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize an Environment data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
            "phase_id": 0,
        }
        self._pkey = {
            "environment": ["revision_id", "phase_id", "environment_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: RAMSTKEnvironment = RAMSTKEnvironment

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_environment_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_environment_attributes")
        pub.subscribe(super().do_set_attributes, "lvw_editing_usage_profile")
        pub.subscribe(super().do_update, "request_update_environment")

        pub.subscribe(self.do_select_all, "selected_revision")

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
        _new_record.phase_id = attributes["phase_id"]
        _new_record.environment_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self._db_id_colname.replace("fld_", ""))

        _new_record.set_attributes(attributes)

        return _new_record

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve the Environment data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        self._fkey["revision_id"] = attributes["revision_id"]
        self._fkey["phase_id"] = attributes["phase_id"]

        for _environment in self.dao.do_select_all(
            RAMSTKEnvironment, key=["revision_id"], value=[self._fkey["revision_id"]]
        ):
            self.tree.create_node(
                tag="environment",
                identifier=_environment.environment_id,
                parent=self._parent_id,
                data={"environment": _environment},
            )

        self.last_id = max(self.tree.nodes.keys())

        pub.sendMessage(
            "succeed_retrieve_environments",
            tree=self.tree,
        )
