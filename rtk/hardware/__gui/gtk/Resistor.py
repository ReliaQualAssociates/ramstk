#!/usr/bin/env python
"""
#################################################
Resistor Module Component Specific Work Book View
#################################################
"""

# -*- coding: utf-8 -*-
#
#       hardware.gui.gtk.Resistor.py is part of The RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

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
<<<<<<< HEAD
matplotlib.use('GTK')
=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

# Import other RTK modules.
try:
<<<<<<< HEAD
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg
=======
    import Configuration
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
<<<<<<< HEAD
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
=======
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

<<<<<<< HEAD
=======
matplotlib.use('GTK')

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

class Inputs(gtk.Frame):
    """
    The Work Book view for displaying all the attributes for a resistor.  The
    attributes of a resistor Work Book view are:
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Creates an input frame for the Resistor data model.

        :param :class `rtk.hardware.Resistor.model`: the Resistor data model
                                                     whose attributes will be
                                                     displayed.
        """

=======
        Method to create an input frame for the Resistor data model.

        :param model: the :py:class:`rtk.hardware.component.resistor.Resistor.Model`
                      whose attributes will be displayed.
        """
# TODO: Re-write __init__; current McCabe Complexity metrix = 24.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

<<<<<<< HEAD
        # ===== ===== === Initialize private list attributes === ===== ===== #
        self._lst_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:"),
                            _(u"Resistance (\u03A9):")]
        self._lst_handler_id = []
        self._lst_style = []

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # ===== = Create the input widgets common to all Resistor types = ===== #
        self.cmbQuality = _widg.make_combo(simple=True)
        self.txtQOverride = _widg.make_entry(width=100)
        self.txtResistance = _widg.make_entry(width=100)

        # Create the tooltips for the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected resistor."))
=======
        # Define private list attributes.
        self._lst_count_labels = [_(u"Quality:")]
        self._lst_stress_labels = [_(u"Quality:"),
                                   _(u"\u03C0<sub>Q</sub> Override:"),
                                   _(u"Resistance (\u03A9):")]
        self._lst_handler_id = []
        self._lst_style = []

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public scalar attributes.
        self.cmbCharacteristic = Widgets.make_combo(simple=True)
        self.cmbConstruction = Widgets.make_combo(simple=True)
        self.cmbQuality = Widgets.make_combo(simple=True)
        self.cmbSpecification = Widgets.make_combo(simple=True)
        self.cmbStyle = Widgets.make_combo(simple=True)
        self.cmbType = Widgets.make_combo(simple=True)
        self.txtNResistors = Widgets.make_entry(width=100)
        self.txtNTaps = Widgets.make_entry(width=100)
        self.txtQOverride = Widgets.make_entry(width=100)
        self.txtResistance = Widgets.make_entry(width=100)

        # Create the tooltips for the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"resistor."))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.txtQOverride.set_tooltip_text(_(u"Enter and display the the "
                                             u"user-defined quality factor "
                                             u"for the selected resistor."))
        self.txtResistance.set_tooltip_text(_(u"Enter and display the nominal "
                                              u"resistance of the selected "
                                              u"resistor."))

        # Connect signals to callback functions.
<<<<<<< HEAD
        _index = 0
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed',
                                    self._on_combo_changed, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtQOverride.connect('focus-out-event',
                                      self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtResistance.connect('focus-out-event',
                                       self._on_focus_out, _index))
        _index += 1
=======
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.txtQOverride.connect('focus-out-event',
                                      self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtResistance.connect('focus-out-event',
                                       self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed',
                                          self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.txtNResistors.connect('focus-out-event',
                                       self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.cmbStyle.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbCharacteristic.connect('changed',
                                           self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.txtNTaps.connect('focus-out-event', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 8))
        self._lst_handler_id.append(
            self.cmbType.connect('changed', self._on_combo_changed, 9))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        # Create the input widgets specific to Resistor subcategories.
        if self._subcategory == 25:         # Carbon composition
            _lst_quality = ["", "S", "R", "P", "M", "MIL-R-11", _(u"Lower")]

        elif self._subcategory == 26:       # Carbon film
<<<<<<< HEAD
            self._lst_labels.append(_(u"Specification:"))

            self.cmbSpecification = _widg.make_combo(simple=True)
=======
            self._lst_stress_labels.append(_(u"Specification:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.cmbSpecification.set_tooltip_text(_(u"Select and display the "
                                                     u"specification for the "
                                                     u"selected resistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "S", "R", "P", "M", "MIL-R-10509",
                            "MIL-R-22684", _("Lower")]
            _lst_specification = ["", "MIL-R-10509 (RN)", "MIL-R-22684 (RL)",
                                  "MIL-R-39017 (RLR)",
                                  "MIL-R-55182 (RNR, RNC, RNN)"]

            for _index, _specification in enumerate(_lst_specification):
                self.cmbSpecification.insert_text(_index, _specification)

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbSpecification.connect('changed',
                                              self._on_combo_changed, _index))

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        elif self._subcategory == 27:       # Carbon film power
            # Populate the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]

        elif self._subcategory == 28:       # Carbon film network
<<<<<<< HEAD
            self._lst_labels.append(_(u"# of Active Resistors:"))

            self.txtNResistors = _widg.make_entry(width=100)
=======
            self._lst_stress_labels.append(_(u"# of Active Resistors:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.txtNResistors.set_tooltip_text(_(u"Enter and display the "
                                                  u"number of active "
                                                  u"resistors in the selected "
                                                  u"resistor network."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.txtNResistors.connect('focus-out-event',
                                           self._on_focus_out, _index))

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        elif self._subcategory == 29:       # Wirewound
            _lst_quality = ["", "S", "R", "P", "M", "MIL-R-93", _(u"Lower")]

        elif self._subcategory == 30:       # Wirewound power
<<<<<<< HEAD
            self._lst_labels.append(_(u"Specification:"))
            self._lst_labels.append(_(u"Style:"))

            self.cmbSpecification = _widg.make_combo(simple=True)
            self.cmbStyle = _widg.make_combo(simple=True)
=======
            self._lst_stress_labels.append(_(u"Specification:"))
            self._lst_stress_labels.append(_(u"Style:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.cmbSpecification.set_tooltip_text(_(u"Select and display the "
                                                     u"specification for the "
                                                     u"selected resistor."))
            self.cmbStyle.set_tooltip_text(_(u"Select and display the style "
                                             u"of the selected resistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "S", "R", "P", "M", "MIL-R-26", _(u"Lower")]
            _lst_specification = ["", "MIL-R-39007 (RWR)", "MIL-R-26 (RW)"]
            self._lst_style = [["", "RWR 71", "RWR 74", "RWR 78", "RWR 80",
                                "RWR 81", "RWR 82", "RWR 84", "RWR 89"],
                               ["", "RW 10", "RW 11", "RW 12", "RW 13",
                                "RW 14", "RW 15", "RW 16", "RW 20", "RW 21",
                                "RW 22", "RW 23", "RW 24", "RW 29", "RW 30",
                                "RW 31", "RW 32", "RW 33", "RW 34", "RW 35",
                                "RW 36", "RW 37", "RW 38", "RW 39", "RW 47",
                                "RW 55", "RW 56", "RW 67", "RW 68", "RW 69",
                                "RW 70", "RW 74", "RW 78", "RW 79", "RW 80",
                                "RW 81"]]

            for _index, _specification in enumerate(_lst_specification):
                self.cmbSpecification.insert_text(_index, _specification)

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbSpecification.connect('changed',
                                              self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbStyle.connect('changed',
                                      self._on_combo_changed, _index))

        elif self._subcategory == 31:       # Wirewound chassis mount
            self._lst_labels.append(_(u"Characteristic:"))
            self._lst_labels.append(_(u"Style:"))

            self.cmbCharacteristic = _widg.make_combo(simple=True)
            self.cmbStyle = _widg.make_combo(simple=True)
=======
        elif self._subcategory == 31:       # Wirewound chassis mount
            self._lst_stress_labels.append(_(u"Characteristic:"))
            self._lst_stress_labels.append(_(u"Style:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.cmbCharacteristic.set_tooltip_text(_(u"Select and display "
                                                      u"the winding "
                                                      u"characteristic for "
                                                      u"the selected "
                                                      u"resistor."))
            self.cmbStyle.set_tooltip_text(_(u"Select and display the style "
                                             u"of the selected resistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "S", "R", "P", "M", "MIL-R-18546", _(u"Lower")]
            _lst_characteristic = ["", _(u"Inductively Wound"),
                                   _(u"Non-Inductively Wound")]
<<<<<<< HEAD
            _lst_style = [["", "RER 60", "RER 65", "RER 70", "RER 75"],
                          ["", "RE 60", "RE 65", "RE 70", "RE 77", "RE 80"]]
=======
            self._lst_style = [["", "RER 60", "RER 65", "RER 70", "RER 75"],
                               ["", "RE 60", "RE 65", "RE 70", "RE 77",
                                "RE 80"]]
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            for _index, _characteristic in enumerate(_lst_characteristic):
                self.cmbCharacteristic.insert_text(_index, _characteristic)

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbCharacteristic.connect('changed',
                                               self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbStyle.connect('changed',
                                      self._on_combo_changed, _index))

        elif self._subcategory == 32:       # Thermistor
            self._lst_labels.append(_(u"Type:"))

            self.cmbType = _widg.make_combo(simple=True)
=======
        elif self._subcategory == 32:       # Thermistor
            self._lst_stress_labels.append(_(u"Type:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.cmbType.set_tooltip_text(_(u"Select and display the type of "
                                            u"the selected thermistor."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            _lst_type = ["", _(u"Bead"), _(u"Disk"), _(u"Rod")]

            for _index, _type in enumerate(_lst_type):
                self.cmbType.insert_text(_index, _type)

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbType.connect('changed',
                                     self._on_combo_changed, _index))

        elif self._subcategory == 33:       # Variable wirewound
            self._lst_labels.append(_(u"# of Taps:"))

            self.txtNTaps = _widg.make_entry(width=100)
=======
        elif self._subcategory == 33:       # Variable wirewound
            self._lst_stress_labels.append(_(u"# of Taps:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.txtNTaps.set_tooltip_text(_(u"Enter and display the number "
                                             u"of potentiometer taps "
                                             u"including the wiper and "
                                             u"terminations."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "S", "R", "P", "M", "MIL-R-27208", _(u"Lower")]

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.txtNTaps.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 34:       # Variable wirewound precisison
            self._lst_labels.append(_(u"Construction:"))
            self._lst_labels.append(_(u"# of Taps:"))

            self.cmbConstruction = _widg.make_combo(simple=True)
            self.txtNTaps = _widg.make_entry(width=100)
=======
        elif self._subcategory == 34:       # Variable wirewound precisison
            self._lst_stress_labels.append(_(u"Construction:"))
            self._lst_stress_labels.append(_(u"# of Taps:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.cmbConstruction.set_tooltip_text(_(u"Select and display the "
                                                    u"construction class for "
                                                    u"the selected resistor."))
            self.txtNTaps.set_tooltip_text(_(u"Enter and display the number "
                                             u"of potentiometer taps "
                                             u"including the wiper and "
                                             u"terminations."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            _lst_construction = ["", _(u"Class 2"), _(u"Class 3"),
                                 _(u"Class 4"), _(u"Class 5")]

            for _index, _construction in enumerate(_lst_construction):
                self.cmbConstruction.insert_text(_index, _construction)

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNTaps.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 35:       # Variable wirewound semi-precision
            self._lst_labels.append(_(u"# of Taps:"))

            self.txtNTaps = _widg.make_entry(width=100)
=======
        elif self._subcategory == 35:       # Variable wirewound semi-precision
            self._lst_stress_labels.append(_(u"# of Taps:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.txtNTaps.set_tooltip_text(_(u"Enter and display the number "
                                             u"of potentiometer taps "
                                             u"including the wiper and "
                                             u"terminations."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.txtNTaps.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 36:       # Variable wirewound power
            self._lst_labels.append(_(u"Construction:"))
            self._lst_labels.append(_(u"# of Taps:"))

            self.cmbConstruction = _widg.make_combo(simple=True)
            self.txtNTaps = _widg.make_entry(width=100)
=======
        elif self._subcategory == 36:       # Variable wirewound power
            self._lst_stress_labels.append(_(u"Construction:"))
            self._lst_stress_labels.append(_(u"# of Taps:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.cmbConstruction.set_tooltip_text(_(u"Select and display the "
                                                    u"construction class for "
                                                    u"the selected resistor."))
            self.txtNTaps.set_tooltip_text(_(u"Enter and display the number "
                                             u"of potentiometer taps "
                                             u"including the wiper and "
                                             u"terminations."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            _lst_construction = ["", _(u"Enclosed"), _(u"Unenclosed")]

            for _index, _construction in enumerate(_lst_construction):
                self.cmbConstruction.insert_text(_index, _construction)

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNTaps.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 37:       # Variable non-wirewound
            self._lst_labels.append(_(u"# of Taps:"))

            self.txtNTaps = _widg.make_entry(width=100)
=======
        elif self._subcategory == 37:       # Variable non-wirewound
            self._lst_stress_labels.append(_(u"# of Taps:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.txtNTaps.set_tooltip_text(_(u"Enter and display the number "
                                             u"of potentiometer taps "
                                             u"including the wiper and "
                                             u"terminations."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "S", "R", "P", "M", "MIL-R-22097", _(u"Lower")]

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.txtNTaps.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 38:       # Variable composition
            self._lst_labels.append(_(u"# of Taps:"))

            self.txtNTaps = _widg.make_entry(width=100)
=======
        elif self._subcategory == 38:       # Variable composition
            self._lst_stress_labels.append(_(u"# of Taps:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.txtNTaps.set_tooltip_text(_(u"Enter and display the number "
                                             u"of potentiometer taps "
                                             u"including the wiper and "
                                             u"terminations."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.txtNTaps.connect('focus-out-event',
                                      self._on_focus_out, _index))

        elif self._subcategory == 39:       # Variable film
            self._lst_labels.append(_(u"Specification:"))
            self._lst_labels.append(_(u"# of Taps:"))

            self.cmbSpecification = _widg.make_combo(simple=True)
            self.txtNTaps = _widg.make_entry(width=100)
=======
        elif self._subcategory == 39:       # Variable film
            self._lst_stress_labels.append(_(u"Specification:"))
            self._lst_stress_labels.append(_(u"# of Taps:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Create the tooltips for the input widgets.
            self.cmbSpecification.set_tooltip_text(_(u"Select and display the "
                                                     u"governing "
                                                     u"specification for "
                                                     u"the selected "
                                                     u"resistor."))
            self.txtNTaps.set_tooltip_text(_(u"Enter and display the number "
                                             u"of potentiometer taps "
                                             u"including the wiper and "
                                             u"terminations."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            _lst_specification = ["", "MIL-R-39023 (RQ)", "MIL-R-23285 (RVC)"]
            self._lst_style = [["", "RQ090", "RQ100", "RQ110", "RQ150",
                                "RQ160", "RQ200", "RQ210", "RQ300"],
                               ["", "RVC5", "RVC6"]]

            for _index, _specification in enumerate(_lst_specification):
                self.cmbSpecification.insert_text(_index, _specification)

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbSpecification.connect('changed',
                                              self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNTaps.connect('focus-out-event',
                                      self._on_focus_out, _index))

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        # Populate the quality gtk.ComboBox().
        for _index, _quality in enumerate(_lst_quality):
            self.cmbQuality.insert_text(_index, _quality)

    def create_217_count_inputs(self, x_pos=5):
        """
