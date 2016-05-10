#!/usr/bin/env python
"""
##################################################
Inductor Package Component Specific Work Book View
##################################################
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       hardware.gui.gtk.Inductor.py is part of The RTK Project
=======
#       rtk.hardware.gui.gtk.Inductor.py is part of The RTK Project
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
    The Work Book view for displaying all the attributes for an inductive
    device.  The attributes of an inductive device Work Book view are:
    """

    dicQuality = {62: ["", "MIL-SPEC", _(u"Lower")],
                  63: ["", "S", "R", "P", "M", "MIL-C-15305", _(u"Lower")]}
    dicSpecification = {62: ["", "MIL-T-27", "MIL-T-21038", "MIL-T-55631"],
                        63: ["", "MIL-C-15305", "MIL-C-39010"]}
    dicInsulation = {62: [["", "Q", "R", "S", "T", "U", "V"],
                          ["", "Q", "R", "S", "T", "U", "V"],
                          ["", "O", "A", "B", "C"]],
                     63: [["", "O", "A", "B", "C"], ["", "A", "B", "F"]]}

    def __init__(self, model):
        """
<<<<<<< HEAD
        Creates an input frame for the inductive device data model.

        :param :class `rtk.hardware.Inductor.model`: the Inductor data model
                                                     whose attributes will be
                                                     displayed.
=======
        Method to creates an input frame for the inductive device data model.

        :param model: the :py:class:`rtk.hardware.inductor.Inductor.Model`
                      whose attributes will be displayed.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

<<<<<<< HEAD
        # ===== ===== === Initialize private list attributes === ===== ===== #
        self._lst_labels = [_(u"Quality:"),
                            _(u"\u03C0<sub>Q</sub> Override:"),
                            _(u"Specification:"), _(u"Insulation Class:")]
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [_(u"Quality:")]
        self._lst_stress_labels = [_(u"Quality:"),
                                   _(u"\u03C0<sub>Q</sub> Override:"),
                                   _(u"Specification:"),
                                   _(u"Insulation Class:")]
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        self._lst_quality = self.dicQuality[model.subcategory]
        self._lst_specification = self.dicSpecification[model.subcategory]
        self._lst_insulation = self.dicInsulation[model.subcategory]

        self._lst_handler_id = []

<<<<<<< HEAD
        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # ===== Create the input widgets common to all Inductor types ===== #
        self.cmbQuality = _widg.make_combo(simple=True)
        self.cmbSpecification = _widg.make_combo(simple=True)
        self.cmbInsulation = _widg.make_combo(simple=True)
        self.txtCommercialPiQ = _widg.make_entry(width=100)

        # Subcategory specific attributes.
        if self._subcategory == 62:         # Transformer
            self._family = ["", _(u"Pulse Transformer"),
                            _(u"Audio Transformer"), _(u"Power Transformer"),
                            _(u"RF Transformer")]

            self._lst_labels.append(_(u"Family Type:"))
            self._lst_labels.append(_(u"Power Loss (W):"))
            self._lst_labels.append(_(u"Case Surface Area (in2):"))
            self._lst_labels.append(_(u"Weight (lbf):"))
            self._lst_labels.append(_(u"Input Power (W):"))

            self.cmbFamily = _widg.make_combo(simple=True)
            self.txtPowerLoss = _widg.make_entry(width=100)
            self.txtSurfaceArea = _widg.make_entry(width=100)
            self.txtWeight = _widg.make_entry(width=100)
            self.txtInputPower = _widg.make_entry(width=100)

        elif self._subcategory == 63:       # Coil
            self._lst_labels.append(_(u"Construction:"))

            self._lst_construction = ["", _(u"Fixed"), _(u"Variable")]

            self.cmbConstruction = _widg.make_combo(simple=True)

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for Inductors.
=======
        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.cmbConstruction = Widgets.make_combo(simple=True)
        self.cmbFamily = Widgets.make_combo(simple=True)
        self.cmbInsulation = Widgets.make_combo(simple=True)
        self.cmbQuality = Widgets.make_combo(simple=True)
        self.cmbSpecification = Widgets.make_combo(simple=True)
        self.txtCommercialPiQ = Widgets.make_entry(width=100)
        self.txtInputPower = Widgets.make_entry(width=100)
        self.txtPowerLoss = Widgets.make_entry(width=100)
        self.txtSurfaceArea = Widgets.make_entry(width=100)
        self.txtWeight = Widgets.make_entry(width=100)

        # Subcategory specific attributes.
        if self._subcategory == 62:         # Transformer
            self._lst_family = ["", _(u"Pulse Transformer"),
                                _(u"Audio Transformer"),
                                _(u"Power Transformer"), _(u"RF Transformer")]

            self._lst_stress_labels.append(_(u"Family Type:"))
            self._lst_stress_labels.append(_(u"Power Loss (W):"))
            self._lst_stress_labels.append(_(u"Case Surface Area (in2):"))
            self._lst_stress_labels.append(_(u"Weight (lbf):"))
            self._lst_stress_labels.append(_(u"Input Power (W):"))

        elif self._subcategory == 63:       # Coil
            self._lst_stress_labels.append(_(u"Construction:"))

            self._lst_construction = ["", _(u"Fixed"), _(u"Variable")]

        # Create the tooltips for all the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected inductive "
                                           u"device."))
        self.txtCommercialPiQ.set_tooltip_text(_(u"Displays the user-defined "
                                                 u"quality factor for the "
                                                 u"selected inductive "
                                                 u"device.  This value over "
                                                 u"rides the quality factor "
                                                 u"selected above"))

        # Connect signals to callback functions.
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.txtCommercialPiQ.connect('focus-out-event',
                                          self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.cmbSpecification.connect('changed',
                                          self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbInsulation.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbFamily.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.txtPowerLoss.connect('focus-out-event',
                                      self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtSurfaceArea.connect('focus-out-event',
                                        self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtWeight.connect('focus-out-event', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtInputPower.connect('focus-out-event',
                                       self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.cmbConstruction.connect('changed', self._on_combo_changed, 9))

    def create_217_count_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count input gtk.Widgets()
        for Inductors.
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

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.add(_scrollwindow)

        # Populate all the gtk.ComboBox().
<<<<<<< HEAD
        for i in range(len(self._lst_quality)):
            self.cmbQuality.insert_text(i, self._lst_quality[i])

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels[0], _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Create the tooltips for all the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality "
                                           u"level for the selected "
                                           u"connection."))

        # Place all the input widgets.
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])

        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, _index))
        _index += 1

=======
        for _index, _quality in enumerate(self._lst_quality):
            self.cmbQuality.insert_text(_index, _quality)

        # Create and place all the labels for the inputs.
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_count_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
        if self.cmbQuality.get_parent() is not None:
            self.cmbQuality.reparent(_fixed)
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.show_all()

        return _x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
<<<<<<< HEAD
        Creates the MIL-HDBK-217FN2 part stress input widgets for Inductors.
=======
        Method to create the MIL-HDBK-217FN2 part stress input gtk.Widgets()
        for Inductors.
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

        # Populate all the gtk.ComboBox().
<<<<<<< HEAD
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
                                           u"connection."))
        self.txtCommercialPiQ.set_tooltip_text(_(u"Displays the user-defined "
                                                 u"quality factor for the "
                                                 u"selected connection.  This "
                                                 u"value over rides the "
                                                 u"quality factor selected "
                                                 u"above."))

        # Place all the input widgets.
=======
        for _index, _quality in enumerate(self._lst_quality):
            self.cmbQuality.insert_text(_index, _quality)
        for _index, _specification in enumerate(self._lst_specification):
            self.cmbSpecification.insert_text(_index, _specification)

        # Create and place all the labels for the inputs.
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Place all the input widgets.
        if self.cmbQuality.get_parent() is not None:
            self.cmbQuality.reparent(_fixed)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.put(self.cmbQuality, _x_pos, _y_pos[0])
        _fixed.put(self.txtCommercialPiQ, _x_pos, _y_pos[1])
        _fixed.put(self.cmbSpecification, _x_pos, _y_pos[2])
        _fixed.put(self.cmbInsulation, _x_pos, _y_pos[3])

<<<<<<< HEAD
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
            self.cmbSpecification.connect('changed',
                                          self._on_combo_changed, _index))
        _index += 1
        self._lst_handler_id.append(
            self.cmbInsulation.connect('changed',
                                       self._on_combo_changed, _index))
        _index += 1

        if self._subcategory == 62:         # Transformer
            # Populate the gtk.ComboBox().
            for i in range(len(self._family)):
                self.cmbFamily.insert_text(i, self._family[i])
=======
        if self._subcategory == 62:         # Transformer
            # Populate the gtk.ComboBox().
            for _index, _family in enumerate(self._lst_family):
                self.cmbFamily.insert_text(_index, _family)

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            try:
                _insulation = self._lst_insulation[self._hardware_model.specification - 1]
            except IndexError:
                _insulation = []
<<<<<<< HEAD
            for _index, _insul in enumerate(_insulation):
                self.cmbInsulation.insert_text(_index, _insul)
=======
            for _index, _insulation in enumerate(_insulation):
                self.cmbInsulation.insert_text(_index, _insulation)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Place all the input widgets.
            _fixed.put(self.cmbFamily, _x_pos, _y_pos[4])
            _fixed.put(self.txtPowerLoss, _x_pos, _y_pos[5])
            _fixed.put(self.txtSurfaceArea, _x_pos, _y_pos[6])
            _fixed.put(self.txtWeight, _x_pos, _y_pos[7])
            _fixed.put(self.txtInputPower, _x_pos, _y_pos[8])

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbFamily.connect('changed',
                                       self._on_combo_changed, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtPowerLoss.connect('focus-out-event',
                                          self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtSurfaceArea.connect('focus-out-event',
                                            self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtWeight.connect('focus-out-event',
                                       self._on_focus_out, _index))
            _index += 1
            self._lst_handler_id.append(
                self.txtInputPower.connect('focus-out-event',
                                           self._on_focus_out, _index))

        elif self._subcategory == 63:       # Coil
            # Populate the gtk.ComboBox().
            for i in range(len(self._lst_construction)):
                self.cmbConstruction.insert_text(i,
                                                 self._lst_construction[i])
=======
        elif self._subcategory == 63:       # Coil
            # Populate the gtk.ComboBox().
            for _index, _construction in enumerate(self._lst_construction):
                self.cmbConstruction.insert_text(_index, _construction)

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            try:
                _insulation = self._lst_insulation[self._hardware_model.specification - 1]
            except IndexError:
                _insulation = []
<<<<<<< HEAD
            for _index, _insul in enumerate(_insulation):
                self.cmbInsulation.insert_text(_index, _insul)
=======
            for _index, _insulation in enumerate(_insulation):
                self.cmbInsulation.insert_text(_index, _insulation)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

            # Place all the input widgets.
            _fixed.put(self.cmbConstruction, _x_pos, _y_pos[4])

<<<<<<< HEAD
            # Connect signals to callback functions.
            self._lst_handler_id.append(
                self.cmbConstruction.connect('changed',
                                             self._on_combo_changed, _index))

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.show_all()

        return _x_pos

<<<<<<< HEAD
    def load_217_stress_inputs(self, model):
        """
        Loads the Connection class gtk.Widgets().

        :param model: the Hardware data model to load the attributes from.
