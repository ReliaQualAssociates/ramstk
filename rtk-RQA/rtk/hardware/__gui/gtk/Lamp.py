#!/usr/bin/env python
"""
#############################################
Lamp Module Component Specific Work Book View
#############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.gui.gtk.Lamp.py is part of The RTK Project
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
    The Work Book view for displaying all the attributes for a fuse.  The
    attributes of a fuse Work Book view are:

    :ivar list _lst_stress_labels: list of MIL-HDBK-217FN2 part stress labels.
    :ivar list _lst_handler_id: list of gtk.Widgets() signal IDs.
    :ivar :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model` _hardware_model:
    :ivar int _subcategory: the Component subcategory.
    :ivar gtk.ComboBox cmbApplication: the gtk.ComboBox() to select and display
                                       the MIL-HDBK-217FN2 application of the
                                       Lamp.
    :ivar gtk.Entry txtRatedVoltage: the gtk.Entry() to enter and display the
                                     rated voltage of the Lamp.
    :ivar gtk.Entry txtIlluminateHours: the gtk.Entry() to enter and display
                                        the number of mission hours the Lamp
                                        will be illuminated.
    :ivar gtk.Entry txtOperateHours: the gtk.Entry() to enter and display the
                                     number of mission hours for the Lamp.
    """

    def __init__(self, model):
        """
        Method to create an input frame for the Lamp data model.

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model`
                      whose attributes will be displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_stress_labels = [_(u"Application:"),
                                   _(u"Rated Voltage (V):"),
                                   _(u"Illuminate Hours:"),
                                   _(u"Operate Hours:")]
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.cmbApplication = Widgets.make_combo(simple=True)
        self.txtRatedVoltage = Widgets.make_entry(width=100)
        self.txtIlluminateHours = Widgets.make_entry(width=100)
        self.txtOperateHours = Widgets.make_entry(width=100)

        # Create the tooltips for the input widgets.
        self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                               u"type of application for the "
                                               u"selected lamp."))
        self.txtRatedVoltage.set_tooltip_text(_(u"Displays the rated voltage "
                                                u"for the selected lamp."))
        self.txtIlluminateHours.set_tooltip_text(_(u"Displays the number of "
                                                   u"hours the selected lamp "
                                                   u"is illuminated during a "
                                                   u"mission."))
        self.txtOperateHours.set_tooltip_text(_(u"Displays the mission length "
                                                u"in hours."))

        # Populate the gtk.ComboBox().
        self.cmbApplication.insert_text(0, '')
        self.cmbApplication.insert_text(1, _(u"Alternating Current"))
        self.cmbApplication.insert_text(2, _(u"Direct Current"))

        # Connect signals to callback functions.
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.txtRatedVoltage.connect('focus-out-event',
                                         self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtIlluminateHours.connect('focus-out-event',
                                            self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.txtOperateHours.connect('focus-out-event',
                                         self._on_focus_out, 3))

    def create_217_count_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part count input gtk.Widgets()
        for Lamps.

        :keyword int x_pos: the x position of the display widgets.
        :return: False if successful or True if an error is encountered.
        """

        return x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress input gtk.Widgets()
        for Lamps.

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
        _fixed.put(self.txtRatedVoltage, _x_pos, _y_pos[1])
        _fixed.put(self.txtIlluminateHours, _x_pos, _y_pos[2])
        _fixed.put(self.txtOperateHours, _x_pos, _y_pos[3])

        _fixed.show_all()

        return _x_pos

    def load_217_count_inputs(self, __model):
        """
        Method to load the Lamp class MIL-HDBK-217FN2 parts count input
        gtk.Widgets().

        :param __model: the :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model`
                        to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return False

    def load_217_stress_inputs(self, model):
        """
        Method to load the Lamp class MIL-HDBK-217FN2 part stress input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.cmbApplication.set_active(model.application)
        self.txtRatedVoltage.set_text(str(fmt.format(model.rated_voltage)))
        self.txtIlluminateHours.set_text(
            str(fmt.format(model.illuminate_hours)))
        self.txtOperateHours.set_text(str(fmt.format(model.operate_hours)))

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
            self._hardware_model.application = combo.get_active()

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

    :ivar list _lst_count_labels: the list of MIL-HDBK-217FN2 parts count
                                  labels.
    :ivar list _lst_stress_labels: the list of MIL-HDBK-217FN2 part stress
                                   labels.
    :ivar :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model` _hardware_model:
    :ivar int _subcategory: the Component subcategory.
    :ivar gtk.Entry txtLambdaB: the gtk.Entry() to display the MIL-HDBK-217FN2
                                base/generic hazard rate.
    :ivar gtk.Entry txtPiU: the gtk.Entry() to display the MIL-HDBK-217FN2
                            utilization factor.
    :ivar gtk.Entry txtPiA: the gtk.Entry() to display the MIL-HDBK-217FN2
                            application factor.
    :ivar gtk.Entry txtPiE: the gtk.Entry() to display the MIL-HDBK-217FN2
                            operating environment factor.
    """

    def __init__(self, model):
        """
        Method to initialize an instance of the Lamp assessment results view.

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model`
                      to create the view for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = \u03BB<sub>g</sub></span>",
                                  u"\u03BB<sub>g</sub>:"]
        self._lst_stress_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>U</sub>\u03C0<sub>A</sub>\u03C0<sub>E</sub></span>",
                                   u"\u03BB<sub>b</sub>:",
                                   u"\u03C0<sub>U</sub>:",
                                   u"\u03C0<sub>A</sub>:",
                                   u"\u03C0<sub>E</sub>:"]

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.txtLambdaB = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtPiU = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiA = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = Widgets.make_entry(width=100, editable=False, bold=True)

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected lamp."))
        self.txtPiU.set_tooltip_text(_(u"Displays the utilization factor for "
                                       u"the selected lamp."))
        self.txtPiA.set_tooltip_text(_(u"Displays the application factor for "
                                       u"the selected lamp."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected lamp."))

    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count result gtk.Widgets()
        for Lamps.

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
        if self.txtLambdaB.get_parent() is not None:
            self.txtLambdaB.reparent(_fixed)
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])

        _fixed.show_all()

        return _x_pos

    def create_217_stress_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress result gtk.Widgets()
        for Lamps.

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
        if self.txtLambdaB.get_parent() is not None:
            self.txtLambdaB.reparent(_fixed)

        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiU, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiA, _x_pos, _y_pos[3])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[4])

        _fixed.show_all()

        return _x_pos

    def load_217_count_results(self, model):
        """
        Method to load the Lamp class MIL-HDBK-217FN2 parts count result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))

        return False

    def load_217_stress_results(self, model):
        """
        Method to load the Lamp class MIL-HDBK-217FN2 part stress result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model`
                      to load the attributes from.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiU.set_text(str(fmt.format(model.piU)))
        self.txtPiA.set_text(str(fmt.format(model.piA)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        return False

    def load_derate_plot(self, __model, frame):
        """
        Method to load the stress derate plot for the Lamp class.

        :param __model: the :py:class:`rtk.hardware.component.miscellaneous.Lamp.Model`
                        to load the attributes from.
        :param gtk.Frame frame: the gtk.Frame() to embed the derate plot into.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        frame.hide()

        return False
