# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mission.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mission Package Data Model."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.exceptions import DataAccessError
from ramstk.models.programdb import RAMSTKMission


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Mission data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_mission_id"
    _db_tablename = "ramstk_mission"
    _tag = "mission"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a RAMSTKFailureDefinition, data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "mission": ["revision_id", "mission_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mission_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mission_attributes")
        pub.subscribe(super().do_set_attributes, "lvw_editing_usage_profile")
        pub.subscribe(super().do_update, "request_update_mission")

        pub.subscribe(self.do_select_all, "selected_revision")

        pub.subscribe(self._do_insert_mission, "request_insert_mission")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve the Mission data from the RAMSTK Program database.

        :param attributes: the attributes for the selected Revision.
        :return: None
        :rtype: None
        """
        self._revision_id = attributes["revision_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        for _mission in self.dao.do_select_all(
            RAMSTKMission, key=["revision_id"], value=[self._revision_id]
        ):
            self.tree.create_node(
                tag="mission",
                identifier=_mission.mission_id,
                parent=self._root,
                data={"mission": _mission},
            )
            self.last_id = _mission.mission_id

        pub.sendMessage(
            "succeed_retrieve_missions",
            tree=self.tree,
        )

    def _do_insert_mission(self) -> None:
        """Add a new mission for revision ID.

        :return: None
        :rtype: None
        """
        try:
            _last_id = self.dao.get_last_id("ramstk_mission", "mission_id")
            _mission = RAMSTKMission()
            _mission.revision_id = self._revision_id
            _mission.mission_id = _last_id + 1

            self.dao.do_insert(_mission)

            self.tree.create_node(
                tag="mission",
                identifier=_mission.mission_id,
                parent=self._root,
                data={"mission": _mission},
            )

            self.last_id = max(self.last_id, _mission.mission_id)

            pub.sendMessage(
                "succeed_insert_mission",
                node_id=_mission.mission_id,
                tree=self.tree,
            )
        except DataAccessError as _error:
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error.msg,
            )
            pub.sendMessage(
                "fail_insert_mission",
                error_message=_error.msg,
            )
