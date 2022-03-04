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

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
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
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
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

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self.do_load_comboboxes,
            "changed_subcategory",
        )
        pub.subscribe(
            self._do_set_hardware_attributes,
            "succeed_get_hardware_attributes",
        )
        pub.subscribe(
            self._do_set_reliability_attributes,
            "succeed_get_reliability_attributes",
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the miscellaneous assessment input RKTComboBox()s.

        :param subcategory_id: the subcategory ID of the selected miscellaneous device.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([["MIL-SPEC"], [_("Lower")]], signal="changed")

        # Load the application RAMSTKComboBox().
        self.cmbApplication.do_load_combo(
            [[_("Incandescent, AC")], [_("Incandescent, DC")]],
            signal="changed",
        )

        # Load the type RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            self.cmbType.do_load_combo(
                [
                    [_("Ceramic-Ferrite")],
                    [_("Discrete LC Components")],
                    [_("Discrete LC and Crystal Components")],
                ],
                signal="changed",
            )
        elif self._hazard_rate_method_id == 2:
            self.cmbType.do_load_combo(
                [
                    [_("MIL-F-15733 Ceramic-Ferrite")],
                    [_("MIL-F-15733 Discrete LC Components")],
                    [_("MIL-F-18327 Discrete LC Components")],
                    [_("MIL-F-18327 Discrete LC and Crystal Components")],
                ],
                signal="changed",
            )

        self._do_set_sensitive()

    def _do_set_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the hardware attributes are retrieved.

        :param attributes: the dict of hardware attributes.
        :return: None
        :rtype: None
        """
        if attributes["hardware_id"] == self._record_id:
            self._duty_cycle = attributes["duty_cycle"]

    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._quality_id = attributes["quality_id"]

        self.cmbQuality.set_sensitive(True)
        self.cmbQuality.do_update(
            self._quality_id,
            signal="changed",
        )

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity for the selected Miscellaneous item.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtFrequency.set_sensitive(False)
        self.txtUtilization.set_sensitive(False)

        _dic_method = {
            1: self.__do_set_crystal_sensitive,
            2: self.__do_set_filter_sensitive,
            4: self.__do_set_lamp_sensitive,
        }
        try:
            _dic_method[self.subcategory_id]()
        except KeyError:
            pass

    def __do_set_crystal_sensitive(self) -> None:
        """Set the widget sensitivity as needed for a Crystal.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:
            self.txtFrequency.set_sensitive(True)

    def __do_set_filter_sensitive(self) -> None:
        """Set the widget sensitivity as needed for an electronic filter.

        :return: None
        :rtype: None
        """
        self.cmbType.set_sensitive(True)

    def __do_set_lamp_sensitive(self) -> None:
        """Set the widget sensitivity as needed for a Lamp.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(True)

        if self._hazard_rate_method_id == 2:
            self.txtUtilization.set_sensitive(True)
