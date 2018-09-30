# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.components.Resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor Work View."""

from pubsub import pub

# Import other RAMSTK modules.
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import _
from ramstk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class ResistorAssessmentInputs(AssessmentInputs):
    """
    Display Resistor assessment input attribute data in the RAMSTK Work Book.

    The Resistor assessment input view displays all the assessment inputs for
    the selected resistor.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Resistor assessment input view are:

    :cvar dict _dic_specifications: dictionary of resistor MIL-SPECs.  Key is
                                    resistor subcategory ID; values are lists
                                    of specifications.
    :cvar dict _dic_styles: dictionary of resistor styles defined in the
                            MIL-SPECs.  Key is resistor subcategory ID; values
                            are lists of styles.

    :ivar cmbSpecification: select and display the governing specification of
                            the resistor.
    :ivar cmbType: select and display the type of thermistor.
    :ivar cmbConstruction: select and display the method of construction of the
                           resistor.
    :ivar txtResistance: enter and display the resistance of the resistor.
    :ivar txtNElements: enter and display the number of active resistors in a
                        resistor network or the number of potentiometers taps.

    Callbacks signals in _lst_handler_id:

    +-------+------------------------------+
    | Index | Widget - Signal              |
    +=======+==============================+
    |   0   | cmbQuality - `changed`       |
    +-------+------------------------------+
    |   1   | cmbSpecification - `changed` |
    +-------+------------------------------+
    |   2   | cmbType - `changed`          |
    +-------+------------------------------+
    |   3   | cmbStyle - `changed`         |
    +-------+------------------------------+
    |   4   | cmbConstruction - `changed`  |
    +-------+------------------------------+
    |   5   | txtResistance - `changed`    |
    +-------+------------------------------+
    |   6   | txtNElements - `changed`     |
    +-------+------------------------------+
    """

    # Define private dict attributes.
    _dic_quality = {
        1: [["S"], ["R"], ["P"], ["M"], ["MIL-R-11"], [_(u"Lower")]],
        2: [["S"], ["R"], ["P"], ["M"], ["MIL-R-10509"], ["MIL-R-22684"],
            [_(u"Lower")]],
        3: [["MIL-SPEC"], [_(u"Lower")]],
        4: [["MIL-SPEC"], [_(u"Lower")]],
        5: [["S"], ["R"], ["P"], ["M"], ["MIL-R-93"], [_(u"Lower")]],
        6: [["S"], ["R"], ["P"], ["M"], ["MIL-R-26"], [_(u"Lower")]],
        7: [["S"], ["R"], ["P"], ["M"], ["MIL-R-18546"], [_(u"Lower")]],
        8: [["MIL-SPEC"], [_(u"Lower")]],
        9: [["S"], ["R"], ["P"], ["M"], ["MIL-R-27208"], [_(u"Lower")]],
        10: [["MIL-SPEC"], [_(u"Lower")]],
        11: [["MIL-SPEC"], [_(u"Lower")]],
        12: [["MIL-SPEC"], [_(u"Lower")]],
        13: [["S"], ["R"], ["P"], ["M"], ["MIL-R-22097"], [_(u"Lower")]],
        14: [["MIL-SPEC"], [_(u"Lower")]],
        15: [["MIL-SPEC"], [_(u"Lower")]]
    }
    # Key is subcategory ID; index is specification ID.
    _dic_specifications = {
        2: [["MIL-R-10509"], ["MIL-R-22684"], ["MIL-R-39017"],
            ["MIL-R-55182"]],
        6: [["MIL-R-26"], ["MIL-R-39007"]],
        7: [["MIL-R-18546"], ["MIL-R-39009"]],
        15: [["MIL-R-23285"], ["MIL-R-39023"]]
    }
    # Key is subcategory ID, index is type ID.
    _dic_types = {
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
    _dic_styles = {
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
    _dic_construction = {
        10: ["2", "3", "4", "5"],
        12: [[_(u"Enclosed")], [_(u"Unenclosed")]]
    }

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Resistor assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`ramstk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentInputs.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Resistance (\u03A9):"))
        self._lst_labels.append(_(u"Specification:"))
        self._lst_labels.append(_(u"Type:"))
        self._lst_labels.append(_(u"Style:"))
        self._lst_labels.append(_(u"Construction:"))
        self._lst_labels.append(_(u"Number of Elements:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbSpecification = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The governing specification for the resistor."))
        self.cmbType = ramstk.RAMSTKComboBox(
            index=0, simple=False, tooltip=_(u"The type of thermistor."))
        self.cmbStyle = ramstk.RAMSTKComboBox(
            index=0, simple=True, tooltip=_(u"The style of resistor."))
        self.cmbConstruction = ramstk.RAMSTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the resistor."))
        self.txtResistance = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The resistance (in \u03A9) of the resistor."))
        self.txtNElements = ramstk.RAMSTKEntry(
            width=125,
            tooltip=_(u"The number of active resistors in a resistor network "
                      u"or the number of potentiometer taps."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed', self._on_combo_changed,
                                          1))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbStyle.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtResistance.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self._on_focus_out, 6))

    def _do_load_comboboxes(self, **kwargs):
        """
        Load the Resisotr RKTComboBox()s.

        :param int subcategory_id: the newly selected resistor subcategory ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_comboboxes(self, **kwargs)

        # Load the quality level RAMSTKComboBox().
        if _attributes['hazard_rate_method_id'] == 1:
            _data = ["S", "R", "P", "M", ["MIL-SPEC"], [_(u"Lower")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the specification RAMSTKComboBox().
        try:
            _data = self._dic_specifications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbSpecification.do_load_combo(_data)

        # Load the type RAMSTKComboBox().
        if _attributes['hazard_rate_method_id'] == 1:
            try:
                _data = self._dic_types[self._subcategory_id]
            except KeyError:
                _data = []
        else:
            _data = [[_(u"Bead")], [_(u"Disk")], [_(u"Rod")]]
        self.cmbType.do_load_combo(_data)

        # Load the style RAMSTKComboBox().
        try:
            _data = self._dic_styles[_attributes['subcategory_id']][
                _attributes['specification_id']]
        except (KeyError, IndexError):
            _data = []
        self.cmbStyle.do_load_combo(_data)

        # Load the construction RAMSTKComboBox().
        try:
            _data = self._dic_construction[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbConstruction.do_load_combo(_data)

        return _return

    def _do_load_page(self, **kwargs):
        """
        Load the Resistor assesment input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_page(self, **kwargs)

        self.cmbType.handler_block(self._lst_handler_id[2])
        self.cmbType.set_active(_attributes['type_id'])
        self.cmbType.handler_unblock(self._lst_handler_id[2])

        if _attributes['hazard_rate_method_id'] == 2:
            self.cmbSpecification.handler_block(self._lst_handler_id[1])
            self.cmbSpecification.set_active(_attributes['specification_id'])
            self.cmbSpecification.handler_unblock(self._lst_handler_id[1])

            self.cmbStyle.handler_block(self._lst_handler_id[3])
            self.cmbStyle.set_active(_attributes['family_id'])
            self.cmbStyle.handler_unblock(self._lst_handler_id[3])

            self.cmbConstruction.handler_block(self._lst_handler_id[4])
            self.cmbConstruction.set_active(_attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[4])

            self.txtResistance.handler_block(self._lst_handler_id[5])
            self.txtResistance.set_text(
                str(self.fmt.format(_attributes['resistance'])))
            self.txtResistance.handler_unblock(self._lst_handler_id[5])

            self.txtNElements.handler_block(self._lst_handler_id[6])
            self.txtNElements.set_text(
                str(self.fmt.format(_attributes['n_elements'])))
            self.txtNElements.handler_unblock(self._lst_handler_id[6])

        return _return

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected resistor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.set_sensitive(True)
        self.cmbSpecification.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.cmbStyle.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.txtResistance.set_sensitive(False)
        self.txtNElements.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id in [1, 2, 5, 6, 7, 9, 11, 13, 15]:
                self.cmbType.set_sensitive(True)
        elif _attributes['hazard_rate_method_id'] == 2:
            self.txtResistance.set_sensitive(True)
            if self._subcategory_id in [2, 6, 7, 15]:
                self.cmbSpecification.set_sensitive(True)
            if self._subcategory_id in [6, 7]:
                self.cmbStyle.set_sensitive(True)
            if self._subcategory_id == 8:
                self.cmbType.set_sensitive(True)
            if self._subcategory_id in [10, 12]:
                self.cmbConstruction.set_sensitive(True)
            else:
                self.cmbConstruction.set_sensitive(False)
            if self._subcategory_id in [4, 9, 10, 11, 12, 13, 14, 15]:
                self.txtNElements.set_sensitive(True)
            else:
                self.txtNElements.set_sensitive(False)

        return _return

    def _make_page(self):
        """
        Make the Hardware class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_load_comboboxes(subcategory_id=self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.txtResistance, _x_pos, _y_pos[1])
        self.put(self.cmbSpecification, _x_pos, _y_pos[2])
        self.put(self.cmbType, _x_pos, _y_pos[3])
        self.put(self.cmbStyle, _x_pos, _y_pos[4])
        self.put(self.cmbConstruction, _x_pos, _y_pos[5])
        self.put(self.txtNElements, _x_pos, _y_pos[6])

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RAMSTKCombo() changes and assign to Resistor attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RAMSTKCombo() that called this method.
        :type combo: :class:`ramstk.gui.gtk.ramstk.RAMSTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RAMSTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    1    | cmbSpecification |    3    | cmbStyle         |
            +---------+------------------+---------+------------------+
            |    2    | cmbType          |    4    | cmbConstruction  |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _attributes = AssessmentInputs.on_combo_changed(self, combo, index)

        if _attributes:
            if index == 1:
                _attributes['specification_id'] = int(combo.get_active())
            elif index == 2:
                _attributes['type_id'] = int(combo.get_active())
            elif index == 3:
                _attributes['family_id'] = int(combo.get_active())
            elif index == 4:
                _attributes['construction_id'] = int(combo.get_active())

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RAMSTKEntry() widgets..

        This method is called by:

            * RAMSTKEntry() 'changed' signal
            * RAMSTKTextView() 'changed' signal

        :param entry: the RAMSTKEntry() or RAMSTKTextView() that called the method.
        :type entry: :class:`ramstk.gui.gtk.ramstk.RAMSTKEntry` or
                     :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

            +---------+---------------------+---------+---------------------+
            |  Index  | Widget              |  Index  | Widget              |
            +=========+=====================+=========+=====================+
            |    5    | txtResistance       |    6    | txtNElements        |
            +---------+---------------------+---------+---------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False
        _text = ''

        entry.handler_block(self._lst_handler_id[index])

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            try:
                _text = float(entry.get_text())
            except ValueError:
                _text = 0.0

            if index == 5:
                _attributes['resistance'] = _text
            elif index == 6:
                _attributes['n_elements'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id, **kwargs):
        """
        Load the resistor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              resistor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)


class ResistorAssessmentResults(AssessmentResults):
    """
    Display Resistor assessment results attribute data in the RAMSTK Work Book.

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

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        6:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        10:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        12:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        13:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        14:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        15:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Resistor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`ramstk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentResults.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>R</sub>:")
        self._lst_labels.append(u"\u03C0<sub>T</sub>:")
        self._lst_labels.append(u"\u03C0<sub>NR</sub>:")
        self._lst_labels.append(u"\u03C0<sub>TAPS</sub>")
        self._lst_labels.append(u"\u03C0<sub>V</sub>:")
        self._lst_labels.append(u"\u03C0<sub>C</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the resistor "
              u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiR = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The resistance factor for the resistor."))
        self.txtPiT = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The temperature factor for the resistor."))
        self.txtPiNR = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The number of resistors factor for the resistor."))
        self.txtPiTAPS = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The potentiometer taps factor for the resistor."))
        self.txtPiV = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The voltage factor for the resistor."))
        self.txtPiC = ramstk.RAMSTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The construction class factor for the resistor."))

        self._make_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self, **kwargs):
        """
        Load the Resistor assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentResults.do_load_page(self, **kwargs)

        self.txtPiR.set_text(str(self.fmt.format(_attributes['piR'])))
        self.txtPiT.set_text(str(self.fmt.format(_attributes['piT'])))
        self.txtPiNR.set_text(str(self.fmt.format(_attributes['piNR'])))
        self.txtPiTAPS.set_text(str(self.fmt.format(_attributes['piTAPS'])))
        self.txtPiV.set_text(str(self.fmt.format(_attributes['piV'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))

        return _return

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected resistor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = AssessmentResults.do_set_sensitive(self, **kwargs)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiR.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtPiNR.set_sensitive(False)
        self.txtPiTAPS.set_sensitive(False)
        self.txtPiV.set_sensitive(False)
        self.txtPiC.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            self.txtPiE.set_sensitive(True)
            if _attributes['subcategory_id'] != 8:
                self.txtPiR.set_sensitive(True)
            if _attributes['subcategory_id'] == 4:
                self.txtPiT.set_sensitive(True)
                self.txtPiNR.set_sensitive(True)
            if _attributes['subcategory_id'] in [9, 10, 11, 12, 13, 14, 15]:
                self.txtPiTAPS.set_sensitive(True)
                self.txtPiV.set_sensitive(True)
            if _attributes['subcategory_id'] in [10, 12]:
                self.txtPiC.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the resistor gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for resistors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiR, _x_pos, _y_pos[3])
        self.put(self.txtPiT, _x_pos, _y_pos[4])
        self.put(self.txtPiNR, _x_pos, _y_pos[5])
        self.put(self.txtPiTAPS, _x_pos, _y_pos[6])
        self.put(self.txtPiV, _x_pos, _y_pos[7])
        self.put(self.txtPiC, _x_pos, _y_pos[8])

        return None

    def on_select(self, module_id, **kwargs):
        """
        Load the resistor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              resistor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)
