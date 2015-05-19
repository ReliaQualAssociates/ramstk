#!/usr/bin/env python
"""
###############################################
Switch Module Component Specific Work Book View
###############################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       hardware.gui.gtk.Switch.py is part of The RTK Project
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
    The Work Book view for displaying all the attributes for a switch.  The
    attributes of a switch Work Book view are:
    """

    def __init__(self, model):
        """
        Creates an input frame for the Switch data model.

        :param :class `rtk.hardware.Switch.model`: the Switch data model whose
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

        # === Create the input widgets common to all Switch types === #
        self.cmbQuality = _widg.make_combo(simple=True)
        self.txtQOverride = _widg.make_entry(width=100)

        # Create the tooltips for the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"switch."))
        self.txtQOverride.set_tooltip_text(_(u"Enter and display the the "
                                             u"user-defined quality factor "
                                             u"for the selected "
                                             u"switch."))

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

        # Create the input widgets specific to Switch subcategories.
        if self._subcategory == 67:         # Toggle
            self._lst_labels.append(_(u"Construction:"))
            self._lst_labels.append(_(u"Contact Form:"))
            self._lst_labels.append(_(u"Load Type:"))
            self._lst_labels.append(_(u"Switching Cycles per Hour:"))

            # Create component specific input widgets.
            self.cmbConstruction = _widg.make_combo(simple=True)
            self.cmbContactForm = _widg.make_combo(simple=True)
            self.cmbLoadType = _widg.make_combo(simple=True)
            self.txtNCycles = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbContactForm.set_tooltip_text(_(u"Select and display the "
                                                   u"contact form of the "
                                                   u"selected switch."))
            self.cmbConstruction.set_tooltip_text(_(u"Select and display the "
                                                    u"type of action for the "
                                                    u"selected switch."))
            self.cmbLoadType.set_tooltip_text(_(u"Select and display the type "
                                                u"of electrical load for the "
                                                u"selected switch."))
            self.txtNCycles.set_tooltip_text(_(u"Enter and display the number "
                                               u"of switching cycles per hour "
                                               u"for the selected switch."))

            # Load the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            _lst_construction = ["", _(u"Snap Action"), _(u"Non-snap Action")]
            _lst_form = ["", "SPST", "DPST", "SPDT", "3PST", "4PST", "DPDT",
                         "3PDT", "4PDT", "6PDT"]
            _lst_load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]

            for i in range(len(_lst_construction)):
                self.cmbConstruction.insert_text(i, _lst_construction[i])
            for i in range(len(_lst_form)):
                self.cmbContactForm.insert_text(i, _lst_form[i])
            for i in range(len(_lst_load)):
                self.cmbLoadType.insert_text(i, _lst_load[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbContactForm.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbLoadType.connect('changed',
                                         self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNCycles.connect('focus-out-event',
                                        self._on_focus_out, _index))

        elif self._subcategory == 68:       # Sensitive
            self._lst_labels.append(_(u"Load Type:"))
            self._lst_labels.append(_(u"# of Active Contacts:"))
            self._lst_labels.append(_(u"Actuation Differential (in):"))
            self._lst_labels.append(_(u"Switching Cycles per Hour:"))

            # Create component specific input widgets.
            self.cmbLoadType = _widg.make_combo(simple=True)
            self.txtNContacts = _widg.make_entry(width=100)
            self.txtDifferential = _widg.make_entry(width=100)
            self.txtNCycles = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbLoadType.set_tooltip_text(_(u"Select and display the type "
                                                u"of electrical load for the "
                                                u"selected switch."))
            self.txtNContacts.set_tooltip_text(_(u"Enter and display the "
                                                 u"number of active contacts "
                                                 u"in the selected switch."))
            self.txtDifferential.set_tooltip_text(_(u"Enter and display the "
                                                    u"actuation differential "
                                                    u"(inches) for the "
                                                    u"selected switch."))
            self.txtNCycles.set_tooltip_text(_(u"Enter and display the number "
                                               u"of switching cycles per hour "
                                               u"for the selected switch."))

            # Load the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            _lst_load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]

            for i in range(len(_lst_load)):
                self.cmbLoadType.insert_text(i, _lst_load[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbLoadType.connect('changed',
                                         self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNContacts.connect('focus-out-event',
                                          self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtDifferential.connect('focus-out-event',
                                             self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNCycles.connect('focus-out-event',
                                        self._on_focus_out, _index))

        elif self._subcategory == 69:       # Rotary
            self._lst_labels.append(_(u"Construction:"))
            self._lst_labels.append(_(u"Load Type:"))
            self._lst_labels.append(_(u"# of Active Contacts:"))
            self._lst_labels.append(_(u"Switching Cycles per Hour:"))

            # Create component specific input widgets.
            self.cmbConstruction = _widg.make_combo(simple=True)
            self.cmbLoadType = _widg.make_combo(simple=True)
            self.txtNContacts = _widg.make_entry(width=100)
            self.txtNCycles = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbConstruction.set_tooltip_text(_(u"Select and display the "
                                                    u"wafer construction of "
                                                    u"the selected switch."))
            self.cmbLoadType.set_tooltip_text(_(u"Select and display the type "
                                                u"of electrical load for the "
                                                u"selected switch."))
            self.txtNContacts.set_tooltip_text(_(u"Enter and display the "
                                                 u"number of active contacts "
                                                 u"in the selected switch."))
            self.txtNCycles.set_tooltip_text(_(u"Enter and display the number "
                                               u"of switching cycles per hour "
                                               u"for the selected switch."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", u"MIL-SPEC", _(u"Lower")]
            _lst_load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]
            _lst_construction = ["", _(u"Ceramic RF Wafers"),
                                 _(u"Medium Power Wafers")]

            for i in range(len(_lst_construction)):
                self.cmbConstruction.insert_text(i, _lst_construction[i])
            for i in range(len(_lst_load)):
                self.cmbLoadType.insert_text(i, _lst_load[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbLoadType.connect('changed',
                                         self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNContacts.connect('focus-out-event',
                                          self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNCycles.connect('focus-out-event',
                                        self._on_focus_out, _index))

        elif self._subcategory == 70:       # Thumbwheel
            self._lst_labels.append(_(u"Load Type:"))
            self._lst_labels.append(_(u"# of Active Contacts:"))
            self._lst_labels.append(_(u"Switching Cycles per Hour:"))

            # Create component specific input widgets.
            self.cmbLoadType = _widg.make_combo(simple=True)
            self.txtNContacts = _widg.make_entry(width=100)
            self.txtNCycles = _widg.make_entry(width=100)

            # Create the tooltips for the input widgets.
            self.cmbLoadType.set_tooltip_text(_(u"Select and display the type "
                                                u"of electrical load for the "
                                                u"selected switch."))
            self.txtNContacts.set_tooltip_text(_(u"Enter and display the "
                                                 u"number of active contacts "
                                                 u"in the selected switch."))
            self.txtNCycles.set_tooltip_text(_(u"Enter and display the number "
                                               u"of switching cycles per hour "
                                               u"for the selected switch."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", u"MIL-SPEC", _(u"Lower")]
            _lst_load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]

            for i in range(len(_lst_load)):
                self.cmbLoadType.insert_text(i, _lst_load[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbLoadType.connect('changed',
                                         self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNContacts.connect('focus-out-event',
                                          self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtNCycles.connect('focus-out-event',
                                        self._on_focus_out, _index))

        elif self._subcategory == 71:       # Circuit breaker
            self._lst_labels.append(_(u"Construction:"))
            self._lst_labels.append(_(u"Contact Form:"))
            self._lst_labels.append(_(u"Application:"))

            # Create component specific input widgets.
            self.cmbConstruction = _widg.make_combo(simple=True)
            self.cmbContactForm = _widg.make_combo(simple=True)
            self.cmbApplication = _widg.make_combo(simple=True)

            # Create the tooltips for the input widgets.
            self.cmbConstruction.set_tooltip_text(_(u"Select and display the "
                                                    u"type of overload for "
                                                    u"the selected breaker."))
            self.cmbContactForm.set_tooltip_text(_(u"Select and display the "
                                                   u"contact form of the "
                                                   u"selected breaker."))
            self.cmbApplication.set_tooltip_text(_(u"Select and display the "
                                                   u"application of the "
                                                   u"selected breaker."))

            # Populate the gtk.ComboBox().
            _lst_quality = ["", u"MIL-SPEC", _(u"Lower")]
            _lst_construction = ["", _(u"Magnetic"), _(u"Thermal"),
                                 _(u"Thermal-Magnetic")]
            _lst_form = ["", u"SPST", u"DPST", u"3PST", u"4PST"]
            _lst_application = ["", _(u"Not Used as Power On/Off Switch"),
                                _(u"Used as Power On/Off Switch")]

            for i in range(len(_lst_construction)):
                self.cmbConstruction.insert_text(i, _lst_construction[i])
            for i in range(len(_lst_form)):
                self.cmbContactForm.insert_text(i, _lst_form[i])
            for i in range(len(_lst_application)):
                self.cmbApplication.insert_text(i, _lst_application[i])

            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbContactForm.connect('changed',
                                            self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.cmbApplication.connect('changed',
                                            self._on_combo_changed, _index))

        # Populate the quality gtk.ComboBox().
        for i in range(len(_lst_quality)):
            self.cmbQuality.insert_text(i, _lst_quality[i])

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for
        Switchs.

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
        Switchs.

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

        if self._subcategory == 67:         # Toggle
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[2])
            _fixed.put(self.cmbContactForm, _x_pos, _y_pos[3])
            _fixed.put(self.cmbLoadType, _x_pos, _y_pos[4])
            _fixed.put(self.txtNCycles, _x_pos, _y_pos[5])
        elif self._subcategory == 68:       # Sensitive
            _fixed.put(self.cmbLoadType, _x_pos, _y_pos[2])
            _fixed.put(self.txtNContacts, _x_pos, _y_pos[3])
            _fixed.put(self.txtDifferential, _x_pos, _y_pos[4])
            _fixed.put(self.txtNCycles, _x_pos, _y_pos[5])
        elif self._subcategory == 69:       # Rotary
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[2])
            _fixed.put(self.cmbLoadType, _x_pos, _y_pos[3])
            _fixed.put(self.txtNContacts, _x_pos, _y_pos[4])
            _fixed.put(self.txtNCycles, _x_pos, _y_pos[5])
        elif self._subcategory == 70:       # Thumbwheel
            _fixed.put(self.cmbLoadType, _x_pos, _y_pos[2])
            _fixed.put(self.txtNContacts, _x_pos, _y_pos[3])
            _fixed.put(self.txtNCycles, _x_pos, _y_pos[4])
        elif self._subcategory == 71:       # Circuit breaker
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[2])
            _fixed.put(self.cmbContactForm, _x_pos, _y_pos[3])
            _fixed.put(self.cmbApplication, _x_pos, _y_pos[4])

        _fixed.show_all()

        return _x_pos

    def load_217_stress_inputs(self, model):
        """
        Loads the Switch class MIL-HDBK-217FN2 part stress gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.cmbQuality.set_active(model.quality)
        self.txtQOverride.set_text(str(fmt.format(model.q_override)))

        if self._subcategory == 67:         # Toggle
            self.cmbConstruction.set_active(model.construction)
            self.cmbContactForm.set_active(model.contact_form)
            self.cmbLoadType.set_active(model.load_type)
            self.txtNCycles.set_text(str(fmt.format(model.cycles_per_hour)))
        elif self._subcategory == 68:       # Sensitive
            self.cmbLoadType.set_active(model.load_type)
            self.txtNContacts.set_text(str(fmt.format(model.n_contacts)))
            self.txtDifferential.set_text(
                str(fmt.format(model.actuation_differential)))
            self.txtNCycles.set_text(str(fmt.format(model.cycles_per_hour)))
        elif self._subcategory == 69:       # Rotary
            self.cmbConstruction.set_active(model.construction)
            self.cmbLoadType.set_active(model.load_type)
            self.txtNContacts.set_text(str(fmt.format(model.n_contacts)))
            self.txtNCycles.set_text(str(fmt.format(model.cycles_per_hour)))
        elif self._subcategory == 70:       # Thumbwheel
            self.cmbLoadType.set_active(model.load_type)
            self.txtNContacts.set_text(str(fmt.format(model.n_contacts)))
            self.txtNCycles.set_text(str(fmt.format(model.cycles_per_hour)))
        elif self._subcategory == 71:       # Circuit breaker
            self.cmbConstruction.set_active(model.construction)
            self.cmbContactForm.set_active(model.contact_form)
            self.cmbApplication.set_active(model.use)

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
        elif index == 2 and self._subcategory in [67, 69, 71]:
            self._hardware_model.construction = combo.get_active()
        elif index == 2 and self._subcategory in [68, 70]:
            self._hardware_model.load_type = combo.get_active()
        elif index == 3 and self._subcategory in [67, 71]:
            self._hardware_model.contact_form = combo.get_active()
        elif index == 3 and self._subcategory == 69:
            self._hardware_model.load_type = combo.get_active()
        elif index == 4 and self._subcategory == 67:
            self._hardware_model.load_type = combo.get_active()
        elif index == 4 and self._subcategory == 71:
            self._hardware_model.use = combo.get_active()

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
        elif index == 3 and self._subcategory in [68, 70]:
            self._hardware_model.n_contacts = int(entry.get_text())
        elif index == 4 and self._subcategory == 68:
            self._hardware_model.actuation_differential = float(entry.get_text())
        elif index == 4 and self._subcategory == 69:
            self._hardware_model.n_contacts = float(entry.get_text())
        elif index == 4 and self._subcategory == 70:
            self._hardware_model.cycles_per_hour = float(entry.get_text())
        elif index == 5 and self._subcategory in [67, 68, 69]:
            self._hardware_model.cycles_per_hour = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a Switch.
    The output attributes of a Switch Work Book view are:
    """

    def __init__(self, model):
        """
        Initializes an instance of the Switch assessment results view.

        :param model: the instance of the Switch data model to create
                      the view for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

        # Initialize private list attributes.
        self._lst_labels = ["", u"\u03BB<sub>b</sub>:", u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

        self.figDerate = Figure(figsize=(6, 4))
        self.axsDerate = self.figDerate.add_subplot(111)
        self.pltDerate = FigureCanvas(self.figDerate)

        if self._subcategory == 67:         # Toggle
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>C</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>CYC</sub>:")
            self._lst_labels.append(u"\u03C0<sub>L</sub>:")
            self._lst_labels.append(u"\u03C0<sub>C</sub>:")

            self.txtPiCYC = _widg.make_entry(width=100,
                                             editable=False, bold=True)
            self.txtPiL = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiC = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiCYC.set_tooltip_text(_(u"Displays the cycling factor "
                                             u"for the selected switch."))
            self.txtPiL.set_tooltip_text(_(u"Displays the load stress factor "
                                           u"for the selected switch."))
            self.txtPiC.set_tooltip_text(_(u"Displays the contact form and "
                                           u"quantity factor for the selected "
                                           u"switch."))

        elif self._subcategory in [68, 69]: # Sensitive or rotary
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>CYC</sub>:")
            self._lst_labels.append(u"\u03C0<sub>L</sub>:")

            self.txtPiCYC = _widg.make_entry(width=100,
                                             editable=False, bold=True)
            self.txtPiL = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiCYC.set_tooltip_text(_(u"Displays the cycling factor "
                                             u"for the selected switch."))
            self.txtPiL.set_tooltip_text(_(u"Displays the load stress factor "
                                           u"for the selected switch."))

        elif self._subcategory == 70:       # Thumbwheel
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (\u03BB<sub>b1</sub> + \u03C0<sub>N</sub>\u03BB<sub>b2</sub>)\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels[1] = u"\u03BB<sub>b1</sub>:"
            self._lst_labels.append(u"\u03C0<sub>N</sub>:")
            self._lst_labels.append(u"\u03BB<sub>b2</sub>:")
            self._lst_labels.append(u"\u03C0<sub>CYC</sub>:")
            self._lst_labels.append(u"\u03C0<sub>L</sub>:")

            self.txtBaseHr2 = _widg.make_entry(width=100,
                                               editable=False, bold=True)
            self.txtPiN = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiCYC = _widg.make_entry(width=100,
                                             editable=False, bold=True)
            self.txtPiL = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiN.set_tooltip_text(_(u"Displays the number of active "
                                           u"contacts factor for the selected "
                                           u"switch."))
            self.txtPiCYC.set_tooltip_text(_(u"Displays the cycling factor "
                                             u"for the selected switch."))
            self.txtPiL.set_tooltip_text(_(u"Displays the load stress factor "
                                           u"for the selected switch."))

        elif self._subcategory == 71:       # Circuit breaker
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>C</sub>:")
            self._lst_labels.append(u"\u03C0<sub>U</sub>:")
            self._lst_labels.append(u"\u03C0<sub>Q</sub>:")

            self.txtPiC = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiU = _widg.make_entry(width=100,
                                           editable=False, bold=True)
            self.txtPiQ = _widg.make_entry(width=100,
                                           editable=False, bold=True)

            self.txtPiC.set_tooltip_text(_(u"Displays the configuration "
                                           u"factor for the selected "
                                           u"breaker."))
            self.txtPiU.set_tooltip_text(_(u"Displays the use factor for the "
                                           u"selected breaker."))
            self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for "
                                           u"the selected breaker."))

        # Create the tooltips for the common results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected switch."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected switch."))

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Switchs.

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

        if self._subcategory == 67:         # Toggle
            _fixed.put(self.txtPiCYC, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiL, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiC, _x_pos, _y_pos[5])
        elif self._subcategory in [68, 69]: # Sensitive or rotary
            _fixed.put(self.txtPiCYC, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiL, _x_pos, _y_pos[4])
        elif self._subcategory == 70:       # Thumbwheel
            _fixed.put(self.txtBaseHr2, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiN, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiCYC, _x_pos, _y_pos[5])
            _fixed.put(self.txtPiL, _x_pos, _y_pos[6])
        elif self._subcategory == 71:       # Circuit breaker
            _fixed.put(self.txtPiC, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiU, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiQ, _x_pos, _y_pos[5])

        # Place the reliability result display widgets.
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[2])

        _fixed.show_all()

        return _x_pos

    def load_217_stress_results(self, model):
        """
        Loads the Switch class result gtk.Widgets().

        :param model: the Switch data model to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        if self._subcategory == 67:
            self.txtPiCYC.set_text(str(fmt.format(model.piCYC)))
            self.txtPiL.set_text(str(fmt.format(model.piL)))
            self.txtPiC.set_text(str(fmt.format(model.piC)))
        elif self._subcategory in [68, 69]:
            self.txtPiCYC.set_text(str(fmt.format(model.piCYC)))
            self.txtPiL.set_text(str(fmt.format(model.piL)))
        elif self._subcategory == 70:
            self.txtBaseHr2.set_text(str(fmt.format(model.base_hr2)))
            self.txtPiN.set_text(str(fmt.format(model.piN)))
            self.txtPiCYC.set_text(str(fmt.format(model.piCYC)))
            self.txtPiL.set_text(str(fmt.format(model.piL)))
        elif self._subcategory == 71:
            self.txtPiC.set_text(str(fmt.format(model.piC)))
            self.txtPiU.set_text(str(fmt.format(model.piU)))
            self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_derate_plot(self, model, frame):
        """
        Loads the stress derate plot for the Switch class.

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
                            model.current_ratio, 'go')
        if(_x[0] != _x[2] and
           model.lst_derate_criteria[1][0] != model.lst_derate_criteria[1][2]):
            self.axsDerate.axis([0.95 * _x[0], 1.05 * _x[2],
                                 model.lst_derate_criteria[1][2],
                                 1.05 * model.lst_derate_criteria[1][0]])
        else:
            self.axsDerate.cla().axis([0.95, 1.05, 0.0, 1.05])

        self.axsDerate.set_title(_(u"Current Derating Curve for %s at %s") %
                                 (model.part_number, model.ref_des),
                                 fontdict={'fontsize': 12,
                                           'fontweight' : 'bold',
                                           'verticalalignment': 'baseline'})
        _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                         _(u"Current Operating Point")])
        _leg = self.axsDerate.legend(_legend, 'upper right', shadow=True)
        for _text in _leg.get_texts():
            _text.set_fontsize('small')

        # Set the proper labels on the derating curve.
        self.axsDerate.set_xlabel(_(u"Temperature (\u2070C)"),
                                  fontdict={'fontsize': 12,
                                            'fontweight' : 'bold'})
        self.axsDerate.set_ylabel(r'$\mathbf{I_{op} / I_{rated}}$',
                                  fontdict={'fontsize': 12,
                                            'fontweight' : 'bold',
                                            'rotation': 'vertical',
                                            'verticalalignment': 'baseline'})

        self.figDerate.tight_layout()

        frame.add(self.pltDerate)
        frame.show_all()

        return False