=======
    def load_217_count_inputs(self, model):
        """
        Method to load the Inductor class MIL-HDBK-217FN2 parts count input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.inductor.Inductor.Model` to
                      load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbQuality.set_active(int(model.quality))

        return False

    def load_217_stress_inputs(self, model):
        """
        Method to load the Inductor class MIL-HDBK-217FN2 part stress input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.inductor.Inductor.Model` to
                      load the attributes from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

<<<<<<< HEAD
        fmt = '{0:0.' + str(_conf.PLACES) + 'G}'
=======
        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.cmbQuality.set_active(int(model.quality))
        self.txtCommercialPiQ.set_text(str(fmt.format(model.q_override)))
        self.cmbSpecification.set_active(model.specification)
        self.cmbInsulation.set_active(model.insulation_class)

        # Load subcategory specific widgets.
        if self._subcategory == 62:         # Transformer
            self.cmbFamily.set_active(model.family)
            self.txtPowerLoss.set_text(str(fmt.format(model.power_loss)))
            self.txtSurfaceArea.set_text(str(fmt.format(model.case_area)))
<<<<<<< HEAD
            self.txtWeight.set_text(
                str(fmt.format(model.weight)))
=======
            self.txtWeight.set_text(str(fmt.format(model.weight)))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            self.txtInputPower.set_text(str(fmt.format(model.input_power)))

        elif self._subcategory == 63:       # Coil
            self._load_insulation(model.specification)

            self.cmbConstruction.set_active(model.construction)
            self.cmbInsulation.set_active(model.insulation_class)

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
            self._hardware_model.specification = combo.get_active()
            self._load_insulation(self._hardware_model.specification)
        elif index == 3:
            self._hardware_model.insulation_class = combo.get_active()
<<<<<<< HEAD
        elif index == 4 and self._subcategory == 62:
            self._hardware_model.family = combo.get_active()
        elif index == 4 and self._subcategory == 63:
=======
        elif index == 4:
            self._hardware_model.family = combo.get_active()
        elif index == 9:
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            self._hardware_model.construction = combo.get_active()

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
        elif index == 5:
            self._hardware_model.power_loss = float(entry.get_text())
        elif index == 6:
            self._hardware_model.case_area = float(entry.get_text())
        elif index == 7:
            self._hardware_model.weight = float(entry.get_text())
        elif index == 8:
            self._hardware_model.input_power = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _load_insulation(self, specification):
        """
<<<<<<< HEAD
        Method to load the insulation class gtk.ComboBox() whenever a new
=======
        Method to load the Inductor class gtk.ComboBox() whenever a new
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        specification is selected.

        :param int specification: the selected specification index.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbInsulation.handler_block(self._lst_handler_id[3])

        # Remove existing entries.
        _model = self.cmbInsulation.get_model()
        _model.clear()

        # Load the new entries.
        _n_classes = len(self._lst_insulation[specification - 1])
        for i in range(_n_classes):
            self.cmbInsulation.insert_text(
                i, self._lst_insulation[specification - 1][i])

        self.cmbInsulation.handler_unblock(self._lst_handler_id[3])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for an
    inductive device.  The output attributes of an inductive device Work Book
    view are:
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Initializes an instance of the inductive device assessment results
        view.

        :param model: the instance of the Inductor data model to create the
                      view for.
=======
        Method to initialize an instance of the Inductive device assessment
        results view.

        :param model: the :py:class:`rtk.hardware.inductor.Inductor.Model` to
                      create the view for.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

<<<<<<< HEAD
        # Initialize private list attributes.
        self._lst_labels = ['', u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = \u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>",
                                  u"\u03BB<sub>g</sub>:",
                                  u"\u03C0<sub>Q</sub>:"]
        self._lst_stress_labels = ['', u"\u03BB<sub>b</sub>:",
                                   u"\u03C0<sub>Q</sub>:",
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
        self.txtPiC = Widgets.make_entry(width=100, editable=False, bold=True)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        self.figDerate = Figure(figsize=(6, 4))
        self.axsDerateV = self.figDerate.add_subplot(111)
        self.axsDerateI = self.axsDerateV.twinx()
        self.pltDerate = FigureCanvas(self.figDerate)

        # Subcategory specific attributes.
        if self._subcategory == 62:         # Transformer
<<<<<<< HEAD
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

        elif self._subcategory == 63:       # Coil
            self._lst_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>C</sub></span>"
            self._lst_labels.append(u"\u03C0<sub>C</sub>:")

            self.txtPiC = _widg.make_entry(width=100,
                                           editable=False, bold=True)

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Inductors.
=======
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>"

        elif self._subcategory == 63:       # Coil
            self._lst_stress_labels[0] = u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub>\u03C0<sub>C</sub></span>"
            self._lst_stress_labels.append(u"\u03C0<sub>C</sub>:")

        # Create the tooltips for all the results display widgets.
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected inductive device."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected inductive device."))
        self.txtPiC.set_tooltip_text(_(u"Displays the construction factor for "
                                       u"the selected inductive device."))

    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count result gtk.Widgets()
        for Inductors.

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

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the generic hazard rate "
                                           u"for the selected inductive "
                                           u"device."))

        # Place the reliability result display widgets.
        if self.txt.LambdaB.get_parent() is not None:
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
        for Inductors.
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

        # Create and place all the labels for the inputs.
<<<<<<< HEAD
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 25)
=======
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 25)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _x_pos = max(x_pos, _x_pos) + 30

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected inductive "
                                           u"device."))
<<<<<<< HEAD
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for the "
                                       u"selected inductive device."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected inductive device."))

        # Place the reliability result display widgets.
=======

        # Place the reliability result display widgets.
        if self.txt.LambdaB.get_parent() is not None:
            self.txtLambdaB.reparent(_fixed)
        if self.txtPiQ.get_parent() is not None:
            self.txtPiQ.reparent(_fixed)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[3])

        # Subcategory specific widgets.
        if self._subcategory == 63:         # Coil
<<<<<<< HEAD
            self.txtPiC.set_tooltip_text(_(u"Displays the construction factor "
                                           u"for the selected inductive "
                                           u"device."))

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _fixed.put(self.txtPiC, _x_pos, _y_pos[4])

        _fixed.show_all()

        return _x_pos

<<<<<<< HEAD
    def load_217_stress_results(self, model):
        """
        Loads the Inductor class result gtk.Widgets().

        :param model: the Inductor data model to load the attributes from.
=======
    def load_217_count_results(self, model):
        """
        Method to load the Inductor class MIL-HDBK-217FN2 parts count result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.inductor.Inductor.Model` to
                      load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        return False

    def load_217_stress_results(self, model):
        """
        Method to load the Inductor class MIL-HDBK-217FN2 part stress result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.inductor.Inductor.Model` to
                      load the attributes from.
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
        self.txtPiQ.set_text(str(fmt.format(model.piQ)))
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        if self._subcategory == 63:         # Coil
            self.txtPiC.set_text(str(fmt.format(model.piC)))

<<<<<<< HEAD
        elif self._subcategory == 74:       # IC Socket
            self.txtPiP.set_text(str(fmt.format(model.piP)))

        elif self._subcategory == 75:       # PTH
            self.txtPiC.set_text(str(fmt.format(model.piC)))
            self.txtPiQ.set_text(str(fmt.format(model.piQ)))

        elif self._subcategory == 76:       # Non-PTH
            self.txtPiQ.set_text(str(fmt.format(model.piQ)))

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        return False

    def load_derate_plot(self, model, frame):
        """
<<<<<<< HEAD
        Loads the stress derate plot for the Inductor class.

        :param model: the Hardware data model to load the attributes from.
=======
        Method to load the stress derate plot for the Inductor class.

        :param model: the :py:class:`rtk.hardware.inductor.Inductor.Model` to
                      load the attributes from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
=======
        _lines = _line0 + _line1 + _line2 + _line3

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
<<<<<<< HEAD
        _lines = _line0 + _line1 + _line2 + _line3
        _leg = self.axsDerateV.legend(_lines, _legend, 'upper right',
=======
        _leg = self.axsDerateV.legend(_lines, _legend, loc='upper right',
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
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
