# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.controllers.similar_item.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Similar Item Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKSimilarItem


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Similar Item data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hardware_id"
    _db_tablename = "ramstk_similar_item"
    _select_msg = "selected_revision"
    _tag = "similar_item"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Initialize a Hardware data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._pkey = {
            "similar_item": ["revision_id", "hardware_id"],
        }

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "hardware_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKSimilarItem] = RAMSTKSimilarItem

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hardware_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_similar_item_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_similar_item_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_similar_item")
        pub.subscribe(super().do_set_tree, "succeed_calculate_similar_item")
        pub.subscribe(super().do_update, "request_update_similar_item")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Any]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes["parent_id"]

        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.hardware_id = attributes["hardware_id"]
        _new_record.parent_id = attributes["parent_id"]

        return _new_record
