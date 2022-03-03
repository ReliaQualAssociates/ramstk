# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_program_status_table.py is part of The
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKProgramStatus Table Model."""

# Standard Library Imports
from datetime import date
from typing import Dict, Type, Union

# Third Party Imports
import pandas as pd
from pubsub import pub

# RAMSTK Local Imports
from ..dbrecords import RAMSTKProgramStatusRecord
from .basetable import RAMSTKBaseTable


class RAMSTKProgramStatusTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Program Status data manager.

    :ivar _dic_status: a dict with the last status date as the key and the status ID
        as the value.  Used to select the correct status when updating.
    """

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

    def __init__(self, **kwargs: Dict[str, Union[float, int, str]]) -> None:
        """Initialize a Program Status data manager instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_status: Dict[date, int] = {}

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "status_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKProgramStatusRecord] = RAMSTKProgramStatusRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "status_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_get_actual_status, "request_get_actual_status")
        pub.subscribe(self._do_set_attributes, "succeed_calculate_program_remaining")

    def do_get_new_record(  # pylint: disable=method-hidden
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> object:
        """Gets a new record instance with attributes set.

        :param attributes: the dict of attribute values to assign to the new record.
        :return: None
        :rtype: None
        """
        _new_record = self._record()
        _new_record.revision_id = attributes["revision_id"]
        _new_record.status_id = self.last_id + 1
        _new_record.date_status = date.today()

        self._dic_status[_new_record.date_status] = self.last_id + 1

        return _new_record

    def do_get_actual_status(self) -> None:
        """Select the actual program status remaining time and cost.

        :return: a pandas DataFrame() containing the actual status update
            dates and the remaining time/cost.
        :rtype: :class:`pandas.DataFrame`
        """
        self._dic_status = {
            _node.data["program_status"]
            .date_status: _node.data["program_status"]
            .status_id
            for _node in self.tree.all_nodes()[1:]
        }
        _dic_actual = {
            pd.to_datetime(_node.data["program_status"].date_status): [
                _node.data["program_status"].cost_remaining,
                _node.data["program_status"].time_remaining,
            ]
            for _node in self.tree.all_nodes()[1:]
        }

        _status = pd.DataFrame(
            _dic_actual.values(),
            index=_dic_actual.keys(),
            columns=["cost", "time"],
        ).sort_index()

        pub.sendMessage("succeed_get_actual_status", status=_status)

    def _do_set_attributes(self, cost_remaining: float, time_remaining: float) -> None:
        """Set the program remaining cost and time.

        :param cost_remaining: total remaining cost of verification program.
        :param time_remaining: total remaining time of verification program.
        :return: None
        :rtype: None
        """
        self.do_get_actual_status()
        try:
            _node_id = self._dic_status[date.today()]
        except KeyError:
            self.do_insert(
                attributes={
                    "revision_id": self._revision_id,
                    "status_id": -1,
                    "date_status": date.today(),
                    "cost_remaining": cost_remaining,
                    "time_remaining": time_remaining,
                }
            )
            _node_id = self.last_id + 1

        self.do_set_attributes(
            node_id=_node_id, package={"cost_remaining": cost_remaining}
        )
        self.do_set_attributes(
            node_id=_node_id, package={"time_remaining": time_remaining}
        )

        self.do_update(_node_id)
