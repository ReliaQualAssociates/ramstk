# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.miscellaneous_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The HardwareMiscellaneousPanel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    WidgetConfig,
    make_widget_config,
)


class HardwareMiscellaneousPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Hardware task."""

    # Define private class attributes.
    _record_field = "hardware_id"
    _select_msg = "selected_hardware"
    _tag = "hardware"
    _title = _("Hardware Miscellaneous Information")

    def __init__(self) -> None:
        """Initialize an instance of the Hardware Task Description panel."""
        super().__init__()

        # Initialize widgets.
        self.chkTagged: RAMSTKCheckButton = RAMSTKCheckButton(label=_("Tagged Part"))
        self.txtAttachments: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.txtAttachments,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "Attachments",
                    "index": 31,
                    "label_text": _("Attachments:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "height_request": 150,
                    "tooltip": _(
                        "Any attachments associated with the selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 600,
                },
            ),
            make_widget_config(
                self.txtRemarks,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "remarks",
                    "index": 23,
                    "label_text": _("Remarks:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "height_request": 150,
                    "tooltip": _(
                        "Any remarks pertinent to the selected hardware item."
                    ),
                    "visible": True,
                    "width_request": 600,
                },
            ),
            make_widget_config(
                self.chkTagged,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "tagged_part",
                    "index": 26,
                    "label_text": _("Tagged Part"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _("Tag the selected hardware item."),
                    "visible": True,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        super().do_set_widget_callbacks()
