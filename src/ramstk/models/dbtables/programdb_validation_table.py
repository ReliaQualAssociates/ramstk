# -*- coding: utf-8 -*-
#
#       ramstk.models.dbtables.programdb_validation_table.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKValidation Table Model."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict, Type, Union

# Third Party Imports
import pandas as pd
from pubsub import pub

# RAMSTK Local Imports
from ..dbrecords import RAMSTKValidationRecord
from .basetable import RAMSTKBaseTable


class RAMSTKValidationTable(RAMSTKBaseTable):
    """Contain the attributes and methods of the Validation table model."""

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

    def __init__(self, **kwargs: Dict[Any, Union[float, int, str]]) -> None:
        """Initialize a RAMSTKValidation table model instance."""
        super().__init__(**kwargs)

        # Initialize private dictionary attributes.
        self._dic_status: Dict[Any, float] = {}

        # Initialize private list attributes.
        self._lst_id_columns = [
            "revision_id",
            "validation_id",
            "parent_id",
            "record_id",
        ]

        # Initialize private scalar attributes.
        self._record: Type[RAMSTKValidationRecord] = RAMSTKValidationRecord

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.pkey = "validation_id"

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_calculate_plan, "request_calculate_plan")
        pub.subscribe(self._do_calculate_task, "request_calculate_validation_task")
        pub.subscribe(
            self._do_calculate_all_tasks,
            "request_calculate_all_validation_tasks",
        )

    # pylint: disable=method-hidden
    def do_get_new_record(
        self, attributes: Dict[str, Union[date, float, int, str]]
    ) -> RAMSTKValidationRecord:
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

    def do_calculate_plan(self) -> None:
        """Calculate the planned burndown of the overall validation effort.

        This method will calculate three values for each scheduled end date
        in the validation plan, the lower bound, average, and upper bound
        for the tasks planned to still be open on each of the scheduled end
        dates in the plan.

        :return: _planned; the pandas DataFrame() containing the planned
            burndown hours for the entire validation effort.
        """
        _dic_planned = {}  # type: ignore
        _time_ll = 0.0
        _time_mean = 0.0
        _time_ul = 0.0
        _start_date = date.today()

        for _node in self.tree.all_nodes()[1:]:
            # Calculate the three times if the mean task time is zero.
            if _node.data["validation"].time_mean <= 0.0:
                _node.data["validation"].calculate_task_time()

            # Keep a running total of the three times and the earliest task
            # start date.  The earliest start date will be assigned the
            # total number of hours in the validation program.
            _start_date = min(
                _start_date,
                pd.to_datetime(_node.data["validation"].date_start),
            )
            _time_ll += _node.data["validation"].time_ll
            _time_mean += _node.data["validation"].time_mean
            _time_ul += _node.data["validation"].time_ul

            # Calculate the sum of task hours for each, unique end date.
            _end_date = _node.data["validation"].date_end
            try:
                # Update the end date's times.
                _dic_planned[pd.to_datetime(_end_date)][0] += _node.data[
                    "validation"
                ].time_ll
                _dic_planned[pd.to_datetime(_end_date)][1] += _node.data[
                    "validation"
                ].time_mean
                _dic_planned[pd.to_datetime(_end_date)][2] += _node.data[
                    "validation"
                ].time_ul
            except KeyError:
                # Add the first time to the end date.
                _dic_planned[pd.to_datetime(_end_date)] = [
                    _node.data["validation"].time_ll,
                    _node.data["validation"].time_mean,
                    _node.data["validation"].time_ul,
                ]

        # Create a pandas DataFrame() of the task times sorted by date in
        # descending order.  The descending order is needed because the
        # ultimate DataFrame() will contain *remaining* total task hours for
        # the validation effort, not the total task hours planned to
        # complete on each day.
        # noinspection PyTypeChecker
        _planned = pd.DataFrame(
            _dic_planned.values(),
            index=_dic_planned.keys(),
            columns=["lower", "mean", "upper"],
        ).sort_index(ascending=False)

        # Calculate the total task time remaining on each planned end date
        # and then sort the DataFrame() by date in ascending order.
        _planned = _planned.cumsum() - _planned
        _planned.loc[_start_date] = [_time_ll, _time_mean, _time_ul]
        _planned = _planned.sort_index()

        _dic_plan = {
            "plan": _planned,
            "assessed": self._do_select_assessment_targets(),
        }

        pub.sendMessage(
            "succeed_calculate_verification_plan",
            attributes=_dic_plan,
        )

    def _do_calculate_all_tasks(self) -> None:
        """Calculate mean, standard error, and bounds on all task's time/cost.

        These values are calculated assuming a beta distribution (typical
        project management assumption).  This method also calculates the
        remaining average time and cost of the overall validation plan.

        :return: None
        :rtype: None
        """
        _program_cost_remaining = 0.0
        _program_time_remaining = 0.0

        for _node in self.tree.all_nodes()[1:]:
            self._do_calculate_task(_node.identifier)

            _program_cost_remaining += _node.data["validation"].cost_average * (
                1.0 - _node.data["validation"].status / 100.0
            )
            _program_time_remaining += _node.data["validation"].time_average * (
                1.0 - _node.data["validation"].status / 100.0
            )

        pub.sendMessage(
            "succeed_calculate_all_validation_tasks",
            tree=self.tree,
        )
        pub.sendMessage(
            "succeed_calculate_program_remaining",
            cost_remaining=_program_cost_remaining,
            time_remaining=_program_time_remaining,
        )

    def _do_calculate_task(self, node_id: int) -> None:
        """Calculate mean, standard error, and bounds on task time and cost.

        These values are calculated assuming a beta distribution (typical
        project management assumption).

        :param node_id: the ID of the node (task) to calculate.
        :return: None
        :rtype: None
        """
        _node = self.tree.get_node(node_id)

        _node.data["validation"].calculate_task_time()
        _node.data["validation"].calculate_task_cost()

        _attributes = _node.data["validation"].get_attributes()
        self.do_set_attributes_all(
            attributes=_attributes,
        )

        pub.sendMessage(
            "succeed_calculate_validation_task",
            attributes=_attributes,
        )

    def _do_select_assessment_targets(self) -> pd.DataFrame:
        """Select the targets for all tasks of Reliability Assessment type.

        :return: _assessed; a pandas DataFrame() containing the assessment
            dates as the index and associated targets.
        """
        _dic_assessed = {
            pd.to_datetime(_node.data["validation"].date_end): [
                _node.data["validation"].acceptable_minimum,
                _node.data["validation"].acceptable_mean,
                _node.data["validation"].acceptable_maximum,
            ]
            for _node in self.tree.all_nodes()[1:]
            if _node.data["validation"].task_type == 5
        }

        # noinspection PyTypeChecker
        return pd.DataFrame(
            _dic_assessed.values(),
            index=_dic_assessed.keys(),
            columns=["lower", "mean", "upper"],
        ).sort_index()
