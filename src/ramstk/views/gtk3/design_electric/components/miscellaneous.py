# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.miscellaneous.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Miscellaneous Devices Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel


class MiscDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Miscellaneous assessment input attribute data.

    The Miscellaneous hardware assessment input view displays all the
    assessment inputs for the selected miscellaneous hardware item.  This
    includes, currently, inputs for MIL-HDBK-217FN2.  The attributes of a
    Miscellaneous hardware assessment input view are:

    :ivar cmbApplication: select and display the application of the
        miscellaneous item (lamps only).
    :ivar cmbType: the type of miscellaneous item (filters only).
    :ivar txtFrequency: enter and display the operating frequency of the
        miscellaneous item (crystals only).
    :ivar txtUtilization: enter and display the utilization factor of the
        miscellaneous item (lamps only).
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Miscellaneous Device Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize instance of the Miscellaneous assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtFrequency: RAMSTKEntry = RAMSTKEntry()
        self.txtUtilization: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._duty_cycle: float = 100.0
        self._hazard_rate_method_id: int = 0
        self._quality_id: int = 0

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map = self._do_initialize_attribute_widget_map()

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.do_load_comboboxes,
                "succeed_get_hardware_attributes": self._set_hardware_attributes,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the miscellaneous assessment input RKTComboBox()s.

        :param subcategory_id: the subcategory ID of the selected miscellaneous device.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.cmbApplication.do_load_combo(
            [
                [_("Incandescent, AC")],
                [_("Incandescent, DC")],
            ],
            signal="changed",
        )
        self.cmbQuality.do_load_combo(
            [
                ["MIL-SPEC"],
                [_("Lower")],
            ],
            signal="changed",
        )
        self.cmbType.do_load_combo(
            self._get_type_list(),
            signal="changed",
        )

        self._set_sensitive()

    def _do_initialize_attribute_widget_map(self) -> Dict[str, Any]:
        """Initialize the attribute widget map."""
        return {
            "quality_id": [
                32,
                self.cmbQuality,
                "changed",
                super().on_changed_combo,
                "wvw_editing_reliability",
                0,
                {
                    "tooltip": _("The quality level."),
                },
                _("Quality Level:"),
                "gint",
            ],
            "application_id": [
                2,
                self.cmbApplication,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The application of the lamp."),
                },
                _("Application:"),
                "gint",
            ],
            "type_id": [
                48,
                self.cmbType,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The type of electronic filter."),
                },
                _("Type:"),
                "gint",
            ],
            "frequency_operating": [
                17,
                self.txtFrequency,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The operating frequency of the crystal."),
                },
                _("Operating Frequency:"),
                "gfloat",
            ],
            "duty_cycle": [
                12,
                self.txtUtilization,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                100.0,
                {
                    "tooltip": _(
                        "The utilization factor (illuminate hours / equipment operate "
                        "hours) of the lamp."
                    ),
                },
                _("Utilization:"),
                "gfloat",
            ],
        }

    def _get_type_list(self) -> List[List[str]]:
        """Return the type list to load into the RAMSTKComboBox().

        :return: list of types for electronic filters.
        :rtype: list
        """
        _type_lists = {
            1: [
                [_("Ceramic-Ferrite")],
                [_("Discrete LC Components")],
                [_("Discrete LC and Crystal Components")],
            ],
            2: [
                [_("MIL-F-15733 Ceramic-Ferrite")],
                [_("MIL-F-15733 Discrete LC Components")],
                [_("MIL-F-18327 Discrete LC Components")],
                [_("MIL-F-18327 Discrete LC and Crystal Components")],
            ],
        }
        return _type_lists.get(self._hazard_rate_method_id, [[""]])

    def _set_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the hardware attributes are retrieved.

        :param attributes: the dict of hardware attributes.
        :return: None
        :rtype: None
        """
        if attributes["hardware_id"] == self._record_id:
            self._duty_cycle = attributes["duty_cycle"]

    def _set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self._set_sensitive()
        super().set_widget_sensitivity([self.cmbQuality])
        self.cmbQuality.do_update(
            self._quality_id,
            signal="changed",
        )

    def _set_sensitive(self) -> None:
        """Set widget sensitivity for the selected Miscellaneous item.

        :return: None
        :rtype: None
        """
        # Reset all widgets to be insensitive.
        super().set_widget_sensitivity(
            [
                self.cmbApplication,
                self.cmbType,
                self.txtFrequency,
                self.txtUtilization,
            ],
            False,
        )

        # Define sensitivity map for each subcategory
        _sensitivity_map = {
            1: [self.txtFrequency],  # Crystal
            2: [self.cmbType],  # Electronic filter
            3: [self.cmbApplication],  # Lamp
        }

        # Determine sensitivity list based on subcategory
        _sensitivity_list = _sensitivity_map.get(self.subcategory_id, [])

        # Set widget sensitivity based on hazard rate method
        if self._hazard_rate_method_id == 2:
            _sensitivity_list += [self.txtUtilization]
        super().set_widget_sensitivity(_sensitivity_list)