<<<<<<< HEAD
        Creates the MIL-HDBK-217FN2 part count input widgets for Resistors.
=======
        Method to create the MIL-HDBK-217FN2 parts count input widgets for
        Resistors.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :keyword int x_pos: the x position of the display widgets.
        :return: False if successful or True if an error is encountered.
        """

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
<<<<<<< HEAD
                          _(u"MIL-HDBK-217FN2 Part Count Inputs") +
=======
                          _(u"MIL-HDBK-217FN2 Parts Count Inputs") +
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
                          "</span>")
        _label.set_justify(gtk.JUSTIFY_LEFT)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.show_all()
        self.set_label_widget(_label)

        _fixed = gtk.Fixed()

<<<<<<< HEAD
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels[:3],
                                             _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtQOverride, _x_pos, _y_pos[1])
        _fixed.put(self.txtResistance, _x_pos, _y_pos[2])
=======
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_count_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        if self.cmbQuality.get_parent() is not None:
            self.cmbQuality.reparent(_fixed)
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.add(_scrollwindow)

        _fixed.show_all()

        return x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
<<<<<<< HEAD
        Creates the MIL-HDBK-217FN2 part stress input widgets for Resistors.
=======
        Method to create the MIL-HDBK-217FN2 part stress input widgets for
        Resistors.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :keyword int x_pos: the x position of the display widgets.
        :return: False if successful or True if an error is encountered.
        """
