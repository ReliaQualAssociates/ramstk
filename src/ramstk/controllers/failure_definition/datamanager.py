# -*- coding: utf-8 -*-
#
#       ramstk.controllers.failure_definition.datamanager.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Definition Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKFailureDefinition


class DataManager(RAMSTKDataManager):
    """Contains attributes and methods of the Failure Definition data manager.

    This class manages the failure definition data from the
    RAMSTKFailureDefinition data models.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_definition_id"
    _db_tablename = "ramstk_failure_definition"
    _select_msg = "selected_revision"
    _tag = "failure_definition"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Failure Definition data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {"revision_id": 0}
        self._pkey: Dict[str, List[str]] = {
            "failure_definition": ["revision_id", "definition_id"]
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKFailureDefinition] = RAMSTKFailureDefinition

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "definition_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().do_get_attributes, "request_get_failure_definition_attributes"
        )
        pub.subscribe(
            super().do_set_attributes, "request_set_failure_definition_attributes"
        )
        pub.subscribe(super().do_set_attributes, "lvw_editing_failure_definition")
        pub.subscribe(super().do_update, "request_update_failure_definition")

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
        _new_record.definition_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self.pkey)

        _new_record.set_attributes(attributes)

        return _new_record
