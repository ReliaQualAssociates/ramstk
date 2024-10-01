# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.inductor.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Inductive Device Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry, RAMSTKFixedPanel

INDUCTOR_INSULATION_DICT = {
    1: [
        [_("Insulation Class A")],
        [_("Insulation Class B")],
        [_("Insulation Class C")],
        [_("Insulation Class O")],
        [_("Insulation Class Q")],
        [_("Insulation Class R")],
        [_("Insulation Class S")],
        [_("Insulation Class T")],
        [_("Insulation Class U")],
        [_("Insulation Class V")],
    ],
    2: [
        [_("Insulation Class A")],
        [_("Insulation Class B")],
        [_("Insulation Class C")],
        [_("Insulation Class F")],
        [_("Insulation Class O")],
    ],
}
INDUCTOR_QUALITY_DICT = {
    1: [["MIL-SPEC"], [_("Lower")]],
    2: [["S"], ["R"], ["P"], ["M"], ["MIL-C-15305"], [_("Lower")]],
}
INDUCTOR_SPECIFICATION_DICT = {
    1: [["MIL-T-27"], ["MIL-T-21038"], ["MIL-T-55631"]],
    2: [["MIL-T-15305"], ["MIL-T-39010"]],
}
PART_COUNT = 1
PART_STRESS = 2


