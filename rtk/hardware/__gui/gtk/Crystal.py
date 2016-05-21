#!/usr/bin/env python
"""
################################################
Crystal Module Component Specific Work Book View
################################################
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       hardware.gui.gtk.Crystal.py is part of The RTK Project
=======
#       rtk.hardware.gui.gtk.Crystal.py is part of The RTK Project
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


class Inputs(gtk.Frame):
    """
    The Work Book view for displaying all the attributes for an integrated
<<<<<<< HEAD
    circuit.  The attributes of an inntegrated circuit Work Book view are:
=======
    circuit.  The attributes of a Crystal Work Book view are:

    :ivar list _lst_count_labels: labels for the MIL-HDBK-217FN2 parts count
                                  method.
    :ivar list _lst_stress_labels: labels for the MIL-HDBK-217FN2 part stress
                                   method.
    :ivar list _lst_handler_id: list of gtk.Widget() callback signals.
    :ivar :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model` _hardware_model:
    :ivar int _subcategory: the Component subcategory.
    :ivar gtk.ComboBox cmbQuality: the gtk.ComboBox() to display and select
                                   the Crystal quality level.
    :ivar gtk.Entry txtCommercialPiQ: the gtk.Entry() to display and enter any
                                      user-defined quality factor.
    :ivar gtk.Entry txtFrequency: the gtk.Entry() to display and enter the
                                  Crystal operating frequency.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Creates an input frame for the meter data model.

        :param :class `rtk.hardware.Crystal.model`: the Crystal data model
                                                    whose attributes will be
                                                    displayed.
=======
        Method to initialize an input frame for the Crystal data model.

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model`
                      whose attributes will be displayed.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

<<<<<<< HEAD
        # ===== ===== === Initialize private list attributes === ===== ===== #
        self._lst_labels = [_(u"Quality:"), _(u"\u03C0<sub>Q</sub> Override:"),
                            _(u"Frequency:")]

        self._lst_handler_id = []

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # = Create the input widgets common to all Crystal types = #
        self.cmbQuality = _widg.make_combo(simple=True)
        self.txtCommercialPiQ = _widg.make_entry(width=100)
        self.txtFrequency = _widg.make_entry(width=100)

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for Crystals.
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [_(u"Quality:")]
        self._lst_stress_labels = [_(u"Quality:"),
                                   _(u"\u03C0<sub>Q</sub> Override:"),
                                   _(u"Frequency:")]

        self._lst_handler_id = []

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.cmbQuality = Widgets.make_combo(simple=True)
        self.txtCommercialPiQ = Widgets.make_entry(width=100)
        self.txtFrequency = Widgets.make_entry(width=100)

        # Create the tooltips for all the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality"
                                           u"level for the selected crystal."))
        self.txtCommercialPiQ.set_tooltip_text(_(u"User-defined quality "
                                                 u"factor for the selected "
                                                 u"crystal."))
        self.txtFrequency.set_tooltip_text(_(u"Select and display the "
                                             u"operating frequency for the "
                                             u"selected crystal."))

        # Load the quality gtk.ComboBox().
        _lst_quality = ['', u"MIL-SPEC", _(u"Lower")]
        for _index, _quality in enumerate(_lst_quality):
            self.cmbQuality.insert_text(_index, _quality)

        # Connect signals to callback functions.
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.txtCommercialPiQ.connect('focus-out-event',
                                          self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtFrequency.connect('focus-out-event',
                                      self._on_focus_out, 2))

    def create_217_count_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count input gtk.Widgets()
        for Crystals.
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

