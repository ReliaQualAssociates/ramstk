# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.semiconductor.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor Work View."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
# noinspection PyPackageRequirements
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKEntry

# RAMSTK Local Imports
from .panels import RAMSTKAssessmentInputPanel, RAMSTKAssessmentResultPanel


class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
    """Display Semiconductor assessment input attribute data.

    The Semiconductor assessment input view displays all the assessment inputs
    for the selected semiconductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Semiconductor assessment input view
    are:

    :cvar dict _dic_applications: dictionary of semiconductor applications.
        Key is semiconductor subcategory ID; values are lists of applications.
    :cvar dict _dic_matchings: dictionary of network matching types.  Key is
        semiconductor subcategory ID; values are lists of network matching
        types.
    :cvar dict _dic_quality: dictionary of semiconductor quality levels.  Key
        is semiconductor subcategory ID; values are lists of quality levels.
    :cvar dict _dic_types: dictionary of semiconductor types.  Key is the
        semiconductor subcategory ID; values are lists of semiconductor types.

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

    # Define private dict class attributes.
    _dic_quality = {
        1: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
        2: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
        3: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
        4: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
        5: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
        6: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")]],
        7: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")]],
        8: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")]],
        9: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")]],
        10: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
        11: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
        12: [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")], [_("Plastic")]],
        13: [[_("Hermetic Package")], [_("Nonhermetic with Facet Coating")],
             [_("Nonhermetic without Facet Coating")]]
    }
    # Key is subcategory ID; index is type ID.
    _dic_types = {
        1:
        [[_("General Purpose Analog")], [_("Switching")],
         [_("Power Rectifier, Fast Recovery")],
         [_("Power Rectifier/Schottky Power Diode")],
         [_("Power Rectifier with High Voltage Stacks")],
         [_("Transient Suppressor/Varistor")], [_("Current Regulator")],
         [_("Voltage Regulator and Voltage Reference (Avalanche and Zener)")]],
        2: [
            [_("Si IMPATT (<35 GHz)")],
            [_("Gunn/Bulk Effect")],
            [_("Tunnel and Back (Including Mixers, Detectors)")],
            [_("PIN")],
            [
                _("Schottky Barrier (Including Detectors) and Point Contact "
                  "(200 MHz < Frequency < 35MHz)")
            ],
            [_("Varactor and Step Recovery")],
        ],
        3: [["NPN/PNP (f < 200MHz)"], [_("Power NPN/PNP (f < 200 MHz)")]],
        4: [["MOSFET"], ["JFET"]],
        7: [[_("Gold Metallization")], [_("Aluminum Metallization")]],
        8: [["GaAs FET (P < 100mW)"], ["GaAs FET (P > 100mW)"]],
        9: [["MOSFET"], ["JFET"]],
        11: [[_("Photo-Transistor")], [_("Photo-Diode")],
             [_("Photodiode Output, Single Device")],
             [_("Phototransistor Output, Single Device")],
             [_("Photodarlington Output, Single Device")],
             [_("Light Sensitive Resistor, Single Device")],
             [_("Photodiode Output, Dual Device")],
             [_("Phototransistor Output, Dual Device")],
             [_("Photodarlington Output, Dual Device")],
             [_("Light Sensitive Resistor, Dual Device")],
             [_("Infrared Light Emitting Diode (IRLED)")],
             [_("Light Emitting Diode")]],
        12: [[_("Segment Display")], [_("Diode Array Display")]],
        13: [["GaAs/Al GaAs"], ["In GaAs/In GaAsP"]]
    }
    # Key is subcategory ID; index is application ID.
    _dic_applications = {
        2: [[_("Varactor, Voltage Control")], [_("Varactor, Multiplier")],
            [_("All Other Diodes")]],
        3: [[_("Linear Amplification")], [_("Switching")]],
        4:
        [[_("Linear Amplification")], [_("Small Signal Switching")],
         [_("Non-Linear (2W < Pr < 5W)")], [_("Non-Linear (5W < Pr < 50W)")],
         [_("Non-Linear (50W < Pr < 250W)")], [_("Non-Linear (Pr > 250W)")]],
        7: [["CW"], [_("Pulsed")]],
        8: [[_("All Lower Power and Pulsed")], ["CW"]],
        13: [["CW"], [_("Pulsed")]]
    }
    # Key is subcategory ID; index is matching ID.
    _dic_matchings = {
        7: [[_("Input and Output")], [_("Input Only")], [_("None")]],
        8: [[_("Input and Output")], [_("Input Only")], [_("None")]]
    }

    # Define private list class attributes.
    _lst_packages = [["TO-1"], ["TO-3"], ["TO-5"], ["TO-8"], ["TO-9"],
                     ["TO-12"], ["TO-18"], ["TO-28"], ["TO-33"], ["TO-39"],
                     ["TO-41"], ["TO-44"], ["TO-46"], ["TO-52"], ["TO-53"],
                     ["TO-57"], ["TO-59"], ["TO-60"], ["TO-61"], ["TO-63"],
                     ["TO-66"], ["TO-71"], ["TO-72"], ["TO-83"], ["TO-89"],
                     ["TO-92"], ["TO-94"], ["TO-99"], ["TO-126"], ["TO-127"],
                     ["TO-204"], ["TO-204AA"], ["TO-205AD"], ["TO-205AF"],
                     ["TO-220"], ["DO-4"], ["DO-5"], ["DO-7"], ["DO-8"],
                     ["DO-9"], ["DO-13"], ["DO-14"], ["DO-29"], ["DO-35"],
                     ["DO-41"], ["DO-45"], ["DO-204MB"], ["DO-205AB"],
                     ["PA-42A,B"], ["PD-36C"], ["PD-50"],
                     ["PD-77"], ["PD-180"], ["PD-319"], ["PD-262"], ["PD-975"],
                     ["PD-280"], ["PD-216"], ["PT-2G"], ["PT-2G"], ["PT-6B"],
                     ["PH-13"], ["PH-16"], ["PH-56"], ["PY-58"], ["PY-373"]]

    # Define private list attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize instance of the Semiconductor assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['quality_id', 'integer'],
            1: ['application_id', 'integer'],
            2: ['construction_id', 'integer'],
            3: ['matching_id', 'integer'],
            4: ['family_id', 'integer'],
            5: ['type_id', 'integer'],
            6: ['frequency_operating', 'float'],
            7: ['n_elements', 'integer'],
            8: ['theta_jc', 'float'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _("Quality Level:"),
            _("Package:"),
            _("Type:"),
            _("Application:"),
            _("Construction:"),
            _("Matching Network:"),
            _("Operating Frequency (GHz):"),
            _("Number of Characters:"),
            "\u03B8<sub>JC</sub>:",
        ]
        self._lst_tooltips: List[str] = [
            _("The quality level of the semiconductor."),
            _("The package type for the semiconductor."),
            _("The type of semiconductor."),
            _("The application of the semiconductor."),
            _("The method of construction of the semiconductor."),
            _("The matching network of the semiconductor."),
            _("The operating frequency of the semiconductor."),
            _("The number of characters in the optoelectronic display."),
            _("The junction-case thermal resistance of the semiconductor."),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbApplication: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbMatching: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbPackage: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()

        self.txtFrequencyOperating: RAMSTKEntry = RAMSTKEntry()
        self.txtNElements: RAMSTKEntry = RAMSTKEntry()
        self.txtThetaJC: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'application_id': [self.cmbApplication.do_update, 'changed', 0],
            'construction_id': [self.cmbConstruction.do_update, 'changed', 1],
            'matching_id': [self.cmbMatching.do_update, 'changed', 2],
            'quality_id': [self.cmbQuality.do_update, 'changed', 3],
            'family_id': [self.cmbPackage.do_update, 'changed', 4],
            'type_id': [self.cmbType.do_update, 'changed', 5],
            'frequency_operating':
            [self.txtFrequencyOperating.do_update, 'changed', 6],
            'n_elements': [self.txtNElements.do_update, 'changed', 7],
            'theta_jc': [self.txtThetaJC.do_update, 'changed', 8],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.cmbPackage,
            self.cmbType,
            self.cmbApplication,
            self.cmbConstruction,
            self.cmbMatching,
            self.txtFrequencyOperating,
            self.txtNElements,
            self.txtThetaJC,
        ]

        self.__set_properties()
        super().do_make_panel_fixed()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_load_comboboxes, 'changed_subcategory')

        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_load_comboboxes(self, subcategory_id: int) -> None:
        """Load the Semiconductor RKTComboBox()s.

        :param subcategory_id: the subcategory ID of the selected capacitor.
            This is unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        self.cmbPackage.do_load_combo(self._lst_packages)

        self.__do_load_quality()
        self.__do_load_application()
        self.__do_load_construction()
        self.__do_load_matching()
        self.__do_load_type()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Semiconductor assessment input widgets.

        :param attributes: the attributes dictionary for the selected
            semiconductor.
        :return: None
        """
        super().do_load_common(attributes)

        self.cmbType.do_update(attributes['type_id'], signal='changed')

        if self._hazard_rate_method_id == 2:
            self.cmbApplication.do_update(attributes['application_id'],
                                          signal='changed')
            self.cmbConstruction.do_update(attributes['construction_id'],
                                           signal='changed')
            self.cmbMatching.do_update(attributes['matching_id'],
                                       signal='changed')
            self.cmbPackage.do_update(attributes['package_id'],
                                      signal='changed')
            self.txtFrequencyOperating.do_update(str(
                self.fmt.format(attributes['frequency_operating'])),
                                                 signal='changed')  # noqa
            self.txtNElements.do_update(str(attributes['n_elements']),
                                        signal='changed')
            self.txtThetaJC.do_update(str(
                self.fmt.format(attributes['theta_jc'])),
                                      signal='changed')  # noqa

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected semiconductor.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)
        self.cmbPackage.set_sensitive(False)
        self.txtThetaJC.set_sensitive(False)

        self.__do_set_application_sensitive()
        self.__do_set_construction_sensitive()
        self.__do_set_elements_sensitive()
        self.__do_set_matching_sensitive()
        self.__do_set_op_freq_sensitive()
        self.__do_set_type_sensitive()

        if (self._hazard_rate_method_id == 1
                and self._subcategory_id in [1, 2, 3, 8, 11, 13]):
            self.cmbType.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:
            self.cmbPackage.set_sensitive(True)
            self.txtThetaJC.set_sensitive(True)

    def __do_load_application(self) -> None:
        """Load the application RAMSTKComboBox() with selections.

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_applications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data, signal='changed')

    def __do_load_construction(self) -> None:
        """Load the construction RAMSTKComboBox() with selections.

        :return: None
        :rtype: None
        """
        self.cmbConstruction.do_load_combo(
            [[_("Metallurgically Bonded")],
             [_("Non-Metallurgically Bonded and Spring Loaded Contacts")]],
            signal='changed')

    def __do_load_matching(self) -> None:
        """Load the matching RAMSTKComboBox() with selections.

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_matchings[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbMatching.do_load_combo(_data, signal='changed')

    def __do_load_quality(self) -> None:
        """Load the quality RAMSTKComboBox() with selections.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:
            if self._subcategory_id == 13:
                _data = [[_("Hermetic Package")],
                         [_("Nonhermetic with Facet Coating")],
                         [_("Nonhermetic without Facet Coating")]]
            else:
                _data = [["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")],
                         [_("Plastic")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data, signal='changed')

    def __do_load_type(self) -> None:
        """Load the type RAMSTKComboBox() with selections.

        :return: None
        :rtype: None
        """
        try:
            if (self._hazard_rate_method_id == 1
                    and self._subcategory_id == 11):
                _data = [[_("Photodetector")], [_("Opto-Isolator")],
                         [_("Emitter")]]
            else:
                _data = self._dic_types[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data, signal='changed')

    def __do_set_application_sensitive(self) -> None:
        """Set the application RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [2, 3, 4, 7, 8, 13]):
            self.cmbApplication.set_sensitive(True)
        else:
            self.cmbApplication.set_sensitive(False)

    def __do_set_construction_sensitive(self) -> None:
        """Set the construction RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [1, 12]):
            self.cmbConstruction.set_sensitive(True)
        else:
            self.cmbConstruction.set_sensitive(False)

    def __do_set_elements_sensitive(self) -> None:
        """Set the number of elements RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id in [7, 8]:
            self.txtNElements.set_sensitive(True)
        else:
            self.txtNElements.set_sensitive(False)

    def __do_set_matching_sensitive(self) -> None:
        """Set the matching RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id in [7, 8]:
            self.cmbMatching.set_sensitive(True)
        else:
            self.cmbMatching.set_sensitive(False)

    def __do_set_op_freq_sensitive(self) -> None:
        """Set the operating frequency RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id in [7, 8]:
            self.txtFrequencyOperating.set_sensitive(True)
        else:
            self.txtFrequencyOperating.set_sensitive(False)

    def __do_set_type_sensitive(self) -> None:
        """Set the type RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [1, 2, 4, 7, 9, 11, 12, 13]):
            self.cmbType.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """Set callback methods for Semiconductor assessment input widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self.on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbApplication.dic_handler_id[
            'changed'] = self.cmbApplication.connect('changed',
                                                     self.on_changed_combo, 1,
                                                     'wvw_editing_hardware')
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      self.on_changed_combo, 2,
                                                      'wvw_editing_hardware')
        self.cmbMatching.dic_handler_id['changed'] = self.cmbMatching.connect(
            'changed', self.on_changed_combo, 3, 'wvw_editing_hardware')
        self.cmbPackage.dic_handler_id['changed'] = self.cmbPackage.connect(
            'changed', self.on_changed_combo, 4, 'wvw_editing_hardware')
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed', self.on_changed_combo, 5, 'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtFrequencyOperating.dic_handler_id[
            'changed'] = self.txtFrequencyOperating.connect(
                'changed', self.on_changed_entry, 6, 'wvw_editing_hardware')
        self.txtNElements.dic_handler_id[
            'changed'] = self.txtNElements.connect('changed',
                                                   self.on_changed_entry, 7,
                                                   'wvw_editing_hardware')
        self.txtThetaJC.dic_handler_id['changed'] = self.txtThetaJC.connect(
            'changed', self.on_changed_entry, 8, 'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for Semiconductor assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties()

        # ----- ENTRIES
        self.txtFrequencyOperating.do_set_properties(
            tooltip=self._lst_tooltips[6], width=125)
        self.txtNElements.do_set_properties(tooltip=self._lst_tooltips[7],
                                            width=125)
        self.txtThetaJC.do_set_properties(tooltip=self._lst_tooltips[8],
                                          width=125)


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    """Display semiconductor assessment results attribute data.

    The semiconductor assessment result view displays all the assessment
    results for the selected semiconductor.  This includes, currently, results
    for MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of
    a semiconductor assessment result view are:

    :ivar txtPiT: displays the temperature factor for the semiconductor.
    :ivar txtPiA: displays the application factor for the semiconductor.
    :ivar txtPiC: displays the construction factor for the semiconductor.
    :ivar txtPiI: displays the forward current factor for the semiconductor.
    :ivar txtPiM: displays the matching network factor for the semiconductor.
    :ivar txtPiP: displays the power degradation factor for the semiconductor.
    :ivar txtPiR: displays the power rating factor for the semiconductor.
    :ivar txtPiS: displays the electrical stress factor for the semiconductor.
    """

    # Define private dict class attributes.
    _dic_part_stress: Dict[int, str] = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>S</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R"
        "</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        6:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        10:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S"
        "</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        12:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        13:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>I"
        "</sub>\u03C0<sub>A</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span> "
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize instance of the Semiconductor assessment result view."""
        super().__init__()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            '\u03C0<sub>T</sub>:',
            '\u03C0<sub>A</sub>:',
            '\u03C0<sub>C</sub>:',
            '\u03C0<sub>R</sub>:',
            '\u03C0<sub>M</sub>:',
            '\u03C0<sub>I</sub>:',
            '\u03C0<sub>P</sub>:',
            '\u03C0<sub>S</sub>:',
        ]
        self._lst_tooltips: List[str] = [
            _("The assessment model used to calculate the semiconductor "
              "hazard rate."),
            _('The base hazard rate for the semiconductor.'),
            _('The quality factor for the semiconductor.'),
            _('The environment factor for the semiconductor.'),
            _('The temperature factor for the semiconductor.'),
            _('The application factor for the semiconductor.'),
            _('The contact construction factor for the semiconductor.'),
            _('The power rating factor for the semiconductor.'),
            _('The matching network factor for the semiconductor.'),
            _('The forward current factor for the semiconductor.'),
            _('The quality factor for the semiconductor.'),
            _('The electrical stress factor for the semiconductor.'),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiA: RAMSTKEntry = RAMSTKEntry()
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiI: RAMSTKEntry = RAMSTKEntry()
        self.txtPiM: RAMSTKEntry = RAMSTKEntry()
        self.txtPiP: RAMSTKEntry = RAMSTKEntry()
        self.txtPiR: RAMSTKEntry = RAMSTKEntry()
        self.txtPiS: RAMSTKEntry = RAMSTKEntry()
        self.txtPiT: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtPiT,
            self.txtPiA,
            self.txtPiC,
            self.txtPiR,
            self.txtPiM,
            self.txtPiI,
            self.txtPiP,
            self.txtPiS,
        ]

        super().do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the semiconductor assessment results page.

        :param attributes: the attributes dictionary for the selected
            Semiconductor.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.txtPiA.do_update(str(self.fmt.format(attributes['piA'])))
        self.txtPiC.do_update(str(self.fmt.format(attributes['piC'])))
        self.txtPiI.do_update(str(self.fmt.format(attributes['piI'])))
        self.txtPiM.do_update(str(self.fmt.format(attributes['piM'])))
        self.txtPiP.do_update(str(self.fmt.format(attributes['piP'])))
        self.txtPiR.do_update(str(self.fmt.format(attributes['piR'])))
        self.txtPiS.do_update(str(self.fmt.format(attributes['piS'])))
        self.txtPiT.do_update(str(self.fmt.format(attributes['piT'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected semiconductor.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

        self.__do_set_pi_a_sensitive()
        self.__do_set_pi_c_sensitive()
        self.__do_set_pi_e_sensitive()
        self.__do_set_pi_i_sensitive()
        self.__do_set_pi_m_sensitive()
        self.__do_set_pi_p_sensitive()
        self.__do_set_pi_r_sensitive()
        self.__do_set_pi_s_sensitive()
        self.__do_set_pi_t_sensitive()

    def __do_set_pi_a_sensitive(self) -> None:
        """Set the PiA RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [2, 3, 4, 7, 8, 13]):
            self.txtPiA.set_sensitive(True)
        else:
            self.txtPiA.set_sensitive(False)

    def __do_set_pi_c_sensitive(self) -> None:
        """Set the PiC RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id == 1:
            self.txtPiC.set_sensitive(True)
        else:
            self.txtPiC.set_sensitive(False)

    def __do_set_pi_e_sensitive(self) -> None:
        """Set the PiE RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
        else:
            self.txtPiE.set_sensitive(False)

    def __do_set_pi_i_sensitive(self) -> None:
        """Set the PiI RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id == 13:
            self.txtPiI.set_sensitive(True)
        else:
            self.txtPiI.set_sensitive(False)

    def __do_set_pi_m_sensitive(self) -> None:
        """Set the PiM RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id in [7, 8]:
            self.txtPiM.set_sensitive(True)
        else:
            self.txtPiM.set_sensitive(False)

    def __do_set_pi_p_sensitive(self) -> None:
        """Set the PiP RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id == 13:
            self.txtPiP.set_sensitive(True)
        else:
            self.txtPiP.set_sensitive(False)

    def __do_set_pi_r_sensitive(self) -> None:
        """Set the PiR RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [2, 3, 6, 10]):
            self.txtPiR.set_sensitive(True)
        else:
            self.txtPiR.set_sensitive(False)

    def __do_set_pi_s_sensitive(self) -> None:
        """Set the PiS RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [1, 3, 6, 10]):
            self.txtPiS.set_sensitive(True)
        else:
            self.txtPiS.set_sensitive(False)

    def __do_set_pi_t_sensitive(self) -> None:
        """Set the PiT RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:
            self.txtPiT.set_sensitive(True)
        else:
            self.txtPiT.set_sensitive(False)
