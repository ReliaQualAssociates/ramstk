# -*- coding: utf-8 -*-
#
#       gui.gtk.workviews.components.IntegratedCircuit.py is part of the
#       RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2018 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import RAMSTKComboBox, RAMSTKEntry
from ramstk.gui.gtk.ramstk.Widget import _

# RAMSTK Local Imports
from .Component import AssessmentInputs, AssessmentResults


class ICAssessmentInputs(AssessmentInputs):
    """
    Display IC assessment input attribute data in the RAMSTK Work Book.

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
    _dic_keys = {
        0: 'quality_id',
        1: 'application_id',
        2: 'construction_id',
        3: 'type_id',
        4: 'manufacturing_id',
        5: 'package_id',
        6: 'technology_id',
        7: 'type_id',
        8: 'area',
        9: 'feature_size',
        10: 'n_active_pins',
        11: 'n_cycles',
        12: 'n_elements',
        13: 'operating_life',
        14: 'theta_jc',
        15: 'voltage_esd',
        16: 'years_in_production',
    }

    _dic_technology = {
        1: [["MOS"], [_("Bipolar")]],
        2: [
            ["TTL"], ["ASTTL"], ["CML"], ["HTTL"], ["FTTL"], ["DTL"], ["ECL"],
            ["ALSTTL"], ["FLTTL"], ["STTL"], ["BiCMOS"], ["LSTTL"], ["III"],
            ["IIIL"], ["ISL"],
        ],
        3: [["MOS"], [_("Bipolar")]],
        4: [["MOS"], [_("Bipolar")]],
        5: [["MOS"], [_("Bipolar")]],
        6: [["MOS"], [_("Bipolar")]],
        7: [["MOS"], [_("Bipolar")]],
        8: [["MOS"], [_("Bipolar")]],
        9: [["MMIC"], [_("Digital")]],
    }

    _dic_types = {
        9: [["MMIC"], [_("Digital")]],
        10: [[_("Logic and Custom")], [_("Gate Array")]],
    }

    # Define private list attributes.
    _lst_labels = [
        _("Quality Level:"),
        _("Package:"),
        _("Die Area:"),
        _("N Elements:"),
        _("\u0398<sub>JC</sub>:"),
        _("Active Pins:"),
        _("Technology:"),
        _("Years in Production:"),
        _("Construction"),
        _("Programming Cycles:"),
        _("Operating Life:"),
        _("Error Correction Code:"),
        _("Application:"),
        _("Device Type:"),
        _("Feature Size:"),
        _("Manufacturing Process:"),
        _("ESD Threshold Voltage:"),
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the IC assessment input view.

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
        self.cmbApplication = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbConstruction = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbECC = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbManufacturing = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbPackage = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbTechnology = RAMSTKComboBox(
            index=0,
            simple=True,
        )
        self.cmbType = RAMSTKComboBox(
            index=0,
            simple=True,
        )

        self.txtArea = RAMSTKEntry()
        self.txtFeatureSize = RAMSTKEntry()
        self.txtNActivePins = RAMSTKEntry()
        self.txtNCycles = RAMSTKEntry()
        self.txtNElements = RAMSTKEntry()
        self.txtOperatingLife = RAMSTKEntry()
        self.txtThetaJC = RAMSTKEntry()
        self.txtVoltageESD = RAMSTKEntry()
        self.txtYearsInProduction = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_comboboxes, 'changed_subcategory')
        pub.subscribe(self._do_load_page, 'loaded_hardware_inputs')

    def __make_ui(self):
        """
        Make the integrated circuit class Gtk.Notebook() assessment input page.

        :return: None
        :rtype: None
        """
        # Build the container for inductors.
        _x_pos, _y_pos = AssessmentInputs.make_ui(self)

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

    def __set_callbacks(self):
        """
        Set callback methods for Integrated Circuit assessment input widgets.

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
            self.cmbECC.connect('changed', self.on_combo_changed, 3),
        )
        self._lst_handler_id.append(
            self.cmbManufacturing.connect(
                'changed', self.on_combo_changed,
                4,
            ),
        )
        self._lst_handler_id.append(
            self.cmbPackage.connect('changed', self.on_combo_changed, 5),
        )
        self._lst_handler_id.append(
            self.cmbTechnology.connect('changed', self.on_combo_changed, 6),
        )
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self.on_combo_changed, 7),
        )

        self._lst_handler_id.append(
            self.txtArea.connect('changed', self.on_focus_out, 8),
        )
        self._lst_handler_id.append(
            self.txtFeatureSize.connect('changed', self.on_focus_out, 9),
        )
        self._lst_handler_id.append(
            self.txtNActivePins.connect('changed', self.on_focus_out, 10),
        )
        self._lst_handler_id.append(
            self.txtNCycles.connect('changed', self.on_focus_out, 11),
        )
        self._lst_handler_id.append(
            self.txtNElements.connect('changed', self.on_focus_out, 12),
        )
        self._lst_handler_id.append(
            self.txtOperatingLife.connect('changed', self.on_focus_out, 13),
        )
        self._lst_handler_id.append(
            self.txtThetaJC.connect('changed', self.on_focus_out, 14),
        )
        self._lst_handler_id.append(
            self.txtVoltageESD.connect('changed', self.on_focus_out, 15),
        )
        self._lst_handler_id.append(
            self.txtYearsInProduction.connect(
                'changed', self.on_focus_out,
                16,
            ),
        )

    def __set_properties(self):
        """
        Set properties for Integrated Circuit assessment input widgets.

        :return: None
        :rtype: None
        """
        self.cmbApplication.do_set_properties(
            tooltip=_("The application of the integrated circuit."),
        )
        self.cmbConstruction.do_set_properties(
            tooltip=_(
                "The integrated circuit method of construction.",
            ),
        )
        self.cmbECC.do_set_properties(
            tooltip=_("The error correction code used by the EEPROM."),
        )
        self.cmbManufacturing.do_set_properties(
            tooltip=_("The manufacturing process for the VLSI device."),
        )
        self.cmbPackage.do_set_properties(
            tooltip=_(
                "The method of construction of the integrated circuit.",
            ),
        )
        self.cmbTechnology.do_set_properties(
            tooltip=_(
                "The technology used to construct the integrated circuit.",
            ),
        )
        self.cmbType.do_set_properties(
            tooltip=_("The type of GaAs or VLSI device."),
        )

        self.txtArea.do_set_properties(
            width=125,
            tooltip=_(
                "The die area (in mil<sup>2</sup>) of the integrated circuit.",
            ),
        )
        self.txtFeatureSize.do_set_properties(
            width=125,
            tooltip=_("The feature size (in microns) of the VLSI device."),
        )
        self.txtNActivePins.do_set_properties(
            width=125,
            tooltip=_("The number of active pins on the integrated circuit."),
        )
        self.txtNCycles.do_set_properties(
            width=125,
            tooltip=_(
                "The total number of programming cycles over the EEPROM life.",
            ),
        )
        self.txtNElements.do_set_properties(
            width=125,
            tooltip=_(
                "The number of active elements in the integrated circuit.",
            ),
        )
        self.txtOperatingLife.do_set_properties(
            width=125, tooltip=_("The system lifetime operating hours."),
        )
        self.txtThetaJC.do_set_properties(
            width=125, tooltip=_("The junction to case thermal resistance."),
        )
        self.txtVoltageESD.do_set_properties(
            width=125,
            tooltip=_(
                "The ESD susceptibility threshold voltage of the VLSI device.",
            ),
        )
        self.txtYearsInProduction.do_set_properties(
            width=125,
            tooltip=_(
                "The number of years the generic device type has been in "
                "production.",
            ),
        )

    def _do_load_comboboxes(self, subcategory_id):
        """
        Load the integrated circuit RKTComboBox()s.

        :param int subcategory_id: the newly selected integrated circuit
        subcategory ID.
        :return: None
        :rtype: None
        """
        # Load the quality level RAMSTKComboBox().
        self.cmbQuality.do_load_combo([
            [_("Class S")], [_("Class B")],
            [_("Class B-1")],
        ])

        # Load the Construction RAMSTKComboBox().
        self.cmbConstruction.do_load_combo([["FLOTOX"], [_("Textured Poly")]])

        # Load the error correction code RAMSTKComboBox().
        self.cmbECC.do_load_combo(
            [
                [_("No on-chip ECC")], [_("On-chip Hamming code")],
                [_("Two-Needs-One redundant cell approach")],
            ],
        )

        # Load the manufacturing process RAMSTKComboBox().
        self.cmbManufacturing.do_load_combo([
            ["QML or QPL"],
            ["Non-QML or non-QPL"],
        ])

        # Load the package RAMSTKComboBox().
        self.cmbPackage.do_load_combo(
            [
                [_("Hermetic DIP w/ Solder or Weld Seal")],
                [_("Hermetic Pin Grid Array (PGA)")],
                [_("Hermetic SMT (Leaded and Nonleaded)")],
                [_("DIP w/ Glass Seal")], [_("Flatpacks w/ Axial Leads")],
                ["Can"], [_("Nonhermetic DIP")],
                [_("Nonhermetic Pin Grid Array (PGA)")],
                [_("Nonhermetic SMT")],
            ],
        )

        # Load the technology RAMSTKComboBox().
        try:
            if self._hazard_rate_method_id == 1:
                if subcategory_id == 9:
                    _data = [["MMIC"], [_("Digital")]]
                else:
                    _data = [["Bipolar"], ["MOS"]]
            else:
                _data = self._dic_technology[subcategory_id]
        except KeyError:
            _data = []
        self.cmbTechnology.do_load_combo(_data)

        # Load the device type RAMSTKComboBox().
        try:
            _data = self._dic_types[subcategory_id]
        except KeyError:
            _data = []
        self.cmbType.do_load_combo(_data)

    def _do_load_page(self, attributes):
        """
        Load the Integrated Circuit assesment input widgets.

        :param dict attributes: the attributes dictionary for the selected
        Integrated Circuit.
        :return: None
        :rtype: None
        """
        AssessmentInputs.do_load_page(self, attributes)

        if attributes['construction_id'] == 1:
            self.cmbApplication.do_load_combo(
                [
                    [_("Low Noise and Low Power (\u2264 100mW)")],
                    [_("Driver and High Power (> 100mW)")], [_("Unknown")],
                ],
            )
        else:
            self.cmbApplication.do_load_combo([[_("All digital devices")]])

        if self._subcategory_id == 10:
            self.cmbManufacturing.handler_block(self._lst_handler_id[4])
            self.cmbManufacturing.set_active(attributes['manufacturing_id'])
            self.cmbManufacturing.handler_unblock(self._lst_handler_id[4])

            self.cmbType.handler_block(self._lst_handler_id[7])
            self.cmbType.set_active(attributes['type_id'])
            self.cmbType.handler_unblock(self._lst_handler_id[7])

            self.txtArea.handler_block(self._lst_handler_id[8])
            self.txtArea.set_text(str(self.fmt.format(attributes['area'])))
            self.txtArea.handler_unblock(self._lst_handler_id[8])

            self.txtFeatureSize.handler_block(self._lst_handler_id[9])
            self.txtFeatureSize.set_text(
                str(self.fmt.format(attributes['feature_size'])),
            )
            self.txtFeatureSize.handler_unblock(self._lst_handler_id[9])

            self.txtVoltageESD.handler_block(self._lst_handler_id[15])
            self.txtVoltageESD.set_text(
                str(self.fmt.format(attributes['voltage_esd'])),
            )
            self.txtVoltageESD.handler_unblock(self._lst_handler_id[15])

        if self._hazard_rate_method_id == 1:
            self.txtNElements.handler_block(self._lst_handler_id[12])
            self.txtNElements.set_text(str(attributes['n_elements']))
            self.txtNElements.handler_unblock(self._lst_handler_id[12])

            if self._subcategory_id in [1, 2, 3, 4, 5, 8]:
                self.cmbTechnology.handler_block(self._lst_handler_id[6])
                self.cmbTechnology.set_active(attributes['technology_id'])
                self.cmbTechnology.handler_unblock(self._lst_handler_id[6])

        elif self._hazard_rate_method_id == 2:
            self.cmbPackage.handler_block(self._lst_handler_id[5])
            self.cmbPackage.set_active(attributes['package_id'])
            self.cmbPackage.handler_unblock(self._lst_handler_id[5])

            self.txtArea.handler_block(self._lst_handler_id[8])
            self.txtArea.set_text(str(self.fmt.format(attributes['area'])))
            self.txtArea.handler_unblock(self._lst_handler_id[8])

            self.txtNElements.handler_block(self._lst_handler_id[12])
            self.txtNElements.set_text(str(attributes['n_elements']))
            self.txtNElements.handler_unblock(self._lst_handler_id[12])

            self.txtThetaJC.handler_block(self._lst_handler_id[14])
            self.txtThetaJC.set_text(
                str(self.fmt.format(attributes['theta_jc'])),
            )
            self.txtThetaJC.handler_unblock(self._lst_handler_id[14])

            if self._subcategory_id in [1, 2, 3, 4]:
                self.cmbTechnology.handler_block(self._lst_handler_id[6])
                self.cmbTechnology.set_active(attributes['technology_id'])
                self.cmbTechnology.handler_unblock(self._lst_handler_id[6])

                self.txtNActivePins.handler_block(self._lst_handler_id[10])
                self.txtNActivePins.set_text(str(attributes['n_active_pins']))
                self.txtNActivePins.handler_unblock(self._lst_handler_id[10])

                self.txtYearsInProduction.handler_block(
                    self._lst_handler_id[16],
                )
                self.txtYearsInProduction.set_text(
                    str(attributes['years_in_production']),
                )
                self.txtYearsInProduction.handler_unblock(
                    self._lst_handler_id[16],
                )
            elif self._subcategory_id in [5, 7, 8]:
                self.cmbTechnology.handler_block(self._lst_handler_id[6])
                self.cmbTechnology.set_active(attributes['technology_id'])
                self.cmbTechnology.handler_unblock(self._lst_handler_id[6])
            elif self._subcategory_id == 6:
                self.cmbConstruction.handler_block(self._lst_handler_id[2])
                self.cmbConstruction.set_active(attributes['construction_id'])
                self.cmbConstruction.handler_unblock(self._lst_handler_id[2])

                self.cmbTechnology.handler_block(self._lst_handler_id[6])
                self.cmbTechnology.set_active(attributes['technology_id'])
                self.cmbTechnology.handler_unblock(self._lst_handler_id[6])

                self.cmbType.handler_block(self._lst_handler_id[7])
                self.cmbType.set_active(attributes['type_id'])  # Use for ECC.
                self.cmbType.handler_unblock(self._lst_handler_id[7])

                self.txtNCycles.handler_block(self._lst_handler_id[11])
                self.txtNCycles.set_text(str(attributes['n_cycles']))
                self.txtNCycles.handler_unblock(self._lst_handler_id[11])

                self.txtOperatingLife.handler_block(self._lst_handler_id[13])
                self.txtOperatingLife.set_text(
                    str(self.fmt.format(attributes['operating_life'])),
                )
                self.txtOperatingLife.handler_unblock(self._lst_handler_id[13])
            elif self._subcategory_id == 9:
                self.cmbApplication.handler_block(self._lst_handler_id[1])
                self.cmbApplication.set_active(attributes['application_id'])
                self.cmbApplication.handler_unblock(self._lst_handler_id[1])

                self.cmbType.handler_block(self._lst_handler_id[7])
                self.cmbType.set_active(attributes['type_id'])
                self.cmbType.handler_unblock(self._lst_handler_id[7])

                self.txtYearsInProduction.handler_block(
                    self._lst_handler_id[16],
                )
                self.txtYearsInProduction.set_text(
                    str(attributes['years_in_production']),
                )
                self.txtYearsInProduction.handler_unblock(
                    self._lst_handler_id[16],
                )

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected integrated circuit.

        :return: None
        :rtype: None
        """
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

        if self._subcategory_id == 10:
            self.cmbManufacturing.set_sensitive(True)
            self.cmbType.set_sensitive(True)
            self.txtArea.set_sensitive(True)
            self.txtFeatureSize.set_sensitive(True)
            self.txtNActivePins.set_sensitive(False)
            self.txtVoltageESD.set_sensitive(True)

        if self._hazard_rate_method_id == 1:
            if self._subcategory_id in [1, 2, 3, 4, 5, 8, 9]:
                self.cmbTechnology.set_sensitive(True)
                self.txtNElements.set_sensitive(True)
            if self._subcategory_id in [6, 7]:
                pub.sendMessage(
                    'wvw_editing_hardware',
                    module_id=self._hardware_id,
                    key='technology_id',
                    value=2,
                )
                self.txtNElements.set_sensitive(True)
        else:
            self.cmbPackage.set_sensitive(True)
            self.txtArea.set_sensitive(True)
            self.txtNElements.set_sensitive(True)
            self.txtThetaJC.set_sensitive(True)

            if self._subcategory_id in [1, 2, 3, 4]:
                self.cmbTechnology.set_sensitive(True)
                self.txtNActivePins.set_sensitive(True)
                self.txtYearsInProduction.set_sensitive(True)
            elif self._subcategory_id in [5, 7, 8]:
                self.cmbTechnology.set_sensitive(True)
            elif self._subcategory_id == 6:
                self.cmbConstruction.set_sensitive(True)
                self.cmbECC.set_sensitive(True)
                self.cmbTechnology.set_sensitive(True)
                self.txtNActivePins.set_sensitive(True)
                self.txtNCycles.set_sensitive(True)
                self.txtOperatingLife.set_sensitive(True)
            elif self._subcategory_id == 9:
                self.cmbApplication.set_sensitive(True)
                self.cmbType.set_sensitive(True)
                self.txtNActivePins.set_sensitive(True)
                self.txtYearsInProduction.set_sensitive(True)


class ICAssessmentResults(AssessmentResults):
    """
    Display IC assessment results attribute data in the RAMSTK Work Book.

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
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        2:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        3:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        4:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        5:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        6:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        7:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        8:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>",
        9:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>L</sub>\u03C0<sub>Q</sub></span>",
        10:
        "<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>BD</sub>\u03C0<sub>MFG</sub>\u03C0<sub>T</sub>\u03C0<sub>CD</sub> + \u03BB<sub>BP</sub>\u03C0<sub>E</sub>\u03C0<sub>Q</sub>\u03C0<sub>PT</sub> + \u03BB<sub>EOS</sub></span>",
    }

    def __init__(self, configuration, **kwargs):
        """
        Initialize an instance of the IC assessment result view.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`Configuration.Configuration`
        """
        AssessmentResults.__init__(self, configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels.append("C1:")
        self._lst_labels.append("\u03C0<sub>T</sub>:")
        self._lst_labels.append("C2:")
        self._lst_labels.append("\u03C0<sub>L</sub>:")
        self._lst_labels.append("\u03BB<sub>CYC</sub>:")
        self._lst_labels.append("\u03BB<sub>BD</sub>")
        self._lst_labels.append("\u03C0<sub>MFG</sub>")
        self._lst_labels.append("\u03C0<sub>CD</sub>")
        self._lst_labels.append("\u03BB<sub>BP</sub>")
        self._lst_labels.append("\u03C0<sub>PT</sub>")
        self._lst_labels.append("\u03BB<sub>EOS</sub>")
        self._lst_labels.append("\u03C0<sub>A</sub>")

        # Initialize private scalar attributes.
        self._lblModel.set_tooltip_markup(
            _(
                "The assessment model used to calculate the integrated circuit "
                "failure rate.",
            ),
        )

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.txtC1 = RAMSTKEntry()
        self.txtPiT = RAMSTKEntry()
        self.txtC2 = RAMSTKEntry()
        self.txtPiC = RAMSTKEntry()
        self.txtPiL = RAMSTKEntry()
        self.txtLambdaCYC = RAMSTKEntry()
        self.txtLambdaBD = RAMSTKEntry()
        self.txtPiMFG = RAMSTKEntry()
        self.txtPiCD = RAMSTKEntry()
        self.txtLambdaBP = RAMSTKEntry()
        self.txtPiPT = RAMSTKEntry()
        self.txtLambdaEOS = RAMSTKEntry()
        self.txtPiA = RAMSTKEntry()

        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_page, 'loaded_hardware_results')

    def __make_ui(self):
        """
        Make the integrated circuit Gtk.Notebook() assessment results page.

        :return: None
        :rtype: None
        """
        # Build the container for capacitors.
        _x_pos, _y_pos = AssessmentResults.make_ui(self)

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

        self.show_all()

    def __set_properties(self):
        """
        Set properties for Integrated Circuit assessment result widgets.

        :return: None
        :rtype: None
        """
        self.txtC1.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The die complexity hazard rate of the integrated "
                "circuit.",
            ),
        )
        self.txtPiT.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The temperature factor for the integrated circuit."),
        )
        self.txtC2.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The package hazard rate for the integrated circuit."),
        )
        self.txtPiC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The construction factor for the integrated circuit."),
        )
        self.txtPiL.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The learning factor for the integrated circuit."),
        )
        self.txtLambdaCYC.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The read/write cycling induced hazard rate for the "
                "EEPROM.",
            ),
        )
        self.txtLambdaBD.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The die base hazard rate for the VLSI device."),
        )
        self.txtPiMFG.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The manufacturing process correction factor for the "
                "VLSI device.",
            ),
        )
        self.txtPiCD.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The die complexity correction factor for the VLSI device.",
            ),
        )
        self.txtLambdaBP.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_("The package base hazard rate for the VLSI device."),
        )
        self.txtPiPT.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The package type correction factor for the VLSI device.",
            ),
        )
        self.txtLambdaEOS.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The electrical overstress hazard rate for the VLSI device.",
            ),
        )
        self.txtPiA.do_set_properties(
            width=125,
            editable=False,
            bold=True,
            tooltip=_(
                "The application correction factor for the GaAs device.",
            ),
        )

    def _do_load_page(self, attributes):
        """
        Load the integrated circuit assessment results page.

        :param dict attributes: the attributes dictionary for the selected
        Integrated Circuit.
        :return: None
        :rtype: None
        """
        AssessmentResults.do_load_page(self, attributes)

        self._hardware_id = attributes['hardware_id']
        self._subcategory_id = attributes['subcategory_id']
        self._hazard_rate_method_id = attributes['hazard_rate_method_id']

        self.txtC1.set_text(str(self.fmt.format(attributes['C1'])))
        self.txtPiT.set_text(str(self.fmt.format(attributes['piT'])))
        self.txtC2.set_text(str(self.fmt.format(attributes['C2'])))
        self.txtPiL.set_text(str(self.fmt.format(attributes['piL'])))
        self.txtLambdaCYC.set_text(
            str(self.fmt.format(attributes['lambdaCYC'])),
        )
        self.txtLambdaBD.set_text(str(self.fmt.format(attributes['lambdaBD'])))
        self.txtPiMFG.set_text(str(self.fmt.format(attributes['piMFG'])))
        self.txtPiCD.set_text(str(self.fmt.format(attributes['piCD'])))
        self.txtLambdaBP.set_text(str(self.fmt.format(attributes['lambdaBP'])))
        self.txtPiPT.set_text(str(self.fmt.format(attributes['piPT'])))
        self.txtLambdaEOS.set_text(
            str(self.fmt.format(attributes['lambdaEOS'])),
        )
        self.txtPiA.set_text(str(self.fmt.format(attributes['piA'])))

        self._do_set_sensitive()

    def _do_set_sensitive(self, **kwargs):  # pylint: disable=unused-argument
        """
        Set widget sensitivity as needed for the selected integrated circuit.

        :return: None
        :rtype: None
        """
        AssessmentResults.do_set_sensitive(self, **kwargs)

        self.txtLambdaB.set_sensitive(False)
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

        if self._subcategory_id == 10:
            self.txtLambdaB.set_sensitive(False)
            self.txtLambdaB.set_visible(False)
            self.txtLambdaBD.set_sensitive(True)
            self.txtPiMFG.set_sensitive(True)
            self.txtPiCD.set_sensitive(True)
            self.txtLambdaBP.set_sensitive(True)
            self.txtPiPT.set_sensitive(True)
            self.txtLambdaEOS.set_sensitive(True)
            self.txtPiE.set_sensitive(True)

        if self._hazard_rate_method_id == 1:
            self.txtLambdaB.set_sensitive(True)
        else:
            self.txtPiT.set_sensitive(True)
            self.txtPiE.set_sensitive(True)
            self.txtPiQ.set_sensitive(True)

            if self._subcategory_id in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                self.txtC1.set_sensitive(True)
                self.txtC2.set_sensitive(True)
                self.txtPiL.set_sensitive(True)

            if self._subcategory_id in [5, 6, 7, 8]:
                self.txtLambdaCYC.set_sensitive(True)

            if self._subcategory_id == 9:
                self.txtPiA.set_sensitive(True)
