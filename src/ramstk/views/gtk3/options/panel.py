# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.options.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK GTK3 Options Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton, RAMSTKEntry, RAMSTKFixedPanel


class OptionsPanel(RAMSTKFixedPanel):
    """The panel to display options to be edited."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_get_siteinfo_attributes"
    _tag = "option"
    _title = _("General Information")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

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

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "site_id": [
                0,
                self.txtSiteID,
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Site ID: "),
            ],
            "site_name": [
                1,
                self.txtSiteName,
                "edited",
                None,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Site Name: "),
            ],
            "product_key": [
                2,
                self.txtProductKey,
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Product Key: "),
            ],
            "expire_on": [
                3,
                self.txtExpireDate,
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Expire Date: "),
            ],
            "function_enabled": [
                4,
                self.chkFunctions,
                "toggled",
                super().on_toggled,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _(""),
            ],
            "requirement_enabled": [
                5,
                self.chkRequirements,
                "toggled",
                super().on_toggled,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
            ],
            "hardware_enabled": [
                6,
                self.chkHardware,
                "toggled",
                super().on_toggled,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
            ],
            "validation_enabled": [
                7,
                self.chkValidation,
                "toggled",
                super().on_toggled,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _(""),
            ],
            "hazard_enabled": [
                8,
                self.chkHazards,
                "toggled",
                super().on_toggled,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
            ],
            "stakeholder_enabled": [
                9,
                self.chkStakeholder,
                "toggled",
                super().on_toggled,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mode Probability"),
            ],
            "allocation_enabled": [
                10,
                self.chkAllocation,
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
            ],
            "similar_item_enabled": [
                11,
                self.chkSimilarItem,
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _(""),
            ],
            "fmea_enabled": [
                12,
                self.chkFMEA,
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Load History Method"),
            ],
            "pof_enabled": [
                13,
                self.chkPoF,
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Boundary Conditions"),
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.

        pub.sendMessage("request_get_option_attributes", attributes={"site_id": 1})
