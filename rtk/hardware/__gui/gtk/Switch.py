#!/usr/bin/env python
"""
###############################################
Switch Module Component Specific Work Book View
###############################################
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       hardware.gui.gtk.Switch.py is part of The RTK Project
=======
#       rtk.hardware.gui.gtk.Switch.py is part of The RTK Project
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
    The Work Book view for displaying all the attributes for a switch.  The
<<<<<<< HEAD
    attributes of a switch Work Book view are:
=======
    attributes of a Switch Work Book input view are:

    :ivar list _lst_count_labels: the MIL-HDBK-217FN2 parts count method
                                  labels.
    :ivar list _lst_stress_labels: the MIL-HDBK-217FN2 part stress method
                                   labels.
    :ivar list _lst_handler_id: the list containing gtk.Widget() signal handler
                                IDs.
    :ivar :py:class:`rtk.hardware.switch.Switch.Model` _hardware_model:
    :ivar int _subcategory: the Switch subcategory.
    :ivar gtk.ComboBox cmbApplication: the gtk.ComboBox() used to select the
                                       MIL-HDBK-217FN2 switch application.
    :ivar gtk.ComboBox cmbConstruction: the gtk.ComboBox() used to select the
                                       MIL-HDBK-217FN2 switch construction.
    :ivar gtk.ComboBox cmbContactForm: the gtk.ComboBox() used to select the
                                       MIL-HDBK-217FN2 switch contact form.
    :ivar gtk.ComboBox cmbLoadType: the gtk.ComboBox() used to select the
                                    MIL-HDBK-217FN2 load type.
    :ivar gtk.ComboBox cmbQuality: the gtk.ComboBox() used to select the
                                   MIL-HDBK-217FN2 quality.
    :ivar gtk.Entry txtDifferential: the gtk.Entry() used to enter the
                                     MIL-HDBK-217FN2 actuation differential.
    :ivar gtk.Entry txtNContacts: the gtk.Entry() used to enter the
                                  MIL-HDBK-217FN2 number of active contacts.
    :ivar gtk.Entry txtNCycles: the gtk.Entry() used to enter the
                                MIL-HDBK-217FN2 number of switch cycles.
    :ivar gtk.Entry txtQOverride: the gtk.Entry() used to enter the
                                  user-defined quality factor.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Creates an input frame for the Switch data model.

        :param :class `rtk.hardware.Switch.model`: the Switch data model whose
                                                   attributes will be
                                                   displayed.
        """

