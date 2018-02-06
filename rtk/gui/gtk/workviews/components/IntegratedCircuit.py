# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.IntegratedCircuit.py is part of the
#       RTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Work View."""

from pubsub import pub  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gtk  # pylint: disable=E0401,W0611


class AssessmentInputs(gtk.Fixed):
    """
    Display IC assessment input attribute data in the RTK Work Book.

    The integrated circuit assessment input view displays all the assessment
    inputs for the selected integrated circuit.  This includes, currently,
    inputs for MIL-HDBK-217FN2.  The attributes of an integrated circuit
    assessment input view are:

    :cvar dict _dic_technology: dictionary of integrated circuit package
                                technologies.  Key is integrated circuit
                                subcategory ID; values are lists of
                                technologies.

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.
    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar int _hardware_id: the ID of the integrated circuit currently being
                            displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the integrated
                               circuit currently being displayed.

    :ivar cmbApplication: select and display the application of the integrated
                          circuit.
    :ivar cmbConstruction: select and display the construction of the
                           integrated circuit.
    :ivar cmbECC: select and display the error correction code used by the
                  EEPROM.
    :ivar cmbManufacturing: select and display the manufacturing approach for
                            the integrated circuit.
    :ivar cmbPackage: select and display the package type of the integrated
                      circuit.
    :ivar cmbTechnology: select and display the technology used in the
                         integrated circuit.
    :ivar cmbType: select and display the type of the integrated circuit.

    :ivar txtArea: enter and display the die area of the integrated circuit.
    :ivar txtFeatureSize: enter and display the feature size (in microns) of
                          the VLSI.
    :ivar txtNActivePins: enter and display the number of active pins.
    :ivar txtNCycles: enter and display the number of programming cycles over
                      the life of the PROM.
    :ivar txtNElements: enter and display the number of elements (transistors,
                        gates, etc.) in the integrated circuit.
    :ivar txtOperatingLife: enter and display the operating life of the
                            integrated circuit.
    :ivar txtThetaJC: enter and display the junction - case thermal resistance
                      of the integrated circuit.
    :ivar txtVoltageESD: enter and display the ESD threshold voltage of the
                         VLSI.
    :ivar txtYearsProduction: enter and display the number of years the
                              integrated circuit type has been in production.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | cmbQuality - `changed`                    |
    +----------+-------------------------------------------+
    |     1    | cmbApplication - `changed`                |
    +----------+-------------------------------------------+
    |     2    | cmbConstruction - `changed`               |
    +----------+-------------------------------------------+
    |     3    | cmbECC - `changed`                        |
    +----------+-------------------------------------------+
    |     4    | cmbManufacturing - `changed`              |
    +----------+-------------------------------------------+
    |     5    | cmbPackage - `changed`                    |
    +----------+-------------------------------------------+
    |     6    | cmbTechnology - `changed`                 |
    +----------+-------------------------------------------+
    |     7    | cmbType - `changed`                       |
    +----------+-------------------------------------------+
    |     8    | txtArea - `changed`                       |
    +----------+-------------------------------------------+
    |     9    | txtFeatureSize - `changed`                |
    +----------+-------------------------------------------+
    |    10    | txtNActivePins - `changed`                |
    +----------+-------------------------------------------+
    |    11    | txtNCycles - `changed`                    |
    +----------+-------------------------------------------+
    |    12    | txtNElements - `changed`                  |
    +----------+-------------------------------------------+
    |    13    | txtOperatingLife - `changed`              |
    +----------+-------------------------------------------+
    |    14    | txtThetaJC - `changed`                    |
    +----------+-------------------------------------------+
    |    15    | txtVoltageESD - `changed`                 |
    +----------+-------------------------------------------+
    |    16    | txtYearsInProduction - `changed`          |
    +----------+-------------------------------------------+
    """

    # Define private dict attributes.
    _dic_technology = {
        1: [["MOS"], [_(u"Bipolar")]],
        2: [["TTL"], ["ASTTL"], ["CML"], ["HTTL"], ["FTTL"], ["DTL"], ["ECL"],
            ["ALSTTL"], ["FLTTL"], ["STTL"], ["BiCMOS"], ["LSTTL"], ["III"],
            ["IIIL"], ["ISL"]],
        3: [["MOS"], [_(u"Bipolar")]],
        4: [["MOS"], [_(u"Bipolar")]],
        5: [["MOS"], [_(u"Bipolar")]],
        6: [["MOS"], [_(u"Bipolar")]],
        7: [["MOS"], [_(u"Bipolar")]],
        8: [["MOS"], [_(u"Bipolar")]],
        9: [["MMIC"], [_(u"Digital")]]
    }

    _dic_types = {
        9: [["MMIC"], [_(u"Digital")]],
        10: [[_(u"Logic and Custom")], [_(u"Gate Array")]]
    }

    # Define private list attributes.
    _lst_labels = [
        _(u"Quality Level:"),
        _(u"Package:"),
        _(u"Die Area:"),
        _(u"N Elements:"),
        _(u"\u0398<sub>JC</sub>:"),
        _(u"Active Pins:"),
        _(u"Technology:"),
        _(u"Years in Production:"),
        _(u"Construction"),
        _(u"Programming Cycles:"),
        _(u"Operating Life:"),
        _(u"Error Correction Code:"),
        _(u"Application:"),
        _(u"Device Type:"),
        _(u"Feature Size:"),
        _(u"Manufacturing Process:"),
        _(u"ESD Threshold Voltage:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Integrated Circuit assessment input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.IntegratedCircuitDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                integrated circuit.
        :param int subcategory_id: the ID of the integrated circuit
                                   subcategory.
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
            tooltip=_(u"The quality level of the integrated circuit."))
        self.cmbApplication = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The application of the integrated circuit."))
        self.cmbConstruction = rtk.RTKComboBox(
            index=0,
            simple=False,
            tooltip=_(u"The integrated circuit method "
                      u"of construction."))
        self.cmbECC = rtk.RTKComboBox(
            index=0,
            simple=False,
            tooltip=_(u"The error correction code used by the EEPROM."))
        self.cmbManufacturing = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The manufacturing process for the VLSI device."))
        self.cmbPackage = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The method of construction of the integrated "
                      u"circuit."))
        self.cmbTechnology = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The technology used to construct the integrated "
                      u"circuit."))
        self.cmbType = rtk.RTKComboBox(
            index=0,
            simple=True,
            tooltip=_(u"The type of GaAs or VLSI device."))

        self.txtArea = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The die area (in mil<sup>2</sup>) of the integrated "
                      u"circuit."))
        self.txtFeatureSize = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The feature size (in microns) of the VLSI device."))
        self.txtNActivePins = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of active pins on the integrated circuit."))
        self.txtNCycles = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The total number of programming cycles over the "
                      u"EEPROM life."))
        self.txtNElements = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of active elements in the integrated "
                      u"circuit."))
        self.txtOperatingLife = rtk.RTKEntry(
            width=125, tooltip=_(u"The system lifetime operating hours."))
        self.txtThetaJC = rtk.RTKEntry(
            width=125, tooltip=_(u"The junction to case thermal resistance."))
        self.txtVoltageESD = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The ESD susceptibility threshold voltage of the VLSI "
                      u"device."))
        self.txtYearsInProduction = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The number of years the generic device type has been "
                      u"in production."))

        self._make_assessment_input_page()
        self.show_all()

        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbECC.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbManufacturing.connect('changed', self._on_combo_changed,
                                          4))
        self._lst_handler_id.append(
            self.cmbPackage.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbTechnology.connect('changed', self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 7))

        self._lst_handler_id.append(
            self.txtArea.connect('changed', self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtFeatureSize.connect('changed', self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.txtNActivePins.connect('changed', self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtNCycles.connect('changed', self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtOperatingLife.connect('changed', self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtThetaJC.connect('changed', self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtVoltageESD.connect('changed', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtYearsInProduction.connect('changed', self._on_focus_out,
                                              16))

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the integrated circuit RKTComboBox()s.

        :param int subcategory_id: the newly selected integrated circuit
                                   subcategory ID.
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

        self.cmbQuality.do_load_combo([[_(u"Class S")], [_(u"Class B")],
                                       [_(u"Class B-1")]])

        # Load the application RTKComboBox().
        _model = self.cmbApplication.get_model()
        _model.clear()

        if _attributes['construction_id'] == 1:
            self.cmbApplication.do_load_combo(
                [[_(u"Low Noise and Low Power (\u2264 100mW)")],
                 [_(u"Driver and High Power (> 100mW)")], [_(u"Unknown")]])
        else:
            self.cmbApplication.do_load_combo(
                [[_(u"All digital devices")]])

        # Load the Construction RTKComboBox().
        _model = self.cmbConstruction.get_model()
        _model.clear()

        self.cmbConstruction.do_load_combo([["FLOTOX"], [_(u"Textured Poly")]])

        # Load the error correction code RTKComboBox().
        _model = self.cmbECC.get_model()
        _model.clear()

        self.cmbECC.do_load_combo(
            [[_(u"No on-chip ECC")], [_(u"On-chip Hamming code")],
             [_(u"Two-Needs-One redundant cell approach")]])

        # Load the manufacturing process RTKComboBox().
        _model = self.cmbManufacturing.get_model()
        _model.clear()

        self.cmbManufacturing.do_load_combo([["QML or QPL"],
                                             ["Non-QML or non-QPL"]])

        # Load the package RTKComboBox().
        _model = self.cmbPackage.get_model()
        _model.clear()

        self.cmbPackage.do_load_combo([[
            _(u"Hermetic DIP w/ Solder or Weld Seal")
        ], [_(u"Hermetic Pin Grid Array (PGA)")], [
            _(u"Hermetic SMT (Leaded and Nonleaded)")
        ], [_(u"DIP w/ Glass Seal")], [_(u"Flatpacks w/ Axial Leads")], [
            "Can"
        ], [_(u"Nonhermetic DIP")], [_(u"Nonhermetic Pin Grid Array (PGA)")],
                                       [_(u"Nonhermetic SMT")]])

        # Load the technology RTKComboBox().
        _model = self.cmbTechnology.get_model()
        _model.clear()

        try:
            if _attributes['hazard_rate_method_id'] == 1:
                if _attributes['subcategory_id'] == 9:
                    _data = [["MMIC"], [_(u"Digital")]]
                else:
                    _data = [["Bipolar"], ["MOS"]]
            else:
                _data = self._dic_technology[_attributes['subcategory_id']]
        except KeyError:
            _data = []
        self.cmbTechnology.do_load_combo(_data)

        # Load the device type RTKComboBox().
        _model = self.cmbType.get_model()
        _model.clear()

        try:
            _data = self._dic_types[_attributes['subcategory_id']]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected integrated circuit.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.cmbQuality.set_sensitive(True)
        self.cmbApplication.set_sensitive(False)
        self.cmbConstruction.set_sensitive(False)
        self.cmbECC.set_sensitive(False)
        self.cmbManufacturing.set_sensitive(False)
        self.cmbPackage.set_sensitive(False)
        self.cmbTechnology.set_sensitive(False)
        self.cmbType.set_sensitive(False)

        self.txtArea.set_sensitive(False)
        self.txtFeatureSize.set_sensitive(False)
        self.txtNActivePins.set_sensitive(False)
        self.txtNCycles.set_sensitive(False)
        self.txtNElements.set_sensitive(False)
        self.txtOperatingLife.set_sensitive(False)
        self.txtThetaJC.set_sensitive(False)
        self.txtVoltageESD.set_sensitive(False)
        self.txtYearsInProduction.set_sensitive(False)

        if _attributes['subcategory_id'] == 10:
            self.cmbManufacturing.set_sensitive(True)
            self.cmbType.set_sensitive(True)
            self.txtArea.set_sensitive(True)
            self.txtFeatureSize.set_sensitive(True)
            self.txtNActivePins.set_sensitive(False)
            self.txtVoltageESD.set_sensitive(True)

        if _attributes['hazard_rate_method_id'] == 1:
            if _attributes['subcategory_id'] in [1, 2, 3, 4, 5, 8, 9]:
                self.cmbTechnology.set_sensitive(True)
                self.txtNElements.set_sensitive(True)
            if _attributes['subcategory_id'] in [6, 7]:
                _attributes['technology_id'] = 2
                self.txtNElements.set_sensitive(True)
        else:
            self.cmbPackage.set_sensitive(True)
            self.txtArea.set_sensitive(True)
            self.txtNElements.set_sensitive(True)
            self.txtThetaJC.set_sensitive(True)

            if _attributes['subcategory_id'] in [1, 2, 3, 4]:
                self.cmbTechnology.set_sensitive(True)
                self.txtNActivePins.set_sensitive(True)
                self.txtYearsInProduction.set_sensitive(True)
            elif _attributes['subcategory_id'] in [5, 7, 8]:
                self.cmbTechnology.set_sensitive(True)
            elif _attributes['subcategory_id'] == 6:
                self.cmbConstruction.set_sensitive(True)
                self.cmbECC.set_sensitive(True)
                self.cmbTechnology.set_sensitive(True)
                self.txtNActivePins.set_sensitive(True)
                self.txtNCycles.set_sensitive(True)
                self.txtOperatingLife.set_sensitive(True)
            elif _attributes['subcategory_id'] == 9:
                self.cmbApplication.set_sensitive(True)
                self.cmbType.set_sensitive(True)
                self.txtNActivePins.set_sensitive(True)
                self.txtYearsInProduction.set_sensitive(True)

        return _return

    def _make_assessment_input_page(self):
        """
        Make the integrated circuit class gtk.Notebook() assessment input page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Load the gtk.ComboBox() widgets.
        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for integrated circuits.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.cmbQuality, _x_pos, _y_pos[0])
        self.put(self.cmbPackage, _x_pos, _y_pos[1])
        self.put(self.txtArea, _x_pos, _y_pos[2])
        self.put(self.txtNElements, _x_pos, _y_pos[3])
        self.put(self.txtThetaJC, _x_pos, _y_pos[4])
        self.put(self.txtNActivePins, _x_pos, _y_pos[5])
        self.put(self.cmbTechnology, _x_pos, _y_pos[6])
        self.put(self.txtYearsInProduction, _x_pos, _y_pos[7])
        self.put(self.cmbConstruction, _x_pos, _y_pos[8])
        self.put(self.txtNCycles, _x_pos, _y_pos[9])
        self.put(self.txtOperatingLife, _x_pos, _y_pos[10])
        self.put(self.cmbECC, _x_pos, _y_pos[11])
        self.put(self.cmbApplication, _x_pos, _y_pos[12])
        self.put(self.cmbType, _x_pos, _y_pos[13])
        self.put(self.txtFeatureSize, _x_pos, _y_pos[14])
        self.put(self.cmbManufacturing, _x_pos, _y_pos[15])
        self.put(self.txtVoltageESD, _x_pos, _y_pos[16])

        self.show_all()

        return None

    def _on_combo_changed(self, combo, index):
        """
        Retrieve RTKCombo() changes and assign to Integrated Circuit attribute.

        This method is called by:

            * gtk.Combo() 'changed' signal

        :param combo: the RTKCombo() that called this method.
        :type combo: :class:`rtk.gui.gtk.rtk.RTKCombo`
        :param int index: the position in the signal handler list associated
                          with the calling RTKComboBox().  Indices are:

            +---------+------------------+---------+------------------+
            |  Index  | Widget           |  Index  | Widget           |
            +=========+==================+=========+==================+
            |    0    | cmbQuality       |    4    | cmbManufacturing |
            +---------+------------------+---------+------------------+
            |    1    | cmbApplication   |    5    | cmbPackage       |
            +---------+------------------+---------+------------------+
            |    2    | cmbConstruction  |    6    | cmbTechnology    |
            +---------+------------------+---------+------------------+
            |    3    | cmbECC           |    7    | cmbType          |
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
                _attributes['type_id'] = int(combo.get_active())
            elif index == 4:
                _attributes['manufacturing_id'] = int(combo.get_active())
            elif index == 5:
                _attributes['package_id'] = int(combo.get_active())
            elif index == 6:
                _attributes['technology_id'] = int(combo.get_active())
            elif index == 7:
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
        :param int index: the position in the integrated circuit class
                          gtk.TreeModel() associated with the data from the
                          calling gtk.Widget().  Indices are:

            +---------+--------------------+---------+----------------------+
            |  Index  | Widget             |  Index  | Widget               |
            +=========+====================+=========+======================+
            |    8    | txtArea            |    13   | txtOperatingLife     |
            +---------+--------------------+---------+----------------------+
            |    9    | txtFeatureSize     |    14   | txtThetaJC           |
            +---------+--------------------+---------+----------------------+
            |   10    | txtNActivePins     |    15   | txtVoltageESD        |
            +---------+--------------------+---------+----------------------+
            |   11    | txtNCycles         |    16   | txtYearsInProduction |
            +---------+--------------------+---------+----------------------+
            |   12    | txtNElements       |         |                      |
            +---------+--------------------+---------+----------------------+

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

            if index == 8:
                _attributes['area'] = _text
            elif index == 9:
                _attributes['feature_size'] = _text
            elif index == 10:
                _attributes['n_active_pins'] = int(_text)
            elif index == 11:
                _attributes['n_cycles'] = int(_text)
            elif index == 12:
                _attributes['n_elements'] = int(_text)
            elif index == 13:
                _attributes['operating_life'] = _text
            elif index == 14:
                _attributes['theta_jc'] = _text
            elif index == 15:
                _attributes['voltage_esd'] = _text
            elif index == 16:
                _attributes['years_in_production'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the integrated circuit assessment input work view widgets.

        :param int module_id: the integrated circuit ID of the selected/edited
                              integrated circuit.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        #self._subcategory_id = _attributes['subcategory_id']

        self.cmbQuality.handler_block(self._lst_handler_id[0])
        self.cmbQuality.set_active(_attributes['quality_id'])
        self.cmbQuality.handler_unblock(self._lst_handler_id[0])

        self._do_set_sensitive()

        if self._subcategory_id == 10:
            self.cmbManufacturing.handler_block(self._lst_handler_id[4])
            self.cmbManufacturing.set_active(
                _attributes['manufacturing_id'])
            self.cmbManufacturing.handler_unblock(self._lst_handler_id[4])

            self.cmbType.handler_block(self._lst_handler_id[7])
            self.cmbType.set_active(_attributes['type_id'])
            self.cmbType.handler_unblock(self._lst_handler_id[7])

            self.txtArea.handler_block(self._lst_handler_id[8])
            self.txtArea.set_text(str(self.fmt.format(_attributes['area'])))
            self.txtArea.handler_unblock(self._lst_handler_id[8])

            self.txtFeatureSize.handler_block(self._lst_handler_id[9])
            self.txtFeatureSize.set_text(
                str(self.fmt.format(_attributes['feature_size'])))
            self.txtFeatureSize.handler_unblock(self._lst_handler_id[9])

            self.txtVoltageESD.handler_block(self._lst_handler_id[15])
            self.txtVoltageESD.set_text(
                str(self.fmt.format(_attributes['voltage_esd'])))
            self.txtVoltageESD.handler_unblock(self._lst_handler_id[15])

        if _attributes['hazard_rate_method_id'] == 1:
            self.txtNElements.handler_block(self._lst_handler_id[12])
            self.txtNElements.set_text(str(_attributes['n_elements']))
            self.txtNElements.handler_unblock(self._lst_handler_id[12])

            if self._subcategory_id in [1, 2, 3, 4, 5, 8]:
                self.cmbTechnology.handler_block(self._lst_handler_id[6])
                self.cmbTechnology.set_active(_attributes['technology_id'])
                self.cmbTechnology.handler_unblock(self._lst_handler_id[6])

        elif _attributes['hazard_rate_method_id'] == 2:
            self.cmbPackage.handler_block(self._lst_handler_id[5])
            self.cmbPackage.set_active(_attributes['package_id'])
            self.cmbPackage.handler_unblock(self._lst_handler_id[5])

            self.txtArea.handler_block(self._lst_handler_id[8])
            self.txtArea.set_text(str(self.fmt.format(_attributes['area'])))
            self.txtArea.handler_unblock(self._lst_handler_id[8])

            self.txtNElements.handler_block(self._lst_handler_id[12])
            self.txtNElements.set_text(str(_attributes['n_elements']))
            self.txtNElements.handler_unblock(self._lst_handler_id[12])

            self.txtThetaJC.handler_block(self._lst_handler_id[14])
            self.txtThetaJC.set_text(
                str(self.fmt.format(_attributes['theta_jc'])))
            self.txtThetaJC.handler_unblock(self._lst_handler_id[14])

            if self._subcategory_id in [1, 2, 3, 4]:
                self.cmbTechnology.handler_block(self._lst_handler_id[6])
                self.cmbTechnology.set_active(_attributes['technology_id'])
                self.cmbTechnology.handler_unblock(self._lst_handler_id[6])

                self.txtNActivePins.handler_block(self._lst_handler_id[10])
                self.txtNActivePins.set_text(str(_attributes['n_active_pins']))
                self.txtNActivePins.handler_unblock(self._lst_handler_id[10])

                self.txtYearsInProduction.handler_block(
                    self._lst_handler_id[16])
                self.txtYearsInProduction.set_text(
                    str(_attributes['years_in_production']))
                self.txtYearsInProduction.handler_unblock(
                    self._lst_handler_id[16])
            elif self._subcategory_id in [5, 7, 8]:
                self.cmbTechnology.handler_block(self._lst_handler_id[6])
                self.cmbTechnology.set_active(_attributes['technology_id'])
                self.cmbTechnology.handler_unblock(self._lst_handler_id[6])
            elif self._subcategory_id == 6:
                self.cmbConstruction.handler_block(self._lst_handler_id[2])
                self.cmbConstruction.set_active(_attributes['construction_id'])
                self.cmbConstruction.handler_unblock(self._lst_handler_id[2])

                self.cmbTechnology.handler_block(self._lst_handler_id[6])
                self.cmbTechnology.set_active(_attributes['technology_id'])
                self.cmbTechnology.handler_unblock(self._lst_handler_id[6])

                self.cmbType.handler_block(self._lst_handler_id[7])
                self.cmbType.set_active(_attributes['type_id'])  # Use for ECC.
                self.cmbType.handler_unblock(self._lst_handler_id[7])

                self.txtNCycles.handler_block(self._lst_handler_id[11])
                self.txtNCycles.set_text(str(_attributes['n_cycles']))
                self.txtNCycles.handler_unblock(self._lst_handler_id[11])

                self.txtOperatingLife.handler_block(self._lst_handler_id[13])
                self.txtOperatingLife.set_text(
                    str(self.fmt.format(_attributes['operating_life'])))
                self.txtOperatingLife.handler_unblock(self._lst_handler_id[13])
            elif self._subcategory_id == 9:
                self.cmbApplication.handler_block(self._lst_handler_id[1])
                self.cmbApplication.set_active(_attributes['application_id'])
                self.cmbApplication.handler_unblock(self._lst_handler_id[1])

                self.cmbType.handler_block(self._lst_handler_id[7])
                self.cmbType.set_active(_attributes['type_id'])
                self.cmbType.handler_unblock(self._lst_handler_id[7])

                self.txtYearsInProduction.handler_block(
                    self._lst_handler_id[16])
                self.txtYearsInProduction.set_text(
                    str(_attributes['years_in_production']))
                self.txtYearsInProduction.handler_unblock(
                    self._lst_handler_id[16])

        return _return


class StressInputs(gtk.Fixed):
    """
    Display IC stress input attribute data in the RTK Work Book.

    The Integrated Circuit stress input view displays all the assessment inputs
    for the selected integrated circuit.  This includes, currently, stress
    inputs for MIL-HDBK-217FN2.  The attributes of a integrated circuit stress
    input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
                            labels.

    :ivar list _lst_handler_id: the list of signal handler IDs for each of the
                                input widgets.

    :ivar _dtc_data_controller: the integrated circuit BoM data controller
                                instance.

    :ivar int _hardware_id: the ID of the integrated circuit item currently
                            being displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the integrated
                               circuit currently being displayed.

    :ivar txtTemperatureCase: enter and display the temperature of the
                              integrated circuit case.
    :ivar txtTemperatureJunction: enter and display the junction temperature of
                                  the integrated circuit.
    :ivar txtTemperatureRatedMin: enter and display the minimum rated
                                  temperature of the integrated circuit.
    :ivar txtTemperatureKnee: enter and display the break temperature beyond
                              which the integrated circuit must be derated.
    :ivar txtTemperatureRatedMax: enter and display the maximum rated
                                  temperature of the integrated circuit.
    :ivar txtCurrentOperating: enter and display the operating current of the
                               integrated circuit.
    :ivar txtCurrentRated: enter and display the rated current of the
                           integrated circuit.
    :ivar txtPowerOperating: enter and display the operating power of the
                             integrated circuit.
    :ivar txtPowerRated: enter and display the rated power of the integrated
                         circuit.
    :ivar txtVoltageRated: enter and display the rated voltage of the
                           integrated circuit.
    :ivar txtVoltageAC: enter and display the operating ac voltage of the
                        integrated circuit.
    :ivar txtVoltageDC: enter and display the operating DC voltage of the
                        integrated circuit.

    Callbacks signals in _lst_handler_id:

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTemperatureCase - `changed`            |
    +----------+-------------------------------------------+
    |     1    | txtTemperatureJunction - `changed`        |
    +----------+-------------------------------------------+
    |     2    | txtTemperatureRatedMin - `changed`        |
    +----------+-------------------------------------------+
    |     3    | txtTemperatureKnee - `changed`            |
    +----------+-------------------------------------------+
    |     4    | txtTemperatureRatedMax - `changed`        |
    +----------+-------------------------------------------+
    |     5    | txtCurrentOperating - `changed`           |
    +----------+-------------------------------------------+
    |     6    | txtCurrentRated - `changed`               |
    +----------+-------------------------------------------+
    |     7    | txtPowerOperating - `changed`             |
    +----------+-------------------------------------------+
    |     8    | txtPowerRated - `changed`                 |
    +----------+-------------------------------------------+
    |     9    | txtVoltageRated - `changed`               |
    +----------+-------------------------------------------+
    |    10    | txtVoltageAC - `changed`                  |
    +----------+-------------------------------------------+
    |    11    | txtVoltageDC - `changed`                  |
    +----------+-------------------------------------------+
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Case Temperature (\u00B0C):"),
        _(u"Junction Temperature (\u00B0C):"),
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
        Initialize an instance of the Integrated Circuit stress input view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.IntegratedCircuitDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                integrated circuit.
        :param int subcategory_id: the ID of the integrated circuit
                                   subcategory.
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

        self.txtTemperatureCase = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The surface temperature (in \u00B0C) of the integrated "
                u"circuit package."))
        self.txtTemperatureJunction = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The worst case temperature (in \u00B0C) of the integrated "
                u"circuit's internal junctions."))
        self.txtTemperatureKnee = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The break temperature (in \u00B0C) of the integrated "
                      u"circuit beyond which it must be derated."))
        self.txtTemperatureRatedMin = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The minimum rated temperature (in \u00B0C) of the "
                      u"integrated circuit."))
        self.txtTemperatureRatedMax = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The maximum rated temperature (in \u00B0C) of the "
                      u"integrated circuit."))
        self.txtCurrentRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated current (in A) of the integreated circuit."))
        self.txtCurrentOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The operating current (in A) of the integreated circuit."))
        self.txtPowerRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated power (in W) of the integrated circuit."))
        self.txtPowerOperating = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The operting power (in W) of the integrated circuit."))
        self.txtVoltageRated = rtk.RTKEntry(
            width=125,
            tooltip=_(u"The rated voltage (in V) of the integrated circuit."))
        self.txtVoltageAC = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The operating ac voltage (in V) of the integrated circuit."))
        self.txtVoltageDC = rtk.RTKEntry(
            width=125,
            tooltip=_(
                u"The operating DC voltage (in V) of the integrated circuit."))

        self._lst_handler_id.append(
            self.txtTemperatureCase.connect('changed', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtTemperatureJunction.connect('changed', self._on_focus_out,
                                                1))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMin.connect('changed', self._on_focus_out,
                                                2))
        self._lst_handler_id.append(
            self.txtTemperatureKnee.connect('changed', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.txtTemperatureRatedMax.connect('changed', self._on_focus_out,
                                                4))
        self._lst_handler_id.append(
            self.txtCurrentOperating.connect('changed', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtCurrentRated.connect('changed', self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtPowerOperating.connect('changed', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtPowerRated.connect('changed', self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtVoltageRated.connect('changed', self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.txtVoltageAC.connect('changed', self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtVoltageDC.connect('changed', self._on_focus_out, 11))

        self._make_stress_input_page()
        self.show_all()

    def _make_stress_input_page(self):
        """
        Make the integrated circuit module stress input container.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        # Build the container for integrated circuits.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 5)
        _x_pos += 50

        self.put(self.txtTemperatureCase, _x_pos, _y_pos[0])
        self.put(self.txtTemperatureJunction, _x_pos, _y_pos[1])
        self.put(self.txtTemperatureRatedMin, _x_pos, _y_pos[2])
        self.put(self.txtTemperatureKnee, _x_pos, _y_pos[3])
        self.put(self.txtTemperatureRatedMax, _x_pos, _y_pos[4])
        self.put(self.txtCurrentRated, _x_pos, _y_pos[5])
        self.put(self.txtCurrentOperating, _x_pos, _y_pos[6])
        self.put(self.txtPowerRated, _x_pos, _y_pos[7])
        self.put(self.txtPowerOperating, _x_pos, _y_pos[8])
        self.put(self.txtVoltageRated, _x_pos, _y_pos[9])
        self.put(self.txtVoltageAC, _x_pos, _y_pos[10])
        self.put(self.txtVoltageDC, _x_pos, _y_pos[11])

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
        :param int index: the position in the signal handler ID list associated
                          with the RTKEntry() calling this method.  Indices
                          are:

            +---------+------------------------+---------+-------------------+
            |  Index  | Widget                 |  Index  | Widget            |
            +=========+========================+=========+===================+
            |    0    | txtTemperatureCase     |    6    | txtCurrentRated   |
            +---------+------------------------+---------+-------------------+
            |    1    | txtTemperatureJunction |    7    | txtPowerOperating |
            +---------+------------------------+---------+-------------------+
            |    2    | txtTemperatureRatedMin |    8    | txtPowerRated     |
            +---------+------------------------+---------+-------------------+
            |    3    | txtTemperatureKnee     |    8    | txtVoltageRated   |
            +---------+------------------------+---------+-------------------+
            |    4    | txtTemperatureRatedMax |   10    | txtVoltageAC      |
            +---------+------------------------+---------+-------------------+
            |    5    | txtCurrentOperating    |   11    | txtVoltageDC      |
            +---------+------------------------+---------+-------------------+

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
                _attributes['temperature_case'] = _text
            elif index == 1:
                _attributes['temperature_junction'] = _text
            elif index == 2:
                _attributes['temperature_rated_min'] = _text
            elif index == 3:
                _attributes['temperature_knee'] = _text
            elif index == 4:
                _attributes['temperature_rated_max'] = _text
            elif index == 5:
                _attributes['current_operating'] = _text
            elif index == 6:
                _attributes['current_rated'] = _text
            elif index == 7:
                _attributes['power_operating'] = _text
            elif index == 8:
                _attributes['power_rated'] = _text
            elif index == 9:
                _attributes['voltage_rated'] = _text
            elif index == 10:
                _attributes['voltage_ac_operating'] = _text
            elif index == 11:
                _attributes['voltage_dc_operating'] = _text

            self._dtc_data_controller.request_set_attributes(
                self._hardware_id, _attributes)

        entry.handler_unblock(self._lst_handler_id[index])

        return _return

    def on_select(self, module_id=None):
        """
        Load the integrated circuit stress input work view widgets.

        :param int module_id: the integrated circuit ID of the selected/edited
                              integrated circuit.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtTemperatureCase.handler_block(self._lst_handler_id[0])
        self.txtTemperatureCase.set_text(
            str(self.fmt.format(_attributes['temperature_case'])))
        self.txtTemperatureCase.handler_unblock(self._lst_handler_id[0])

        self.txtTemperatureJunction.handler_block(self._lst_handler_id[1])
        self.txtTemperatureJunction.set_text(
            str(self.fmt.format(_attributes['temperature_junction'])))
        self.txtTemperatureJunction.handler_unblock(self._lst_handler_id[1])

        self.txtTemperatureRatedMin.handler_block(self._lst_handler_id[2])
        self.txtTemperatureRatedMin.set_text(
            str(self.fmt.format(_attributes['temperature_rated_min'])))
        self.txtTemperatureRatedMin.handler_unblock(self._lst_handler_id[2])

        self.txtTemperatureKnee.handler_block(self._lst_handler_id[3])
        self.txtTemperatureKnee.set_text(
            str(self.fmt.format(_attributes['temperature_knee'])))
        self.txtTemperatureKnee.handler_unblock(self._lst_handler_id[3])

        self.txtTemperatureRatedMax.handler_block(self._lst_handler_id[4])
        self.txtTemperatureRatedMax.set_text(
            str(self.fmt.format(_attributes['temperature_rated_max'])))
        self.txtTemperatureRatedMax.handler_unblock(self._lst_handler_id[4])

        self.txtCurrentRated.handler_block(self._lst_handler_id[6])
        self.txtCurrentRated.set_text(
            str(self.fmt.format(_attributes['current_rated'])))
        self.txtCurrentRated.handler_unblock(self._lst_handler_id[6])

        self.txtCurrentOperating.handler_block(self._lst_handler_id[5])
        self.txtCurrentOperating.set_text(
            str(self.fmt.format(_attributes['current_operating'])))
        self.txtCurrentOperating.handler_unblock(self._lst_handler_id[5])

        self.txtPowerRated.handler_block(self._lst_handler_id[8])
        self.txtPowerRated.set_text(
            str(self.fmt.format(_attributes['power_rated'])))
        self.txtPowerRated.handler_unblock(self._lst_handler_id[8])

        self.txtPowerOperating.handler_block(self._lst_handler_id[7])
        self.txtPowerOperating.set_text(
            str(self.fmt.format(_attributes['power_operating'])))
        self.txtPowerOperating.handler_unblock(self._lst_handler_id[7])

        self.txtVoltageRated.handler_block(self._lst_handler_id[9])
        self.txtVoltageRated.set_text(
            str(self.fmt.format(_attributes['voltage_rated'])))
        self.txtVoltageRated.handler_unblock(self._lst_handler_id[9])

        self.txtVoltageAC.handler_block(self._lst_handler_id[10])
        self.txtVoltageAC.set_text(
            str(self.fmt.format(_attributes['voltage_ac_operating'])))
        self.txtVoltageAC.handler_unblock(self._lst_handler_id[10])

        self.txtVoltageDC.handler_block(self._lst_handler_id[11])
        self.txtVoltageDC.set_text(
            str(self.fmt.format(_attributes['voltage_dc_operating'])))
        self.txtVoltageDC.handler_unblock(self._lst_handler_id[11])

        return _return


class AssessmentResults(gtk.Fixed):
    """
    Display IC assessment results attribute data in the RTK Work Book.

    The integrated circuit assessment result view displays all the assessment
    results for the selected integrated circuit.  This includes, currently,
    results for MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress
    methods.  The attributes of a integrated circuit assessment result view
    are:

    :cvar list _lst_labels: the text to use for the assessment results widget
                            labels.

    :ivar int _hardware_id: the ID of the integrated circuit item currently
                            being displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the integrated
                               circuit currently being displayed.
    :ivar _lblModel: the :class:`rtk.gui.gtk.rtk.Label.RTKLabel` to display
                     the failure rate mathematical model used.

    :ivar txtC1: displays the die complexity hazard rate of the integrated
                 circuit.
    :ivar txtPiT: displays the temperature factor for the integrated circuit.
    :ivar txtC2: displays the package failure rate for the integrated circuit.
    :ivar txtPiE: displays the environment factor for the integrated circuit.
    :ivar txtPiQ: displays the quality factor for the integrated circuit.
    :ivar txtPiL: displays the learning factor for the integrated circuit.
    :ivar txtLambdaCYC: displays the read/write cycling induced hazard rate for
                        the EEPROM.
    :ivar txtLambdaBD: displays the die base hazard rate for the VLSI device.
    :ivar txtPiMFG: displays the manufacturing process correction factor for
                    VLSI device.
    :ivar txtPiCD: displays the die complexity correction factor for the VLSI
                   device.
    :ivar txtLambdaBP: displays the package base hazard rate for the VLSI
                       device.
    :ivar txtPiPT: displays the package type correction factor for the VLSI
                   device.
    :ivar txtLambdaEOS: displays the electrical overstress hazard rate for the
                        VLSI device.
    :ivar txtPiA: displays the application factor for the integrated circuit.
    """

    # Define private dict attributes.
    _dic_part_stress = {
        1:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        2:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        3:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        4:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        5:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        6:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        7:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        8:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        9:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>L</sub>\u03C0<sub>Q</sub></span>",
        10:
        u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>BD</sub>\u03C0<sub>MFG</sub>\u03C0<sub>T</sub>\u03C0<sub>CD</sub> + \u03BB<sub>BP</sub>\u03C0<sub>E</sub>\u03C0<sub>Q</sub>\u03C0<sub>PT</sub> + \u03BB<sub>EOS</sub></span>"
    }

    # Define private list attributes.
    _lst_labels = [
        u"", u"C1:", u"\u03C0<sub>T</sub>:", u"C2:", u"\u03C0<sub>E</sub>:",
        u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>L</sub>:",
        u"\u03BB<sub>CYC</sub>:", u"\u03BB<sub>BD</sub>",
        u"\u03C0<sub>MFG</sub>", u"\u03C0<sub>CD</sub>",
        u"\u03BB<sub>BP</sub>", u"\u03C0<sub>PT</sub>",
        u"\u03BB<sub>EOS</sub>", u"\u03C0<sub>A</sub>"
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Integrated Circuit assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.IntegratedCircuitBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                integrated circuit.
        :param int subcategory_id: the ID of the integrated circuit subcategory.
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
            width=-1,
            tooltip=_(u"The assessment model used to calculate the integrated "
                      u"circuit failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.txtLambdaB = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The base hazard rate for the integrated circuit."))
        self.txtC1 = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The die complexity hazard rate of the integrated "
                      u"circuit."))
        self.txtPiT = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The temperature factor for the integrated circuit."))
        self.txtC2 = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The package hazard rate for the integrated circuit."))
        self.txtPiC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The construction factor for the integrated circuit."))
        self.txtPiE = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The environment factor for the integrated circuit."))
        self.txtPiQ = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The quality factor for the integrated circuit."))
        self.txtPiL = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The learning factor for the integrated circuit."))
        self.txtLambdaCYC = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The read/write cycling induced hazard rate for the "
                      u"EEPROM."))
        self.txtLambdaBD = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The die base hazard rate for the VLSI device."))
        self.txtPiMFG = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The manufacturing process correction factor for the "
                      u"VLSI device."))
        self.txtPiCD = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The die complexity correction factor for the VLSI "
                      u"device."))
        self.txtLambdaBP = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The package base hazard rate for the VLSI device."))
        self.txtPiPT = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The package type correction factor for the VLSI "
                      u"device."))
        self.txtLambdaEOS = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The electrical overstress hazard rate for the VLSI "
                      u"device."))
        self.txtPiA = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The application correction factor for the GaAs "
                      u"device."))

        self._make_assessment_results_page()
        self.show_all()

        pub.subscribe(self._do_load_page, 'calculatedHardware')

    def _do_load_page(self):
        """
        Load the integrated circuit assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_text(str(self.fmt.format(_attributes['lambda_b'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtC1.set_text(str(self.fmt.format(_attributes['C1'])))
        self.txtPiT.set_text(str(self.fmt.format(_attributes['piT'])))
        self.txtC2.set_text(str(self.fmt.format(_attributes['C2'])))
        self.txtPiE.set_text(str(self.fmt.format(_attributes['piE'])))
        self.txtPiQ.set_text(str(self.fmt.format(_attributes['piQ'])))
        self.txtPiL.set_text(str(self.fmt.format(_attributes['piL'])))
        self.txtLambdaCYC.set_text(
            str(self.fmt.format(_attributes['lambdaCYC'])))
        self.txtLambdaBD.set_text(
            str(self.fmt.format(_attributes['lambdaBD'])))
        self.txtPiMFG.set_text(str(self.fmt.format(_attributes['piMFG'])))
        self.txtPiCD.set_text(str(self.fmt.format(_attributes['piCD'])))
        self.txtLambdaBP.set_text(
            str(self.fmt.format(_attributes['lambdaBP'])))
        self.txtPiPT.set_text(str(self.fmt.format(_attributes['piPT'])))
        self.txtLambdaEOS.set_text(
            str(self.fmt.format(_attributes['lambdaEOS'])))
        self.txtPiA.set_text(str(self.fmt.format(_attributes['piA'])))

        return _return

    def _do_set_sensitive(self):
        """
        Set widget sensitivity as needed for the selected integrated circuit.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtLambdaB.set_sensitive(False)
        self.txtLambdaB.set_visible(True)
        self.txtC1.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtC2.set_sensitive(False)
        self.txtPiE.set_sensitive(False)
        self.txtPiL.set_sensitive(False)
        self.txtLambdaCYC.set_sensitive(False)
        self.txtLambdaBD.set_sensitive(False)
        self.txtPiMFG.set_sensitive(False)
        self.txtPiCD.set_sensitive(False)
        self.txtLambdaBP.set_sensitive(False)
        self.txtPiPT.set_sensitive(False)
        self.txtLambdaEOS.set_sensitive(False)
        self.txtPiA.set_sensitive(False)

        if _attributes['subcategory_id'] == 10:
            self.txtLambdaB.set_sensitive(False)
            self.txtLambdaB.set_visible(False)
            self.txtLambdaBD.set_sensitive(True)
            self.txtPiMFG.set_sensitive(True)
            self.txtPiCD.set_sensitive(True)
            self.txtLambdaBP.set_sensitive(True)
            self.txtPiPT.set_sensitive(True)
            self.txtLambdaEOS.set_sensitive(True)
            self.txtPiE.set_sensitive(True)

        if _attributes['hazard_rate_method_id'] == 1:
            self.txtLambdaB.set_sensitive(True)
        else:
            self.txtPiT.set_sensitive(True)
            self.txtPiE.set_sensitive(True)
            self.txtPiQ.set_sensitive(True)

            if _attributes['subcategory_id'] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                self.txtC1.set_sensitive(True)
                self.txtC2.set_sensitive(True)
                self.txtPiL.set_sensitive(True)

            if _attributes['subcategory_id'] in [5, 6, 7, 8]:
                self.txtLambdaCYC.set_sensitive(True)

            if _attributes['subcategory_id'] == 9:
                self.txtPiA.set_sensitive(True)

        return _return

    def _make_assessment_results_page(self):
        """
        Make the integrated circuit gtk.Notebook() assessment results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        if _attributes['hazard_rate_method_id'] == 1:
            if self._subcategory_id == 10:
                self._lblModel.set_markup(
                    self._dic_part_stress[self._subcategory_id])
            else:
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

        self._do_set_sensitive()

        # Build the container for integrated circuits.
        _x_pos, _y_pos = rtk.make_label_group(self._lst_labels, self, 5, 35)
        _x_pos += 50

        self.put(self._lblModel, _x_pos, 5)
        self.put(self.txtLambdaB, _x_pos, _y_pos[0])
        self.put(self.txtC1, _x_pos, _y_pos[1])
        self.put(self.txtPiT, _x_pos, _y_pos[2])
        self.put(self.txtC2, _x_pos, _y_pos[3])
        self.put(self.txtPiE, _x_pos, _y_pos[4])
        self.put(self.txtPiQ, _x_pos, _y_pos[5])
        self.put(self.txtPiL, _x_pos, _y_pos[6])
        self.put(self.txtLambdaCYC, _x_pos, _y_pos[7])
        self.put(self.txtLambdaBD, _x_pos, _y_pos[8])
        self.put(self.txtPiMFG, _x_pos, _y_pos[9])
        self.put(self.txtPiCD, _x_pos, _y_pos[10])
        self.put(self.txtLambdaBP, _x_pos, _y_pos[11])
        self.put(self.txtPiPT, _x_pos, _y_pos[12])
        self.put(self.txtLambdaEOS, _x_pos, _y_pos[13])
        self.put(self.txtPiA, _x_pos, _y_pos[14])

        self.show_all()

        return None

    def on_select(self, module_id=None):
        """
        Load the integrated circuit assessment input work view widgets.

        :param int module_id: the integrated circuit ID of the selected/edited
                              integrated circuit.
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
    Display IC stress results attribute data in the RTK Work Book.

    The integrated circuit stress result view displays all the stress results
    for the selected integrated circuit.  This includes, currently, results
    for MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress methods.
    The attributes of an integrated circuit stress result view are:

    :cvar list _lst_labels: the text to use for the sress results widget
                            labels.

    :ivar int _hardware_id: the ID of the integrated circuit item currently
                            being displayed.
    :ivar int _subcategory_id: the ID of the subcategory for the integrated
                               circuit currently being displayed.

    :ivar cmbSpecification: select and display the governing specification of
                            the integrated circuit.
    :ivar cmbStyle: select and display the style of the integrated circuit.
    :ivar cmbConfiguration: select and display the configuration of the
                            integrated circuit.
    :ivar cmbConstruction: select and display the method of construction of the
                           integrated circuit.
    :ivar txtCapacitance: enter and display the capacitance rating of the
                          integrated circuit.
    :ivar txtESR: enter and display the equivalent series resistance.
    """

    # Define private list attributes.
    _lst_labels = [
        _(u"Current Ratio:"),
        _(u"Voltage Ratio:"), "",
        _(u"Overstress Reason:")
    ]

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Integrated Circuit assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.IntegratedCircuitDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                integrated circuit.
        :param int subcategory_id: the ID of the integrated circuit
                                   subcategory.
        """
        gtk.HPaned.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_derate_criteria = [[0.8, 0.8, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._dtc_data_controller = controller
        self._hardware_id = hardware_id
        self._subcategory_id = subcategory_id

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.fmt = None

        self.pltDerate = rtk.RTKPlot()

        self.chkOverstress = rtk.RTKCheckButton(
            label=_(u"Overstressed"),
            tooltip=_(
                u"Indicates whether or not the selected integrated circuit "
                u"is overstressed."))
        self.txtReason = rtk.RTKTextView(
            gtk.TextBuffer(),
            width=250,
            tooltip=_(u"The reason(s) the selected hardware item is "
                      u"overstressed."))
        self.txtCurrentRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating current to rated current for "
                      u"the integrated circuit."))
        self.txtVoltageRatio = rtk.RTKEntry(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(u"The ratio of operating voltage to rated voltage for "
                      u"the integrated circuit."))

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
            y_values=[_attributes['voltage_ratio']],
            plot_type='scatter',
            marker='go')

        self.pltDerate.do_make_title(
            _(u"Voltage Derating Curve for {0:s} at {1:s}").format(
                _attributes['part_number'], _attributes['ref_des']),
            fontsize=12)
        self.pltDerate.do_make_legend([
            _(u"Harsh Environment"),
            _(u"Mild Environment"),
            _(u"Voltage Operating Point")
        ])

        self.pltDerate.do_make_labels(
            _(u"Temperature (\u2070C)"), 0, -0.2, fontsize=10)
        self.pltDerate.do_make_labels(
            _(u"Voltage Ratio"), -1, 0, set_x=False, fontsize=10)

        self.pltDerate.figure.canvas.draw()

        return _return

    def _do_load_page(self):
        """
        Load the integrated circuit stress results page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtCurrentRatio.set_text(
            str(self.fmt.format(_attributes['current_ratio'])))
        self.txtVoltageRatio.set_text(
            str(self.fmt.format(_attributes['voltage_ratio'])))
        self.chkOverstress.set_active(_attributes['overstress'])
        _textbuffer = self.txtReason.do_get_buffer()
        _textbuffer.set_text(_attributes['reason'])

        self._do_load_derating_curve()

        return _return

    def _make_stress_results_page(self):
        """
        Make the integrated circuit gtk.Notebook() assessment results page.

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
        _fixed.put(self.txtVoltageRatio, _x_pos, _y_pos[1])
        _fixed.put(self.chkOverstress, _x_pos, _y_pos[2])
        _fixed.put(self.txtReason.scrollwindow, _x_pos, _y_pos[3])

        _fixed.show_all()

        # Create the derating plot.
        _frame = rtk.RTKFrame(label=_(u"Derating Curve and Operating Point"))
        _frame.add(self.pltDerate.plot)
        _frame.show_all()

        self.pack2(_frame, True, True)

        return _return

    def on_select(self, module_id=None):
        """
        Load the integrated circuit assessment input work view widgets.

        :param int module_id: the hardware ID of the selected/edited
                              integrated circuit.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._hardware_id = module_id

        self._do_load_page()

        return _return
