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
    The Work Book view for displaying all the attributes for a capacitor.  The
    attributes of a capacitor Work Book view are:
    """

    dicQuality = {40: ["", "MIL-SPEC", _(u"Lower")],
                  41: ["", "M", _(u"Non-Established Reliability"),
                       _(u"Lower")],
                  42: ["", "S", "R", "P", "M", "L",
                       _(u"MIL-C-19978, Non-Established Reliability"),
                       _(u"Lower")],
                  43: ["", "S", "R", "P", "M", "L",
                       _(u"MIL-C-18312, Non-Established Reliability"),
                       _(u"Lower")],
                  44: ["", "S", "R", "P", "M", _(u"Lower")],
                  45: ["", "S", "R", "P", "M", _(u"Lower")],
                  46: ["", "T", "S", "R", "P", "M", "L",
                       _(u"MIL-C-5, Non-Established Reliability, Dipped"),
                       _(u"MIL-C-5, Non-Established Reliability, Molded"),
                       _(u"Lower")],
                  47: ["", "MIL-C-10950", _(u"Lower")],
                  48: ["", "S", "R", "P", "M", "L",
                       _(u"MIL-C-11272, Non-Established Reliability"),
                       _(u"Lower")],
                  49: ["", "S", "R", "P", "M", "L",
                       _(u"MIL-C-11015, Non-Established Reliability"),
                       _(u"Lower")],
                  50: ["", "S", "R", "P", "M",
                       _(u"Non-Established Reliability"), _(u"Lower")],
                  51: ["", "D", "C", "S", "B", "R", "P", "M", "L",
                       _(u"Lower")],
                  52: ["", "S", "R", "P", "M", "L",
                       _(u"MIL-C-3965, Non-Established Reliability"),
                       _(u"Lower")],
                  53: ["", "S", "R", "P", "M",
                       _(u"Non-Established Reliability"), _(u"Lower")],
                  54: ["", "MIL-SPEC", _(u"Lower")],
                  55: ["", "MIL-SPEC", _(u"Lower")],
                  56: ["", "MIL-SPEC", _(u"Lower")],
                  57: ["", "MIL-SPEC", _(u"Lower")],
                  58: ["", "MIL-SPEC", _(u"Lower")]}
    dicSpecification = {40: ["", "MIL-C-25 (CP)", "MIL-C-12889 (CA)"],
                        41: ["", "MIL-C-11693 (CZ/CZR)"],
                        42: ["", "MIL-C-14157 (CPV)", "MIL-C-19978 (CQ/CQR)"],
                        43: ["", "MIL-C-18312 (CH)", "MIL-C-39022 (CHR)"],
                        44: ["", "MIL-C-55514 (CFR)"],
                        45: ["", "MIL-C-83421 (CRH)"],
                        46: ["", "MIL-C-5 (CM)", "MIL-C-39001 (CMR)"],
                        47: ["", "MIL-C-10950 (CB)"],
                        48: ["", "MIL-C-11272 (CY)", "MIL-C-23269 (CYR)"],
                        49: ["", "MIL-C-11015 (CK)", "MIL-C-39014 (CKR)"],
                        50: ["", "MIL-C-20 (CC/CCR)", "MIL-C-55681 (CDR)"],
                        51: ["", "MIL-C-39003 (CSR)"],
                        52: ["", "MIL-C-3965 (CL)", "MIL-C-39003 (CLR)"],
                        53: ["", "MIL-C-39016 (CU and CUR)"],
                        54: ["", "MIL-C-62 (CE)"],
                        55: ["", "MIL-C-81 (CV)"],
                        56: ["", "MIL-C-14409 (PC)"],
                        57: ["", "MIL-C-92 (CT)"],
                        58: ["", "MIL-C-23183 (CT)"]}
    dicSpecSheet = {40: [["", u"85\u00B0C", u"125\u00B0C"],
                         ["", u"85\u00B0C"]],
                    41: [["", u"85\u00B0C", u"125\u00B0C", u"150\u00B0C"]],
                    42: [["", u"65\u00B0C", u"85\u00B0C", u"125\u00B0C"],
                         ["", u"65\u00B0C", u"85\u00B0C", u"125\u00B0C",
                          u"170\u00B0C"]],
                    43: [["", u"85\u00B0C", u"125\u00B0C"],
                         ["", u"85\u00B0C", u"125\u00B0C"]],
                    44: [["", u"85\u00B0C", u"125\u00B0C"]],
                    45: [["", u"125\u00B0C"]],
                    46: [["", u"70\u00B0C", u"85\u00B0C", u"125\u00B0C",
                          u"150\u00B0C"], ["", u"125\u00B0C", u"150\u00B0C"]],
                    47: [["", u"85\u00B0C", u"150\u00B0C"]],
                    48: [["", u"125\u00B0C", u"200\u00B0C"],
                         ["", u"125\u00B0C"]],
                    49: [["", u"85\u00B0C", u"125\u00B0C", u"150\u00B0C"],
                         ["", u"85\u00B0C", u"125\u00B0C"]],
                    50: [["", u"85\u00B0C", u"125\u00B0C"],
                         ["", u"85\u00B0C"]],
                    51: [["", _(u"All")]],
                    52: [["", u"85\u00B0C", u"125\u00B0C", u"175\u00B0C"],
                         ["", u"125\u00B0C"]],
                    53: [["", u"85\u00B0C"]],
                    54: [["", u"85\u00B0C", u"105\u00B0C", u"125\u00B0C"]],
                    55: [["", u"85\u00B0C", u"125\u00B0C"]],
                    56: [["", u"125\u00B0C", u"150\u00B0C"]],
                    57: [["", u"85\u00B0C"]],
                    58: [["", u"85\u00B0C", u"100\u00B0C", u"125\u00B0C"]]}

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
                            _(u"Capacitance (F):"), _(u"Specification:"),
                            _(u"Temperature Rating:")]
        self._lst_quality = self.dicQuality[model.subcategory]
        self._lst_specification = self.dicSpecification[model.subcategory]
        self._lst_specsheet = self.dicSpecSheet[model.subcategory]

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
        self.cmbSpecification = _widg.make_combo(simple=True)
        self.cmbSpecSheet = _widg.make_combo(simple=True)

        # Subcategory specific attributes.
        if self._subcategory == 51:         # Solid tantalum
            self._lst_labels.append(_(u"Eff. Series Resistance:"))

            self.txtEffResistance = _widg.make_entry(width=100)

        elif self._subcategory == 52:       # Non-solid tantalum
            self._lst_construction = ["", _(u"Slug, All Tantalum"),
                                      _(u"Foil, Hermetic"),
                                      _(u"Slug, Hermetic"),
                                      _(u"Foil, Non-Hermetic"),
                                      _(u"Slug, Non-Hermetic")]

            self._lst_labels.append(_(u"Construction:"))

            self.cmbConstruction = _widg.make_combo(simple=True)

        elif self._subcategory == 58:       # Variable vacuum
            self._lst_configuration = ["", _(u"Fixed"), _(u"Variable")]

            self.cmbConfiguration = _widg.make_combo(simple=True)

            self._lst_labels.append(_(u"Configuration:"))

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for Capacitors.

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
                                           u"capacitor."))

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
        for i in range(len(self._lst_specification)):
            self.cmbSpecification.insert_text(i, self._lst_specification[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Create the tooltips for all the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"capacitor."))
        self.txtCommercialPiQ.set_tooltip_text(_(u"Displays the user-defined "
                                                 u"quality factor for the "
                                                 u"selected capacitor.  This "
                                                 u"value over rides the "
                                                 u"quality factor selected "
                                                 u"above."))
        self.txtVoltRated.set_tooltip_text(_(u"Displays the rated voltage for "
                                             u"the selected capacitor."))
        self.txtVoltApplied.set_tooltip_text(_(u"Display the operating DC "
                                               u"voltage for the selected "
                                               u"capacitor."))
        self.txtACVoltApplied.set_tooltip_text(_(u"Displays the peak "
                                                 u"operating AC voltage for "
                                                 u"the selected capacitor."))
        self.txtCapacitance.set_tooltip_text(_(u"Display the capacitance in "
                                               u"farads for the selected "
                                               u"capacitor."))
        self.cmbSpecification.set_tooltip_text(_(u"Selects the governing "
                                                 u"specification for the "
                                                 u"selected capacitor."))
        self.cmbSpecSheet.set_tooltip_text(_(u"Selects the maximum "
                                             u"temperature rating for the "
                                             u"selected capacitor."))

        # Place all the input widgets.
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtCommercialPiQ, _x_pos, _y_pos[1])
        _fixed.put(self.txtVoltRated, _x_pos, _y_pos[2])
        _fixed.put(self.txtVoltApplied, _x_pos, _y_pos[3])
        _fixed.put(self.txtACVoltApplied, _x_pos, _y_pos[4])
        _fixed.put(self.txtCapacitance, _x_pos, _y_pos[5])
        _fixed.put(self.cmbSpecification, _x_pos, _y_pos[6])
        _fixed.put(self.cmbSpecSheet, _x_pos, _y_pos[7])

        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtCommercialPiQ.connect('focus-out-event',
                                          self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtVoltRated.connect('focus-out-event',
                                      self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtVoltApplied.connect('focus-out-event',
                                        self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtACVoltApplied.connect('focus-out-event',
                                          self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtCapacitance.connect('focus-out-event',
                                        self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed',
                                          self._on_combo_changed, _index))
        _index += 1
        self._lst_handler_id.append(
            self.cmbSpecSheet.connect('changed',
                                      self._on_combo_changed, _index))
        _index += 1

        if self._subcategory == 51:         # Solid tantalum
            self.txtEffResistance.set_tooltip_text(_(u"Displays the effective "
                                                     u"series resistance "
                                                     u"between the power "
                                                     u"supply and the "
                                                     u"capacitor."))
            _fixed.put(self.txtEffResistance, _x_pos, _y_pos[8])
            self._lst_handler_id.append(
                self.txtEffResistance.connect('focus-out-event',
                                              self._on_focus_out, _index))
            _index += 1
        elif self._subcategory == 52:       # Non-solid tantalum
            for i in range(len(self._lst_construction)):
                self.cmbConstruction.insert_text(i, self._lst_construction[i])
            self.cmbConstruction.set_tooltip_text(_(u"Displays the method of "
                                                    u"construction for the "
                                                    u"selected capacitor."))
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[8])
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
        elif self._subcategory == 58:       # Gas or vacuum
            for i in range(len(self._lst_configuration)):
                self.cmbConfiguration.insert_text(i,
                                                  self._lst_configuration[i])
            self.cmbConfiguration.set_tooltip_text(_(u"Displays whether the "
                                                     u"selected capacitor is "
                                                     u"fixed or variable."))
            _fixed.put(self.cmbConfiguration, _x_pos, _y_pos[8])
            self._lst_handler_id.append(
                self.cmbConfiguration.connect('changed',
                                              self._on_combo_changed, _index))
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
        if self._subcategory in [40, 41, 42, 43, 46, 47, 48, 49, 50, 52]:
            self.cmbSpecification.set_active(int(model.specification))
        if self._subcategory in [40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 52,
                                 53, 55, 56, 57, 58]:
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
        elif index == 5:
            self._hardware_model.spec_sheet = combo.get_active()
        elif index == 5 and self._subcategory == 58:
            self._hardware_model.configuration = combo.get_active()
        elif index == 6:
            self._hardware_model.specification = combo.get_active()
            self._load_spec_sheet(self._hardware_model.specification - 1)
        elif index == 7:
            self._hardware_model.spec_sheet = combo.get_active()
            self._hardware_model.reference_temperature = \
                self._hardware_model.lst_ref_temp[combo.get_active() - 1]
        elif index == 8 and self._subcategory == 52:
            self._hardware_model.construction = combo.get_active()
        elif index == 8 and self._subcategory == 58:
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
        elif index == 8 and self._subcategory == 51:
            self._hardware_model.effective_resistance = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _load_spec_sheet(self, specification):
        """
        Method to load the specification sheet gtk.ComboBox() whenever a new
        specification is selected.

        :param int specification: the selected specification index.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Remove existing entries.
        _model = self.cmbSpecSheet.get_model()
        _model.clear()

        # Load the new entries.
        _n_spec_sheets = len(self._lst_specsheet[specification])
        for i in range(_n_spec_sheets):
            self.cmbSpecSheet.insert_text(
                i, self._lst_specsheet[specification][i])

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

        self.figDerate = Figure(figsize=(6, 4))
        self.axsDerate = self.figDerate.add_subplot(111)
        self.pltDerate = FigureCanvas(self.figDerate)

        # Subcategory specific attributes.
        if self._subcategory in [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
                                 53, 54]:
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub></span>"

        elif self._subcategory == 51:       # Solid tantalum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub>\u03C0<sub>SR</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>SR</sub>:")

            self.txtPiSR = _widg.make_entry(width=100, editable=False,
                                            bold=True)

        elif self._subcategory == 52:       # Non-solid tantalum
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CV</sub>\u03C0<sub>C</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>C</sub>:")

            self.txtPiC = _widg.make_entry(width=100, editable=False,
                                           bold=True)

        elif self._subcategory in [55, 56, 57]:
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.pop(4)

        elif self._subcategory == 58:
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>CF</sub></span>"
            self._lst_labels[4] = u"\u03C0<sub>CF</sub>:"

            self.txtPiCF = _widg.make_entry(width=100, editable=False,
                                            bold=True)

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

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected capacitor."))
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected capacitor."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environement factor for "
                                       u"the selected capacitor."))
        self.txtPiCV.set_tooltip_text(_(u"Displays the capacitance correction "
                                        u"factor for the selected capacitor."))

        # Place the reliability result display widgets.
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[3])

        # Subcategory specific widgets.
        if self._subcategory == 51:
            self.txtPiSR.set_tooltip_text(_(u"Displays the effective series "
                                            u"resistance factor for the "
                                            u"selected capacitor."))
            _fixed.put(self.txtPiSR, _x_pos, _y_pos[5])
        elif self._subcategory == 52:
            self.txtPiC.set_tooltip_text(_(u"Displays the construction "
                                           u"factor for the selected "
                                           u"capacitor."))
            _fixed.put(self.txtPiC, _x_pos, _y_pos[5])
        elif self._subcategory not in [55, 56, 57, 58]:     # Not variable
            _fixed.put(self.txtPiCV, _x_pos, _y_pos[4])

        if self._subcategory == 58:
            self.txtPiCF.set_tooltip_text(_(u"Displays the configuration "
                                            u"factor for the selected "
                                            u"capacitor."))
            _fixed.put(self.txtPiCF, _x_pos, _y_pos[4])

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
        elif self._subcategory == 58:
            self.txtPiCF.set_text(str(fmt.format(model.piCF)))

        return False

    def load_derate_plot(self, model, frame):
        """
        Loads the stress derate plot for the Capacitor class.

        :param model: the Hardware data model to load the attributes from.
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
        self.axsDerate.plot(model.temperature_active,
                            model.voltage_ratio, 'go')
        if(_x[0] != _x[2] and
           model.lst_derate_criteria[1][0] != model.lst_derate_criteria[1][2]):
            self.axsDerate.axis([0.95 * _x[0], 1.05 * _x[2],
                                 model.lst_derate_criteria[1][2],
                                 1.05 * model.lst_derate_criteria[1][0]])
        else:
            self.axsDerate.cla().axis([0.95, 1.05, 0.0, 1.05])

        self.axsDerate.set_title(_(u"Voltage Derating Curve for %s at %s") %
                                 (model.part_number, model.ref_des),
                                 fontdict={'fontsize': 12,
                                           'fontweight' : 'bold',
                                           'verticalalignment': 'baseline'})
        _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                         _(u"Voltage Operating Point")])
        _leg = self.axsDerate.legend(_legend, 'upper right', shadow=True)
        for _text in _leg.get_texts():
            _text.set_fontsize('small')

        # Set the proper labels on the derating curve.
        self.axsDerate.set_xlabel(_(u"Temperature (\u2070C)"),
                                  fontdict={'fontsize': 12,
                                            'fontweight' : 'bold'})
        self.axsDerate.set_ylabel(r'$\mathbf{V_{op} / V_{rated}}$',
                                  fontdict={'fontsize': 12,
                                            'fontweight' : 'bold',
                                            'rotation': 'vertical',
                                            'verticalalignment': 'baseline'})

        self.figDerate.tight_layout()

        frame.add(self.pltDerate)
        frame.show_all()

        return False
