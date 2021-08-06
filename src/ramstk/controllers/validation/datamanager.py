# -*- coding: utf-8 -*-
#
#       ramstk.controllers.validation.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Validation Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKValidation


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Validation data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_validation_id"
    _db_tablename = "ramstk_validation"
    _select_msg = "selected_revision"
    _tag = "validation"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Validation data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_status: Dict[Any, float] = {}
        self._pkey = {"validation": ["revision_id", "validation_id"]}

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "validation_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKValidation] = RAMSTKValidation

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "validation_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_validation_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_validation_attributes")
        pub.subscribe(super().do_set_attributes, "mvw_editing_validation")
        pub.subscribe(super().do_set_attributes, "wvw_editing_validation")
        pub.subscribe(super().do_update, "request_update_validation")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.validation_id = self.last_id + 1
        _new_record.name = "New Validation Task"

        return _new_record
