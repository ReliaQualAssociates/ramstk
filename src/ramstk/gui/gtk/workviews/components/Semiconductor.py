# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.Semiconductor.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Semiconductor Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKComboBox, RAMSTKEntry
from ramstk.gui.gtk.ramstk.Widget import _

# RAMSTK Local Imports
from .Component import AssessmentInputs, AssessmentResults


class SemiconductorAssessmentInputs(AssessmentInputs):
    """
    Display Semiconductor assessment input attribute data in RAMSTK Work Book.

    The Semiconductor assessment input view displays all the assessment inputs
    for the selected semiconductor.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Semiconductor assessment input view
    are:

    :cvar dict _dic_applications: dictionary of semiconductor applications.
                                  Key is semiconductor subcategory ID; values
                                  are lists of applications.
    :cvar dict _dic_matchings: dictionary of network matching types.  Key is
                               semiconductor subcategory ID; values are lists
                               of network matching types.
    :cvar dict _dic_quality: dictionary of semiconductor quality levels.  Key
                             is semiconductor subcategory ID; values are lists
                             of quality levels.
    :cvar dict _dic_types: dictionary of semiconductor types.  Key is the
                           semiconductor subcategory ID; values are lists of
                           semiconductor types.

    :ivar cmbApplication: select and display the application of the
                          semiconductor.
    :ivar cmbConstruction: select and display the construction of the
                           semiconductor.
    :ivar cmbMatching: select and display the matching arrangement for the
                       semiconductor.
    :ivar cmbPackage: select and display the type of package for the
                      semiconductor.
    :ivar cmbType: select and display the type of semiconductor.
    :ivar txtFrequencyOperating: enter and display the operating frequencty of
                                 the semiconductor.
    :ivar txtNElements: enter and display the number of elements in the
                        optoelectronic display.
    :ivar txtThetaJC: enter and display the junction-case thermal resistance.

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | cmbQuality - `changed`                    |
    +-------+-------------------------------------------+
    |   1   | cmbApplication - `changed`                |
    +-------+-------------------------------------------+
    |   2   | cmbConstruction - `changed`               |
    +-------+-------------------------------------------+
    |   3   | cmbMatching - `changed`                   |
    +-------+-------------------------------------------+
    |   4   | cmbPackage - `changed`                    |
    +-------+-------------------------------------------+
    |   5   | cmbType - `changed`                       |
    +-------+-------------------------------------------+
    |   6   | txtFrequencyOperating - `changed`         |
    +-------+-------------------------------------------+
    |   7   | txtNElements - `changed`                  |
    +-------+-------------------------------------------+
    |   8   | txtThetaJC - `changed`                    |
    +-------+-------------------------------------------+
    """

    # Define private dict attributes.
    _dic_keys = {
        0: 'quality_id',
        1: 'application_id',
        2: 'construction_id',
        3: 'matching_id',
        4: 'family_id',
        5: 'type_id',
        6: 'frequency_operating',
        7: 'n_elements',
        8: 'theta_jc',
    }

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
        13: [
            [_("Hermetic Package")], [_("Nonhermetic with Facet Coating")],
            [_("Nonhermetic without Facet Coating")],
        ],
    }
    # Key is subcategory ID; index is type ID.
    _dic_types = {
        1:
        [
            [_("General Purpose Analog")], [_("Switching")],
            [_("Power Rectifier, Fast Recovery")],
            [_("Power Rectifier/Schottky Power Diode")],
            [_("Power Rectifier with High Voltage Stacks")],
            [_("Transient Suppressor/Varistor")], [_("Current Regulator")],
            [_("Voltage Regulator and Voltage Reference (Avalanche and Zener)")],
        ],
        2: [
            [_("Si IMPATT (<35 GHz)")], [_("Gunn/Bulk Effect")],
            [_("Tunnel and Back (Including Mixers, Detectors)")], [_("PIN")],
            [
                _(
                    "Schottky Barrier (Including Detectors) and "
                    "Point Contact (200 MHz < Frequency < 35MHz)",
                ),
            ], [_("Varactor and Step Recovery")],
        ],
        3: [["NPN/PNP (f < 200MHz)"], [_("Power NPN/PNP (f < 200 MHz)")]],
        4: [["MOSFET"], ["JFET"]],
        7: [[_("Gold Metallization")], [_("Aluminum Metallization")]],
        8: [["GaAs FET (P < 100mW)"], ["GaAs FET (P > 100mW)"]],
        9: [["MOSFET"], ["JFET"]],
        11: [
            [_("Photo-Transistor")], [_("Photo-Diode")],
            [_("Photodiode Output, Single Device")],
            [_("Phototransistor Output, Single Device")],
            [_("Photodarlington Output, Single Device")],
            [_("Light Sensitive Resistor, Single Device")],
            [_("Photodiode Output, Dual Device")],
            [_("Phototransistor Output, Dual Device")],
            [_("Photodarlington Output, Dual Device")],
            [_("Light Sensitive Resistor, Dual Device")],
            [_("Infrared Light Emitting Diode (IRLED)")],
            [_("Light Emitting Diode")],
        ],
        12: [[_("Segment Display")], [_("Diode Array Display")]],
        13: [["GaAs/Al GaAs"], ["In GaAs/In GaAsP"]],
    }
    # Key is subcategory ID; index is application ID.
    _dic_applications = {
        2: [
            [_("Varactor, Voltage Control")], [_("Varactor, Multiplier")],
            [_("All Other Diodes")],
        ],
        3: [[_("Linear Amplification")], [_("Switching")]],
        4: [
            [_("Linear Amplification")], [_("Small Signal Switching")],
            [_("Non-Linear (2W < Pr < 5W)")],
            [_("Non-Linear (5W < Pr < 50W)")],
            [_("Non-Linear (50W < Pr < 250W)")],
            [_("Non-Linear (Pr > 250W)")],
        ],
        7: [["CW"], [_("Pulsed")]],
        8: [[_("All Lower Power and Pulsed")], ["CW"]],
        13: [["CW"], [_("Pulsed")]],
    }
    # Key is subcategory ID; index is matching ID.
    _dic_matchings = {
        7: [[_("Input and Output")], [_("Input Only")], [_("None")]],
        8: [[_("Input and Output")], [_("Input Only")], [_("None")]],
    }

    # Define private list attributes.
    _lst_packages = [
        ["TO-1"], ["TO-3"], ["TO-5"], ["TO-8"], ["TO-9"],
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
        ["PH-13"], ["PH-16"], ["PH-56"], ["PY-58"], ["PY-373"],
    ]

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Package:"),
        _("Type:"),
        _("Application:"),
        _("Construction:"),
        _("Matching Network:"),
        _("Operating Frequency (GHz):"),
        _("Number of Characters:"), "\u03B8<sub>JC</sub>:",
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize instance of the Semiconductor assessment input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentInputs.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbPackage = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbType = RAMSTKComboBox(
            index=0, simple=True,
        )
        self.cmbApplication = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbConstruction = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbMatching = RAMSTKComboBox(
            index=0,
            simple=True,
        )

        self.txtFrequencyOperating = RAMSTKEntry()
        self.txtNElements = RAMSTKEntry()
        self.txtThetaJC = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __make_ui(self):
        """
        Make the Semiconductor Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_ui(self)

        self.put(self.cmbPackage, _x_pos, _y_pos[1])
        self.put(self.cmbType, _x_pos, _y_pos[2])
        self.put(self.cmbApplication, _x_pos, _y_pos[3])
        self.put(self.cmbConstruction, _x_pos, _y_pos[4])
        self.put(self.cmbMatching, _x_pos, _y_pos[5])
        self.put(self.txtFrequencyOperating, _x_pos, _y_pos[6])
        self.put(self.txtNElements, _x_pos, _y_pos[7])
        self.put(self.txtThetaJC, _x_pos, _y_pos[8])

        self.show_all()

    def __set_callbacks(self):
        """
        Set callback methods for Semiconductor assessment input widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self.on_combo_changed, 0),
        )
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self.on_combo_changed, 1),
        )
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self.on_combo_changed, 2),
        )
        self._lst_handler_id.append(
            self.cmbMatching.connect('changed', self.on_combo_changed, 3),
        )
        self._lst_handler_id.append(
            self.cmbPackage.connect('changed', self.on_combo_changed, 4),
        )
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self.on_combo_changed, 5),
        )
        self._lst_handler_id.append(
            self.txtFrequencyOperating.connect(
                'changed', self.on_focus_out,
                6,
            ),
        )
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self.on_focus_out, 7),
        )
        self._lst_handler_id.append(
            self.txtThetaJC.connect('changed', self.on_focus_out, 8),
        )

    def __set_properties(self):
        """
        Set properties for Semiconductor assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbPackage.do_set_properties(
            tooltip=_("The package type for the semiconductor."),
        )
        self.cmbType.do_set_properties(
            tooltip=_("The type of semiconductor."),
        )
        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the semiconductor."),
        )
        self.cmbConstruction.do_set_properties(
            tooltip=_("The method of construction of the semiconductor."),
        )
        self.cmbMatching.do_set_properties(
            tooltip=_("The matching network of the semiconductor."),
        )

        self.txtFrequencyOperating.do_set_properties(
            width=125,
            tooltip=_("The operating frequency of the semiconductor."),
        )
        self.txtNElements.do_set_properties(
            width=125,
            tooltip=_(
                "The number of characters in the optoelectronic display.",
            ),
        )
        self.txtThetaJC.do_set_properties(
            width=125,
            tooltip=_(
                "The junction-case thermal resistance of the semiconductor.",
            ),
        )

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the Semiconductor RKTComboBox()s.

        This method is used to load the specification RAMSTKComboBox() whenever
        the semiconductor subcategory is changed.

        :param int subcategory_id: the newly selected semiconductor subcategory
                                   ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        if self._hazard_rate_method_id == 1:
            if subcategory_id == 13:
                _data = [
                    [_("Hermetic Package")],
                    [_("Nonhermetic with Facet Coating")],
                    [_("Nonhermetic without Facet Coating")],
                ]
            else:
                _data = [
                    ["JANTXV"], ["JANTX"], ["JAN"], [_("Lower")],
                    [_("Plastic")],
                ]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the application RAMSTKComboBox().
        try:
            _data = self._dic_applications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data)

        # Load the construction RAMSTKComboBox().
        self.cmbConstruction.do_load_combo(
            [
                [_("Metallurgically Bonded")],
                [_("Non-Metallurgically Bonded and Spring Loaded Contacts")],
            ],
        )

        # Load the matching network RAMSTKComboBox().
        try:
            _data = self._dic_matchings[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbMatching.do_load_combo(_data)

        # Load the package RAMSTKComboBox().
        self.cmbPackage.do_load_combo(self._lst_packages)

        # Load the type RAMSTKComboBox().
        try:
            if (self._hazard_rate_method_id == 1 and subcategory_id == 11):
                _data = [
                    [_("Photodetector")], [_("Opto-Isolator")],
                    [_("Emitter")],
                ]
            else:
                _data = self._dic_types[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

    def _do_load_page(self, attributes):
        """
        Load the Semiconductor assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Semiconductor.
        :return: None
        :rtype: None
        """
        AssessmentInputs.do_load_page(self, attributes)

        self.cmbType.handler_block(self._lst_handler_id[5])
        self.cmbType.set_active(attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[5])

        if self._hazard_rate_method_id == 2:
            self.cmbApplication.handler_block(self._lst_handler_id[1])
            self.cmbApplication.set_active(attributes['application_id'])
            self.cmbApplication.handler_unblock(self._lst_handler_id[1])

            self.cmbConstruction.handler_block(self._lst_handler_id[2])
            self.cmbConstruction.set_active(attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[2])

            self.cmbMatching.handler_block(self._lst_handler_id[3])
            self.cmbMatching.set_active(attributes['matching_id'])
            self.cmbMatching.handler_unblock(self._lst_handler_id[3])

            self.cmbPackage.handler_block(self._lst_handler_id[4])
            self.cmbPackage.set_active(attributes['package_id'])
            self.cmbPackage.handler_unblock(self._lst_handler_id[4])

            self.txtFrequencyOperating.handler_block(self._lst_handler_id[6])
            self.txtFrequencyOperating.set_text(
                str(self.fmt.format(attributes['frequency_operating'])),
            )
            self.txtFrequencyOperating.handler_unblock(self._lst_handler_id[6])

            self.txtNElements.handler_block(self._lst_handler_id[7])
            self.txtNElements.set_text(
                str(self.fmt.format(attributes['n_elements'])),
            )
            self.txtNElements.handler_unblock(self._lst_handler_id[7])

            self.txtThetaJC.handler_block(self._lst_handler_id[8])
            self.txtThetaJC.set_text(
                str(self.fmt.format(attributes['theta_jc'])),
            )
            self.txtThetaJC.handler_unblock(self._lst_handler_id[8])

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected semiconductor.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.cmbMatching.set_sensitive(False)
        self.cmbPackage.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtFrequencyOperating.set_sensitive(False)
        self.txtNElements.set_sensitive(False)
        self.txtThetaJC.set_sensitive(False)

        if self._hazard_rate_method_id == 1:
            if self._subcategory_id in [1, 2, 3, 8, 11, 13]:
                self.cmbType.set_sensitive(True)
        elif self._hazard_rate_method_id == 2:
            self.cmbPackage.set_sensitive(True)
            self.txtThetaJC.set_sensitive(True)

            if self._subcategory_id in [2, 3, 4, 7, 8, 13]:
                self.cmbApplication.set_sensitive(True)
            if self._subcategory_id in [1, 12]:
                self.cmbConstruction.set_sensitive(True)
            if self._subcategory_id in [7, 8]:
                self.cmbMatching.set_sensitive(True)
                self.txtFrequencyOperating.set_sensitive(True)
            if self._subcategory_id in [1, 2, 4, 7, 9, 11, 12, 13]:
                self.cmbType.set_sensitive(True)
            if self._subcategory_id == 12:
                self.txtNElements.set_sensitive(True)


class SemiconductorAssessmentResults(AssessmentResults):
    """
    Display semiconductor assessment results attribute data.

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

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        6:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        10:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        12:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        13:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>I</sub>\u03C0<sub>A</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>",
    }

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of Semiconductor assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentResults.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>T</sub>:")
        self._lst_labels.append("\u03C0<sub>A</sub>:")
        self._lst_labels.append("\u03C0<sub>C</sub>:")
        self._lst_labels.append("\u03C0<sub>R</sub>:")
        self._lst_labels.append("\u03C0<sub>M</sub>:")
        self._lst_labels.append("\u03C0<sub>I</sub>:")
        self._lst_labels.append("\u03C0<sub>P</sub>:")
        self._lst_labels.append("\u03C0<sub>S</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(
                "The assessment model used to calculate the semiconductor "
                "failure rate.",
            ),
        )

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiT = RAMSTKEntry()
        self.txtPiA = RAMSTKEntry()
        self.txtPiC = RAMSTKEntry()
        self.txtPiR = RAMSTKEntry()
        self.txtPiM = RAMSTKEntry()
        self.txtPiI = RAMSTKEntry()
        self.txtPiP = RAMSTKEntry()
        self.txtPiS = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __make_ui(self):
        """
        Make the Semiconductor Gtk.Notebook() assessment results page.

        :return: None
        :rtype: NOne
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_ui(self)

        self.put(self.txtPiT, _x_pos, _y_pos[3])
        self.put(self.txtPiA, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])
        self.put(self.txtPiR, _x_pos, _y_pos[6])
        self.put(self.txtPiM, _x_pos, _y_pos[7])
        self.put(self.txtPiI, _x_pos, _y_pos[8])
        self.put(self.txtPiP, _x_pos, _y_pos[9])
        self.put(self.txtPiS, _x_pos, _y_pos[10])

        self.show_all()

    def __set_properties(self):
        """
        Set properties for Semiconductor assessment result widgets.

        :return: None
        :rtype: None
        """
        self.txtPiT.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The temperature factor for the semiconductor."),
        )
        self.txtPiA.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The application factor for the semiconductor."),
        )
        self.txtPiC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The construction factor for the semiconductor."),
        )
        self.txtPiR.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The power rating factor for the semiconductor."),
        )
        self.txtPiM.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The matching network factor for the semiconductor."),
        )
        self.txtPiI.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The forward current factor for the semiconductor."),
        )
        self.txtPiP.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The power degradation factor for the semiconductor."),
        )
        self.txtPiS.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The electrical stress factor for the semiconductor."),
        )

    def _do_load_page(self, attributes):
        """
        Load the semiconductor assessment results page.

        :param dict attributes: the attributes dictionary for the selected
                                Semiconductor.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiT.set_text(str(self.fmt.format(attributes['piT'])))
        self.txtPiA.set_text(str(self.fmt.format(attributes['piA'])))
        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))
        self.txtPiR.set_text(str(self.fmt.format(attributes['piR'])))
        self.txtPiM.set_text(str(self.fmt.format(attributes['piM'])))
        self.txtPiI.set_text(str(self.fmt.format(attributes['piI'])))
        self.txtPiP.set_text(str(self.fmt.format(attributes['piP'])))
        self.txtPiS.set_text(str(self.fmt.format(attributes['piS'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected semiconductor.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        self.txtPiT.set_sensitive(False)
        self.txtPiA.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiR.set_sensitive(False)
        self.txtPiM.set_sensitive(False)
        self.txtPiI.set_sensitive(False)
        self.txtPiP.set_sensitive(False)
        self.txtPiS.set_sensitive(False)

        if self._hazard_rate_method_id == 2:
            self.txtPiE.set_sensitive(True)
            self.txtPiT.set_sensitive(True)
            if self._subcategory_id == 1:
                self.txtPiC.set_sensitive(True)
            if self._subcategory_id == 13:
                self.txtPiI.set_sensitive(True)
                self.txtPiP.set_sensitive(True)
            if self._subcategory_id in [2, 3, 4, 7, 8, 13]:
                self.txtPiA.set_sensitive(True)
            if self._subcategory_id in [7, 8]:
                self.txtPiM.set_sensitive(True)
            if self._subcategory_id in [2, 3, 6, 10]:
                self.txtPiR.set_sensitive(True)
            if self._subcategory_id in [1, 3, 6, 10]:
                self.txtPiS.set_sensitive(True)
