# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.similar_item.tree_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Similar Item Tree panel module."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel, WidgetConfig


class SimilarItemTreePanel(RAMSTKTreePanel):
    """Panel to display Similar Item analysis worksheet."""

    # Define private class attributes.
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
    _select_msg = "succeed_retrieve_all_similar_item"
    _tag = "similar_item"
    _title = _("Similar Item Analysis")

    def __init__(self) -> None:
        """Initialize an instance of the Similar Item analysis worksheet."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hardware_id",
                    "index": 1,
                    "label_text": _("Hardware ID"),
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "name",
                    "index": 2,
                    "label_text": _("Assembly"),
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "hazard_rate_active",
                    "index": 3,
                    "label_text": _("Current Hazard Rate"),
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "quality_from_id",
                    "index": 4,
                    "label_text": _("From Quality"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "quality_to_id",
                    "index": 5,
                    "label_text": _("To Quality"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "environment_from_id",
                    "index": 6,
                    "label_text": _("From Environment"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererCombo(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "environment_to_id",
                    "index": 7,
                    "label_text": _("To Environment"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 25.0,
                    "field": "temperature_from",
                    "index": 8,
                    "label_text": _("From Temperature"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 25.0,
                    "field": "temperature_to",
                    "index": 9,
                    "label_text": _("To Temperature"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_1",
                    "index": 10,
                    "label_text": _("Change Description 1"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_1",
                    "index": 11,
                    "label_text": _("Change Factor 1"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_2",
                    "index": 12,
                    "label_text": _("Change Description 2"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_2",
                    "index": 13,
                    "label_text": _("Change Factor 2"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_3",
                    "index": 14,
                    "label_text": _("Change Description 3"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_3",
                    "index": 15,
                    "label_text": _("Change Factor 3"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_4",
                    "index": 16,
                    "label_text": _("Change Description 4"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_4",
                    "index": 17,
                    "label_text": _("Change Factor 4"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_5",
                    "index": 18,
                    "label_text": _("Change Description 5"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_5",
                    "index": 19,
                    "label_text": _("Change Factor 5"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_6",
                    "index": 20,
                    "label_text": _("Change Description 6"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_6",
                    "index": 21,
                    "label_text": _("Change Factor 6"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_7",
                    "index": 22,
                    "label_text": _("Change Description 7"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_7",
                    "index": 23,
                    "label_text": _("Change Factor 7"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_8",
                    "index": 24,
                    "label_text": _("Change Description 8"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_8",
                    "index": 25,
                    "label_text": _("Change Factor 8"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_9",
                    "index": 26,
                    "label_text": _("Change Description 9"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_9",
                    "index": 27,
                    "label_text": _("Change Factor 9"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "change_description_10",
                    "index": 28,
                    "label_text": _("Change Description 10"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "change_factor_10",
                    "index": 29,
                    "label_text": _("Change Factor 10"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_1",
                    "index": 30,
                    "label_text": _("Function 1"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_2",
                    "index": 31,
                    "label_text": _("Function 2"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_3",
                    "index": 32,
                    "label_text": _("Function 3"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_4",
                    "index": 33,
                    "label_text": _("Function 4"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_5",
                    "index": 34,
                    "label_text": _("Function 5"),
                },
                "properties": {
                    "editable": True,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "result_1",
                    "index": 35,
                    "label_text": _("Result 1"),
                },
                "properties": {
                    "editable": False,
                    "visible": True,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "result_2",
                    "index": 36,
                    "label_text": _("Result 2"),
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "result_3",
                    "index": 37,
                    "label_text": _("Result 3"),
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "result_4",
                    "index": 38,
                    "label_text": _("Result 4"),
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "result_5",
                    "index": 39,
                    "label_text": _("Result 5"),
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_blob_1",
                    "index": 40,
                    "label_text": _("User Text 1"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_blob_2",
                    "index": 41,
                    "label_text": _("User Text 2"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_blob_3",
                    "index": 42,
                    "label_text": _("User Text 3"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_blob_4",
                    "index": 43,
                    "label_text": _("User Text 4"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "user_blob_5",
                    "index": 44,
                    "label_text": _("User Text 5"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_1",
                    "index": 45,
                    "label_text": _("User Float 1"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_2",
                    "index": 46,
                    "label_text": _("User Float 2"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_3",
                    "index": 47,
                    "label_text": _("User Float 3"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_4",
                    "index": 48,
                    "label_text": _("User Float 4"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "user_float_5",
                    "index": 49,
                    "label_text": _("User Float 5"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "user_int_1",
                    "index": 50,
                    "label_text": _("User Integer 1"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "user_int_2",
                    "index": 51,
                    "label_text": _("User Integer 2"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "user_int_3",
                    "index": 52,
                    "label_text": _("User Integer 3"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "user_int_4",
                    "index": 53,
                    "label_text": _("User Integer 4"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "user_int_5",
                    "index": 54,
                    "label_text": _("User Integer 5"),
                },
                "properties": {
                    "editable": True,
                    "visible": False,
                },
            },
            {
                "widget": Gtk.CellRendererText(),
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "parent_id",
                    "index": 55,
                    "label_text": _("Parent ID"),
                },
                "properties": {
                    "editable": False,
                    "visible": False,
                },
            },
        ]
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
        self._filtered_tree = True
        self._method_id: int = 0
        self._on_edit_message: str = f"mvw_editing_{self._tag}"

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        self._do_load_environments()
        self._do_load_quality()
        super().do_set_widget_callbacks()
        self._do_subscribe_to_messages()

        # FIXME: Is this line necessary?
        self.tvwTreeView.dic_row_loader = {
            "similar_item": self.__do_load_similar_item,
        }
        self.tvwTreeView.set_tooltip_text(
            _(
                "Displays the Similar Item Analysis for the currently selected "
                "Hardware item."
            )
        )

    # ----- SimilarItemTreePanel specific methods. ----- #
    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_filter_tree(
        self, model: Gtk.TreeModel, row: Gtk.TreeIter, data: Any
    ) -> bool:
        """Filter to show only those associated with the selected Hardware.

        :param model: the filtered model for the Similar Item RAMSTKTreeView.
        :param row: the iter to check against condition(s).
        :param data: unused in this method; required by Gtk.TreeModelFilter() widget.
        :return: True if row should be visible, False else.
        :rtype: bool
        """
        return model[row][55] == self._parent_id

    def do_refresh_functions(self, row: Gtk.TreeIter, function: List[str]) -> None:
        """Refresh the Similar Item functions in the RAMSTKTreeView().

        :param row: the row in the Similar Item RAMSTKTreeView() whose functions need to
            be updated. This is required to allow a recursive calling function to load
            the same function in all rows.
        :param function: the list of user-defined Similar Item functions.
        """
        _model = self.tvwTreeView.get_model()

        _model.set_value(row, self.tvwTreeView.position["function_1"], function[0])
        _model.set_value(row, self.tvwTreeView.position["function_2"], function[1])
        _model.set_value(row, self.tvwTreeView.position["function_3"], function[2])
        _model.set_value(row, self.tvwTreeView.position["function_4"], function[3])
        _model.set_value(row, self.tvwTreeView.position["function_5"], function[4])

    def _do_load_environments(self) -> None:
        """Load Similar Item analysis environment RAMSTKComboBox."""
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["environment_from_id"],
            self._lst_environments,
        )
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["environment_to_id"],
            self._lst_environments,
        )

    def _do_load_quality(self) -> None:
        """Load Similar Item analysis quality RAMSTKComboBox."""
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["quality_from_id"],
            self._lst_qualities,
        )
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["quality_to_id"],
            self._lst_qualities,
        )

    def _do_set_columns_visible(self) -> None:
        """Set editable columns based on the Similar Item method selected."""
        if self._method_id == -1:
            self._method_id = 0
        self.tvwTreeView.visible = self._dic_visible_mask[self._method_id]
        self.tvwTreeView.do_set_visible_columns()

    def _do_set_hardware_attributes(self, tree: treelib.Tree) -> None:
        """Set the attributes when the hardware tree is retrieved.

        :param tree: the hardware treelib.Tree.
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

        :param tree: the reliability treelib.Tree.
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

    def _do_subscribe_to_messages(self) -> None:
        """Subscribe to messages for Similar Item worksheet."""
        pub.subscribe(super().do_load_panel, "succeed_calculate_similar_item")
        pub.subscribe(self._do_set_hardware_attributes, "succeed_get_hardware_tree")
        pub.subscribe(
            self._do_set_reliability_attributes, "succeed_get_reliability_tree"
        )
        pub.subscribe(self._on_method_changed, "succeed_change_similar_item_method")
        pub.subscribe(self._on_select_hardware, "selected_hardware")

    def _on_method_changed(self, method_id: int) -> None:
        """Set method ID attributes when user changes the selection.

        :param method_id: the newly selected allocation method.
        """
        self._method_id = method_id
        self._do_set_columns_visible()

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Respond to user changing selected row in Similar Item worksheet.

        :param selection: the Gtk.TreeSelection() that is the newly selected row.
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["hardware_id"]

            pub.sendMessage(
                "selected_similar_item",
                attributes=_attributes,
            )

    def _on_select_hardware(
        self, attributes: Dict[str, Union[int, float, str]]
    ) -> None:
        """Filter Similar Item worksheet when Hardware is selected.

        :param attributes: the dict of attributes for the selected Hardware.
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