=======
        Method to create an input frame for the Switch data model.

        :param model: the :py:class:`rtk.hardware.switch.Switch.Model` whose
                      attributes will be displayed.
        """
# TODO: Re-write __init__; current McCabe Complexity metric = 17.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

<<<<<<< HEAD
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
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [_(u"Quality:")]
        self._lst_stress_labels = [_(u"Quality:"),
                                   _(u"\u03C0<sub>Q</sub> Override:")]
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.cmbApplication = Widgets.make_combo(simple=True)
        self.cmbConstruction = Widgets.make_combo(simple=True)
        self.cmbContactForm = Widgets.make_combo(simple=True)
        self.cmbLoadType = Widgets.make_combo(simple=True)
        self.cmbQuality = Widgets.make_combo(simple=True)
        self.txtDifferential = Widgets.make_entry(width=100)
        self.txtNContacts = Widgets.make_entry(width=100)
        self.txtNCycles = Widgets.make_entry(width=100)
        self.txtQOverride = Widgets.make_entry(width=100)

        # Create the tooltips for the input widgets.
        self.cmbConstruction.set_tooltip_text(_(u"Select and display the type "
                                                u"of action for the selected "
                                                u"switch."))
        self.cmbContactForm.set_tooltip_text(_(u"Select and display the "
                                               u"contact form of the selected "
                                               u"switch."))
        self.cmbLoadType.set_tooltip_text(_(u"Select and display the type of "
                                            u"electrical load for the "
                                            u"selected switch."))
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"switch."))
        self.txtDifferential.set_tooltip_text(_(u"Enter and display the "
                                                u"actuation differential "
                                                u"(inches) for the selected "
                                                u"switch."))
        self.txtNContacts.set_tooltip_text(_(u"Enter and display the number "
                                             u"of active contacts in the "
                                             u"selected switch."))
        self.txtNCycles.set_tooltip_text(_(u"Enter and display the number of "
                                           u"switching cycles per hour for "
                                           u"the selected switch."))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self.txtQOverride.set_tooltip_text(_(u"Enter and display the the "
                                             u"user-defined quality factor "
                                             u"for the selected "
                                             u"switch."))

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
=======
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.txtQOverride.connect('focus-out-event',
                                      self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbContactForm.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbLoadType.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtNCycles.connect('focus-out-event', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtNContacts.connect('focus-out-event',
                                      self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtDifferential.connect('focus-out-event',
                                         self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.cmbApplication.connect('changed', self._on_combo_changed, 8))

        # Create the input widgets specific to Switch subcategories.
        if self._subcategory == 67:         # Toggle
            self._lst_stress_labels.append(_(u"Construction:"))
            self._lst_stress_labels.append(_(u"Contact Form:"))
            self._lst_stress_labels.append(_(u"Load Type:"))
            self._lst_stress_labels.append(_(u"Switching Cycles per Hour:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Load the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            _lst_construction = ["", _(u"Snap Action"), _(u"Non-snap Action")]
            _lst_form = ["", "SPST", "DPST", "SPDT", "3PST", "4PST", "DPDT",
                         "3PDT", "4PDT", "6PDT"]
            _lst_load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]

            for _index, _construction in enumerate(_lst_construction):
                self.cmbConstruction.insert_text(_index, _construction)
            for _index, _form in enumerate(_lst_form):
                self.cmbContactForm.insert_text(_index, _form)
            for _index, _load in enumerate(_lst_load):
                self.cmbLoadType.insert_text(_index, _load)

<<<<<<< HEAD
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
=======
        elif self._subcategory == 68:       # Sensitive
            self._lst_stress_labels.append(_(u"Load Type:"))
            self._lst_stress_labels.append(_(u"# of Active Contacts:"))
            self._lst_stress_labels.append(_(u"Actuation Differential (in):"))
            self._lst_stress_labels.append(_(u"Switching Cycles per Hour:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Load the gtk.ComboBox().
            _lst_quality = ["", "MIL-SPEC", _(u"Lower")]
            _lst_load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]

            for _index, _load in enumerate(_lst_load):
                self.cmbLoadType.insert_text(_index, _load)

<<<<<<< HEAD
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
=======
        elif self._subcategory == 69:       # Rotary
            self._lst_stress_labels.append(_(u"Construction:"))
            self._lst_stress_labels.append(_(u"Load Type:"))
            self._lst_stress_labels.append(_(u"# of Active Contacts:"))
            self._lst_stress_labels.append(_(u"Switching Cycles per Hour:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Populate the gtk.ComboBox().
            _lst_quality = ["", u"MIL-SPEC", _(u"Lower")]
            _lst_load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]
            _lst_construction = ["", _(u"Ceramic RF Wafers"),
                                 _(u"Medium Power Wafers")]

            for _index, _construction in enumerate(_lst_construction):
                self.cmbConstruction.insert_text(_index, _construction)
            for _index, _load in enumerate(_lst_load):
                self.cmbLoadType.insert_text(_index, _load)

<<<<<<< HEAD
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
=======
        elif self._subcategory == 70:       # Thumbwheel
            self._lst_stress_labels.append(_(u"Load Type:"))
            self._lst_stress_labels.append(_(u"# of Active Contacts:"))
            self._lst_stress_labels.append(_(u"Switching Cycles per Hour:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Populate the gtk.ComboBox().
            _lst_quality = ["", u"MIL-SPEC", _(u"Lower")]
            _lst_load = ["", _(u"Resistive"), _(u"Inductive"), _(u"Lamp")]

            for _index, _load in enumerate(_lst_load):
                self.cmbLoadType.insert_text(_index, _load)

<<<<<<< HEAD
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
=======
        elif self._subcategory == 71:       # Circuit breaker
            self._lst_stress_labels.append(_(u"Construction:"))
            self._lst_stress_labels.append(_(u"Contact Form:"))
            self._lst_stress_labels.append(_(u"Application:"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Populate the gtk.ComboBox().
            _lst_quality = ["", u"MIL-SPEC", _(u"Lower")]
            _lst_construction = ["", _(u"Magnetic"), _(u"Thermal"),
                                 _(u"Thermal-Magnetic")]
            _lst_form = ["", u"SPST", u"DPST", u"3PST", u"4PST"]
            _lst_application = ["", _(u"Not Used as Power On/Off Switch"),
                                _(u"Used as Power On/Off Switch")]

            for _index, _construction in enumerate(_lst_construction):
                self.cmbConstruction.insert_text(_index, _construction)
            for _index, _form in enumerate(_lst_form):
                self.cmbContactForm.insert_text(_index, _form)
            for _index, _application in enumerate(_lst_application):
                self.cmbApplication.insert_text(_index, _application)

<<<<<<< HEAD
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
=======
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
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        # Populate the quality gtk.ComboBox().
        for _index, _quality in enumerate(_lst_quality):
            self.cmbQuality.insert_text(_index, _quality)

    def create_217_count_inputs(self, x_pos=5):
        """
