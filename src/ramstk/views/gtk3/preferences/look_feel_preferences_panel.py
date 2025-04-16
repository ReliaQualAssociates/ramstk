# pylint: disable=unused-import, missing-docstring
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.preferences.look_feel_preferences_panel.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""THe look & feel preferences panel module."""

# Standard Library Imports
from typing import List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gdk, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKColorButton,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class LookFeelPreferencesPanel(RAMSTKFixedPanel):
    """The panel to display options to be edited."""

    # Define private class attributes.
    _select_msg = "succeed_get_preferences_attributes"
    _tag = "preferences"
    _title = _("Look &amp; Feel")

    def __init__(self) -> None:
        """Initialize an instance of the Look and Feel panel."""
        super().__init__()

        # Initialize widgets.
        self.btnRevisionBGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnRevisionFGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnFunctionBGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnFunctionFGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnRequirementsBGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnRequirementsFGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnHardwareBGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnHardwareFGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnValidationBGColor: RAMSTKColorButton = RAMSTKColorButton()
        self.btnValidationFGColor: RAMSTKColorButton = RAMSTKColorButton()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.btnRevisionBGColor,
                {
                    "datatype": "gchararray",
                    "default": "#FFFFFF",
                    "field": "revisionbg",
                    "index": 0,
                    "label_text": _("Revision Tree Background Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnRevisionFGColor,
                {
                    "datatype": "gchararray",
                    "default": "#000000",
                    "field": "revisionfg",
                    "index": 1,
                    "label_text": _("Revision Tree Foreground Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnFunctionBGColor,
                {
                    "datatype": "gchararray",
                    "default": "#FFFFFF",
                    "field": "functionbg",
                    "index": 2,
                    "label_text": _("Function Tree Background Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnFunctionFGColor,
                {
                    "datatype": "gchararray",
                    "default": "#000000",
                    "field": "functionfg",
                    "index": 3,
                    "label_text": _("Function Tree Foreground Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnRequirementsBGColor,
                {
                    "datatype": "gchararray",
                    "default": "#FFFFFF",
                    "field": "requirementbg",
                    "index": 4,
                    "label_text": _("Requirements Tree Background Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                    "width_request": 75,
                },
            ),
            make_widget_config(
                self.btnRequirementsFGColor,
                {
                    "datatype": "gchararray",
                    "default": "#000000",
                    "field": "requirementfg",
                    "index": 5,
                    "label_text": _("Requirements Tree Foreground Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                    "width_request": 75,
                },
            ),
            make_widget_config(
                self.btnHardwareBGColor,
                {
                    "datatype": "gchararray",
                    "default": "#FFFFFF",
                    "field": "hardwarebg",
                    "index": 6,
                    "label_text": _("Hardware Tree Background Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnHardwareFGColor,
                {
                    "datatype": "gchararray",
                    "default": "#000000",
                    "field": "hardwarefg",
                    "index": 7,
                    "label_text": _("Hardware Tree Foreground Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnValidationBGColor,
                {
                    "datatype": "gchararray",
                    "default": "#FFFFFF",
                    "field": "validationbg",
                    "index": 8,
                    "label_text": _("Validation Tree Background Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                },
            ),
            make_widget_config(
                self.btnValidationFGColor,
                {
                    "datatype": "gchararray",
                    "default": "#000000",
                    "field": "validationfg",
                    "index": 9,
                    "label_text": _("Validation Tree Foreground Color:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_preferences",
                },
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "height_request": 30,
                    "visible": True,
                },
            ),
        ]
        self._configuration: RAMSTKUserConfiguration = RAMSTKUserConfiguration()

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        self._do_set_widget_callbacks()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "request_load_preferences": self._do_load_panel,
            }
        )

    def _do_load_panel(self, configuration: RAMSTKUserConfiguration) -> None:
        """Load the current preference values."""
        self._configuration = configuration

        self.btnRevisionBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["revisionbg"])
        )
        self.btnRevisionFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["revisionfg"])
        )
        self.btnFunctionBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["functionbg"])
        )
        self.btnFunctionFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["functionfg"])
        )
        self.btnRequirementsBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["requirementbg"])
        )
        self.btnRequirementsFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["requirementfg"])
        )
        self.btnHardwareBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["hardwarebg"])
        )
        self.btnHardwareFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["hardwarefg"])
        )
        self.btnValidationBGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["validationbg"])
        )
        self.btnValidationFGColor.set_color(
            Gdk.color_parse(self._configuration.RAMSTK_COLORS["validationfg"])
        )

    def _do_set_color(self, colorbutton: Gtk.ColorButton, ramstk_color: int) -> None:
        """Set the selected color.

        :param colorbutton: the Gtk.ColorButton() that called this method.
        :param ramstk_color: the name of the color to set.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Retrieve the six digit hexadecimal version of the selected color.
        _color = colorbutton.get_color()
        try:
            _red = f"{int(_color.red / 255)}:#02"
        except ValueError:
            _red = f"{int(_color.red / 255)}"
        try:
            _green = f"{int(_color.green / 255)}:#02"
        except ValueError:
            _green = f"{int(_color.green / 255)}"
        try:
            _blue = f"{int(_color.blue / 255)}:#02"
        except ValueError:
            _blue = f"{int(_color.blue / 255)}"
        _color = f"#{_red}{_green}{_blue}"

        # Set the color variable.
        self._configuration.RAMSTK_COLORS[ramstk_color] = _color

    def _do_set_widget_callbacks(self) -> None:
        """Set the callback functions/methods for each of the widgets."""
        # ----- BUTTONS
        self.btnRevisionBGColor.connect("color-set", self._do_set_color, "revisionbg")
        self.btnRevisionFGColor.connect("color-set", self._do_set_color, "revisionfg")
        self.btnFunctionBGColor.connect("color-set", self._do_set_color, "functionbg")
        self.btnFunctionFGColor.connect("color-set", self._do_set_color, "functionfg")
        self.btnRequirementsBGColor.connect(
            "color-set", self._do_set_color, "requirementbg"
        )
        self.btnRequirementsFGColor.connect(
            "color-set", self._do_set_color, "requirementfg"
        )
        self.btnHardwareBGColor.connect("color-set", self._do_set_color, "hardwarebg")
        self.btnHardwareFGColor.connect("color-set", self._do_set_color, "hardwarefg")
        self.btnValidationBGColor.connect(
            "color-set", self._do_set_color, "validationbg"
        )
        self.btnValidationFGColor.connect(
            "color-set", self._do_set_color, "validationfg"
        )
