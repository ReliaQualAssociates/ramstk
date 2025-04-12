# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.resistor.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List, cast

# RAMSTK Package Imports
from ramstk.constants.resistor import (
    RESISTOR_CONSTRUCTION_DICT,
    RESISTOR_QUALITY_DICT,
    RESISTOR_SPECIFICATION_DICT,
    RESISTOR_STYLE_DICT,
    RESISTOR_TYPE_DICT,
)
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
)


class ResistorDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Resistor assessment input attribute data.

    The Resistor assessment input view displays all the assessment inputs for the
    selected resistor.  This includes, currently, inputs for MIL-HDBK-217FN2.  The
    attributes of a Resistor assessment input view are:

    :ivar cmbSpecification: select and display the governing specification of     the
    resistor.
    :ivar cmbType: select and display the type of thermistor.
    :ivar cmbConstruction: select and display the method of construction of the
        resistor.
    :ivar txtResistance: enter and display the resistance of the resistor.
    :ivar txtNElements: enter and display the number of active resistors in a resistor
    network or the number of potentiometers taps.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Resistor Design Inputs")

    def __init__(self) -> None:
        """Initialize an instance of the Resistor assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbStyle: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()
        self.txtResistance: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            {
                "widget": self.cmbQuality,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "quality_id",
                    "index": 32,
                    "label_text": _("Quality Level:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The quality level of the resistor."),
                    "visible": True,
                },
            },
            {
                "widget": self.txtResistance,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0,
                    "field": "resistance",
                    "index": 35,
                    "label_text": _("Resistance (\u03a9):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The resistance (in \u03a9) of the resistor."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbSpecification,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "specification_id",
                    "index": 36,
                    "label_text": _("Specification:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The governing specification for the resistor."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbType,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "type_id",
                    "index": 48,
                    "label_text": _("Type:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The type of thermistor."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbStyle,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "family_id",
                    "index": 15,
                    "label_text": _("Style:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The style of resistor."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbConstruction,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "construction_id",
                    "index": 6,
                    "label_text": _("Construction:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The method of construction of the resistor."),
                    "visible": True,
                },
            },
            {
                "widget": self.txtNElements,
                "attributes": {
                    "datatype": "gint",
                    "default": 0.0,
                    "field": "n_elements",
                    "index": 2,
                    "label_text": _("Number of Elements:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The number of active resistors in a resistor network or the "
                        "number of potentiometer taps."
                    ),
                    "visible": True,
                },
            },
        ]
        self._hazard_rate_method_id: int = 0
        self._quality_id: int = 0

        # Initialize public instance attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_panel()
        super().do_set_widget_callbacks()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.on_subcategory_change,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def on_subcategory_change(self, subcategory_id: int) -> None:
        """Load the resistor RAMSTKComboBoxes with subcategory specific entries.

        :param subcategory_id: the subcategory ID of the selected capacitor. This is
            unused in this method but required because this method is a PyPubSub
            listener.
        """
        self.subcategory_id = subcategory_id

        self.cmbConstruction.do_load_combo(
            RESISTOR_CONSTRUCTION_DICT.get(self.subcategory_id, [[""]]),
        )
        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
        )
        self.cmbSpecification.do_load_combo(
            RESISTOR_SPECIFICATION_DICT.get(self.subcategory_id, [[""]]),
        )
        self.cmbStyle.do_load_combo(
            self._get_style_list(),
        )
        self.cmbType.do_load_combo(
            self._get_type_list(),
        )

        self._set_sensitive()

    def _get_quality_list(self) -> List[List[str]]:
        """Return the list of resistor quality levels.

        :return: list of resistor quality levels.
        :rtype: list
        """
        _default_quality_list: List[List[str]] = [
            ["S"],
            ["R"],
            ["P"],
            ["M"],
            ["MIL-SPEC"],
            [_("Lower")],
        ]

        if self._hazard_rate_method_id == 1:
            return _default_quality_list

        _list = RESISTOR_QUALITY_DICT.get(self.subcategory_id, [[""]])
        return cast(List[List[str]], _list)

    def _get_style_list(self) -> List[List[str]]:
        """Return the list of resistor styles.

        :return: list of resistor styles.
        :rtype: list
        """
        _specification_id = int(self.cmbSpecification.get_active())
        _spec_list: Dict[int, List[List[str]]] = cast(
            Dict[int, List[List[str]]], RESISTOR_STYLE_DICT[self.subcategory_id]
        )
        _style_list = _spec_list.get(_specification_id, [[""]])
        return cast(List[List[str]], _style_list)

    def _get_type_list(self) -> List[List[str]]:
        """Return the list of resistor (thermistor) types.

        :return: list of resistor types.
        :rtype: list
        """
        _default_type_list = [[_("Bead")], [_("Disk")], [_("Rod")]]

        if self._hazard_rate_method_id == 2:
            return _default_type_list

        _list = RESISTOR_TYPE_DICT.get(self.subcategory_id, [[""]])
        return cast(List[List[str]], _list)

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self._set_sensitive()
        super().set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            {"quality_id": self._quality_id},
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected resistor."""
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbConstruction,
            self.cmbSpecification,
            self.cmbStyle,
            self.cmbType,
            self.txtNElements,
            self.txtResistance,
        ]

        # Reset all widgets to be insensitive.
        super().do_set_widget_sensitivity(
            _all_widgets,
            False,
        )

        # Set txtResistance sensitive if hazard_rate_method_id is 2
        if self._hazard_rate_method_id == 2:
            self.txtResistance.set_sensitive(True)

        # Define a sensitivity map for different widgets based on hazard rate method
        # and subcategory
        _sensitivity_map = {
            1: {
                1: [self.cmbType],
                2: [self.cmbType],
                5: [self.cmbType],
                6: [self.cmbType],
                7: [self.cmbType],
                9: [self.cmbType],
                11: [self.cmbType],
                13: [self.cmbType],
                15: [self.cmbType],
            },
            2: {
                2: [self.cmbSpecification],
                4: [self.txtNElements],
                6: [
                    self.cmbSpecification,
                    self.cmbStyle,
                ],
                7: [
                    self.cmbSpecification,
                    self.cmbStyle,
                ],
                8: [self.cmbType],
                9: [self.txtNElements],
                10: [
                    self.cmbConstruction,
                    self.txtNElements,
                ],
                11: [self.txtNElements],
                12: [
                    self.cmbConstruction,
                    self.txtNElements,
                ],
                13: [self.txtNElements],
                14: [self.txtNElements],
                15: [
                    self.cmbSpecification,
                    self.txtNElements,
                ],
            },
        }

        super().do_set_widget_sensitivity(
            _sensitivity_map.get(self._hazard_rate_method_id, {}).get(
                self.subcategory_id, []
            )
        )