class InductorDesignElectricInputPanel(RAMSTKFixedPanel):
    """Displays Inductor assessment input attribute data.

    The Inductor assessment input view displays all the assessment inputs for
    the selected inductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analysis.  The attributes of an
    Inductor assessment input view are:

    :cvar _dic_insulation: dictionary of insulation classes.  Key is
        inductor subcategory ID; values are lists of insulation classes.
    :cvar dict _dic_specifications: dictionary of inductor MIL-SPECs.  Key is
        inductor subcategory ID; values are lists of specifications.

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.
    :ivar _lst_widgets: the list of widgets to display in the panel.  These
        are listed in the order they should appear on the panel.

    :ivar cmbInsulation: select and display the insulation class of the
        inductor.
    :ivar cmbSpecification: select and display the governing specification for
        the inductor.
    :ivar cmbConstruction: select and display the method of construction of the
        inductor.
    :ivar cmbFamily: select and display the family of the transformer.
    :ivar txtArea: enter and display the heat dissipating area of the inductor.
    :ivar txtWeight: enter and display the weight of the inductor.
    """

    # Define private dict class attributes.
    _dic_insulation: Dict[int, List[List[str]]] = INDUCTOR_INSULATION_DICT
    _dic_quality: Dict[int, List[List[str]]] = INDUCTOR_QUALITY_DICT
    _dic_specifications: Dict[int, List[List[str]]] = INDUCTOR_SPECIFICATION_DICT

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Inductive Device Design Inputs")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Inductor assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbFamily: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbInsulation: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.txtArea: RAMSTKEntry = RAMSTKEntry()
        self.txtWeight: RAMSTKEntry = RAMSTKEntry()

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

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.do_load_comboboxes,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the inductive device assessment input RAMSTKComboBox().

        :param subcategory_id: the subcategory ID of the selected inductive device.
        :return: None
        :rtype: None
        """
        self.subcategory_id = subcategory_id

        self.cmbConstruction.do_load_combo(
            [[_("Fixed")], [_("Variable")]],
            signal="changed",
        )
        self.cmbFamily.do_load_combo(
            self._get_family_list(),
            signal="changed",
        )
        self.cmbInsulation.do_load_combo(
            self._dic_insulation.get(self.subcategory_id, []),
            signal="changed",
        )
        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
            signal="changed",
        )
        self.cmbSpecification.do_load_combo(
            self._dic_specifications.get(self.subcategory_id, []),
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
                    "tooltip": _("The quality level of the inductive device."),
                },
                _("Quality Level:"),
                "gint",
            ],
            "specification_id": [
                36,
                self.cmbSpecification,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "The governing specification for the inductive device."
                    ),
                },
                _("Specification:"),
                "gint",
            ],
            "insulation_id": [
                19,
                self.cmbInsulation,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The insulation class of the inductive device."),
                },
                _("Insulation Class:"),
                "gint",
            ],
            "area": [
                3,
                self.txtArea,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _(
                        "The case radiating surface (in square inches) of the "
                        "inductive device."
                    ),
                },
                _("Area:"),
                "gfloat",
            ],
            "weight": [
                54,
                self.txtWeight,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {
                    "tooltip": _("The transformer weight (in lbf)."),
                },
                _("Weight:"),
                "gfloat",
            ],
            "family_id": [
                15,
                self.cmbFamily,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _("The application family of the transformer."),
                },
                _("Family:"),
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
                    "tooltip": _("The method of construction of the coil."),
                },
                _("Construction:"),
                "gint",
            ],
        }

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Inductor assessment input widgets.

        :param attributes: the attributes dictionary for the selected
        Inductor.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.cmbFamily.do_update(
            attributes["family_id"],
            signal="changed",
        )

        if self._hazard_rate_method_id == PART_STRESS:
            self.cmbSpecification.do_update(
                attributes["specification_id"],
                signal="changed",
            )
            self.cmbInsulation.do_update(
                attributes["insulation_id"],
                signal="changed",
            )
            self.cmbConstruction.do_update(
                attributes["construction_id"],
                signal="changed",
            )
            self.txtArea.do_update(
                str(self.fmt.format(attributes["area"])),
                signal="changed",
            )
            self.txtWeight.do_update(
                str(self.fmt.format(attributes["weight"])),
                signal="changed",
            )

    def _get_family_list(self) -> List[List[str]]:
        """Return the transformer type list to load into the RAMSTKComboBox().

        :return: list of transformer types.
        :rtype: list
        """
        _transformer_types = {
            1: {
                1: [
                    [_("Low Power Pulse Transformer")],
                    [_("Audio Transformer")],
                    [_("High Power Pulse and Power Transformer, Filter")],
                    [_("RF Transformer")],
                ],
                "default": [
                    [_("RF Coils, Fixed or Molded")],
                    [_("RF Coils, Variable")],
                ],
            },
            "default": [
                [_("Pulse Transformer")],
                [_("Audio Transformer")],
                [_("Power Transformer or Filter")],
                [_("RF Transformer")],
            ],
        }

        # Determine the correct data based on the hazard rate method and subcategory.
        _xfmr_type = _transformer_types.get(
            self._hazard_rate_method_id, _transformer_types["default"]
        )
        if isinstance(_xfmr_type, dict):
            _xfmr_type = _xfmr_type.get(self.subcategory_id, _xfmr_type["default"])

        return _xfmr_type

    def _get_quality_list(self) -> List[List[str]]:
        """Return the quality data to load into the RAMSTKComboBox().

        :return: list of inductor quality levels.
        :rtype: list
        """
        _default_quality_list = [
            [_("Established Reliability")],
            ["MIL-SPEC"],
            [_("Lower")],
        ]
        return (
            _default_quality_list
            if self._hazard_rate_method_id == 1
            else self._dic_quality.get(self.subcategory_id, [[""]])
        )

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
        """Set widget sensitivity as needed for the selected inductor.

        :return: None
        :rtype: None
        """
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbSpecification,
            self.cmbInsulation,
            self.cmbFamily,
            self.cmbConstruction,
            self.txtArea,
            self.txtWeight,
        ]

        # Reset all widgets to be insensitive.
        super().set_widget_sensitivity(
            _all_widgets,
            False,
        )

        # Define default sensitivity list
        _default_sensitivity_list = [
            self.cmbSpecification,
            self.cmbInsulation,
            self.txtArea,
            self.txtWeight,
        ]
        # Define sensitivity map for each subcategory
        _sensitivity_map = {
            1: _default_sensitivity_list + [self.cmbFamily],
            2: _default_sensitivity_list + [self.cmbConstruction],
        }

        # Determine sensitivity list based on subcategory
        _sensitivity_list = _sensitivity_map.get(
            self.subcategory_id, _default_sensitivity_list
        )

        # Set widget sensitivity based on hazard rate method
        if self._hazard_rate_method_id == PART_COUNT:
            super().set_widget_sensitivity([self.cmbFamily])
        else:
            super().set_widget_sensitivity(_sensitivity_list)
