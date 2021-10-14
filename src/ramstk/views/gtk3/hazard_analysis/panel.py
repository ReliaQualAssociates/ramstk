# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hazard_analysis.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Hazard Analysis Panels."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel


class HazardsTreePanel(RAMSTKTreePanel):
    """The panel to display the hazards analysis for the selected Function."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_hazards"
    _tag = "hazard"
    _title: str = _("Hazards Analysis")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Function Hazard Analysis panel."""
        super().__init__()

        # Initialize private dict instance attributes.
        self.tvwTreeView.dic_row_loader = {
            "hazard": super().do_load_treerow,
        }

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._on_edit_message: str = f"wvw_editing_{self._tag}"

        # Initialize public dict instance attributes.
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
            "function_id": [
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
                _("Function ID"),
                "gint",
            ],
            "hazard_id": [
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
                    "visible": True,
                },
                _("Hazard ID"),
                "gint",
            ],
            "potential_hazard": [
                3,
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
                _("Potential Hazard"),
                "gchararray",
            ],
            "potential_cause": [
                4,
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
                _("Potential Cause"),
                "gchararray",
            ],
            "assembly_effect": [
                5,
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
                _("Assembly Effect"),
                "gchararray",
            ],
            "assembly_severity": [
                6,
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
                _("Assembly Severity"),
                "gchararray",
            ],
            "assembly_probability": [
                7,
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
                _("Assembly Probability"),
                "gchararray",
            ],
            "assembly_hri": [
                8,
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
                _("Assembly HRI"),
                "gint",
            ],
            "assembly_mitigation": [
                9,
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
                _("Assembly Mitigation"),
                "gchararray",
            ],
            "assembly_severity_f": [
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
                _("Final Assembly Severity"),
                "gchararray",
            ],
            "assembly_probability_f": [
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
                _("Final Assembly Probability"),
                "gchararray",
            ],
            "assembly_hri_f": [
                12,
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
                _("Final Assembly HRI"),
                "gint",
            ],
            "system_effect": [
                13,
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
                _("System Effect"),
                "gchararray",
            ],
            "system_severity": [
                14,
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
                _("System Severity"),
                "gchararray",
            ],
            "system_probability": [
                15,
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
                _("System Probability"),
                "gchararray",
            ],
            "system_hri": [
                16,
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
                _("System HRI"),
                "gint",
            ],
            "system_mitigation": [
                17,
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
                _("System Mitigation"),
                "gchararray",
            ],
            "system_severity_f": [
                18,
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
                _("Final System Severity"),
                "gchararray",
            ],
            "system_probability_f": [
                19,
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
                _("Final System Probability"),
                "gchararray",
            ],
            "system_hri_f": [
                20,
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
                _("Final System HRI"),
                "gint",
            ],
            "remarks": [
                21,
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
            "function_1": [
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
                _("Function 1"),
                "gchararray",
            ],
            "function_2": [
                23,
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
                _("Function 3"),
                "gchararray",
            ],
            "function_4": [
                25,
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
                _("Function 5"),
                "gchararray",
            ],
            "result_1": [
                27,
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
                _("Result 1"),
                "gfloat",
            ],
            "result_2": [
                28,
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
                _("Result 2"),
                "gfloat",
            ],
            "result_3": [
                29,
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
                _("Result 3"),
                "gfloat",
            ],
            "result_4": [
                30,
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
                _("Result 4"),
                "gfloat",
            ],
            "result_5": [
                31,
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
                _("Result 5"),
                "gfloat",
            ],
            "user_blob_1": [
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
                _("User Text 1"),
                "gchararray",
            ],
            "user_blob_2": [
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
                _("User Text 2"),
                "gchararray",
            ],
            "user_blob_3": [
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
                _("User Text 3"),
                "gchararray",
            ],
            "user_float_1": [
                35,
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
                36,
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
                37,
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
            "user_int_1": [
                38,
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
                39,
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
                40,
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
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the Hazards Analysis for the currently selected Function.")
        )

        # Subscribe to PyPubSub messages.

    def do_load_severity(self, criticalities: Dict[int, Tuple[str, str, int]]) -> None:
        """Load the Gtk.CellRendererCombo() containing severities.

        :param criticalities: the dict containing the hazard severity
            categories and values.
        :return: None
        :rtype: None
        """
        for i in [6, 10, 14, 18]:
            _model = self.tvwTreeView.get_cell_model(i)
            for _key in criticalities:
                _model.append((criticalities[_key][1],))

    def do_load_hazards(self, hazards: Dict[Any, Any]) -> None:
        """Load the Gtk.CellRendererCombos() containing hazards.

        :param hazards: the dict containing the hazards and hazard types
            to be considered.
        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(3)
        for _key in hazards:
            _hazard = f"{hazards[_key][0]}, {hazards[_key][1]}"
            _model.append((_hazard,))

    def do_load_probability(self, probabilities: List[str]) -> None:
        """Load the Gtk.CellRendererCombos() containing probabilities.

        :param probabilities: the list of hazard probabilities.
        :return: None
        :rtype: None
        """
        for i in [7, 11, 15, 19]:
            _model = self.tvwTreeView.get_cell_model(i)
            for _probability in probabilities:
                _model.append((_probability[0],))

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the HazOps Tree View RAMSTKTreeView().

        This method is called whenever a Tree View row is activated.

        :param selection: the HazOps RAMSTKTreeview Gtk.TreeSelection().
        :return: None
        :rtype: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._parent_id = _attributes["function_id"]
            self._record_id = _attributes["hazard_id"]

            pub.sendMessage(
                "selected_hazard",
                attributes=_attributes,
            )
