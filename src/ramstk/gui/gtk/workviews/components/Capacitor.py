# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Capacitor.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKComboBox, RAMSTKEntry
from ramstk.gui.gtk.ramstk.Widget import _

# RAMSTK Local Imports
from .Component import AssessmentInputs, AssessmentResults


class CapacitorAssessmentInputs(AssessmentInputs):
    """
    Display Capacitor assessment input attribute data in the RAMSTK Work Book.

    The Capacitor assessment input view displays all the assessment inputs for
    the selected capacitor.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analyses.  The attributes of a
    Capacitor assessment input view are:

    :cvar dict _dic_quality: dictionary of MIL-HDBK-217 capacitor quality
                             levels.  Key is capacitor subcategory ID; values
                             are lists of quality levels.
    :cvar dict _dic_specifications: dictionary of capacitor MIL-SPECs.  Key is
                                    capacitor subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of capacitor styles defined in the
                            MIL-SPECs.  Key is capacitor subcategory ID; values
                            are lists of styles.
    :cvar list _lst_labels: list of label text to display for the capacitor
                            MIL-HDBK-217 input parameters.

    :ivar cmbSpecification: select and display the governing specification of
                            the capacitor.
    :ivar cmbStyle: select and display the style of the capacitor.
    :ivar cmbConfiguration: select and display the configuration of the
                            capacitor.
    :ivar cmbConstruction: select and display the method of construction of the
                           capacitor.
    :ivar txtCapacitance: enter and display the capacitance rating of the
                          capacitor.
    :ivar txtESR: enter and display the equivalent series resistance.

    Callbacks signals in RAMSTKBaseView._lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   1   | cmbSpecification - `changed`              |
    +-------+-------------------------------------------+
    |   2   | cmbStyle - `changed`                      |
    +-------+-------------------------------------------+
    |   3   | cmbConfiguration - `changed`              |
    +-------+-------------------------------------------+
    |   4   | cmbConstruction - `changed`               |
    +-------+-------------------------------------------+
    |   5   | txtCapacitance - `changed`                |
    +-------+-------------------------------------------+
    |   6   | txtESR - `changed`                        |
    +-------+-------------------------------------------+
    """

    # Define private dict attributes.
    _dic_keys = {
        0: 'quality_id',
        1: 'specification_id',
        2: 'type_id',
        3: 'configuration_id',
        4: 'construction_id',
        5: 'capacitance',
        6: 'resistance',
    }

    _dic_quality = {
        1: [["MIL-SPEC"], [_("Lower")]],
        2: [["M"], [_("Non-Established Reliability")], [_("Lower")]],
        3: [
            "S", "R", "P", "M", "L",
            [_("MIL-C-19978 Non-Established Reliability")], [_("Lower")],
        ],
        4: [
            "S", "R", "P", "M", "L",
            [_("MIL-C-18312 Non-Established Reliability")], [_("Lower")],
        ],
        5: ["S", "R", "P", "M", [_("Lower")]],
        6: ["S", "R", "P", "M", [_("Lower")]],
        7: [
            "T", "S", "R", "P", "M", "L",
            [_("MIL-C-5 Non-Established Reliability, Dipped")],
            [_("MIL-C-5 Non-Established Reliability, Molded")], [_("Lower")],
        ],
        8: [["MIL-C-10950"], [_("Lower")]],
        9: [
            "S", "R", "P", "M", "L",
            [_("MIL-C-11272 Non-Established Reliability")], [_("Lower")],
        ],
        10: [
            "S", "R", "P", "M", "L",
            [_("MIL-C-11015 Non-Established Reliability")], [_("Lower")],
        ],
        11: [
            "S", "R", "P", "M", [_("Non-Established Reliability")],
            [_("Lower")],
        ],
        12: ["D", "C", "S", "B", "R", "P", "M", "L", [_("Lower")]],
        13: [
            "S", "R", "P", "M", "L",
            [_("MIL-C-3965 Non-Established Reliability")], [_("Lower")],
        ],
        14: [
            "S", "R", "P", "M", [_("Non-Established Reliability")],
            [_("Lower")],
        ],
        15: [["MIL-SPEC"], [_("Lower")]],
        16: [["MIL-SPEC"], [_("Lower")]],
        17: [["MIL-SPEC"], [_("Lower")]],
        18: [["MIL-SPEC"], [_("Lower")]],
        19: [["MIL-SPEC"], [_("Lower")]],
    }

    _dic_specifications = {
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

    _dic_styles = {
        1: [
            [
                ["CP4"], ["CP5"], ["CP8"], ["CP9"], ["CP10"], ["CP11"], ["CP12"],
                ["CP13"], ["CP25"], ["CP26"], ["CP27"], ["CP28"], ["CP29"],
                ["CP40"], ["CP41"], ["CP67"], ["CP69"], ["CP70"], ["CP72"],
                ["CP75"], ["CP76"], ["CP77"], ["CP78"], ["CP80"], ["CP81"],
                ["CP82"],
            ], [["CA"]],
        ],
        2: [
            [_("Characteristic E")], [_("Characteristic K")],
            [_("Characteristic P")], [_("Characteristic W")],
        ],
        3: [
            [["CPV07"], ["CPV09"], ["CPV17"]],
            [
                [_("Characteristic E")], [_("Characteristic F")],
                [_("Characteristic G")], [_("Characteristic K")],
                [_("Characteristic L")], [_("Characteristic M")],
                [_("Characteristic P")], [_("Characteristic Q")],
                [_("Characteristic S")], [_("Characteristic T")],
            ],
        ],
        4: [
            [[_("Characteristic N")], [_("Characteristic R")]],
            [
                [_("Characteristic 1")], [_("Characteristic 9")],
                [_("Characteristic 10")], [_("Characteristic 12")],
                [_("Characteristic 19")], [_("Characteristic 29")],
                [_("Characteristic 49")], [_("Characteristic 59")],
            ],
        ],
        5: [
            [_("Characteristic M")], [_("Characteristic N")],
            [_("Characteristic Q")], [_("Characteristic R")],
            [_("Characteristic S")],
        ],
        6: [["CRH"]],
        7: [
            [
                [_("Temperature Range M")], [_("Temperature Range N")],
                [_("Temperature Range O")], [_("Temperature Range P")],
            ],
            [[_("Temperature Range O")], [_("Temperature Range P")]],
        ],
        8: [["CB50"], [_("Other")]],
        9: [
            [[_("Temperature Range C")], [_("Temperature Range D")]],
            [[_("All")]],
        ],
        10:
        [
            [
                [_("Type A Rated Temperature")], [_("Type B Rated Temperature")],
                [_("Type C Rated Temperature")],
            ],
            [
                ["CKR05"], ["CKR06"], ["CKR07"], ["CKR08"], ["CKR09"], ["CKR10"],
                ["CKR11"], ["CKR12"], ["CKR13"], ["CKR14"], ["CKR15"], ["CKR16"],
                ["CKR17"], ["CKR18"], ["CKR19"], ["CKR48"], ["CKR64"], ["CKR72"],
                ["CKR73"], ["CKR74"],
            ],
        ],
        11: [
            [
                ["CC5"], ["CC6"], ["CC7"], ["CC8"], ["CC9"], ["CC13"], ["CC14"],
                ["CC15"], ["CC16"], ["CC17"], ["CC18"], ["CC19"], ["CC20"],
                ["CC21"], ["CC22"], ["CC25"], ["CC26"], ["CC27"], ["CC30"],
                ["CC31"], ["CC32"], ["CC33"], ["CC35"], ["CC36"], ["CC37"],
                ["CC45"], ["CC47"], ["CC50"], ["CC51"], ["CC52"], ["CC53"],
                ["CC54"], ["CC55"], ["CC56"], ["CC57"], ["CC75"], ["CC76"],
                ["CC77"], ["CC78"], ["CC79"], ["CC81"], ["CC82"], ["CC83"],
                ["CC85"], ["CC95"], ["CC96"], ["CC97"], ["CCR05"], ["CCR06"],
                ["CCR07"], ["CCR08"], ["CCR09"], ["CCR13"], ["CCR14"], ["CCR15"],
                ["CCR16"], ["CCR17"], ["CCR18"], ["CCR19"], ["CCR54"], ["CCR55"],
                ["CCR56"], ["CCR57"], ["CCR75"], ["CCR76"], ["CCR77"], ["CCR78"],
                ["CCR79"], ["CCR81"], ["CCR82"], ["CCR83"], ["CCR90"],
            ],
            [["CDR"]],
        ],
        12: [["CSR"]],
        13: [
            [
                ["CL10"], ["CL13"], ["CL14"], ["CL16"], ["CL17"], ["CL18"],
                ["CL24"], ["CL25"], ["CL26"], ["CL27"], ["CL30"], ["CL31"],
                ["CL32"], ["CL33"], ["CL34"], ["CL35"], ["CL36"], ["CL37"],
                ["CL40"], ["CL41"], ["CL42"], ["CL43"], ["CL46"], ["CL47"],
                ["CL48"], ["CL49"], ["CL50"], ["CL51"], ["CL52"], ["CL53"],
                ["CL54"], ["CL55"], ["CL56"], ["CL64"], ["CL65"], ["CL66"],
                ["CL67"], ["CL70"], ["CL71"], ["CL72"], ["CL73"],
            ], [["CLR"]],
        ],
        14: [
            [_("Style 16")], [_("Style 17")], [_("Style 71")],
            [_("All Others")],
        ],
        15: [["CE"]],
        16: [
            ["CV11"], ["CV14"], ["CV21"], ["CV31"], ["CV32"], ["CV34"],
            ["CV35"], ["CV36"], ["CV40"], ["CV41"],
        ],
        17: [
            [_("Style G")], [_("Style H")], [_("Style J")],
            [_("Style L")], [_("Style Q")], [_("Style T")],
        ],
        18: [["CT"]],
        19: [
            ["CG20"], ["CG21"], ["CG30"], ["CG31"], ["CG32"], ["CG40"],
            ["CG41"], ["CG42"], ["CG43"], ["CG44"], ["CG50"], ["CG51"],
            ["CG60"], ["CG61"], ["CG62"], ["CG63"], ["CG64"], ["CG65"],
            ["CG66"], ["CG67"],
        ],
    }

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Capacitance (F):"),
        _("Specification:"),
        _("Style:"),
        _("Configuration:"),
        _("Construction:"),
        _("Equivalent Series Resistance (\u03A9):"),
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Capacitor assessment input view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        AssessmentInputs.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbSpecification = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbStyle = RAMSTKComboBox(
            index=0, simple=True,
        )
        self.cmbConfiguration = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbConstruction = RAMSTKComboBox(
            index=0,
            simple=True,
        )

        self.txtCapacitance = RAMSTKEntry()
        self.txtESR = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __make_ui(self):
        """
        Make the Capacitor class Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentInputs.make_ui(self)

        self.put(self.txtCapacitance, _x_pos, _y_pos[1])
        self.put(self.cmbSpecification, _x_pos, _y_pos[2])
        self.put(self.cmbStyle, _x_pos, _y_pos[3])
        self.put(self.cmbConfiguration, _x_pos, _y_pos[4])
        self.put(self.cmbConstruction, _x_pos, _y_pos[5])
        self.put(self.txtESR, _x_pos, _y_pos[6])

    def __set_callbacks(self):
        """
        Set callback methods for Capacitor assessment input widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0),
        )
        self._lst_handler_id.append(
            self.cmbSpecification.connect(
                'changed', self._on_combo_changed,
                1,
            ),
        )
        self._lst_handler_id.append(
            self.cmbStyle.connect('changed', self._on_combo_changed, 2),
        )
        self._lst_handler_id.append(
            self.cmbConfiguration.connect(
                'changed', self._on_combo_changed,
                3,
            ),
        )
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 4),
        )
        self._lst_handler_id.append(
            self.txtCapacitance.connect('changed', self.on_focus_out, 5),
        )
        self._lst_handler_id.append(
            self.txtESR.connect('changed', self.on_focus_out, 6),
        )

    def __set_properties(self):
        """
        Set properties for Capacitor assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbSpecification.do_set_properties(
            tooltip=_("The governing specification for the capacitor."),
        )
        self.cmbStyle.do_set_properties(
            tooltip=_("The style of the capacitor."),
        )
        self.cmbConfiguration.do_set_properties(
            tooltip=_("The configuration of the capacitor."),
        )
        self.cmbConstruction.do_set_properties(
            tooltip=_("The method of construction of the capacitor."),
        )
        self.txtCapacitance.do_set_properties(
            width=125,
            tooltip=_("The capacitance rating (in farads) of the capacitor."),
        )
        self.txtESR.do_set_properties(
            width=125,
            tooltip=_("The equivalent series resistance of the capacitor."),
        )

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the specification RKTComboBox().

        :param int subcategory_id: the newly selected capacitor subcategory ID.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F parts count.
            _data = ["S", "R", "P", "M", "L", ["MIL-SPEC"], [_("Lower")]]
        else:
            try:
                _data = self._dic_quality[subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        try:
            _data = self._dic_specifications[subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        self.cmbConstruction.do_load_combo([
            [_("Slug, All Tantalum")],
            [_("Foil, Hermetic")],
            [_("Slug, Hermetic")],
            [_("Foil, Non-Hermetic")],
            [_("Slug, Non-Hermetic")],
        ])

        self.cmbConfiguration.do_load_combo([[_("Fixed")], [_("Variable")]])

        _model = self.cmbStyle.get_model()
        _model.clear()

    def _do_load_page(self, attributes):
        """
        Load the Capacitor Assessment Inputs page.

        :param dict attributes: the attributes dictionary for the selected
        Capacitor.
        :return: None
        :rtype: None
        """
        AssessmentInputs.do_load_page(self, attributes)

        # We don't block the callback signal otherwise the style
        # RAMSTKComboBox() will not be loaded and set.
        self.cmbSpecification.set_active(attributes['specification_id'])

        if self._hazard_rate_method_id != 1:
            self.cmbStyle.handler_block(self._lst_handler_id[2])
            self.cmbStyle.set_active(attributes['type_id'])
            self.cmbStyle.handler_unblock(self._lst_handler_id[2])

            self.cmbConfiguration.handler_block(self._lst_handler_id[3])
            self.cmbConfiguration.set_active(attributes['configuration_id'])
            self.cmbConfiguration.handler_unblock(self._lst_handler_id[3])

            self.cmbConstruction.handler_block(self._lst_handler_id[4])
            self.cmbConstruction.set_active(attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[4])

            self.txtCapacitance.handler_block(self._lst_handler_id[5])
            self.txtCapacitance.set_text(
                str(self.fmt.format(attributes['capacitance'])),
            )
            self.txtCapacitance.handler_unblock(self._lst_handler_id[5])

            self.txtESR.handler_block(self._lst_handler_id[6])
            self.txtESR.set_text(
                str(self.fmt.format(attributes['resistance'])),
            )
            self.txtESR.handler_unblock(self._lst_handler_id[6])

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected capacitor.

        :return: None
        :rtype: None
        """
        self.cmbQuality.set_sensitive(True)

        if self._hazard_rate_method_id == 1:
            if self._subcategory_id == 1:
                self.cmbSpecification.set_sensitive(True)
            else:
                self.cmbSpecification.set_sensitive(False)
            self.cmbStyle.set_sensitive(False)
            self.cmbConfiguration.set_sensitive(False)
            self.cmbConstruction.set_sensitive(False)
            self.txtCapacitance.set_sensitive(False)
            self.txtESR.set_sensitive(False)
        else:
            self.cmbSpecification.set_sensitive(True)
            self.cmbStyle.set_sensitive(True)
            self.txtCapacitance.set_sensitive(True)

            if self._subcategory_id == 12:
                self.txtESR.set_sensitive(True)
            else:
                self.txtESR.set_sensitive(False)

            if self._subcategory_id == 13:
                self.cmbConstruction.set_sensitive(True)
            else:
                self.cmbConstruction.set_sensitive(False)

            if self._subcategory_id == 19:
                self.cmbConfiguration.set_sensitive(True)
            else:
                self.cmbConfiguration.set_sensitive(False)

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Capacitor attribute.

        This method is called by:

            * Gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    3    | cmbConfiguration |
            +---------+------------------+---------+------------------+
            |    1    | cmbSpecification |    4    | cmbConstruction  |
            +---------+------------------+---------+------------------+
            |    2    | cmbStyle         |         |                  |
            +---------+------------------+---------+------------------+

        :return: None
        :rtype: None
        """
        AssessmentInputs.on_combo_changed(self, combo, index)

        # If the capacitor specification changed, load the capacitor style
        # RAMSTKComboBox().
        if index == 1:
            try:
                if self._subcategory_id in [1, 3, 4, 7, 9, 10, 11, 13]:
                    _index = int(combo.get_active()) - 1
                    _data = self._dic_styles[self._subcategory_id][_index]
                else:
                    _data = self._dic_styles[self._subcategory_id]
            except KeyError:
                _data = []
            self.cmbStyle.do_load_combo(_data)


class CapacitorAssessmentResults(AssessmentResults):
    """
    Display capacitor assessment results attribute data in the RAMSTK Work Book.

    The capacitor assessment result view displays all the assessment results
    for the selected capacitor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.  The
    attributes of a capacitor assessment result view are:

    :cvar dict _dic_part_stress: dictionary of MIL-HDBK-217F part stress
                                 models.  The key is the subcategory ID
                                 attribute of the component.

    :ivar txtPiCV: displays the capacitance factor for the capacitor.
    :ivar txtPiCF: displays the configuration factor for the capacitor.
    :ivar txtPiC: displays the construction factor for the capacitor.
    """

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the Capacitor assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        """
        AssessmentResults.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.
        self._dic_part_stress = {
            1:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            2:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            3:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            4:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            5:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            6:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            7:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            8:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            9:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            10:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            11:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            12:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>SR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            13:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            14:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            15:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            16:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            17:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            18:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
            19:
            "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CF</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        }

        # Initialize private list attributes.
        self._lst_labels.append("\u03C0<sub>CV</sub>:")
        self._lst_labels.append("\u03C0<sub>CF</sub>:")
        self._lst_labels.append("\u03C0<sub>C</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiCV = RAMSTKEntry()
        self.txtPiCF = RAMSTKEntry()
        self.txtPiC = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __make_ui(self):
        """
        Make the capacitor Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_ui(self)

        self.put(self.txtPiCV, _x_pos, _y_pos[3])
        self.put(self.txtPiCF, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])

        self.show_all()

    def __set_properties(self):
        """
        Set properties for Capacitor assessment result widgets.

        :return: None
        :rtype: None
        """
        self._lblModel.set_tooltip_markup(
            _(
                "The assessment model used to calculate the capacitor failure "
                "rate.",
            ),
        )

        self.txtPiCV.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The capacitance factor for the capacitor."),
        )
        self.txtPiCF.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The configuration factor for the capacitor."),
        )
        self.txtPiC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The construction factor for the capacitor."),
        )

    def _do_load_page(self, attributes):
        """
        Load the capacitor assessment results page.

        :param dict attributes: the attributes dictionary for the selected
                                Capacitor.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtPiCV.set_text(str(self.fmt.format(attributes['piCV'])))
        self.txtPiCF.set_text(str(self.fmt.format(attributes['piCF'])))
        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected capacitor.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        if self._hazard_rate_method_id == 1:
            self.txtPiCV.set_sensitive(False)
            self.txtPiCF.set_sensitive(False)
            self.txtPiC.set_sensitive(False)
            self.txtPiE.set_sensitive(False)
        else:
            self.txtPiCV.set_sensitive(True)
            self.txtPiCF.set_sensitive(True)
            self.txtPiC.set_sensitive(True)
            self.txtPiE.set_sensitive(True)