<<<<<<< HEAD
        Creates the MIL-HDBK-217FN2 part count input widgets for
        Switchs.
=======
        Method to create the MIL-HDBK-217FN2 parts count input gtk.Widgets()
        for Switches.
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
        Creates the MIL-HDBK-217FN2 part stress input widgets for
        Switchs.
=======
        Method to create the MIL-HDBK-217FN2 part stress input gtk.Widgets()
        for Switches.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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

<<<<<<< HEAD
    def load_217_stress_inputs(self, model):
        """
        Loads the Switch class MIL-HDBK-217FN2 part stress gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
=======
    def load_217_count_inputs(self, model):
        """
        Method to load the Switch class MIL-HDBK-217FN2 parts count
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.switch.Switch.Model` to load
                      the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbQuality.set_active(model.quality)

        return False

    def load_217_stress_inputs(self, model):
        """
        Method to load the Switch class MIL-HDBK-217FN2 part stress
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.switch.Switch.Model` to load
                      the attributes from.
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
<<<<<<< HEAD
        Responds to gtk.ComboBox() changed signals and calls the correct
        function or method, passing any parameters as needed.
=======
        Method to respond to gtk.ComboBox() 'changed' signals and call the
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
=======
        elif index == 2:
            self._hardware_model.construction = combo.get_active()
        elif index == 3:
            self._hardware_model.contact_form = combo.get_active()
        elif index == 4:
            self._hardware_model.load_type = combo.get_active()
        elif index == 8:
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            self._hardware_model.use = combo.get_active()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
<<<<<<< HEAD
        Responds to gtk.Entry() focus_out signals and calls the correct
        function or method, passing any parameters as needed.
=======
        Method to respond to gtk.Entry() 'focus_out' signals and call the
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
=======
        elif index == 5:
            self._hardware_model.cycles_per_hour = float(entry.get_text())
        elif index == 6:
            self._hardware_model.n_contacts = int(entry.get_text())
        elif index == 7:
            self._hardware_model.actuation_differential = float(entry.get_text())
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a Switch.
<<<<<<< HEAD
    The output attributes of a Switch Work Book view are:
=======
    The output attributes of a Switch Work Book results view are:

    :ivar list _lst_count_labels: list containing MIL-HDBK-217FN2 parts count
                                  method labels.
    :ivar list _lst_stress_labels: list containing MIL-HDBK-217FN2 part stress
                                   method labels.
    :ivar :py:class:`rtk.hardware.switch.Switch.Model` _hardware_model:
    :ivar int _subcategory: the Switch subcategory.
    :ivar gtk.Entry txtLambdaB: the gtk.Entry() that displays the
                                MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar gtk.Entry txtPiQ: the gtk.Entry() that displays the MIL-HDBK-217FN2
                            quality factor.
    :ivar gtk.Entry txtPiE: the gtk.Entry() that displays the MIL-HDBK-217FN2
                            operating environment factor.
    :ivar gtk.Entry txtPiCYC: the gtk.Entry() that displays the MIL-HDBK-217FN2
                              cycling factor.
    :ivar gtk.Entry txtPiL: the gtk.Entry() that displays the MIL-HDBK-217FN2
                            load factor.
    :ivar gtk.Entry txtPiC: the gtk.Entry() that displays the MIL-HDBK-217FN2
                            contact form and quantity factor.
    :ivar gtk.Entry txtBaseHr2: the gtk.Entry() that displays the
                                MIL-HDBK-217FN2 thumbwheel switch active
                                contact base hazard rate.
    :ivar gtk.Entry txtPiN: the gtk.Entry() that displays the MIL-HDBK-217FN2
                            active contact factor.
    :ivar gtk.Entry txtPiU: the gtk.Entry() that displays the MIL-HDBK-217FN2
                            circuit breaker usage factor.
    :ivar figDerate:
    :ivar axsDerate:
    :ivar pltDerate:
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Initializes an instance of the Switch assessment results view.

        :param model: the instance of the Switch data model to create
                      the view for.
=======
        Method to initialize an instance of the Switch assessment results view.

        :param model: the :py:class:`rtk.hardware.switch.Switch.Model` to
                      create the view for.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

