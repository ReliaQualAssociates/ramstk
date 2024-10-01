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

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel

CAPACITOR_QUALITY_DICT = {
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
CAPACITOR_SPECIFICATION_DICT = {
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
    12: [["MIL-C-39003"], ["MIL-C-55365"]],
    13: [["MIL-C-3965"], ["MIL-C-39006"]],
    14: [["MIL-C-39018"]],
    15: [["MIL-C-62"]],
    16: [["MIL-C-81"]],
    17: [["MIL-C-14409"]],
    18: [["MIL-C-92"]],
    19: [["MIL-C-23183"]],
}
CAPACITOR_STYLE_DICT = {
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
    _dic_quality: Dict[int, object] = CAPACITOR_QUALITY_DICT
    _dic_specifications: Dict[int, List[Any]] = CAPACITOR_SPECIFICATION_DICT
    _dic_styles: Dict[int, List[Any]] = CAPACITOR_STYLE_DICT

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
        self.dic_attribute_widget_map = self._do_initialize_attribute_widget_map()

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.cmbSpecification.connect("changed", self._do_load_styles)

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.do_load_comboboxes,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the capacitor assessment input RAMSTKComboBox()s.

        :param subcategory_id: the subcategory ID of the selected capacitor.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.cmbConfiguration.do_load_combo(
            [
                [_("Fixed")],
                [_("Variable")],
            ],
            signal="changed",
        )
        self.cmbConstruction.do_load_combo(
            [
                [_("Slug, All Tantalum")],
                [_("Foil, Hermetic")],
                [_("Slug, Hermetic")],
                [_("Foil, Non-Hermetic")],
                [_("Slug, Non-Hermetic")],
            ],
            signal="changed",
        )
        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
            signal="changed",
        )
        self.cmbSpecification.do_load_combo(
            self._dic_specifications.get(self.subcategory_id, [[""]]),
            signal="changed",
        )
        self.cmbStyle.do_load_combo(
            [],
            signal="changed",
        )

        self._set_sensitive()

    def _do_initialize_attribute_widget_map(self) -> Dict[str, List[Any]]:
        """Initialize the attribute widget map.

        :return: the attributes dict for the Gtk widgets.
        :rtype: dict
        """
        return {
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

    def _do_load_styles(self, combo: RAMSTKComboBox) -> None:
        """Load the style RAMSTKComboBox() when the specification changes.

        :param combo: the specification RAMSTKCombo() that called this method.
        :return: None
        :rtype: None
        """
        self.cmbStyle.do_load_combo(
            self._get_style_list(combo),
            signal="changed",
        )

    def _get_quality_list(self) -> List[Any]:
        """Return the list of quality levels based on subcategory.

        :return: list of capacitor quality levels.
        :rtype: list
        """
        _default_quality_list = ["S", "R", "P", "M", "L", ["MIL-SPEC"], [_("Lower")]]
        return (
            _default_quality_list
            if self._hazard_rate_method_id == 1
            else self._dic_quality.get(self.subcategory_id, [[""]])
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
            _subcategory_styles = self._dic_styles.get(self.subcategory_id, [])

            if self.subcategory_id in [1, 3, 4, 7, 9, 10, 11, 13]:
                # Get the active index from the combo box
                _active_index = int(combo.get_active()) - 1
                # Select styles based on the active index
                _styles = (
                    _subcategory_styles[_active_index]
                    if 0 <= _active_index < len(_subcategory_styles)
                    else []
                )
            else:
                # Use default styles for the subcategory
                _styles = _subcategory_styles

        except (KeyError, ValueError, IndexError):
            # Handle any errors that occur (e.g., invalid index)
            _styles = []

        return _styles

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
        """Set widget sensitivity as needed for the selected capacitor type.

        :return: None
        :rtype: None
        """
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
        super().set_widget_sensitivity(
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
            super().set_widget_sensitivity([self.cmbSpecification])
        else:
            super().set_widget_sensitivity(_sensitivity_list)
