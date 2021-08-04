# -*- coding: utf-8 -*-
#
#       ramstk.controllers.hazards.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Hazards Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKHazardAnalysis


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Hazard data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_hazard_id"
    _db_tablename = "ramstk_hazard_analysis"
    _select_msg = "selected_function"
    _tag = "hazard"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Hazard data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
            "function_id": 0,
        }
        self._pkey = {"hazard": ["revision_id", "function_id", "hazard_id"]}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKHazardAnalysis] = RAMSTKHazardAnalysis

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "hazard_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_hazard_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_hazard_attributes")
        pub.subscribe(super().do_set_attributes, "wvw_editing_hazard")
        pub.subscribe(super().do_update, "request_update_hazard")

        pub.subscribe(self.do_set_all_attributes, "request_set_all_hazard_attributes")

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
        _new_record.function_id = self._fkey["function_id"]
        _new_record.hazard_id = self.last_id + 1

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self._db_id_colname.replace("fld_", ""))

        _new_record.set_attributes(attributes)

        return _new_record

    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set all the attributes of the selected hazard.

        This is a helper method to set a group of attributes in a single
        call.  Used mainly by the AnalysisManager.

        :param attributes: the aggregate attributes dict for the hardware item.
        :return: None
        :rtype: None
        """
        for _key in attributes:
            super().do_set_attributes(
                node_id=[attributes["hazard_id"], ""], package={_key: attributes[_key]}
            )
