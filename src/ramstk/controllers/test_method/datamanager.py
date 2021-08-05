# -*- coding: utf-8 -*-
#
#       ramstk.controllers.test_method.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Test Method Package Data Controller."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKTestMethod


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Test Method data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_test_id"
    _db_tablename = "ramstk_test_method"
    _select_msg = "selected_load"
    _tag = "test_method"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Test Method data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
            "hardware_id": 0,
            "mode_id": 0,
            "mechanism_id": 0,
            "load_id": 0,
        }
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
        self._record: Type[RAMSTKTestMethod] = RAMSTKTestMethod

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "test_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_test_method_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_test_method_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_test_method")
        pub.subscribe(super().do_update, "request_update_test_method")

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
        _new_record.hardware_id = self._fkey["hardware_id"]
        _new_record.mode_id = self._fkey["mode_id"]
        _new_record.mechanism_id = self._fkey["mechanism_id"]
        _new_record.load_id = self._fkey["load_id"]
        _new_record.test_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self.pkey)

        _new_record.set_attributes(attributes)

        return _new_record
