# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.pof.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 PoF Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel


class PoFTreePanel(RAMSTKTreePanel):
    """Panel to display Physics if Failure analysis worksheet."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_modes"
    _tag = "pof"
    _title = _("Physics of Failure (PoF) Analysis")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the PoF analysis worksheet."""
        super().__init__()

        # Initialize private dictionary instance attributes.
        self.tvwTreeView.dic_row_loader = {
            "mode": self.__do_load_mode,
            "mechanism": self.__do_load_mechanism,
            "opload": self.__do_load_opload,
            "opstress": self.__do_load_opstress,
            "method": self.__do_load_test_method,
        }
        self._dic_visible_mask: Dict[str, List[str]] = {
            "mode": [
                "True",
                "True",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
            ],
            "mechanism": [
                "True",
                "True",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
                "False",
            ],
            "opload": [
                "True",
                "True",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "False",
                "True",
                "False",
                "False",
            ],
            "opstress": [
                "True",
                "True",
                "True",
                "True",
                "True",
                "False",
                "True",
                "True",
                "False",
                "False",
                "True",
                "False",
            ],
            "testmethod": [
                "True",
                "True",
                "True",
                "True",
                "True",
                "False",
                "False",
                "False",
                "True",
                "False",
                "True",
                "False",
            ],
        }

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        # Initialize public dictionary instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "mode_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Mode ID"),
                "gint",
            ],
            "mechanism_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Mechanism ID"),
                "gint",
            ],
            "load_id": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Load ID"),
                "gint",
            ],
            "stress_id": [
                3,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Stress ID"),
                "gint",
            ],
            "test_id": [
                4,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Test ID"),
                "gint",
            ],
            "description": [
                5,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Description"),
                "gchararray",
            ],
            "effect_end": [
                6,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("End Effect"),
                "gchararray",
            ],
            "severity_class": [
                7,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Severity"),
                "gchararray",
            ],
            "mode_probability": [
                8,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mode Probability"),
                "gfloat",
            ],
            "damage_model": [
                9,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Damage Model"),
                "gchararray",
            ],
            "measurable_parameter": [
                10,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Measurable Parameter"),
                "gchararray",
            ],
            "load_history": [
                11,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Load History Method"),
                "gchararray",
            ],
            "boundary_conditions": [
                12,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Boundary Conditions"),
                "gchararray",
            ],
            "priority_id": [
                13,
                Gtk.CellRendererSpin(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Priority"),
                "gint",
            ],
            "remarks": [
                14,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Remarks"),
                "gchararray",
            ],
        }
        self.dic_icons: Dict[str, str] = {}

        # Initialize public list instance attributes.
        self.lst_damage_models: List[str] = []
        self.lst_load_history: List[str] = []
        self.lst_measurable_parameters: List[str] = []

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _(
                "Displays the Physics of Failure (PoF) Analysis for the currently "
                "selected hardware item."
            )
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, "succeed_delete_test_method")
        pub.subscribe(super().do_load_panel, "succeed_delete_opstress")
        pub.subscribe(super().do_load_panel, "succeed_delete_opload")
        pub.subscribe(super().do_load_panel, "succeed_delete_mechanism")
        pub.subscribe(super().do_load_panel, "succeed_delete_mode")
        pub.subscribe(super().do_load_panel, "succeed_insert_test_method")
        pub.subscribe(super().do_load_panel, "succeed_insert_opstress")
        pub.subscribe(super().do_load_panel, "succeed_insert_opload")
        pub.subscribe(super().do_load_panel, "succeed_insert_mechanism")
        pub.subscribe(super().do_load_panel, "succeed_insert_mode")

    def do_load_comboboxes(self) -> None:
        """Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.__do_load_damage_models()
        self.__do_load_measureable_parameters()
        self.__do_load_load_history()

        # Set the priority Gtk.CellRendererSpin()'s adjustment limits and
        # step increments.
        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["priority_id"]
        ).get_cells()[0]
        _adjustment = _cell.get_property("adjustment")
        _adjustment.configure(5, 1, 5, -1, 0, 0)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the PoF Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param selection: the TreeSelection() of the currently
            selected row in the PoF RAMSTKTreeView().
        :return: None
        """
        _model, _row = selection.get_selected()

        if _row is not None:
            if _model.get_value(_row, 0) == 0:
                _level = "mode"
            elif _model.get_value(_row, 1) == 0:
                _level = "mechanism"
            elif _model.get_value(_row, 2) == 0:
                _level = "load"
            elif _model.get_value(_row, 3) == 0:
                _level = "stress"
            else:
                _level = "test"

            self.tvwTreeView.visible = self._dic_visible_mask[_level]
            self.tvwTreeView.do_set_visible_columns()

    def __do_load_damage_models(self) -> None:
        """Load the RAMSTKTreeView() damage model CellRendererCombo().

        :return: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["damage_model"], self.lst_damage_models
        )

    def __do_load_load_history(self) -> None:
        """Load the operating load history CellRendererCombo().

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["load_history"], self.lst_load_history
        )

    def __do_load_measureable_parameters(self) -> None:
        """Load the measureable parameters CellRendererCombo().

        :return: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["measurable_parameter"],
            self.lst_measurable_parameters,
        )

    def __do_load_mechanism(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["mechanism"], 22, 22
        )

        _attributes = [
            _entity.mode_id,
            _entity.mechanism_id,
            0,
            0,
            0,
            _entity.description,
            "",
            "",
            0.0,
            "",
            "",
            "",
            "",
            0,
            "",
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure mechanism {0:s} in "
                "the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_mode(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mode record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["mode"], 22, 22)

        _attributes = [
            _entity.mode_id,
            0,
            0,
            0,
            0,
            _entity.description,
            _entity.effect_end,
            _entity.severity_class,
            _entity.mode_ratio,
            "",
            "",
            "",
            "",
            0,
            "",
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure mode {0:s} in the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_opload(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["opload"], 22, 22)

        _damage_model = self.dic_damage_models[_entity.damage_model]

        _attributes = [
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.load_id,
            0,
            0,
            _entity.description,
            "",
            "",
            0.0,
            _damage_model,
            "",
            "",
            "",
            _entity.priority_id,
            "",
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading operating load {0:s} in the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_opstress(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["opstress"], 22, 22
        )

        _load_history = self.dic_load_history[_entity.load_history]
        _measurable_parameter = self.dic_measurable_parameters[
            _entity.measurable_parameter
        ]

        _attributes = [
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.load_id,
            _entity.stress_id,
            0,
            _entity.description,
            "",
            "",
            0.0,
            "",
            _measurable_parameter,
            _load_history,
            "",
            0,
            _entity.remarks,
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading operating stress {0:s} in the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row

    def __do_load_test_method(
        self, node: treelib.Node, row: Gtk.TreeIter
    ) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :param row: the parent row of the mechanism to load into the FMEA form.
        :return: _new_row; the row that was just populated with mechanism data.
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["testmethod"], 22, 22
        )

        _attributes = [
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.load_id,
            _entity.stress_id,
            _entity.test_id,
            _entity.description,
            "",
            "",
            0.0,
            "",
            "",
            "",
            _entity.boundary_conditions,
            0,
            _entity.remarks,
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading test method {0:s} in the "
                "physics of failure analysis.  This might indicate it was "
                "missing it's data package, some of the data in the package "
                "was missing, or some of the data was the wrong type.  Row "
                "data was: {1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row
