# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.similar_item.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Similar Item Panels."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKFixedPanel, RAMSTKTreePanel


class SimilarItemMethodPanel(RAMSTKFixedPanel):
    """Panel to display Similar Item analysis methods."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "hardware_id"
    _select_msg = "succeed_get_similar_item_attributes"
    _tag = "similar_item"
    _title = _("Similar Item Method")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self):
        """Initialize an instance of the Similar Item methods panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbSimilarItemMethod: RAMSTKComboBox = RAMSTKComboBox()

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._method_id: int = 0
        self._on_edit_message = f"wvw_editing_{self._tag}"

        # Initialize public dictionary instance attributes.
        self.dic_attribute_widget_map = {
            "similar_item_method_id": [
                29,
                self.cmbSimilarItemMethod,
                "changed",
                super().on_changed_combo,
                self._on_edit_message,
                0,
                {
                    "tooltip": _("Select the similar item analysis method."),
                },
                _("Select Similar Item Method "),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.method_id: int = 0

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.cmbSimilarItemMethod.connect("changed", self._on_method_changed)

        # Subscribe to PyPubSub messages.

    def do_load_comboboxes(self) -> None:
        """Load Similar Item analysis RAMSTKComboBox()s.

        :return: None
        :rtype: None
        """
        self.cmbSimilarItemMethod.do_load_combo(
            [
                [_("Topic 633"), 0],
                [_("User-Defined"), 1],
            ],
            signal="changed",
        )

    def _do_set_sensitive(self, attributes: Dict[str, Union[int, float, str]]) -> None:
        """Set widget sensitivity as needed for the selected R(t) goal.

        :param attributes: the Similar Item attribute dict.
        :return: None
        :rtype: None
        """
        self.cmbSimilarItemMethod.set_sensitive(True)
        self.cmbSimilarItemMethod.do_update(
            attributes["similar_item_method_id"],
            signal="changed",
        )

    def _on_method_changed(self, combo: RAMSTKComboBox) -> None:
        """Let others know when similar item method combo changes.

        :param combo: the similar item calculation method RAMSTKComboBox().
        :return: None
        :rtype: None
        """
        self.method_id = combo.get_active()

        pub.sendMessage(
            "succeed_change_similar_item_method",
            method_id=self.method_id,
        )


class SimilarItemTreePanel(RAMSTKTreePanel):
    """Panel to display Similar Item analysis worksheet."""

    # Define private dict class attributes.

    # Define private list class attributes.
    _lst_environments: List[str] = [
        "",
        "Ground, Benign",
        "Ground,Mobile",
        "Naval, Sheltered",
        "Airborne, Inhabited, Cargo",
        "Airborne, Rotary Wing",
        "Space, Flight",
    ]
    _lst_qualities: List[str] = [
        "",
        "Space",
        "Full Military",
        "Ruggedized",
        "Commercial",
    ]

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_all_similar_item"
    _tag = "similar_item"
    _title = _("Similar Item Analysis")

    # Define public dictionary class attributes.

    # Define public dictionary list attributes.

    # Define public dictionary scalar attributes.

    # Define private dictionary class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Similar Item analysis worksheet."""
        super().__init__()

        # Initialize private dict instance attributes.
        self.tvwTreeView.dic_row_loader = {
            "similar_item": self.__do_load_similar_item,
        }
        self._dic_visible_mask: Dict[int, Dict[str, bool]] = {
            0: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "hazard_rate_active": True,
                "quality_from_id": False,
                "quality_to_id": False,
                "environment_from_id": False,
                "environment_to_id": False,
                "temperature_from": False,
                "temperature_to": False,
                "change_description_1": False,
                "change_factor_1": False,
                "change_description_2": False,
                "change_factor_2": False,
                "change_description_3": False,
                "change_factor_3": False,
                "change_description_4": False,
                "change_factor_4": False,
                "change_description_5": False,
                "change_factor_5": False,
                "change_description_6": False,
                "change_factor_6": False,
                "change_description_7": False,
                "change_factor_7": False,
                "change_description_8": False,
                "change_factor_8": False,
                "change_description_9": False,
                "change_factor_9": False,
                "change_description_10": False,
                "change_factor_10": False,
                "function_1": False,
                "function_2": False,
                "function_3": False,
                "function_4": False,
                "function_5": False,
                "result_1": True,
                "result_2": False,
                "result_3": False,
                "result_4": False,
                "result_5": False,
                "user_blob_1": False,
                "user_blob_2": False,
                "user_blob_3": False,
                "user_blob_4": False,
                "user_blob_5": False,
                "user_float_1": False,
                "user_float_2": False,
                "user_float_3": False,
                "user_float_4": False,
                "user_float_5": False,
                "user_int_1": False,
                "user_int_2": False,
                "user_int_3": False,
                "user_int_4": False,
                "user_int_5": False,
                "parent_id": False,
            },
            1: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "hazard_rate_active": True,
                "quality_from_id": True,
                "quality_to_id": True,
                "environment_from_id": True,
                "environment_to_id": True,
                "temperature_from": True,
                "temperature_to": True,
                "change_description_1": False,
                "change_factor_1": False,
                "change_description_2": False,
                "change_factor_2": False,
                "change_description_3": False,
                "change_factor_3": False,
                "change_description_4": False,
                "change_factor_4": False,
                "change_description_5": False,
                "change_factor_5": False,
                "change_description_6": False,
                "change_factor_6": False,
                "change_description_7": False,
                "change_factor_7": False,
                "change_description_8": False,
                "change_factor_8": False,
                "change_description_9": False,
                "change_factor_9": False,
                "change_description_10": False,
                "change_factor_10": False,
                "function_1": False,
                "function_2": False,
                "function_3": False,
                "function_4": False,
                "function_5": False,
                "result_1": True,
                "result_2": False,
                "result_3": False,
                "result_4": False,
                "result_5": False,
                "user_blob_1": False,
                "user_blob_2": False,
                "user_blob_3": False,
                "user_blob_4": False,
                "user_blob_5": False,
                "user_float_1": False,
                "user_float_2": False,
                "user_float_3": False,
                "user_float_4": False,
                "user_float_5": False,
                "user_int_1": False,
                "user_int_2": False,
                "user_int_3": False,
                "user_int_4": False,
                "user_int_5": False,
                "parent_id": False,
            },
            2: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "hazard_rate_active": True,
                "quality_from_id": False,
                "quality_to_id": False,
                "environment_from_id": False,
                "environment_to_id": False,
                "temperature_from": False,
                "temperature_to": False,
                "change_description_1": True,
                "change_factor_1": True,
                "change_description_2": True,
                "change_factor_2": True,
                "change_description_3": True,
                "change_factor_3": True,
                "change_description_4": True,
                "change_factor_4": True,
                "change_description_5": True,
                "change_factor_5": True,
                "change_description_6": True,
                "change_factor_6": True,
                "change_description_7": True,
                "change_factor_7": True,
                "change_description_8": True,
                "change_factor_8": True,
                "change_description_9": True,
                "change_factor_9": True,
                "change_description_10": True,
                "change_factor_10": True,
                "function_1": False,
                "function_2": False,
                "function_3": False,
                "function_4": False,
                "function_5": False,
                "result_1": True,
                "result_2": True,
                "result_3": True,
                "result_4": True,
                "result_5": True,
                "user_blob_1": True,
                "user_blob_2": True,
                "user_blob_3": True,
                "user_blob_4": True,
                "user_blob_5": True,
                "user_float_1": True,
                "user_float_2": True,
                "user_float_3": True,
                "user_float_4": True,
                "user_float_5": True,
                "user_int_1": True,
                "user_int_2": True,
                "user_int_3": True,
                "user_int_4": True,
                "user_int_5": True,
                "parent_id": False,
            },
        }

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._filtered_tree = True
        self._method_id: int = 0
        self._on_edit_message: str = f"mvw_editing_{self._tag}"

        # Initialize public dictionary instance attributes.
        self.dic_attribute_widget_map = {
            "revision_id": [
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
                _("Revision ID"),
                "gint",
            ],
            "hardware_id": [
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
                    "visible": True,
                },
                _("Hardware ID"),
                "gint",
            ],
            "name": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Assembly"),
                "gchararray",
            ],
            "hazard_rate_active": [
                3,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Current Hazard Rate"),
                "gfloat",
            ],
            "quality_from_id": [
                4,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("From Quality"),
                "gchararray",
            ],
            "quality_to_id": [
                5,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("To Quality"),
                "gchararray",
            ],
            "environment_from_id": [
                6,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("From Environment"),
                "gchararray",
            ],
            "environment_to_id": [
                7,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("To Environment"),
                "gchararray",
            ],
            "temperature_from": [
                8,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                25.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("From Temperature"),
                "gfloat",
            ],
            "temperature_to": [
                9,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                25.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("To Temperature"),
                "gfloat",
            ],
            "change_description_1": [
                10,
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
                _("Change Description 1"),
                "gchararray",
            ],
            "change_factor_1": [
                11,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Change Factor 1"),
                "gfloat",
            ],
            "change_description_2": [
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
                _("Change Description 2"),
                "gchararray",
            ],
            "change_factor_2": [
                13,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 2"),
                "gfloat",
            ],
            "change_description_3": [
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
                _("Change Description 3"),
                "gchararray",
            ],
            "change_factor_3": [
                15,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 3"),
                "gfloat",
            ],
            "change_description_4": [
                16,
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
                _("Change Description 4"),
                "gchararray",
            ],
            "change_factor_4": [
                17,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 4"),
                "gfloat",
            ],
            "change_description_5": [
                18,
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
                _("Change Description 5"),
                "gchararray",
            ],
            "change_factor_5": [
                19,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 5"),
                "gfloat",
            ],
            "change_description_6": [
                20,
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
                _("Change Description 6"),
                "gchararray",
            ],
            "change_factor_6": [
                21,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 6"),
                "gfloat",
            ],
            "change_description_7": [
                22,
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
                _("Change Description 7"),
                "gchararray",
            ],
            "change_factor_7": [
                23,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 7"),
                "gfloat",
            ],
            "change_description_8": [
                24,
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
                _("Change Description 8"),
                "gchararray",
            ],
            "change_factor_8": [
                25,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 8"),
                "gfloat",
            ],
            "change_description_9": [
                26,
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
                _("Change Description 9"),
                "gchararray",
            ],
            "change_factor_9": [
                27,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 9"),
                "gfloat",
            ],
            "change_description_10": [
                28,
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
                _("Change Description 10"),
                "gchararray",
            ],
            "change_factor_10": [
                29,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Change Factor 10"),
                "gfloat",
            ],
            "function_1": [
                30,
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
                _("Function 1"),
                "gchararray",
            ],
            "function_2": [
                31,
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
                _("Function 2"),
                "gchararray",
            ],
            "function_3": [
                32,
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
                _("Function 3"),
                "gchararray",
            ],
            "function_4": [
                33,
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
                _("Function 4"),
                "gchararray",
            ],
            "function_5": [
                34,
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
                _("Function 5"),
                "gchararray",
            ],
            "result_1": [
                35,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Result 1"),
                "gfloat",
            ],
            "result_2": [
                36,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Result 2"),
                "gfloat",
            ],
            "result_3": [
                37,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Result 3"),
                "gfloat",
            ],
            "result_4": [
                38,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Result 4"),
                "gfloat",
            ],
            "result_5": [
                39,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Result 5"),
                "gfloat",
            ],
            "user_blob_1": [
                40,
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
                _("User Text 1"),
                "gchararray",
            ],
            "user_blob_2": [
                41,
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
                _("User Text 2"),
                "gchararray",
            ],
            "user_blob_3": [
                42,
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
                _("User Text 3"),
                "gchararray",
            ],
            "user_blob_4": [
                43,
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
                _("User Text 4"),
                "gchararray",
            ],
            "user_blob_5": [
                44,
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
                _("User Text 5"),
                "gchararray",
            ],
            "user_float_1": [
                45,
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
                _("User Float 1"),
                "gfloat",
            ],
            "user_float_2": [
                46,
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
                _("User Float 2"),
                "gfloat",
            ],
            "user_float_3": [
                47,
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
                _("User Float 3"),
                "gfloat",
            ],
            "user_float_4": [
                48,
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
                _("User Float 4"),
                "gfloat",
            ],
            "user_float_5": [
                49,
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
                _("User Float 5"),
                "gfloat",
            ],
            "user_int_1": [
                50,
                Gtk.CellRendererText(),
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
                _("User Integer 1"),
                "gint",
            ],
            "user_int_2": [
                51,
                Gtk.CellRendererText(),
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
                _("User Integer 2"),
                "gint",
            ],
            "user_int_3": [
                52,
                Gtk.CellRendererText(),
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
                _("User Integer 3"),
                "gint",
            ],
            "user_int_4": [
                53,
                Gtk.CellRendererText(),
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
                _("User Integer 4"),
                "gint",
            ],
            "user_int_5": [
                54,
                Gtk.CellRendererText(),
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
                _("User Integer 5"),
                "gint",
            ],
            "parent_id": [
                55,
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
                _("Parent ID"),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _(
                "Displays the Similar Item Analysis for the currently selected "
                "Hardware item."
            )
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, "succeed_calculate_similar_item")
        pub.subscribe(self._do_set_hardware_attributes, "succeed_get_hardware_tree")
        pub.subscribe(
            self._do_set_reliability_attributes, "succeed_get_reliability_tree"
        )
        pub.subscribe(self._on_method_changed, "succeed_change_similar_item_method")
        pub.subscribe(self._on_select_hardware, "selected_hardware")

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool:
        """Filter Similar Item to show only those associated with the selected
        Hardware.

        :param model: the filtered model for the Similar Item RAMSTKTreeView.
        :param row: the iter to check against condition(s).
        :param data: unused in this method; required by Gtk.TreeModelFilter() widget.
        :return: True if row should be visible, False else.
        :rtype: bool
        """
        return model[row][55] == self._parent_id

    def do_load_comboboxes(self) -> None:
        """Load Similar Item analysis RAMSTKComboBox()s.

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["environment_from_id"],
            self._lst_environments,
        )
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["environment_to_id"],
            self._lst_environments,
        )
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["quality_from_id"],
            self._lst_qualities,
        )
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["quality_to_id"],
            self._lst_qualities,
        )

    def do_refresh_functions(self, row: Gtk.TreeIter, function: List[str]) -> None:
        """Refresh the Similar Item functions in the RAMSTKTreeView().

        :param row: the row in the Similar Item RAMSTKTreeView() whose
            functions need to be updated.  This is required to allow a recursive
            calling function to load the same function in all rows.
        :param function: the list of user-defined Similar Item functions.
        :return: None
        """
        _model = self.tvwTreeView.get_model()

        _model.set_value(row, self.tvwTreeView.position["function_1"], function[0])
        _model.set_value(row, self.tvwTreeView.position["function_2"], function[1])
        _model.set_value(row, self.tvwTreeView.position["function_3"], function[2])
        _model.set_value(row, self.tvwTreeView.position["function_4"], function[3])
        _model.set_value(row, self.tvwTreeView.position["function_5"], function[4])

    def _do_set_hardware_attributes(self, tree: treelib.Tree) -> None:
        """Set the attributes when the hardware tree is retrieved.

        :param tree: the hardware treelib.Tree().
        :return: None
        :rtype: None
        """
        for _node in tree.all_nodes()[1:]:
            _hardware = _node.data["hardware"]
            _row = self.tvwTreeView.do_get_row_by_value(1, _hardware.hardware_id)
            if _row is not None:
                self.tvwTreeView.unfilt_model.set_value(
                    _row,
                    2,
                    _hardware.name,
                )

    def _do_set_reliability_attributes(self, tree: treelib.Tree) -> None:
        """Set the attributes when the reliability tree is retrieved.

        :param tree: the reliability treelib.Tree().
        :return: None
        :rtype: None
        """
        for _node in tree.all_nodes()[1:]:
            _reliability = _node.data["reliability"]
            _row = self.tvwTreeView.do_get_row_by_value(1, _reliability.hardware_id)
            if _row is not None:
                self.tvwTreeView.unfilt_model.set_value(
                    _row,
                    3,
                    _reliability.hazard_rate_active,
                )

    def _on_method_changed(self, method_id: int) -> None:
        """Set method ID attributes when user changes the selection.

        :param method_id: the newly selected allocation method.
        :return: None
        :rtype: None
        """
        self._method_id = method_id
        self._do_set_columns_visible()

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Respond to user changing selected row in Similar Item worksheet.

        :param selection: the Gtk.TreeSelection() that is the newly selected row.
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["hardware_id"]

            pub.sendMessage(
                "selected_similar_item",
                attributes=_attributes,
            )

    def _do_set_columns_visible(self) -> None:
        """Set editable columns based on the Allocation method selected.

        :return: None
        :rtype: None
        """
        if self._method_id == -1:
            self._method_id = 0
        self.tvwTreeView.visible = self._dic_visible_mask[self._method_id]
        self.tvwTreeView.do_set_visible_columns()

    def _on_select_hardware(
        self, attributes: Dict[str, Union[int, float, str]]
    ) -> None:
        """Filter allocation list when Hardware is selected.

        :param attributes: the dict of attributes for the selected Hardware.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes["hardware_id"]
        self.tvwTreeView.filt_model.refilter()
        pub.sendMessage("request_get_similar_item_attributes", node_id=self._parent_id)

    def __do_load_similar_item(self, node: Any = "", row: Gtk.TreeIter = None) -> None:
        """Load the similar item RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the hardware tree.
        :return: _new_row; the row that was just populated with hardware data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _entity = node.data["similar_item"]

        if _entity.parent_id != 0:
            _attributes = [
                _entity.revision_id,
                _entity.hardware_id,
                "",
                0.0,
                self._lst_qualities[_entity.quality_from_id],
                self._lst_qualities[_entity.quality_to_id],
                self._lst_environments[_entity.environment_from_id],
                self._lst_environments[_entity.environment_to_id],
                _entity.temperature_from,
                _entity.temperature_to,
                _entity.change_description_1,
                _entity.change_factor_1,
                _entity.change_description_2,
                _entity.change_factor_2,
                _entity.change_description_3,
                _entity.change_factor_3,
                _entity.change_description_4,
                _entity.change_factor_4,
                _entity.change_description_5,
                _entity.change_factor_5,
                _entity.change_description_6,
                _entity.change_factor_6,
                _entity.change_description_7,
                _entity.change_factor_7,
                _entity.change_description_8,
                _entity.change_factor_8,
                _entity.change_description_9,
                _entity.change_factor_9,
                _entity.change_description_10,
                _entity.change_factor_10,
                _entity.function_1,
                _entity.function_2,
                _entity.function_3,
                _entity.function_4,
                _entity.function_5,
                _entity.result_1,
                _entity.result_2,
                _entity.result_3,
                _entity.result_4,
                _entity.result_5,
                _entity.user_blob_1,
                _entity.user_blob_2,
                _entity.user_blob_3,
                _entity.user_blob_4,
                _entity.user_blob_5,
                _entity.user_float_1,
                _entity.user_float_2,
                _entity.user_float_3,
                _entity.user_float_4,
                _entity.user_float_5,
                _entity.user_int_1,
                _entity.user_int_2,
                _entity.user_int_3,
                _entity.user_int_4,
                _entity.user_int_5,
                _entity.parent_id,
            ]

            try:
                self.tvwTreeView.unfilt_model.append(row, _attributes)
                pub.sendMessage("request_get_hardware_tree")
                pub.sendMessage("request_get_reliability_tree")
            except (AttributeError, TypeError, ValueError):
                _message = _(
                    f"An error occurred when loading similar item record "
                    f"{node.identifier} into the similar item list.  This might "
                    f"indicate it was missing it's data package, some of the data in "
                    f"the package was missing, or some of the data was the wrong "
                    f"type.  Row data was: {_attributes}"
                )
                pub.sendMessage(
                    "do_log_warning_msg",
                    logger_name="WARNING",
                    message=_message,
                )
