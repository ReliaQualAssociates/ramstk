#!/usr/bin/env python
"""
###############################################
Meter Package Component Specific Work Book View
###############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.gui.gtk.Meter.py is part of The RTK Project
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

# Import other RTK modules.
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Inputs(gtk.Frame):
    """
    The Work Book view for displaying all the attributes for an integrated
    circuit.  The attributes of an Meter Work Book view are:
    """

    def __init__(self, model):
        """
        Method to create an input frame for the Meter data model.

        :param model: the :py:class:`rtk.hardware.component.meter.Meter.Model`
                      whose attributes will be displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [_(u"Quality:")]
        self._lst_stress_labels = [_(u"Application:")]

        self._lst_handler_id = []

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.cmbApplication = Widgets.make_combo(simple=True)
        self.cmbFunction = Widgets.make_combo(simple=True)
        self.cmbQuality = Widgets.make_combo(simple=True)
        self.txtCommercialPiQ = Widgets.make_entry(width=100)

        # Subcategory specific attributes.
        if self._subcategory == 2:          # Panel
            self._lst_stress_labels.append(_(u"Quality:"))
            self._lst_stress_labels.append(_(u"Quality Override:"))
            self._lst_stress_labels.append(_(u"Function:"))

        # Create the tooltips for all the input widgets.
        self.cmbApplication.set_tooltip_text(_(u"Select and display the type "
                                               u"of application for the "
                                               u"selected meter."))
        self.cmbFunction.set_tooltip_text(_(u"Select and display the function "
                                            u"of the selected meter."))
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected meter."))
        self.txtCommercialPiQ.set_tooltip_text(_(u"Displays the user-defined "
                                                 u"quality factor for the "
                                                 u"selected meter.  This "
                                                 u"value over rides the "
                                                 u"quality factor selected "
                                                 u"above."))

        # Connect signals to callback functions.
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.txtCommercialPiQ.connect('focus-out-event',
                                          self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbFunction.connect('changed', self._on_combo_changed, 3))

    def create_217_count_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count input gtk.Widgets()
        for Meters.

        :keyword int x_pos: the x position of the display widgets.
        :return: False if successful or True if an error is encountered.
        """

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"MIL-HDBK-217FN2 Parts Count Inputs") +
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

        # Create and place the inputs if this is a panel meter.
        if self._subcategory == 2:
            (_x_pos, _y_pos) = Widgets.make_labels(self._lst_count_labels,
                                                   _fixed, 5, 5)
            _x_pos = max(x_pos, _x_pos) + 50

            self.cmbQuality.reparent(_fixed)
            _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])

        _fixed.show_all()

        return x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress input gtk.Widgets()
        for Meters.

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
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
        _fixed.put(self.cmbApplication, _x_pos, _y_pos[0])

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

            # Place all the input widgets.
            self.cmbQuality.reparent(_fixed)
            _fixed.put(self.cmbQuality, _x_pos, _y_pos[1])
            _fixed.put(self.txtCommercialPiQ, _x_pos, _y_pos[2])
            _fixed.put(self.cmbFunction, _x_pos, _y_pos[3])

        _fixed.show_all()

        return _x_pos

    def load_217_count_inputs(self, model):
        """
        Method to load the Meter class MIL-HDBK-217FN2 parts count input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.meter.Meter.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self._subcategory == 2:
            self.cmbQuality.set_active(model.quality)

        return False

    def load_217_stress_inputs(self, model):
        """
        Method to load the Meter class MIL-HDBK-217FN2 part stress input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.meter.Meter.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.cmbApplication.set_active(model.application)

        # Load subcategory specific widgets.
        if self._subcategory == 2:          # Panel
            self.cmbQuality.set_active(model.quality)
            self.txtCommercialPiQ.set_text(str(fmt.format(model.q_override)))
            self.cmbFunction.set_active(model.function)

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() 'changed' signals and call the
        correct function or method, passing any parameters as needed.

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
        elif index == 2:
            self._hardware_model.application = combo.get_active()
        elif index == 3:
            self._hardware_model.function = combo.get_active()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Method to respond to gtk.Entry() 'focus_out' signals and call the
        correct function or method, passing any parameters as needed.

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

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    meter.  The output attributes of a Meter Work Book view are:
    """

    def __init__(self, model):
        """
        Method to initialize an instance of the Meter assessment results view.

        :param model: the :py:class:`rtk.hardware.component.meter.Meter.Model`
                      to create the view for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = \u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>",
                                  u"\u03BB<sub>g</sub>:",
                                  u"\u03C0<sub>Q</sub>:"]
        self._lst_stress_labels = ['', u"\u03BB<sub>b</sub>:",
                                   u"\u03C0<sub>E</sub>:"]

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.txtLambdaB = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtPiE = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiT = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiA = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiF = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiQ = Widgets.make_entry(width=100, editable=False, bold=True)

        # Subcategory specific attributes.
        if self._subcategory == 1:          # Elapsed time
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>T</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>T</sub>:")

        elif self._subcategory == 2:        # Panel
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>A</sub>\u03C0<sub>F</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>A</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>F</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>Q</sub>:")

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected meter."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected meter."))
        self.txtPiT.set_tooltip_text(_(u"Displays the temperature factor for "
                                       u"the selected meter."))
        self.txtPiA.set_tooltip_text(_(u"Displays the application factor for "
                                       u"the selected meter."))
        self.txtPiF.set_tooltip_text(_(u"Displays the function factor for the "
                                       u"selected meter."))
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected meter."))

    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count result gtk.Widgets()
        for Meters.

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

        # Create and place all the labels for the inputs.
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_count_labels, _fixed, 5, 25)
        _x_pos = max(x_pos, _x_pos) + 30

        # Place the reliability result display widgets.
        self.txtLambdaB.reparent(_fixed)
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        if self._subcategory == 2:
            self.txtPiQ.reparent(_fixed)
            _fixed.put(self.txtPiQ, _x_pos, _y_pos[1])

        _fixed.show_all()

        return _x_pos

    def create_217_stress_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress result gtk.Widgets()
        for Meters.

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
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 25)
        _x_pos = max(x_pos, _x_pos) + 30

        # Place the reliability result display widgets.
        self.txtLambdaB.reparent(_fixed)
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[2])

        # Subcategory specific widgets.
        if self._subcategory == 1:
            _fixed.put(self.txtPiT, _x_pos, _y_pos[3])

        elif self._subcategory == 2:
            self.txtPiQ.reparent(_fixed)
            _fixed.put(self.txtPiA, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiF, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiQ, _x_pos, _y_pos[5])

        _fixed.show_all()

        return _x_pos

    def load_217_count_results(self, model):
        """
        Method to load the Meter class MIL-HDBK-217FN2 parts count result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.meter.Meter.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))

        if self._subcategory == 2:
            self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_217_stress_results(self, model):
        """
        Method to load the Meter class MIL-HDBK-217FN2 part stress result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.meter.Meter.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        if self._subcategory == 1:
            self.txtPiT.set_text(str(fmt.format(model.piT)))
        elif self._subcategory == 2:
            self.txtPiA.set_text(str(fmt.format(model.piA)))
            self.txtPiF.set_text(str(fmt.format(model.piF)))
            self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_derate_plot(self, __model, frame):
        """
        Method to load the stress derate plot for the Meter class.

        :param __model: the :py:class:`rtk.hardware.component.meter.Meter.Model`
                        to load the attributes from.
        :param gtk.Frame frame: the gtk.Frame() to embed the derate plot into.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        frame.hide()

        return False
