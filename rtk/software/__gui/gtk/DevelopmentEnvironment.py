#!/usr/bin/env python
"""
##############################################################################
Software Package Risk Analysis Development Environment Specific Work Book View
##############################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.__gui.gtk.DevelopmentEnvironment.py is part of The RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
#    may be used to endorse or promote products derived from this software 
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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


class RiskAnalysis(gtk.VPaned):
    """
    The Work Book view for analyzing and displaying the risk associated with
    the development environment.  The attributes of a development environment
    Work Book view are:

    :ivar list _lst_handler_id: the list of gtk.Widget() signal handler IDs.
    :ivar _software_model: the :py:class:`rtk.software.Software.Model` to
                           display.
    """

    def __init__(self):
        """
        Method to initialize the development environment risk analysis
        questions Work Book page.
        """

        gtk.VPaned.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._software_model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.chkDevEnvQ1 = Widgets.make_check_button()
        self.chkDevEnvQ2 = Widgets.make_check_button()
        self.chkDevEnvQ3 = Widgets.make_check_button()
        self.chkDevEnvQ4 = Widgets.make_check_button()
        self.chkDevEnvQ5 = Widgets.make_check_button()
        self.chkDevEnvQ6 = Widgets.make_check_button()
        self.chkDevEnvQ7 = Widgets.make_check_button()
        self.chkDevEnvQ8 = Widgets.make_check_button()
        self.chkDevEnvQ9 = Widgets.make_check_button()
        self.chkDevEnvQ10 = Widgets.make_check_button()
        self.chkDevEnvQ11 = Widgets.make_check_button()
        self.chkDevEnvQ12 = Widgets.make_check_button()
        self.chkDevEnvQ13 = Widgets.make_check_button()
        self.chkDevEnvQ14 = Widgets.make_check_button()
        self.chkDevEnvQ15 = Widgets.make_check_button()
        self.chkDevEnvQ16 = Widgets.make_check_button()
        self.chkDevEnvQ17 = Widgets.make_check_button()
        self.chkDevEnvQ18 = Widgets.make_check_button()
        self.chkDevEnvQ19 = Widgets.make_check_button()
        self.chkDevEnvQ20 = Widgets.make_check_button()
        self.chkDevEnvQ21 = Widgets.make_check_button()
        self.chkDevEnvQ22 = Widgets.make_check_button()
        self.chkDevEnvQ23 = Widgets.make_check_button()
        self.chkDevEnvQ24 = Widgets.make_check_button()
        self.chkDevEnvQ25 = Widgets.make_check_button()
        self.chkDevEnvQ26 = Widgets.make_check_button()
        self.chkDevEnvQ27 = Widgets.make_check_button()
        self.chkDevEnvQ28 = Widgets.make_check_button()
        self.chkDevEnvQ29 = Widgets.make_check_button()
        self.chkDevEnvQ30 = Widgets.make_check_button()
        self.chkDevEnvQ31 = Widgets.make_check_button()
        self.chkDevEnvQ32 = Widgets.make_check_button()
        self.chkDevEnvQ33 = Widgets.make_check_button()
        self.chkDevEnvQ34 = Widgets.make_check_button()
        self.chkDevEnvQ35 = Widgets.make_check_button()
        self.chkDevEnvQ36 = Widgets.make_check_button()
        self.chkDevEnvQ37 = Widgets.make_check_button()
        self.chkDevEnvQ38 = Widgets.make_check_button()
        self.chkDevEnvQ39 = Widgets.make_check_button()
        self.chkDevEnvQ40 = Widgets.make_check_button()
        self.chkDevEnvQ41 = Widgets.make_check_button()
        self.chkDevEnvQ42 = Widgets.make_check_button()
        self.chkDevEnvQ43 = Widgets.make_check_button()

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.chkDevEnvQ1.connect('toggled', self._on_toggled, 0))
        self._lst_handler_id.append(
            self.chkDevEnvQ2.connect('toggled', self._on_toggled, 1))
        self._lst_handler_id.append(
            self.chkDevEnvQ3.connect('toggled', self._on_toggled, 2))
        self._lst_handler_id.append(
            self.chkDevEnvQ4.connect('toggled', self._on_toggled, 3))
        self._lst_handler_id.append(
            self.chkDevEnvQ5.connect('toggled', self._on_toggled, 4))
        self._lst_handler_id.append(
            self.chkDevEnvQ6.connect('toggled', self._on_toggled, 5))
        self._lst_handler_id.append(
            self.chkDevEnvQ7.connect('toggled', self._on_toggled, 6))
        self._lst_handler_id.append(
            self.chkDevEnvQ8.connect('toggled', self._on_toggled, 7))
        self._lst_handler_id.append(
            self.chkDevEnvQ9.connect('toggled', self._on_toggled, 8))
        self._lst_handler_id.append(
            self.chkDevEnvQ10.connect('toggled', self._on_toggled, 9))
        self._lst_handler_id.append(
            self.chkDevEnvQ11.connect('toggled', self._on_toggled, 10))
        self._lst_handler_id.append(
            self.chkDevEnvQ12.connect('toggled', self._on_toggled, 11))
        self._lst_handler_id.append(
            self.chkDevEnvQ13.connect('toggled', self._on_toggled, 12))
        self._lst_handler_id.append(
            self.chkDevEnvQ14.connect('toggled', self._on_toggled, 13))
        self._lst_handler_id.append(
            self.chkDevEnvQ15.connect('toggled', self._on_toggled, 14))
        self._lst_handler_id.append(
            self.chkDevEnvQ16.connect('toggled', self._on_toggled, 15))
        self._lst_handler_id.append(
            self.chkDevEnvQ17.connect('toggled', self._on_toggled, 16))
        self._lst_handler_id.append(
            self.chkDevEnvQ18.connect('toggled', self._on_toggled, 17))
        self._lst_handler_id.append(
            self.chkDevEnvQ19.connect('toggled', self._on_toggled, 18))
        self._lst_handler_id.append(
            self.chkDevEnvQ20.connect('toggled', self._on_toggled, 19))
        self._lst_handler_id.append(
            self.chkDevEnvQ21.connect('toggled', self._on_toggled, 20))
        self._lst_handler_id.append(
            self.chkDevEnvQ22.connect('toggled', self._on_toggled, 21))
        self._lst_handler_id.append(
            self.chkDevEnvQ23.connect('toggled', self._on_toggled, 22))
        self._lst_handler_id.append(
            self.chkDevEnvQ24.connect('toggled', self._on_toggled, 23))
        self._lst_handler_id.append(
            self.chkDevEnvQ25.connect('toggled', self._on_toggled, 24))
        self._lst_handler_id.append(
            self.chkDevEnvQ26.connect('toggled', self._on_toggled, 25))
        self._lst_handler_id.append(
            self.chkDevEnvQ27.connect('toggled', self._on_toggled, 26))
        self._lst_handler_id.append(
            self.chkDevEnvQ28.connect('toggled', self._on_toggled, 27))
        self._lst_handler_id.append(
            self.chkDevEnvQ29.connect('toggled', self._on_toggled, 28))
        self._lst_handler_id.append(
            self.chkDevEnvQ30.connect('toggled', self._on_toggled, 29))
        self._lst_handler_id.append(
            self.chkDevEnvQ31.connect('toggled', self._on_toggled, 30))
        self._lst_handler_id.append(
            self.chkDevEnvQ32.connect('toggled', self._on_toggled, 31))
        self._lst_handler_id.append(
            self.chkDevEnvQ33.connect('toggled', self._on_toggled, 32))
        self._lst_handler_id.append(
            self.chkDevEnvQ34.connect('toggled', self._on_toggled, 33))
        self._lst_handler_id.append(
            self.chkDevEnvQ35.connect('toggled', self._on_toggled, 34))
        self._lst_handler_id.append(
            self.chkDevEnvQ36.connect('toggled', self._on_toggled, 35))
        self._lst_handler_id.append(
            self.chkDevEnvQ37.connect('toggled', self._on_toggled, 36))
        self._lst_handler_id.append(
            self.chkDevEnvQ38.connect('toggled', self._on_toggled, 37))
        self._lst_handler_id.append(
            self.chkDevEnvQ39.connect('toggled', self._on_toggled, 38))
        self._lst_handler_id.append(
            self.chkDevEnvQ40.connect('toggled', self._on_toggled, 39))
        self._lst_handler_id.append(
            self.chkDevEnvQ41.connect('toggled', self._on_toggled, 40))
        self._lst_handler_id.append(
            self.chkDevEnvQ42.connect('toggled', self._on_toggled, 41))
        self._lst_handler_id.append(
            self.chkDevEnvQ43.connect('toggled', self._on_toggled, 42))

    def create_risk_analysis_page(self, notebook):
        """
        Method to create the development environment risk analysis page and add
        it to the risk analysis gtk.Notebook().

        :param gtk.Notebook notebook: the gtk.Notebook() instance that will
                                      hold the development environment risk
                                      analysis questions.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HPaned()
        self.pack1(_hpaned, resize=True, shrink=True)

        # Create the organizational risk pane.
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Organization"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned.pack1(_frame, True, True)

        _labels = [_(u"1. There are separate design and coding "
                     u"organizations."),
                   _(u"2. There is an independent software test "
                     u"organization."),
                   _(u"3. There is an independent software quality "
                     u"assurance organization."),
                   _(u"4. There is an independent software configuration "
                     u"management organization."),
                   _(u"5. There is an independent software verification "
                     u"and validation organization."),
                   _(u"6. A structured programming team will develop the "
                     u"software."),
                   _(u"7. The educational level of the software team members "
                     u"is above average."),
                   _(u"8. The experience level of the software team members "
                     u"is above average.")]
        (_x_pos,
         _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5, wrap=False)
        _x_pos += 125

        _fixed.put(self.chkDevEnvQ1, _x_pos, _y_pos[0])
        _fixed.put(self.chkDevEnvQ2, _x_pos, _y_pos[1])
        _fixed.put(self.chkDevEnvQ3, _x_pos, _y_pos[2])
        _fixed.put(self.chkDevEnvQ4, _x_pos, _y_pos[3])
        _fixed.put(self.chkDevEnvQ5, _x_pos, _y_pos[4])
        _fixed.put(self.chkDevEnvQ6, _x_pos, _y_pos[5])
        _fixed.put(self.chkDevEnvQ7, _x_pos, _y_pos[6])
        _fixed.put(self.chkDevEnvQ8, _x_pos, _y_pos[7])

        # Create the methods risk pane.
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Methods"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned.pack2(_frame, True, True)

        _labels = [_(u"1. Standards are defined and will be enforced."),
                   _(u"2. Software will be developed using a higher order "
                     u"language."),
                   _(u"3. The development process will include formal "
                     u"reviews (PDR, CDR, etc.)."),
                   _(u"4. The development process will include frequent "
                     u"walkthroughs."),
                   _(u"5. Development will take a top-down and "
                     u"structured approach."),
                   _(u"6. Unit development folders will be used."),
                   _(u"7. A software development library will be used."),
                   _(u"8. A formal change and error reporting process "
                     u"will be used."),
                   _(u"9. Progress and status will routinely be "
                     u"reported.")]
        (__, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5, wrap=False)

        _fixed.put(self.chkDevEnvQ9, _x_pos, _y_pos[0])
        _fixed.put(self.chkDevEnvQ10, _x_pos, _y_pos[1])
        _fixed.put(self.chkDevEnvQ11, _x_pos, _y_pos[2])
        _fixed.put(self.chkDevEnvQ12, _x_pos, _y_pos[3])
        _fixed.put(self.chkDevEnvQ13, _x_pos, _y_pos[4])
        _fixed.put(self.chkDevEnvQ14, _x_pos, _y_pos[5])
        _fixed.put(self.chkDevEnvQ15, _x_pos, _y_pos[6])
        _fixed.put(self.chkDevEnvQ16, _x_pos, _y_pos[7])
        _fixed.put(self.chkDevEnvQ17, _x_pos, _y_pos[8])

        # Create the documentation risk pane.
        _hpaned = gtk.HPaned()
        self.pack2(_hpaned, resize=True, shrink=True)

        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Documentation"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned.pack1(_frame, True, True)

        _labels = [_(u" 1. System requirements specifications will be "
                     u"documented."),
                   _(u" 2. Software requirements specifications will be "
                     u"documented."),
                   _(u" 3. Interface design specifications will be "
                     u"documented."),
                   _(u" 4. Software design specification will be "
                     u"documented."),
                   _(u" 5. Test plans, procedures, and reports will be "
                     u"documented."),
                   _(u" 6. The software development plan will be "
                     u"documented."),
                   _(u" 7. The software quality assurance plan will be "
                     u"documented."),
                   _(u" 8. The software configuration management plan will "
                     u"be documented."),
                   _(u" 9. A requirements traceability matrix will be "
                     u"used."),
                   _(u"10. The software version description will be "
                     u"documented."),
                   _(u"11. All software discrepancies will be "
                     u"documented.")]
        (__, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5, wrap=False)

        _fixed.put(self.chkDevEnvQ18, _x_pos, _y_pos[0])
        _fixed.put(self.chkDevEnvQ19, _x_pos, _y_pos[1])
        _fixed.put(self.chkDevEnvQ20, _x_pos, _y_pos[2])
        _fixed.put(self.chkDevEnvQ21, _x_pos, _y_pos[3])
        _fixed.put(self.chkDevEnvQ22, _x_pos, _y_pos[4])
        _fixed.put(self.chkDevEnvQ23, _x_pos, _y_pos[5])
        _fixed.put(self.chkDevEnvQ24, _x_pos, _y_pos[6])
        _fixed.put(self.chkDevEnvQ25, _x_pos, _y_pos[7])
        _fixed.put(self.chkDevEnvQ26, _x_pos, _y_pos[8])
        _fixed.put(self.chkDevEnvQ27, _x_pos, _y_pos[9])
        _fixed.put(self.chkDevEnvQ28, _x_pos, _y_pos[10])

        # Create the tools and test techniques risk pane.
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        _frame = Widgets.make_frame(label=_(u"Tools &amp; Test Techniques"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hpaned.pack2(_frame, True, True)

        _labels = [_(u" 1. The software language requirements will be "
                     u"specified."),
                   _(u" 2. Formal program design language will be used."),
                   _(u" 3. Program design graphical techniques "
                     u"(flowcharts, HIPO, etc.) will be used."),
                   _(u" 4. Simulation/emulation tools will be used."),
                   _(u" 5. Configuration management tools will be used."),
                   _(u" 6. A code auditing tool will be used."),
                   _(u" 7. A data flow analyzer will be used."),
                   _(u" 8. A programmer's workbench will be used."),
                   _(u" 9. Measurement tools will be used."),
                   _(u"10. Software code reviews will be used."),
                   _(u"11. Software branch testing will be used."),
                   _(u"12. Random testing will be used."),
                   _(u"13. Functional testing will be used."),
                   _(u"14. Error and anomaly detection testing will be "
                     u"used."),
                   _(u"15. Structure analysis will be used.")]
        (__, _y_pos) = Widgets.make_labels(_labels, _fixed, 5, 5, wrap=False)

        _fixed.put(self.chkDevEnvQ29, _x_pos, _y_pos[0])
        _fixed.put(self.chkDevEnvQ30, _x_pos, _y_pos[1])
        _fixed.put(self.chkDevEnvQ31, _x_pos, _y_pos[2])
        _fixed.put(self.chkDevEnvQ32, _x_pos, _y_pos[3])
        _fixed.put(self.chkDevEnvQ33, _x_pos, _y_pos[4])
        _fixed.put(self.chkDevEnvQ34, _x_pos, _y_pos[5])
        _fixed.put(self.chkDevEnvQ35, _x_pos, _y_pos[6])
        _fixed.put(self.chkDevEnvQ36, _x_pos, _y_pos[7])
        _fixed.put(self.chkDevEnvQ37, _x_pos, _y_pos[8])
        _fixed.put(self.chkDevEnvQ38, _x_pos, _y_pos[9])
        _fixed.put(self.chkDevEnvQ39, _x_pos, _y_pos[10])
        _fixed.put(self.chkDevEnvQ40, _x_pos, _y_pos[11])
        _fixed.put(self.chkDevEnvQ41, _x_pos, _y_pos[12])
        _fixed.put(self.chkDevEnvQ42, _x_pos, _y_pos[13])
        _fixed.put(self.chkDevEnvQ43, _x_pos, _y_pos[14])

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Development\nEnvironment") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_angle(0)
        _label.show_all()
        _label.set_tooltip_text(_(u"Assesses risk due to the development "
                                  u"environment."))
        notebook.insert_page(self, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Development Environment Risk Analysis answers.

        :param `rtk.software.Software` model: the Software data model to load
                                              the gtk.ToggleButton() from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = model

        self.chkDevEnvQ1.set_active(model.lst_development[0])
        self.chkDevEnvQ2.set_active(model.lst_development[1])
        self.chkDevEnvQ3.set_active(model.lst_development[2])
        self.chkDevEnvQ4.set_active(model.lst_development[3])
        self.chkDevEnvQ5.set_active(model.lst_development[4])
        self.chkDevEnvQ6.set_active(model.lst_development[5])
        self.chkDevEnvQ7.set_active(model.lst_development[6])
        self.chkDevEnvQ8.set_active(model.lst_development[7])
        self.chkDevEnvQ9.set_active(model.lst_development[8])
        self.chkDevEnvQ10.set_active(model.lst_development[9])
        self.chkDevEnvQ11.set_active(model.lst_development[10])
        self.chkDevEnvQ12.set_active(model.lst_development[11])
        self.chkDevEnvQ13.set_active(model.lst_development[12])
        self.chkDevEnvQ14.set_active(model.lst_development[13])
        self.chkDevEnvQ15.set_active(model.lst_development[14])
        self.chkDevEnvQ16.set_active(model.lst_development[15])
        self.chkDevEnvQ17.set_active(model.lst_development[16])
        self.chkDevEnvQ18.set_active(model.lst_development[17])
        self.chkDevEnvQ19.set_active(model.lst_development[18])
        self.chkDevEnvQ20.set_active(model.lst_development[19])
        self.chkDevEnvQ21.set_active(model.lst_development[20])
        self.chkDevEnvQ22.set_active(model.lst_development[21])
        self.chkDevEnvQ23.set_active(model.lst_development[22])
        self.chkDevEnvQ24.set_active(model.lst_development[23])
        self.chkDevEnvQ25.set_active(model.lst_development[24])
        self.chkDevEnvQ26.set_active(model.lst_development[25])
        self.chkDevEnvQ27.set_active(model.lst_development[26])
        self.chkDevEnvQ28.set_active(model.lst_development[27])
        self.chkDevEnvQ29.set_active(model.lst_development[28])
        self.chkDevEnvQ30.set_active(model.lst_development[29])
        self.chkDevEnvQ31.set_active(model.lst_development[30])
        self.chkDevEnvQ32.set_active(model.lst_development[31])
        self.chkDevEnvQ33.set_active(model.lst_development[32])
        self.chkDevEnvQ34.set_active(model.lst_development[33])
        self.chkDevEnvQ35.set_active(model.lst_development[34])
        self.chkDevEnvQ36.set_active(model.lst_development[35])
        self.chkDevEnvQ37.set_active(model.lst_development[36])
        self.chkDevEnvQ38.set_active(model.lst_development[37])
        self.chkDevEnvQ39.set_active(model.lst_development[38])
        self.chkDevEnvQ40.set_active(model.lst_development[39])
        self.chkDevEnvQ41.set_active(model.lst_development[40])
        self.chkDevEnvQ42.set_active(model.lst_development[41])
        self.chkDevEnvQ43.set_active(model.lst_development[42])

        return False

    def _on_toggled(self, check, index):
        """
        Callback method for gtk.CheckButton() 'toggled' event.

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the index of the Development Environment question
                          associated with the gtk.CheckButton() that was
                          toggled.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        check.handler_block(self._lst_handler_id[index])

        self._software_model.lst_development[index] = int(check.get_active())

        check.handler_unblock(self._lst_handler_id[index])

        return False
