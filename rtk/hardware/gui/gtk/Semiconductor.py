#!/usr/bin/env python
"""
######################################################
Semiconductor Module Component Specific Work Book View
######################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.gui.gtk.Semiconductor.py is part of The RTK Project
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

# Modules required for plotting.
import matplotlib
matplotlib.use('GTK')
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Inputs(gtk.Frame):
    """
    The Work Book view for displaying all the attributes for a semiconductor.
    The attributes of a semiconductor Work Book view are:
    """

    def __init__(self, model):
        """
        Creates an input frame for the Semiconductor data model.

        :param :class `rtk.hardware.Semiconductor.model`: the Semiconductor
                                                          data model whose
                                                          attributes will be
                                                          displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # ===== ===== === Initialize private list attributes === ===== ===== #
        self._lst_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:")]
        self._lst_handler_id = []

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # === Create the input widgets common to all Semiconductor types === #
        self.cmbQuality = _widg.make_combo(simple=True)
        self.txtQOverride = _widg.make_entry(width=100)

        # Create the tooltips for the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"semiconductor."))
        self.txtQOverride.set_tooltip_text(_(u"Enter and display the the "
                                             u"user-defined quality factor "
                                             u"for the selected "
                                             u"semiconductor."))

        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed',
                                    self._on_combo_changed, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtQOverride.connect('focus-out-event',
                                      self._on_focus_out, _index))
        _index += 1

        # Create the input widgets specific to Semiconductor subcategories.
        if self._subcategory == 12:         # Low frequency diode
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Contact Construction:"))
            self._lst_labels.append(_(u"Applied Reverse Voltage:"))
            self._lst_labels.append(_(u"Rated Reverse Voltage:"))

            # Create component specific input widgets.
            self.cmbApplication = _widg.make_combo(simple=True)
            self.cmbConstruction = _widg.make_combo(simple=True)
            self.txtVApplied = _widg.make_entry(width=100)
            self.txtVRated = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                                   u"application of the "
                                                   u"selected diode."))
            self.cmbConstruction.set_tooltip_text(_(u"Select and display the "
                                                    u"contact construction "
                                                    u"for the selected "
                                                    u"diode."))
            self.txtVApplied.set_tooltip_text(_(u"Enter and display the "
                                                u"applied reverse voltage for "
                                                u"the selected diode."))
            self.txtVRated.set_tooltip_text(_(u"Select and display the rated "
                                              u"reverse voltage for the "
                                              u"selected diode."))

            # Load the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower"),
                            _(u"Plastic")]
            _lst_application = ["", _(u"General Purpose Analog"),
                                _(u"Switching"),
                                _(u"Power Rectifier, Fast Recovery"),
                                _(u"Power Rectifier, Schottky"),
                                _(u"Power Rectifier, Stacked"),
                                _(u"Transient Suppressor"),
                                _(u"Current Regulator"),
                                _(u"Voltage Regulator/Reference")]
            _lst_construction = ["", _(u"Metallurgically Bonded"),
                                 _(u"Spring Loaded")]

            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])
            for i in range(len(_lst_construction)):
                self.cmbConstruction.insert_text(i, _lst_construction[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVApplied.connect('focus-out-event',
                                         self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVRated.connect('focus-out-event',
                                       self._on_focus_out, _index))

        elif self._subcategory == 13:       # High frequency diode
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Diode Type:"))
            self._lst_labels.append(_(u"Rated Power:"))

            # Create component specific input widgets.
            self.cmbApplication = _widg.make_combo(simple=True)
            self.cmbType = _widg.make_combo(simple=True)
            self.txtPRated = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                                   u"application of the "
                                                   u"selected diode."))
            self.cmbType.set_tooltip_text(_(u"Select and display the diode "
                                            u"type for the selected diode."))
            self.txtPRated.set_tooltip_text(_(u"Enter and display the rated "
                                              u"power for the selected "
                                              u"diode.  Only applicable for "
                                              u"PIN type diodes."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower"),
                            _(u"Plastic")]
            _lst_application = ["", _(u"Varactor, Voltage Control"),
                                _(u"Varactor, Multiplier"), _(u"All Others")]
            _lst_type = ["", u"Si IMPATT", _(u"Gunn/Bulk Effect"),
                         _(u"Tunnel and Back"), u"PIN", _(u"Schottky Barrier"),
                         u"Varactor"]

            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])
            for i in range(len(_lst_type)):
                self.cmbType.insert_text(i, _lst_type[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbType.connect('changed',
                                     self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtPRated.connect('focus-out-event',
                                       self._on_focus_out, _index))

        elif self._subcategory == 14:       # Low frequency bipolar transistor
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Rated Power:"))
            self._lst_labels.append(_(u"Applied CE Voltage:"))
            self._lst_labels.append(_(u"Rated CE Voltage:"))

            # Create component specific input widgets.
            self.cmbApplication = _widg.make_combo(simple=True)
            self.txtPRated = _widg.make_entry(width=100)
            self.txtVApplied = _widg.make_entry(width=100)
            self.txtVRated = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                                   u"application of the "
                                                   u"selected trnasistor."))
            self.txtPRated.set_tooltip_text(_(u"Enter and display the rated "
                                              u"power for the selected "
                                              u"transistor."))
            self.txtVApplied.set_tooltip_text(_(u"Enter and display the "
                                                u"applied CE voltage for the "
                                                u"selected transistor."))
            self.txtVRated.set_tooltip_text(_(u"Enter and display the rated "
                                              u"CE Voltage for the selected "
                                              u"transistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower"),
                            _(u"Plastic")]
            _lst_application = ["", _(u"Linear Amplification"),
                                _(u"Switching")]

            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtPRated.connect('focus-out-event',
                                       self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVApplied.connect('focus-out-event',
                                         self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVRated.connect('focus-out-event',
                                       self._on_focus_out, _index))

        elif self._subcategory == 15:       # Low frequency silicon FET
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Transistor Type:"))
            self._lst_labels.append(_(u"Rated Power:"))

            # Create component specific input widgets.
            self.cmbApplication = _widg.make_combo(simple=True)
            self.cmbType = _widg.make_combo(simple=True)
            self.txtPRated = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                                   u"application of the "
                                                   u"selected transistor."))
            self.cmbType.set_tooltip_text(_(u"Select and display the type of "
                                            u"the selected transistor."))
            self.txtPRated.set_tooltip_text(_(u"Enter and display the rated "
                                              u"power for the selected "
                                              u"transistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]
            _lst_application = ["", _(u"Linear Amplification"),
                                _(u"Small-Signal Switching"), _(u"Power")]
            _lst_type = ["", "MOSFET", "JFET"]

            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])
            for i in range(len(_lst_type)):
                self.cmbType.insert_text(i, _lst_type[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbType.connect('changed',
                                     self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtPRated.connect('focus-out-event',
                                       self._on_focus_out, _index))

        elif self._subcategory == 16:       # Unijunction transistor
            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]

        elif self._subcategory == 17:       # Low noise, high frequency bipolar transistor
            self._lst_labels.append(_(u"Rated Power:"))
            self._lst_labels.append(_(u"Applied CE Voltage:"))
            self._lst_labels.append(_(u"Rated CE Voltage:"))

            # Create component specific input widgets.
            self.txtPRated = _widg.make_entry(width=100)
            self.txtVApplied = _widg.make_entry(width=100)
            self.txtVRated = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.txtPRated.set_tooltip_text(_(u"Enter and display the rated "
                                              u"power for the selected "
                                              u"transistor."))
            self.txtVApplied.set_tooltip_text(_(u"Enter and display the "
                                                u"applied CE voltage for the "
                                                u"selected transistor."))
            self.txtVRated.set_tooltip_text(_(u"Enter and display the rated "
                                              u"CE voltage for the selected "
                                              u"transistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.txtPRated.connect('focus-out-event',
                                       self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVApplied.connect('focus-out-event',
                                         self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVRated.connect('focus-out-event',
                                       self._on_focus_out, _index))

        elif self._subcategory == 18:       # High power, high frequency bipolar transistor
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Construction:"))
            self._lst_labels.append(_(u"Network Matching:"))
            self._lst_labels.append(_(u"Operating Frequency:"))
            self._lst_labels.append(_(u"Operating CE Voltage:"))
            self._lst_labels.append(_(u"Breakdown CE Voltage:"))
            self._lst_labels.append(_(u"Duty Cycle:"))

            # Create component specific input widgets.
            self.cmbApplication = _widg.make_combo(simple=True)
            self.cmbConstruction = _widg.make_combo(simple=True)
            self.cmbMatching = _widg.make_combo(simple=True)
            self.txtFrequency = _widg.make_entry(width=100)
            self.txtVApplied = _widg.make_entry(width=100)
            self.txtVRated = _widg.make_entry(width=100)
            self.txtDutyCycle = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                                   u"application for the "
                                                   u"selected transistor."))
            self.cmbConstruction.set_tooltip_text(_(u"Select and display the "
                                                    u"metallization style "
                                                    u"of the selected "
                                                    u"transistor."))
            self.cmbMatching.set_tooltip_text(_(u"Select and display the "
                                                u"matching network for the "
                                                u"selected transistor."))
            self.txtFrequency.set_tooltip_text(_(u"Select and display the "
                                                 u"operating frequency of the "
                                                 u"selected transistor."))
            self.txtVApplied.set_tooltip_text(_(u"Select and display the "
                                                u"applied collector-emitter "
                                                u"voltage for the selected "
                                                u"transistor."))
            self.txtVRated.set_tooltip_text(_(u"Select and display the rated "
                                              u"collector-emitter breakdown "
                                              u"voltage with base shorted to "
                                              u"emitter for the selected "
                                              u"transistor."))
            self.txtDutyCycle.set_tooltip_text(_(u"Select and display the "
                                                 u"duty cycle for the "
                                                 u"selected transistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]
            _lst_application = ["", _(u"Pulsed"), "CW"]
            _lst_construction = ["", _(u"Gold Metallization"),
                                 _(u"Aluminum Metallization")]
            _lst_matching = ["", _(u"Input and Output"), _(u"Input Only"),
                             _(u"None")]

            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])
            for i in range(len(_lst_construction)):
                self.cmbConstruction.insert_text(i, _lst_construction[i])
            for i in range(len(_lst_matching)):
                self.cmbMatching.insert_text(i, _lst_matching[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbMatching.connect('changed',
                                         self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtFrequency.connect('focus-out-event',
                                          self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVApplied.connect('focus-out-event',
                                         self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVRated.connect('focus-out-event',
                                       self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtDutyCycle.connect('focus-out-event',
                                          self._on_focus_out, _index))

        elif self._subcategory == 19:       # High frequency GaAs FET
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Network Matching:"))
            self._lst_labels.append(_(u"Operating Frequency (GHz):"))
            self._lst_labels.append(_(u"Operating Power (W):"))

            # Create component specific input widgets.
            self.cmbApplication = _widg.make_combo(simple=True)
            self.cmbMatching = _widg.make_combo(simple=True)
            self.txtFrequency = _widg.make_entry(width=100)
            self.txtPOperating = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                                   u"application for the "
                                                   u"selected transistor."))
            self.cmbMatching.set_tooltip_text(_(u"Select and display the "
                                                u"matching network for the "
                                                u"selected transistor."))
            self.txtFrequency.set_tooltip_text(_(u"Enter and display the "
                                                 u"operating frequency of the "
                                                 u"selected transistor."))
            self.txtPOperating.set_tooltip_text(_(u"Enter and display the "
                                                  u"average operating power "
                                                  u"of the selected "
                                                  u"transistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]
            _lst_application = ["", _(u"Low Power and Pulsed"), "CW"]
            _lst_matching = ["", _(u"Input and Output"), _(u"Input Only"),
                             _(u"None")]

            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])
            for i in range(len(_lst_matching)):
                self.cmbMatching.insert_text(i, _lst_matching[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbMatching.connect('changed',
                                         self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtFrequency.connect('focus-out-event',
                                          self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtPOperating.connect('focus-out-event',
                                           self._on_focus_out, _index))

        elif self._subcategory == 20:       # High frequency silicon FET
            self._lst_labels.append(_(u"Transistor Type:"))

            self.cmbType = _widg.make_combo(simple=True)

            # Create the tooltips for the input widgets.
            self.cmbType.set_tooltip_text(_(u"Select and display the type of "
                                            u"the selected thermistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower")]
            _lst_type = ["", u"MOSFET", u"JFET"]

            for i in range(len(_lst_type)):
                self.cmbType.insert_text(i, _lst_type[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbType.connect('changed',
                                     self._on_combo_changed, _index))

        elif self._subcategory == 21:       # Thyristor
            self._lst_labels.append(_(u"Rated Forward Current "
                                      u"(I<sub>F</sub>):"))
            self._lst_labels.append(_(u"Applied Voltage "
                                      u"(V<sub>Applied</sub>):"))
            self._lst_labels.append(_(u"Rated Voltage (V<sub>Rated</sub>):"))

            self.txtIRated = _widg.make_entry(width=100)
            self.txtVApplied = _widg.make_entry(width=100)
            self.txtVRated = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.txtIRated.set_tooltip_text(_(u"Enter and display the rated "
                                              u"RMS forward current (amps) of "
                                              u"the selected thyristor."))
            self.txtVApplied.set_tooltip_text(_(u"Enter and display the "
                                                u"applied blocking voltage "
                                                u"for the selected "
                                                u"thyristor."))
            self.txtVRated.set_tooltip_text(_(u"Enter and display the rated "
                                              u"blocking voltage for "
                                              u"the selected thyristor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower"),
                            _(u"Plastic")]

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.txtIRated.connect('focus-out-event',
                                       self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVApplied.connect('focus-out-event',
                                         self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtVRated.connect('focus-out-event',
                                       self._on_focus_out, _index))

        elif self._subcategory == 22:       # Optoelectronic detector
            self._lst_labels.append(_(u"Optoelectronic Type:"))

            self.cmbType = _widg.make_combo(simple=True)

            # Create the tooltips for the input widgets.
            self.cmbType.set_tooltip_text(_(u"Select and display the "
                                            u"type of the selected "
                                            u"optoelectronic device."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower"),
                            _(u"Plastic")]
            _lst_type = ["", _(u"Photodector, Photo-Transistor"),
                         _(u"Photodector, Photo-Diode"),
                         _(u"Opto-Isolator, Photodiode Output, Single Device"),
                         _(u"Opto-Isolator, Phototransistor Output, Single Device"),
                         _(u"Opto-Isolator, Photodarlington Output, Single Device"),
                         _(u"Opto-Isolator, Light Sensitive Resistor, Single Device"),
                         _(u"Opto-Isolator, Photodiode Output, Dual Device"),
                         _(u"Opto-Isolator, Phototransistor Output, Dual Device"),
                         _(u"Opto-Isolator, Photodarlington Output, Dual Device"),
                         _(u"Opto-Isolator, Light Sensitive Resistor, Dual Device"),
                         _(u"Emitter, Infrared Light Emitting Diode (IRLED)"),
                         _(u"Emitter, Light Emitting Diode (LED)")]

            for i in range(len(_lst_type)):
                self.cmbType.insert_text(i, _lst_type[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbType.connect('changed',
                                     self._on_combo_changed, _index))

        elif self._subcategory == 23:       # Optoelectronic display
            self._lst_labels.append(_(u"Display Type:"))
            self._lst_labels.append(_(u"Construction:"))
            self._lst_labels.append(_(u"# of Segments:"))

            self.cmbType = _widg.make_combo(simple=True)
            self.cmbConstruction = _widg.make_combo(simple=True)
            self.txtNCharacters = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbType.set_tooltip_text(_(u"Select and display the type of "
                                            u"the selected display."))
            self.cmbConstruction.set_tooltip_text(_(u"Select and display the "
                                                    u"construction of the "
                                                    u"selected display."))
            self.txtNCharacters.set_tooltip_text(_(u"Enter and display the "
                                                   u"of characters for the "
                                                   u"selected display."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "JANTXV", "JANTX", "JAN", _(u"Lower"),
                            _(u"Plastic")]
            _lst_type = ["", _(u"Segment"), _(u"Diode Array")]
            _lst_construction = ["", _(u"With Logic Chip"),
                                 _(u"Without Logic Chip")]

            for i in range(len(_lst_type)):
                self.cmbType.insert_text(i, _lst_type[i])
            for i in range(len(_lst_construction)):
                self.cmbConstruction.insert_text(i, _lst_construction[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbType.connect('changed',
                                     self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNCharacters.connect('focus-out-event',
                                            self._on_focus_out, _index))

        elif self._subcategory == 24:       # Optoelectronic laser diode
            self._lst_labels.append(_(u"Laser Diode Type:"))
            self._lst_labels.append(_(u"Application:"))
            self._lst_labels.append(_(u"Duty Cycle:"))
            self._lst_labels.append(_(u"Peak Forward Current (I<sub>Fpk</sub>):"))
            self._lst_labels.append(_(u"Rated Optical Power (P<sub>s</sub>):"))
            self._lst_labels.append(_(u"Required Optical Power(P<sub>r</sub>):"))

            self.cmbType = _widg.make_combo(simple=True)
            self.cmbApplication = _widg.make_combo(simple=True)
            self.txtDutyCycle = _widg.make_entry(width=100)
            self.txtFwdCurrent = _widg.make_entry(width=100)
            self.txtPRated = _widg.make_entry(width=100)
            self.txtPRequired = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbType.set_tooltip_text(_(u"Select and display the type of "
                                            u"the selected laser diode."))
            self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                                   u"application of the "
                                                   u"selected laser diode."))
            self.txtDutyCycle.set_tooltip_text(_(u"Enter and display the "
                                                 u"duty cycle of the selected "
                                                 u"laser diode."))
            self.txtFwdCurrent.set_tooltip_text(_(u"Enter and display the "
                                                  u"forward peak current for "
                                                  u"the selected laser "
                                                  u"diode.  For variable "
                                                  u"current sources, use the "
                                                  u"initial current value."))
            self.txtPRated.set_tooltip_text(_(u"Enter and display the "
                                              u"rated optical power output "
                                              u"(mW) of the selected laser "
                                              u"diode."))
            self.txtPRequired.set_tooltip_text(_(u"Enter and display the "
                                                 u"required optical power "
                                                 u"output (mW) of the "
                                                 u"selected laser diode."))


            # Populate the gtk.ComboBox().
            _lst_quality = ["", _(u"Hermetic Package"),
                            _(u"Nonhermetic with Facet Coating"),
                            _(u"Nonhermetic without Facet Coating")]
            _lst_type = ["", "GaAs/Al GaAs", "In GaAs/In GaAsP"]
            _lst_application = ["", _(u"Continuous"), _(u"Pulsed")]

            for i in range(len(_lst_type)):
                self.cmbType.insert_text(i, _lst_type[i])
            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbType.connect('changed',
                                     self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtDutyCycle.connect('focus-out-event',
                                          self._on_focus_out, _index))#4
            _index += 1
            self._lst_handler_id.append(
                self.txtFwdCurrent.connect('focus-out-event',
                                           self._on_focus_out, _index))#5
            _index += 1
            self._lst_handler_id.append(
                self.txtPRated.connect('focus-out-event',
                                       self._on_focus_out, _index))#6
            _index += 1
            self._lst_handler_id.append(
                self.txtPRequired.connect('focus-out-event',
                                          self._on_focus_out, _index))#7

        # Populate the quality gtk.ComboBox().
        for i in range(len(_lst_quality)):
            self.cmbQuality.insert_text(i, _lst_quality[i])

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for
        Semiconductors.

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

        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels[:3],
                                             _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtQOverride, _x_pos, _y_pos[1])

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.add(_scrollwindow)

        _fixed.show_all()

        return x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress input widgets for
        Semiconductors.

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

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtQOverride, _x_pos, _y_pos[1])

        if self._subcategory == 12:         # Low frequency diode
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[3])
            _fixed.put(self.txtVApplied, _x_pos, _y_pos[4])
            _fixed.put(self.txtVRated, _x_pos, _y_pos[5])
        elif self._subcategory == 13:       # High frequency diode
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.cmbType, _x_pos, _y_pos[3])
            _fixed.put(self.txtPRated, _x_pos, _y_pos[4])
        elif self._subcategory == 14:       # Low frequency bipolar transistor
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.txtPRated, _x_pos, _y_pos[3])
            _fixed.put(self.txtVApplied, _x_pos, _y_pos[4])
            _fixed.put(self.txtVRated, _x_pos, _y_pos[5])
        elif self._subcategory == 15:       # Low frequency silicon FET
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.cmbType, _x_pos, _y_pos[3])
            _fixed.put(self.txtPRated, _x_pos, _y_pos[4])
        elif self._subcategory == 17:       # Low noise, high frequency bipolar transistor
            _fixed.put(self.txtPRated, _x_pos, _y_pos[2])
            _fixed.put(self.txtVApplied, _x_pos, _y_pos[3])
            _fixed.put(self.txtVRated, _x_pos, _y_pos[4])
        elif self._subcategory == 18:       # High power, high frequency bipolar transistor
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[3])
            _fixed.put(self.cmbMatching, _x_pos, _y_pos[4])
            _fixed.put(self.txtFrequency, _x_pos, _y_pos[5])
            _fixed.put(self.txtVApplied, _x_pos, _y_pos[6])
            _fixed.put(self.txtVRated, _x_pos, _y_pos[7])
            _fixed.put(self.txtDutyCycle, _x_pos, _y_pos[8])
        elif self._subcategory == 19:       # High frequency GaAs FET
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.cmbMatching, _x_pos, _y_pos[3])
            _fixed.put(self.txtFrequency, _x_pos, _y_pos[4])
            _fixed.put(self.txtPOperating, _x_pos, _y_pos[5])
        elif self._subcategory == 20:       # High frequency silicon FET
            _fixed.put(self.cmbType, _x_pos, _y_pos[2])
        elif self._subcategory == 21:       # Thyristor
            _fixed.put(self.txtIRated, _x_pos, _y_pos[2])
            _fixed.put(self.txtVApplied, _x_pos, _y_pos[3])
            _fixed.put(self.txtVRated, _x_pos, _y_pos[4])
        elif self._subcategory == 22:       # Optoelectronic detector
            _fixed.put(self.cmbType, _x_pos, _y_pos[2])
        elif self._subcategory == 23:       # Optoelectronic display
            _fixed.put(self.cmbType, _x_pos, _y_pos[2])
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[3])
            _fixed.put(self.txtNCharacters, _x_pos, _y_pos[4])
        elif self._subcategory == 24:       # Optoelectronic laser diode
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[2])
            _fixed.put(self.cmbType, _x_pos, _y_pos[3])
            _fixed.put(self.txtDutyCycle, _x_pos, _y_pos[4])
            _fixed.put(self.txtFwdCurrent, _x_pos, _y_pos[5])
            _fixed.put(self.txtPRated, _x_pos, _y_pos[6])
            _fixed.put(self.txtPRequired, _x_pos, _y_pos[7])

        _fixed.show_all()

        return _x_pos

    def load_217_stress_inputs(self, model):
        """
        Loads the Semiconductor class MIL-HDBK-217FN2 part stress gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.cmbQuality.set_active(model.quality)
        self.txtQOverride.set_text(str(fmt.format(model.q_override)))

        if self._subcategory == 12:         # Low frequency diode
            self.cmbApplication.set_active(model.application)
            self.cmbConstruction.set_active(model.construction)
            self.txtVApplied.set_text(str(fmt.format(model.operating_voltage)))
            self.txtVRated.set_text(str(fmt.format(model.rated_voltage)))
        elif self._subcategory == 13:       # High frequency diode
            self.cmbApplication.set_active(model.application)
            self.cmbType.set_active(model.type)
            self.txtPRated.set_text(str(fmt.format(model.rated_power)))
        elif self._subcategory == 14:       # Low frequency biploar transistor
            self.cmbApplication.set_active(model.application)
            self.txtPRated.set_text(str(fmt.format(model.rated_power)))
            self.txtVApplied.set_text(str(fmt.format(model.operating_voltage)))
            self.txtVRated.set_text(str(fmt.format(model.rated_voltage)))
        elif self._subcategory == 15:       # Low frequency silicon FET
            self.cmbApplication.set_active(model.application)
            self.cmbType.set_active(model.type)
            self.txtPRated.set_text(str(fmt.format(model.rated_power)))
        elif self._subcategory == 17:       # Low noise, high frequency bipolar transistor
            self.txtPRated.set_text(str(fmt.format(model.rated_power)))
            self.txtVApplied.set_text(str(fmt.format(model.operating_voltage)))
            self.txtVRated.set_text(str(fmt.format(model.rated_voltage)))
        elif self._subcategory == 18:       # High power, high frequency bipolar transistor
            self.cmbApplication.set_active(model.application)
            self.cmbConstruction.set_active(model.construction)
            self.cmbMatching.set_active(model.matching)
            self.txtFrequency.set_text(str(model.frequency))
            self.txtVApplied.set_text(str(model.operating_voltage))
            self.txtVRated.set_text(str(model.rated_voltage))
            self.txtDutyCycle.set_text(str(model.duty_cycle))
        elif self._subcategory == 19:       # High frequency GaAs FET
            self.cmbApplication.set_active(model.application)
            self.cmbMatching.set_active(model.matching)
            self.txtFrequency.set_text(str(model.frequency))
            self.txtPOperating.set_text(str(model.operating_power))
        elif self._subcategory == 20:       # High frequency silicon FET
            self.cmbType.set_active(model.type)
        elif self._subcategory == 21:       # Thyristor
            self.txtIRated.set_text(str(fmt.format(model.rated_current)))
            self.txtVApplied.set_text(str(fmt.format(model.operating_voltage)))
            self.txtVRated.set_text(str(fmt.format(model.rated_voltage)))
        elif self._subcategory == 22:       # Optoelectronic detector
            self.cmbType.set_active(model.type)
        elif self._subcategory == 23:       # Optoelectronic display
            self.cmbType.set_active(model.type)
            self.cmbConstruction.set_active(model.construction)
            self.txtNCharacters.set_text(str(model.n_characters))
        elif self._subcategory == 24:       # Optoelectronic laser diode
            self.cmbType.set_active(model.type)
            self.cmbApplication.set_active(model.application)
            self.txtDutyCycle.set_text(str(fmt.format(model.duty_cycle)))
            self.txtFwdCurrent.set_text(
                str(fmt.format(model.operating_current)))
            self.txtPRated.set_text(str(fmt.format(model.rated_power)))
            self.txtPRequired.set_text(str(fmt.format(model.required_power)))

        return False

    def _on_combo_changed(self, combo, index):
        """
        Responds to gtk.ComboBox() changed signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 0:
            self._hardware_model.quality = combo.get_active()
        elif index == 2 and self._subcategory in [12, 13, 14, 15, 18, 19, 24]:
            self._hardware_model.application = combo.get_active()
        elif index == 2 and self._subcategory in [20, 22, 23]:
            self._hardware_model.type = combo.get_active()
        elif index == 3 and self._subcategory in [12, 23]:
            self._hardware_model.construction = combo.get_active()
        elif index == 3 and self._subcategory in [13, 15, 24]:
            self._hardware_model.type = combo.get_active()
        elif index == 3 and self._subcategory == 18:
            self._hardware_model.construction = combo.get_active()
        elif index == 3 and self._subcategory == 19:
            self._hardware_model.matching = combo.get_active()
        elif index == 4 and self._subcategory == 18:
            self._hardware_model.matching = combo.get_active()

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
        elif index == 2 and self._subcategory == 17:
            self._hardware_model.rated_power = float(entry.get_text())
        elif index == 2 and self._subcategory == 21:
            self._hardware_model.rated_current = float(entry.get_text())
        elif index == 3 and self._subcategory == 14:
            self._hardware_model.rated_power = float(entry.get_text())
        elif index == 3 and self._subcategory in [17, 21]:
            self._hardware_model.operating_voltage = float(entry.get_text())
        elif index == 4 and self._subcategory == 12:
            self._hardware_model.operating_voltage = float(entry.get_text())
        elif index == 4 and self._subcategory == 13:
            self._hardware_model.rated_power = float(entry.get_text())
        elif index == 4 and self._subcategory == 14:
            self._hardware_model.operating_voltage = float(entry.get_text())
        elif index == 4 and self._subcategory == 15:
            self._hardware_model.rated_power = float(entry.get_text())
        elif index == 4 and self._subcategory == 17:
            self._hardware_model.rated_voltage = float(entry.get_text())
        elif index == 4 and self._subcategory == 19:
            self._hardware_model.frequency = float(entry.get_text())
        elif index == 4 and self._subcategory == 21:
            self._hardware_model.rated_voltage = float(entry.get_text())
        elif index == 4 and self._subcategory == 23:
            self._hardware_model.n_characters = int(entry.get_text())
        elif index == 4 and self._subcategory == 24:
            self._hardware_model.duty_cycle = float(entry.get_text())
        elif index == 5 and self._subcategory == 12:
            self._hardware_model.rated_voltage = float(entry.get_text())
        elif index == 5 and self._subcategory == 14:
            self._hardware_model.rated_voltage = float(entry.get_text())
        elif index == 5 and self._subcategory == 18:
            self._hardware_model.frequency = float(entry.get_text())
        elif index == 5 and self._subcategory == 19:
            self._hardware_model.operating_power = float(entry.get_text())
        elif index == 5 and self._subcategory == 24:
            self._hardware_model.operating_currents = float(entry.get_text())
        elif index == 6 and self._subcategory == 18:
            self._hardware_model.operating_voltage = float(entry.get_text())
        elif index == 6 and self._subcategory == 24:
            self._hardware_model.rated_power = float(entry.get_text())
        elif index == 7 and self._subcategory == 18:
            self._hardware_model.rated_voltage = float(entry.get_text())
        elif index == 7 and self._subcategory == 24:
            self._hardware_model.required_power = float(entry.get_text())
        elif index == 8 and self._subcategory == 18:
            self._hardware_model.duty_cycle = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    Semiconductor.  The output attributes of a Semiconductor Work Book view
    are:
    """

    def __init__(self, model):
        """
        Initializes an instance of the Semiconductor assessment results view.

        :param model: the instance of the Semiconductor data model to create
                      the view for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Initialize private list attributes.
        self._lst_labels = ["", u"\u03BB<sub>b</sub>:", u"\u03C0<sub>T</sub>:",
                            u"\u03C0<sub>Q</sub>:", u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiT = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        self.figDerate = Figure(figsize=(6, 4))
        self.axsDerate1 = self.figDerate.add_subplot(111)
        self.axsDerate2 = self.axsDerate1.twinx()
        self.pltDerate = FigureCanvas(self.figDerate)

        if self._subcategory == 12:         # Low frequency diode
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>S</sub>\u03C0<sub>C</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>S</sub>:")
            self._lst_labels.append(u"\u03C0<sub>C</sub>:")

            self.txtPiS = _widg.make_entry(width=100, editable=False, bold=True)
            self.txtPiC = _widg.make_entry(width=100, editable=False, bold=True)

            self.txtPiS.set_tooltip_text(_(u"Displays the voltage stress "
                                           u"factor for the selected diode."))
            self.txtPiC.set_tooltip_text(_(u"Displays the contact "
                                           u"construction factor for the "
                                           u"selected diode."))

        elif self._subcategory == 13:       # High frequency diode
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>A</sub>:")
            self._lst_labels.append(u"\u03C0<sub>R</sub>:")

            self.txtPiA = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiR = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiA.set_tooltip_text(_(u"Displays the application factor "
                                           u"for the selected diode."))
            self.txtPiR.set_tooltip_text(_(u"Displays the power rating "
                                           u"factor for the selected diode."))

        elif self._subcategory == 14:       # Low frequency bipolar transistor
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>A</sub>:")
            self._lst_labels.append(u"\u03C0<sub>R</sub>:")
            self._lst_labels.append(u"\u03C0<sub>S</sub>:")

            self.txtPiA = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiR = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiS = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiA.set_tooltip_text(_(u"Displays the application factor "
                                           u"for the selected transistor."))
            self.txtPiR.set_tooltip_text(_(u"Displays the power rating "
                                           u"factor for the selected "
                                           u"transistor."))
            self.txtPiS.set_tooltip_text(_(u"Displays the voltage stress "
                                           u"factor for the selected diode."))

        elif self._subcategory == 15:       # Low frequency silicon FET
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>A</sub>")

            self.txtPiA = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiA.set_tooltip_text(_(u"Displays the application factor "
                                           u"for the selected transistor."))

        elif self._subcategory == 16:       # Unijunction transistor
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

        elif self._subcategory == 17:       # Low noise, high frequency bipolar transistor
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>R</sub>:")
            self._lst_labels.append(u"\u03C0<sub>S</sub>:")

            self.txtPiR = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiS = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiR.set_tooltip_text(_(u"Displays the power rating factor "
                                           u"for the selected transistor."))
            self.txtPiS.set_tooltip_text(_(u"Displays the voltage stress "
                                           u"factor for the selected "
                                           u"transistor."))

        elif self._subcategory in [18, 19]:
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>A</sub>\u03C0<sub>M</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>A</sub>:")
            self._lst_labels.append(u"\u03C0<sub>M</sub>:")

            self.txtPiA = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiM = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiA.set_tooltip_text(_(u"Displays the application factor "
                                           u"for the selected transistor."))
            self.txtPiM.set_tooltip_text(_(u"Displays the matching network "
                                           u"factor for the selected "
                                           u"transistor."))

        elif self._subcategory == 20:       # High frequency silicon FET
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

        elif self._subcategory == 21:       # Thyristor
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>R</sub>\u03C0<sub>S</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>R</sub>:")
            self._lst_labels.append(u"\u03C0<sub>S</sub>:")

            self.txtPiR = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiS = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiR.set_tooltip_text(_(u"Displays the current rating "
                                           u"factor for the selected "
                                           u"thyristor."))
            self.txtPiS.set_tooltip_text(_(u"Displays the voltage stress "
                                           u"factor for the selected "
                                           u"thyristor."))

        elif self._subcategory in [22, 23]: # Optoelectronic detector, display
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

        elif self._subcategory == 24:       # Optoelectronic detector, laser diode
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>Q</sub>\u03C0<sub>C</sub>\u03C0<sub>I</sub>\u03C0<sub>A</sub>\u03C0<sub>P</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>I</sub>:")
            self._lst_labels.append(u"\u03C0<sub>A</sub>:")
            self._lst_labels.append(u"\u03C0<sub>P</sub>:")

            self.txtPiI = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiA = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiP = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiI.set_tooltip_text(_(u"Displays the forward current "
                                           u"factor for the selected "
                                           u"laser diode."))
            self.txtPiA.set_tooltip_text(_(u"Displays the application "
                                           u"factor for the selected "
                                           u"laser diode."))
            self.txtPiP.set_tooltip_text(_(u"Displays the power degradation "
                                           u"factor for the selected "
                                           u"laser diode."))

        # Create the tooltips for the common results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected semiconductor."))
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected semiconductor."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected semiconductor."))
        self.txtPiT.set_tooltip_text(_(u"Displays the temperature factor for "
                                       u"the selected semiconductor."))

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Semiconductors.

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

        # Create and place all the labels for the results.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 25)
        _x_pos = max(x_pos, _x_pos) + 30

        if self._subcategory == 12:         # Low frequency diode
            _fixed.put(self.txtPiS, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiC, _x_pos, _y_pos[6])

        elif self._subcategory == 13:       # High frequency diode
            _fixed.put(self.txtPiA, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiR, _x_pos, _y_pos[6])

        elif self._subcategory == 14:       # Low frequency bipolar transistor
            _fixed.put(self.txtPiA, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiR, _x_pos, _y_pos[6])
            _fixed.put(self.txtPiS, _x_pos, _y_pos[7])

        elif self._subcategory == 15:       # Low frequency silicon FET
            _fixed.put(self.txtPiA, _x_pos, _y_pos[5])

        elif self._subcategory == 17:       # Low noise, high frequency bipolar transistor
            _fixed.put(self.txtPiR, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiS, _x_pos, _y_pos[6])

        elif self._subcategory in [18, 19]:
            _fixed.put(self.txtPiA, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiM, _x_pos, _y_pos[6])

        elif self._subcategory == 21:       # Thyristor
            _fixed.put(self.txtPiR, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiS, _x_pos, _y_pos[6])

        elif self._subcategory == 24:       # Optoelectronic laser diode
            _fixed.put(self.txtPiI, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiA, _x_pos, _y_pos[6])
            _fixed.put(self.txtPiP, _x_pos, _y_pos[7])

        # Place the reliability result display widgets.
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiT, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[3])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[4])

        _fixed.show_all()

        return _x_pos

    def load_217_stress_results(self, model):
        """
        Loads the Semiconductor class result gtk.Widgets().

        :param model: the Semiconductor data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiT.set_text(str(fmt.format(model.piT)))
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        if self._subcategory == 12:
            self.txtPiS.set_text(str(fmt.format(model.piS)))
            self.txtPiC.set_text(str(fmt.format(model.piC)))

        elif self._subcategory == 13:
            self.txtPiA.set_text(str(fmt.format(model.piA)))
            self.txtPiR.set_text(str(fmt.format(model.piR)))

        elif self._subcategory == 14:
            self.txtPiA.set_text(str(fmt.format(model.piA)))
            self.txtPiR.set_text(str(fmt.format(model.piR)))
            self.txtPiS.set_text(str(fmt.format(model.piS)))

        elif self._subcategory == 15:
            self.txtPiA.set_text(str(fmt.format(model.piA)))

        elif self._subcategory == 17:
            self.txtPiR.set_text(str(fmt.format(model.piR)))
            self.txtPiS.set_text(str(fmt.format(model.piS)))

        elif self._subcategory in [18, 19]:
            self.txtPiA.set_text(str(fmt.format(model.piA)))
            self.txtPiM.set_text(str(fmt.format(model.piM)))

        elif self._subcategory == 21:
            self.txtPiR.set_text(str(fmt.format(model.piR)))
            self.txtPiS.set_text(str(fmt.format(model.piS)))

        elif self._subcategory == 24:
            self.txtPiI.set_text(str(fmt.format(model.piI)))
            self.txtPiA.set_text(str(fmt.format(model.piA)))
            self.txtPiP.set_text(str(fmt.format(model.piP)))

        return False

    def load_derate_plot(self, model, frame):
        """
        Loads the stress derate plot for the Semiconductor class.

        :param model: the Hardware data model to load the attributes from.
        :param gtk.Frame frame: the gtk.Frame() to embed the derate plot into.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Clear the operating point and derating curve for the component.
        self.axsDerate1.cla()
        self.axsDerate2.cla()

        # Plot the derating curve and operating point.
        _x = [float(model.min_rated_temperature),
              float(model.knee_temperature),
              float(model.max_rated_temperature)]

        _line0 = self.axsDerate1.plot(_x, model.lst_derate_criteria[0], 'r.-',
                                      linewidth=2)
        _line1 = self.axsDerate1.plot(_x, model.lst_derate_criteria[1], 'b.-',
                                      linewidth=2)

        if model.subcategory in [12, 13]:
            _line2 = self.axsDerate1.plot(model.temperature_active,
                                          model.power_ratio, 'go')
            _lines = _line0 + _line1 + _line2

            self.axsDerate1.set_title(
                _(u"Power Derating Curve for %s at %s") %
                (model.part_number, model.ref_des),
                fontdict={'fontsize': 12, 'fontweight' : 'bold',
                          'verticalalignment': 'baseline'})
            _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                             _(u"Power Operating Point")])
            self.axsDerate1.set_ylabel(r'$\mathbf{P_{op} / P_{rated}}$',
                                       fontdict={'fontsize': 12,
                                                 'fontweight' : 'bold',
                                                 'rotation': 'vertical',
                                                 'verticalalignment': 'baseline'})
        elif model.subcategory in [14, 15, 16, 17, 18, 19, 20]:
            _line2 = self.axsDerate1.plot(model.temperature_active,
                                          model.power_ratio, 'go')
            _line3 = self.axsDerate2.plot(model.temperature_active,
                                          model.voltage_ratio, 'ms')
            _lines = _line0 + _line1 + _line2 + _line3

            self.axsDerate1.set_title(
                _(u"Power and Voltage Derating Curve for %s at %s") %
                (model.part_number, model.ref_des),
                fontdict={'fontsize': 12, 'fontweight' : 'bold',
                          'verticalalignment': 'baseline'})
            _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                             _(u"Power Operating Point"),
                             _(u"Voltage Operating Point")])
        elif model.subcategory == 21:
            _line2 = self.axsDerate2.plot(model.temperature_active,
                                          model.voltage_ratio, 'go')
            _line3 = self.axsDerate2.plot(model.temperature_active,
                                          model.current_ratio, 'ms')
            _lines = _line0 + _line1 + _line2 + _line3

            self.axsDerate1.set_title(
                _(u"Voltage and Current Derating Curve for %s at %s") %
                (model.part_number, model.ref_des),
                fontdict={'fontsize': 12, 'fontweight' : 'bold',
                          'verticalalignment': 'baseline'})
            _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                             _(u"Voltage Operating Point"),
                             _(u"Current Operating Point")])

        elif model.subcategory in [22, 23, 24]:
            _line2 = self.axsDerate1.plot(model.temperature_active,
                                          model.voltage_ratio, 'go')
            _lines = _line0 + _line1 + _line2

            self.axsDerate1.set_title(
                _(u"Voltage Derating Curve for %s at %s") %
                (model.part_number, model.ref_des),
                fontdict={'fontsize': 12, 'fontweight' : 'bold',
                          'verticalalignment': 'baseline'})
            _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                             _(u"Voltage Operating Point")])
            self.axsDerate1.set_ylabel(r'$\mathbf{V_{op} / V_{rated}}$',
                                       fontdict={'fontsize': 12,
                                                 'fontweight' : 'bold',
                                                 'rotation': 'vertical',
                                                 'verticalalignment': 'baseline'})

        if(_x[0] != _x[2] and
           model.lst_derate_criteria[1][0] != model.lst_derate_criteria[1][2]):
            self.axsDerate1.axis([0.95 * _x[0], 1.05 * _x[2],
                                  model.lst_derate_criteria[1][2],
                                  1.05 * model.lst_derate_criteria[1][0]])
            self.axsDerate2.axis([0.95 * _x[0], 1.05 * _x[2],
                                  model.lst_derate_criteria[1][2],
                                  1.05 * model.lst_derate_criteria[1][0]])
        else:
            self.axsDerate1.axis([0.95, 1.05, 0.0, 1.05])
            self.axsDerate2.axis([0.95, 1.05, 0.0, 1.05])

        _leg = self.axsDerate1.legend(_lines, _legend, 'upper right',
                                      shadow=True)
        for _text in _leg.get_texts():
            _text.set_fontsize('small')

        # Set the proper labels on the derating curve.
        self.axsDerate1.set_xlabel(_(u"Temperature (\u2070C)"),
                                   fontdict={'fontsize': 12,
                                             'fontweight' : 'bold'})

        self.figDerate.tight_layout()

        frame.add(self.pltDerate)
        frame.show_all()

        return False
