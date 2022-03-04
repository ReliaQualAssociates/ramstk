# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.meter.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKFixedPanel


class MeterDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Meter assessment input attribute data in the RAMSTK Work Book.

    The Meter assessment input view displays all the assessment inputs for
    the selected Meter item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Meter assessment input view are:

    :cvar dict _dic_quality: dictionary of meter quality levels.  Key is
        meter subcategory ID; values are lists of quality levels.
    :cvar dict _dic_type: dictionary of meter types.  Key is meter
        subcategory ID; values are lists of types.
    :cvar dict _dic_specification: dictionary of meter MIL-SPECs.  Key is
        meter tye ID; values are lists of specifications.
    :cvar dict _dic_insert: dictionary of meter insert materials.  First
        key is meter type ID, second key is meter specification ID; values are
        lists of insert materials.

    :ivar cmbApplication: select and display the application of the meter.
    :ivar cmbType: select and display the type of meter.
    """

    # Define private dict class attributes.

    # Quality levels; key is the subcategory ID.
    _dic_quality: Dict[int, List[List[str]]] = {
        2: [["MIL-SPEC"], [_("Lower")]],
        1: [["MIL-SPEC"], [_("Lower")]],
    }
    # Meter types; key is the subcategory ID.
    _dic_types: Dict[int, List[List[str]]] = {
        1: [[_("AC")], [_("Inverter Driver")], [_("Commutator DC")]],
        2: [[_("Direct Current")], [_("Alternating Current")]],
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Meter Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Meter assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
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
                    "tooltip": _("The quality level of the meter."),
                },
                _("Quality Level:"),
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
                    "tooltip": _("The type of meter."),
                },
                _("Meter Type:"),
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
                    "tooltip": _("The application of the panel meter."),
                },
                _("Meter Function:"),
                "gint",
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
            self._do_set_reliability_attributes,
            "succeed_get_reliability_attributes",
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the meter assessment input RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected meter.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            _data = [["MIL-SPEC"], [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[self.subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data, signal="changed")

        # Load the meter application RAMSTKComboBox().
        self.cmbApplication.do_load_combo(
            [[_("Ammeter")], [_("Voltmeter")], [_("Other")]], signal="changed"
        )

        # Load the meter type RAMSTKComboBox().
        try:
            _data = self._dic_types[self.subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data, signal="changed")

        self._do_set_sensitive()

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
        """Set widget sensitivity as needed for the selected meter.

        :return: None
        :rtype: None
        """
        self.cmbApplication.set_sensitive(False)
        self.cmbType.set_sensitive(True)

        if self._hazard_rate_method_id == 2 and self.subcategory_id == 2:
            self.cmbApplication.set_sensitive(True)