<<<<<<< HEAD

=======
# TODO: Re-write create_217_stress_inputs; current McCabe Complexity metrix = 13.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
=======
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
        if self.cmbQuality.get_parent() is not None:
            self.cmbQuality.reparent(_fixed)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtQOverride, _x_pos, _y_pos[1])
        _fixed.put(self.txtResistance, _x_pos, _y_pos[2])

        if self._subcategory == 26:         # Carbon film
            _fixed.put(self.cmbSpecification, _x_pos, _y_pos[3])
        elif self._subcategory == 28:       # Carbon film network
            _fixed.put(self.txtNResistors, _x_pos, _y_pos[3])
        elif self._subcategory == 30:       # Wirewound power
            _fixed.put(self.cmbSpecification, _x_pos, _y_pos[3])
            _fixed.put(self.cmbStyle, _x_pos, _y_pos[4])
        elif self._subcategory == 31:       # Wirewound chassis mount
            _fixed.put(self.cmbCharacteristic, _x_pos, _y_pos[3])
            _fixed.put(self.cmbStyle, _x_pos, _y_pos[4])
        elif self._subcategory == 32:       # Thermistor
            _fixed.put(self.cmbType, _x_pos, _y_pos[3])
        elif self._subcategory == 33:       # Variable wirewound
            _fixed.put(self.txtNTaps, _x_pos, _y_pos[3])
        elif self._subcategory == 34:       # Variable wirewound precision
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[3])
            _fixed.put(self.txtNTaps, _x_pos, _y_pos[4])
        elif self._subcategory == 35:       # Variable wirewound semi-precision
            _fixed.put(self.txtNTaps, _x_pos, _y_pos[3])
        elif self._subcategory == 36:       # Variable wirewound power
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[3])
            _fixed.put(self.txtNTaps, _x_pos, _y_pos[4])
        elif self._subcategory == 37:       # Variable non-wirewound
            _fixed.put(self.txtNTaps, _x_pos, _y_pos[3])
        elif self._subcategory == 38:       # Variable composition
            _fixed.put(self.txtNTaps, _x_pos, _y_pos[3])
        elif self._subcategory == 39:       # Variable film
            _fixed.put(self.cmbSpecification, _x_pos, _y_pos[3])
            _fixed.put(self.txtNTaps, _x_pos, _y_pos[4])

        _fixed.show_all()

        return _x_pos

