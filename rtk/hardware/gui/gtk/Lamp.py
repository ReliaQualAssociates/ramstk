#!/usr/bin/env python
"""
#############################################
Lamp Module Component Specific Work Book View
#############################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.gui.gtk.Lamp.py is part of The RTK Project
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
    The Work Book view for displaying all the attributes for a fuse.  The
    attributes of a fuse Work Book view are:
    """

    def __init__(self, model):
        """
        Creates an input frame for the Lamp data model.

        :param :class `rtk.hardware.Lamp.model`: the Lamp data model whose
                                                 attributes will be displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # ===== ===== === Initialize private list attributes === ===== ===== #
        self._lst_labels = [_(u"Application:"), _(u"Rated Voltage (V):"),
                            _(u"Illuminate Hours:"), _(u"Operate Hours:")]
        self._lst_handler_id = []

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # ===== = Create the input widgets common to all Lamp types = ===== #
        self.cmbApplication = _widg.make_combo(simple=True)
        self.txtRatedVoltage = _widg.make_entry(width=100)
        self.txtIlluminateHours = _widg.make_entry(width=100)
        self.txtOperateHours = _widg.make_entry(width=100)

        # Create the tooltips for the input widgets.
        self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                               u"type of application for the "
                                               u"selected lamp."))

        # Populate the gtk.ComboBox().
        self.cmbApplication.insert_text(0, '')
        self.cmbApplication.insert_text(1, _(u"Alternating Current"))
        self.cmbApplication.insert_text(2, _(u"Direct Current"))

        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed',
                                        self._on_combo_changed, _index))

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for Lamps.

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
        self.txtRatedVoltage.set_tooltip_text(_(u"Displays the rated "
                                                u"voltage for the selected "
                                                u"lamp."))
        self.txtIlluminateHours.set_tooltip_text(_(u"Displays the number of "
                                                   u"hours the selected "
                                                   u"lamp is illuminated "
                                                   u"during a mission."))
        self.txtOperateHours.set_tooltip_text(_(u"Displays the mission length "
                                                u"in hours."))

        # Place all the input widgets.
        _fixed.put(self.cmbApplication, _x_pos, _y_pos[0])
        _fixed.put(self.txtRatedVoltage, _x_pos, _y_pos[1])
        _fixed.put(self.txtIlluminateHours, _x_pos, _y_pos[2])
        _fixed.put(self.txtOperateHours, _x_pos, _y_pos[3])

        # Connect signals to callback functions.
        _index = 1
        self._lst_handler_id.append(
            self.txtRatedVoltage.connect('focus-out-event',
                                         self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtIlluminateHours.connect('focus-out-event',
                                            self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtOperateHours.connect('focus-out-event',
                                         self._on_focus_out, _index))

        _fixed.show_all()

        return _x_pos

    def load_217_stress_inputs(self, model):
        """
        Loads the Lamp class MIL-HDBK-217FN2 part stress gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.cmbApplication.set_active(model.application)
        self.txtRatedVoltage.set_text(str(fmt.format(model.rated_voltage)))
        self.txtIlluminateHours.set_text(
            str(fmt.format(model.illuminate_hours)))
        self.txtOperateHours.set_text(str(fmt.format(model.operate_hours)))

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
            self._hardware_model.rated_voltage = float(entry.get_text())
        elif index == 2:
            self._hardware_model.illuminate_hours = float(entry.get_text())
        elif index == 3:
            self._hardware_model.operate_hours = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    Lamp.  The output attributes of a Lamp Work Book view are:
    """

    def __init__(self, model):
        """
        Initializes an instance of the Lamp assessment results view.

        :param model: the instance of the Lamp data model to create the view
                      for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Initialize private list attributes.
        self._lst_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>U</sub>\u03C0<sub>A</sub>\u03C0<sub>E</sub></span>",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>U</sub>:",
                            u"\u03C0<sub>A</sub>:", u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiU = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiA = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Lamps.

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
                                           u"for the selected lamp."))
        self.txtPiU.set_tooltip_text(_(u"Displays the utilization factor for "
                                       u"the selected lamp."))
        self.txtPiA.set_tooltip_text(_(u"Displays the application factor for "
                                       u"the selected lamp."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected lamp."))

        # Place the reliability result display widgets.
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiU, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiA, _x_pos, _y_pos[3])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[4])

        _fixed.show_all()

        return _x_pos

    def load_217_stress_results(self, model):
        """
        Loads the Lamp class result gtk.Widgets().

        :param model: the Lamp data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiU.set_text(str(fmt.format(model.piU)))
        self.txtPiA.set_text(str(fmt.format(model.piA)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        return False
