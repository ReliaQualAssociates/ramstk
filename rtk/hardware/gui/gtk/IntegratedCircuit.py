#!/usr/bin/env python
"""
############################################################
Integrated Circuit Package Component Specific Work Book View
############################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.gui.gtk.IntegratedCircuit.py is part of The RTK Project
#
# All rights reserved.

import sys

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk
except ImportError:
    sys.exit(1)
try:
    import gtk.glade
except ImportError:
    sys.exit(1)

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.widgets as _widg

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Inputs(gtk.Frame):
    """
    The Work Book view for displaying all the attributes for an integrated
    circuit.  The attributes of an inntegrated circuit Work Book view are:
    """

    _lst_package = ["", _(u"Hermetic DIP w/ Weld Seal"), _(u"Pin Grid Array"),
                    _(u"Surface Mount"), _(u"Hermetic DIP w/ Glass Seal"),
                    _(u"Flatpack"), _(u"Can"),
                    _(u"Non-Hermetic DIP, PGA, SMT")]

    def __init__(self, model):
        """
        Creates an input frame for the inntegrated circuit data model.

        :param :class `rtk.hardware.IntegratedCircuit.model`: the IntegratedCircuit data
                                                     model whose attributes
                                                     will be displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # ===== ===== === Initialize private list attributes === ===== ===== #
        self._lst_labels = [_(u"Quality:"),
                            _(u"\u03C0<sub>Q</sub> Override:")]
        self._lst_quality = ["", "S", "B", "B-1"]

        self._lst_handler_id = []

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # = Create the input widgets common to all Integrated Circuit types = #
        self.cmbQuality = _widg.make_combo(simple=True)
        self.txtCommercialPiQ = _widg.make_entry(width=100)

        # Subcategory specific attributes.
        if self._subcategory == 1:          # Linear
            self._lst_labels.append(_(u"Technology:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"# of Transistors:"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))

            self.cmbTechnology = _widg.make_combo(simple=True)
            self.cmbFamily = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.txtNumTransistors = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)

        elif self._subcategory == 2:        # Logic
            self._lst_labels.append(_(u"Technology:"))
            self._lst_labels.append(_(u"Family:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"# of Gates:"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))

            self.cmbTechnology = _widg.make_combo(simple=True)
            self.cmbFamily = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.txtNumGates = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)

        elif self._subcategory == 3:        # PAL/PLA
            self._lst_labels.append(_(u"Technology:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"# of Gates:"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))

            self.cmbTechnology = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.txtNumGates = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)

        elif self._subcategory == 4:        # Microprocessor
            self._lst_labels.append(_(u"Technology:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"# of Bits:"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))

            self.cmbTechnology = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.txtNumBits = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)

        elif self._subcategory == 5:        # ROM
            self._lst_labels.append(_(u"Technology:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"Memory Size (bits):"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))

            self.cmbTechnology = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.txtNumBits = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)

        elif self._subcategory == 6:        # EEPROM
            self._lst_labels.append(_(u"Technology:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"Manufacturing Process:"))
            self._lst_labels.append(_(u"Memory Size (bits):"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))
            self._lst_labels.append(_(u"# of Programming Cycles:"))
            self._lst_labels.append(_(u"Error Correction Code:"))
            self._lst_labels.append(_(u"System Lifetime Operating Hours:"))

            self.cmbTechnology = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.cmbManufacturing = _widg.make_combo(simple=True)
            self.cmbECC = _widg.make_combo(simple=True)
            self.txtNumBits = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)
            self.txtCycles = _widg.make_entry(width=100)
            self.txtLifeOpHours = _widg.make_entry(width=100)

        elif self._subcategory == 7:        # DRAM
            self._lst_labels.append(_(u"Technology:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"Memory Size (bits):"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))

            self.cmbTechnology = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.txtNumBits = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)

        elif self._subcategory == 8:        # SRAM
            self._lst_labels.append(_(u"Technology:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"Memory Size (bits):"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))

            self.cmbTechnology = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.txtNumBits = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)

        elif self._subcategory == 9:        # GaAs
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"# of Elements:"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))

            self.cmbApplication = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.txtNumElements = _widg.make_entry(width=100)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)

        elif self._subcategory == 10:       # VLSI
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Package Type:"))
            self._lst_labels.append(_(u"Manufacturing Process:"))
            self._lst_labels.append(_(u"# of Pins:"))
            self._lst_labels.append(_(u"Years in Production:"))
            self._lst_labels.append(_(u"Feature Size (microns):"))
            self._lst_labels.append(_(u"Die Area (cm2):"))
            self._lst_labels.append(_(u"ESD Susceptibility (Volts):"))

            self.cmbApplication = _widg.make_combo(simple=True)
            self.cmbPackage = _widg.make_combo(simple=True)
            self.cmbManufacturing = _widg.make_combo(simple=True)
            self.txtNumPins = _widg.make_entry(width=100)
            self.txtYears = _widg.make_entry(width=100)
            self.txtFeatureSize = _widg.make_entry(width=100)
            self.txtDieArea = _widg.make_entry(width=100)
            self.txtESDVolts = _widg.make_entry(width=100)

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for Integrated
        Circuits.

        :keyword int x_pos: the x position of the display widgets.
        :return: False if successful or True if an error is encountered.
        """

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"MIL-HDBK-217FN2 Part Count Inputs") +
                          "</span>")
        _label.set_justify(gtk.JUSTIFY_LEFT)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.show_all()
        self.set_label_widget(_label)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.add(_scrollwindow)

        # Populate all the gtk.ComboBox().
        for i in range(len(self._lst_quality)):
            self.cmbQuality.insert_text(i, self._lst_quality[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels[0], _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Create the tooltips for all the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"connection."))

        # Place all the input widgets.
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])

        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, _index))
        _index += 1

        _fixed.show_all()

        return _x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress input widgets for Integrated
        Circuits.

        :keyword int x_pos: the x position of the display widgets.
        :return: False if successful or True if an error is encountered.
        """

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"MIL-HDBK-217FN2 Part Stress Inputs") +
                          "</span>")
        _label.set_justify(gtk.JUSTIFY_LEFT)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.show_all()
        self.set_label_widget(_label)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.add(_scrollwindow)

        # Populate all the gtk.ComboBox().
        for i in range(len(self._lst_quality)):
            self.cmbQuality.insert_text(i, self._lst_quality[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Create the tooltips for all the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"connection."))
        self.txtCommercialPiQ.set_tooltip_text(_(u"Displays the user-defined "
                                                 u"quality factor for the "
                                                 u"selected connection.  This "
                                                 u"value over rides the "
                                                 u"quality factor selected "
                                                 u"above."))

        # Place all the input widgets.
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtCommercialPiQ, _x_pos, _y_pos[1])

        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtCommercialPiQ.connect('focus-out-event',
                                          self._on_focus_out, _index))
        _index += 1

        if self._subcategory == 1:          # Linear
            # Populate the gtk.ComboBox().
            self.cmbTechnology.insert_text(0, '')
            self.cmbTechnology.insert_text(1, "Bipolar")
            self.cmbTechnology.insert_text(2, "MOS")

            for i in range(len(self._lst_package)):
                self.cmbPackage.insert_text(i, self._lst_package[i])

            # Place all the input widgets.
            _fixed.put(self.cmbTechnology, _x_pos, _y_pos[2])
            _fixed.put(self.cmbPackage, _x_pos, _y_pos[3])
            _fixed.put(self.txtNumTransistors, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumPins, _x_pos, _y_pos[5])
            _fixed.put(self.txtYears, _x_pos, _y_pos[6])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbTechnology.connect('changed',
                                           self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbPackage.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumTransistors.connect('focus-out-event',
                                               self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumPins.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtYears.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 2:        # Logic
            _lst_family = ["", "TTL", "ASTTL", "CML", "HTTL", "FTTL", "DTL",
                           "ECL", "ALSTTL", "FLTTL", "STTL", "BiCMOS",
                           "LSTTL", "III", "IIIL", "ISL"]

            # Populate the gtk.ComboBox().
            self.cmbTechnology.insert_text(0, '')
            self.cmbTechnology.insert_text(1, "Bipolar")
            self.cmbTechnology.insert_text(2, "MOS")

            for i in range(len(_lst_family)):
                self.cmbFamily.insert_text(i, self._lst_family[i])

            for i in range(len(self._lst_package)):
                self.cmbPackage.insert_text(i, self._lst_package[i])

            # Place all the input widgets.
            _fixed.put(self.cmbTechnology, _x_pos, _y_pos[2])
            _fixed.put(self.cmbFamily, _x_pos, _y_pos[3])
            _fixed.put(self.cmbPackage, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumGates, _x_pos, _y_pos[5])
            _fixed.put(self.txtNumPins, _x_pos, _y_pos[6])
            _fixed.put(self.txtYears, _x_pos, _y_pos[7])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbTechnology.connect('changed',
                                           self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbFamily.connect('changed',
                                       self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbPackage.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumGates.connect('focus-out-event',
                                         self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumPins.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtYears.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 3:        # PAL/PLA
            # Populate the gtk.ComboBox().
            self.cmbTechnology.insert_text(0, '')
            self.cmbTechnology.insert_text(1, "Bipolar")
            self.cmbTechnology.insert_text(2, "MOS")

            for i in range(len(self._lst_package)):
                self.cmbPackage.insert_text(i, self._lst_package[i])

            # Place all the input widgets.
            _fixed.put(self.cmbTechnology, _x_pos, _y_pos[2])
            _fixed.put(self.cmbPackage, _x_pos, _y_pos[3])
            _fixed.put(self.txtNumGates, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumPins, _x_pos, _y_pos[5])
            _fixed.put(self.txtYears, _x_pos, _y_pos[6])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbTechnology.connect('changed',
                                           self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbPackage.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumGates.connect('focus-out-event',
                                         self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumPins.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtYears.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 4:        # Microprocessor
            # Populate the gtk.ComboBox().
            self.cmbTechnology.insert_text(0, '')
            self.cmbTechnology.insert_text(1, "Bipolar")
            self.cmbTechnology.insert_text(2, "MOS")

            for i in range(len(self._lst_package)):
                self.cmbPackage.insert_text(i, self._lst_package[i])

            # Place all the input widgets.
            _fixed.put(self.cmbTechnology, _x_pos, _y_pos[2])
            _fixed.put(self.cmbPackage, _x_pos, _y_pos[3])
            _fixed.put(self.txtNumBits, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumPins, _x_pos, _y_pos[5])
            _fixed.put(self.txtYears, _x_pos, _y_pos[6])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbTechnology.connect('changed',
                                           self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbPackage.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumBits.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumPins.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtYears.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory in [5, 7, 8]:    # ROM, DRAM, or SRAM
            # Populate the gtk.ComboBox().
            self.cmbTechnology.insert_text(0, '')
            self.cmbTechnology.insert_text(1, "Bipolar")
            self.cmbTechnology.insert_text(2, "MOS")

            for i in range(len(self._lst_package)):
                self.cmbPackage.insert_text(i, self._lst_package[i])

            # Place all the input widgets.
            _fixed.put(self.cmbTechnology, _x_pos, _y_pos[2])
            _fixed.put(self.cmbPackage, _x_pos, _y_pos[3])
            _fixed.put(self.txtNumBits, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumPins, _x_pos, _y_pos[5])
            _fixed.put(self.txtYears, _x_pos, _y_pos[6])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbTechnology.connect('changed',
                                           self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbPackage.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumBits.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumPins.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtYears.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 6:        # EEPROM
            _lst_family = [_(u"Flotox"), _(u"Textured Poly")]
            _lst_ecc = [_(u"No On-Chip ECC"), _(u"On-Chip Hamming Code"),
                        _(u"Two-Needs-One Redundant Cell")]

            # Populate the gtk.ComboBox().
            self.cmbTechnology.insert_text(0, '')
            self.cmbTechnology.insert_text(1, "Bipolar")
            self.cmbTechnology.insert_text(2, "MOS")

            for i in range(len(self._lst_package)):
                self.cmbPackage.insert_text(i, self._lst_package[i])

            for i in range(len(_lst_family)):
                self.cmbManufacturing.insert_text(i, _lst_family[i])

            for i in range(len(_lst_ecc)):
                self.cmbECC.insert_text(i, _lst_ecc[i])

            # Place all the input widgets.
            _fixed.put(self.cmbTechnology, _x_pos, _y_pos[2])
            _fixed.put(self.cmbPackage, _x_pos, _y_pos[3])
            _fixed.put(self.cmbManufacturing, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumBits, _x_pos, _y_pos[5])
            _fixed.put(self.txtNumPins, _x_pos, _y_pos[6])
            _fixed.put(self.txtYears, _x_pos, _y_pos[7])
            _fixed.put(self.txtCycles, _x_pos, _y_pos[8])
            _fixed.put(self.cmbECC, _x_pos, _y_pos[9])
            _fixed.put(self.txtLifeOpHours, _x_pos, _y_pos[10])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbTechnology.connect('changed',
                                           self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbPackage.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbManufacturing.connect('changed',
                                              self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumBits.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumPins.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtYears.connect('focus-out-event',
                                      self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtCycles.connect('focus-out-event',
                                       self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbECC.connect('changed',
                                    self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtLifeOpHours.connect('focus-out-event',
                                            self._on_focus_out, _index))

        elif self._subcategory == 9:        # GaAs
            _lst_application = ["", _(u"MMIC, Low Noise & Low Power"),
                                _(u"MMIC, Driver & High Power"),
                                _(u"MMIC, Unknonw"), _(u"Digital")]

            # Populate the gtk.ComboBox().
            for i in range(len(self._lst_package)):
                self.cmbPackage.insert_text(i, self._lst_package[i])

            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])

            # Place all the input widgets.
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.cmbPackage, _x_pos, _y_pos[3])
            _fixed.put(self.txtNumElements, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumPins, _x_pos, _y_pos[5])
            _fixed.put(self.txtYears, _x_pos, _y_pos[6])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbPackage.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumElements.connect('focus-out-event',
                                            self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumPins.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtYears.connect('focus-out-event',
                                      self._on_focus_out, _index))
            _index += 1

        elif self._subcategory == 10:       # VLSI
            _lst_application = ["", _(u"Logic or Custom"), _(u"Gate Array")]
            _lst_package = ["", _(u"Hermetic DIP"), _(u"Non-Hermetic DIP"),
                            _(u"Hermetic PGA"), _(u"Non-Hermetic PGA"),
                            _(u"Hermetic Chip Carrier"),
                            _(u"Non-Hermetic Chip Carrier")]
            _lst_manufacturing = ["", _(u"QML or QPL"),
                                  _(u"Non QML or Non QPL")]

            # Populate the gtk.ComboBox().
            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])

            for i in range(len(_lst_package)):
                self.cmbPackage.insert_text(i, _lst_package[i])

            for i in range(len(_lst_manufacturing)):
                self.cmbManufacturing.insert_text(i, _lst_manufacturing[i])

            # Place all the input widgets.
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.cmbPackage, _x_pos, _y_pos[3])
            _fixed.put(self.cmbManufacturing, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumPins, _x_pos, _y_pos[5])
            _fixed.put(self.txtYears, _x_pos, _y_pos[6])
            _fixed.put(self.txtFeatureSize, _x_pos, _y_pos[7])
            _fixed.put(self.txtDieArea, _x_pos, _y_pos[8])
            _fixed.put(self.txtESDVolts, _x_pos, _y_pos[9])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbPackage.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbManufacturing.connect('changed',
                                              self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNumPins.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtYears.connect('focus-out-event',
                                      self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtFeatureSize.connect('focus-out-event',
                                            self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtDieArea.connect('focus-out-event',
                                        self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtESDVolts.connect('focus-out-event',
                                         self._on_focus_out, _index))

        _fixed.show_all()

        return _x_pos

    def load_217_stress_inputs(self, model):
        """
        Loads the Connection class gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.cmbQuality.set_active(int(model.quality))
        self.txtCommercialPiQ.set_text(str(fmt.format(model.q_override)))

        # Load subcategory specific widgets.
        if self._subcategory == 1:          # Linear
            self.cmbTechnology.set_active(model.technology)
            self.cmbPackage.set_active(model.package)
            self.txtNumTransistors.set_text(
                str(fmt.format(model.n_transistors)))
            self.txtNumPins.set_text(str(fmt.format(model.n_pins)))
            self.txtYears.set_text(str(fmt.format(model.years_production)))

        elif self._subcategory == 2:        # Logic
            self.cmbTechnology.set_active(model.technology)
            self.cmbFamily.set_active(model.family)
            self.cmbPackage.set_active(model.package)
            self.txtNumGates.set_text(str(fmt.format(model.n_gates)))
            self.txtNumPins.set_text(str(fmt.format(model.n_pins)))
            self.txtYears.set_text(str(fmt.format(model.years_production)))

        elif self._subcategory == 3:        # PAL/PLA
            self.cmbTechnology.set_active(model.technology)
            self.cmbPackage.set_active(model.package)
            self.txtNumGates.set_text(str(fmt.format(model.n_gates)))
            self.txtNumPins.set_text(str(fmt.format(model.n_pins)))
            self.txtYears.set_text(str(fmt.format(model.years_production)))

        elif self._subcategory == 4:        # Microprocessor
            self.cmbTechnology.set_active(model.technology)
            self.cmbPackage.set_active(model.package)
            self.txtNumBits.set_text(str(fmt.format(model.n_bits)))
            self.txtNumPins.set_text(str(fmt.format(model.n_pins)))
            self.txtYears.set_text(str(fmt.format(model.years_production)))

        elif self._subcategory in [5, 7, 8]:    # ROM, DRAM, SRAM
            self.cmbTechnology.set_active(model.technology)
            self.cmbPackage.set_active(model.package)
            self.txtNumBits.set_text(str(fmt.format(model.memory_size)))
            self.txtNumPins.set_text(str(fmt.format(model.n_pins)))
            self.txtYears.set_text(str(fmt.format(model.years_production)))

        elif self._subcategory == 6:        # EEPROM
            self.cmbTechnology.set_active(model.technology)
            self.cmbPackage.set_active(model.package)
            self.cmbManufacturing.set_active(model.manufacturing)
            self.cmbECC.set_active(model.ecc)
            self.txtNumBits.set_text(str(fmt.format(model.memory_size)))
            self.txtNumPins.set_text(str(fmt.format(model.n_pins)))
            self.txtYears.set_text(str(fmt.format(model.years_production)))
            self.txtCycles.set_text(str(model.n_cycles))
            self.txtLifeOpHours.set_text(str(fmt.format(model.life_op_hours)))

        elif self._subcategory == 9:        # GaAs
            self.cmbApplication.set_active(model.application)
            self.cmbPackage.set_active(model.package)
            self.txtNumElements.set_text(str(fmt.format(model.n_elements)))
            self.txtNumPins.set_text(str(fmt.format(model.n_pins)))
            self.txtYears.set_text(str(fmt.format(model.years_production)))

        elif self._subcategory == 10:       # VLSI
            self.cmbApplication.set_active(model.application)
            self.cmbPackage.set_active(model.package)
            self.cmbManufacturing.set_active(model.manufacturing)
            self.txtNumPins.set_text(str(fmt.format(model.n_pins)))
            self.txtYears.set_text(str(fmt.format(model.years_production)))
            self.txtFeatureSize.set_text(str(fmt.format(model.feature_size)))
            self.txtDieArea.set_text(str(fmt.format(model.die_area)))
            self.txtESDVolts.set_text(
                str(fmt.format(model.esd_susceptibility)))

        return False

    def _on_combo_changed(self, combo, index):
        """
        Responds to gtk.ComboBox() changed signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list oc the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 0:
            self._hardware_model.quality = combo.get_active()
        elif index == 2 and self._subcategory in [1, 2, 3, 4, 5, 6, 7, 8]:
            self._hardware_model.technology = combo.get_active()
        elif index == 2 and self._subcategory in [9, 10]:
            self._hardware_model.application = combo.get_active()
        elif index == 3 and self._subcategory in [1, 3, 4, 5, 6, 7, 8, 9, 10]:
            self._hardware_model.package = combo.get_active()
        elif index == 3 and self._subcategory == 2:
            self._hardware_model.family = combo.get_active()
        elif index == 4 and self._subcategory == 2:
            self._hardware_model.package = combo.get_active()
        elif index == 4 and self._subcategory in [6, 10]:
            self._hardware_model.manufacturing = combo.get_active()
        elif index == 9 and self._subcategory == 6:
            self._hardware_model.ecc = combo.get_active()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Responds to gtk.Entry() focus_out signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Entry() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        entry.handler_block(self._lst_handler_id[index])

        if index == 1:
            self._hardware_model.q_override = float(entry.get_text())
        elif index == 4 and self._subcategory == 1:
            self._hardware_model.n_transistors = int(entry.get_text())
        elif index == 4 and self._subcategory == 3:
            self._hardware_model.n_gates = int(entry.get_text())
        elif index == 4 and self._subcategory == 4:
            self._hardware_model.n_bits = int(entry.get_text())
        elif index == 4 and self._subcategory in [5, 7, 8]:
            self._hardware_model.memory_size = int(entry.get_text())
        elif index == 4 and self._subcategory == 9:
            self._hardware_model.n_elements = int(entry.get_text())
        elif index == 5 and self._subcategory in [1, 3, 4, 9, 10]:
            self._hardware_model.n_pins = int(entry.get_text())
        elif index == 5 and self._subcategory == 2:
            self._hardware_model.n_gates = int(entry.get_text())
        elif index == 5 and self._subcategory == 6:
            self._hardware_model.memory_size = int(entry.get_text())
        elif index == 6 and self._subcategory in [1, 3, 4, 9, 10]:
            self._hardware_model.years_production = float(entry.get_text())
        elif index == 6 and self._subcategory == 2:
            self._hardware_model.n_pins = int(entry.get_text())
        elif index == 6 and self._subcategory == 6:
            self._hardware_model.n_pins = int(entry.get_text())
        elif index == 7 and self._subcategory in [2, 6]:
            self._hardware_model.years_production = float(entry.get_text())
        elif index == 7 and self._subcategory == 10:
            self._hardware_model.feature_size = float(entry.get_text())
        elif index == 8 and self._subcategory == 6:
            self._hardware_model.n_cycles = float(entry.get_text())
        elif index == 8 and self._subcategory == 10:
            self._hardware_model.die_area = float(entry.get_text())
        elif index == 9 and self._subcategory == 10:
            self._hardware_model.esd_susceptibility = float(entry.get_text())
        elif index == 10 and self._subcategory == 6:
            self._hardware_model.life_op_hours = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for an
    integrated circuit.  The output attributes of an integrated circuit Work
    Book view are:
    """

    def __init__(self, model):
        """
        Initializes an instance of the integrated circuit assessment results
        view.

        :param model: the instance of the Integrated Circuit data model to
                      create the view for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Initialize private list attributes.
        self._lst_labels = ['', u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:",
                            u"\u03C0<sub>T</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiT = _widg.make_entry(width=100, editable=False, bold=True)

        # Subcategory specific attributes.
        if self._subcategory in [1, 2, 3, 4]:
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"
            self._lst_labels.append(u"C1:")
            self._lst_labels.append(u"C2:")
            self._lst_labels.append(u"\u03C0<sub>L</sub>:")
            self._lst_labels.append(_(u"Case Temperature:"))

            self.txtC1 = _widg.make_entry(width=100, editable=False, bold=True)
            self.txtC2 = _widg.make_entry(width=100, editable=False, bold=True)
            self.txtPiL = _widg.make_entry(width=100, editable=False,
                                           bold=True)
            self.txtCaseTemperature = _widg.make_entry(width=100,
                                                       editable=False,
                                                       bold=True)

        elif self._subcategory in [5, 6, 7, 8]:
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub> + C<sub>2</sub>\u03C0<sub>E</sub> + \u03BB<sub>CYC</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"
            self._lst_labels.append(u"C1:")
            self._lst_labels.append(u"C2:")
            self._lst_labels.append(u"\u03BB<sub>CYC</sub>:")
            self._lst_labels.append(u"\u03C0<sub>L</sub>:")
            self._lst_labels.append(_(u"Case Temperature:"))

            self.txtC1 = _widg.make_entry(width=100, editable=False, bold=True)
            self.txtC2 = _widg.make_entry(width=100, editable=False, bold=True)
            self.txtLambdaCyc = _widg.make_entry(width=100, editable=False,
                                                 bold=True)
            self.txtPiL = _widg.make_entry(width=100, editable=False,
                                           bold=True)
            self.txtCaseTemperature = _widg.make_entry(width=100,
                                                       editable=False,
                                                       bold=True)

        elif self._subcategory == 9:
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (C<sub>1</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub> + C<sub>2</sub>\u03C0<sub>E</sub>)\u03C0<sub>Q</sub>\u03C0<sub>L</sub></span>"
            self._lst_labels.append(u"C1:")
            self._lst_labels.append(u"C2:")
            self._lst_labels.append(u"\u03C0<sub>L</sub>:")
            self._lst_labels.append(u"\u03C0<sub>A</sub>:")
            self._lst_labels.append(_(u"Case Temperature:"))

            self.txtC1 = _widg.make_entry(width=100, editable=False, bold=True)
            self.txtC2 = _widg.make_entry(width=100, editable=False, bold=True)
            self.txtPiL = _widg.make_entry(width=100, editable=False,
                                           bold=True)
            self.txtPiA = _widg.make_entry(width=100, editable=False,
                                           bold=True)
            self.txtCaseTemperature = _widg.make_entry(width=100,
                                                       editable=False,
                                                       bold=True)

        elif self._subcategory == 10:       # VLSI
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>BD</sub>\u03C0<sub>T</sub>\u03C0<sub>MFG</sub>\u03C0<sub>CD</sub> + \u03BB<sub>BP</sub>\u03C0<sub>E</sub>\u03C0<sub>Q</sub>\u03C0<sub>PT</sub> + \u03BB<sub>EOS</sub></span>"
            self._lst_labels.append(u"\u03BB<sub>BD</sub>:")
            self._lst_labels.append(u"\u03C0<sub>MFG</sub>:")
            self._lst_labels.append(u"\u03C0<sub>PT</sub>:")
            self._lst_labels.append(u"\u03C0<sub>CD</sub>:")
            self._lst_labels.append(u"\u03BB<sub>BP</sub>:")
            self._lst_labels.append(u"\u03BB<sub>EOS</sub>:")
            self._lst_labels.append(_(u"Case Temperature:"))

            self.txtLambdaBD = _widg.make_entry(width=100, editable=False,
                                                bold=True)
            self.txtPiMFG = _widg.make_entry(width=100, editable=False,
                                             bold=True)
            self.txtPiPT = _widg.make_entry(width=100, editable=False,
                                            bold=True)
            self.txtPiCD = _widg.make_entry(width=100, editable=False,
                                            bold=True)
            self.txtLambdaBP = _widg.make_entry(width=100, editable=False,
                                                bold=True)
            self.txtLambdaEOS = _widg.make_entry(width=100, editable=False,
                                                 bold=True)
            self.txtCaseTemperature = _widg.make_entry(width=100,
                                                       editable=False,
                                                       bold=True)

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Inductors.

        :keyword int x_pos: the x position of the display widgets.
        :return: _x_pos: the x-coordinate of the widgets.
        :rtype: int
        """

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"MIL-HDBK-217FN2 Part Stress Results") +
                          "</span>")
        _label.set_justify(gtk.JUSTIFY_LEFT)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.show_all()
        self.set_label_widget(_label)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.add(_scrollwindow)

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 25)
        _x_pos = max(x_pos, _x_pos) + 30

        # Create the tooltips for all the results display widgets.
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected integrated circuit."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected integrated circuit."))
        self.txtPiT.set_tooltip_text(_(u"Displays the temperature factor for "
                                       u"the selected integrated circuit."))

        # Place the reliability result display widgets.
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiT, _x_pos, _y_pos[3])

        # Subcategory specific widgets.
        if self._subcategory in [1, 2, 3, 4]:
            self.txtC1.set_tooltip_text(_(u"Displays the die complexity "
                                          u"factor for the selected "
                                          u"integrated circuit."))
            self.txtC2.set_tooltip_text(_(u"Displays the package hazard rate "
                                          u"for the selected integrated "
                                          u"circuit."))
            self.txtPiL.set_tooltip_text(_(u"Displays the learning factor "
                                           u"for the selected integrated "
                                           u"circuit."))
            self.txtCaseTemperature.set_tooltip_text(_(u"Displays the case "
                                                       u"temperature for the "
                                                       u"selected integrated "
                                                       u"circuit."))

            _fixed.put(self.txtC1, _x_pos, _y_pos[4])
            _fixed.put(self.txtC2, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiL, _x_pos, _y_pos[6])
            _fixed.put(self.txtCaseTemperature, _x_pos, _y_pos[7])

        elif self._subcategory in [5, 6, 7, 8]:
            self.txtC1.set_tooltip_text(_(u"Displays the die complexity "
                                          u"factor for the selected "
                                          u"integrated circuit."))
            self.txtC2.set_tooltip_text(_(u"Displays the package hazard rate "
                                          u"for the selected integrated "
                                          u"circuit."))
            self.txtLambdaCyc.set_tooltip_text(_(u"Displays the programming "
                                                 u"cycle failure rate for the "
                                                 u"selected integrated "
                                                 u"circuit."))
            self.txtPiL.set_tooltip_text(_(u"Displays the learning factor "
                                           u"for the selected integrated "
                                           u"circuit."))
            self.txtCaseTemperature.set_tooltip_text(_(u"Displays the case "
                                                       u"temperature for the "
                                                       u"selected integrated "
                                                       u"circuit."))

            _fixed.put(self.txtC1, _x_pos, _y_pos[4])
            _fixed.put(self.txtC2, _x_pos, _y_pos[5])
            _fixed.put(self.txtLambdaCyc, _x_pos, _y_pos[6])
            _fixed.put(self.txtPiL, _x_pos, _y_pos[7])
            _fixed.put(self.txtCaseTemperature, _x_pos, _y_pos[8])

        elif self._subcategory == 9:
            self.txtC1.set_tooltip_text(_(u"Displays the die complexity "
                                          u"factor for the selected "
                                          u"integrated circuit."))
            self.txtC2.set_tooltip_text(_(u"Displays the package hazard rate "
                                          u"for the selected integrated "
                                          u"circuit."))
            self.txtPiL.set_tooltip_text(_(u"Displays the learning factor "
                                           u"for the selected integrated "
                                           u"circuit."))
            self.txtPiA.set_tooltip_text(_(u"Displays the application factor "
                                           u"for the selected integrated "
                                           u"circuit."))
            self.txtCaseTemperature.set_tooltip_text(_(u"Displays the case "
                                                       u"temperature for the "
                                                       u"selected integrated "
                                                       u"circuit."))

            _fixed.put(self.txtC1, _x_pos, _y_pos[4])
            _fixed.put(self.txtC2, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiL, _x_pos, _y_pos[6])
            _fixed.put(self.txtPiA, _x_pos, _y_pos[7])
            _fixed.put(self.txtCaseTemperature, _x_pos, _y_pos[8])

        elif self._subcategory == 10:
            self.txtLambdaBD.set_tooltip_text(_(u"Displays the die base "
                                                u"hazard rate for the "
                                                u"selected integrated "
                                                u"circuit."))
            self.txtPiMFG.set_tooltip_text(_(u"Displays the manufacturing "
                                             u"process correction factor for "
                                             u"the selected integrated "
                                             u"circuit."))
            self.txtPiPT.set_tooltip_text(_(u"Displays the package type "
                                            u"correction factor for the "
                                            u"selected integrated circuit."))
            self.txtPiCD.set_tooltip_text(_(u"Displays the die complexity "
                                            u"correction factor for the "
                                            u"selected integrated circuit."))
            self.txtCaseTemperature.set_tooltip_text(_(u"Displays the case "
                                                       u"temperature for the "
                                                       u"selected integrated "
                                                       u"circuit."))
            self.txtLambdaBP.set_tooltip_text(_(u"Displays the package base "
                                                u"hazard rate for the "
                                                u"selected integrated "
                                                u"circuit."))
            self.txtLambdaEOS.set_tooltip_text(_(u"Displays the electrical "
                                                 u"overstress hazard rate for "
                                                 u"the selected integrated "
                                                 u"circuit."))

            _fixed.put(self.txtLambdaBD, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiMFG, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiPT, _x_pos, _y_pos[6])
            _fixed.put(self.txtPiCD, _x_pos, _y_pos[7])
            _fixed.put(self.txtLambdaBP, _x_pos, _y_pos[8])
            _fixed.put(self.txtLambdaEOS, _x_pos, _y_pos[9])
            _fixed.put(self.txtCaseTemperature, _x_pos, _y_pos[10])

        _fixed.show_all()

        return _x_pos

    def load_217_stress_results(self, model):
        """
        Loads the Inductor class result gtk.Widgets().

        :param model: the Inductor data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.txtPiQ.set_text(str(fmt.format(model.piQ)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))
        self.txtPiT.set_text(str(fmt.format(model.piT)))

        if self._subcategory in [1, 2, 3, 4]:
            self.txtC1.set_text(str(fmt.format(model.C1)))
            self.txtC2.set_text(str(fmt.format(model.C2)))
            self.txtPiL.set_text(str(fmt.format(model.piL)))
            self.txtCaseTemperature.set_text(
                str(fmt.format(model.junction_temperature)))

        elif self._subcategory in [5, 6, 7, 8]:
            self.txtC1.set_text(str(fmt.format(model.C1)))
            self.txtC2.set_text(str(fmt.format(model.C2)))
            self.txtLambdaCyc.set_text(str(fmt.format(model.lambda_cyc)))
            self.txtPiL.set_text(str(fmt.format(model.piL)))
            self.txtCaseTemperature.set_text(
                str(fmt.format(model.junction_temperature)))

        elif self._subcategory == 9:
            self.txtC1.set_text(str(fmt.format(model.C1)))
            self.txtC2.set_text(str(fmt.format(model.C2)))
            self.txtPiL.set_text(str(fmt.format(model.piL)))
            self.txtPiA.set_text(str(fmt.format(model.piA)))
            self.txtCaseTemperature.set_text(
                str(fmt.format(model.junction_temperature)))

        elif self._subcategory == 10:
            self.txtLambdaBD.set_text(str(fmt.format(model.lambda_bd)))
            self.txtPiMFG.set_text(str(fmt.format(model.piMFG)))
            self.txtPiPT.set_text(str(fmt.format(model.piPT)))
            self.txtPiCD.set_text(str(fmt.format(model.piCD)))
            self.txtLambdaBP.set_text(str(fmt.format(model.lambda_bp)))
            self.txtLambdaEOS.set_text(str(fmt.format(model.lambda_eos)))
            self.txtCaseTemperature.set_text(
                str(fmt.format(model.junction_temperature)))

        return False
