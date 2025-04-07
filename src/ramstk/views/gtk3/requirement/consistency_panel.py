# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.consistency_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RequirementConsistencyPanel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton, RAMSTKFixedPanel, WidgetConfig


class RequirementConsistencyPanel(RAMSTKFixedPanel):
    """Panel to display consistency questions about selected Requirement."""

    # Define private class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("Consistency of Requirement")

    def __init__(self) -> None:
        """Initialize an instance of the Requirement consistency panel."""
        super().__init__()

        # Initialize widgets.
        self.chkConsistentQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkConsistentQ8: RAMSTKCheckButton = RAMSTKCheckButton()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.chkConsistentQ0,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_0",
                    "index": 33,
                    "label_text": _(
                        "1. The requirement describes a single need or want; it could "
                        "not be broken into several different requirements."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement describes a single need or want; it could not "
                        "be broken into several different requirements."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkConsistentQ1,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_1",
                    "index": 34,
                    "label_text": _(
                        "2. The requirement requires non-standard hardware or must "
                        "use software to implement."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement requires non-standard hardware or must use "
                        "software to implement."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkConsistentQ2,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_2",
                    "index": 35,
                    "label_text": _(
                        "3. The requirement can be implemented within known "
                        "constraints."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement can be implemented within known constraints."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkConsistentQ3,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_3",
                    "index": 36,
                    "label_text": _(
                        "4. The requirement provides an adequate basis for design and "
                        "testing."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement provides an adequate basis for design and "
                        "testing."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkConsistentQ4,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_4",
                    "index": 37,
                    "label_text": _(
                        "5. The requirement adequately supports the business goal of "
                        "the project."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement adequately supports the business goal of the "
                        "project."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkConsistentQ5,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_5",
                    "index": 38,
                    "label_text": _(
                        "6. The requirement does not conflict with some constraint, "
                        "policy or regulation."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement does not conflict with some constraint, "
                        "policy or regulation."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkConsistentQ6,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_6",
                    "index": 39,
                    "label_text": _(
                        "7. The requirement does not conflict with another requirement."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement does not conflict with another requirement."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkConsistentQ7,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_7",
                    "index": 40,
                    "label_text": _(
                        "8. The requirement is not a duplicate of another requirement."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is not a duplicate of another requirement."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkConsistentQ8,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_consistent_8",
                    "index": 41,
                    "label_text": _("9. The requirement is in scope for the project."),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _("The requirement is in scope for the project."),
                    "visible": True,
                },
            },
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel(justify=Gtk.Justification.LEFT)
        super().do_set_widget_callbacks()
