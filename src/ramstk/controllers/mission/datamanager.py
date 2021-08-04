# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mission.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Mission Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKMission


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Mission data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_mission_id"
    _db_tablename = "ramstk_mission"
    _select_msg = "selected_revision"
    _tag = "mission"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a RAMSTKFailureDefinition, data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
        }
        self._pkey = {
            "mission": ["revision_id", "mission_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKMission] = RAMSTKMission

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "mission_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_mission_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_mission_attributes")
        pub.subscribe(super().do_set_attributes, "lvw_editing_usage_profile")
        pub.subscribe(super().do_update, "request_update_mission")

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
        _new_record.mission_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self._db_id_colname.replace("fld_", ""))

        _new_record.set_attributes(attributes)

        return _new_record
