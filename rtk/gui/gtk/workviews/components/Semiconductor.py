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
from rtk.gui.gtk.rtk.Widget import _, gtk


class AssessmentInputs(gtk.Fixed):
    """
    Display Hardware assessment input attribute data in the RTK Work Book.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2.  The attributes of a Hardware assessment input view are:

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
    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.
    :cvar list _lst_packages: the list of semiconductor packages types.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the semiconductor
                               currently being displayed.

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
    ], ["TO-99"], ["TO-126"], ["TO-127"], ["TO-204"], ["TO-204AA"], [
        "TO-205AD"
    ], ["TO-205AF"], ["TO-220"], ["DO-4"], ["DO-5"], ["DO-7"], ["DO-8"], [
        "DO-9"
    ], ["DO-13"], ["DO-14"], ["DO-29"], ["DO-35"], ["DO-41"], ["DO-45"], [
        "DO-204MB"
    ], ["DO-205AB"], ["PA-42A,B"], ["PD-36C"], ["PD-50"], ["PD-77"],
                     ["PD-180"], ["PD-319"], ["PD-262"], ["PD-975"],
                     ["PD-280"], ["PD-216"], ["PT-2G"], ["PT-2G"], ["PT-6B"],
                     ["PH-13"], ["PH-16"], ["PH-56"], ["PY-58"], ["PY-373"]]

    _lst_labels = [
        _(u"Quality Level:"),
        _(u"Package:"),
        _(u"Type:"),
        _(u"Application:"),
        _(u"Construction:"),
        _(u"Matching Network:"),
        _(u"Operating Frequency (GHz):"),
        _(u"Number of Characters:"), u"\u03B8<sub>JC</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Semiconductor assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                semiconductor.
        :param int subcategory_id: the ID of the semiconductor subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.cmbQuality = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The quality level of the semiconductor."))
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

        self._make_assessment_input_page()
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

    def _do_load_comboboxes(self, subcategory_id):
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

        self._subcategory_id = subcategory_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # Load the quality level RTKComboBox().
        _model = self.cmbQuality.get_model()
        _model.clear()

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
        _model = self.cmbApplication.get_model()
        _model.clear()

        try:
            _data = self._dic_applications[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbApplication.do_load_combo(_data)

        # Load the construction RTKComboBox().
        _model = self.cmbConstruction.get_model()
        _model.clear()

        self.cmbConstruction.do_load_combo(
            [[_(u"Metallurgically Bonded")],
             [_(u"Non-Metallurgically Bonded and Spring Loaded Contacts")]])

        # Load the matching network RTKComboBox().
        _model = self.cmbMatching.get_model()
        _model.clear()

        try:
            _data = self._dic_matchings[self._subcategory_id]
        except KeyError:
            _data = []
        self.cmbMatching.do_load_combo(_data)

        # Load the package RTKComboBox().
        _model = self.cmbPackage.get_model()
        _model.clear()

        self.cmbPackage.do_load_combo(self._lst_packages)

        # Load the type RTKComboBox().
        _model = self.cmbType.get_model()
        _model.clear()

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

    def _do_set_sensitive(self):
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

    def _make_assessment_input_page(self):
        """
        Make the semiconductor gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for semiconductors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])
        self.put(self.cmbPackage, _x_pos, _y_pos[1])
        self.put(self.cmbType, _x_pos, _y_pos[2])
        self.put(self.cmbApplication, _x_pos, _y_pos[3])
        self.put(self.cmbConstruction, _x_pos, _y_pos[4])
        self.put(self.cmbMatching, _x_pos, _y_pos[5])
        self.put(self.txtFrequencyOperating, _x_pos, _y_pos[6])
        self.put(self.txtNElements, _x_pos, _y_pos[7])
        self.put(self.txtThetaJC, _x_pos, _y_pos[8])

        self.show_all()

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

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    3    | cmbMatching      |
            +---------+------------------+---------+------------------+
            |    1    | cmbApplication   |    4    | cmbPackage       |
            +---------+------------------+---------+------------------+
            |    2    | cmbConstruction  |    5    | cmbType          |
            +---------+------------------+---------+------------------+

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        combo.handler_block(self._lst_handler_id[index])

        _model = combo.get_model()
        _row = combo.get_active_iter()

        if self._dtc_data_controller is not None:
            _attributes = self._dtc_data_controller.request_get_attributes(
                self._hardware_id)

            if index == 0:
                _attributes['quality_id'] = int(combo.get_active())
            elif index == 1:
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

    def on_select(self, module_id=None):
        """
        Load the semiconductor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              semiconductor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(_attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        self._do_set_sensitive()

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


class StressInputs(gtk.Fixed):
    """
    Display Semiconductor stress input attribute data in the RTK Work Book.

    The Semiconductor stress input view displays all the assessment inputs for
    the selected semiconductor.  This includes, currently, stress inputs for
    MIL-HDBK-217FN2.  The attributes of a semiconductor stress input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the Hardware BoM data controller instance.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the semiconductor
                               currently being displayed.

    :ivar txtTemperatureRatedMin: enter and display the minimum rated
                                  temperature of the semiconductor device.
    :ivar txtTemperatureKnee: enter and display the temperature beyond which
                              the semiconductor device must be derated.
    :ivar txtTemperatureRatedMax: enter and display the maximum rated
                                  temperature of the semiconductor device.
    :ivar txtCurrentRated: enter and display the rated current of the
                           semiconductor device.
    :ivar txtCurrentOperating: enter and display the operating power of the
                               semiconductor device.
    :ivar txtPowerRated: enter and display the rated power of the semiconductor
                         device.
    :ivar txtPowerOperating: enter and display the operating power of the
                             semiconductor device.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           semiconductor device.
    :ivar txtVoltageAC: enter and display the operating ac voltage of the
                        semiconductor device.
    :ivar txtVoltageDC: enter and display the operating DC voltage of the
                        semiconductor device.

    Callbacks signals in _lst_handler_id:

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | txtTemperatureRatedMin - `changed`        |
    +-------+-------------------------------------------+
    |   1   | txtTemperatureKnee - `changed`            |
    +-------+-------------------------------------------+
    |   2   | txtTemperatureRatedMax - `changed`        |
    +-------+-------------------------------------------+
    |   3   | txtPowerRated - `changed`                 |
    +-------+-------------------------------------------+
    |   4   | txtPowerOperating - `changed`             |
    +-------+-------------------------------------------+
    |   5   | txtVoltageRated - `changed`               |
    +-------+-------------------------------------------+
    |   6   | txtVoltageAC - `changed`                  |
    +-------+-------------------------------------------+
    |   7   | txtVoltageDC - `changed`                  |
    +-------+-------------------------------------------+
    |   8   | txtCurrentRated - `changed`               |
    +-------+-------------------------------------------+
    |   9   | txtCurrentOperating - `changed`           |
    +-------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Minimum Rated Temperature (\u00B0C):"),
        _(u"Knee Temperature (\u00B0C):"),
        _(u"Maximum Rated Temperature (\u00B0C):"),
        _(u"Rated Current (A):"),
        _(u"Operating Current (A):"),
        _(u"Rated Power (W):"),
        _(u"Operating Power (W):"),
        _(u"Rated Voltage (V):"),
        _(u"Operating ac Voltage (V):"),
        _(u"Operating DC Voltage (V):")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Semiconductor stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                semiconductor.
        :param int subcategory_id: the ID of the semiconductor subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtTemperatureRatedMin = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The minimum rated temperature (in \u00B0C) of the "
                      u"semiconductor device."))
        self.txtTemperatureKnee = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The break temperature (in \u00B0C) of the semiconductor "
                u"device beyond which it must be derated."))
        self.txtTemperatureRatedMax = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The maximum rated temperature (in \u00B0C) of the "
                      u"semiconductor device."))
        self.txtCurrentRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated current (in A) of the semiconductor "
                      u"device."))
        self.txtCurrentOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating current (in A) of the semiconductor "
                      u"device."))
        self.txtPowerRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated power (in W) of the semiconductor device."))
        self.txtPowerOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating power (in W) of the semiconductor "
                      u"device."))
        self.txtVoltageRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated voltage (in V) of the semiconductor "
                      u"device."))
        self.txtVoltageAC = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating ac voltage (in V) of the semiconductor "
                      u"device."))
        self.txtVoltageDC = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operating DC voltage (in V) of the semiconductor "
                      u"device."))

        self._lst_handler_id.append(
            self.txtTemperatureRatedMin.connect('changed', self._on_focus_out,
                                                0))
        self._lst_handler_id.append(
            self.txtTemperatureKnee.connect('changed', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect('changed', self._on_focus_out,
                                                2))
        self._lst_handler_id.append(
            self.txtPowerRated.connect('changed', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.txtPowerOperating.connect('changed', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtVoltageAC.connect('changed', self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtVoltageDC.connect('changed', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtCurrentRated.connect('changed', self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtCurrentOperating.connect('changed', self._on_focus_out, 9))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the semiconductor module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for semiconductors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[2])
        self.put(self.txtCurrentRated, _x_pos, _y_pos[3])
        self.put(self.txtCurrentOperating, _x_pos, _y_pos[4])
        self.put(self.txtPowerRated, _x_pos, _y_pos[5])
        self.put(self.txtPowerOperating, _x_pos, _y_pos[6])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[7])
        self.put(self.txtVoltageAC, _x_pos, _y_pos[8])
        self.put(self.txtVoltageDC, _x_pos, _y_pos[9])

        self.show_all()

        return None

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

            +-------+------------------------+-------+---------------------+
            | Index | Widget                 | Index | Widget              |
            +=======+========================+=======+=====================+
            |   0   | txtTemperatureRatedMin |   5   | txtVoltageRated     |
            +-------+------------------------+-------+---------------------+
            |   1   | txtTemperatureKnee     |   6   | txtVoltageAC        |
            +-------+------------------------+-------+---------------------+
            |   2   | txtTemperatureRatedMax |   7   | txtVoltageDC        |
            +-------+------------------------+-------+---------------------+
            |   3   | txtPowerRated          |   8   | txtCurrentRated     |
            +-------+------------------------+-------+---------------------+
            |   4   | txtPowerOperating      |   9   | txtCurrentOperating |
            +-------+------------------------+-------+---------------------+

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

            if index == 0:
                _attributes['temperature_rated_min'] = _text
            elif index == 1:
                _attributes['temperature_knee'] = _text
            elif index == 2:
                _attributes['temperature_rated_max'] = _text
            elif index == 3:
                _attributes['power_rated'] = _text
            elif index == 4:
                _attributes['power_operating'] = _text
            elif index == 5:
                _attributes['voltage_rated'] = _text
            elif index == 6:
                _attributes['voltage_ac_operating'] = _text
            elif index == 7:
                _attributes['voltage_dc_operating'] = _text
            elif index == 8:
                _attributes['current_rated'] = _text
            elif index == 9:
                _attributes['current_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the semiconductor stress input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              semiconductor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # We don't block the callback signal otherwise the style RTKComboBox()
        # will not be loaded and set.
        self.txtTemperatureRatedMin.handler_block(self._lst_handler_id[0])
        self.txtTemperatureRatedMin.set_text(
            str(self.fmt.format(_attributes['temperature_rated_min'])))
        self.txtTemperatureRatedMin.handler_unblock(self._lst_handler_id[0])

        self.txtTemperatureKnee.handler_block(self._lst_handler_id[1])
        self.txtTemperatureKnee.set_text(
            str(self.fmt.format(_attributes['temperature_knee'])))
        self.txtTemperatureKnee.handler_unblock(self._lst_handler_id[1])

        self.txtTemperatureRatedMax.handler_block(self._lst_handler_id[2])
        self.txtTemperatureRatedMax.set_text(
            str(self.fmt.format(_attributes['temperature_rated_max'])))
        self.txtTemperatureRatedMax.handler_unblock(self._lst_handler_id[2])

        self.txtPowerRated.handler_block(self._lst_handler_id[3])
        self.txtPowerRated.set_text(
            str(self.fmt.format(_attributes['power_rated'])))
        self.txtPowerRated.handler_unblock(self._lst_handler_id[3])

        self.txtPowerOperating.handler_block(self._lst_handler_id[4])
        self.txtPowerOperating.set_text(
            str(self.fmt.format(_attributes['power_operating'])))
        self.txtPowerOperating.handler_unblock(self._lst_handler_id[4])

        self.txtVoltageRated.handler_block(self._lst_handler_id[5])
        self.txtVoltageRated.set_text(
            str(self.fmt.format(_attributes['voltage_rated'])))
        self.txtVoltageRated.handler_unblock(self._lst_handler_id[5])

        self.txtVoltageAC.handler_block(self._lst_handler_id[6])
        self.txtVoltageAC.set_text(
            str(self.fmt.format(_attributes['voltage_ac_operating'])))
        self.txtVoltageAC.handler_unblock(self._lst_handler_id[6])

        self.txtVoltageDC.handler_block(self._lst_handler_id[7])
        self.txtVoltageDC.set_text(
            str(self.fmt.format(_attributes['voltage_dc_operating'])))
        self.txtVoltageDC.handler_unblock(self._lst_handler_id[7])

        self.txtCurrentRated.handler_block(self._lst_handler_id[8])
        self.txtCurrentRated.set_text(
            str(self.fmt.format(_attributes['current_rated'])))
        self.txtCurrentRated.handler_unblock(self._lst_handler_id[8])

        self.txtCurrentOperating.handler_block(self._lst_handler_id[9])
        self.txtCurrentOperating.set_text(
            str(self.fmt.format(_attributes['current_operating'])))
        self.txtCurrentOperating.handler_unblock(self._lst_handler_id[9])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display semiconductor assessment results attribute data.

    The semiconductor assessment result view displays all the assessment
    results for the selected semiconductor.  This includes, currently, results
    for MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of
    a semiconductor assessment result view are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the semiconductor
                               currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtLambdaB: displays the base hazard rate of the semiconductor.
    :ivar txtPiQ: displays the quality factor for the semiconductor.
    :ivar txtPiE: displays the environment factor for the semiconductor.
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

    # Define private list attributes.
    _lst_labels = [
        u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:",
        u"\u03C0<sub>T</sub>:", u"\u03C0<sub>A</sub>:", u"\u03C0<sub>C</sub>:",
        u"\u03C0<sub>R</sub>:", u"\u03C0<sub>M</sub>:", u"\u03C0<sub>I</sub>:",
        u"\u03C0<sub>P</sub>:", u"\u03C0<sub>S</sub>:"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Semiconductor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                semiconductor.
        :param int subcategory_id: the ID of the semiconductor subcategory.
        """
        gtk.Fixed.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        self._lblModel = rtk.RTKLabel(
            '',
            tooltip=_(
                u"The assessment model used to calculate the semiconductor "
                u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate of the semiconductor."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the semiconductor."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the semiconductor."))
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

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the semiconductor assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))

        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))
        self.txtPiT.set_text(str(self.fmt.format(_attributes['piT'])))
        self.txtPiA.set_text(str(self.fmt.format(_attributes['piA'])))
        self.txtPiC.set_text(str(self.fmt.format(_attributes['piC'])))
        self.txtPiR.set_text(str(self.fmt.format(_attributes['piR'])))
        self.txtPiM.set_text(str(self.fmt.format(_attributes['piM'])))
        self.txtPiI.set_text(str(self.fmt.format(_attributes['piI'])))
        self.txtPiP.set_text(str(self.fmt.format(_attributes['piP'])))
        self.txtPiS.set_text(str(self.fmt.format(_attributes['piS'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected semiconductor.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtPiQ.set_sensitive(True)
        self.txtPiE.set_sensitive(False)
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

    def _make_assessment_results_page(self):
        """
        Make the semiconductor gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        if _attributes['hazard_rate_method_id'] == 1:
            self._lblModel.set_markup(
                u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = "
                u"\u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>")
            self._lst_labels[0] = u"\u03BB<sub>g</sub>:"
        else:
            try:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id])
            except KeyError:
                self._lblModel.set_markup(_(u"Missing Model"))
            self._lst_labels[0] = u"\u03BB<sub>b</sub>:"

        self._do_set_sensitive()

        # Build the container for semiconductors.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtPiQ, _x_pos, _y_pos[1])
        self.put(self.txtPiE, _x_pos, _y_pos[2])
        self.put(self.txtPiT, _x_pos, _y_pos[3])
        self.put(self.txtPiA, _x_pos, _y_pos[4])
        self.put(self.txtPiC, _x_pos, _y_pos[5])
        self.put(self.txtPiR, _x_pos, _y_pos[6])
        self.put(self.txtPiM, _x_pos, _y_pos[7])
        self.put(self.txtPiI, _x_pos, _y_pos[8])
        self.put(self.txtPiP, _x_pos, _y_pos[9])
        self.put(self.txtPiS, _x_pos, _y_pos[10])

        self.show_all()

        return None

    def on_select(self, module_id=None):
        """
        Load the semiconductor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              semiconductor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_set_sensitive()
        self._do_load_page()

        return _return


class StressResults(gtk.HPaned):
    """
    Display semiconductor stress results attribute data in the RTK Work Book.

    The semiconductor stress result view displays all the stress results for
    the selected semiconductor.  This includes, currently, results for
    MIL-HDBK-217FN2 parts count and part stress methods.  The attributes of a
    semiconductor stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar int _hardware_id: the ID of the Hardware item currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the semiconductor
                               currently being displayed.

    :ivar txtCurrentRatio: display the current ratio for the semiconductor.
    :ivar txtPowerRatio: display the power ratio for the semiconductor.
    :ivar txtVoltageRatio: display the voltage ratio for the semiconductor.
    :ivar txtTemperatureCase: display the surface temperature of the
                              semiconductor.
    :ivar txtTemperatureJunction: display the junction temperature for the
                                  semiconductor.
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Current Ratio:"),
        _(u"Power Ratio:"),
        _(u"Voltage Ratio:"),
        _(u"Case Temperature (\u00B0C):"),
        _(u"Junction Temperature (\u00B0C):"), "",
        _(u"Overstress Reason:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Semiconductor assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.Controller.HardwareBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                semiconductor.
        :param int subcategory_id: the ID of the semiconductor subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.7, 0.7, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.pltDerate = rtk.RTKPlot()

        self.txtCurrentRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating current to rated current for "
                      u"the semiconductor."))
        self.txtPowerRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating power to rated power for "
                      u"the semiconductor."))
        self.txtVoltageRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating voltage to rated voltage for "
                      u"the semiconductor."))
        self.txtTemperatureCase = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The case temperature (in \u00B0C) of the "
                      u"semiconductor."))
        self.txtTemperatureJunction = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The junction temperature (in \u00B0C) of the "
                      u"semiconductor."))
        self.chkOverstress = rtk.RTKCheckButton(
            label=_(u"Overstressed"),
            tooltip=_(u"Indicates whether or not the selected semiconductor "
                      u"is overstressed."))
        self.txtReason = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=250,
            tooltip=_(u"The reason(s) the selected hardware item is "
                      u"overstressed."))

        self.chkOverstress.set_sensitive(False)
        self.txtReason.set_editable(False)
        _bg_color = gtk.gdk.Color('#ADD8E6')
        self.txtReason.modify_base(gtk.STATE_NORMAL, _bg_color)
        self.txtReason.modify_base(gtk.STATE_ACTIVE, _bg_color)
        self.txtReason.modify_base(gtk.STATE_PRELIGHT, _bg_color)
        self.txtReason.modify_base(gtk.STATE_SELECTED, _bg_color)
        self.txtReason.modify_base(gtk.STATE_INSENSITIVE, _bg_color)

        self._make_stress_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_derating_curve(self):
        """
        Load the benign and harsh environment derating curves.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        # Plot the derating curve.
        _x = [
            float(_attributes['temperature_rated_min']),
            float(_attributes['temperature_knee']),
            float(_attributes['temperature_rated_max'])
        ]

        self.pltDerate.axis.cla()
        self.pltDerate.axis.grid(True, which='both')

        self.pltDerate.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[0],
            plot_type='scatter',
            marker='r.-')

        self.pltDerate.do_load_plot(
            x_values=_x,
            y_values=self._lst_derate_criteria[1],
            plot_type='scatter',
            marker='b.-')

        self.pltDerate.do_load_plot(
            x_values=[_attributes['temperature_active']],
            y_values=[_attributes['power_ratio']],
            plot_type='scatter',
            marker='go')

        self.pltDerate.do_make_title(
            _(u"Power Derating Curve for {0:s} at {1:s}").format(
                _attributes['part_number'], _attributes['ref_des']),
            fontsize=12)
        self.pltDerate.do_make_legend([
            _(u"Harsh Environment"),
            _(u"Mild Environment"),
            _(u"Power Operating Point")
        ])

        self.pltDerate.do_make_labels(
            _(u"Temperature (\u2070C)"), 0, -0.2, fontsize=10)
        self.pltDerate.do_make_labels(
            _(u"Power Ratio"), -1, 0, set_x=False, fontsize=10)

        self.pltDerate.figure.canvas.draw()

        return _return

    def _do_load_page(self):
        """
        Load the semiconductor assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtCurrentRatio.set_text(
            str(self.fmt.format(_attributes['current_ratio'])))
        self.txtPowerRatio.set_text(
            str(self.fmt.format(_attributes['power_ratio'])))
        self.txtVoltageRatio.set_text(
            str(self.fmt.format(_attributes['voltage_ratio'])))
        self.txtTemperatureCase.set_text(
            str(self.fmt.format(_attributes['temperature_case'])))
        self.txtTemperatureJunction.set_text(
            str(self.fmt.format(_attributes['temperature_junction'])))
        self.chkOverstress.set_active(_attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(_attributes['reason'])

        self._do_load_derating_curve()

        return _return

    def _make_stress_results_page(self):
        """
        Make the semiconductor gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        # Create the left side.
        _fixed = gtk.Fixed()
        self.pack1(_fixed, True, True)

        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, _fixed, 5, 35)
        _x_pos += 50

        _fixed.put(self.txtCurrentRatio, _x_pos, _y_pos[0])
        _fixed.put(self.txtPowerRatio, _x_pos, _y_pos[1])
        _fixed.put(self.txtVoltageRatio, _x_pos, _y_pos[2])
        _fixed.put(self.txtTemperatureCase, _x_pos, _y_pos[3])
        _fixed.put(self.txtTemperatureJunction, _x_pos, _y_pos[4])
        _fixed.put(self.chkOverstress, _x_pos, _y_pos[5])
        _fixed.put(self.txtReason.scrollwindow, _x_pos, _y_pos[6])

        _fixed.show_all()

        # Create the derating plot.
        _frame = rtk.RTKFrame(label=_(u"Derating Curve and Operating Point"))
        _frame.add(self.pltDerate.plot)
        _frame.show_all()

        self.pack2(_frame, True, True)

        return _return

    def on_select(self, module_id=None):
        """
        Load the semiconductor assessment input work view widgets.

        :param int module_id: the Hardware ID of the selected/edited
                              semiconductor.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_load_page()

        return _return
