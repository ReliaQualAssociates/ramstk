#!/usr/bin/env python
"""
##############################################
Relay Module Component Specific Work Book View
##############################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.gui.gtk.Relay.py is part of The RTK Project
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
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

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

matplotlib.use('GTK')


class Inputs(gtk.Frame):
    """
    The Work Book view for displaying all the attributes for a relay.  The
    attributes of a relay Work Book view are:
    """

    _lst_application = [["", _(u"Dry Circuit")],
                        ["", _(u"General Purpose"), _(u"Sensitive (0-100 mW)"),
                         _(u"Polarized"), _(u"Vibrating Reed"),
                         _(u"High Speed"), _(u"Thermal Time Delay"),
                         _(u"Electronic Time Delay"), _(u"Magnetic Latching")],
                        ["", _(u"High Voltage"), _(u"Medium Power")],
                        ["", _(u"Contactor")]]
    _lst_construction = [[["", _(u"Long Armature"), _(u"Dry Reed"),
                           _(u"Mercury Wetted"), _(u"Magnetic Latching"),
                           _(u"Balanced Armature"), _(u"Solenoid")]],
                         [["", _(u"Long Armature"), _(u"Balanaced Armature"),
                           _(u"Solenoid")],
                          ["", _(u"Long Armature"), _(u"Short Armature"),
                           _(u"Mercury Wetted"), _(u"Magnetic Latching"),
                           _(u"Meter Movement"), _(u"Balanced Armature")],
                          ["", _(u"Short Armature"), _(u"Meter Movement")],
                          ["", _(u"Dry Reed"), _(u"Mecury Wetted")],
                          ["", _(u"Balanced Armature"), _(u"Short Armature"),
                           _(u"Dry Reed")],
                          ["", _(u"Bimetal")],
                          [""],
                          ["", _(u"Dry Reed"), _(u"Mercury Wetted"),
                           _(u"Balanced Armature")]],
                         [["", _(u"Vacuum, Glass"), _(u"Vacuum, Ceramic")],
                          ["", _(u"Long Armature"), _(u"Short Armature"),
                           _(u"Mercury Wetted"), _(u"Magnetic Latching"),
                           _(u"Mechanical Latching"), _(u"Balanced Armature"),
                           _(u"Solenoid")]],
                         [["", _(u"Short Armature"), _(u"Mechanical Latching"),
                           _(u"Balanced Armature"), _(u"Solenoid")]]]

    def __init__(self, model):
        """
        Method to create an input frame for the Relay data model.

        :param model: the :py:class:`rtk.hardware.relay.Relay.Model` whose
                      attributes will be displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [_(u"Quality:")]
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.cmbApplication = Widgets.make_combo(simple=True)
        self.cmbContactForm = Widgets.make_combo(simple=True)
        self.cmbContactRating = Widgets.make_combo(simple=True)
        self.cmbConstruction = Widgets.make_combo(simple=True)
        self.cmbLoadType = Widgets.make_combo(simple=True)
        self.cmbQuality = Widgets.make_combo(simple=True)
        self.cmbTempRating = Widgets.make_combo(simple=True)
        self.txtCyclePerHour = Widgets.make_entry(width=100)
        self.txtQOverride = Widgets.make_entry(width=100)

        # Create the tooltips for the input widgets.
        self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                               u"application for the selected "
                                               u"relay."))
        self.cmbContactForm.set_tooltip_text(_(u"Select and display the "
                                               u"contact form for the "
                                               u"selected relay."))
        self.cmbContactRating.set_tooltip_text(_(u"Select and display the "
                                                 u"contact current rating for "
                                                 u"the selected relay."))
        self.cmbConstruction.set_tooltip_text(_(u"Select and display the type "
                                                u"of construction for the "
                                                u"sselected relay."))
        self.cmbLoadType.set_tooltip_text(_(u"Select and display the type of "
                                            u"load connected to the selected "
                                            u"relay."))
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected relay."))
        self.cmbTempRating.set_tooltip_text(_(u"Select and display the "
                                              u"temperature rating for the "
                                              u"selected relay."))
        self.txtCyclePerHour.set_tooltip_text(_(u"Enter and display the "
                                                u"average cycles per hour for "
                                                u"the selected relay."))
        self.txtQOverride.set_tooltip_text(_(u"Enter and display the the "
                                             u"user-defined quality factor "
                                             u"for the selected relay."))

        # Connect signals to callback functions.
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed',
                                    self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.txtQOverride.connect('focus-out-event',
                                      self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbTempRating.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbLoadType.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbContactForm.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbContactRating.connect('changed',
                                          self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 7))
        self._lst_handler_id.append(
            self.txtCyclePerHour.connect('focus-out-event',
                                         self._on_focus_out, 8))

        # Create the input widgets specific to Relay subcategories.
        if self._subcategory == 64:         # Mechanical
            self._lst_stress_labels = [_(u"Quality:"),
                                       _(u"\u03C0<sub>Q</sub> Override:"),
                                       _(u"Contact Rating:"),
                                       _(u"Application:"), _(u"Construction:"),
                                       _(u"Rated Temperature (\u00B0C):"),
                                       _(u"Load Type:"), _(u"Contact Form:"),
                                       _(u"Cycling Rate (Cycles/Hour):")]

            # Populate the gtk.ComboBox().
            _lst_quality = ["", "R", "P", "X", "U", "M", "L",
                            _(u"Non-Established Reliability"), _(u"Lower")]
            _lst_form = ["", "SPST", "DPST", "SPDT", "3PST", "4PST", "DPDT",
                         "3PDT", "4PDT", "6PDT"]
            for _index, _quality in enumerate(_lst_quality):
                self.cmbQuality.insert_text(_index, _quality)
            for _index, _form in enumerate(_lst_form):
                self.cmbContactForm.insert_text(_index, _form)

            self.cmbTempRating.insert_text(0, '')
            self.cmbTempRating.insert_text(1, u"85\u00B0C")
            self.cmbTempRating.insert_text(2, u"125\u00B0C")

            self.cmbLoadType.insert_text(0, '')
            self.cmbLoadType.insert_text(1, _(u"Resistive"))
            self.cmbLoadType.insert_text(2, _(u"Inductive"))
            self.cmbLoadType.insert_text(3, _(u"Lamp"))

            self.cmbContactRating.insert_text(0, '')
            self.cmbContactRating.insert_text(1, _(u"Signal Current (Low mV "
                                                   u"and mA)"))
            self.cmbContactRating.insert_text(2, "0-5 Amp")
            self.cmbContactRating.insert_text(3, "5-20 Amp")
            self.cmbContactRating.insert_text(4, "20-600 Amp")

        elif self._subcategory == 65:       # Solid State
            self._lst_stress_labels = [_(u"Quality:"),
                                       _(u"\u03C0<sub>Q</sub> Override:"),
                                       _(u"Construction:")]

            # Populate the gtk.ComboBox().
            self.cmbQuality.insert_text(0, '')
            self.cmbQuality.insert_text(1, u"MIL-SPEC")
            self.cmbQuality.insert_text(2, _(u"Lower"))

            self.cmbConstruction.insert_text(0, '')
            self.cmbConstruction.insert_text(1, _(u"Solid State"))
            self.cmbConstruction.insert_text(2, _(u"Solid State Time Delay"))
            self.cmbConstruction.insert_text(3, _(u"Hybrid"))

    def create_217_count_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count input gtk.Widgets()
        for Relays.

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

        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_count_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        self.cmbQuality.reparent(_fixed)
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.add(_scrollwindow)

        _fixed.show_all()

        return x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress input gtk.Widgets()
        for Relays.

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
        if self._subcategory == 64:         # Mechanical
            (_x_pos, _y_pos) = Widgets.make_labels(self._lst_stress_labels,
                                                   _fixed, 5, 5)
        else:
            (_x_pos, _y_pos) = Widgets.make_labels(self._lst_stress_labels[:3],
                                                   _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
        self.cmbQuality.reparent(_fixed)
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtQOverride, _x_pos, _y_pos[1])

        if self._subcategory == 64:         # Mechanical
            _fixed.put(self.cmbContactRating, _x_pos, _y_pos[2])
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[3])
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[4])
            _fixed.put(self.cmbTempRating, _x_pos, _y_pos[5])
            _fixed.put(self.cmbLoadType, _x_pos, _y_pos[6])
            _fixed.put(self.cmbContactForm, _x_pos, _y_pos[7])
            _fixed.put(self.txtCyclePerHour, _x_pos, _y_pos[8])
        elif self._subcategory == 65:       # Solid State
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[2])

        _fixed.show_all()

        return _x_pos

    def load_217_count_inputs(self, model):
        """
        Method to load the Relay class MIL-HDBK-217FN2 parts count results
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.relay.Relay.Model` to load
                      the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbQuality.set_active(model.quality)

        return False

    def load_217_stress_inputs(self, model):
        """
        Method to load the Relay class MIL-HDBK-217FN2 part stress results
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.relay.Relay.Model` to load
                      the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.cmbQuality.set_active(model.quality)
        self.txtQOverride.set_text(str(fmt.format(model.q_override)))

        if self._subcategory == 64:         # Mechanical
            self.cmbContactRating.set_active(model.contact_rating)
            self._load_application(model.contact_rating)

            self.cmbApplication.set_active(model.application)
            self._load_construction(model.contact_rating, model.application)

            self.cmbConstruction.set_active(model.construction)
            self.cmbTempRating.set_active(model.temperature_rating)
            self.cmbLoadType.set_active(model.load_type)
            self.cmbContactForm.set_active(model.contact_form)
            self.txtCyclePerHour.set_text(
                str(fmt.format(model.cycles_per_hour)))
        elif self._subcategory == 65:       # Solid State
            self.cmbConstruction.set_active(model.construction)

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
            self._hardware_model.construction = combo.get_active()
        elif index == 3:
            self._hardware_model.temperature_rating = combo.get_active()
        elif index == 4:
            self._hardware_model.load_type = combo.get_active()
        elif index == 5:
            self._hardware_model.contact_form = combo.get_active()
        elif index == 6:
            self._hardware_model.contact_rating = combo.get_active()
            self._load_application(self._hardware_model.contact_rating)
        elif index == 7:
            self._hardware_model.application = combo.get_active()
            self._load_construction(self._hardware_model.contact_rating,
                                    self._hardware_model.application)

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
        elif index == 8:
            self._hardware_model.cycles_per_hour = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _load_application(self, rating):
        """
        Method to load the application gtk.Combo() depending on the selected
        contact rating.

        :param int rating: the selected contact rating index.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbApplication.handler_block(self._lst_handler_id[7])

        # Remove existing entries.
        _model = self.cmbApplication.get_model()
        _model.clear()

        # Load the new entries.
        _n_applications = len(self._lst_application[rating - 1])
        for i in range(_n_applications):
            self.cmbApplication.insert_text(
                i, self._lst_application[rating - 1][i])

        self.cmbApplication.handler_unblock(self._lst_handler_id[7])

        return False

    def _load_construction(self, rating, application):
        """
        Method to load the construction gtk.Combo() depending on the selected
        contact rating.

        :param int rating: the selected contact rating index.
        :param int application: the selected application index.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbConstruction.handler_block(self._lst_handler_id[2])

        # Remove existing entries.
        _model = self.cmbConstruction.get_model()
        _model.clear()

        # Load the new entries.
        try:
            _n_constructions = len(self._lst_construction[rating - 1][application - 1])
        except IndexError:
            _n_constructions = 0
            print rating, application
        for i in range(_n_constructions):
            self.cmbConstruction.insert_text(
                i, self._lst_construction[rating - 1][application - 1][i])

        self.cmbConstruction.handler_unblock(self._lst_handler_id[2])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    Relay.  The output attributes of a Relay Work Book view are:
    """

    def __init__(self, model):
        """
        Method to initialize an instance of the Relay assessment results view.

        :param model: the :py:class:`rtk.hardware.relay.Relay.Model` to create
                      the view for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = \u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>",
                                  u"\u03BB<sub>g</sub>:",
                                  u"\u03C0<sub>Q</sub>:"]
        self._lst_stress_labels = ["",
                                   u"\u03BB<sub>b</sub>:",
                                   u"\u03C0<sub>Q</sub>:",
                                   u"\u03C0<sub>E</sub>:",
                                   u"\u03C0<sub>L</sub>:",
                                   u"\u03C0<sub>C</sub>:",
                                   u"\u03C0<sub>CYC</sub>:",
                                   u"\u03C0<sub>F</sub>:"]

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
        self.txtPiL = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiC = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiCYC = Widgets.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiF = Widgets.make_entry(width=100, editable=False, bold=True)

        self.figDerate = Figure(figsize=(6, 4))
        self.axsDerate = self.figDerate.add_subplot(111)
        self.pltDerate = FigureCanvas(self.figDerate)

        if self._subcategory == 64:         # Mechanical
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>L</sub>\u03C0<sub>C</sub>\u03C0<sub>CYC</sub>\u03C0<sub>F</sub></span>"

        elif self._subcategory == 65:       # Solid State
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected relay."))
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected relay."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected relay."))
        self.txtPiL.set_tooltip_text(_(u"Displays the load stress factor for "
                                       u"the selected relay."))
        self.txtPiC.set_tooltip_text(_(u"Displays the contact form factor for "
                                       u"the selected relay."))
        self.txtPiCYC.set_tooltip_text(_(u"Displays the cycling factor for "
                                         u"the selected relay."))
        self.txtPiF.set_tooltip_text(_(u"Displays the application and "
                                       u"construction factor for the selected "
                                       u"relay."))

    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count result gtk.Widgets()
        for Relays.

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
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])

        _fixed.show_all()

        return _x_pos

    def create_217_stress_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress result gtk.Widgets()
        for Relays.

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

        if self._subcategory == 64:
            # Create and place all the labels for the inputs.
            (_x_pos, _y_pos) = Widgets.make_labels(self._lst_stress_labels,
                                                   _fixed, 5, 25)
            _x_pos = max(x_pos, _x_pos) + 30

            _fixed.put(self.txtPiL, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiC, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiCYC, _x_pos, _y_pos[6])
            _fixed.put(self.txtPiF, _x_pos, _y_pos[7])

        else:
            # Create and place all the labels for the inputs.
            (_x_pos, _y_pos) = Widgets.make_labels(self._lst_stress_labels[:4],
                                                   _fixed, 5, 25)
            _x_pos = max(x_pos, _x_pos) + 30

        # Place the reliability result display widgets.
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[3])

        _fixed.show_all()

        return _x_pos

    def load_217_count_results(self, model):
        """
        Method to load the Relay class MIL-HDBK-217FN2 parts count result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.relay.Relay.Model` to load
                      the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_217_stress_results(self, model):
        """
        Method to load the Relay class MIL-HDBK-217FN2 part stress result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.relay.Relay.Model` to load
                      the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        if self._subcategory == 64:         # Mechanical
            self.txtPiL.set_text(str(fmt.format(model.piL)))
            self.txtPiC.set_text(str(fmt.format(model.piC)))
            self.txtPiCYC.set_text(str(fmt.format(model.piCYC)))
            self.txtPiF.set_text(str(fmt.format(model.piF)))

        return False

    def load_derate_plot(self, model, frame):
        """
        Method to load the stress derate plot for the Relay class.

        :param model: the :py:class:`rtk.hardware.relay.Relay.Model` to load
                      the attributes from.
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
                            model.current_ratio, 'go')
        if(_x[0] != _x[2] and
           model.lst_derate_criteria[1][0] != model.lst_derate_criteria[1][2]):
            self.axsDerate.axis([0.95 * _x[0], 1.05 * _x[2],
                                 model.lst_derate_criteria[1][2],
                                 1.05 * model.lst_derate_criteria[1][0]])
        else:
            self.axsDerate.axis([0.95, 1.05, 0.0, 1.05])

        self.axsDerate.set_title(_(u"Current Derating Curve for %s at %s") %
                                 (model.part_number, model.ref_des),
                                 fontdict={'fontsize': 12,
                                           'fontweight': 'bold',
                                           'verticalalignment': 'baseline'})
        _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                         _(u"Voltage Operating Point")])
        _leg = self.axsDerate.legend(_legend, loc='upper right', shadow=True)
        for _text in _leg.get_texts():
            _text.set_fontsize('small')

        # Set the proper labels on the derating curve.
        self.axsDerate.set_xlabel(_(u"Temperature (\u2070C)"),
                                  fontdict={'fontsize': 12,
                                            'fontweight': 'bold'})
        self.axsDerate.set_ylabel(r'$\mathbf{I_{op} / I_{rated}}$',
                                  fontdict={'fontsize': 12,
                                            'fontweight': 'bold',
                                            'rotation': 'vertical',
                                            'verticalalignment': 'baseline'})

        self.figDerate.tight_layout()

        frame.add(self.pltDerate)
        frame.show_all()

        return False
