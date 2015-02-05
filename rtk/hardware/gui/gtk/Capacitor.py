#!/usr/bin/env python
"""
###################################################
Hardware Package Component Specific Work Book Views
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

    def __init__(self, subcategory):

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # Initialize private list attributes.
        self._lst_labels = [_(u"Quality:"),
                            _(u"\u03C0<sub>Q</sub> Override:"),
                            _(u"Specification:"), _(u"Spec. Sheet:"),
                            _(u"Rated Voltage:"), _(u"Applied DC Voltage:"),
                            _(u"Applied AC Voltage:"),
                            _(u"Capacitance (F):")]

        # Derating points for the derating curve.  The list at position 0 is
        # for severe environments.  The list at position 1 is for benign
        # environments.
        self._derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]

        # Initialize private scalar attributes.
        self._subcategory = subcategory

        # Create the input widgets.
        self.cmbQuality = _widg.make_combo(simple=True)
        self.cmbSpecification = _widg.make_combo(simple=True)
        self.cmbSpecSheet = _widg.make_combo(simple=True)

        self.txtCommercialPiQ = _widg.make_entry(width=100)
        self.txtVoltRated = _widg.make_entry(width=100)
        self.txtVoltApplied = _widg.make_entry(width=100)
        self.txtACVoltApplied = _widg.make_entry(width=100)
        self.txtCapacitance = _widg.make_entry(width=100)

        # Subcategory specific attributes.
        if subcategory == 51:               # Solid tantalum
            self._lst_quality = ["", "D", "C", "S", "B", "R", "P", "M", "L",
                                 _(u"Lower")]
            self._lst_specification = ["", "MIL-C-39003 (CSR)"]
            self._lst_specsheet = [["", _(u"All")]]

            self._lst_labels.append(_(u"Eff. Series Resistance:"))

            self.txtEffResistance = _widg.make_entry(width=100)

        elif subcategory == 52:             # Non-solid tantalum
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

        elif subcategory == 53:             # Wet aluminum
            self._lst_quality = ["", "S", "R", "P", "M",
                                 _(u"Non-Established Reliability"),
                                 _(u"Lower")]
            self._lst_specification = ["", "MIL-C-39016 (CU and CUR)"]
            self._lst_specsheet = [["", u"85\u00B0C"]]

            self._lst_labels[3] = _(u"Temperature Rating:")

        elif subcategory == 54:             # Dry aluminum
            self._lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            self._lst_specification = ["", "MIL-C-62 (CE)"]
            self._lst_specsheet = [["", u"85\u00B0C", u"105\u00B0C",
                                    u"125\u00B0C"]]

            self._lst_labels[3] = _(u"Temperature Rating:")

    def create_217_stress_inputs(self, x_pos):
        """
        Creates the MIL-HDBK-217FN2 part stress input widgets for Capacitors.

        :param int x_pos: the x position of the display widgets.
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
        for i in range(len(self._lst_specification)):
            self.cmbSpecification.insert_text(i, self._lst_specification[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place the input widgets.
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtCommercialPiQ, _x_pos, _y_pos[1])
        _fixed.put(self.cmbSpecification, _x_pos, _y_pos[2])
        _fixed.put(self.cmbSpecSheet, _x_pos, _y_pos[3])
        _fixed.put(self.txtVoltRated, _x_pos, _y_pos[4])
        _fixed.put(self.txtVoltApplied, _x_pos, _y_pos[5])
        _fixed.put(self.txtACVoltApplied, _x_pos, _y_pos[6])
        _fixed.put(self.txtCapacitance, _x_pos, _y_pos[7])

        # Connect signals to callback functions.
        #cmbQuality.connect('changed', self._callback_combo, part, 85)
        #cmbSpecification.connect('changed', self._callback_combo, part, 101)
        #cmbSpecSheet.connect('changed', self._callback_combo, part, 102)

        #txtCommercialPiQ.connect('focus-out-event', self._callback_entry,
        #                          part, 'float', 79)
        #txtVoltRated.connect('focus-out-event', self._callback_entry,
        #                     part, 'float', 94)
        #txtVoltApplied.connect('focus-out-event', self._callback_entry,
        #                       part, 'float', 66)
        #txtACVoltApplied.connect('focus-out-event', self._callback_entry,
        #                         part, 'float', 64)
        #txtCapacitance.connect('focus-out-event', self._callback_entry,
        #                       part, 'float', 15)

        # Subcategory specific widgets.
        if self._subcategory == 51:
            _fixed.put(self.txtEffResistance, _x_pos, _y_pos[8])
        elif self._subcategory == 52:
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[8])
            for i in range(len(self._lst_construction)):
                self.cmbConstruction.insert_text(i, self._lst_construction[i])
            #self.cmbConstruction.connect('changed', self._callback_combo, part, 85)

        _fixed.show_all()

        return _x_pos

    def load_217_stress_inputs(self, model):
        """

        :param model: the Hardware data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        self.cmbQuality.set_active(int(model.quality))
        self.txtCommercialPiQ.set_text(str(fmt.format(model.q_override)))
        self.cmbSpecification.set_active(int(model.specification))
        self.cmbSpecSheet.set_active(int(model.spec_sheet))
        self.txtVoltRated.set_text(str(fmt.format(model.rated_voltage)))
        self.txtVoltApplied.set_text(str(fmt.format(model.operating_voltage)))
        self.txtACVoltApplied.set_text(str(fmt.format(model.acvapplied)))
        self.txtCapacitance.set_text(str(fmt.format(model.capacitance)))

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    capacitor.  The output attributes of a capacitor Work Book view are:
    """

    def __init__(self, subcategory):

        gtk.Frame.__init__(self)

        # Initialize private list attributes.
        self._lst_labels = ['', u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:", u"\u03C0<sub>CV</sub>:"]

        # Initialize private scalar attributes.
        self._subcategory = subcategory

        # Create the input widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiCV = _widg.make_entry(width=100, editable=False, bold=True)

        # Subcategory specific attributes.
        if subcategory == 51:               # Solid tantalum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub>\u03C0<sub>SR</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>SR</sub>:")

            self.txtPiSR = _widg.make_entry(width=100, editable=False,
                                            bold=True)

        elif subcategory == 52:             # Non-solid tantalum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub>\u03C0<sub>C</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>C</sub>:")

            self.txtPiC = _widg.make_entry(width=100, editable=False,
                                           bold=True)

        elif subcategory == 53:             # Wet aluminum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub></span>"

        elif subcategory == 54:             # Dry aluminum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub></span>"

    def create_217_stress_results(self, x_pos):
        """
        Populates the RTK Workbook reliability calculation results tab with
        the widgets to display Capacitor Component Class results.

        :param int x_pos: the x position of the display widgets.
        :param int y_pos: the y position of the first display widget.
        :return: (_x_pos, _y_pos); the x-coordinate and list of y-coordinates.
        :rtype: tuple
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
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

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
