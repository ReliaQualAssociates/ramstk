# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.task_effort_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The ValidationTaskEffortPanel module."""

# Standard Library Imports
from typing import Dict, List, Tuple, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton,
    RAMSTKDateSelectDialog,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class ValidationTaskEffortPanel(RAMSTKFixedPanel):
    """Panel to display effort data about the selected Validation task."""

    # Define private class attributes.
    _record_field = "validation_id"
    _select_msg = "selected_validation"
    _tag = "validation"
    _title = _("Verification Task Effort")

    def __init__(self) -> None:
        """Initialize an instance of the Validation Task Effort panel."""
        super().__init__()

        # Initialize widgets.
        self.txtMinTime: RAMSTKEntry = RAMSTKEntry()
        self.txtExpTime: RAMSTKEntry = RAMSTKEntry()
        self.txtMaxTime: RAMSTKEntry = RAMSTKEntry()
        self.txtMinCost: RAMSTKEntry = RAMSTKEntry()
        self.txtExpCost: RAMSTKEntry = RAMSTKEntry()
        self.txtMaxCost: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanTimeLL: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanTime: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanTimeUL: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanCostLL: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanCost: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanCostUL: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._dic_task_types: Dict[int, List[str]] = {}
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.txtMinTime,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_minimum",
                    "index": 26,
                    "label_text": _("Min. Task Time:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "Minimum person-time needed to complete the selected task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtExpTime,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_average",
                    "index": 22,
                    "label_text": _("Most Likely Task Time:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "Most likely person-time needed to complete the selected task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMaxTime,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_maximum",
                    "index": 24,
                    "label_text": _("Max. Task Time:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "Maximum person-time needed to complete the selected task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMeanTimeLL,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_ll",
                    "index": 23,
                    "label_text": "",
                    "listen_topic": "mvw_editing_validation",
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "The calculated lower confidence limit on the time needed to "
                        "complete the selected task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMeanTime,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_mean",
                    "index": 25,
                    "label_text": _("Task Time (95% Confidence):"),
                    "listen_topic": "mvw_editing_validation",
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "The calculated mean for the time needed to complete the "
                        "selected task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMeanTimeUL,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "time_ul",
                    "index": 25,
                    "label_text": "",
                    "listen_topic": "mvw_editing_validation",
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "The calculated upper confidence limit on the time needed to "
                        "complete the selected task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMinCost,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_minimum",
                    "index": 11,
                    "label_text": _("Min. Task Cost:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                {
                    "editable": True,
                    "tooltip": _("Minimum cost to complete the selected task."),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtExpCost,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_average",
                    "index": 7,
                    "label_text": _("Most Likely Task Cost:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                {
                    "editable": True,
                    "tooltip": _("Most likely cost to complete the selected task."),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMaxCost,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_maximum",
                    "index": 9,
                    "label_text": _("Max. Task Cost:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                {
                    "editable": True,
                    "tooltip": _("Maximum cost to complete the selected task."),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMeanCostLL,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_ll",
                    "index": 8,
                    "label_text": "",
                    "listen_topic": "mvw_editing_validation",
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "The calculated lower confidence limit on the cost to complete "
                        "the selected task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMeanCost,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_mean",
                    "index": 10,
                    "label_text": _("Task Cost (95% Confidence):"),
                    "listen_topic": "mvw_editing_validation",
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "The calculated mean for the cost to complete the selected "
                        "task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
            make_widget_config(
                self.txtMeanCostUL,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_ul",
                    "index": 12,
                    "label_text": "",
                    "listen_topic": "mvw_editing_validation",
                },
                {
                    "editable": False,
                    "tooltip": _(
                        "The calculated upper confidence limit on the cost to complete "
                        "the selected task."
                    ),
                    "visible": True,
                    "width_request": 100,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        self.__do_adjust_widgets()
        super().do_set_widget_callbacks()

        # Subscribe to PyPubSub messages.
        self._do_subscribe_to_messages()

    def do_load_validation_types(
        self, validation_type: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the validation task types RAMSTKComboBox.

        :param validation_type: a dict of validation task types.  The key is an
            integer representing the ID field in the database.  The value is a
            tuple with a task code, task name, and generic task type.  For
            example:

            ('RAA', 'Reliability, Assessment', 'validation')
        """
        for _index, _key in enumerate(validation_type):
            self._dic_task_types[_index + 1] = [
                validation_type[_key][0],
                validation_type[_key][1],
            ]

    def _do_load_code(self, task_code: int) -> None:
        """Load the Validation code RAMSTKEntry.

        :param task_code: the Validation code to load.
        """
        self.txtCode.do_update(str(task_code), signal="changed")

    def _do_make_task_code(self, task_type: str) -> str:
        """Create the validation task code.

        This method builds the task code based on the task type and the task ID.  The
        code created has the form:

        task type 3-letter abbreviation-task ID

        :param task_type: the three letter abbreviation for the task type.
        :return: _code
        :rtype: str
        """
        _code = ""

        # pylint: disable=unused-variable
        for __, _type in self._dic_task_types.items():
            if _type[1] == task_type:
                _code = f"{_type[0]}-{self._record_id:04d}"

        pub.sendMessage(
            "wvw_editing_validation",
            node_id=self._record_id,
            package={"name": _code},
        )

        return _code

    @staticmethod
    def _do_select_date(
        __button: RAMSTKButton, __event: Gdk.Event, entry: RAMSTKEntry
    ) -> str:
        """Request to launch a date selection dialog.

        This method is used to select the validation date for the Validation.

        :param __button: the RAMSTKButton that called this method.
        :param __event: the Gdk.Event that called this method.
        :param entry: the RAMSTKEntry that the new date should be displayed in.
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _parent = (
            entry.get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
            .get_parent()
        )

        _dialog: RAMSTKDateSelectDialog = RAMSTKDateSelectDialog(
            _("Select Date"),
            _parent,
        )

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.set_text(str(_date))

        return _date

    def _do_subscribe_to_messages(self) -> None:
        """Subscribe to PyPubSub messages."""
        pub.subscribe(
            self._on_calculate_task,
            "succeed_calculate_validation_task",
        )

    def _on_calculate_task(self, attributes: Dict[str, Union[float, int, str]]) -> None:
        """Wrap do_load_panel on successful task calculation.

        :param attributes: the verification task attribute dict.
        """
        if attributes["validation_id"] == self._record_id:
            super().do_load_panel(attributes)

    def __do_adjust_widgets(self) -> None:
        """Adjust position of some widgets."""
        _fixed: Gtk.Fixed = self.get_children()[0].get_children()[0].get_children()[0]

        _time_entry: RAMSTKEntry = _fixed.get_children()[9]
        _cost_entry: RAMSTKEntry = _fixed.get_children()[21]

        # We add the mean time and mean time UL to the same y position as
        # the mean time LL widget.
        _x_pos: int = _fixed.child_get_property(_time_entry, "x")
        _y_pos: int = _fixed.child_get_property(_time_entry, "y")
        _fixed.move(self.txtMeanTimeLL, _x_pos, _y_pos)
        _fixed.move(self.txtMeanTime, _x_pos + 175, _y_pos)
        _fixed.move(self.txtMeanTimeUL, _x_pos + 350, _y_pos)

        # We add the mean cost and mean cost UL to the same y position as
        # the mean cost LL widget.
        _x_pos = _fixed.child_get_property(_cost_entry, "x")
        _y_pos = _fixed.child_get_property(_cost_entry, "y")
        _fixed.move(self.txtMeanCostLL, _x_pos, _y_pos)
        _fixed.move(self.txtMeanCost, _x_pos + 175, _y_pos)
        _fixed.move(self.txtMeanCostUL, _x_pos + 350, _y_pos)
