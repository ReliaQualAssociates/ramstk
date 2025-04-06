# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.function.general_data_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The FunctionGeneralDataPanel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    WidgetConfig,
)


class FunctionGeneralDataPanel(RAMSTKFixedPanel):
    """The panel to display general data about the selected function."""

    # Define private class attributes.
    _record_field = "function_id"
    _select_msg = "selected_function"
    _tag = "function"
    _title = _("General Function Information")

    def __init__(self) -> None:
        """Initialize an instance of the Function General Data panel."""
        super().__init__()

        # Initialize widgets.
        self.chkSafetyCritical: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Function is safety critical.")
        )
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.txtCode,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "function_code",
                    "index": 5,
                    "label_text": _("Function Code:"),
                    "listen_topic": f"mvw_editing_{self._tag}",
                },
                "properties": {
                    "editable": False,
                    "tooltip": _("A unique code for the selected function."),
                    "visible": True,
                    "width_request": 125,
                },
            },
            {
                "widget": self.txtName,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "name",
                    "index": 15,
                    "label_text": _("Function Name:"),
                    "listen_topic": f"mvw_editing_{self._tag}",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The name of the selected function."),
                    "visible": True,
                    "width_request": 800,
                },
            },
            {
                "widget": self.txtRemarks,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "remarks",
                    "index": 17,
                    "label_text": _("Remarks:"),
                    "listen_topic": f"mvw_editing_{self._tag}",
                },
                "properties": {
                    "editable": True,
                    "height_request": 100,
                    "tooltip": _(
                        "Enter any remarks associated with the selected function."
                    ),
                    "visible": True,
                    "width_request": 800,
                },
            },
            {
                "widget": self.chkSafetyCritical,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "safet_critical",
                    "index": 15,
                    "label_text": _("Function Name:"),
                    "listen_topic": f"mvw_editing_{self._tag}",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "Indicates whether or not the selected function is safety "
                        "critical."
                    ),
                    "visible": True,
                },
            },
        ]

        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()