<<<<<<< HEAD
    def load_217_stress_inputs(self, model):
        """
        Loads the Resistor class MIL-HDBK-217FN2 part stress gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
=======
    def load_217_count_inputs(self, model):
        """
        Method to load the Resistor class MIL-HDBK-217FN2 parts count input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.resistor.Resistor.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbQuality.set_active(model.quality)

        return False

    def load_217_stress_inputs(self, model):
        """
        Method to load the Resistor class MIL-HDBK-217FN2 part stress input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.resistor.Resistor.Model`
                      to load the attributes from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

<<<<<<< HEAD
        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'
=======
        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.cmbQuality.set_active(model.quality)
        self.txtQOverride.set_text(str(fmt.format(model.q_override)))
        self.txtResistance.set_text(str(fmt.format(model.resistance)))

<<<<<<< HEAD
        if self._subcategory == 26:         # Carbon film
            self.cmbSpecification.set_active(model.specification)
        elif self._subcategory == 28:       # Carbon film network
            self.txtNResistors.set_text(str(model.n_resistors))
        elif self._subcategory == 30:       # Wirewound power
            self.cmbSpecification.set_active(model.specification)
            self.cmbStyle.set_active(model.style)
        elif self._subcategory == 31:       # Wirewound chassis mount
            self.cmbCharacteristic.set_active(model.characteristic)
            self.cmbStyle.set_active(model.style)
        elif self._subcategory == 32:       # Thermistor
            self.cmbType.set_active(model.type)
        elif self._subcategory in [33, 34, 35, 36, 37, 38, 39]:
            self.txtNTaps.set_text(str(model.n_taps))
        elif self._subcategory == 34:       # Variable wirewound precision
            self.cmbConstruction.set_active(model.construction)
        elif self._subcategory == 36:       # Variable wirewound power
            self.cmbConstruction.set_active(model.construction)
        elif self._subcategory == 39:       # Variable film
            self.cmbSpecification.set_active(model.style)
=======
        if self._subcategory in [26, 39]:
            self.cmbSpecification.set_active(model.specification)
        if self._subcategory == 28:
            self.txtNResistors.set_text(str(model.n_resistors))
        if self._subcategory == 30:
            self.cmbSpecification.set_active(model.specification)
            self.cmbStyle.set_active(model.style)
        if self._subcategory == 31:
            self.cmbCharacteristic.set_active(model.characteristic)
            self.cmbStyle.set_active(model.style)
        if self._subcategory == 32:
            self.cmbType.set_active(model.type)
        if self._subcategory in [33, 34, 35, 36, 37, 38, 39]:
            self.txtNTaps.set_text(str(model.n_taps))
        if self._subcategory in [34, 36]:
            self.cmbConstruction.set_active(model.construction)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        return False

    def _on_combo_changed(self, combo, index):
        """