<<<<<<< HEAD
=======
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

        return x_pos

    def create_217_stress_inputs(self, x_pos=5):
        """
<<<<<<< HEAD
        Creates the MIL-HDBK-217FN2 part stress input widgets for Integrated
        Circuits.
=======
        Method to create the MIL-HDBK-217FN2 part stress input gtk.Widgets()
        for Crystals.
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

<<<<<<< HEAD
        # Load the gtk.ComboBox().
        _lst_quality = ['', u"MIL-SPEC", _(u"Lower")]
        for _index, _quality in enumerate(_lst_quality):
            self.cmbQuality.insert_text(_index, _quality)

        # Create and place all the labels for the inputs.
        (_x_pos, _y_pos) = _widg.make_labels(self._lst_labels, _fixed, 5, 5)
        _x_pos = max(x_pos, _x_pos) + 50

        # Create the tooltips for all the input widgets.
        self.cmbQuality.set_tooltip_text(_(u"Select and display the quality"
                                           u"level for the selected crystal."))
        self.txtCommercialPiQ.set_tooltip_text(_(u"User-defined quality "
                                                 u"factor for the selected "
                                                 u"crystal."))
        self.txtFrequency.set_tooltip_text(_(u"Select and display the "
                                             u"operating frequency for the "
                                             u"selected crystal."))

        # Place all the input widgets.
=======
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
        _fixed.put(self.txtFrequency, _x_pos, _y_pos[2])

<<<<<<< HEAD
        # Connect signals to callback functions.
        _index = 0
        self._lst_handler_id.append(
            self.cmbQuality.connect('changed',
                                    self._on_combo_changed, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtCommercialPiQ.connect('focus-out-event',
                                          self._on_focus_out, _index))
        _index += 1
        self._lst_handler_id.append(
            self.txtFrequency.connect('focus-out-event',
                                      self._on_focus_out, _index))

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
        Method to load the Crystal class MIL-HDBK-217FN2 parts count input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbQuality.set_active(model.quality)

        return False

    def load_217_stress_inputs(self, model):
        """
        Method to load the Crystal class MIL-HDBK-217FN2 part stress input
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model`
                      to load the attributes from.
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
        self.txtCommercialPiQ.set_text(str(fmt.format(model.q_override)))
        self.txtFrequency.set_text(str(fmt.format(model.frequency)))

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

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
<<<<<<< HEAD
        Responds to gtk.Entry() focus_out signals and calls the correct
        function or method, passing any parameters as needed.
=======
        Method to respond to gtk.Entry() 'focus_out' signals and call the
        correct Method to function or method, passing any parameters as needed.
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
        elif index == 2:
            self._hardware_model.frequency = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    Crystal.  The output attributes of a Crystal Work Book view are:
<<<<<<< HEAD
=======

    :ivar list _lst_count_labels: labels for the MIL-HDBK-217FN2 parts count
                                  method.
    :ivar list _lst_stress_labels: labels for the MIL-HDBK-217FN2 part stress
                                   method.
    :ivar :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model` _hardware_model:
    :ivar int _subcategory: the Component subcategory.
    :ivar gtk.Entry txtLambdaB: the gtk.Entry() to display the base/generic
                                hazard rate.
    :ivar gtk.Entry txtPiQ: the gtk.Entry() to display the quality factor.
    :ivar gtk.Entry txtPiE: the gtk.Entry() to display the operating
                            environment factor.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Initializes an instance of the Crystal assessment results view.

        :param model: the instance of the Crystal data model to create the view
                      for.
=======
        Method to initialize an instance of the Crystal assessment results
        view.

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model`
                      to create the view for.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

<<<<<<< HEAD
        # Initialize private list attributes.
        self._lst_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>Q</sub>:",
                            u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiQ = _widg.make_entry(width=100, editable=False, bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Crystals.
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = \u03BB<sub>g</sub>\u03C0<sub>Q</sub></span>",
                                  u"\u03BB<sub>g</sub>:",
                                  u"\u03C0<sub>Q</sub>:"]
        self._lst_stress_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>Q</sub>\u03C0<sub>E</sub></span>",
                                   u"\u03BB<sub>b</sub>:",
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

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected crystal."))
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for "
                                       u"the selected crystal."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected crystal."))

    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count result gtk.Widgets()
        for Crystals.

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
        for Crystals.
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
        _x_pos = max(x_pos, _x_pos) + 30

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected crystal."))
        self.txtPiQ.set_tooltip_text(_(u"Displays the quality factor for "
                                       u"the selected crystal."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected crystal."))

=======
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 25)
        _x_pos = max(x_pos, _x_pos) + 30

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        # Place the reliability result display widgets.
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiQ, _x_pos, _y_pos[2])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[3])

        _fixed.show_all()

        return _x_pos

<<<<<<< HEAD
    def load_217_stress_results(self, model):
        """
        Loads the Crystal class result gtk.Widgets().

        :param model: the Crystal data model to load the attributes from.
=======
    def load_217_count_results(self, model):
        """
        Method to load the Crystal class MIL-HDBK-217FN2 parts count result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model`
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
        Method to load the Crystal class MIL-HDBK-217FN2 part stress result
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model`
                      to load the attributes from.
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

        return False

    def load_derate_plot(self, __model, frame):
        """
<<<<<<< HEAD
        Loads the stress derate plot for the Crystal class.

        :param __model: the Hardware data model to load the attributes from.
=======
        Method to load the stress derate plot for the Crystal class.

        :param __model: the :py:class:`rtk.hardware.component.miscellaneous.Crystal.Model`
                        to load the derating plot from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :param gtk.Frame frame: the gtk.Frame() to embed the derate plot into.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        frame.hide()

        return False
