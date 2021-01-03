# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.components.resistor.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Work View."""

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
    """Display Resistor assessment input attribute data.

    The Resistor assessment input view displays all the assessment inputs for
    the selected resistor.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Resistor assessment input view are:

    :cvar dict _dic_specifications: dictionary of resistor MIL-SPECs.  Key is
        resistor subcategory ID; values are lists of specifications.
    :cvar dict _dic_styles: dictionary of resistor styles defined in the
        MIL-SPECs.  Key is resistor subcategory ID; values are lists of styles.

    :ivar cmbSpecification: select and display the governing specification of
        the resistor.
    :ivar cmbType: select and display the type of thermistor.
    :ivar cmbConstruction: select and display the method of construction of the
        resistor.
    :ivar txtResistance: enter and display the resistance of the resistor.
    :ivar txtNElements: enter and display the number of active resistors in a
        resistor network or the number of potentiometers taps.
    """

    # Define private dict class attributes.
    _dic_quality: Dict[int, List[List[str]]] = {
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-R-11"], [_("Lower")]],
        2: [["S"], ["R"], ["P"], ["M"], ["MIL-R-10509"], ["MIL-R-22684"],
            [_("Lower")]],
        3: [["MIL-SPEC"], [_("Lower")]],
        4: [["MIL-SPEC"], [_("Lower")]],
        5: [["S"], ["R"], ["P"], ["M"], ["MIL-R-93"], [_("Lower")]],
        6: [["S"], ["R"], ["P"], ["M"], ["MIL-R-26"], [_("Lower")]],
        7: [["S"], ["R"], ["P"], ["M"], ["MIL-R-18546"], [_("Lower")]],
        8: [["MIL-SPEC"], [_("Lower")]],
        9: [["S"], ["R"], ["P"], ["M"], ["MIL-R-27208"], [_("Lower")]],
        10: [["MIL-SPEC"], [_("Lower")]],
        11: [["MIL-SPEC"], [_("Lower")]],
        12: [["MIL-SPEC"], [_("Lower")]],
        13: [["S"], ["R"], ["P"], ["M"], ["MIL-R-22097"], [_("Lower")]],
        14: [["MIL-SPEC"], [_("Lower")]],
        15: [["MIL-SPEC"], [_("Lower")]]
    }
    # Key is subcategory ID; index is specification ID.
    _dic_specifications: Dict[int, List[List[str]]] = {
        2: [["MIL-R-10509"], ["MIL-R-22684"], ["MIL-R-39017"],
            ["MIL-R-55182"]],
        6: [["MIL-R-26"], ["MIL-R-39007"]],
        7: [["MIL-R-18546"], ["MIL-R-39009"]],
        15: [["MIL-R-23285"], ["MIL-R-39023"]]
    }
    # Key is subcategory ID, index is type ID.
    _dic_types: Dict[int, List[List[str]]] = {
        1: [["RCR"], ["RC"]],
        2: [["RLR"], ["RL"], ["RNR"], ["RN"]],
        5: [["RBR"], ["RB"]],
        6: [["RWR"], ["RW"]],
        7: [["RER"], ["RE"]],
        9: [["RTR"], ["RT"]],
        11: [["RA"], ["RK"]],
        13: [["RJR"], ["RJ"]],
        15: [["RO"], ["RVC"]]
    }
    # First key is subcategory ID; second key is specification ID.
    # Index is style ID.
    _dic_styles: Dict[int, Dict[int, List[List[str]]]] = {
        6: {
            1: [["RWR 71"], ["RWR 74"], ["RWR 78"], ["RWR 80"], ["RWR 81"],
                ["RWR 82"], ["RWR 84"], ["RWR 89"]],
            2:
            [["RW 10"], ["RW 11"], ["RW 12"], ["RW 13"], ["RW 14"], ["RW 15"],
             ["RW 16"], ["RW 20"], ["RW 21 "], ["RW 22"], ["RW 23"], ["RW 24"],
             ["RW 29"], ["RW 30"], ["RW 31"], ["RW 32"], ["RW 33"], ["RW 34"],
             ["RW 35"], ["RW 36"], ["RW 37"], ["RW 38"], ["RW 39"], ["RW 47"],
             ["RW 55"], ["RW 56"], ["RW 67"], ["RW 68"], ["RW 69"], ["RW 70"],
             ["RW 74"], ["RW 78"], ["RW 79"], ["RW 80"], ["RW 81"]]
        },
        7: {
            1: [["RE 60/RER 60"], ["RE 65/RER 65"], ["RE 70/RER 70"],
                ["RE 75/RER 75"], ["RE 77"], ["RE 80"]],
            2: [["RE 60/RER40"], ["RE 65/RER 45"], ["RE 70/ RER 50"],
                ["RE 75/RER 55"], ["RE 77"], ["RE 80"]]
        }
    }
    # Key is subcategory ID; index is construction ID.
    _dic_construction: Dict[int, List[List[str]]] = {
        10: [["RR0900A2A9J103"], ["RR0900A3A9J103"], ["RR0900A4A9J103"],
             ["RR0900A5A9J103"]],
        12: [[_("Enclosed")], [_("Unenclosed")]]
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Resistor assessment input view."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['quality_id', 'integer'],
            1: ['specification_id', 'integer'],
            2: ['type_id', 'integer'],
            3: ['family_id', 'integer'],
            4: ['construction_id', 'integer'],
            5: ['resistance', 'float'],
            6: ['n_elements', 'integer'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            _("Quality Level:"),
            _("Resistance (\u03A9):"),
            _("Specification:"),
            _("Type:"),
            _("Style:"),
            _("Construction:"),
            _("Number of Elements:"),
        ]
        self._lst_tooltips: List[str] = [
            _('The quality level of the resistor.'),
            _("The resistance (in \u03A9) of the resistor."),
            _("The governing specification for the resistor."),
            _("The type of thermistor."),
            _("The style of resistor."),
            _("The method of construction of the resistor."),
            _("The number of active resistors in a resistor network or the "
              "number of potentiometer taps."),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbConstruction: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSpecification: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbStyle: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbType: RAMSTKComboBox = RAMSTKComboBox()

        self.txtNElements: RAMSTKEntry = RAMSTKEntry()
        self.txtResistance: RAMSTKEntry = RAMSTKEntry()

        self._dic_attribute_updater = {
            'construction_id': [self.cmbConstruction.do_update, 'changed', 0],
            'family_id': [self.cmbStyle.do_update, 'changed', 1],
            'n_elements': [self.txtNElements.do_update, 'changed', 2],
            'quality_id': [self.cmbQuality.do_update, 'changed', 3],
            'resistance': [self.txtResistance.do_update, 'changed', 4],
            'specification_id':
            [self.cmbSpecification.do_update, 'changed', 5],
            'type_id': [self.cmbType.do_update, 'changed', 6],
        }
        self._lst_widgets = [
            self.cmbQuality,
            self.txtResistance,
            self.cmbSpecification,
            self.cmbType,
            self.cmbStyle,
            self.cmbConstruction,
            self.txtNElements,
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
        """Load the Resistor RKTComboBox()s.

        :param subcategory_id: the subcategory ID of the selected capacitor.
            This is unused in this method but required because this method is a
            PyPubSub listener.
        :return: None
        :rtype: None
        """
        self.__do_load_quality_combo()
        self.__do_load_specification_combo()
        self.__do_load_type_combo()
        self.__do_load_style_combo()
        self.__do_load_construction_combo()

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Resistor assessment input widgets.

        :param attributes: the attributes dictionary for the selected
            Resistor.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.cmbType.do_update(attributes['type_id'], signal='changed')

        if self._hazard_rate_method_id == 2:  # MIL-HDBK-17F, Part Stress
            self.cmbSpecification.do_update(attributes['specification_id'],
                                            signal='changed')
            self.cmbStyle.do_update(attributes['family_id'], signal='changed')
            self.cmbConstruction.do_update(attributes['construction_id'],
                                           signal='changed')
            self.txtResistance.do_update(str(
                self.fmt.format(attributes['resistance'])),
                                         signal='changed')  # noqa
            self.txtNElements.do_update(str(attributes['n_elements']),
                                        signal='changed')  # noqa

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected resistor.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)

        if self._hazard_rate_method_id == 2:
            self.txtResistance.set_sensitive(True)
        else:
            self.txtResistance.set_sensitive(False)

        self.__do_set_construction_combo_sensitive()
        self.__do_set_elements_entry_sensitive()
        self.__do_set_specification_combo_sensitive()
        self.__do_set_style_combo_sensitive()
        self.__do_set_type_combo_sensitive()

    def __do_load_construction_combo(self) -> None:
        """Load the Resistor construction RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_construction[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data, signal='changed')

    def __do_load_quality_combo(self) -> None:
        """Load the Resistor quality RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            if self._hazard_rate_method_id == 1:
                _quality: List[List[str]] = [["S"], ["R"], ["P"], ["M"],
                                             ["MIL-SPEC"], [_("Lower")]]
            else:
                _quality = self._dic_quality[self._subcategory_id]
        except KeyError:
            _quality = [['']]
        self.cmbQuality.do_load_combo(entries=_quality, signal='changed')

    def __do_load_specification_combo(self) -> None:
        """Load the Resistor specification RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data, signal='changed')

    def __do_load_style_combo(self) -> None:
        """Load the Resistor style RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        _specification_id = int(self.cmbSpecification.get_active())
        try:
            _styles: List[List[str]] = self._dic_styles[
                self._subcategory_id][_specification_id]
        except (KeyError, IndexError):
            _styles = [['']]
        self.cmbStyle.do_load_combo(entries=_styles, signal='changed')

    def __do_load_type_combo(self) -> None:
        """Load the Resistor (thermistor) type RAMSTKComboBox().

        :return: None
        :rtype: None
        """
        try:
            if self._hazard_rate_method_id == 1:
                _types: List[Any] = self._dic_types[self._subcategory_id]
            else:
                _types = [[_("Bead")], [_("Disk")], [_("Rod")]]
        except KeyError:
            _types = []
        self.cmbType.do_load_combo(entries=_types, signal='changed')

    def __do_set_construction_combo_sensitive(self) -> None:
        """Set the Resistor construction RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [10, 12]):
            self.cmbConstruction.set_sensitive(True)
        else:
            self.cmbConstruction.set_sensitive(False)

    def __do_set_elements_entry_sensitive(self) -> None:
        """Set Resistor number of elements RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [4, 9, 10, 11, 12, 13, 14, 15]):
            self.txtNElements.set_sensitive(True)
        else:
            self.txtNElements.set_sensitive(False)

    def __do_set_specification_combo_sensitive(self) -> None:
        """Set the Resistor specification RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [2, 6, 7, 15]):
            self.cmbSpecification.set_sensitive(True)
        else:
            self.cmbSpecification.set_sensitive(False)

    def __do_set_style_combo_sensitive(self) -> None:
        """Set the Resistor style RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [6, 7]):
            self.cmbStyle.set_sensitive(True)
        else:
            self.cmbStyle.set_sensitive(False)

    def __do_set_type_combo_sensitive(self) -> None:
        """Set the Resistor type RAMSTKComboBox() sensitive or not.

        :return: None
        :rtype: None
        """
        self.cmbType.set_sensitive(False)

        if (self._hazard_rate_method_id == 1
                and self._subcategory_id in [1, 2, 5, 6, 7, 9, 11, 13, 15]):
            self.cmbType.set_sensitive(True)
        elif self._hazard_rate_method_id == 2 and self._subcategory_id == 8:
            self.cmbType.set_sensitive(True)

    def __set_callbacks(self) -> None:
        """Set callback methods for Resistor assessment input widgets.

        :return: None
        :rtype: None
        """
        # ----- COMBOBOXES
        self.cmbQuality.dic_handler_id['changed'] = self.cmbQuality.connect(
            'changed', self.on_changed_combo, 0, 'wvw_editing_hardware')
        self.cmbSpecification.dic_handler_id[
            'changed'] = self.cmbSpecification.connect('changed',
                                                       self.on_changed_combo,
                                                       1,
                                                       'wvw_editing_hardware')
        self.cmbType.dic_handler_id['changed'] = self.cmbType.connect(
            'changed', self.on_changed_combo, 2, 'wvw_editing_hardware')
        self.cmbStyle.dic_handler_id['changed'] = self.cmbStyle.connect(
            'changed', self.on_changed_combo, 3, 'wvw_editing_hardware')
        self.cmbConstruction.dic_handler_id[
            'changed'] = self.cmbConstruction.connect('changed',
                                                      self.on_changed_combo, 4,
                                                      'wvw_editing_hardware')

        # ----- ENTRIES
        self.txtResistance.dic_handler_id[
            'changed'] = self.txtResistance.connect('changed',
                                                    self.on_changed_entry, 5,
                                                    'wvw_editing_hardware')
        self.txtNElements.dic_handler_id[
            'changed'] = self.txtNElements.connect('changed',
                                                   self.on_changed_entry, 6,
                                                   'wvw_editing_hardware')

    def __set_properties(self) -> None:
        """Set properties for Resistor assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties()

        # ----- ENTRIES
        self.txtNElements.do_set_properties(tooltip=self._lst_tooltips[6],
                                            width=125)
        self.txtResistance.do_set_properties(tooltip=self._lst_tooltips[1],
                                             width=125)


class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    """Display Resistor assessment results attribute data.

    The Resistor assessment result view displays all the assessment results
    for the selected resistor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a Resistor assessment result view are:

    :ivar txtPiR: displays the resistance factor for the resistor.
    :ivar txtPiT: displays the temperature factor for the resistor.
    :ivar txtPiNR: displays the number of resistors factor for the resistor.
    :ivar txtPiTAPS: displays the potentiometer taps factor for the resistor.
    :ivar txtPiV: displays the voltage factor for the resistor.
    :ivar txtPiC: displays the construction class factor for the resistor.
    """

    # Define private dict class attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q"
        "</sub>\u03C0<sub>E</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        6:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        7:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E"
        "</sub></span>",
        8:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub"
        ">V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        10:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub"
        ">R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub"
        "></span>",
        11:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub"
        ">V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        12:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub"
        ">V</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub"
        "></span>",
        13:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub"
        ">V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        14:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub"
        ">V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        15:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = "
        "\u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub"
        ">V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span> "
    }

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Resistor assessment result view."""
        super().__init__()

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_labels = [
            "",
            "\u03BB<sub>b</sub>:",
            "\u03C0<sub>Q</sub>:",
            "\u03C0<sub>E</sub>:",
            "\u03C0<sub>R</sub>:",
            '\u03C0<sub>T</sub>:',
            '\u03C0<sub>NR</sub>:',
            "\u03C0<sub>TAPS</sub>",
            "\u03C0<sub>V</sub>:",
            "\u03C0<sub>C</sub>:",
        ]
        self._lst_tooltips: List[str] = [
            _("The assessment model used to calculate the resistor hazard "
              "rate."),
            _('The base hazard rate for the resistor.'),
            _('The quality factor for the resistor.'),
            _('The environment factor for the resistor.'),
            _('The resistance factor for the resistor.'),
            _('The temperature factor for the resistor.'),
            _('The number of resistors factor for the resistor network.'),
            _('The potentiometer taps factor for the resistor.'),
            _('The voltage factor for the resistor.'),
            _('The construction class factor for the resistor.'),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiC: RAMSTKEntry = RAMSTKEntry()
        self.txtPiNR: RAMSTKEntry = RAMSTKEntry()
        self.txtPiR: RAMSTKEntry = RAMSTKEntry()
        self.txtPiT: RAMSTKEntry = RAMSTKEntry()
        self.txtPiTAPS: RAMSTKEntry = RAMSTKEntry()
        self.txtPiV: RAMSTKEntry = RAMSTKEntry()

        self._lst_widgets = [
            self.lblModel,
            self.txtLambdaB,
            self.txtPiQ,
            self.txtPiE,
            self.txtPiR,
            self.txtPiT,
            self.txtPiNR,
            self.txtPiTAPS,
            self.txtPiV,
            self.txtPiC,
        ]

        super().do_set_properties()
        super().do_make_panel_fixed()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_panel,
                      'succeed_get_all_hardware_attributes')

    def _do_load_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the Resistor assessment results page.

        :param attributes: the attributes dictionary for the selected
            Resistor.
        :return: None
        :rtype: None
        """
        super().do_load_common(attributes)

        self.txtPiR.do_update(str(self.fmt.format(attributes['piR'])))
        self.txtPiT.do_update(str(self.fmt.format(attributes['piT'])))
        self.txtPiNR.do_update(str(self.fmt.format(attributes['piNR'])))
        self.txtPiTAPS.do_update(str(self.fmt.format(attributes['piTAPS'])))
        self.txtPiV.do_update(str(self.fmt.format(attributes['piV'])))
        self.txtPiC.do_update(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self) -> None:
        """Set widget sensitivity as needed for the selected resistor.

        :return: None
        :rtype: None
        """
        self.txtPiQ.set_sensitive(True)

        self.__do_set_pic_sensitive()
        self.__do_set_pie_sensitive()
        self.__do_set_pir_sensitive()
        self.__do_set_pit_pinr_sensitive()
        self.__do_set_pitaps_piv_sensitive()

    def __do_set_pic_sensitive(self) -> None:
        """Set the Resistor PiC RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [10, 12]):
            self.txtPiC.set_sensitive(True)
        else:
            self.txtPiC.set_sensitive(False)

    def __do_set_pie_sensitive(self) -> None:
        """Set the Resistor PiE RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
        else:
            self.txtPiE.set_sensitive(False)

    def __do_set_pir_sensitive(self) -> None:
        """Set the Resistor PiR RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id != 8:
            self.txtPiR.set_sensitive(True)
        else:
            self.txtPiR.set_sensitive(False)

    def __do_set_pit_pinr_sensitive(self) -> None:
        """Set the Resistor PiT and PiNR RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 2 and self._subcategory_id == 4:
            self.txtPiT.set_sensitive(True)
            self.txtPiNR.set_sensitive(True)
        else:
            self.txtPiT.set_sensitive(False)
            self.txtPiNR.set_sensitive(False)

    def __do_set_pitaps_piv_sensitive(self) -> None:
        """Set the Resistor PiTAPS and PiV RAMSTKEntry() sensitive or not.

        :return: None
        :rtype: None
        """
        if (self._hazard_rate_method_id == 2
                and self._subcategory_id in [9, 10, 11, 12, 13, 14, 15]):
            self.txtPiTAPS.set_sensitive(True)
            self.txtPiV.set_sensitive(True)
        else:
            self.txtPiTAPS.set_sensitive(False)
            self.txtPiV.set_sensitive(False)
