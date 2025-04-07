# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.clarity_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RequirementClarityPanel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton, RAMSTKFixedPanel, WidgetConfig


class RequirementClarityPanel(RAMSTKFixedPanel):
    """Panel to display clarity questions about the selected Requirement."""

    # Define private class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("Clarity of Requirement")

    def __init__(self) -> None:
        """Initialize an instance of the Requirement clarity panel."""
        super().__init__()

        # Initialize widgets.
        self.chkClarityQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkClarityQ8: RAMSTKCheckButton = RAMSTKCheckButton()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.chkClarityQ0,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_0",
                    "index": 14,
                    "label_text": _(
                        "1. The requirement clearly states what is needed or desired."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement clearly states what is needed or desired."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkClarityQ1,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_1",
                    "index": 15,
                    "label_text": _(
                        "2. The requirement is unambiguous and not open to "
                        "interpretation."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is unambiguous and not open to interpretation."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkClarityQ2,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_2",
                    "index": 16,
                    "label_text": _(
                        "3. All terms that can have more than one meaning are "
                        "qualified so that the desired meaning is readily apparent."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "All terms that can have more than one meaning are qualified "
                        "so that the desired meaning is readily apparent."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkClarityQ3,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_3",
                    "index": 17,
                    "label_text": _(
                        "4. Diagrams, drawings, etc. are used to increase "
                        "understanding of the requirement."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "Diagrams, drawings, etc. are used to increase understanding "
                        "of the requirement."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkClarityQ4,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_4",
                    "index": 18,
                    "label_text": _(
                        "5. The requirement is free from spelling and grammatical "
                        "errors."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is free from spelling and grammatical errors."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkClarityQ5,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_5",
                    "index": 19,
                    "label_text": _(
                        "6. The requirement is written in non-technical language "
                        "using the vocabulary of the stakeholder."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is written in non-technical language using "
                        "the vocabulary of the stakeholder."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkClarityQ6,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_6",
                    "index": 20,
                    "label_text": _(
                        "7. Stakeholders understand the requirement as written."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _("Stakeholders understand the requirement as written."),
                    "visible": True,
                },
            },
            {
                "widget": self.chkClarityQ7,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_7",
                    "index": 21,
                    "label_text": _(
                        "8. The requirement is clear enough to be turned over to an "
                        "independent group and still be understood."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is clear enough to be turned over to an "
                        "independent group and still be understood."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.chkClarityQ8,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_clarity_8",
                    "index": 22,
                    "label_text": _(
                        "9. The requirement avoids stating how the problem is to be "
                        "solved or what techniques are to be used."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                "properties": {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement avoids stating how the problem is to be "
                        "solved or what techniques are to be used."
                    ),
                    "visible": True,
                },
            },
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel(justify=Gtk.Justification.LEFT)
        super().do_set_widget_callbacks()