<<<<<<< HEAD
        Responds to gtk.ComboBox() changed signals and calls the correct
        function or method, passing any parameters as needed.
=======
        Method to respond to gtk.ComboBox() changed signals and calls the
        correct function or method, passing any parameters as needed.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
        elif index == 3 and self._subcategory == 26:
            self._hardware_model.specification = combo.get_active()
        elif index == 3 and self._subcategory in [30, 39]:
            self._hardware_model.specification = combo.get_active()
            self._load_styles(self._hardware_model.specification)
        elif index == 3 and self._subcategory == 31:
            self._hardware_model.characteristic = combo.get_active()
        elif index == 3 and self._subcategory == 32:
            self._hardware_model.type = combo.get_active()
        elif index == 3 and self._subcategory in [34, 36]:
            self._hardware_model.construction = combo.get_active()
        elif index == 4 and self._subcategory in [30, 31]:
            self._hardware_model.style = combo.get_active()
=======
        elif index == 3:
            self._hardware_model.specification = combo.get_active()
            if self._subcategory in [30, 39]:
                self._load_styles(self._hardware_model.specification)
        elif index == 5:
            self._hardware_model.style = combo.get_active()
        elif index == 6:
            self._hardware_model.characteristic = combo.get_active()
            if self._subcategory == 31:
                self._load_styles(self._hardware_model.characteristic)
        elif index == 8:
            self._hardware_model.construction = combo.get_active()
        elif index == 9:
            self._hardware_model.type = combo.get_active()
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
<<<<<<< HEAD
        Responds to gtk.Entry() focus_out signals and calls the correct
        function or method, passing any parameters as needed.
