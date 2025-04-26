# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.verifiability_panel.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RequirementVerifiabilityPanel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class RequirementVerifiabilityPanel(RAMSTKFixedPanel):
    """Panel to display verifiability questions about selected Requirement."""

    # Define private class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("Verifiability of Requirement")

    def __init__(self) -> None:
        """Initialize an instance of the Requirement verifiability panel."""
        super().__init__()

        # Initialize widgets.
        self.chkVerifiableQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkVerifiableQ5: RAMSTKCheckButton = RAMSTKCheckButton()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.chkVerifiableQ0,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_verifiable_0",
                    "index": 42,
                    "label_text": _(
                        "1. The requirement is verifiable by testing, demonstration, "
                        "review, or analysis."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is verifiable by testing, demonstration, "
                        "review, or analysis."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkVerifiableQ1,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_verifiable_1",
                    "index": 43,
                    "label_text": _(
                        "2. The requirement lacks 'weasel words' (e.g. various, "
                        "mostly, suitable, integrate, maybe, consistent, robust, "
                        "modular, user-friendly, superb, good)."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement lacks 'weasel words' (e.g. various, mostly, "
                        "suitable, integrate, maybe, consistent, robust, modular, "
                        "user-friendly, superb, good)."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkVerifiableQ2,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_verifiable_2",
                    "index": 44,
                    "label_text": _(
                        "3. Any performance criteria are quantified such that they are "
                        "testable."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "Any performance criteria are quantified such that they are "
                        "testable."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkVerifiableQ3,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_verifiable_3",
                    "index": 45,
                    "label_text": _(
                        "4. Independent testing would be able to determine whether the "
                        "requirement has been satisfied."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "Independent testing would be able to determine whether the "
                        "requirement has been satisfied."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkVerifiableQ4,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_verifiable_4",
                    "index": 46,
                    "label_text": _(
                        "5. The task(s) that will validate and verify the final design "
                        "satisfies the requirement have been identified."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The task(s) that will validate and verify the final design "
                        "satisfies the requirement have been identified."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkVerifiableQ5,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_verifiable_5",
                    "index": 47,
                    "label_text": _(
                        "6. The identified V&amp;V task(s) have been added to the "
                        "validation plan (e.g., DVP)"
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The identified V&amp;V task(s) have been added to the "
                        "validation plan (e.g., DVP)"
                    ),
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel(justify=Gtk.Justification.LEFT)
        super().do_set_widget_callbacks()
