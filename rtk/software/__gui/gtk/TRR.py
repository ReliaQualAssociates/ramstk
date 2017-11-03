#!/usr/bin/env python
"""
#############################################################################
Software Package Risk Analysis Test Readiness Review Specific Work Book View
#############################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.__gui.gtk.TRR.py is part of The RTK Project
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


class CSCIRiskAnalysis(gtk.VPaned):
    """
    The Work Book view for analyzing and displaying the risk at the Test
    Readiness Review phase for CSCI.  The attributes of a TRR Work Book view
    are:

    :ivar list _lst_handler_id: the list of gtk.Widget() signal handler IDs.
    :ivar _software_model: the :py:class:`rtk.software.Software.Model` to
                           display.
    """

    def __init__(self):
        """
        Creates an input vertical paned for the CSCI TRR risk analysis
        questions.
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
        # CSCI-level quantity from WS8D and WS9D (4 questions)
        self.txtTRRLTCMQ1 = Widgets.make_entry(width=50)
        self.txtTRRLTCMQ2 = Widgets.make_entry(width=50)
        self.txtTRRLTCMQ3 = Widgets.make_entry(width=50)
        self.txtTRRLTCMQ4 = Widgets.make_entry(width=50)

        # Connect the gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.txtTRRLTCMQ1.connect('focus-out-event',
                                      self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtTRRLTCMQ2.connect('focus-out-event',
                                      self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtTRRLTCMQ3.connect('focus-out-event',
                                      self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.txtTRRLTCMQ4.connect('focus-out-event',
                                      self._on_focus_out, 3))

    def create_risk_analysis_page(self, notebook):
        """
        Method to create the Test Readiness Review risk analysis page and add
        it to the risk analysis gtk.Notebook().

        :param gtk.Notebook notebook: the gtk.Notebook() instance that will
                                      hold the TRR risk analysis questions.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the module-level containers and set them as the default
        # to display.
        _fxdcscilt = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdcscilt)

        _frame = Widgets.make_frame(_(u"Software Module Language Type, "
                                      u"Complexity, &amp; Modularity"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack1(_frame, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the language type, modularity, and complexity risk pane
        # for CSCI.
        _labels = [_(u"1. Number of units in this module:"),
                   _(u"2. Total executable lines of source code in this "
                     u"module:"),
                   _(u"3. Total assembly language lines of code in this "
                     u"module:"),
                   _(u"4. Total higher order language lines of code in this "
                     u"module:")]
        (_x_pos,
         _y_pos) = Widgets.make_labels(_labels, _fxdcscilt, 5, 5, wrap=False)
        _x_pos += 125

        _fxdcscilt.put(self.txtTRRLTCMQ1, _x_pos, _y_pos[0])
        _fxdcscilt.put(self.txtTRRLTCMQ2, _x_pos, _y_pos[1])
        _fxdcscilt.put(self.txtTRRLTCMQ3, _x_pos, _y_pos[2])
        _fxdcscilt.put(self.txtTRRLTCMQ4, _x_pos, _y_pos[3])

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Test\nReadiness\nReview") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_angle(0)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows assessment of the reliability risk "
                                  u"at the test readiness review."))
        notebook.insert_page(self, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Test Readiness Review Risk Analysis answers.

        :param model: the :py:class:`rtk.software.Software.Model` data model to
                      load the gtk.ToggleButton() from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = model

        self.txtTRRLTCMQ1.set_text(str(model.lst_modularity[0]))
        self.txtTRRLTCMQ2.set_text(str(model.lst_modularity[1]))
        self.txtTRRLTCMQ3.set_text(str(model.lst_modularity[2]))
        self.txtTRRLTCMQ4.set_text(str(model.lst_modularity[3]))

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Responds to gtk.Entry() 'focus_out' signals and calls the correct
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

        try:
            self._software_model.lst_modularity[index] = int(entry.get_text())
        except ValueError:
            self._software_model.lst_modularity[index] = 0

        entry.handler_unblock(self._lst_handler_id[index])

        return False


class UnitRiskAnalysis(gtk.VPaned):
    """
    The Work Book view for analyzing and displaying the risk at the Test
    Readiness Review phase for Units.  The attributes of a TRR Work Book view
    are:

    :ivar list _lst_handler_id: the list of gtk.Widget() signal handler IDs.
    :ivar _software_model: the :py:class:`rtk.software.Software.Model` to
                           display.
    """

    def __init__(self):
        """
        Creates an input vertical paned for the Unit TRR risk analysis
        questions.
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
        # Unit-level Yes/No from WS2C (2 questions)
        self.chkTRRAMQ1 = Widgets.make_check_button()
        self.chkTRRAMQ2 = Widgets.make_check_button()

        # Unit-level Yes/No from WS4C (14 questions)
        self.chkTRRQCQ1 = Widgets.make_check_button()
        self.chkTRRQCQ2 = Widgets.make_check_button()
        self.chkTRRQCQ3 = Widgets.make_check_button()
        self.chkTRRQCQ4 = Widgets.make_check_button()
        self.chkTRRQCQ5 = Widgets.make_check_button()
        self.chkTRRQCQ6 = Widgets.make_check_button()
        self.chkTRRQCQ7 = Widgets.make_check_button()
        self.chkTRRQCQ8 = Widgets.make_check_button()
        self.chkTRRQCQ9 = Widgets.make_check_button()
        self.chkTRRQCQ10 = Widgets.make_check_button()
        self.chkTRRQCQ11 = Widgets.make_check_button()
        self.chkTRRQCQ12 = Widgets.make_check_button()
        self.chkTRRQCQ13 = Widgets.make_check_button()
        self.chkTRRQCQ14 = Widgets.make_check_button()

        # Unit-level Yes/No from WS8D (3 questions)
        self.txtTRRLTCMQ1 = Widgets.make_entry(width=50)
        self.txtTRRLTCMQ2 = Widgets.make_entry(width=50)
        self.txtTRRLTCMQ3 = Widgets.make_entry(width=50)
        self.txtLTCMQ4 = Widgets.make_entry(width=50)
        self.txtLTCMQ5 = Widgets.make_entry(width=50)

    def create_risk_analysis_page(self, notebook):
        """
        Method to create the Test Readiness Review risk analysis page and add
        it to the risk analysis gtk.Notebook().

        :param gtk.Notebook notebook: the gtk.Notebook() instance that will
                                      hold the development environment analysis
                                      questions.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the unit-level containers.
        _fxdunitlt = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdunitlt)

        _frame = Widgets.make_frame(_(u"Software Unit Language Type, "
                                      u"Complexity, &amp; Modularity"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack1(_frame, resize=True, shrink=True)

        _fxdunitqc = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdunitqc)

        _frame = Widgets.make_frame(_(u"Software Unit Quality Control"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack2(_frame, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the language type, modularity, and complexity risk pane
        # for the unit.
        _labels = [_(u"1. Total executable lines of source code in this "
                     u"unit:"),
                   _(u"2. Total assembly language lines of code in this "
                     u"unit:"),
                   _(u"3. Total higher order language lines of code in "
                     u"this unit:"),
                   _(u"4. Number of conditional branching statements in "
                     u"this unit:"),
                   _(u"5. Number of unconditional branching statements in "
                     u"this unit:")]
        (_x_pos,
         _y_pos1) = Widgets.make_labels(_labels, _fxdunitlt, 5, 5, wrap=False)

        # Create the quality control and anomaly management risk pane for
        # the unit.
        _labels = [_(u" 1. When an error condition is detected in this "
                     u"unit, resolution of the error is determined by "
                     u"this unit."),
                   _(u" 2. A check is performed before processing begins "
                     u"to determine that all data is available."),
                   _(u" 3. All inputs, processing, and outputs are "
                     u"clearly and precisely defined for this unit."),
                   _(u" 4. All data references in this unit are defined."),
                   _(u" 5. All data references in this unit are "
                     u"identified."),
                   _(u" 6. All conditions and alternative processing "
                     u"options in this unit are defined for each decision "
                     u"point."),
                   _(u" 7. All parameters in the argument list for this "
                     u"unit are used."),
                   _(u" 8. All design representations in this unit are in "
                     u"the formats of the established standard."),
                   _(u" 9. The between unit calling sequence protocol in "
                     u"this unit complies with the established standard."),
                   _(u"10. The I/O protocol and format in this unit "
                     u"complies with the established standard."),
                   _(u"11. The handling of errors in this unit complies "
                     u"with the established standard."),
                   _(u"12. All references to this unit use the same, "
                     u"unique name."),
                   _(u"13. All data representation in this unit complies "
                     u"with the established standard."),
                   _(u"14. The naming of all data in this unit complies "
                     u"with the established standard."),
                   _(u"15. The definition and use of all global variables "
                     u"in this unit is in accordance with the established "
                     u"standard."),
                   _(u"16. All references to the same data in this unit "
                     u"use a single, unique name.")]
        (_x_pos2,
         _y_pos2) = Widgets.make_labels(_labels, _fxdunitqc, 5, 5, wrap=False)
        _x_pos = max(_x_pos, _x_pos2) + 125

        _fxdunitlt.put(self.txtTRRLTCMQ1, _x_pos, _y_pos1[0])
        _fxdunitlt.put(self.txtTRRLTCMQ2, _x_pos, _y_pos1[1])
        _fxdunitlt.put(self.txtTRRLTCMQ3, _x_pos, _y_pos1[2])
        _fxdunitlt.put(self.txtLTCMQ4, _x_pos, _y_pos1[3])
        _fxdunitlt.put(self.txtLTCMQ5, _x_pos, _y_pos1[4])

        _fxdunitqc.put(self.chkTRRAMQ1, _x_pos, _y_pos2[0])
        _fxdunitqc.put(self.chkTRRAMQ2, _x_pos, _y_pos2[1])
        _fxdunitqc.put(self.chkTRRQCQ1, _x_pos, _y_pos2[2])
        _fxdunitqc.put(self.chkTRRQCQ2, _x_pos, _y_pos2[3])
        _fxdunitqc.put(self.chkTRRQCQ3, _x_pos, _y_pos2[4])
        _fxdunitqc.put(self.chkTRRQCQ4, _x_pos, _y_pos2[5])
        _fxdunitqc.put(self.chkTRRQCQ5, _x_pos, _y_pos2[6])
        _fxdunitqc.put(self.chkTRRQCQ6, _x_pos, _y_pos2[7])
        _fxdunitqc.put(self.chkTRRQCQ7, _x_pos, _y_pos2[8])
        _fxdunitqc.put(self.chkTRRQCQ8, _x_pos, _y_pos2[9])
        _fxdunitqc.put(self.chkTRRQCQ9, _x_pos, _y_pos2[10])
        _fxdunitqc.put(self.chkTRRQCQ10, _x_pos, _y_pos2[11])
        _fxdunitqc.put(self.chkTRRQCQ11, _x_pos, _y_pos2[12])
        _fxdunitqc.put(self.chkTRRQCQ12, _x_pos, _y_pos2[13])
        _fxdunitqc.put(self.chkTRRQCQ13, _x_pos, _y_pos2[14])
        _fxdunitqc.put(self.chkTRRQCQ14, _x_pos, _y_pos2[15])

        self._lst_handler_id.append(
            self.txtTRRLTCMQ1.connect('focus-out-event',
                                      self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtTRRLTCMQ2.connect('focus-out-event',
                                      self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtTRRLTCMQ3.connect('focus-out-event',
                                      self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.txtLTCMQ4.connect('focus-out-event', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.txtLTCMQ5.connect('focus-out-event', self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.chkTRRAMQ1.connect('toggled', self._on_toggled, 5))
        self._lst_handler_id.append(
            self.chkTRRAMQ2.connect('toggled', self._on_toggled, 6))
        self._lst_handler_id.append(
            self.chkTRRQCQ1.connect('toggled', self._on_toggled, 7))
        self._lst_handler_id.append(
            self.chkTRRQCQ2.connect('toggled', self._on_toggled, 8))
        self._lst_handler_id.append(
            self.chkTRRQCQ3.connect('toggled', self._on_toggled, 9))
        self._lst_handler_id.append(
            self.chkTRRQCQ4.connect('toggled', self._on_toggled, 10))
        self._lst_handler_id.append(
            self.chkTRRQCQ5.connect('toggled', self._on_toggled, 11))
        self._lst_handler_id.append(
            self.chkTRRQCQ6.connect('toggled', self._on_toggled, 12))
        self._lst_handler_id.append(
            self.chkTRRQCQ7.connect('toggled', self._on_toggled, 13))
        self._lst_handler_id.append(
            self.chkTRRQCQ8.connect('toggled', self._on_toggled, 14))
        self._lst_handler_id.append(
            self.chkTRRQCQ9.connect('toggled', self._on_toggled, 15))
        self._lst_handler_id.append(
            self.chkTRRQCQ10.connect('toggled', self._on_toggled, 16))
        self._lst_handler_id.append(
            self.chkTRRQCQ11.connect('toggled', self._on_toggled, 17))
        self._lst_handler_id.append(
            self.chkTRRQCQ12.connect('toggled', self._on_toggled, 18))
        self._lst_handler_id.append(
            self.chkTRRQCQ13.connect('toggled', self._on_toggled, 19))
        self._lst_handler_id.append(
            self.chkTRRQCQ14.connect('toggled', self._on_toggled, 20))

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Test\nReadiness\nReview") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_angle(90)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows assessment of the reliability risk "
                                  u"at the test readiness review."))
        notebook.insert_page(self, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Test Readiness Review Risk Analysis answers.

        :param model: the :py:class:`rtk.software.Software.Model` data model to
                      load the gtk.ToggleButton() from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = model

        self.txtTRRLTCMQ1.set_text(str(model.sloc))
        self.txtTRRLTCMQ2.set_text(str(model.aloc))
        self.txtTRRLTCMQ3.set_text(str(model.hloc))
        self.txtLTCMQ4.set_text(str(model.cb))
        self.txtLTCMQ5.set_text(str(model.ncb))

        self.chkTRRAMQ1.set_active(model.lst_anomaly_mgmt[3][0])
        self.chkTRRAMQ2.set_active(model.lst_anomaly_mgmt[3][1])

        self.chkTRRQCQ1.set_active(model.lst_sftw_quality[3][0])
        self.chkTRRQCQ2.set_active(model.lst_sftw_quality[3][1])
        self.chkTRRQCQ3.set_active(model.lst_sftw_quality[3][2])
        self.chkTRRQCQ4.set_active(model.lst_sftw_quality[3][3])
        self.chkTRRQCQ5.set_active(model.lst_sftw_quality[3][4])
        self.chkTRRQCQ6.set_active(model.lst_sftw_quality[3][5])
        self.chkTRRQCQ7.set_active(model.lst_sftw_quality[3][6])
        self.chkTRRQCQ8.set_active(model.lst_sftw_quality[3][7])
        self.chkTRRQCQ9.set_active(model.lst_sftw_quality[3][8])
        self.chkTRRQCQ10.set_active(model.lst_sftw_quality[3][9])
        self.chkTRRQCQ11.set_active(model.lst_sftw_quality[3][10])
        self.chkTRRQCQ12.set_active(model.lst_sftw_quality[3][11])
        self.chkTRRQCQ13.set_active(model.lst_sftw_quality[3][12])
        self.chkTRRQCQ14.set_active(model.lst_sftw_quality[3][13])

        return False

    def _on_focus_out(self, entry, __event, index):
        """
        Responds to gtk.Entry() 'focus_out' signals and calls the correct
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

        try:
            self._software_model.lst_modularity[index] = int(entry.get_text())
            if index == 0:
                self._software_model.sloc = int(entry.get_text())
            elif index == 1:
                self._software_model.aloc = int(entry.get_text())
            elif index == 2:
                self._software_model.hloc = int(entry.get_text())
            elif index == 3:
                self._software_model.cb = int(entry.get_text())
            elif index == 4:
                self._software_model.ncb = int(entry.get_text())
        except ValueError:
            self._software_model.lst_modularity[index] = 0

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_toggled(self, check, index):
        """
        Callback method for gtk.CheckButton() 'toggled' signals.

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the index of the Development Environment question
                          associated with the gtk.CheckButton() that was
                          toggled.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        check.handler_block(self._lst_handler_id[index])

        if index in []:
            self._software_model.lst_anomaly_mgmt[index - 5] = int(check.get_active())
        elif index in []:
            self._software_model.lst_sftw_quality[index - 7] = int(check.get_active())

        check.handler_unblock(self._lst_handler_id[index])

        return False