=======
        Method to respond to gtk.Entry() focus_out signals and calls the
        correct function or method, passing any parameters as needed.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
        elif index == 3 and self._subcategory == 28:
            self._hardware_model.n_resistors = int(entry.get_text())
        elif index == 3 and self._subcategory in [33, 35, 37, 38]:
            self._hardware_model.n_taps = int(entry.get_text())
        elif index == 4 and self._subcategory in [34, 36, 39]:
=======
        elif index == 2:
            self._hardware_model.resistance = float(entry.get_text())
        elif index == 4:
            self._hardware_model.n_resistors = int(entry.get_text())
        elif index == 7:
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            self._hardware_model.n_taps = int(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _load_styles(self, specification):
        """
        Method to load the style gtk.Combo() depending on the selected
        specification.

        :param int specification: the selected specifications index.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Remove existing entries.
        _model = self.cmbStyle.get_model()
        _model.clear()

        # Load the new entries.
        _n_styles = len(self._lst_style[specification - 1])
        for i in range(_n_styles):
            self.cmbStyle.insert_text(
                i, self._lst_style[specification - 1][i])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    Resistor.  The output attributes of a Resistor Work Book view are:
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Initializes an instance of the Resistor assessment results view.

        :param model: the instance of the Resistor data model to create the view
                      for.
=======
        Method to initialize an instance of the Resistor assessment results
        view.

        :param model: the :py:class:`rtk.hardware.component.resistor.Resistor.Model`
                      to create the view for.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

<<<<<<< HEAD
        # Initialize private list attributes.
        self._lst_labels = ["", u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = \u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>",
                                  u"\u03BB<sub>g</sub>:",
                                  u"\u03C0<sub>Q</sub>:"]
        self._lst_stress_labels = ["", u"\u03BB<sub>b</sub>:",
                                   u"\u03C0<sub>Q</sub>:",
                                   u"\u03C0<sub>E</sub>:"]

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.txtLambdaB = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtPiQ = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = Widgets.make_entry(width=100, editable=False, bold=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.figDerate = Figure(figsize=(6, 4))
        self.axsDerate = self.figDerate.add_subplot(111)
        self.pltDerate = FigureCanvas(self.figDerate)

        if self._subcategory in [25, 26, 27, 29, 30, 31]:
<<<<<<< HEAD
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>R</sub>:")

            self.txtPiR = _widg.make_entry(width=100, editable=False, bold=True)
=======
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>R</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>R</sub>:")

            self.txtPiR = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            self.txtPiR.set_tooltip_text(_(u"Displays the resistance factor "
                                           u"for the selected resistor."))

        elif self._subcategory == 28:
<<<<<<< HEAD
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>T</sub>:")
            self._lst_labels.append(u"\u03C0<sub>NR</sub>:")

            self.txtPiT = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiNR = _widg.make_entry(width=100,
                                            editable=False, bold=True)
=======
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>NR</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>T</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>NR</sub>:")

            self.txtPiT = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
            self.txtPiNR = Widgets.make_entry(width=100, editable=False,
                                              bold=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            self.txtPiT.set_tooltip_text(_(u"Displays the temperature factor "
                                           u"for the selected resistor."))
            self.txtPiNR.set_tooltip_text(_(u"Displays the number of "
                                            u"resistors factor for the "
                                            u"selected resistor."))

        elif self._subcategory == 32:
<<<<<<< HEAD
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

        elif self._subcategory in [34, 36]:
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>TAPS</sub>:")
            self._lst_labels.append(u"\u03C0<sub>C</sub>:")
            self._lst_labels.append(u"\u03C0<sub>R</sub>:")
            self._lst_labels.append(u"\u03C0<sub>V</sub>:")

            self.txtPiTAPS = _widg.make_entry(width=100,
                                              editable=False, bold=True)
            self.txtPiC = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiR = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiV = _widg.make_entry(width=100,
                                           editable=False, bold=True)
=======
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

        elif self._subcategory in [34, 36]:
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>C</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>TAPS</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>C</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>R</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>V</sub>:")

            self.txtPiTAPS = Widgets.make_entry(width=100, editable=False,
                                                bold=True)
            self.txtPiC = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
            self.txtPiR = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
            self.txtPiV = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            self.txtPiTAPS.set_tooltip_text(_(u"Displays the potentiometer "
                                              u"taps factor for the selected "
                                              u"resistor."))
            self.txtPiC.set_tooltip_text(_(u"Displays the construction class "
                                           u"factor for the selected "
                                           u"resistor."))
            self.txtPiR.set_tooltip_text(_(u"Displays the resistance factor "
                                           u"for the selected resistor."))
            self.txtPiV.set_tooltip_text(_(u"Displays the voltage factor "
                                           u"for the selected resistor."))

        elif self._subcategory in [33, 35, 37, 38, 39]:
<<<<<<< HEAD
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>TAPS</sub>:")
            self._lst_labels.append(u"\u03C0<sub>R</sub>:")
            self._lst_labels.append(u"\u03C0<sub>V</sub>:")

            self.txtPiTAPS = _widg.make_entry(width=100,
                                              editable=False, bold=True)
            self.txtPiR = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiV = _widg.make_entry(width=100,
                                           editable=False, bold=True)
=======
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>TAPS</sub>\u03C0<sub>R</sub>\u03C0<sub>V</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>TAPS</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>R</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>V</sub>:")

            self.txtPiTAPS = Widgets.make_entry(width=100, editable=False,
                                                bold=True)
            self.txtPiR = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
            self.txtPiV = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            self.txtPiTAPS.set_tooltip_text(_(u"Displays the potentiometer "
                                              u"taps factor for the selected "
                                              u"resistor."))
            self.txtPiR.set_tooltip_text(_(u"Displays the resistance factor "
                                           u"for the selected resistor."))
            self.txtPiV.set_tooltip_text(_(u"Displays the voltage factor "
                                           u"for the selected resistor."))

        # Create the tooltips for the common results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected resistor."))
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected resistor."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected resistor."))

<<<<<<< HEAD
    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Resistors.
=======
    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count result gtk.Widgets()
        for Resistors.

        :keyword int x_pos: the x position of the display widgets.
        :return: _x_pos: the x-coordinate of the widgets.
        :rtype: int
        """

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"MIL-HDBK-217FN2 Parts Count Results") +
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
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_count_labels, _fixed, 5, 25)
        _x_pos = max(x_pos, _x_pos) + 30

        # Place the reliability result display widgets.
        if self.txtLambdaB.get_parent() is not None:
            self.txtLambdaB.reparent(_fixed)
        if self.txtPiQ.get_parent() is not None:
            self.txtPiQ.reparent(_fixed)
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])

        _fixed.show_all()

        return _x_pos

    def create_217_stress_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress result gtk.Widgets()
        for Resistors.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 25)
