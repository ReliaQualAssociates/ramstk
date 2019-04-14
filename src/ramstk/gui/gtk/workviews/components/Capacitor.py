# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Capacitor.py is part of the RAMSTK
#       Project.
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                           AssessmentResults)


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
    _dic_quality = {
        1: [["MIL-SPEC"], [_(u"Lower")]],
        2: [["M"], [_(u"Non-Established Reliability")], [_(u"Lower")]],
        3: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-19978 Non-Established Reliability")], [_(u"Lower")]
        ],
        4: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-18312 Non-Established Reliability")], [_(u"Lower")]
        ],
        5: ["S", "R", "P", "M", [_(u"Lower")]],
        6: ["S", "R", "P", "M", [_(u"Lower")]],
        7: [
            "T", "S", "R", "P", "M", "L",
            [_(u"MIL-C-5 Non-Established Reliability, Dipped")],
            [_(u"MIL-C-5 Non-Established Reliability, Molded")], [_(u"Lower")]
        ],
        8: [["MIL-C-10950"], [_(u"Lower")]],
        9: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-11272 Non-Established Reliability")], [_(u"Lower")]
        ],
        10: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-11015 Non-Established Reliability")], [_(u"Lower")]
        ],
        11: [
            "S", "R", "P", "M", [_(u"Non-Established Reliability")],
            [_(u"Lower")]
        ],
        12: ["D", "C", "S", "B", "R", "P", "M", "L", [_(u"Lower")]],
        13: [
            "S", "R", "P", "M", "L",
            [_(u"MIL-C-3965 Non-Established Reliability")], [_(u"Lower")]
        ],
        14: [
            "S", "R", "P", "M", [_(u"Non-Established Reliability")],
            [_(u"Lower")]
        ],
        15: [["MIL-SPEC"], [_(u"Lower")]],
        16: [["MIL-SPEC"], [_(u"Lower")]],
        17: [["MIL-SPEC"], [_(u"Lower")]],
        18: [["MIL-SPEC"], [_(u"Lower")]],
        19: [["MIL-SPEC"], [_(u"Lower")]]
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
        19: [["MIL-C-23183"]]
    }

    _dic_styles = {
        1: [[["CP4"], ["CP5"], ["CP8"], ["CP9"], ["CP10"], ["CP11"], ["CP12"],
             ["CP13"], ["CP25"], ["CP26"], ["CP27"], ["CP28"], ["CP29"],
             ["CP40"], ["CP41"], ["CP67"], ["CP69"], ["CP70"], ["CP72"],
             ["CP75"], ["CP76"], ["CP77"], ["CP78"], ["CP80"], ["CP81"],
             ["CP82"]], [["CA"]]],
        2: [[_(u"Characteristic E")], [_(u"Characteristic K")],
            [_(u"Characteristic P")], [_(u"Characteristic W")]],
        3: [[["CPV07"], ["CPV09"], ["CPV17"]],
            [[_(u"Characteristic E")], [_(u"Characteristic F")],
             [_(u"Characteristic G")], [_(u"Characteristic K")],
             [_(u"Characteristic L")], [_(u"Characteristic M")],
             [_(u"Characteristic P")], [_(u"Characteristic Q")],
             [_(u"Characteristic S")], [_(u"Characteristic T")]]],
        4: [[[_(u"Characteristic N")], [_(u"Characteristic R")]],
            [[_(u"Characteristic 1")], [_(u"Characteristic 9")],
             [_(u"Characteristic 10")], [_(u"Characteristic 12")],
             [_(u"Characteristic 19")], [_(u"Characteristic 29")],
             [_(u"Characteristic 49")], [_(u"Characteristic 59")]]],
        5: [[_(u"Characteristic M")], [_(u"Characteristic N")],
            [_(u"Characteristic Q")], [_(u"Characteristic R")],
            [_(u"Characteristic S")]],
        6: [["CRH"]],
        7: [[[_(u"Temperature Range M")], [_(u"Temperature Range N")],
             [_(u"Temperature Range O")], [_(u"Temperature Range P")]],
            [[_(u"Temperature Range O")], [_(u"Temperature Range P")]]],
        8: [["CB50"], [_(u"Other")]],
        9: [[[_(u"Temperature Range C")], [_(u"Temperature Range D")]],
            [[_(u"All")]]],
        10:
        [[[_(u"Type A Rated Temperature")], [_(u"Type B Rated Temperature")],
          [_(u"Type C Rated Temperature")]],
         [["CKR05"], ["CKR06"], ["CKR07"], ["CKR08"], ["CKR09"], ["CKR10"],
          ["CKR11"], ["CKR12"], ["CKR13"], ["CKR14"], ["CKR15"], ["CKR16"],
          ["CKR17"], ["CKR18"], ["CKR19"], ["CKR48"], ["CKR64"], ["CKR72"],
          ["CKR73"], ["CKR74"]]],
        11: [[["CC5"], ["CC6"], ["CC7"], ["CC8"], ["CC9"], ["CC13"], ["CC14"],
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
              ["CCR79"], ["CCR81"], ["CCR82"], ["CCR83"], ["CCR90"]],
             [["CDR"]]],
        12: [["CSR"]],
        13: [[["CL10"], ["CL13"], ["CL14"], ["CL16"], ["CL17"], ["CL18"],
              ["CL24"], ["CL25"], ["CL26"], ["CL27"], ["CL30"], ["CL31"],
              ["CL32"], ["CL33"], ["CL34"], ["CL35"], ["CL36"], ["CL37"],
              ["CL40"], ["CL41"], ["CL42"], ["CL43"], ["CL46"], ["CL47"],
              ["CL48"], ["CL49"], ["CL50"], ["CL51"], ["CL52"], ["CL53"],
              ["CL54"], ["CL55"], ["CL56"], ["CL64"], ["CL65"], ["CL66"],
              ["CL67"], ["CL70"], ["CL71"], ["CL72"], ["CL73"]], [["CLR"]]],
        14: [[_(u"Style 16")], [_(u"Style 17")], [_(u"Style 71")],
             [_(u"All Others")]],
        15: [["CE"]],
        16: [["CV11"], ["CV14"], ["CV21"], ["CV31"], ["CV32"], ["CV34"],
             ["CV35"], ["CV36"], ["CV40"], ["CV41"]],
        17: [[_(u"Style G")], [_(u"Style H")], [_(u"Style J")],
             [_(u"Style L")], [_(u"Style Q")], [_(u"Style T")]],
        18: [["CT"]],
        19: [["CG20"], ["CG21"], ["CG30"], ["CG31"], ["CG32"], ["CG40"],
             ["CG41"], ["CG42"], ["CG43"], ["CG44"], ["CG50"], ["CG51"],
             ["CG60"], ["CG61"], ["CG62"], ["CG63"], ["CG64"], ["CG65"],
             ["CG66"], ["CG67"]]
    }

    # Define private list attributes.
    _lst_labels = [
        _(u"Quality Level:"),
        _(u"Capacitance (F):"),
        _(u"Specification:"),
        _(u"Style:"),
        _(u"Configuration:"),
        _(u"Construction:"),
        _(u"Equivalent Series Resistance (\u03A9):")
    ]

    def __init__(self, **kwargs):
        """Initialize an instance of the Capacitor assessment input view."""
        AssessmentInputs.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbSpecification = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The governing specification for the capacitor."))
        self.cmbStyle = ramstk.RAMSTKComboBox(
            index=0, simple=False, tooltip=_(u"The style of the capacitor."))
        self.cmbConfiguration = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The configuration of the capacitor."))
        self.cmbConstruction = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the capacitor."))

        self.txtCapacitance = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The capacitance rating (in farads) of the capacitor."))
        self.txtESR = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The equivalent series resistance of the capacitor."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed', self._on_combo_changed,
                                          1))
        self._lst_handler_id.append(
            self.cmbStyle.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbConfiguration.connect('changed', self._on_combo_changed,
                                          3))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtCapacitance.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtESR.connect('changed', self._on_focus_out, 6))

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the specification RKTComboBox().

        This method is used to load the specification RAMSTKComboBox() whenever
        the capacitor subcategory is changed.

        :param int subcategery_id: the ID of the Capacitor sub-subcategory that
                                   is selected.
        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:  # MIL-HDBK-217F parts count.
            _data = ["S", "R", "P", "M", "L", ["MIL-SPEC"], [_(u"Lower")]]
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

        self.cmbConstruction.do_load_combo([[_(u"Slug, All Tantalum")],
                                            [_(u"Foil, Hermetic")],
                                            [_(u"Slug, Hermetic")],
                                            [_(u"Foil, Non-Hermetic")],
                                            [_(u"Slug, Non-Hermetic")]])

        self.cmbConfiguration.do_load_combo([[_(u"Fixed")], [_(u"Variable")]])

        _model = self.cmbStyle.get_model()
        _model.clear()

        return None

    def _do_load_page(self, attributes):
        """
        Load the Capacitor Assessment Inputs page.

        :param dict attributes: the attributes dictionary for the selected
                                Capacitor.
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self._do_load_comboboxes(self._subcategory_id)

        # We don't block the callback signal otherwise the style
        # RAMSTKComboBox() will not be loaded and set.
        self.cmbSpecification.set_active(attributes['specification_id'])

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        if attributes['hazard_rate_method_id'] != 1:
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
                str(self.fmt.format(attributes['capacitance'])))
            self.txtCapacitance.handler_unblock(self._lst_handler_id[5])

            self.txtESR.handler_block(self._lst_handler_id[6])
            self.txtESR.set_text(
                str(self.fmt.format(attributes['resistance'])))
            self.txtESR.handler_unblock(self._lst_handler_id[6])

        self._do_set_sensitive()

        return None

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

        return None

    def _make_page(self):
        """
        Make the Capacitor class gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.txtCapacitance, _x_pos, _y_pos[1])
        self.put(self.cmbSpecification, _x_pos, _y_pos[2])
        self.put(self.cmbStyle, _x_pos, _y_pos[3])
        self.put(self.cmbConfiguration, _x_pos, _y_pos[4])
        self.put(self.cmbConstruction, _x_pos, _y_pos[5])
        self.put(self.txtESR, _x_pos, _y_pos[6])

        # Load the gtk.ComboBox() widgets.
        self._do_load_comboboxes(subcategory_id=self._subcategory_id)

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Capacitor attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

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
        _dic_keys = {
            0: 'quality_id',
            1: 'specification_id',
            2: 'type_id',
            3: 'configuration_id',
            4: 'construction_id',
        }
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        combo.handler_block(self._lst_handler_id[index])

        try:
            _new_text = int(combo.get_active())
        except ValueError:
            _new_text = 0

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

        # Only publish the message if something is selected in the ComboBox.
        if _new_text != -1:
            pub.sendMessage(
                'wvw_editing_hardware',
                module_id=self._hardware_id,
                key=_key,
                value=_new_text)

        combo.handler_unblock(self._lst_handler_id[index])

        return None

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the
                      method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

            +---------+---------------------+---------+---------------------+
            |  Index  | Widget              |  Index  | Widget              |
            +=========+=====================+=========+=====================+
            |    5    | txtCapacitance      |    6    | txtESR              |
            +---------+---------------------+---------+---------------------+

        :return: None
        :rtype: None
        """
        _dic_keys = {5: 'capacitance', 6: 'resistance'}
        try:
            _key = _dic_keys[index]
        except KeyError:
            _key = ''

        entry.handler_block(self._lst_handler_id[index])

        try:
            _new_text = float(entry.get_text())
        except ValueError:
            _new_text = 0.0

        pub.sendMessage(
            'wvw_editing_hardware',
            module_id=self._hardware_id,
            key=_key,
            value=_new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return None


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

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        6:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        10:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        12:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>SR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        13:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        14:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        15:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CV</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        16:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        17:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        18:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        19:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CF</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
    }

    def __init__(self, **kwargs):
        """Initialize an instance of the Capacitor assessment result view."""
        AssessmentResults.__init__(self, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>CV</sub>:")
        self._lst_labels.append(u"\u03C0<sub>CF</sub>:")
        self._lst_labels.append(u"\u03C0<sub>C</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the capacitor failure "
              u"rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiCV = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The capacitance factor for the capacitor."))
        self.txtPiCF = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The configuration factor for the capacitor."))
        self.txtPiC = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The construction factor for the capacitor."))

        self._make_page()
        self.show_all()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def _do_load_page(self, attributes):
        """
        Load the capacitor assessment results page.

        :param str fmt: the format code for displaying floats.
        :param dict attributes: the attributes dictionary for the selected
                                Connection.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        # Display the correct calculation model.
        if self._hazard_rate_method_id == 1:
            self._lblModel.set_markup(
                u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub></span>"
            )
        elif self._hazard_rate_method_id == 2:
            try:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id])
            except KeyError:
                self._lblModel.set_markup("No Model")
        else:
            self._lblModel.set_markup("No Model")

        self.txtPiCV.set_text(str(self.fmt.format(attributes['piCV'])))
        self.txtPiCF.set_text(str(self.fmt.format(attributes['piCF'])))
        self.txtPiC.set_text(str(self.fmt.format(attributes['piC'])))

        self._do_set_sensitive()

        return None

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

        return None

    def _make_page(self):
        """
        Make the capacitor gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiCV, _x_pos, _y_pos[3])
        self.put(self.txtPiCF, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])

        return None
