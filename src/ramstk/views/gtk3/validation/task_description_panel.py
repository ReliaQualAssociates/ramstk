# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.task_description_panel.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The ValidationTaskDescriptionPanel module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Tuple

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton,
    RAMSTKComboBox,
    RAMSTKDateSelectDialog,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKSpinButton,
    RAMSTKTextView,
    WidgetConfig,
)


class ValidationTaskDescriptionPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Validation task."""

    # Define private class attributes.
    _record_field = "validation_id"
    _select_msg = "selected_validation"
    _tag = "validation"
    _title = _("Verification Task Description")

    def __init__(self) -> None:
        """Initialize an instance of the Validation Task Description panel."""
        super().__init__()

        # Initialize child widgets.
        self.btnEndDate: RAMSTKButton = RAMSTKButton()
        self.btnStartDate: RAMSTKButton = RAMSTKButton()
        self.cmbTaskType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbMeasurementUnit: RAMSTKComboBox = RAMSTKComboBox()
        self.spnStatus: RAMSTKSpinButton = RAMSTKSpinButton()
        self.txtTaskID: RAMSTKEntry = RAMSTKEntry()
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtMaxAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtMeanAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtMinAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtVarAcceptable: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()
        self.txtTask: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtEndDate: RAMSTKEntry = RAMSTKEntry()
        self.txtStartDate: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._dic_task_types: Dict[int, List[str]] = {}
        self._dic_units: Dict[int, str] = {}
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.txtTaskID,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "validation_id",
                    "index": 1,
                    "label_text": _("Task ID:"),
                    "listen_topic": "mvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "width_request": 50,
                },
            },
            {
                "widget": self.txtCode,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "name",
                    "index": 2,
                    "label_text": _("Task Code"),
                    "listen_topic": "mvw_editing_validation",
                },
                "properties": {
                    "editable": False,
                    "width_request": 50,
                },
            },
            {
                "widget": self.txtTask,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 16,
                    "label_text": _("Task Description"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "height_request": 100,
                    "tooltip": _(
                        "Displays the description of the selected V&amp;V activity."
                    ),
                    "width_request": 500,
                },
            },
            {
                "widget": self.cmbTaskType,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "task_type",
                    "index": 21,
                    "label_text": _("Task Type"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Selects and displays the type of task for the selected "
                        "V&amp;V activity."
                    ),
                },
            },
            {
                "widget": self.txtSpecification,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "task_specification",
                    "index": 20,
                    "label_text": _("Specification:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Displays the internal or industry specification or procedure "
                        "governing the selected V&amp;V activity."
                    ),
                },
            },
            {
                "widget": self.cmbMeasurementUnit,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "measurement_unit",
                    "index": 17,
                    "label_text": _("Measurement Unit:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Selects and displays the measurement unit for the selected "
                        "V&amp;V activity acceptance parameter."
                    ),
                },
            },
            {
                "widget": self.txtMinAcceptable,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "acceptable_minimum",
                    "index": 4,
                    "label_text": _("Min. Acceptable:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Displays the minimum acceptable value for the selected "
                        "V&amp;V activity."
                    ),
                    "width_request": 100,
                },
            },
            {
                "widget": self.txtMaxAcceptable,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "acceptable_maximum",
                    "index": 2,
                    "label_text": "Max. Acceptable:",
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Displays the maximum acceptable value for the selected "
                        "V&amp;V activity."
                    ),
                    "width_request": 100,
                },
            },
            {
                "widget": self.txtMeanAcceptable,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "acceptable_mean",
                    "index": 3,
                    "label_text": _("Mean Acceptable:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Displays the mean acceptable value for the selected V&amp;V "
                        "activity."
                    ),
                    "width_request": 100,
                },
            },
            {
                "widget": self.txtVarAcceptable,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "acceptable_variance",
                    "index": 5,
                    "label_text": _("Variance:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Displays the acceptable variance for the selected V&amp;V "
                        "activity."
                    ),
                    "width_request": 100,
                },
            },
            {
                "widget": self.txtStartDate,
                "attributes": {
                    "datatype": "gchararray",
                    "default": date.today(),
                    "field": "date_start",
                    "index": 15,
                    "label_text": _("Start Date:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Displays the date the selected V&amp;V activity is scheduled "
                        "to start."
                    ),
                    "width_request": 100,
                },
            },
            {
                "widget": self.txtEndDate,
                "attributes": {
                    "datatype": "gchararray",
                    "default": date.today(),
                    "field": "date_end",
                    "index": 14,
                    "label_text": _("Date End:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "tooltip": _(
                        "Displays the date the selected V&amp;V activity is scheduled "
                        "to end."
                    ),
                    "width_request": 100,
                },
            },
            {
                "widget": self.spnStatus,
                "attributes": {
                    "datatype": "float",
                    "default": 0.0,
                    "field": "status",
                    "index": 19,
                    "label_text": _("% Complete:"),
                    "listen_topic": "mvw_editing_validation",
                    "send_topic": "wvw_editing_validation",
                },
                "properties": {
                    "lower": 0.0,
                    "numeric": True,
                    "page_increment": 0.1,
                    "page_size": 1.0,
                    "step_increment": 1.0,
                    "ticks": True,
                    "tooltip": _(
                        "Displays % complete of the selected V&amp;V activity."
                    ),
                    "upper": 100.0,
                },
            },
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        self._do_set_widget_callbacks()

    def do_load_measurement_units(
        self, measurement_unit: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the measurement units RAMSTKComboBox.

        :param measurement_unit: the list of measurement units to load. The key is an
            integer representing the ID field in the database. The value is a tuple with
            a unit abbreviation, unit name, and generic unit type. For example: ('lbf',
            'Pounds Force', 'unit')
        """
        _model = self.cmbMeasurementUnit.get_model()
        _model.clear()

        _units = []
        for _index, _key in enumerate(measurement_unit):
            self._dic_units[_index + 1] = measurement_unit[_key][1]
            _units.append([measurement_unit[_key][1]])
        self.cmbMeasurementUnit.do_load_combo(entries=_units)

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
        _model = self.cmbTaskType.get_model()
        _model.clear()

        _task_types = []
        for _index, _key in enumerate(validation_type):
            self._dic_task_types[_index + 1] = [
                validation_type[_key][0],
                validation_type[_key][1],
            ]
            _task_types.append([validation_type[_key][1]])
        self.cmbTaskType.do_load_combo(entries=_task_types)

    def _do_make_task_code(self, combo: RAMSTKComboBox) -> None:
        """Create the validation task code.

        This method builds the task code based on the task type and the task ID.  The
        code created has the form:

        task type 3-letter abbreviation-task ID

        :param combo: the RAMSTKComboBox that called this method.
        """
        try:
            _index = combo.get_active()

            _task_type = self._dic_task_types[_index][0]
            _task_code = f"{_task_type}-{self._record_id:04d}"

            self.txtCode.do_update({"task_code": str(_task_code)})

            pub.sendMessage(
                "wvw_editing_validation",
                node_id=self._record_id,
                package={"name": _task_code},
            )
        except (AttributeError, KeyError):
            pass

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

    def _do_set_widget_callbacks(self):
        """Set the callback methods for the RAMSTKValidationTaskDescriptionPanel."""
        super().do_set_widget_callbacks()

        self.btnEndDate.connect(
            "button-release-event", self._do_select_date, self.txtEndDate
        )
        self.btnStartDate.connect(
            "button-release-event", self._do_select_date, self.txtStartDate
        )
        self.cmbTaskType.connect("changed", self._do_make_task_code)