=======
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 25)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _x_pos = max(x_pos, _x_pos) + 30

        if self._subcategory in [25, 26, 27, 29, 30, 31]:
            _fixed.put(self.txtPiR, _x_pos, _y_pos[4])

        elif self._subcategory == 28:
            _fixed.put(self.txtPiT, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiNR, _x_pos, _y_pos[5])

        elif self._subcategory in [34, 36]:
            _fixed.put(self.txtPiTAPS, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiC, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiR, _x_pos, _y_pos[6])
            _fixed.put(self.txtPiV, _x_pos, _y_pos[7])

        elif self._subcategory in [33, 35, 37, 38, 39]:
            _fixed.put(self.txtPiTAPS, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiR, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiV, _x_pos, _y_pos[6])

        # Place the reliability result display widgets.
<<<<<<< HEAD
=======
        if self.txtLambdaB.get_parent() is not None:
            self.txtLambdaB.reparent(_fixed)
        if self.txtPiQ.get_parent() is not None:
            self.txtPiQ.reparent(_fixed)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[3])

        _fixed.show_all()

        return _x_pos

<<<<<<< HEAD
    def load_217_stress_results(self, model):
        """
        Loads the Resistor class result gtk.Widgets().

        :param model: the Resistor data model to load the attributes from.
=======
    def load_217_count_results(self, model):
        """
        Method to load the Resistor class MIL-HDBK-217FN2 parts count result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.resistor.Resistor.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_217_stress_results(self, model):
        """
        Method to load the Resistor class MIL-HDBK-217FN2 part stress result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.resistor.Resistor.Model`
                      to load the attributes from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

<<<<<<< HEAD
        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'
=======
        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        if self._subcategory in [25, 26, 27, 29, 30, 31]:
            self.txtPiR.set_text(str(fmt.format(model.piR)))

        elif self._subcategory == 28:
            self.txtPiT.set_text(str(fmt.format(model.piT)))
            self.txtPiNR.set_text(str(fmt.format(model.piNR)))

        elif self._subcategory in [34, 36]:
            self.txtPiTAPS.set_text(str(fmt.format(model.piTAPS)))
            self.txtPiC.set_text(str(fmt.format(model.piC)))
            self.txtPiR.set_text(str(fmt.format(model.piR)))
            self.txtPiV.set_text(str(fmt.format(model.piV)))

        elif self._subcategory in [33, 35, 37, 38, 39]:
            self.txtPiTAPS.set_text(str(fmt.format(model.piTAPS)))
            self.txtPiR.set_text(str(fmt.format(model.piR)))
            self.txtPiV.set_text(str(fmt.format(model.piV)))

        return False

    def load_derate_plot(self, model, frame):
        """
