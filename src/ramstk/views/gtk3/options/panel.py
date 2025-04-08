# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.options.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Options panel module."""

# Standard Library Imports
from typing import List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
)


class OptionsPanel(RAMSTKFixedPanel):
    """The panel to display options to be edited."""

    # Define private class attributes.
    _select_msg = "succeed_get_siteinfo_attributes"
    _tag = "option"
    _title = _("General Information")

    def __init__(self) -> None:
        """Initialize an instance of the Edit Options panel."""
        super().__init__()

        # Initialize widgets.
        self.chkFunctions: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Function Module Enabled")
        )
        self.chkRequirements: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Requirements Module Enabled")
        )
        self.chkHardware: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Hardware Module Enabled")
        )
        self.chkValidation: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Validation Module Enabled")
        )
        self.chkHazards: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Hazards Analysis Module Enabled")
        )
        self.chkStakeholder: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Stakeholder Analysis Module Enabled")
        )
        self.chkAllocation: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("R(t) Allocation Module Enabled")
        )
        self.chkSimilarItem: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Similar Item Analysis Module Enabled")
        )
        self.chkFMEA: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("(D)FME(C)A Module Enabled")
        )
        self.chkPoF: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Physics of Failure (PoF) Module Enabled")
        )

        self.txtSiteID: RAMSTKEntry = RAMSTKEntry()
        self.txtSiteName: RAMSTKEntry = RAMSTKEntry()
        self.txtProductKey: RAMSTKEntry = RAMSTKEntry()
        self.txtExpireDate: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.txtSiteID,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "site_id",
                    "index": 0,
                    "label_text": _("Site ID:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": False,
                    "tooltip": "",
                    "visible": False,
                },
            },
            {
                "widget": self.txtSiteName,
                "attributes": {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "site_name",
                    "index": 1,
                    "label_text": _("Site Name:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": False,
                    "tooltip": "",
                    "visible": False,
                },
            },
            {
                "widget": self.txtProductKey,
                "attributes": {
                    "datatype": "gchararray",
                    "default": 0,
                    "field": "product_key",
                    "index": 2,
                    "label_text": _("Product Key:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": False,
                    "tooltip": "",
                    "visible": False,
                },
            },
            {
                "widget": self.txtExpireDate,
                "attributes": {
                    "datatype": "gchararray",
                    "default": 0,
                    "field": "expire_on",
                    "index": 3,
                    "label_text": _("Expire Date:"),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": False,
                    "tooltip": "",
                    "visible": False,
                },
            },
            {
                "widget": self.chkFunctions,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "function_enabled",
                    "index": 4,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": False,
                    "tooltip": "",
                    "visible": False,
                },
            },
            {
                "widget": self.chkRequirements,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "requirement_enabled",
                    "index": 5,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            },
            {
                "widget": self.chkHardware,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hardware_enabled",
                    "index": 6,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            },
            {
                "widget": self.chkValidation,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "validation_enabled",
                    "index": 7,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": False,
                    "tooltip": "",
                    "visible": False,
                },
            },
            {
                "widget": self.chkHazards,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hazard_enabled",
                    "index": 8,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            },
            {
                "widget": self.chkStakeholder,
                "attributes": {
                    "datatype": "gint",
                    "default": 0.0,
                    "field": "stakeholder_enabled",
                    "index": 9,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            },
            {
                "widget": self.chkAllocation,
                "attributes": {
                    "datatype": "gint",
                    "default": "",
                    "field": "allocation_enabled",
                    "index": 10,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            },
            {
                "widget": self.chkSimilarItem,
                "attributes": {
                    "datatype": "gint",
                    "default": "",
                    "field": "similar_item_enabled",
                    "index": 11,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            },
            {
                "widget": self.chkFMEA,
                "attributes": {
                    "datatype": "gint",
                    "default": "",
                    "field": "fmea_enabled",
                    "index": 12,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            },
            {
                "widget": self.chkPoF,
                "attributes": {
                    "datatype": "gint",
                    "default": "",
                    "field": "pof_enabled",
                    "index": 13,
                    "label_text": _(""),
                    "listen_topic": None,
                    "send_topic": None,
                },
                "properties": {
                    "editable": True,
                    "tooltip": "",
                    "visible": True,
                },
            },
        ]

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

        pub.sendMessage("request_get_option_attributes2", attributes={"site_id": 1})
