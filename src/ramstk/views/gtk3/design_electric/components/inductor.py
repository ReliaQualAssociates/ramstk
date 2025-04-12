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
from ramstk.constants.inductor import (
    INDUCTOR_INSULATION_DICT,
    INDUCTOR_QUALITY_DICT,
    INDUCTOR_SPECIFICATION_DICT,
)
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    WidgetConfig,
)

PART_COUNT = 1
PART_STRESS = 2


class InductorDesignElectricInputPanel(RAMSTKFixedPanel):
    """Displays Inductor assessment input attribute data.

    The Inductor assessment input view displays all the assessment inputs for
    the selected inductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analysis.  The attributes of an
    Inductor assessment input view are:

    :ivar list _lst_labels: list of label text to display for the capacitor
        MIL-HDBK-217 input parameters.

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

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Inductive Device Design Inputs")

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
                    "tooltip": _("The quality level of the inductive device."),
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
                    "tooltip": _(
                        "The governing specification for the inductive device."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbInsulation,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "insulation_id",
                    "index": 19,
                    "label_text": _("Insulation Class:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The insulation class of the inductive device."),
                    "visible": True,
                },
            },
            {
                "widget": self.txtArea,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "area",
                    "index": 3,
                    "label_text": _("Area:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _(
                        "The case radiating surface (in square inches) of the "
                        "inductive device."
                    ),
                    "visible": True,
                },
            },
            {
                "widget": self.txtWeight,
                "attributes": {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "weight",
                    "index": 54,
                    "label_text": _("Weight:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The transformer weight (in lbf)."),
                    "visible": True,
                },
            },
            {
                "widget": self.cmbFamily,
                "attributes": {
                    "datatype": "gint",
                    "default": 0,
                    "field": "family_id",
                    "index": 15,
                    "label_text": _("Family:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                "properties": {
                    "editable": True,
                    "tooltip": _("The application family of the transformer."),
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
                    "tooltip": _("The method of construction of the coil."),
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
        """Load the inductive device RAMSTKComboBoxes with subcategory specific entries.

        :param subcategory_id: the subcategory ID of the selected inductive device.
        """
        self.subcategory_id = subcategory_id

        self.cmbFamily.do_load_combo(
            self._get_family_list(),
        )
        self.cmbInsulation.do_load_combo(
            INDUCTOR_INSULATION_DICT.get(self.subcategory_id, []),
        )
        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
        )
        self.cmbSpecification.do_load_combo(
            INDUCTOR_SPECIFICATION_DICT.get(self.subcategory_id, []),
        )

        self._set_sensitive()

    def _do_load_construction(self) -> None:
        """Load the construction RAMSTKComboBox."""
        self.cmbConstruction.do_load_combo(
            [[_("Fixed")], [_("Variable")]],
        )

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Inductor assessment input widgets.

        :param attributes: the attributes dictionary for the selected Inductor.
        """
        super().do_load_common(attributes)

        self.cmbFamily.do_update(
            {"family_id": attributes["family_id"]},
        )

        if self._hazard_rate_method_id == PART_STRESS:
            self.cmbSpecification.do_update(
                {"specification_id": attributes["specification_id"]},
            )
            self.cmbInsulation.do_update(
                {"insulation_id": attributes["insulation_id"]},
            )
            self.cmbConstruction.do_update(
                {"construction_id": attributes["construction_id"]},
            )
            self.txtArea.do_update(
                {"area": str(self.fmt.format(attributes["area"]))},
            )
            self.txtWeight.do_update(
                {"weight": str(self.fmt.format(attributes["weight"]))},
            )

    def _get_family_list(self) -> List[List[str]]:
        """Return the transformer family list to load into the RAMSTKComboBox.

        :return: list of transformer families.
        :rtype: list
        """
        if self._hazard_rate_method_id == PART_STRESS:
            return [
                [_("Pulse Transformer")],
                [_("Audio Transformer")],
                [_("Power Transformer or Filter")],
                [_("RF Transformer")],
            ]

        if self._subcategory_id == 1:
            return [
                [_("Low Power Pulse Transformer")],
                [_("Audio Transformer")],
                [_("High Power Pulse and Power Transformer, Filter")],
                [_("RF Transformer")],
            ]
        else:
            return [
                [_("RF Coils, Fixed or Molded")],
                [_("RF Coils, Variable")],
            ]

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
            else INDUCTOR_QUALITY_DICT.get(self.subcategory_id, [[""]])
        )

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
        """Set widget sensitivity as needed for the selected inductor."""
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
        super().do_set_widget_sensitivity(
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
            super().do_set_widget_sensitivity([self.cmbFamily])
        else:
            super().do_set_widget_sensitivity(_sensitivity_list)