<<<<<<< HEAD
        Loads the stress derate plot for the Resistor class.

        :param model: the Hardware data model to load the attributes from.
=======
        Method to load the stress derate plot for the Resistor class.

        :param model: the :py:class:`rtk.hardware.component.resistor.Resistor.Model`
                      to load the attributes from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :param gtk.Frame frame: the gtk.Frame() to embed the derate plot into.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Clear the operating point and derating curve for the component.  We
        # do this here so the component-specific GUI will set the proper x and
        # y-axis labels.
        self.axsDerate.cla()

        # Plot the derating curve and operating point.
        _x = [float(model.min_rated_temperature),
              float(model.knee_temperature),
              float(model.max_rated_temperature)]

        self.axsDerate.plot(_x, model.lst_derate_criteria[0], 'r.-',
                            linewidth=2)
        self.axsDerate.plot(_x, model.lst_derate_criteria[1], 'b.-',
                            linewidth=2)
        self.axsDerate.plot(model.temperature_active, model.power_ratio, 'go')
        if(_x[0] != _x[2] and
           model.lst_derate_criteria[1][0] != model.lst_derate_criteria[1][2]):
            self.axsDerate.axis([0.95 * _x[0], 1.05 * _x[2],
                                 model.lst_derate_criteria[1][2],
                                 1.05 * model.lst_derate_criteria[1][0]])
        else:
<<<<<<< HEAD
            self.axsDerate.cla().axis([0.95, 1.05, 0.0, 1.05])
=======
            self.axsDerate.axis([0.95, 1.05, 0.0, 1.05])
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.axsDerate.set_title(_(u"Power Derating Curve for %s at %s") %
                                 (model.part_number, model.ref_des),
                                 fontdict={'fontsize': 12,
                                           'fontweight': 'bold',
                                           'verticalalignment': 'baseline'})
        _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                         _(u"Power Operating Point")])
<<<<<<< HEAD
        _leg = self.axsDerate.legend(_legend, 'upper right', shadow=True)
=======
        _leg = self.axsDerate.legend(_legend, loc='upper right', shadow=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        for _text in _leg.get_texts():
            _text.set_fontsize('small')

        # Set the proper labels on the derating curve.
        self.axsDerate.set_xlabel(_(u"Temperature (\u2070C)"),
                                  fontdict={'fontsize': 12,
                                            'fontweight': 'bold'})
        self.axsDerate.set_ylabel(r'$\mathbf{P_{op} / P_{rated}}$',
                                  fontdict={'fontsize': 12,
                                            'fontweight': 'bold',
                                            'rotation': 'vertical',
                                            'verticalalignment': 'baseline'})

        self.figDerate.tight_layout()

        frame.add(self.pltDerate)
        frame.show_all()

        return False
