#!/usr/bin/env python
"""
###################################################
Capacitor Package Component Specific Work Book View
###################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.gui.gtk.Capacitor.py is part of The RTK Project
#
# All rights reserved.

import sys

import pango

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
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Inputs(gtk.Frame):
    """
    The Work Book view for displaying all the attributes for a capacitor.  The
    attributes of a capacitor Work Book view are:
    """

    def __init__(self, model):
        """
        Creates an input frame for the Capacitor data model.

        :param :class `rtk.hardware.Capacitor.model`: the Capacitor data model
                                                      whose attributes will be
                                                      displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # ===== ===== === Initialize private list attributes === ===== ===== #
        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

        self._lst_labels = [_(u"Quality:"),
                            _(u"\u03C0<sub>Q</sub> Override:"),
                            _(u"Rated Voltage:"), _(u"Applied DC Voltage:"),
                            _(u"Applied AC Voltage:"),
                            _(u"Capacitance (F):")]
        self._lst_quality = []
        self._lst_specification = []
        self._lst_specsheet = []
        self._lst_construction = []

        self._lst_handler_id = []

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the input widgets common to all Capacitor types.
        self.cmbQuality = _widg.make_combo(simple=True)
        self.txtCommercialPiQ = _widg.make_entry(width=100)
        self.txtVoltRated = _widg.make_entry(width=100)
        self.txtVoltApplied = _widg.make_entry(width=100)
        self.txtACVoltApplied = _widg.make_entry(width=100)
        self.txtCapacitance = _widg.make_entry(width=100)

        # Subcategory specific attributes.
        if self._subcategory in [40, 42, 43, 46, 47, 48, 49, 50, 52]:
            self._lst_labels.append(_(u"Specification:"))
            self.cmbSpecification = _widg.make_combo(simple=True)
        if self._subcategory in [40, 42, 43, 44, 46, 47, 48, 49, 50, 52, 53,
                                 55, 56, 57, 58]:
            self._lst_labels.append(_(u"Spec. Sheet:"))
            self.cmbSpecSheet = _widg.make_combo(simple=True)

        if self._subcategory == 51:         # Solid tantalum
            self._lst_quality = ["", "D", "C", "S", "B", "R", "P", "M", "L",
                                 _(u"Lower")]
            self._lst_specification = ["", "MIL-C-39003 (CSR)"]
            self._lst_specsheet = [["", _(u"All")]]

            self._lst_labels.append(_(u"Eff. Series Resistance:"))

            self.txtEffResistance = _widg.make_entry(width=100)

        elif self._subcategory == 52:       # Non-solid tantalum
            self._lst_quality = ["", "S", "R", "P", "M", "L",
                                 _(u"MIL-C-3965, Non-Established Reliability"),
                                 _(u"Lower")]
            self._lst_specification = ["", "MIL-C-3965 (CL)",
                                       "MIL-C-39003 (CLR)"]
            self._lst_specsheet = [["", u"85\u00B0C", u"125\u00B0C",
                                    u"175\u00B0C"], ["", u"125\u00B0C"]]
            self._lst_construction = ["", _(u"Slug, All Tantalum"),
                                      _(u"Foil, Hermetic"),
                                      _(u"Slug, Hermetic"),
                                      _(u"Foil, Non-Hermetic"),
                                      _(u"Slug, Non-Hermetic")]

            self._lst_labels[3] = _(u"Temperature Rating:")
            self._lst_labels.append(_(u"Construction:"))

            self.cmbConstruction = _widg.make_combo(simple=True)

        elif self._subcategory == 53:       # Wet aluminum
            self._lst_quality = ["", "S", "R", "P", "M",
                                 _(u"Non-Established Reliability"),
                                 _(u"Lower")]
            self._lst_specification = ["", "MIL-C-39016 (CU and CUR)"]
            self._lst_specsheet = [["", u"85\u00B0C"]]

            self._lst_labels[3] = _(u"Temperature Rating:")

        elif self._subcategory == 54:       # Dry aluminum
            self._lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            self._lst_specification = ["", "MIL-C-62 (CE)"]
            self._lst_specsheet = [["", u"85\u00B0C", u"105\u00B0C",
                                    u"125\u00B0C"]]

            self._lst_labels[3] = _(u"Temperature Rating:")

    def create_217_stress_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress input widgets for Capacitors.

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

        # Place the input widgets common to all Capacitor types.
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtCommercialPiQ, _x_pos, _y_pos[1])
        _fixed.put(self.txtVoltRated, _x_pos, _y_pos[2])
        _fixed.put(self.txtVoltApplied, _x_pos, _y_pos[3])
        _fixed.put(self.txtACVoltApplied, _x_pos, _y_pos[4])
        _fixed.put(self.txtCapacitance, _x_pos, _y_pos[5])

        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, _index)) #0
        _index += 1
        self._lst_handler_id.append(
            self.txtCommercialPiQ.connect('focus-out-event',
                                          self._on_focus_out, _index))  #1
        _index += 1
        self._lst_handler_id.append(
            self.txtVoltRated.connect('focus-out-event',
                                      self._on_focus_out, _index))  #2
        _index += 1
        self._lst_handler_id.append(
            self.txtVoltApplied.connect('focus-out-event',
                                        self._on_focus_out, _index))    #3
        _index += 1
        self._lst_handler_id.append(
            self.txtACVoltApplied.connect('focus-out-event',
                                          self._on_focus_out, _index))  #4
        _index += 1
        self._lst_handler_id.append(
            self.txtCapacitance.connect('focus-out-event',
                                        self._on_focus_out, _index))    #5
        _index += 1

        # Subcategory specific widgets.
        if self._subcategory in [40, 42, 43, 46, 47, 48, 49, 50, 52]:
            for i in range(len(self._lst_specification)):
                self.cmbSpecification.insert_text(i,
                                                  self._lst_specification[i])

            _fixed.put(self.cmbSpecification, _x_pos, _y_pos[6])
            self._lst_handler_id.append(
                self.cmbSpecification.connect('changed',
                                              self._on_combo_changed, _index))
            _index += 1
        if self._subcategory in [40, 42, 43, 44, 46, 47, 48, 49, 50, 52, 53,
                                 55, 56, 57, 58]:
            _fixed.put(self.cmbSpecSheet, _x_pos, _y_pos[7])
            self._lst_handler_id.append(
                self.cmbSpecSheet.connect('changed',
                                          self._on_combo_changed, _index))
            _index += 1

        if self._subcategory == 51:         # Solid tantalum
            _fixed.put(self.txtEffResistance, _x_pos, _y_pos[6])
            self._lst_handler_id.append(
                self.txtEffResistance.connect('focus-out-event',
                                              self._on_focus_out, _index))  #6
            _index += 1
        elif self._subcategory == 52:       # Non-solid tantalum
            for i in range(len(self._lst_construction)):
                self.cmbConstruction.insert_text(i, self._lst_construction[i])
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[8])
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index)) #8
            _index += 1
        elif self._subcategory == 58:       # Gas or vacuum
            for i in range(len(self._lst_construction)):
                self.cmbConfiguraiton.insert_text(i,
                                                  self._lst_configuration[i])
            _fixed.put(self.cmbConfiguration, _x_pos, _y_pos[7])
            self._lst_handler_id.append(
                self.cmbConfiguration.connect('changed',
                                              self._on_combo_changed, _index))    #7
            _index += 1

        _fixed.show_all()

        return _x_pos

    def load_217_stress_inputs(self, model):
        """
        Loads the Capacitor class gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.cmbQuality.set_active(int(model.quality))
        self.txtCommercialPiQ.set_text(str(fmt.format(model.q_override)))
        self.txtVoltRated.set_text(str(fmt.format(model.rated_voltage)))
        self.txtVoltApplied.set_text(str(fmt.format(model.operating_voltage)))
        self.txtACVoltApplied.set_text(str(fmt.format(model.acvapplied)))
        self.txtCapacitance.set_text(str('{0:0.8G}'.format(model.capacitance)))

        # Load subcategory specific widgets.
        if self._subcategory in [40, 42, 43, 46, 47, 48, 49, 50, 52]:
            self.cmbSpecification.set_active(int(model.specification))
        if self._subcategory in [40, 42, 43, 44, 46, 47, 48, 49, 50, 52, 53,
                                 55, 56, 57, 58]:
            self.cmbSpecSheet.set_active(int(model.spec_sheet))
        if self._subcategory == 51:
            self.txtEffResistance.set_text(
                str(fmt.format(model.effective_resistance)))
        if self._subcategory == 52:
            self.cmbConstruction.set_active(int(model.construction))

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
        elif index == 4:
            self._hardware_model.specification = combo.get_active()
        elif index == 5:
            self._hardware_model.spec_sheet = combo.get_active()
        elif index == 6 and self._subcategory == 52:
            self._hardware_model.construction = combo.get_active()
        elif index == 5 and self._subcategory == 58:
            self._hardware_model.configuration = combo.get_active()

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
        elif index == 2:
            self._hardware_model.rated_voltage = float(entry.get_text())
        elif index == 3:
            self._hardware_model.operating_voltage = float(entry.get_text())
        elif index == 4:
            self._hardware_model.acvapplied = float(entry.get_text())
        elif index == 5:
            self._hardware_model.capacitance = float(entry.get_text())
        elif index == 6 and self._subcategory == 51:
            self._hardware_model.effective_resistance = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    capacitor.  The output attributes of a capacitor Work Book view are:
    """

    def __init__(self, model):
        """
        Initializes an instance of the Capacitor assessment results view.

        :param int subcategory: the Capacitor subcategory ID of the component
                                to create the view for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Initialize private list attributes.
        self._lst_labels = ['', u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:", u"\u03C0<sub>CV</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiCV = _widg.make_entry(width=100, editable=False, bold=True)

        # Subcategory specific attributes.
        if self._subcategory == 51:         # Solid tantalum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub>\u03C0<sub>SR</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>SR</sub>:")

            self.txtPiSR = _widg.make_entry(width=100, editable=False,
                                            bold=True)

        elif self._subcategory == 52:       # Non-solid tantalum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub>\u03C0<sub>C</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>C</sub>:")

            self.txtPiC = _widg.make_entry(width=100, editable=False,
                                           bold=True)

        elif self._subcategory == 53:       # Wet aluminum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub></span>"

        elif self._subcategory == 54:       # Dry aluminum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub></span>"

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Capacitors.

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
        _x_pos = max(x_pos, _x_pos) + 25

        # Place the reliability result display widgets.
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[3])
        _fixed.put(self.txtPiCV, _x_pos, _y_pos[4])

        # Subcategory specific widgets.
        if self._subcategory == 51:
            _fixed.put(self.txtPiSR, _x_pos, _y_pos[5])
        elif self._subcategory == 52:
            _fixed.put(self.txtPiC, _x_pos, _y_pos[5])

        _fixed.show_all()

        return _x_pos

    def load_217_stress_results(self, model):
        """
        Loads the Capacitor class result gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))
        self.txtPiCV.set_text(str(fmt.format(model.piCV)))

        if self._subcategory == 51:
            self.txtPiSR.set_text(str(fmt.format(model.piSR)))
        elif self._subcategory == 52:
            self.txtPiC.set_text(str(fmt.format(model.piC)))

        return False
