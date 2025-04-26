# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.general_data_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Revision general data panel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    WidgetConfig,
    make_widget_config,
)


class RevisionGeneralDataPanel(RAMSTKFixedPanel):
    """The panel to display general data about the selected Revision."""

    # Define private class attributes.
    _record_field = "revision_id"
    _select_msg = "selected_revision"
    _tag = "revision"
    _title = _("General Revision Information")

    def __init__(self) -> None:
        """Initialize an instance of the Revision General Data panel."""
        super().__init__()

        # Initialize widgets.
        self.txtCode: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.txtCode,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "revision_code",
                    "index": 22,
                    "label_text": _("Revision Code"),
                    "listen_topic": "mvw_editing_revision",
                    "send_topic": "wvw_editing_revision",
                },
                {
                    "tooltip": _("A unique code for the selected revision."),
                    "width_request": 125,
                },
            ),
            make_widget_config(
                self.txtName,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "revision_code",
                    "index": 17,
                    "label_text": _("Revision Name"),
                    "listen_topic": "mvw_editing_revision",
                    "send_topic": "wvw_editing_revision",
                },
                {
                    "tooltip": _("The name of the selected revision."),
                    "width_request": 800,
                },
            ),
            make_widget_config(
                self.txtRemarks,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "revision_code",
                    "index": 20,
                    "label_text": _("Revision Name"),
                    "listen_topic": "mvw_editing_revision",
                    "send_topic": "wvw_editing_revision",
                },
                {
                    "height_request": 100,
                    "tooltip": _(
                        "Enter any remarks associated with the selected revision."
                    ),
                    "width_request": 800,
                },
            ),
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        super().do_set_widget_callbacks()
