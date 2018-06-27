# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.Semiconductor.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Semiconductor Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _
from rtk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class SemiconductorAssessmentInputs(AssessmentInputs):
    """
    Display Semiconductor assessment input attribute data in the RTK Work Book.

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
    _dic_quality = {
        1: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")], [_(u"Plastic")]],
        2: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")], [_(u"Plastic")]],
        3: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")], [_(u"Plastic")]],
        4: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")], [_(u"Plastic")]],
        5: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")], [_(u"Plastic")]],
        6: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")]],
        7: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")]],
        8: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")]],
        9: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")]],
        10: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")], [_(u"Plastic")]],
        11: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")], [_(u"Plastic")]],
        12: [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")], [_(u"Plastic")]],
        13: [[_(u"Hermetic Package")], [_(u"Nonhermetic with Facet Coating")],
             [_(u"Nonhermetic without Facet Coating")]]
    }
    # Key is subcategory ID; index is type ID.
    _dic_types = {
        1: [[_(u"General Purpose Analog")], [_(u"Switching")], [
            _(u"Power Rectifier, Fast Recovery")
        ], [_(u"Power Rectifier/Schottky Power Diode")], [
            _(u"Power Rectifier with High Voltage Stacks")
        ], [_(u"Transient Suppressor/Varistor")], [_(u"Current Regulator")], [
            _(u"Voltage Regulator and Voltage Reference (Avalanche and Zener)")
        ]],
        2:
        [[_(u"Si IMPATT (<35 GHz)")], [_(u"Gunn/Bulk Effect")],
         [_(u"Tunnel and Back (Including Mixers, Detectors)")], [_(u"PIN")], [
             _(u"Schottky Barrier (Including Detectors) and "
               u"Point Contact (200 MHz < Frequency < 35MHz)")
         ], [_(u"Varactor and Step Recovery")]],
        3: [[u"NPN/PNP (f < 200MHz)"], [_(u"Power NPN/PNP (f < 200 MHz)")]],
        4: [["MOSFET"], ["JFET"]],
        7: [[_(u"Gold Metallization")], [_(u"Aluminum Metallization")]],
        8: [[u"GaAs FET (P < 100mW)"], [u"GaAs FET (P > 100mW)"]],
        9: [["MOSFET"], ["JFET"]],
        11: [[_(u"Photo-Transistor")], [_(u"Photo-Diode")], [
            _(u"Photodiode Output, Single Device")
        ], [_(u"Phototransistor Output, Single Device")], [
            _(u"Photodarlington Output, Single Device")
        ], [_(u"Light Sensitive Resistor, Single Device")], [
            _(u"Photodiode Output, Dual Device")
        ], [_(u"Phototransistor Output, Dual Device")], [
            _(u"Photodarlington Output, Dual Device")
        ], [_(u"Light Sensitive Resistor, Dual Device")],
             [_(u"Infrared Light Emitting Diode (IRLED)")],
             [_(u"Light Emitting Diode")]],
        12: [[_(u"Segment Display")], [_(u"Diode Array Display")]],
        13: [["GaAs/Al GaAs"], ["In GaAs/In GaAsP"]]
    }
    # Key is subcategory ID; index is application ID.
    _dic_applications = {
        2: [[_(u"Varactor, Voltage Control")], [_(u"Varactor, Multiplier")],
            [_(u"All Other Diodes")]],
        3: [[_(u"Linear Amplification")], [_(u"Switching")]],
        4:
        [[_(u"Linear Amplification")], [_(u"Small Signal Switching")],
         [_(u"Non-Linear (2W < Pr < 5W)")], [_(u"Non-Linear (5W < Pr < 50W)")],
         [_(u"Non-Linear (50W < Pr < 250W)")], [_(u"Non-Linear (Pr > 250W)")]],
        7: [["CW"], [_(u"Pulsed")]],
        8: [[_(u"All Lower Power and Pulsed")], ["CW"]],
        13: [["CW"], [_(u"Pulsed")]]
    }
    # Key is subcategory ID; index is matching ID.
    _dic_matchings = {
        7: [[_(u"Input and Output")], [_(u"Input Only")], [_(u"None")]],
        8: [[_(u"Input and Output")], [_(u"Input Only")], [_(u"None")]]
    }

    # Define private list attributes.
    _lst_packages = [["TO-1"], ["TO-3"], ["TO-5"], ["TO-8"], ["TO-9"], [
        "TO-12"
    ], ["TO-18"], ["TO-28"], ["TO-33"], ["TO-39"], ["TO-41"], ["TO-44"], [
        "TO-46"
    ], ["TO-52"], ["TO-53"], ["TO-57"], ["TO-59"], ["TO-60"], ["TO-61"], [
        "TO-63"
    ], ["TO-66"], ["TO-71"], ["TO-72"], ["TO-83"], ["TO-89"], ["TO-92"], [
        "TO-94"
    ], ["TO-99"], ["TO-126"], ["TO-127"], ["TO-204"], ["TO-204AA"],
                     ["TO-205AD"], ["TO-205AF"], ["TO-220"], ["DO-4"], [
                         "DO-5"
                     ], ["DO-7"], ["DO-8"], ["DO-9"], ["DO-13"], ["DO-14"],
                     ["DO-29"], ["DO-35"], ["DO-41"], ["DO-45"], ["DO-204MB"],
                     ["DO-205AB"], ["PA-42A,B"], ["PD-36C"], ["PD-50"], [
                         "PD-77"
                     ], ["PD-180"], ["PD-319"], ["PD-262"], ["PD-975"], [
                         "PD-280"
                     ], ["PD-216"], ["PT-2G"], ["PT-2G"], ["PT-6B"], ["PH-13"],
                     ["PH-16"], ["PH-56"], ["PY-58"], ["PY-373"]]

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Semiconductor assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentInputs.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Package:"))
        self._lst_labels.append(_(u"Type:"))
        self._lst_labels.append(_(u"Application:"))
        self._lst_labels.append(_(u"Construction:"))
        self._lst_labels.append(_(u"Matching Network:"))
        self._lst_labels.append(_(u"Operating Frequency (GHz):"))
        self._lst_labels.append(_(u"Number of Characters:"))
        self._lst_labels.append(u"\u03B8<sub>JC</sub>:")

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.cmbPackage = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The package type for the semiconductor."))
        self.cmbType = rtk.RTKComboBox(
            index=0, simple=False, tooltip=_(u"The type of semiconductor."))
        self.cmbApplication = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The application of the semiconductor."))
        self.cmbConstruction = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the semiconductor."))
        self.cmbMatching = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The matching network of the semiconductor."))

        self.txtFrequencyOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating frequency of the semiconductor."))
        self.txtNElements = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The number of characters in the optoelectronic display."))
        self.txtThetaJC = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The junction-case thermal resistance of the semiconductor."))

        self._make_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbMatching.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbPackage.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.txtFrequencyOperating.connect('changed', self._on_focus_out,
                                               6))
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtThetaJC.connect('changed', self._on_focus_out, 8))

    def _do_load_comboboxes(self, **kwargs):
        """
        Load the semiconductor RKTComboBox()s.

        This method is used to load the specification RTKComboBox() whenever
        the semiconductor subcategory is changed.

        :param int subcategory_id: the newly selected semiconductor subcategory
                                   ID.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_comboboxes(self, **kwargs)

        # Load the quality level RTKComboBox().
        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id == 13:
                _data = [[_(u"Hermetic Package")],
                         [_(u"Nonhermetic with Facet Coating")],
                         [_(u"Nonhermetic without Facet Coating")]]
            else:
                _data = [["JANTXV"], ["JANTX"], ["JAN"], [_(u"Lower")],
                         [_(u"Plastic")]]
        else:
            try:
                _data = self._dic_quality[self._subcategory_id]
            except KeyError:
                _data = []
        self.cmbQuality.do_load_combo(_data)

        # Load the application RTKComboBox().
        try:
            _data = self._dic_applications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data)

        # Load the construction RTKComboBox().
        self.cmbConstruction.do_load_combo(
            [[_(u"Metallurgically Bonded")],
             [_(u"Non-Metallurgically Bonded and Spring Loaded Contacts")]])

        # Load the matching network RTKComboBox().
        try:
            _data = self._dic_matchings[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbMatching.do_load_combo(_data)

        # Load the package RTKComboBox().
        self.cmbPackage.do_load_combo(self._lst_packages)

        # Load the type RTKComboBox().
        try:
            if (_attributes['hazard_rate_method_id'] == 1
                    and self._subcategory_id == 11):
                _data = [[_(u"Photodetector")], [_(u"Opto-Isolator")],
                         [_(u"Emitter")]]
            else:
                _data = self._dic_types[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

        return _return

    def _do_load_page(self, **kwargs):
        """
        Load the Semiconductor assesment input widgets.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentInputs.do_load_page(self, **kwargs)

        if _attributes['hazard_rate_method_id'] == 2:
            self.cmbApplication.handler_block(self._lst_handler_id[1])
            self.cmbApplication.set_active(_attributes['application_id'])
            self.cmbApplication.handler_unblock(self._lst_handler_id[1])

            self.cmbConstruction.handler_block(self._lst_handler_id[2])
            self.cmbConstruction.set_active(_attributes['construction_id'])
            self.cmbConstruction.handler_unblock(self._lst_handler_id[2])

            self.cmbMatching.handler_block(self._lst_handler_id[3])
            self.cmbMatching.set_active(_attributes['matching_id'])
            self.cmbMatching.handler_unblock(self._lst_handler_id[3])

            self.cmbPackage.handler_block(self._lst_handler_id[4])
            self.cmbPackage.set_active(_attributes['package_id'])
            self.cmbPackage.handler_unblock(self._lst_handler_id[4])

            self.cmbType.handler_block(self._lst_handler_id[5])
            self.cmbType.set_active(_attributes['type_id'])
            self.cmbType.handler_unblock(self._lst_handler_id[5])

            self.txtFrequencyOperating.handler_block(self._lst_handler_id[6])
            self.txtFrequencyOperating.set_text(
                str(self.fmt.format(_attributes['frequency_operating'])))
            self.txtFrequencyOperating.handler_unblock(self._lst_handler_id[6])

            self.txtNElements.handler_block(self._lst_handler_id[7])
            self.txtNElements.set_text(
                str(self.fmt.format(_attributes['n_elements'])))
            self.txtNElements.handler_unblock(self._lst_handler_id[7])

            self.txtThetaJC.handler_block(self._lst_handler_id[8])
            self.txtThetaJC.set_text(
                str(self.fmt.format(_attributes['theta_jc'])))
            self.txtThetaJC.handler_unblock(self._lst_handler_id[8])

        return _return

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected semiconductor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.cmbMatching.set_sensitive(False)
        self.cmbPackage.set_sensitive(False)
        self.cmbType.set_sensitive(False)
        self.txtFrequencyOperating.set_sensitive(False)
        self.txtNElements.set_sensitive(False)
        self.txtThetaJC.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 1:
            if _attributes['subcategory_id'] in [1, 2, 3, 8, 11, 13]:
                self.cmbType.set_sensitive(True)
        elif _attributes['hazard_rate_method_id'] == 2:
            self.cmbPackage.set_sensitive(True)
            self.txtThetaJC.set_sensitive(True)

            if _attributes['subcategory_id'] in [2, 3, 4, 7, 8, 13]:
                self.cmbApplication.set_sensitive(True)
            if _attributes['subcategory_id'] in [1, 12]:
                self.cmbConstruction.set_sensitive(True)
            if _attributes['subcategory_id'] in [7, 8]:
                self.cmbMatching.set_sensitive(True)
                self.txtFrequencyOperating.set_sensitive(True)
            if _attributes['subcategory_id'] in [1, 2, 4, 7, 9, 11, 12, 13]:
                self.cmbType.set_sensitive(True)
            if _attributes['subcategory_id'] == 12:
                self.txtNElements.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the semiconductor gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._do_load_comboboxes(subcategory_id=self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_page(self)

        self.put(self.cmbPackage, _x_pos, _y_pos[1])
        self.put(self.cmbType, _x_pos, _y_pos[2])
        self.put(self.cmbApplication, _x_pos, _y_pos[3])
        self.put(self.cmbConstruction, _x_pos, _y_pos[4])
        self.put(self.cmbMatching, _x_pos, _y_pos[5])
        self.put(self.txtFrequencyOperating, _x_pos, _y_pos[6])
        self.put(self.txtNElements, _x_pos, _y_pos[7])
        self.put(self.txtThetaJC, _x_pos, _y_pos[8])

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Semiconductor attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   1   | cmbApplication   |   4   | cmbPackage       |
            +-------+------------------+-------+------------------+
            |   2   | cmbConstruction  |   5   | cmbType          |
            +-------+------------------+-------+------------------+
            |   3   | cmbMatching      |       |                  |
            +-------+------------------+-------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _attributes = AssessmentInputs.on_combo_changed(self, combo, index)

        if _attributes:
            if index == 1:
                _attributes['application_id'] = int(combo.get_active())
            elif index == 2:
                _attributes['construction_id'] = int(combo.get_active())
            elif index == 3:
                _attributes['matching_id'] = int(combo.get_active())
            elif index == 4:
                _attributes['package_id'] = int(combo.get_active())
            elif index == 5:
                _attributes['type_id'] = int(combo.get_active())

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        combo.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_focus_out(self, entry, index):
        """
        Retrieve changes made in RTKEntry() widgets..

        This method is called by:

            * RTKEntry() 'changed' signal
            * RTKTextView() 'changed' signal

        :param entry: the RTKEntry() or RTKTextView() that called the method.
        :type entry: :class:`rtk.gui.gtk.rtk.RTKEntry` or
                     :class:`rtk.gui.gtk.rtk.RTKTextView`
        :param int index: the position in the Hardware class gtk.TreeModel()
                          associated with the data from the calling
                          gtk.Widget().  Indices are:

            +-------+-----------------------+-------+---------------------+
            | Index | Widget                | Index | Widget              |
            +=======+=======================+=======+=====================+
            |   6   | txtFrequencyOperating |   8   | txtThetaJC          |
            +-------+-----------------------+-------+---------------------+
            |   7   | txtNElements          |       |                     |
            +-------+-----------------------+-------+---------------------+

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

            if index == 6:
                _attributes['frequency_operating'] = _text
            elif index == 7:
                _attributes['n_elements'] = _text
            elif index == 8:
                _attributes['theta_jc'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id, **kwargs):
        """
        Load the semiconductor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              semiconductor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)


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
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        3:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        4:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        5:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        6:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        7:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        8:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        9:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        10:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        11:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        12:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
        13:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>I</sub>\u03C0<sub>A</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>"
    }

    def __init__(self, controller, **kwargs):
        """
        Initialize an instance of the Semiconductor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        """
        AssessmentResults.__init__(self, controller, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"\u03C0<sub>T</sub>:")
        self._lst_labels.append(u"\u03C0<sub>A</sub>:")
        self._lst_labels.append(u"\u03C0<sub>C</sub>:")
        self._lst_labels.append(u"\u03C0<sub>R</sub>:")
        self._lst_labels.append(u"\u03C0<sub>M</sub>:")
        self._lst_labels.append(u"\u03C0<sub>I</sub>:")
        self._lst_labels.append(u"\u03C0<sub>P</sub>:")
        self._lst_labels.append(u"\u03C0<sub>S</sub>:")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the semiconductor "
              u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtPiT = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The temperature factor for the semiconductor."))
        self.txtPiA = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The application factor for the semiconductor."))
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The construction factor for the semiconductor."))
        self.txtPiR = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The power rating factor for the semiconductor."))
        self.txtPiM = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The matching network factor for the semiconductor."))
        self.txtPiI = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The forward current factor for the semiconductor."))
        self.txtPiP = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The power degradation factor for the semiconductor."))
        self.txtPiS = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The electrical stress factor for the semiconductor."))

        self._make_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self, **kwargs):
        """
        Load the semiconductor assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = AssessmentResults.do_load_page(self, **kwargs)

        self.txtPiT.set_text(str(self.fmt.format(_attributes['piT'])))
        self.txtPiA.set_text(str(self.fmt.format(_attributes['piA'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiR.set_text(str(self.fmt.format(_attributes['piR'])))
        self.txtPiM.set_text(str(self.fmt.format(_attributes['piM'])))
        self.txtPiI.set_text(str(self.fmt.format(_attributes['piI'])))
        self.txtPiP.set_text(str(self.fmt.format(_attributes['piP'])))
        self.txtPiS.set_text(str(self.fmt.format(_attributes['piS'])))

        return _return

    def _do_set_sensitive(self, **kwargs):
        """
        Set widget sensitivity as needed for the selected semiconductor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = AssessmentResults.do_set_sensitive(self, **kwargs)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiT.set_sensitive(False)
        self.txtPiA.set_sensitive(False)
        self.txtPiC.set_sensitive(False)
        self.txtPiR.set_sensitive(False)
        self.txtPiM.set_sensitive(False)
        self.txtPiI.set_sensitive(False)
        self.txtPiP.set_sensitive(False)
        self.txtPiS.set_sensitive(False)

        if _attributes['hazard_rate_method_id'] == 2:
            self.txtPiE.set_sensitive(True)
            self.txtPiT.set_sensitive(True)
            if _attributes['subcategory_id'] == 1:
                self.txtPiC.set_sensitive(True)
            if _attributes['subcategory_id'] == 13:
                self.txtPiI.set_sensitive(True)
                self.txtPiP.set_sensitive(True)
            if _attributes['subcategory_id'] in [2, 3, 4, 7, 8, 13]:
                self.txtPiA.set_sensitive(True)
            if _attributes['subcategory_id'] in [7, 8]:
                self.txtPiM.set_sensitive(True)
            if _attributes['subcategory_id'] in [2, 3, 6, 10]:
                self.txtPiR.set_sensitive(True)
            if _attributes['subcategory_id'] in [1, 3, 6, 10]:
                self.txtPiS.set_sensitive(True)

        return _return

    def _make_page(self):
        """
        Make the semiconductor gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_page(self)

        self.put(self.txtPiT, _x_pos, _y_pos[3])
        self.put(self.txtPiA, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])
        self.put(self.txtPiR, _x_pos, _y_pos[6])
        self.put(self.txtPiM, _x_pos, _y_pos[7])
        self.put(self.txtPiI, _x_pos, _y_pos[8])
        self.put(self.txtPiP, _x_pos, _y_pos[9])
        self.put(self.txtPiS, _x_pos, _y_pos[10])

        return None

    def on_select(self, module_id, **kwargs):
        """
        Load the semiconductor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              semiconductor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._hardware_id = module_id

        self._do_set_sensitive(**kwargs)

        return self._do_load_page(**kwargs)
