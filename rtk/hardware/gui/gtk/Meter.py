#!/usr/bin/env python
"""
###############################################
Meter Package Component Specific Work Book View
###############################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.gui.gtk.Meter.py is part of The RTK Project
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

    def __init__(self, model):
        """
        Creates an input frame for the meter data model.

        :param :class `rtk.hardware.Meter.model`: the Meter data model whose
                                                  attributes will be displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # ===== ===== === Initialize private list attributes === ===== ===== #
        self._lst_labels = [_(u"Application:")]

        self._lst_handler_id = []

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # ===== = Create the input widgets common to all Meter types = ===== #
        self.cmbApplication = _widg.make_combo(simple=True)

        # Subcategory specific attributes.
        if self._subcategory == 2:          # Panel
            self._lst_labels.append(_(u"Quality:"))
            self._lst_labels.append(_(u"Quality Override:"))
            self._lst_labels.append(_(u"Function:"))

            self.cmbQuality = _widg.make_combo(simple=True)
            self.cmbFunction = _widg.make_combo(simple=True)
            self.txtCommercialPiQ = _widg.make_entry(width=100)

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for Meters.

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

        _fixed.show_all()

        return x_pos

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

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Create the tooltips for all the input widgets.
        self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                               u"type of application for the "
                                               u"selected meter."))

        # Place all the input widgets.
        _fixed.put(self.cmbApplication, _x_pos, _y_pos[0])

        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed',
                                        self._on_combo_changed, _index))
        _index += 1

        if self._subcategory == 1:          # Elapsed time
            # Populate the gtk.ComboBox().
            self.cmbApplication.insert_text(0, '')
            self.cmbApplication.insert_text(1, "A.C.")
            self.cmbApplication.insert_text(2, _(u"Inverter Driven"))
            self.cmbApplication.insert_text(3, _(u"Cummutator D.C."))

        elif self._subcategory == 2:        # Panel
            # Populate the gtk.ComboBox().
            self.cmbApplication.insert_text(0, '')
            self.cmbApplication.insert_text(1, _(u"Direct Current"))
            self.cmbApplication.insert_text(2, _(u"Alternating Current"))

            self.cmbFunction.insert_text(0, '')
            self.cmbFunction.insert_text(1, _(u"Ammeter"))
            self.cmbFunction.insert_text(2, _(u"Voltmeter"))
            self.cmbFunction.insert_text(3, _(u"Other"))

            self.cmbQuality.insert_text(0, '')
            self.cmbQuality.insert_text(0, u"MIL-M-10304")
            self.cmbQuality.insert_text(0, _(u"Lower"))

            self.cmbQuality.set_tooltip_text(_(u"Select and display the "
                                               u"quality level for the "
                                               u"selected meter."))
            self.txtCommercialPiQ.set_tooltip_text(_(u"Displays the "
                                                     u"user-defined quality "
                                                     u"factor for the "
                                                     u"selected meter.  This "
                                                     u"value over rides the "
                                                     u"quality factor "
                                                     u"selected above."))
            self.cmbFunction.set_tooltip_text(_(u"Select and display the "
                                                u"function of the "
                                                u"selected meter."))

            # Place all the input widgets.
            _fixed.put(self.cmbQuality, _x_pos, _y_pos[1])
            _fixed.put(self.txtCommercialPiQ, _x_pos, _y_pos[2])
            _fixed.put(self.cmbFunction, _x_pos, _y_pos[3])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbQuality.connect('changed',
                                        self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbFunction.connect('changed',
                                         self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtCommercialPiQ.connect('focus-out-event',
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

        self.cmbApplication.set_active(model.application)

        # Load subcategory specific widgets.
        if self._subcategory == 2:          # Panel
            self.cmbQuality.set_active(model.quality)
            self.txtCommercialPiQ.set_text(str(fmt.format(model.q_override)))
            self.cmbFunction.set_active(model.function)

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
            self._hardware_model.application = combo.get_active()
        elif index == 1 and self._subcategory == 2:
            self._hardware_model.quality = combo.get_active()
        elif index == 2 and self._subcategory == 2:
            self._hardware_model.function = combo.get_active()

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

        if index == 3 and self._subcategory == 2:
            self._hardware_model.q_override = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    meter.  The output attributes of a meter Work Book view are:
    """

    def __init__(self, model):
        """
        Initializes an instance of the meter assessment results view.

        :param model: the instance of the Meter data model to create the view
                      for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Initialize private list attributes.
        self._lst_labels = ['', u"\u03BB<sub>b</sub>:", u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        # Subcategory specific attributes.
        if self._subcategory == 1:          # Elapsed time
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>T</sub>:")

            self.txtPiT = _widg.make_entry(width=100, editable=False,
                                           bold=True)

        elif self._subcategory == 2:        # Panel
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>A</sub>:")
            self._lst_labels.append(u"\u03C0<sub>F</sub>:")
            self._lst_labels.append(u"\u03C0<sub>Q</sub>:")

            self.txtPiA = _widg.make_entry(width=100, editable=False,
                                           bold=True)
            self.txtPiF = _widg.make_entry(width=100, editable=False,
                                           bold=True)
            self.txtPiQ = _widg.make_entry(width=100, editable=False,
                                           bold=True)

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Meters.

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
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected meter."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected meter."))

        # Place the reliability result display widgets.
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[2])

        # Subcategory specific widgets.
        if self._subcategory == 1:
            self.txtPiT.set_tooltip_text(_(u"Displays the temperature factor "
                                           u"for the selected meter."))

            _fixed.put(self.txtPiT, _x_pos, _y_pos[3])

        elif self._subcategory == 2:
            self.txtPiA.set_tooltip_text(_(u"Displays the application factor "
                                           u"for the selected meter."))
            self.txtPiF.set_tooltip_text(_(u"Displays the function factor for "
                                           u"the selected meter."))
            self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for "
                                           u"the selected meter."))

            _fixed.put(self.txtPiA, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiF, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiQ, _x_pos, _y_pos[5])

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

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        if self._subcategory == 1:
            self.txtPiT.set_text(str(fmt.format(model.piT)))
        elif self._subcategory == 2:
            self.txtPiA.set_text(str(fmt.format(model.piA)))
            self.txtPiF.set_text(str(fmt.format(model.piF)))
            self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_derate_plot(self, model, frame):
        """
        Loads the stress derate plot for the Meter class.

        :param model: the Hardware data model to load the attributes from.
        :param gtk.Frame frame: the gtk.Frame() to embed the derate plot into.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        frame.hide()

        return False
