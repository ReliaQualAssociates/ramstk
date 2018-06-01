# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.workviews.components.IntegratedCircuit.py is part of the
#       RTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Work View."""

from pubsub import pub

# Import other RTK modules.
from rtk.gui.gtk import rtk
from rtk.gui.gtk.rtk.Widget import _
from rtk.gui.gtk.workviews.components.Component import (AssessmentInputs,
                                                        AssessmentResults)


class ICAssessmentInputs(AssessmentInputs):
    """
    Display IC assessment input attribute data in the RTK Work Book.

    The Integrated Circuit assessment input view displays all the assessment
    inputs for the selected integrated circuit.  This includes, currently,
    inputs for MIL-HDBK-217FN2.  The attributes of an integrated circuit
    assessment input view are:

    :cvar dict _dic_technology: dictionary of integrated circuit package
                                technologies.  Key is integrated circuit
                                subcategory ID; values are lists of
                                technologies.

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

    +-------+-------------------------------------------+
    | Index | Widget - Signal                           |
    +=======+===========================================+
    |   0   | cmbQuality - `changed`                    |
    +-------+-------------------------------------------+
    |   1   | cmbApplication - `changed`                |
    +-------+-------------------------------------------+
    |   2   | cmbConstruction - `changed`               |
    +-------+-------------------------------------------+
    |   3   | cmbECC - `changed`                        |
    +-------+-------------------------------------------+
    |   4   | cmbManufacturing - `changed`              |
    +-------+-------------------------------------------+
    |   5   | cmbPackage - `changed`                    |
    +-------+-------------------------------------------+
    |   6   | cmbTechnology - `changed`                 |
    +-------+-------------------------------------------+
    |   7   | cmbType - `changed`                       |
    +-------+-------------------------------------------+
    |   8   | txtArea - `changed`                       |
    +-------+-------------------------------------------+
    |   9   | txtFeatureSize - `changed`                |
    +-------+-------------------------------------------+
    |  10   | txtNActivePins - `changed`                |
    +-------+-------------------------------------------+
    |  11   | txtNCycles - `changed`                    |
    +-------+-------------------------------------------+
    |  12   | txtNElements - `changed`                  |
    +-------+-------------------------------------------+
    |  13   | txtOperatingLife - `changed`              |
    +-------+-------------------------------------------+
    |  14   | txtThetaJC - `changed`                    |
    +-------+-------------------------------------------+
    |  15   | txtVoltageESD - `changed`                 |
    +-------+-------------------------------------------+
    |  16   | txtYearsInProduction - `changed`          |
    +-------+-------------------------------------------+
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
        AssessmentInputs.__init__(self, controller, hardware_id,
                                  subcategory_id)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(_(u"Package:"))
        self._lst_labels.append(_(u"Die Area:"))
        self._lst_labels.append(_(u"N Elements:"))
        self._lst_labels.append(_(u"\u0398<sub>JC</sub>:"))
        self._lst_labels.append(_(u"Active Pins:"))
        self._lst_labels.append(_(u"Technology:"))
        self._lst_labels.append(_(u"Years in Production:"))
        self._lst_labels.append(_(u"Construction"))
        self._lst_labels.append(_(u"Programming Cycles:"))
        self._lst_labels.append(_(u"Operating Life:"))
        self._lst_labels.append(_(u"Error Correction Code:"))
        self._lst_labels.append(_(u"Application:"))
        self._lst_labels.append(_(u"Device Type:"))
        self._lst_labels.append(_(u"Feature Size:"))
        self._lst_labels.append(_(u"Manufacturing Process:"))
        self._lst_labels.append(_(u"ESD Threshold Voltage:"))

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
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

        _attributes = AssessmentInputs.do_load_comboboxes(self, subcategory_id)

        # Load the quality level RTKComboBox().
        self.cmbQuality.do_load_combo([[_(u"Class S")], [_(u"Class B")],
                                       [_(u"Class B-1")]])

        # Load the application RTKComboBox().
        if _attributes['construction_id'] == 1:
            self.cmbApplication.do_load_combo(
                [[_(u"Low Noise and Low Power (\u2264 100mW)")],
                 [_(u"Driver and High Power (> 100mW)")], [_(u"Unknown")]])
        else:
            self.cmbApplication.do_load_combo([[_(u"All digital devices")]])

        # Load the Construction RTKComboBox().
        self.cmbConstruction.do_load_combo([["FLOTOX"], [_(u"Textured Poly")]])

        # Load the error correction code RTKComboBox().
        self.cmbECC.do_load_combo(
            [[_(u"No on-chip ECC")], [_(u"On-chip Hamming code")],
             [_(u"Two-Needs-One redundant cell approach")]])

        # Load the manufacturing process RTKComboBox().
        self.cmbManufacturing.do_load_combo([["QML or QPL"],
                                             ["Non-QML or non-QPL"]])

        # Load the package RTKComboBox().
        self.cmbPackage.do_load_combo([[
            _(u"Hermetic DIP w/ Solder or Weld Seal")
        ], [_(u"Hermetic Pin Grid Array (PGA)")], [
            _(u"Hermetic SMT (Leaded and Nonleaded)")
        ], [_(u"DIP w/ Glass Seal")], [_(u"Flatpacks w/ Axial Leads")], [
            "Can"
        ], [_(u"Nonhermetic DIP")], [_(u"Nonhermetic Pin Grid Array (PGA)")],
                                       [_(u"Nonhermetic SMT")]])

        # Load the technology RTKComboBox().
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
        self._do_load_comboboxes(self._subcategory_id)
        self._do_set_sensitive()

        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_assessment_input_page(self)

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

            +-------+------------------+-------+------------------+
            | Index | Widget           | Index | Widget           |
            +=======+==================+=======+==================+
            |   1   | cmbApplication   |   5   | cmbPackage       |
            +-------+------------------+-------+------------------+
            |   2   | cmbConstruction  |   6   | cmbTechnology    |
            +-------+------------------+-------+------------------+
            |   3   | cmbECC           |   7   | cmbType          |
            +-------+------------------+-------+------------------+
            |   4   | cmbManufacturing |       |                  |
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

        _attributes = AssessmentInputs.on_select(self, module_id)

        if self._subcategory_id == 10:
            self.cmbManufacturing.handler_block(self._lst_handler_id[4])
            self.cmbManufacturing.set_active(_attributes['manufacturing_id'])
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

        self._do_set_sensitive()

        return _return


class ICAssessmentResults(AssessmentResults):
    """
    Display IC assessment results attribute data in the RTK Work Book.

    The Integrated Circuit assessment result view displays all the assessment
    results for the selected integrated circuit.  This includes, currently,
    results for MIL-HDBK-217FN2 parts count and MIL-HDBK-217FN2 part stress
    methods.  The attributes of a integrated circuit assessment result view
    are:

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

    def __init__(self, controller, hardware_id, subcategory_id):
        """
        Initialize an instance of the Integrated Circuit assessment result view.

        :param controller: the hardware data controller instance.
        :type controller: :class:`rtk.hardware.IntegratedCircuitBoMDataController`
        :param int hardware_id: the hardware ID of the currently selected
                                integrated circuit.
        :param int subcategory_id: the ID of the integrated circuit subcategory.
        """
        AssessmentResults.__init__(self, controller, hardware_id,
                                   subcategory_id)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append(u"C1:")
        self._lst_labels.append(u"\u03C0<sub>T</sub>:")
        self._lst_labels.append(u"C2:")
        self._lst_labels.append(u"\u03C0<sub>L</sub>:")
        self._lst_labels.append(u"\u03BB<sub>CYC</sub>:")
        self._lst_labels.append(u"\u03BB<sub>BD</sub>")
        self._lst_labels.append(u"\u03C0<sub>MFG</sub>")
        self._lst_labels.append(u"\u03C0<sub>CD</sub>")
        self._lst_labels.append(u"\u03BB<sub>BP</sub>")
        self._lst_labels.append(u"\u03C0<sub>PT</sub>")
        self._lst_labels.append(u"\u03BB<sub>EOS</sub>")
        self._lst_labels.append(u"\u03C0<sub>A</sub>")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(u"The assessment model used to calculate the integrated circuit "
              u"failure rate."))

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
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

        _attributes = AssessmentResults.do_load_page(self)

        self.txtC1.set_text(str(self.fmt.format(_attributes['C1'])))
        self.txtPiT.set_text(str(self.fmt.format(_attributes['piT'])))
        self.txtC2.set_text(str(self.fmt.format(_attributes['C2'])))
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
        _return = AssessmentResults.do_set_sensitive(self)
        _attributes = self._dtc_data_controller.request_get_attributes(
            self._hardware_id)

        self.txtC1.set_sensitive(False)
        self.txtPiT.set_sensitive(False)
        self.txtC2.set_sensitive(False)
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
        self._do_set_sensitive()

        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_assessment_results_page(self)

        self.put(self.txtC1, _x_pos, _y_pos[3])
        self.put(self.txtPiT, _x_pos, _y_pos[4])
        self.put(self.txtC2, _x_pos, _y_pos[5])
        self.put(self.txtPiL, _x_pos, _y_pos[6])
        self.put(self.txtLambdaCYC, _x_pos, _y_pos[7])
        self.put(self.txtLambdaBD, _x_pos, _y_pos[8])
        self.put(self.txtPiMFG, _x_pos, _y_pos[9])
        self.put(self.txtPiCD, _x_pos, _y_pos[10])
        self.put(self.txtLambdaBP, _x_pos, _y_pos[11])
        self.put(self.txtPiPT, _x_pos, _y_pos[12])
        self.put(self.txtLambdaEOS, _x_pos, _y_pos[13])
        self.put(self.txtPiA, _x_pos, _y_pos[14])

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