<<<<<<< HEAD
        # Initialize private list attributes.
        self._lst_labels = ["", u"\u03BB<sub>b</sub>:", u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = \u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>",
                                  u"\u03BB<sub>g</sub>:",
                                  u"\u03C0<sub>Q</sub>:"]
        self._lst_stress_labels = ["", u"\u03BB<sub>b</sub>:",
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
        self.txtPiCYC = Widgets.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiL = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiC = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtBaseHr2 = Widgets.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtPiN = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiU = Widgets.make_entry(width=100, editable=False, bold=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.figDerate = Figure(figsize=(6, 4))
        self.axsDerate = self.figDerate.add_subplot(111)
        self.pltDerate = FigureCanvas(self.figDerate)

<<<<<<< HEAD
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
=======
        # Create the tooltips for the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected switch."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected switch."))
        self.txtPiCYC.set_tooltip_text(_(u"Displays the cycling factor for "
                                         u"the selected switch."))
        self.txtPiL.set_tooltip_text(_(u"Displays the load stress factor for "
                                       u"the selected switch."))
        self.txtPiC.set_tooltip_text(_(u"Displays the contact form and "
                                       u"quantity factor for the selected "
                                       u"switch."))
        self.txtPiN.set_tooltip_text(_(u"Displays the number of active "
                                       u"contacts factor for the selected "
                                       u"switch."))

        if self._subcategory == 67:         # Toggle
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>C</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>CYC</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>L</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>C</sub>:")

        elif self._subcategory in [68, 69]: # Sensitive or rotary
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>CYC</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>L</sub>:")

        elif self._subcategory == 70:       # Thumbwheel
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = (\u03BB<sub>b1</sub> + \u03C0<sub>N</sub>\u03BB<sub>b2</sub>)\u03BB<sub>b</sub>\u03C0<sub>CYC</sub>\u03C0<sub>L</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels[1] = u"\u03BB<sub>b1</sub>:"
            self._lst_stress_labels.append(u"\u03C0<sub>N</sub>:")
            self._lst_stress_labels.append(u"\u03BB<sub>b2</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>CYC</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>L</sub>:")

        elif self._subcategory == 71:       # Circuit breaker
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>C</sub>\u03C0<sub>U</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>C</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>U</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>Q</sub>:")
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            self.txtPiC.set_tooltip_text(_(u"Displays the configuration "
                                           u"factor for the selected "
                                           u"breaker."))
            self.txtPiU.set_tooltip_text(_(u"Displays the use factor for the "
                                           u"selected breaker."))
            self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for "
                                           u"the selected breaker."))

<<<<<<< HEAD
        # Create the tooltips for the common results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected switch."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected switch."))

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Switchs.
=======
    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count result widgets for
        Switchs.

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
        Method to create the MIL-HDBK-217FN2 part stress result widgets for
        Switchs.
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
<<<<<<< HEAD
=======
            if self.txtPiQ.get_parent() is not None:
                self.txtPiQ.reparent(_fixed)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _fixed.put(self.txtPiC, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiU, _x_pos, _y_pos[4])
            _fixed.put(self.txtPiQ, _x_pos, _y_pos[5])

        # Place the reliability result display widgets.
<<<<<<< HEAD
=======
        if self.txtLambdaB.get_parent() is not None:
            self.txtLambdaB.reparent(_fixed)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[2])

        _fixed.show_all()

        return _x_pos

<<<<<<< HEAD
    def load_217_stress_results(self, model):
        """
        Loads the Switch class result gtk.Widgets().

        :param model: the Switch data model to load the attributes from.
=======
    def load_217_count_results(self, model):
        """
        Method to load the MIL-HDBK-217FN2 Switch class parts count result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.switch.Switch.Model` to load
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
        Method to load the MIL-HDBK-217FN2 Switch class part stress result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.switch.Switch.Model` to load
                      the attributes from.
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
<<<<<<< HEAD
        Loads the stress derate plot for the Switch class.

        :param model: the Hardware data model to load the attributes from.
=======
        Method to load the stress derate plot for the Switch class.

        :param model: the :py:class:`rtk.hardware.switch.Switch.Model` to load
                      the attributes from.
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
        self.axsDerate.plot(model.temperature_active,
                            model.current_ratio, 'go')
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

        self.axsDerate.set_title(_(u"Current Derating Curve for %s at %s") %
                                 (model.part_number, model.ref_des),
                                 fontdict={'fontsize': 12,
                                           'fontweight': 'bold',
                                           'verticalalignment': 'baseline'})
        _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                         _(u"Current Operating Point")])
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
        self.axsDerate.set_ylabel(r'$\mathbf{I_{op} / I_{rated}}$',
                                  fontdict={'fontsize': 12,
                                            'fontweight': 'bold',
                                            'rotation': 'vertical',
                                            'verticalalignment': 'baseline'})

        self.figDerate.tight_layout()

        frame.add(self.pltDerate)
        frame.show_all()

        return False
