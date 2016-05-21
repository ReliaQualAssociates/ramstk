#!/usr/bin/env python
"""
#############################################
Fuse Module Component Specific Work Book View
#############################################
"""

# -*- coding: utf-8 -*-
#
<<<<<<< HEAD
#       hardware.gui.gtk.Fuse.py is part of The RTK Project
=======
#       rtk.hardware.gui.gtk.Fuse.py is part of The RTK Project
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
    The Work Book view for displaying all the attributes for a fuse.  The
    attributes of a fuse Work Book view are:
<<<<<<< HEAD
=======

    :ivar :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model` _hardware_model:
    :ivar int _subcategory: the Component subcategory.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Creates an input frame for the Fuse data model.

        :param :class `rtk.hardware.Fuse.model`: the Fuse data model whose
                                                 attributes will be displayed.
=======
        Method to create an input frame for the Fuse data model.

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model`
                      whose attributes will be displayed.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        gtk.Frame.__init__(self)

        self.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

<<<<<<< HEAD
        # ===== ===== === Initialize private list attributes === ===== ===== #
        self._lst_labels = []
        self._lst_handler_id = []

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

    def create_217_count_inputs(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part count input widgets for Fuses.
=======
        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.

    def create_217_count_inputs(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count input gtk.Widgets()
        for Fuses.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

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
<<<<<<< HEAD
        Creates the MIL-HDBK-217FN2 part stress input widgets for Integrated
        Circuits.
=======
        Method to create the MIL-HDBK-217FN2 part stress input gtk.Widgets()
        for Fuses.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :keyword int x_pos: the x position of the display widgets.
        :return: False if successful or True if an error is encountered.
        """

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>""</span>")
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

<<<<<<< HEAD
    def load_217_stress_inputs(self, __model):
        """
        Loads the Fuse class MIL-HDBK-217FN2 part stress gtk.Widgets().

        :param __model: the Hardware data model to load the attributes from.
=======
    def load_217_count_inputs(self, __model):
        """
        Method to loads the Fuse class MIL-HDBK-217FN2 part stress inputs
        gtk.Widgets().

        :param __model: the :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model`
                        to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return False

    def load_217_stress_inputs(self, __model):
        """
        Method to loads the Fuse class MIL-HDBK-217FN2 part stress inputs
        gtk.Widgets().

        :param __model: the :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model`
                        to load the attributes from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return False


class Results(gtk.Frame):
    """
    The Work Book view for displaying all the output attributes for a
    Fuse.  The output attributes of a Fuse Work Book view are:
<<<<<<< HEAD
=======

    :ivar list _lst_count_labels: the MIL-HDBK-217FN2 parts count labels.
    :ivar list _lst_stress_labels: the MIL-HDBK-217FN2 part stress labels.
    :ivar :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model` _hardware_model:
    :ivar int _subcategory: the Component subcategory.
    :ivar gtk.Entry txtLambdaB: the gtk.Entry() that displays the
                                MIL-HDBK-217FN2 base/generic hazard rate.
    :ivar gtk.Entry txtPiE: the gtk.Entry() that displays the MIL-HDBK-217FN2
                            operating environment factor.
    :ivar gtk.Entry txtPiQ: the gtk.Entry() that displays the MIL-HDBK-217FN2
                            quality factor.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self, model):
        """
<<<<<<< HEAD
        Initializes an instance of the Fuse assessment results view.

        :param model: the instance of the Fuse data model to create the view
                      for.
=======
        Method to initialize an instance of the Fuse assessment results view.

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model`
                      to create the view for.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        gtk.Frame.__init__(self)

<<<<<<< HEAD
        # Initialize private list attributes.
        self._lst_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub></span>",
                            u"\u03BB<sub>b</sub>:", u"\u03C0<sub>E</sub>:"]

        # ===== ===== == Initialize private scalar attributes == ===== ===== #
        self._hardware_model = model
        self._subcategory = model.subcategory

        # Create the result widgets.
        self.txtLambdaB = _widg.make_entry(width=100, editable=False,
                                           bold=True)
        self.txtPiE = _widg.make_entry(width=100, editable=False, bold=True)

    def create_217_stress_results(self, x_pos=5):
        """
        Creates the MIL-HDBK-217FN2 part stress result widgets for Fuses.
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_count_labels = [u"<span foreground=\"blue\">\u03BB<sub>EQUIP</sub> = \u03BB<sub>g</sub></span>",
                                  u"\u03BB<sub>g</sub>:"]
        self._lst_stress_labels = [u"<span foreground=\"blue\">\u03BB<sub>p</sub> = \u03BB<sub>b</sub>\u03C0<sub>E</sub></span>",
                                   u"\u03BB<sub>b</sub>:",
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

        # Create the tooltips for all the results display widgets.
        self.txtLambdaB.set_tooltip_text(_(u"Displays the base hazard rate "
                                           u"for the selected fuse."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected fuse."))

    def create_217_count_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 parts count results gtk.Widgets()
        for Fuses.

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
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 25)
        _x_pos = max(x_pos, _x_pos) + 30

        # Place the reliability result display widgets.
        if self.txt.LambdaB.get_parent() is not None:
            self.txtLambdaB.reparent(_fixed)
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])

        _fixed.show_all()

        return _x_pos

    def create_217_stress_results(self, x_pos=5):
        """
        Method to create the MIL-HDBK-217FN2 part stress results gtk.Widgets()
        for Fuses.
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
                                           u"for the selected filter."))
        self.txtPiE.set_tooltip_text(_(u"Displays the environment factor for "
                                       u"the selected filter."))

        # Place the reliability result display widgets.
=======
        (_x_pos,
         _y_pos) = Widgets.make_labels(self._lst_stress_labels, _fixed, 5, 25)
        _x_pos = max(x_pos, _x_pos) + 30

        # Place the reliability result display widgets.
        if self.txt.LambdaB.get_parent() is not None:
            self.txtLambdaB.reparent(_fixed)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _fixed.put(self.txtLambdaB, _x_pos, _y_pos[1])
        _fixed.put(self.txtPiE, _x_pos, _y_pos[2])

        _fixed.show_all()

        return _x_pos

<<<<<<< HEAD
    def load_217_stress_results(self, model):
        """
        Loads the Fuse class result gtk.Widgets().

        :param model: the Fuse data model to load the attributes from.
=======
    def load_217_count_results(self, model):
        """
        Method to load the Fuse class MIL-HDBK-217FN2 parts count results
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model`
                      to load the attributes from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(Configuration.PLACES) + 'G}'

        self.txtLambdaB.set_text(str(fmt.format(model.base_hr)))

        return False

    def load_217_stress_results(self, model):
        """
        Method to load the Fuse class MIL-HDBK-217FN2 part stress results
        gtk.Widgets().

        :param model: the :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model`
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
        self.txtPiE.set_text(str(fmt.format(model.piE)))

        return False

    def load_derate_plot(self, __model, frame):
        """
<<<<<<< HEAD
        Loads the stress derate plot for the Fuse class.

        :param __model: the Hardware data model to load the attributes from.
=======
        Method to load the stress derate plot for the Fuse class.

        :param __model: the :py:class:`rtk.hardware.component.miscellaneous.Fuse.Model`
                        to load the attributes from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :param gtk.Frame frame: the gtk.Frame() to embed the derate plot into.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        frame.hide()

        return False
