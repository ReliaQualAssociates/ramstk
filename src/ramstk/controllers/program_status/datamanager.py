# -*- coding: utf-8 -*-
#
#       ramstk.controllers.program_status.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Program Status Package Data Model."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict, List, Type

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.programdb import RAMSTKProgramStatus


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Program Status data manager."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_status_id"
    _db_tablename = "ramstk_program_status"
    _select_msg = "selected_revision"
    _tag = "program_status"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs: Dict[Any, Any]) -> None:
        """Initialize a Program Status data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._fkey = {
            "revision_id": 0,
        }
        self._dic_status: Dict[Any, List[float]] = {}
        self._pkey = {"program_status": ["revision_id", "status_id"]}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKProgramStatus] = RAMSTKProgramStatus

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "status_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().do_get_attributes, "request_get_program_status_attributes"
        )
        pub.subscribe(
            super().do_set_attributes, "request_set_program_status_attributes"
        )
        pub.subscribe(super().do_update, "request_update_program_status")

        pub.subscribe(self._do_set_attributes, "succeed_calculate_all_validation_tasks")

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
        _new_record.status_id = self.last_id + 1
        _new_record.date_status = date.today()

        for _key in self._fkey.items():
            attributes.pop(_key[0])
        attributes.pop(self.pkey)

        _new_record.set_attributes(attributes)
        self._dic_status[_new_record.date_status] = _new_record.status_id

        return _new_record

    def _do_set_attributes(self, cost_remaining, time_remaining) -> None:
        """Set the program remaining cost and time.

        :param cost_remaining: total remaining cost of verification program.
        :param time_remaining: total remaining time of verification program.
        :return: None
        :rtype: None
        """
        try:
            _node_id = self._dic_status[date.today()]
        except KeyError:
            self.do_insert(
                attributes={
                    "revision_id": self._fkey["revision_id"],
                    "status_id": -1,
                    "date_status": date.today(),
                    "cost_remaining": cost_remaining,
                    "time_remaining": time_remaining,
                }
            )
            _node_id = self.last_id

        self.tree.get_node(_node_id).data[
            "program_status"
        ].cost_remaining = cost_remaining
        self.tree.get_node(_node_id).data[
            "program_status"
        ].time_remaining = time_remaining

        self.do_update(_node_id, table="program_status")
