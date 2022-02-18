# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.pof.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 PoF Panels."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel


class PoFTreePanel(RAMSTKTreePanel):
    """Panel to display Physics if Failure analysis worksheet."""

    # Define private dictionary class attributes.
    _dic_visible_mask: Dict[str, List[bool]] = {
        "mode": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
        ],
        "mechanism": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
        "opload": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            True,
            False,
        ],
        "opstress": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            True,
        ],
        "test_method": [
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
        ],
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_pof"
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
            "test_method": self.__do_load_test_method,
        }

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._filtered_tree = True
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        # Initialize public dictionary instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "hardware_id": [
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
                _("Hardware ID"),
                "gint",
            ],
            "mode_id": [
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
                _("Mode ID"),
                "gint",
            ],
            "mechanism_id": [
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
                _("Mechanism ID"),
                "gint",
            ],
            "opload_id": [
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
                _("Load ID"),
                "gint",
            ],
            "opstress_id": [
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
                _("Stress ID"),
                "gint",
            ],
            "test_method_id": [
                5,
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
                6,
                Gtk.CellRendererText(),
                "edited",
                self._on_cell_edit,
                "wvw_editing_pof",
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
                _("End Effect"),
                "gchararray",
            ],
            "severity_class": [
                8,
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
                9,
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
                10,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                "wvw_editing_opload",
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
                11,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                "wvw_editing_opstress",
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
                12,
                Gtk.CellRendererCombo(),
                "edited",
                super().on_cell_edit,
                "wvw_editing_opstress",
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
                13,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                "wvw_editing_test_method",
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
                14,
                Gtk.CellRendererSpin(),
                "edited",
                super().on_cell_edit,
                "wvw_editing_opload",
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
                15,
                Gtk.CellRendererText(),
                "edited",
                self._on_cell_edit,
                "wvw_editing_pof",
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
        pub.subscribe(super().do_load_panel, "succeed_retrieve_pof")

        pub.subscribe(self._on_select_hardware, "selected_hardware")

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool:
        """Filter PoF to show only those rows associated with the selected Hardware.

        :param model: the filtered model for the PoF RAMSTKTreeView.
        :param row: the iter to check against condition(s).
        :param data: unused in this method; required by Gtk.TreeModelFilter() widget.
        :return: True if row should be visible, False else.
        :rtype: bool
        """
        return model[row][0] == self._parent_id

    def do_get_pof_level(self, model: Gtk.TreeModel, row: Gtk.TreeIter) -> None:
        """Determine the FMEA level of the selected FMEA row.

        :param model: the FMEA Gtk.TreeModel().
        :param row: the selected Gtk.TreeIter() in the FMECA.
        :return: None
        :rtype: None
        """
        _cid = ""

        for _col in [1, 2, 3, 4, 5]:
            _cid = f"{_cid}{int(bool(model.get_value(row, _col)))}"

        self.level = {
            "10000": "mode",
            "11000": "mechanism",
            "11100": "opload",
            "11110": "opstress",
            "11101": "test_method",
        }[_cid]

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

    def _on_cell_edit(
        self,
        cell: Gtk.CellRenderer,
        path: str,
        new_text: str,
        key: str,
        message: str,
    ) -> None:
        """Handle edits of description column to ensure proper level is updated.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param key: the column key of the edited Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        """
        super().on_cell_edit(
            cell,
            path,
            new_text,
            key,
            f"wvw_editing_{self.level}",
        )

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the PoF Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param selection: the TreeSelection() of the currently
            selected row in the PoF RAMSTKTreeView().
        :return: None
        """
        _attributes = super().on_row_change(selection)
        _model, _row = selection.get_selected()

        if _row is not None:
            self.do_get_pof_level(_model, _row)
            super().do_set_visible_columns(_attributes)
            self._record_id = _attributes[f"{self.level}_id"]

    def _on_select_hardware(
        self, attributes: Dict[str, Union[int, float, str]]
    ) -> None:
        """Filter FMEA when Hardware is selected.

        :param attributes: the dict of attributes for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes["hardware_id"]
        self.tvwTreeView.filt_model.refilter()

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

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["mechanism"], 22, 22
        )

        _attributes = [
            _entity.hardware_id,
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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading failure mechanism {node.identifier} "
                f"in the physics of failure analysis.  This might indicate it was "
                f"missing it's data package, some of the data in the package was "
                f"missing, or some of the data was the wrong type.  Row data "
                f"was: {_attributes}"
            )
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

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["mode"], 22, 22)

        _attributes = [
            _entity.hardware_id,
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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading failure mode {node.identifier} in the "
                f"physics of failure analysis.  This might indicate it was missing "
                f"its data package, some of the data in the package was missing, or "
                f"some of the data was the wrong type.  Row data was: {_attributes}"
            )
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

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["opload"], 22, 22)

        _attributes = [
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.opload_id,
            0,
            0,
            _entity.description,
            "",
            "",
            0.0,
            _entity.damage_model,
            "",
            "",
            "",
            _entity.priority_id,
            "",
            _icon,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading operating load {node.identifier} in "
                f"the physics of failure analysis.  This might indicate it was "
                f"missing its data package, some of the data in the package was "
                f"missing, or some of the data was the wrong type.  Row data "
                f"was: {_attributes}"
            )
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

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["opstress"], 22, 22
        )

        _attributes = [
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.opload_id,
            _entity.opstress_id,
            0,
            _entity.description,
            "",
            "",
            0.0,
            "",
            _entity.measurable_parameter,
            _entity.load_history,
            "",
            0,
            _entity.remarks,
            _icon,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading operating stress {node.identifier} in "
                f"the physics of failure analysis.  This might indicate it was "
                f"missing its data package, some of the data in the package was "
                f"missing, or some of the data was the wrong type.  Row data "
                f"was: {_attributes}"
            )
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

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["test_method"], 22, 22
        )

        _attributes = [
            _entity.hardware_id,
            _entity.mode_id,
            _entity.mechanism_id,
            _entity.opload_id,
            0,
            _entity.test_method_id,
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
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                f"An error occurred when loading test method {node.identifier} in the "
                f"physics of failure analysis.  This might indicate it was missing its "
                f"data package, some of the data in the package was missing, or some "
                f"of the data was the wrong type.  Row data was: {_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg", logger_name="WARNING", message=_message
            )

        return _new_row
