# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.design_electric.components.semiconductor.py is part of the
#       RAMSTK Project.
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor Input Panel."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.constants.semiconductor import (
    SEMICONDUCTOR_APPLICATION_DICT,
    SEMICONDUCTOR_MATCHING_DICT,
    SEMICONDUCTOR_PACKAGES_LIST,
    SEMICONDUCTOR_QUALITY_DICT,
    SEMICONDUCTOR_TYPE_DICT,
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


class SemiconductorDesignElectricInputPanel(RAMSTKFixedPanel):
    """Display Semiconductor assessment input attribute data.

    The Semiconductor assessment input view displays all the assessment inputs
    for the selected semiconductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Semiconductor assessment input view
    are:

    :ivar cmbApplication: select and display the application of the
        semiconductor.
    :ivar cmbConstruction: select and display the construction of the
        semiconductor.
    :ivar cmbMatching: select and display the matching arrangement for the
        semiconductor.
    :ivar cmbPackage: select and display the type of package for the
        semiconductor.
    :ivar cmbType: select and display the type of semiconductor.
    :ivar txtFrequencyOperating: enter and display the operating frequency of
        the semiconductor.
    :ivar txtNElements: enter and display the number of elements in the
        optoelectronic display.
    :ivar txtThetaJC: enter and display the junction-case thermal resistance.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_design_electric_attributes"
    _tag: str = "design_electric"
    _title: str = _("Semiconductor Design Inputs")

    def __init__(self) -> None:
        """Initialize instance of the Semiconductor assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbMatching: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbPackage: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()
        self.txtFrequencyOperating: RAMSTKEntry = RAMSTKEntry()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()
        self.txtThetaJC: RAMSTKEntry = RAMSTKEntry()

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
                    "tooltip": _("The quality level of the semiconductor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbPackage,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "package_id",
                    "index": 30,
                    "label_text": _("Package:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The package type for the semiconductor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbType,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "type_id",
                    "index": 48,
                    "label_text": _("Type:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The type of semiconductor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbApplication,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "application_id",
                    "index": 2,
                    "label_text": _("Application:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The application of the semiconductor."),
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
                    "tooltip": _("The method of construction of the semiconductor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbMatching,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "matching_id",
                    "index": 6,
                    "label_text": _("Matching Network:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The matching network of the semiconductor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtFrequencyOperating,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "frequency_operating",
                    "index": 2,
                    "label_text": _("Operating Frequency (GHz):"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _("The operating frequency of the semiconductor."),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtNElements,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "n_elements",
                    "index": 25,
                    "label_text": _("Number of Characters:"),
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The number of characters in the optoelectronic display."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtThetaJC,
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "theta_jc",
                    "index": 47,
                    "label_text": "\u03b8<sub>JC</sub>:",
                    "listen_topic": None,
                    "send_topic": "wvw_editing_design_electric",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The junction-case thermal resistance of the semiconductor."
                    ),
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
        super().do_set_widget_callbacks()
        self._do_load_construction()
        self._do_load_package()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "changed_subcategory": self.on_subcategory_change,
                "succeed_get_reliability_attributes": self._set_reliability_attributes,
            }
        )

    def on_subcategory_change(self, subcategory_id: int) -> None:
        """Load the semiconductor RAMSTKComboBoxes with subcategory specific entries.

        :param subcategory_id: the subcategory ID of the selected semiconductor.
        """
        self.subcategory_id = subcategory_id

        self.cmbApplication.do_load_combo(
            SEMICONDUCTOR_APPLICATION_DICT.get(self.subcategory_id, []),
        )
        self.cmbMatching.do_load_combo(
            SEMICONDUCTOR_MATCHING_DICT.get(self.subcategory_id, []),
        )
        self.cmbQuality.do_load_combo(
            self._get_quality_list(),
        )
        self.cmbType.do_load_combo(
            self._get_type_list(),
        )

        self._set_sensitive()

    def _do_load_construction(self) -> None:
        """Load the construction RAMSTKComboBox."""
        self.cmbConstruction.do_load_combo(
            [
                [_("Metallurgically Bonded")],
                [_("Non-Metallurgically Bonded and Spring Loaded Contacts")],
            ],
        )

    def _do_load_package(self) -> None:
        """Load the package RAMSTKComboBox."""
        self.cmbPackage.do_load_combo(
            SEMICONDUCTOR_PACKAGES_LIST,
        )

    def _get_quality_list(self) -> List[List[str]]:
        """Return the list of semiconductor quality levels.

        :return: list of semiconductor quality levels.
        :rtype: list
        """
        if self._hazard_rate_method_id == 1:
            return self._get_part_count_quality_list()
        return SEMICONDUCTOR_QUALITY_DICT.get(self.subcategory_id, [])

    def _get_part_count_quality_list(self) -> List[List[str]]:
        """Return the quality list to load into the quality level RAMSTKComboBox().

        :return: list of semiconductor quality levels.
        :rtype: list
        """
        if self.subcategory_id == 13:
            return [
                [_("Hermetic Package")],
                [_("Nonhermetic with Facet Coating")],
                [_("Nonhermetic without Facet Coating")],
            ]
        else:
            return [
                ["JANTXV"],
                ["JANTX"],
                ["JAN"],
                [_("Lower")],
                [_("Plastic")],
            ]

    def _get_type_list(self) -> List[List[str]]:
        """Return the type list to load into the type RAMSTKComboBox."""
        _default_type_list = [
            [_("Photodetector")],
            [_("Opto-Isolator")],
            [_("Emitter")],
        ]
        return (
            _default_type_list
            if self._hazard_rate_method_id == 1 and self.subcategory_id == 11
            else SEMICONDUCTOR_TYPE_DICT.get(self.subcategory_id, [[""]])
        )

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
        """Set widget sensitivity as needed for the selected semiconductor."""
        # Define all widgets that could be sensitive
        _all_widgets = [
            self.cmbApplication,
            self.cmbConstruction,
            self.cmbMatching,
            self.cmbPackage,
            self.cmbType,
            self.txtFrequencyOperating,
            self.txtNElements,
            self.txtThetaJC,
        ]

        # Reset all widgets to be insensitive.
        super().do_set_widget_sensitivity(
            _all_widgets,
            False,
        )

        # Set cmbPackage and txtThetaJC sensitive if hazard_rate_method_id is 2
        if self._hazard_rate_method_id == 2:
            super().do_set_widget_sensitivity(
                [
                    self.cmbPackage,
                    self.txtThetaJC,
                ],
            )

        # Define a sensitivity map for different widgets based on hazard rate method
        # and subcategory
        _sensitivity_map = {
            1: {
                1: [self.cmbType],
                2: [self.cmbType],
                3: [self.cmbType],
                8: [self.cmbType],
                11: [self.cmbType],
                13: [self.cmbType],
            },
            2: {
                1: [
                    self.cmbConstruction,
                    self.cmbType,
                ],
                2: [
                    self.cmbApplication,
                    self.cmbType,
                ],
                3: [self.cmbApplication],
                4: [
                    self.cmbApplication,
                    self.cmbType,
                ],
                7: [
                    self.cmbApplication,
                    self.cmbMatching,
                    self.cmbType,
                    self.txtNElements,
                    self.txtFrequencyOperating,
                ],
                8: [
                    self.cmbApplication,
                    self.cmbMatching,
                    self.txtNElements,
                    self.txtFrequencyOperating,
                ],
                9: [self.cmbType],
                11: [self.cmbType],
                12: [
                    self.cmbConstruction,
                    self.cmbType,
                ],
                13: [
                    self.cmbApplication,
                    self.cmbType,
                ],
            },
        }

        super().do_set_widget_sensitivity(
            _sensitivity_map.get(self._hazard_rate_method_id, {}).get(
                self.subcategory_id, []
            )
        )
