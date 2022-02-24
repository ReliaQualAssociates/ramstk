# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Validation Panels."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Tuple, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKButton,
    RAMSTKComboBox,
    RAMSTKDateSelect,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKSpinButton,
    RAMSTKTextView,
    RAMSTKTreePanel,
)


class ValidationTreePanel(RAMSTKTreePanel):
    """Panel to display flat list of validation tasks."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_all_validation"
    _tag = "validation"
    _title = _("Verification Task List")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Validation panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self.tvwTreeView.dic_row_loader = {
            "validation": self.__do_load_validation,
        }

        # Initialize private list class attributes.
        self._lst_measurement_units: List[str] = []
        self._lst_verification_types: List[str] = []

        # Initialize private scalar class attributes.

        # Initialize public dictionary class attributes.
        self.dic_attribute_widget_map = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Revision ID"),
                "gint",
            ],
            "validation_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Validation ID"),
                "gint",
            ],
            "acceptable_maximum": [
                2,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Acceptable Max."),
                "gfloat",
            ],
            "acceptable_mean": [
                3,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Acceptable Mean"),
                "gfloat",
            ],
            "acceptable_minimum": [
                4,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Acceptable Min."),
                "gfloat",
            ],
            "acceptable_variance": [
                5,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Acceptable Variance"),
                "gfloat",
            ],
            "confidence": [
                6,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                95.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Confidence"),
                "gfloat",
            ],
            "cost_average": [
                7,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Expected Cost"),
                "gfloat",
            ],
            "cost_ll": [
                8,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Cost LCL"),
                "gfloat",
            ],
            "cost_maximum": [
                9,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Maximum Cost"),
                "gfloat",
            ],
            "cost_mean": [
                10,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mean Cost"),
                "gfloat",
            ],
            "cost_minimum": [
                11,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Minimum Cost"),
                "gfloat",
            ],
            "cost_ul": [
                12,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Cost UCL"),
                "gfloat",
            ],
            "cost_variance": [
                13,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Cost Vaiance"),
                "gfloat",
            ],
            "date_end": [
                14,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                date.today(),
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("End Date"),
                "gchararray",
            ],
            "date_start": [
                15,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                date.today(),
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Start Date"),
                "gchararray",
            ],
            "description": [
                16,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Task Description"),
                "gchararray",
            ],
            "measurement_unit": [
                17,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                "mvw_editing_validation",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Unit of Measure"),
                "gchararray",
            ],
            "name": [
                18,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Task Code"),
                "gchararray",
            ],
            "status": [
                19,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("% Complete"),
                "gfloat",
            ],
            "task_specification": [
                20,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Task Specification"),
                "gchararray",
            ],
            "task_type": [
                21,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                "mvw_editing_validation",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Task Type"),
                "gchararray",
            ],
            "time_average": [
                22,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Expected Task Time"),
                "gfloat",
            ],
            "time_ll": [
                23,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Task Time LCL"),
                "gfloat",
            ],
            "time_maximum": [
                24,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Maximum Task Time"),
                "gfloat",
            ],
            "time_mean": [
                25,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mean Task Time"),
                "gfloat",
            ],
            "time_minimum": [
                26,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Minimum Task Time"),
                "gfloat",
            ],
            "time_ul": [
                27,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Task Time UCL"),
                "gfloat",
            ],
            "time_variance": [
                28,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_validation",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Task Time Variance"),
                "gfloat",
            ],
        }

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of validations.")
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().do_load_panel,
            "succeed_calculate_all_validation_tasks",
        )

        pub.subscribe(
            self._on_module_switch,
            "mvwSwitchedPage",
        )
        pub.subscribe(
            self._on_workview_edit,
            f"wvw_editing_{self._tag}",
        )

    def do_load_measurement_units(
        self, measurement_unit: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the verification task measurement unit list.

        :param measurement_unit: the dict containing the units of measure.
        :return: None
        """
        self._lst_measurement_units = [""]

        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["measurement_unit"]
        ).get_cells()[0]
        _cell.set_property("has-entry", False)
        _cellmodel = _cell.get_property("model")
        _cellmodel.clear()
        _cellmodel.append([""])

        # pylint: disable=unused-variable
        for _key, value in measurement_unit.items():
            self._lst_measurement_units.append(measurement_unit[_key][1])
            _cellmodel.append([value[1]])

    def do_load_verification_types(
        self, verification_type: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the verification task type list.

        :param verification_type: the dict containing the verification task
            types.
        :return: None
        """
        self._lst_verification_types = [""]

        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["task_type"]
        ).get_cells()[0]
        _cell.set_property("has-entry", False)
        _cellmodel = _cell.get_property("model")
        _cellmodel.clear()
        _cellmodel.append([""])

        # pylint: disable=unused-variable
        for _key, value in verification_type.items():
            self._lst_verification_types.append(verification_type[_key][1])
            _cellmodel.append([value[1]])

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to change in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _code = _model.get_value(_row, self.tvwTreeView.position["validation_id"])
            _name = _model.get_value(_row, self.tvwTreeView.position["name"])
            _title = _(f"Analyzing Validation Task {_code}: {_name}")

            pub.sendMessage("request_set_title", title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Validation Module View RAMSTKTreeView().

        This method is called whenever a Validation Module View
        RAMSTKTreeView() row is activated/changed.

        :param selection: the Validation class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["validation_id"]

            _attributes["measurement_unit"] = self._lst_measurement_units.index(
                _attributes["measurement_unit"]
            )
            _attributes["task_type"] = self._lst_verification_types.index(
                _attributes["task_type"]
            )

            _title = _(f"Analyzing Verification Task {_attributes['name']}")

            pub.sendMessage(
                "selected_validation",
                attributes=_attributes,
            )
            pub.sendMessage(
                "request_set_title",
                title=_title,
            )

    def _on_workview_edit(
        self, node_id: int, package: Dict[str, Union[bool, float, int, str]]
    ) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

        This is a wrapper for the metaclass method do_refresh_tree().  It is
        necessary to handle RAMSTKComboBox() changes because the package value will
        be an integer and the Gtk.CellRendererCombo() needs a string input to update.

        :param node_id: the ID of the validation task being edited.
        :param package: the key:value for the data being updated.
        :return: None
        """
        [[_key, _value]] = package.items()

        _column = self.tvwTreeView.get_column(self.tvwTreeView.position[_key])
        _cell = _column.get_cells()[-1]

        if isinstance(_cell, Gtk.CellRendererCombo):
            if _key == "measurement_unit":
                package[_key] = self._lst_measurement_units[_value]
            elif _key == "task_type":
                package[_key] = self._lst_verification_types[_value]

            super().do_refresh_tree(node_id, package)

    def __do_load_validation(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a verification task into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the task to load into the validation tree.
        :return: _new_row; the row that was just populated with validation data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None
        _date_format = "%Y-%m-%d"

        # pylint: disable=unused-variable
        _entity = node.data["validation"]

        _attributes = [
            _entity.revision_id,
            _entity.validation_id,
            _entity.acceptable_maximum,
            _entity.acceptable_mean,
            _entity.acceptable_minimum,
            _entity.acceptable_variance,
            _entity.confidence,
            _entity.cost_average,
            _entity.cost_ll,
            _entity.cost_maximum,
            _entity.cost_mean,
            _entity.cost_minimum,
            _entity.cost_ul,
            _entity.cost_variance,
            _entity.date_end.strftime(_date_format),
            _entity.date_start.strftime(_date_format),
            _entity.description,
            self._lst_measurement_units[_entity.measurement_unit],
            _entity.name,
            _entity.status,
            _entity.task_specification,
            self._lst_verification_types[_entity.task_type],
            _entity.time_average,
            _entity.time_ll,
            _entity.time_maximum,
            _entity.time_mean,
            _entity.time_minimum,
            _entity.time_ul,
            _entity.time_variance,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _message = _(
                f"An error occurred when loading verification task {node.identifier} "
                f"into the verification tree.  This might indicate it was missing it's "
                f"data package, some of the data in the package was missing, or "
                f"some of the data was the wrong type.  Row data was: "
                f"{_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg",
                logger_name="WARNING",
                message=_message,
            )

        return _new_row


class ValidationTaskDescriptionPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Validation task."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "validation_id"
    _select_msg = "selected_validation"
    _tag = "validation"
    _title = _("Verification Task Description")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Validation Task Description panel."""
        super().__init__()

        # Initialize widgets.
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

        # Initialize private dict instance attributes.
        self._dic_task_types: Dict[int, List[str]] = {}
        self._dic_units: Dict[int, str] = {}

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "validation_id": [
                1,
                self.txtTaskID,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 50,
                    "editable": False,
                },
                _("Task ID:"),
                "gint",
            ],
            "name": [
                18,
                self.txtCode,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                "",
                {
                    "width": 50,
                    "editable": False,
                    "tooltip": _("Displays the ID of the selected V&amp;V activity."),
                },
                _("Task Code:"),
                "gchararray",
            ],
            "description": [
                16,
                self.txtTask,
                "changed",
                super().on_changed_textview,
                "wvw_editing_validation",
                "",
                {
                    "height": 100,
                    "width": 500,
                    "tooltip": _(
                        "Displays the description of the selected V&amp;V activity."
                    ),
                },
                _("Task Description:"),
                "gchararray",
            ],
            "task_type": [
                21,
                self.cmbTaskType,
                "changed",
                super().on_changed_combo,
                "wvw_editing_validation",
                "",
                {
                    "tooltip": _(
                        "Selects and displays the type of task for the selected "
                        "V&amp;V activity."
                    ),
                },
                _("Task Type:"),
                "gint",
            ],
            "task_specification": [
                20,
                self.txtSpecification,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                "",
                {
                    "tooltip": _(
                        "Displays the internal or industry specification or procedure "
                        "governing the selected V&amp;V activity."
                    ),
                },
                _("Specification:"),
                "gchararray",
            ],
            "measurement_unit": [
                17,
                self.cmbMeasurementUnit,
                "changed",
                super().on_changed_combo,
                "wvw_editing_validation",
                "",
                {
                    "tooltip": _(
                        "Selects and displays the measurement unit for the selected "
                        "V&amp;V activity acceptance parameter."
                    ),
                },
                _("Measurement Unit:"),
                "gint",
            ],
            "acceptable_minimum": [
                4,
                self.txtMinAcceptable,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _(
                        "Displays the minimum acceptable value for the selected "
                        "V&amp;V activity."
                    ),
                },
                _("Min. Acceptable:"),
                "gfloat",
            ],
            "acceptable_maximum": [
                2,
                self.txtMaxAcceptable,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _(
                        "Displays the maximum acceptable value for the selected "
                        "V&amp;V activity."
                    ),
                },
                _("Max. Acceptable:"),
                "gfloat",
            ],
            "acceptable_mean": [
                3,
                self.txtMeanAcceptable,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _(
                        "Displays the mean acceptable value for the selected V&amp;V "
                        "activity."
                    ),
                },
                _("Mean Acceptable:"),
                "gfloat",
            ],
            "acceptable_variance": [
                5,
                self.txtVarAcceptable,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _(
                        "Displays the acceptable variance for the selected V&amp;V "
                        "activity."
                    ),
                },
                _("Variance:"),
                "gfloat",
            ],
            "date_start": [
                15,
                self.txtStartDate,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                date.today(),
                {
                    "width": 100,
                    "tooltip": _(
                        "Displays the date the selected V&amp;V activity is scheduled "
                        "to start."
                    ),
                },
                _("Start Date:"),
                "gchararray",
            ],
            "date_end": [
                14,
                self.txtEndDate,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                date.today(),
                {
                    "width": 100,
                    "tooltip": _(
                        "Displays the date the selected V&amp;V activity is scheduled "
                        "to end."
                    ),
                },
                _("Start End:"),
                "gchararray",
            ],
            "status": [
                19,
                self.spnStatus,
                "value-changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "limits": [0, 0, 100, 1, 0.1],
                    "numeric": True,
                    "ticks": True,
                    "tooltip": _(
                        "Displays % complete of the selected V&amp;V activity."
                    ),
                },
                _("% Complete:"),
                "gfloat",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.btnEndDate.connect(
            "button-release-event", self._do_select_date, self.txtEndDate
        )
        self.btnStartDate.connect(
            "button-release-event", self._do_select_date, self.txtStartDate
        )
        self.cmbTaskType.connect("changed", self._do_make_task_code)

        # Subscribe to PyPubSub messages.

    def do_load_measurement_units(
        self, measurement_unit: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the measurement units RAMSTKComboBox().

        :param measurement_unit: the list of measurement units to load.  The
            key is an integer representing the ID field in the database.  The
            value is a tuple with a unit abbreviation, unit name, and generic
            unit type.  For example:

            ('lbf', 'Pounds Force', 'unit')

        :return: None
        :rtype: None
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
        """Load the validation task types RAMSTKComboBox().

        :param validation_type: a dict of validation task types.  The key is an
            integer representing the ID field in the database.  The value is a
            tuple with a task code, task name, and generic task type.  For
            example:

            ('RAA', 'Reliability, Assessment', 'validation')

        :return: None
        :rtype: None
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

        This method builds the task code based on the task type and the task
        ID.  The code created has the form:

            task type 3-letter abbreviation-task ID

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        :rtype: None
        """
        try:
            _index = combo.get_active()

            _task_type = self._dic_task_types[_index][0]
            _task_code = f"{_task_type}-{self._record_id:04d}"

            self.txtCode.do_update(str(_task_code), signal="changed")

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

        :param __button: the ramstk.RAMSTKButton() that called this method.
        :type __button: :class:`ramstk.gui.gtk.ramstk.RAMSTKButton`
        :param __event: the Gdk.Event() that called this method.
        :type __event: :class:`Gdk.Event`
        :param entry: the Gtk.Entry() that the new date should be displayed in.
        :type entry: :class:`Gtk.Entry`
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _dialog: RAMSTKDateSelect = RAMSTKDateSelect()

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.set_text(str(_date))

        return _date


class ValidationTaskEffortPanel(RAMSTKFixedPanel):
    """Panel to display effort data about the selected Validation task."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "validation_id"
    _select_msg = "selected_validation"
    _tag = "validation"
    _title = _("Verification Task Effort")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

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

        # Initialize private dict instance attributes.
        self._dic_task_types: Dict[int, List[str]] = {}

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map = {
            "time_minimum": [
                26,
                self.txtMinTime,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _(
                        "Minimum person-time needed to complete the selected task."
                    ),
                },
                _("Min. Task Time:"),
                "gfloat",
            ],
            "time_average": [
                22,
                self.txtExpTime,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _(
                        "Most likely person-time needed to complete the selected task."
                    ),
                },
                _("Most Likely Task Time:"),
                "gfloat",
            ],
            "time_maximum": [
                24,
                self.txtMaxTime,
                "changed",
                super().on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _(
                        "Maximum person-time needed to complete the selected task."
                    ),
                },
                _("Max. Task Time:"),
                "gfloat",
            ],
            "time_ll": [
                23,
                self.txtMeanTimeLL,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "editable": False,
                },
                "",
                "gfloat",
            ],
            "time_mean": [
                25,
                self.txtMeanTime,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "editable": False,
                },
                _("Task Time (95% Confidence):"),
                "gfloat",
            ],
            "time_ul": [
                27,
                self.txtMeanTimeUL,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "editable": False,
                },
                "",
                "gfloat",
            ],
            "cost_minimum": [
                11,
                self.txtMinCost,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _("Minimim cost of the selected task."),
                },
                _("Min. Task Cost:"),
                "gfloat",
            ],
            "cost_average": [
                7,
                self.txtExpCost,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _("Most likely cost of the selected task."),
                },
                _("Most Likely Task Cost:"),
                "gfloat",
            ],
            "cost_maximum": [
                9,
                self.txtMaxCost,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "tooltip": _("Maximum cost of the selected task."),
                },
                _("Max. Task Cost:"),
                "gfloat",
            ],
            "cost_ll": [
                8,
                self.txtMeanCostLL,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "editable": False,
                },
                "",
                "gfloat",
            ],
            "cost_mean": [
                10,
                self.txtMeanCost,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "editable": False,
                },
                _("Task Cost (95% Confidence):"),
                "gfloat",
            ],
            "cost_ul": [
                12,
                self.txtMeanCostUL,
                "changed",
                self.on_changed_entry,
                "wvw_editing_validation",
                0.0,
                {
                    "width": 100,
                    "editable": False,
                },
                "",
                "gfloat",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        self.__do_adjust_widgets()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_calculate_task, "succeed_calculate_validation_task")

    def do_load_validation_types(
        self, validation_type: Dict[int, Tuple[str, str]]
    ) -> None:
        """Load the validation task types RAMSTKComboBox().

        :param validation_type: a dict of validation task types.  The key is an
            integer representing the ID field in the database.  The value is a
            tuple with a task code, task name, and generic task type.  For
            example:

            ('RAA', 'Reliability, Assessment', 'validation')

        :return: None
        :rtype: None
        """
        for _index, _key in enumerate(validation_type):
            self._dic_task_types[_index + 1] = [
                validation_type[_key][0],
                validation_type[_key][1],
            ]

    def _do_load_code(self, task_code: int) -> None:
        """Load the Validation code RAMSTKEntry().

        :param task_code: the Validation code to load.
        :return: None
        :rtype: None
        """
        self.txtCode.do_update(str(task_code), signal="changed")

    def _do_make_task_code(self, task_type: str) -> str:
        """Create the validation task code.

        This method builds the task code based on the task type and the task
        ID.  The code created has the form:

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

        :param __button: the ramstk.RAMSTKButton() that called this method.
        :type __button: :class:`ramstk.gui.gtk.ramstk.RAMSTKButton`
        :param __event: the Gdk.Event() that called this method.
        :type __event: :class:`Gdk.Event`
        :param entry: the Gtk.Entry() that the new date should be displayed in.
        :type entry: :class:`Gtk.Entry`
        :return: _date; the date in ISO-8601 (YYYY-mm-dd) format.
        :rtype: str
        """
        _dialog: RAMSTKDateSelect = RAMSTKDateSelect()

        _date = _dialog.do_run()
        _dialog.do_destroy()

        entry.set_text(str(_date))

        return _date

    def _on_calculate_task(self, attributes: Dict[str, Union[float, int, str]]) -> None:
        """Wrap _do_load_panel() on successful task calculation.

        :param attributes: the verification task attribute dict.
        :return: None
        :rtype: None
        """
        if attributes["validation_id"] == self._record_id:
            super().do_load_panel(attributes)

    def __do_adjust_widgets(self) -> None:
        """Adjust position of some widgets.

        :return: None
        :rtype: None
        """
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
