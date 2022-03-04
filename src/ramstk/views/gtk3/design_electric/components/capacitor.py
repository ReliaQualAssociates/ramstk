# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.capacitor.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel


class CapacitorDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Capacitor assessment input attribute data.

    The Capacitor assessment input view displays all the assessment inputs for
    the selected capacitor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analyses.  The attributes of a
    Capacitor assessment input view are:

    :cvar dict _dic_quality: dictionary of MIL-HDBK-217 capacitor quality
        levels.  Key is capacitor subcategory ID; values are lists of quality
        levels.
    :cvar dict _dic_specifications: dictionary of capacitor MIL-SPECs.  Key is
        capacitor subcategory ID; values are lists of specifications.
    :cvar dict _dic_styles: dictionary of capacitor styles defined in the
        MIL-SPECs.  Key is capacitor subcategory ID; values are lists of
        styles.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.
    :ivar _lst_widgets: the list of widgets to display in the panel.  These
        are listed in the order they should appear on the panel.

    :ivar cmbConfiguration: select and display the configuration of the
        capacitor.
    :ivar cmbConstruction: select and display the method of construction of the
        capacitor.
    :ivar cmbSpecification: select and display the governing specification of
        the capacitor.
    :ivar cmbStyle: select and display the style of the capacitor.
    :ivar txtCapacitance: enter and display the capacitance rating of the
        capacitor.
    :ivar txtESR: enter and display the equivalent series resistance.
    """

    # Define private dictionary class attributes.
    _dic_quality: Dict[int, List[Any]] = {
        1: [["MIL-SPEC"], [_("Lower")]],
        2: [
            ["M"],
            [_("MIL-C-11693 Non-Established Reliability")],
            [_("Lower")],
        ],
        3: [
            "S",
            "R",
            "P",
            "M",
            "L",
            [_("MIL-C-19978 Non-Established Reliability")],
            [_("Lower")],
        ],
        4: [
            "S",
            "R",
            "P",
            "M",
            "L",
            [_("MIL-C-18312 Non-Established Reliability")],
            [_("Lower")],
        ],
        5: ["S", "R", "P", "M", [_("Lower")]],
        6: ["S", "R", "P", "M", [_("Lower")]],
        7: [
            "T",
            "S",
            "R",
            "P",
            "M",
            "L",
            [_("MIL-C-5 Non-Established Reliability, Dipped")],
            [_("MIL-C-5 Non-Established Reliability, Molded")],
            [_("Lower")],
        ],
        8: [["MIL-C-10950"], [_("Lower")]],
        9: [
            "S",
            "R",
            "P",
            "M",
            "L",
            [_("MIL-C-11272 Non-Established Reliability")],
            [_("Lower")],
        ],
        10: [
            "S",
            "R",
            "P",
            "M",
            "L",
            [_("MIL-C-11015 Non-Established Reliability")],
            [_("Lower")],
        ],
        11: [
            "S",
            "R",
            "P",
            "M",
            [_("MIL-C-20 Non-Established Reliability")],
            [_("Lower")],
        ],
        12: ["D", "C", "S", "B", "R", "P", "M", "L", [_("Lower")]],
        13: [
            "S",
            "R",
            "P",
            "M",
            "L",
            [_("MIL-C-3965 Non-Established Reliability")],
            [_("Lower")],
        ],
        14: [
            "S",
            "R",
            "P",
            "M",
            [_("MIL-C-39018 Non-Established Reliability")],
            [_("Lower")],
        ],
        15: [["MIL-SPEC"], [_("Lower")]],
        16: [["MIL-SPEC"], [_("Lower")]],
        17: [["MIL-SPEC"], [_("Lower")]],
        18: [["MIL-SPEC"], [_("Lower")]],
        19: [["MIL-SPEC"], [_("Lower")]],
    }
    _dic_specifications: Dict[int, List[Any]] = {
        1: [["MIL-C-25"], ["MIL-C-12889"]],
        2: [["MIL-C-11693"]],
        3: [["MIL-C-14157"], ["MIL-C-19978"]],
        4: [["MIL-C-18312"], ["MIL-C-39022"]],
        5: [["MIL-C-55514"]],
        6: [["MIL-C-83421"]],
        7: [["MIL-C-5"], ["MIL-C-39001"]],
        8: [["MIL-C-10950"]],
        9: [["MIL-C-11272"], ["MIL-C-23269"]],
        10: [["MIL-C-11015"], ["MIL-C-39014"]],
        11: [["MIL-C-20"], ["MIL-C-55681"]],
        12: [["MIL-C-39003"]],
        13: [["MIL-C-3965"], ["MIL-C-39006"]],
        14: [["MIL-C-39018"]],
        15: [["MIL-C-62"]],
        16: [["MIL-C-81"]],
        17: [["MIL-C-14409"]],
        18: [["MIL-C-92"]],
        19: [["MIL-C-23183"]],
    }
    _dic_styles: Dict[int, List[Any]] = {
        1: [
            [
                ["CP4"],
                ["CP5"],
                ["CP8"],
                ["CP9"],
                ["CP10"],
                ["CP11"],
                ["CP12"],
                ["CP13"],
                ["CP25"],
                ["CP26"],
                ["CP27"],
                ["CP28"],
                ["CP29"],
                ["CP40"],
                ["CP41"],
                ["CP67"],
                ["CP69"],
                ["CP70"],
                ["CP72"],
                ["CP75"],
                ["CP76"],
                ["CP77"],
                ["CP78"],
                ["CP80"],
                ["CP81"],
                ["CP82"],
            ],
            [["CA"]],
        ],
        2: [
            [_("Characteristic E")],
            [_("Characteristic K")],
            [_("Characteristic P")],
            [_("Characteristic W")],
        ],
        3: [
            [["CPV07"], ["CPV09"], ["CPV17"]],
            [
                [_("Characteristic E")],
                [_("Characteristic F")],
                [_("Characteristic G")],
                [_("Characteristic K")],
                [_("Characteristic L")],
                [_("Characteristic M")],
                [_("Characteristic P")],
                [_("Characteristic Q")],
                [_("Characteristic S")],
                [_("Characteristic T")],
            ],
        ],
        4: [
            [[_("Characteristic N")], [_("Characteristic R")]],
            [
                [_("Characteristic 1")],
                [_("Characteristic 9")],
                [_("Characteristic 10")],
                [_("Characteristic 12")],
                [_("Characteristic 19")],
                [_("Characteristic 29")],
                [_("Characteristic 49")],
                [_("Characteristic 59")],
            ],
        ],
        5: [
            [_("Characteristic M")],
            [_("Characteristic N")],
            [_("Characteristic Q")],
            [_("Characteristic R")],
            [_("Characteristic S")],
        ],
        6: [["CRH"]],
        7: [
            [
                [_("Temperature Range M")],
                [_("Temperature Range N")],
                [_("Temperature Range O")],
                [_("Temperature Range P")],
            ],
            [[_("Temperature Range O")], [_("Temperature Range P")]],
        ],
        8: [["CB50"], [_("Other")]],
        9: [
            [[_("Temperature Range C")], [_("Temperature Range D")]],
            [[_("All")]],
        ],
        10: [
            [
                [_("Type A Rated Temperature")],
                [_("Type B Rated Temperature")],
                [_("Type C Rated Temperature")],
            ],
            [
                ["CKR05"],
                ["CKR06"],
                ["CKR07"],
                ["CKR08"],
                ["CKR09"],
                ["CKR10"],
                ["CKR11"],
                ["CKR12"],
                ["CKR13"],
                ["CKR14"],
                ["CKR15"],
                ["CKR16"],
                ["CKR17"],
                ["CKR18"],
                ["CKR19"],
                ["CKR48"],
                ["CKR64"],
                ["CKR72"],
                ["CKR73"],
                ["CKR74"],
            ],
        ],
        11: [
            [
                ["CC5"],
                ["CC6"],
                ["CC7"],
                ["CC8"],
                ["CC9"],
                ["CC13"],
                ["CC14"],
                ["CC15"],
                ["CC16"],
                ["CC17"],
                ["CC18"],
                ["CC19"],
                ["CC20"],
                ["CC21"],
                ["CC22"],
                ["CC25"],
                ["CC26"],
                ["CC27"],
                ["CC30"],
                ["CC31"],
                ["CC32"],
                ["CC33"],
                ["CC35"],
                ["CC36"],
                ["CC37"],
                ["CC45"],
                ["CC47"],
                ["CC50"],
                ["CC51"],
                ["CC52"],
                ["CC53"],
                ["CC54"],
                ["CC55"],
                ["CC56"],
                ["CC57"],
                ["CC75"],
                ["CC76"],
                ["CC77"],
                ["CC78"],
                ["CC79"],
                ["CC81"],
                ["CC82"],
                ["CC83"],
                ["CC85"],
                ["CC95"],
                ["CC96"],
                ["CC97"],
                ["CCR05"],
                ["CCR06"],
                ["CCR07"],
                ["CCR08"],
                ["CCR09"],
                ["CCR13"],
                ["CCR14"],
                ["CCR15"],
                ["CCR16"],
                ["CCR17"],
                ["CCR18"],
                ["CCR19"],
                ["CCR54"],
                ["CCR55"],
                ["CCR56"],
                ["CCR57"],
                ["CCR75"],
                ["CCR76"],
                ["CCR77"],
                ["CCR78"],
                ["CCR79"],
                ["CCR81"],
                ["CCR82"],
                ["CCR83"],
                ["CCR90"],
            ],
            [["CDR"]],
        ],
        12: [["CSR"]],
        13: [
            [
                ["CL10"],
                ["CL13"],
                ["CL14"],
                ["CL16"],
                ["CL17"],
                ["CL18"],
                ["CL24"],
                ["CL25"],
                ["CL26"],
                ["CL27"],
                ["CL30"],
                ["CL31"],
                ["CL32"],
                ["CL33"],
                ["CL34"],
                ["CL35"],
                ["CL36"],
                ["CL37"],
                ["CL40"],
                ["CL41"],
                ["CL42"],
                ["CL43"],
                ["CL46"],
                ["CL47"],
                ["CL48"],
                ["CL49"],
                ["CL50"],
                ["CL51"],
                ["CL52"],
                ["CL53"],
                ["CL54"],
                ["CL55"],
                ["CL56"],
                ["CL64"],
                ["CL65"],
                ["CL66"],
                ["CL67"],
                ["CL70"],
                ["CL71"],
                ["CL72"],
                ["CL73"],
            ],
            [["CLR"]],
        ],
        14: [
            [_("Style 16")],
            [_("Style 17")],
            [_("Style 71")],
            [_("All Others")],
        ],
        15: [["CE"]],
        16: [
            ["CV11"],
            ["CV14"],
            ["CV21"],
            ["CV31"],
            ["CV32"],
            ["CV34"],
            ["CV35"],
            ["CV36"],
            ["CV40"],
            ["CV41"],
        ],
        17: [
            [_("Style G")],
            [_("Style H")],
            [_("Style J")],
            [_("Style L")],
            [_("Style Q")],
            [_("Style T")],
        ],
        18: [["CT"]],
        19: [
            ["CG20"],
            ["CG21"],
            ["CG30"],
            ["CG31"],
            ["CG32"],
            ["CG40"],
            ["CG41"],
            ["CG42"],
            ["CG43"],
            ["CG44"],
            ["CG50"],
            ["CG51"],
            ["CG60"],
            ["CG61"],
            ["CG62"],
            ["CG63"],
            ["CG64"],
            ["CG65"],
            ["CG66"],
            ["CG67"],
        ],
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Capacitor Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

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

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = 0
        self._quality_id: int = 0

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map = {
            "quality_id": [
                32,
                self.cmbQuality,
                "changed",
                super().on_changed_combo,
                "wvw_editing_reliability",
                0,
                {
                    "tooltip": _("The quality level of the capacitor."),
                },
                _("Quality Level:"),
                "gint",
            ],
            "capacitance": [
                4,
                self.txtCapacitance,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The capacitance rating (in farads) of the capacitor."
                    ),
                },
                _("Capacitance (F):"),
                "gfloat",
            ],
            "specification_id": [
                36,
                self.cmbSpecification,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The governing specification for the capacitor."),
                },
                _("Specification:"),
                "gint",
            ],
            "type_id": [
                48,
                self.cmbStyle,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The style of the capacitor."),
                },
                _("Style:"),
                "gint",
            ],
            "configuration_id": [
                5,
                self.cmbConfiguration,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The configuration of the capacitor."),
                },
                _("Configuration:"),
                "gint",
            ],
            "construction_id": [
                6,
                self.cmbConstruction,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The method of construction of the capacitor."),
                },
                _("Construction:"),
                "gint",
            ],
            "resistance": [
                35,
                self.txtESR,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The equivalent series resistance of the capacitor."),
                },
                _("Equivalent Series Resistance (\u03A9):"),
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

        self.cmbSpecification.connect("changed", self._do_load_styles)

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
        """Load the capacitor assessment input RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected capacitor.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F parts count.
            _quality: List[Any] = [
                "S",
                "R",
                "P",
                "M",
                "L",
                ["MIL-SPEC"],
                [_("Lower")],
            ]
        else:
            try:
                _quality = self._dic_quality[self.subcategory_id]
            except KeyError:
                _quality = []

        self.cmbQuality.do_load_combo(_quality, signal="changed")

        try:
            _specification: List[Any] = self._dic_specifications[self.subcategory_id]
        except KeyError:
            _specification = []

        self.cmbSpecification.do_load_combo(_specification, signal="changed")

        self.cmbStyle.do_load_combo([], signal="changed")

        self.cmbConfiguration.do_load_combo(
            [[_("Fixed")], [_("Variable")]], signal="changed"
        )

        _construction: List[Any] = [
            [_("Slug, All Tantalum")],
            [_("Foil, Hermetic")],
            [_("Slug, Hermetic")],
            [_("Foil, Non-Hermetic")],
            [_("Slug, Non-Hermetic")],
        ]
        self.cmbConstruction.do_load_combo(_construction, signal="changed")

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

    def _do_load_styles(self, combo: RAMSTKComboBox) -> None:
        """Load the style RAMSTKComboBox() when the specification changes.

        :param combo: the specification RAMSTKCombo() that called this method.
        :return: None
        :rtype: None
        """
        # If the capacitor specification changed, load the capacitor style
        # RAMSTKComboBox().
        try:
            if self.subcategory_id in [1, 3, 4, 7, 9, 10, 11, 13]:
                _idx = int(combo.get_active()) - 1
                _styles = self._dic_styles[self.subcategory_id][_idx]
            else:
                _styles = self._dic_styles[self.subcategory_id]
        except KeyError:
            _styles = []
        self.cmbStyle.do_load_combo(entries=_styles, signal="changed")

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected capacitor type.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:
            self.__do_set_parts_count_sensitive()
        else:
            self.__do_set_part_stress_sensitive()

    # pylint: disable=unused-argument
    def __do_set_parts_count_sensitive(self) -> None:
        """Set widget sensitivity as needed for MIL-HDBK-217F, Parts Count.

        :return: None
        :rtype: None
        """
        if self.subcategory_id == 1:
            self.cmbSpecification.set_sensitive(True)
        else:
            self.cmbSpecification.set_sensitive(False)
            self.cmbStyle.set_sensitive(False)
            self.cmbConfiguration.set_sensitive(False)
            self.cmbConstruction.set_sensitive(False)
            self.txtCapacitance.set_sensitive(False)
            self.txtESR.set_sensitive(False)

    def __do_set_part_stress_sensitive(self) -> None:
        """Set widget sensitivity as needed for MIL-HDBK-217F, Part Stress.

        :return: None
        :rtype: None
        """
        self.cmbSpecification.set_sensitive(True)
        self.cmbStyle.set_sensitive(True)
        self.txtCapacitance.set_sensitive(True)
        self.txtESR.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.cmbConfiguration.set_sensitive(False)

        if self.subcategory_id == 12:
            self.txtESR.set_sensitive(True)

        if self.subcategory_id == 13:
            self.cmbConstruction.set_sensitive(True)

        if self.subcategory_id == 19:
            self.cmbConfiguration.set_sensitive(True)
