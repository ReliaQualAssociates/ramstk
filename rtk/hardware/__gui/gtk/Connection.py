#!/usr/bin/env python
"""
####################################################
Connection Package Component Specific Work Book View
####################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.hardware.gui.gtk.Connection.py is part of The RTK Project
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
    The Work Book view for displaying all the attributes for a connection.  The
    attributes of a connection Work Book view are:

    :cvar dict dicQuality:

    :ivar list _lst_count_labels:
    :ivar list _lst_stress_labels:
    :ivar list _lst_quality:
    :ivar list _lst_handler_id:
    :ivar :py:class:`rtk.hardware.connection.Connection.Model` _hardware_model:
    :ivar int _subcategory:
    :ivar gtk.ComboBox cmbConfiguration:
    :ivar gtk.ComboBox cmbConnectionType:
    :ivar gtk.ComboBox cmbInsert:
    :ivar gtk.ComboBox cmbQuality:
    :ivar gtk.ComboBox cmbSpecification:
    :ivar gtk.ComboBox cmbTechnology:
    :ivar gtk.Entry txtActiveContacts:
    :ivar gtk.Entry txtAmpsPerContact:
    :ivar gtk.Entry txtCommercialPiQ:
    :ivar gtk.Entry txtContactGauge:
    :ivar gtk.Entry txtMateCycles:
    :ivar gtk.Entry txtNumberWave:
    :ivar gtk.Entry txtNumberHand:
    :ivar gtk.Entry txtNumberPlanes:
    """

    dicQuality = {72: ["", "MIL-SPEC", _(u"Lower")],
                  73: ["", "MIL-SPEC", _(u"Lower")],
                  74: ["", "MIL-SPEC", _(u"Lower")],
                  75: ["", "MIL-SPEC", _(u"Lower")],
                  76: ["", _(u"Automated with daily pull test."),
                       _(u"Manual, MIL-SPEC tools and terminals with pull "
                         u"test at beginning and end of each shift."),
                       _(u"Manual, MIL-SPEC tools with pull test at beginning "
                         u"of each shift."),
                       _(u"Anything less than standard criteria.")]}

    def __init__(self, model):
        """
        Method to create an input frame for the Connection data model.

        :param model: the :py:class:`rtk.hardware.connection.Connection.Model`
                      whose attributes will be displayed.
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [_(u"Quality:")]
        self._lst_stress_labels = [_(u"Quality:"),
                                   _(u"\u03C0<sub>Q</sub> Override:")]
        self._lst_quality = self.dicQuality[model.subcategory]

        self._lst_handler_id = []

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.cmbConfiguration = Widgets.make_combo(simple=True)
        self.cmbConnectionType = Widgets.make_combo(simple=True)
        self.cmbInsert = Widgets.make_combo(simple=True)
        self.cmbQuality = Widgets.make_combo(simple=True)
        self.cmbSpecification = Widgets.make_combo(simple=True)
        self.cmbTechnology = Widgets.make_combo(simple=True)
        self.txtActiveContacts = Widgets.make_entry(width=100)
        self.txtAmpsPerContact = Widgets.make_entry(width=100)
        self.txtCommercialPiQ = Widgets.make_entry(width=100)
        self.txtContactGauge = Widgets.make_entry(width=100)
        self.txtMateCycles = Widgets.make_entry(width=100)
        self.txtNumberWave = Widgets.make_entry(width=100)
        self.txtNumberHand = Widgets.make_entry(width=100)
        self.txtNumberPlanes = Widgets.make_entry(width=100)

        # Subcategory specific attributes.
        if self._subcategory == 72:         # Multi-pin
            self._lst_stress_labels.append(_(u"Configuration:"))
            self._lst_stress_labels.append(_(u"Specification:"))
            self._lst_stress_labels.append(_(u"Insert Material:"))
            self._lst_stress_labels.append(_(u"Contact Gauge:"))
            self._lst_stress_labels.append(_(u"# of Active Pins:"))
            self._lst_stress_labels.append(_(u"Amperes per Contact:"))
            self._lst_stress_labels.append(_(u"Mate/Unmate Cycles\n"
                                             u"(per 1000 hours):"))

            self._lst_configuration = ["", _(u"Rack and Panel"),
                                       _(u"Circular"), _(u"Power"),
                                       _(u"Coaxial/Triaxial")]
            self._lst_specification = [["", _(u"MIL-C-28748"),
                                        _(u"MIL-C-83733"), _(u"MIL-C-24303"),
                                        _(u"MIL-C-28804"), _(u"MIL-C-83513")],
                                       ["", _(u"MIL-C-5015"),
                                        _(u"MIL-C-26482"), _(u"MIL-C-28840"),
                                        _(u"MIL-C-38999"), _(u"MIL-C-81511"),
                                        _(u"MIL-C-83723")],
                                       ["", _(u"MIL-C-3767"),
                                        _(u"MIL-C-22992")],
                                       ["", _(u"MIL-C-3607"), _(u"MIL-C-3643"),
                                        _(u"MIL-C-3650"), _(u"MIL-C-3655"),
                                        _(u"MIL-C-25516"), _(u"MIL-C-39012"),
                                        _(u"MIL-C-55235"), _(u"MIL-C-55339"),
                                        _(u"MIL-C-49142")]]
            _lst_A = ["", _(u"Virtreous Glass"), _(u"Alumina Ceramic"),
                      _(u"Polyimide")]
            _lst_B = ["", _(u"Diallylphtalate"), _(u"Melamine"),
                      _(u"Flourosilicone"), _(u"Silicone Rubber"),
                      _(u"Polysulfone"), _(u"Epoxy Resin")]
            _lst_C = ["", _(u"Polytetraflouroethelyne (Teflon)"),
                      _(u"Chlorotriflourethylene (Kel-f)")]
            _lst_D = ["", _(u"Polyamide (Nylon)"),
                      _(u"Polychloroprene (Neoprene)"), _(u"Polyethylene")]

            self.dicInsert = {1: {1: _lst_B, 2: _lst_B,
                                  3: _lst_A + list(x for x in _lst_B
                                                   if x not in _lst_A),
                                  4: _lst_A + list(x for x in _lst_B
                                                   if x not in _lst_A),
                                  5: _lst_A + list(x for x in _lst_B
                                                   if x not in _lst_A)},
                              2: {1: _lst_B + list(x for x in _lst_D
                                                   if x not in _lst_B),
                                  2: _lst_A + list(x for x in _lst_B
                                                   if x not in _lst_A) +
                                     list(x for x in _lst_D
                                          if x not in _lst_A),
                                  3: _lst_A + list(x for x in _lst_B
                                                   if x not in _lst_A),
                                  4: _lst_A + list(x for x in _lst_B
                                                   if x not in _lst_A),
                                  5: _lst_B, 6: _lst_B},
                              3: {1: _lst_B + list(x for x in _lst_D
                                                   if x not in _lst_B),
                                  2: _lst_B + list(x for x in _lst_D
                                                   if x not in _lst_B)},
                              4: {1: _lst_C, 2: _lst_C, 3: _lst_C, 4: _lst_C,
                                  5: _lst_C, 6: _lst_C, 7: _lst_C,
                                  8: _lst_B + list(x for x in _lst_C
                                                   if x not in _lst_B),
                                  9: _lst_B + list(x for x in _lst_C
                                                   if x not in _lst_B)}}

        elif self._subcategory == 73:       # PCB
            self._lst_stress_labels.append(_(u"Contact Gauge:"))
            self._lst_stress_labels.append(_(u"# of Active Pins:"))
            self._lst_stress_labels.append(_(u"Amperes per Contact:"))
            self._lst_stress_labels.append(_(u"Mate/Unmate Cycles\n"
                                             u"(per 1000 hours):"))

        elif self._subcategory == 74:       # IC Socket
            self._lst_stress_labels.append(_(u"# of Active Pins:"))

        elif self._subcategory == 75:       # PTH
            self._lst_technology = ["",
                                    _(u"Printed Wiring Assembly with PTHs"),
                                    _(u"Discrete Wiring with Electroless "
                                      u"Deposited PTH")]

            self._lst_stress_labels.append(_(u"Technology:"))
            self._lst_stress_labels.append(_(u"# of Wave Soldered PTH:"))
            self._lst_stress_labels.append(_(u"# of Hand Soldered PTH:"))
            self._lst_stress_labels.append(_(u"# of Circuit Planes:"))

        elif self._subcategory == 76:
            self._lst_connections = ["",
                                     _(u"Hand Solder, w/o Wrapping"),
                                     _(u"Hand Solder, w/ Wrapping"),
                                     _(u"Crimp"), _(u"Weld"),
                                     _(u"Solderless Wrap"),
                                     _(u"Clip Termination"),
                                     _(u"Reflow Solder")]

            self._lst_stress_labels.append(_(u"Connection Type:"))

        # Create the tooltips for all the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"connection."))
        self.txtCommercialPiQ.set_tooltip_text(_(u"Displays the user-defined "
                                                 u"quality factor for the "
                                                 u"selected connection.  This "
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
            self.cmbConfiguration.connect('changed',
                                          self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed',
                                          self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbInsert.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtContactGauge.connect('focus-out-event',
                                         self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtActiveContacts.connect('focus-out-event',
                                           self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtAmpsPerContact.connect('focus-out-event',
                                           self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtMateCycles.connect('focus-out-event',
                                       self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.cmbTechnology.connect('changed', self._on_combo_changed, 9))
        self._lst_handler_id.append(
            self.txtNumberWave.connect('focus-out-event',
                                       self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtNumberHand.connect('focus-out-event',
                                       self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtNumberPlanes.connect('focus-out-event',
                                         self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.cmbConnectionType.connect('changed',
                                           self._on_combo_changed, 13))

    def create_217_count_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count input gtk.Widgets()
        for Connections.

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
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_count_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
        if self.cmbQuality.get_parent() is not None:
            self.cmbQuality.reparent(_fixed)
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])

        _fixed.show_all()

        return _x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress input gtk.Widgets()
        for Connections.

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
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
        if self.cmbQuality.get_parent() is not None:
            self.cmbQuality.reparent(_fixed)
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtCommercialPiQ, _x_pos, _y_pos[1])

        if self._subcategory == 72:         # Multi-Pin
            # Populate the gtk.ComboBox().
            for _index, _configuration in enumerate(self._lst_configuration):
                self.cmbConfiguration.insert_text(_index, _configuration)

            try:
                _specifications = self._lst_specification[self._hardware_model.configuration - 1]
            except IndexError:
                _specifications = []
            for _index, _specification in enumerate(_specifications):
                self.cmbSpecification.insert_text(_index, _specification)

            # Place all the input widgets.
            _fixed.put(self.cmbConfiguration, _x_pos, _y_pos[2])
            _fixed.put(self.cmbSpecification, _x_pos, _y_pos[3])
            _fixed.put(self.cmbInsert, _x_pos, _y_pos[4])
            _fixed.put(self.txtContactGauge, _x_pos, _y_pos[5])
            _fixed.put(self.txtActiveContacts, _x_pos, _y_pos[6])
            _fixed.put(self.txtAmpsPerContact, _x_pos, _y_pos[7])
            _fixed.put(self.txtMateCycles, _x_pos, _y_pos[8])

        elif self._subcategory == 73:       # PCB
            # Place all the input widgets.
            _fixed.put(self.txtContactGauge, _x_pos, _y_pos[2])
            _fixed.put(self.txtActiveContacts, _x_pos, _y_pos[3])
            _fixed.put(self.txtAmpsPerContact, _x_pos, _y_pos[4])
            _fixed.put(self.txtMateCycles, _x_pos, _y_pos[5])

        elif self._subcategory == 74:       # IC Socket
            # Place the input widgets.
            _fixed.put(self.txtActiveContacts, _x_pos, _y_pos[2])

        elif self._subcategory == 75:       # PTH
            # Load the gtk.ComboBox().
            for _index, _technology in enumerate(self._lst_technology):
                self.cmbTechnology.insert_text(_index, _technology)

            # Place the input widgets.
            _fixed.put(self.cmbTechnology, _x_pos, _y_pos[2])
            _fixed.put(self.txtNumberWave, _x_pos, _y_pos[3])
            _fixed.put(self.txtNumberHand, _x_pos, _y_pos[4])
            _fixed.put(self.txtNumberPlanes, _x_pos, _y_pos[5])

        elif self._subcategory == 76:
            # Load the gtk.ComboBox().
            for _index, _connection in enumerate(self._lst_connections):
                self.cmbConnectionType.insert_text(_index, _connection)

            # Place the input widgets.
            _fixed.put(self.cmbConnectionType, _x_pos, _y_pos[2])

        _fixed.show_all()

        return _x_pos

    def load_217_count_inputs(self, model):
        """
        Method to load the Connection class MIL-HDBK-217FN2 parts count input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.connection.Connection.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbQuality.set_active(int(model.quality))

        return False

    def load_217_stress_inputs(self, model):
        """
        Method to load the Connection class MIL-HDBK-217FN2 part stress input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.connection.Connection.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.cmbQuality.set_active(int(model.quality))
        self.txtCommercialPiQ.set_text(str(fmt.format(model.q_override)))

        # Load subcategory specific widgets.
        if self._subcategory == 72:         # Multi-pin
            self._load_specification(model.configuration)
            self._load_insert_material(model.configuration,
                                       model.specification)

            self.cmbConfiguration.set_active(model.configuration)
            self.cmbSpecification.set_active(model.specification)
            self.cmbInsert.set_active(model.insert)
            self.txtContactGauge.set_text(str(model.contact_gauge))
            self.txtActiveContacts.set_text(str(model.n_active_contacts))
            self.txtAmpsPerContact.set_text(
                str(fmt.format(model.amps_per_contact)))
            self.txtMateCycles.set_text(str(model.mate_unmate_cycles))

        elif self._subcategory == 73:       # PCB
            self.txtContactGauge.set_text(str(model.contact_gauge))
            self.txtActiveContacts.set_text(str(model.n_active_contacts))
            self.txtAmpsPerContact.set_text(
                str(fmt.format(model.amps_per_contact)))
            self.txtMateCycles.set_text(str(model.mate_unmate_cycles))

        elif self._subcategory == 74:       # IC Socket
            self.txtActiveContacts.set_text(str(model.n_active_contacts))

        elif self._subcategory == 75:       # PTH
            self.cmbTechnology.set_active(model.technology)
            self.txtNumberWave.set_text(str(fmt.format(model.n_wave_soldered)))
            self.txtNumberHand.set_text(str(fmt.format(model.n_hand_soldered)))
            self.txtNumberPlanes.set_text(
                str(fmt.format(model.n_circuit_planes)))

        elif self._subcategory == 76:       # Non-PTH
            self.cmbConnectionType.set_active(model.connection_type)

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() 'changed' signals and calls the
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
            self._hardware_model.configuration = combo.get_active()
            self._load_specification(self._hardware_model.configuration)
        elif index == 3:
            self._hardware_model.specification = combo.get_active()
            self._load_insert_material(self._hardware_model.configuration,
                                       self._hardware_model.specification)
        elif index == 4:
            self._hardware_model.insert_material = combo.get_active()
        elif index == 9:
            self._hardware_model.technology = combo.get_active()
        elif index == 13:
            self._hardware_model.connection_type = combo.get_active()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Method to respond to gtk.Entry() 'focus_out' signals and calls the
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
        elif index == 5:
            self._hardware_model.contact_gauge = int(entry.get_text())
        elif index == 6:
            self._hardware_model.n_active_contacts = int(entry.get_text())
        elif index == 7:
            self._hardware_model.amps_per_contact = float(entry.get_text())
        elif index == 8:
            self._hardware_model.mate_unmate_cycles = float(entry.get_text())
        elif index == 10:
            self._hardware_model.n_wave_soldered = int(entry.get_text())
        elif index == 11:
            self._hardware_model.n_hand_soldered = int(entry.get_text())
        elif index == 12:
            self._hardware_model.n_circuit_planes = int(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _load_specification(self, configuration):
        """
        Method to load the specification gtk.ComboBox() whenever a new
        configuration is selected.

        :param int configuration: the selected configuration index.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbSpecification.handler_block(self._lst_handler_id[3])

        # Remove existing entries.
        _model = self.cmbSpecification.get_model()
        _model.clear()

        # Load the new entries.
        _n_specifications = len(self._lst_specification[configuration - 1])
        for i in range(_n_specifications):
            self.cmbSpecification.insert_text(
                i, self._lst_specification[configuration - 1][i])

        self.cmbSpecification.handler_unblock(self._lst_handler_id[3])

        return False

    def _load_insert_material(self, configuration, specification):
        """
        Method to load the insert material gtk.ComboBox() whenever a new
        specification is selected.

        :param int configuration: the selected configuration index.
        :param int specification: the selected specification index.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if configuration < 1 or specification < 1:
            return True

        self.cmbInsert.handler_block(self._lst_handler_id[4])

        # Remove existing entries.
        _model = self.cmbInsert.get_model()
        _model.clear()

        # Load the new entries.
        _inserts = self.dicInsert[configuration][specification]
        _n_inserts = len(_inserts)
        for i in range(_n_inserts):
            self.cmbInsert.insert_text(i, _inserts[i])

        self.cmbInsert.handler_unblock(self._lst_handler_id[4])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    connection.  The output attributes of a connection Work Book view are:
    """

    def __init__(self, model):
        """
        Method to initialize an instance of the Connection assessment results
        view.

        :param model: the :py:class:`rtk.hardware.connection.Connection.Model`
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
        self.txtPiQ = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiK = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiP = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtPiC = Widgets.make_entry(width=100, editable=False, bold=True)
        self.txtInternalTemp = Widgets.make_entry(width=100, editable=False,
                                                  bold=True)

        self.figDerate = Figure(figsize=(6, 4))
        self.axsDerateV = self.figDerate.add_subplot(111)
        self.axsDerateI = self.axsDerateV.twinx()
        self.pltDerate = FigureCanvas(self.figDerate)

        # Subcategory specific attributes.
        if self._subcategory in [72, 73]:   # Multi-pin or PCB
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub>\u03C0<sub>K</sub>\u03C0<sub>P</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>K</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>P</sub>:")
            self._lst_stress_labels.append(u"Internal Contact Temp:")

        elif self._subcategory == 74:       # IC Socket
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub>\u03C0<sub>P</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>P</sub>:")

        elif self._subcategory == 75:       # PTH
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>[N<sub>1</sub>\u03C0<sub>C</sub> + N<sub>2</sub>(\u03C0<sub>C</sub> + 13)]\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>C</sub>:")
            self._lst_stress_labels.append(u"\u03C0<sub>Q</sub>:")

        elif self._subcategory == 76:
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>Q</sub>:")

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected connection."))
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected connection."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected connection."))
        self.txtPiK.set_tooltip_text(_(u"Displays the mating/unmating "
                                       u"correction factor for the selected "
                                       u"connection."))
        self.txtPiP.set_tooltip_text(_(u"Displays the active pins factor for "
                                       u"the selected connection."))
        self.txtInternalTemp.set_tooltip_text(_(u"Displays the internal "
                                                u"contact operating "
                                                u"temperature for the "
                                                u"selected connection."))
        self.txtPiC.set_tooltip_text(_(u"Displays the complexity factor for "
                                       u"the selected connection."))

    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count result gtk.Widgets()
        for Connections.

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
        if self.txtPiQ.get_parent() is not None:
            self.txtPiQ.reparent(_fixed)
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])

        _fixed.show_all()

        return _x_pos

    def create_217_stress_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress result gtk.Widgets()
        for Connections.

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
        if self.txtPiQ.get_parent() is not None:
            self.txtPiQ.reparent(_fixed)
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[2])

        # Subcategory specific widgets.
        if self._subcategory in [72, 73]:   # Multi-pin or PCB
            _fixed.put(self.txtPiK, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiP, _x_pos, _y_pos[4])
            _fixed.put(self.txtInternalTemp, _x_pos, _y_pos[5])

        elif self._subcategory == 74:       # IC Socket
            _fixed.put(self.txtPiP, _x_pos, _y_pos[3])

        elif self._subcategory == 75:       # PTH
            if self.txtPiQ.get_parent() is not None:
                self.txtPiQ.reparent(_fixed)
            _fixed.put(self.txtPiC, _x_pos, _y_pos[3])
            _fixed.put(self.txtPiQ, _x_pos, _y_pos[4])

        elif self._subcategory == 76:
            self.txtPiP.set_tooltip_text(_(u"Displays the effective series "
                                           u"resistance factor for the "
                                           u"selected connection."))

            if self.txtPiQ.get_parent() is not None:
                self.txtPiQ.reparent(_fixed)
            _fixed.put(self.txtPiQ, _x_pos, _y_pos[3])

        _fixed.show_all()

        return _x_pos

    def load_217_count_results(self, model):
        """
        Method to load the Connection class MIL-HDBK-217FN2 parts count result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.connection.Connection.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_217_stress_results(self, model):
        """
        Method to load the Connection class MIL-HDBK-217FN2 part stress result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.connection.Connection.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        if self._subcategory in [72, 73]:   # Multi-pin or PCB
            self.txtPiK.set_text(str(fmt.format(model.piK)))
            self.txtPiP.set_text(str(fmt.format(model.piP)))
            self.txtInternalTemp.set_text(
                str(fmt.format(model.contact_temperature)))

        elif self._subcategory == 74:       # IC Socket
            self.txtPiP.set_text(str(fmt.format(model.piP)))

        elif self._subcategory == 75:       # PTH
            self.txtPiC.set_text(str(fmt.format(model.piC)))
            self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        elif self._subcategory == 76:       # Non-PTH
            self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_derate_plot(self, model, frame):
        """
        Method to load the stress derate plot for the Connection class.

        :param model: the :py:class:`rtk.hardware.connection.Connection.Model`
                      to load the attributes from.
        :param gtk.Frame frame: the gtk.Frame() to embed the derate plot into.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Clear the operating point and derating curve for the component.
        self.axsDerateV.cla()
        self.axsDerateI.cla()

        # Plot the derating curve and operating point.
        _x = [float(model.min_rated_temperature),
              float(model.knee_temperature),
              float(model.max_rated_temperature)]

        _line0 = self.axsDerateV.plot(_x, model.lst_derate_criteria[0], 'r.-',
                                      linewidth=2)
        _line1 = self.axsDerateV.plot(_x, model.lst_derate_criteria[1], 'b.-',
                                      linewidth=2)
        _line2 = self.axsDerateV.plot(model.temperature_active,
                                      model.voltage_ratio, 'go')
        _line3 = self.axsDerateI.plot(model.temperature_active,
                                      model.current_ratio, 'ms')
        _lines = _line0 + _line1 + _line2 + _line3

        if(_x[0] != _x[2] and
           model.lst_derate_criteria[1][0] != model.lst_derate_criteria[1][2]):
            self.axsDerateV.axis([0.95 * _x[0], 1.05 * _x[2],
                                  model.lst_derate_criteria[1][2],
                                  1.05 * model.lst_derate_criteria[1][0]])
            self.axsDerateI.axis([0.95 * _x[0], 1.05 * _x[2],
                                  model.lst_derate_criteria[1][2],
                                  1.05 * model.lst_derate_criteria[1][0]])
        else:
            self.axsDerateV.axis([0.95, 1.05, 0.0, 1.05])
            self.axsDerateI.axis([0.95, 1.05, 0.0, 1.05])

        self.axsDerateV.set_title(
            _(u"Voltage and Current Derating Curve for %s at %s") %
            (model.part_number, model.ref_des),
            fontdict={'fontsize': 12, 'fontweight': 'bold',
                      'verticalalignment': 'baseline'})
        _legend = tuple([_(u"Harsh Environment"), _(u"Mild Environment"),
                         _(u"Voltage Operating Point"),
                         _(u"Current Operating Point")])
        _leg = self.axsDerateV.legend(_lines, _legend, loc='upper right',
                                      shadow=True)
        for _text in _leg.get_texts():
            _text.set_fontsize('small')

        # Set the proper labels on the derating curve.
        self.axsDerateV.set_xlabel(_(u"Temperature (\u2070C)"),
                                   fontdict={'fontsize': 12,
                                             'fontweight': 'bold'})
        self.axsDerateV.set_ylabel(r'$\mathbf{V_{op} / V_{rated}}$',
                                   fontdict={'fontsize': 12,
                                             'fontweight': 'bold',
                                             'rotation': 'vertical',
                                             'verticalalignment': 'baseline'})
        self.axsDerateI.set_ylabel(r'$\mathbf{I_{op} / I_{rated}}$',
                                   fontdict={'fontsize': 12,
                                             'fontweight': 'bold',
                                             'rotation': 'vertical',
                                             'verticalalignment': 'baseline'})

        self.figDerate.tight_layout()

        frame.add(self.pltDerate)
        frame.show_all()

        return False
