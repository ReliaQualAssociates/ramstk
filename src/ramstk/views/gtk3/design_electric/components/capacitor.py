# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.capacitor.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# RAMSTK Package Imports
from ramstk.constants.capacitor import (
    CAPACITOR_QUALITY_DICT,
    CAPACITOR_SPECIFICATION_DICT,
    CAPACITOR_STYLE_DICT,
    CAPACITOR_STYLE_DICT2,
)
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class CapacitorDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Capacitor assessment input attribute data.

    The Capacitor assessment input view displays all the assessment inputs for
    the selected capacitor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analyses.  The attributes of a
    Capacitor assessment input view are:

    :ivar list _lst_labels: list of strings for labels to display for the capacitor
        MIL-HDBK-217 input parameters.

    :ivar cmbConfiguration: select and display the configuration of the
        capacitor.
    :ivar cmbConstruction: select and display the capacitor's method of construction.
    :ivar cmbSpecification: select and display the governing specification of
        the capacitor.
    :ivar cmbStyle: select and display the style of the capacitor.
    :ivar txtCapacitance: enter and display the capacitance rating of the
        capacitor.
    :ivar txtESR: enter and display the equivalent series resistance.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Capacitor Design Inputs")

    def __init__(self) -> None:
        """Initialize an instance of the Capacitor assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbConfiguration: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbStyle: RAMSTKComboBox = RAMSTKComboBox()
        self.txtCapacitance: RAMSTKEntry = RAMSTKEntry()
        self.txtESR: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.cmbQuality,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "quality_id",
                    "index": 32,
                    "label_text": _("Quality Level:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_reliability",
                },
                {
                    "editable": True,
                    "tooltip": _("The quality level of the capacitor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtCapacitance,
                {
                    "datatype": "gfloat",
                    "default": 0,
                    "field": "capacitance",
                    "index": 4,
                    "label_text": _("Capacitance (F):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The capacitance rating (in farads) of the capacitor."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbSpecification,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "specification_id",
                    "index": 36,
                    "label_text": _("Specification:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The governing specification for the capacitor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbStyle,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "type_id",
                    "index": 48,
                    "label_text": _("Style:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The style of the capacitor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbConfiguration,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "configuration_id",
                    "index": 5,
                    "label_text": _("Configuration:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The configuration of the capacitor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbConstruction,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "construction_id",
                    "index": 6,
                    "label_text": _("Construction:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The method of construction of the capacitor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtESR,
                {
                    "datatype": "gfloat",
                    "default": 0,
                    "field": "resistance",
                    "index": 35,
                    "label_text": _("Equivalent Series Resistance (\u03a9):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The equivalent series resistance of the capacitor."),
                    "visible": True,
                },
            ),
        ]
        self._hazard_rate_method_id: int = 0
        self._quality_id: int = 0

        # Initialize public instance attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        self._do_set_widget_callbacks()
        self._do_load_configuration()
        self._do_load_construction()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.on_subcategory_change,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def on_subcategory_change(self, subcategory_id: int) -> None:
        """Load the capacitor RAMSTKComboBoxes with subcategory specific entries.

        :param subcategory_id: the subcategory ID of the selected capacitor.
        """
        self.subcategory_id = subcategory_id

        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
        )
        self.cmbSpecification.do_load_combo(
            CAPACITOR_SPECIFICATION_DICT.get(self.subcategory_id, [[""]]),
        )
        self.cmbStyle.do_load_combo(
            [],
        )

        self._set_sensitive()

    def _do_load_configuration(self) -> None:
        """Load the configuration RAMSTKComboBox."""
        self.cmbConfiguration.do_load_combo(
            [
                [_("Fixed")],
                [_("Variable")],
            ],
        )

    def _do_load_construction(self) -> None:
        """Load the construction RAMSTKComboBox."""
        self.cmbConstruction.do_load_combo(
            [
                [_("Slug, All Tantalum")],
                [_("Foil, Hermetic")],
                [_("Slug, Hermetic")],
                [_("Foil, Non-Hermetic")],
                [_("Slug, Non-Hermetic")],
            ],
        )

    def _do_load_styles(self, combo: RAMSTKComboBox) -> None:
        """Load the style RAMSTKComboBox when the specification changes.

        :param combo: the specification RAMSTKCombo that called this method.
        """
        self.cmbStyle.do_load_combo(
            self._get_style_list(combo),
        )

    def _do_set_widget_callbacks(self) -> None:
        """Set the callbacks for the widgets in the Capacitor assessment input view."""
        super().do_set_widget_callbacks()

        self.cmbSpecification.connect("changed", self._do_load_styles)

    def _get_quality_list(self) -> List[Union[str, List[str]]]:
        """Return the list of quality levels based on subcategory.

        :return: list of capacitor quality levels.
        :rtype: list
        """
        return (
            ["S", "R", "P", "M", "L", ["MIL-SPEC"], [_("Lower")]]
            if self._hazard_rate_method_id == 1
            else CAPACITOR_QUALITY_DICT.get(self.subcategory_id, [[""]])
        )

    def _get_style_list(self, combo: RAMSTKComboBox) -> List[List[str]]:
        """Return the list of styles based on the subcategory and specification.

        :param combo: the specification RAMSTKComboBox() from which the active index is
            retrieved.
        :return: the list of styles for the current subcategory and specification.
        :rtype: List[List[str]]
        """
        # Determine the styles based on the subcategory and active specification index
        try:
            if self.subcategory_id in [1, 3, 4, 7, 9, 10, 11, 13]:
                # Get the active index from the combo box
                _active_index = int(combo.get_active()) - 1
                # Select styles based on the active index
                _styles: List[List[str]] = (
                    CAPACITOR_STYLE_DICT[self.subcategory_id][_active_index]
                    if 0
                    <= _active_index
                    < len(CAPACITOR_STYLE_DICT[self.subcategory_id])
                    else []
                )
            else:
                # Use default styles for the subcategory
                _styles = CAPACITOR_STYLE_DICT2[self.subcategory_id]

        except (KeyError, ValueError, IndexError):
            # Handle any errors that occur (e.g., invalid index)
            _styles = []

        return _styles

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self._set_sensitive()
        super().do_set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            {"quality_id": self._quality_id},
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected capacitor type."""
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbConstruction,
            self.cmbConfiguration,
            self.cmbSpecification,
            self.cmbStyle,
            self.txtCapacitance,
            self.txtESR,
        ]

        # Reset all widgets to be insensitive.
        super().do_set_widget_sensitivity(
            _all_widgets,
            False,
        )

        # Define default sensitivity list
        _default_sensitivity_list = [
            self.cmbSpecification,
            self.cmbStyle,
            self.txtCapacitance,
        ]
        # Define sensitivity map for each subcategory
        _sensitivity_map = {
            12: _default_sensitivity_list + [self.txtESR],
            13: _default_sensitivity_list + [self.cmbConstruction],
            19: _default_sensitivity_list + [self.cmbConfiguration],
        }

        # Determine sensitivity list based on subcategory
        _sensitivity_list = _sensitivity_map.get(
            self.subcategory_id, _default_sensitivity_list
        )

        # Set widget sensitivity based on hazard rate method
        if self._hazard_rate_method_id == 1:
            super().do_set_widget_sensitivity([self.cmbSpecification])
        else:
            super().do_set_widget_sensitivity(_sensitivity_list)
