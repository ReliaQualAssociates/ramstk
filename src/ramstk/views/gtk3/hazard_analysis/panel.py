# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hazard_analysis.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Hazard Analysis tree panel module."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict, List, Tuple, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererText,
    RAMSTKTreePanel,
    WidgetConfig,
)


class HazardsTreePanel(RAMSTKTreePanel):
    """The panel to display the hazards analysis for the selected Function."""

    # Define private class attributes.
    _select_msg = "succeed_retrieve_all_hazard"
    _tag = "hazard"
    _title: str = _("Hazards Analysis")

    def __init__(self) -> None:
        """Initialize an instance of the Hazards tree panel."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "function_id",
                    "index": 1,
                    "label_text": _("Function ID"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hazard_id",
                    "index": 2,
                    "label_text": _("Hazard ID"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "potential_hazard",
                    "index": 3,
                    "label_text": _("Potential Hazard"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "potential_cause",
                    "index": 4,
                    "label_text": _("Potential Cause"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "assembly_effect",
                    "index": 5,
                    "label_text": _("Assembly Effect"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "assembly_severity",
                    "index": 6,
                    "label_text": _("Assembly Severity"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "assembly_probability",
                    "index": 7,
                    "label_text": _("Assembly Probability"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "assembly_hri",
                    "index": 8,
                    "label_text": _("Assembly HRI"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "assembly_mitigation",
                    "index": 9,
                    "label_text": _("Assembly Mitigation"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "assembly_severity_f",
                    "index": 10,
                    "label_text": _("Final Assembly Severity"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "assembly_probability_f",
                    "index": 11,
                    "label_text": _("Final Assembly Probability"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "assembly_hri_f",
                    "index": 12,
                    "label_text": _("Final Assembly HRI"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "system_effect",
                    "index": 13,
                    "label_text": _("System Effect"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "system_severity",
                    "index": 14,
                    "label_text": _("System Severity"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "system_probability",
                    "index": 15,
                    "label_text": _("System Probability"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "system_hri",
                    "index": 16,
                    "label_text": _("System HRI"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "system_mitigation",
                    "index": 17,
                    "label_text": _("System Mitigation"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "system_severity_f",
                    "index": 18,
                    "label_text": _("Final System Severity"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "system_probability_f",
                    "index": 19,
                    "label_text": _("Final System Probability"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "system_hri_f",
                    "index": 20,
                    "label_text": _("Final System HRI"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "remarks",
                    "index": 21,
                    "label_text": _("Remarks"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_1",
                    "index": 22,
                    "label_text": _("User Function 1"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_2",
                    "index": 23,
                    "label_text": _("User Function 2"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_3",
                    "index": 24,
                    "label_text": _("User Function 3"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_4",
                    "index": 25,
                    "label_text": _("User Function 4"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_5",
                    "index": 26,
                    "label_text": _("User Function 5"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "result_1",
                    "index": 27,
                    "label_text": _("Result 1"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "result_2",
                    "index": 28,
                    "label_text": _("Result 2"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "result_3",
                    "index": 29,
                    "label_text": _("Result 3"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "result_4",
                    "index": 30,
                    "label_text": _("Result 4"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "result_5",
                    "index": 31,
                    "label_text": _("Result 5"),
                    "listen_topic": "wvw_editing_hazard",
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_blob_1",
                    "index": 32,
                    "label_text": _("User Text 1"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_blob_2",
                    "index": 33,
                    "label_text": _("User Text 2"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_blob_3",
                    "index": 34,
                    "label_text": _("User Text 3"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_1",
                    "index": 35,
                    "label_text": _("User Float 1"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_2",
                    "index": 36,
                    "label_text": _("User Float 2"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_3",
                    "index": 37,
                    "label_text": _("User Float 3"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "user_int_1",
                    "index": 38,
                    "label_text": _("User Integer 1"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "user_int_2",
                    "index": 39,
                    "label_text": _("User Integer 2"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": RAMSTKCellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "user_int_3",
                    "index": 40,
                    "label_text": _("User Integer 3"),
                    "listen_topic": "wvw_editing_hazard",
                    "send_topic": "mvw_editing_hazard",
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
        ]
        self._filtered_tree = True

        # Initialize public instance attributes.
        self.lst_hazards: List[str] = [""]
        self.lst_probability: List[str] = [""]
        self.lst_severity: List[str] = [""]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

        # FIXME: Is this line necessary?
        # self.tvwTreeView.dic_row_loader = {
        #    "hazard": super().do_load_treerow,
        # }
        self.tvwTreeView.set_tooltip_text(
            _("Displays the Hazards Analysis for the currently selected Function.")
        )

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                f"succeed_calculate_{self._tag}": super().do_load_panel,
                "selected_function": self._on_select_function,
            }
        )

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the HazOps Tree View RAMSTKTreeView.

        This method is called whenever a Tree View row is activated.

        :param selection: the HazOps RAMSTKTreeview Gtk.TreeSelection.
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["hazard_id"]

            pub.sendMessage(
                "selected_hazard",
                attributes=_attributes,
            )

    # ----- -- HazardsTreePanel specific methods. --- ----- #
    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_filter_tree(
        self,
        model: Gtk.TreeModel,
        row: Gtk.TreeIter,
        data: Union[bool, date, float, int, str],
    ) -> bool:
        """Filter Hazards to show only those associated with the selected Function.

        :param model: the filtered model for the Hazard RAMSTKTreeView.
        :param row: the iter to check against condition(s).
        :param data: unused in this method; required by Gtk.TreeModelFilter() widget.
        :return: True if row should be visible, False otherwise.
        :rtype: bool
        """
        return model[row][1] == self._parent_id

    def do_load_hazards(self, hazards: Dict[int, Tuple[str, str]]) -> None:
        """Load the hazards list.

        :param hazards: the list of hazards to load into the hazards combo box.
        """
        for _hazard in hazards:
            self.lst_hazards.append(f"{hazards[_hazard][0]} {hazards[_hazard][1]}")

        self.tvwTreeView.do_load_cellrenderercombo("potential_hazard", self.lst_hazards)

    def do_load_probabilities(self, probabilities: List[List[str]]) -> None:
        """Load the probabilities list.

        :param probabilities: the list of probabilities to load into the probabilities
            combo box.
        """
        for _probability in probabilities:
            self.lst_probability.append(_probability[0])

        for _field in [
            "assembly_probability",
            "assembly_probability_f",
            "system_probability",
            "system_probability_f",
        ]:
            self.tvwTreeView.do_load_cellrenderercombo(_field, self.lst_probability)

    def do_load_severities(self, severities: Dict[int, Tuple[str, str, int]]) -> None:
        """Load the severities list.

        :param severities: the list of severities to load into the severities combo box.
        """
        for _severity in severities:
            self.lst_severity.append(severities[_severity][1])

        for _field in [
            "assembly_severity",
            "assembly_severity_f",
            "system_severity",
            "system_severity_f",
        ]:
            self.tvwTreeView.do_load_cellrenderercombo(_field, self.lst_severity)

    def do_refresh_functions(self, row: Gtk.TreeIter, function: List[str]) -> None:
        """Refresh the Hazard Analysis functions in the RAMSTKTreeView.

        :param row: the row in the Hazard Analysis RAMSTKTreeView whose functions need
            to be updated. This is required to allow a recursive calling function to
            load the same function in all rows.
        :param function: the list of user-defined Hazard Analysis functions.
        """
        _model = self.tvwTreeView.get_model()

        _model.set_value(row, self.tvwTreeView.position["function_1"], function[0])
        _model.set_value(row, self.tvwTreeView.position["function_2"], function[1])
        _model.set_value(row, self.tvwTreeView.position["function_3"], function[2])
        _model.set_value(row, self.tvwTreeView.position["function_4"], function[3])
        _model.set_value(row, self.tvwTreeView.position["function_5"], function[4])

    def _on_select_function(self, attributes: Dict[str, Any]) -> None:
        """Filter hazards list when a Function is selected.

        :param attributes: the dict of Function attributes for the selected Function.
        """
        self._parent_id = attributes["function_id"]
        self.tvwTreeView.filt_model.refilter()
