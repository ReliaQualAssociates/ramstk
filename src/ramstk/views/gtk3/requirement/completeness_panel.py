# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.completeness_panel.py is part of The RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RequirementCompletenessPanel module."""

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


class RequirementCompletenessPanel(RAMSTKFixedPanel):
    """Panel to display completeness questions about selected Requirement."""

    # Define private class attributes.
    _record_field = "requirement_id"
    _select_msg = "selected_requirement"
    _tag = "requirement"
    _title = _("Completeness of Requirement")

    def __init__(self) -> None:
        """Initialize an instance of the Requirement completeness panel."""
        super().__init__()

        # Initialize widgets.
        self.chkCompleteQ0: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ1: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ2: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ3: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ4: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ5: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ6: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ7: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ8: RAMSTKCheckButton = RAMSTKCheckButton()
        self.chkCompleteQ9: RAMSTKCheckButton = RAMSTKCheckButton()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.chkCompleteQ0,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_0",
                    "index": 23,
                    "label_text": _(
                        "1. Performance objectives are properly documented from the "
                        "user's point of view."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "Performance objectives are properly documented from the "
                        "user's point of view."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ1,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_1",
                    "index": 24,
                    "label_text": _(
                        "2. No necessary information is missing from the requirement."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "No necessary information is missing from the requirement."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ2,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_2",
                    "index": 25,
                    "label_text": _("3. The requirement has been assigned a priority."),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _("The requirement has been assigned a priority."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ3,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_3",
                    "index": 26,
                    "label_text": _(
                        "4. The requirement is realistic given the technology that "
                        "will be used to implement the system."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is realistic given the technology that will "
                        "be used to implement the system."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ4,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_4",
                    "index": 27,
                    "label_text": _(
                        "5. The requirement is feasible to implement given the defined "
                        "project time frame, scope, structure and budget."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is feasible to implement given the defined "
                        "project time frame, scope, structure and budget."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ5,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_5",
                    "index": 28,
                    "label_text": _(
                        "6. If the requirement describes something as a 'standard' the "
                        "specific source is cited."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "If the requirement describes something as a 'standard' the "
                        "specific source is cited."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ6,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_6",
                    "index": 29,
                    "label_text": _(
                        "7. The requirement is relevant to the problem and its "
                        "solution."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement is relevant to the problem and its solution."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ7,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_7",
                    "index": 30,
                    "label_text": _(
                        "8. The requirement contains no implied design details."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _("The requirement contains no implied design details."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ8,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_8",
                    "index": 31,
                    "label_text": _(
                        "9. The requirement contains no implied implementation "
                        "constraints."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement contains no implied implementation "
                        "constraints."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkCompleteQ9,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "q_complete_9",
                    "index": 32,
                    "label_text": _(
                        "10. The requirement contains no implied project management "
                        "constraints."
                    ),
                    "listen_topic": "wvw_editing_requirement",
                    "send_topic": "wvw_editing_requirement",
                },
                {
                    "editable": True,
                    "height_request": 30,
                    "tooltip": _(
                        "The requirement contains no implied project management "
                        "constraints."
                    ),
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel(justify=Gtk.Justification.LEFT)
        super().do_set_widget_callbacks()
