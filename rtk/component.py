#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
the hardware of the Program.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       component.py is part of The RTK Project
#
# All rights reserved.
import gettext
import locale
import sys

import pandas as pd
from datetime import datetime
from lxml import etree
from math import exp, log

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
try:
    import gobject
except ImportError:
    sys.exit(1)
try:
    import pango
except ImportError:
    sys.exit(1)

# Modules required for plotting.
import matplotlib
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure
matplotlib.use('GTK')

# Import other RTK modules.
import calculations as _calc
import configuration as _conf
import utilities as _util
import widgets as _widg
from hardware import Hardware

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Component(Hardware):


    def __init__(self, application):

        Hardware.__init__(self, application)

        # Define private Hardware class scalar attributes.
        self._app = application
        self._component = None

        # Define public Hardware class scalar attributes.
        self.burnin_temp = 0.0
        self.burnin_time = 0.0
        self.lab_devices = 0.0
        self.lab_time = 0.0
        self.lab_temp = 0.0
        self.lab_failures = 0.0
        self.field_time = 0.0
        self.field_failures = 0.0
        self.min_temp = 0.0
        self.knee_temp = 0.0
        self.max_temp = 0.0
        self.rated_current = 0.0
        self.rated_power = 0.0
        self.rated_voltage = 0.0
        self.op_current = 0.0
        self.op_power = 0.0
        self.op_voltage = 0.0
        self.current_ratio = 1.0
        self.voltage_ratio = 1.0
        self.power_ratio = 1.0
        self.theta_jc = 0.0
        self.temp_rise = 0.0
        self.case_temp = 0.0

        # Assessment Input page widgets.
        self.cmbCalcModel = _widg.make_combo()

        self.fxdReliabilityInputs = gtk.Fixed()
        self.fxdStressInputs = gtk.Fixed()

        self.scwReliabilityInputs = gtk.ScrolledWindow()
        self.scwStressInputs = gtk.ScrolledWindow()

        # Assessment Results page widgets.
        self.chkOverstressed = _widg.make_check_button()

        self.figDerate = Figure(figsize=(6, 4))

        self.fraDerate = gtk.Frame()

        self.fxdStressResults = gtk.Fixed()
        self.fxdMiscResults = gtk.Fixed()

        self.pltDerate = FigureCanvas(self.figDerate)

        self.scwStressResults = gtk.ScrolledWindow()
        self.scwMiscResults = gtk.ScrolledWindow()

        self.txtAssemblyCrit = _widg.make_entry(editable=False, bold=True)
        self.txtPartCount = _widg.make_entry(width=100, editable=False,
                                             bold=True)
        self.txtTotalPwr = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        self.txtVoltageRatio = _widg.make_entry(width=100, editable=False,
                                                bold=True)
        self.txtCurrentRatio = _widg.make_entry(width=100, editable=False,
                                                bold=True)
        self.txtPwrRatio = _widg.make_entry(width=100, editable=False,
                                            bold=True)
        self.txtOSReason = gtk.TextBuffer()




    def _create_assessment_inputs_tab(self, notebook):
            _labels = [_(u"Burn-In Temp:"), _(u"Burn-In Time:"),
                       _(u"# of Lab Devices:"), _(u"Lab Test Time:"),
                       _(u"Lab Test Temp:"), _(u"# of Lab Failures:"),
                       _(u"Field Op Time:"), _(u"# of Field Failures:")]
            (_x_pos_r,
             _y_pos_r) = _widg.make_labels(_labels,
                                           self.fxdRelInputQuad1, 5, 5)
            _x_pos_r += 50
            self._component_x[0] = _x_pos_r
            self._component_y[0] = _y_pos_r[7] + 50

            self.txtBurnInTemp.set_tooltip_text(_(u"Enter the temperature "
                                                  u"that the selected "
                                                  u"component will be "
                                                  u"burned-in."))
            self.txtBurnInTime.set_tooltip_text(_(u"Enter the total time the "
                                                  u"selected component will "
                                                  u"be burned-in."))
            self.txtLabDevices.set_tooltip_text(_(u"The total number of units "
                                                  u"that will be included in "
                                                  u"life testing in the "
                                                  u"laboratory."))
            self.txtLabTime.set_tooltip_text(_(u"The total time the units "
                                               u"will undergo life testing in "
                                               u"the laboratory."))
            self.txtLabTemp.set_tooltip_text(_(u"The temperature the selected "
                                               u"component will be exposed to "
                                               u"during life testing in the "
                                               u"laboratory."))
            self.txtLabFailures.set_tooltip_text(_(u"The total number of "
                                                   u"failure observed during "
                                                   u"life testing in the "
                                                   u"laboratory."))
            self.txtFieldTime.set_tooltip_text(_(u"The total time that the "
                                                 u"selected component has "
                                                 u"been fielded."))
            self.txtFieldFailures.set_tooltip_text(_(u"The total number of "
                                                     u"failures of the "
                                                     u"selected component "
                                                     u"that have been "
                                                     u"observed in the "
                                                     u"field."))

            self.fxdRelInputQuad1.put(self.txtBurnInTemp, _x_pos_r,
                                      _y_pos_r[0])
            self.fxdRelInputQuad1.put(self.txtBurnInTime, _x_pos_r,
                                      _y_pos_r[1])
            self.fxdRelInputQuad1.put(self.txtLabDevices, _x_pos_r,
                                      _y_pos_r[2])
            self.fxdRelInputQuad1.put(self.txtLabTime, _x_pos_r, _y_pos_r[3])
            self.fxdRelInputQuad1.put(self.txtLabTemp, _x_pos_r, _y_pos_r[4])
            self.fxdRelInputQuad1.put(self.txtLabFailures, _x_pos_r,
                                      _y_pos_r[5])
            self.fxdRelInputQuad1.put(self.txtFieldTime, _x_pos_r, _y_pos_r[6])
            self.fxdRelInputQuad1.put(self.txtFieldFailures, _x_pos_r,
                                      _y_pos_r[7])

            self._lst_handler_id.append(
                self.txtBurnInTemp.connect('focus-out-event',
                                           self._callback_entry, 'float', 206))
            self._lst_handler_id.append(
                self.txtBurnInTime.connect('focus-out-event',
                                           self._callback_entry, 'float', 207))
            self._lst_handler_id.append(
                self.txtLabDevices.connect('focus-out-event',
                                           self._callback_entry, "int", 220))
            self._lst_handler_id.append(
                self.txtLabTime.connect('focus-out-event',
                                        self._callback_entry, 'float', 308))
            self._lst_handler_id.append(
                self.txtLabTemp.connect('focus-out-event',
                                        self._callback_entry, 'float', 306))
            self._lst_handler_id.append(
                self.txtLabFailures.connect('focus-out-event',
                                            self._callback_entry, "int", 227))
            self._lst_handler_id.append(
                self.txtFieldTime.connect('focus-out-event',
                                          self._callback_entry, 'float', 265))
            self._lst_handler_id.append(
                self.txtFieldFailures.connect('focus-out-event',
                                              self._callback_entry,
                                              'int', 226))
