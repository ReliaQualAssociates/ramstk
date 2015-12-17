#!/usr/bin/env python
"""
##########################################################################
Software Package Risk Analysis Requirements Review Specific Work Book View
##########################################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       software.gui.gtk.SRR.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    import Utilities as _util
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
    import rtk.gui.gtk.Widgets as _widg

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class RiskAnalysis(gtk.VPaned):
    """
    The Work Book view for analyzing and displaying the risk at the System
    Requirement Review phase.  The attributes of a SRR Work Book view are:
    """

    def __init__(self):
        """
        Creates an input vertical paned for the SRR risk analysis questions.
        """

        gtk.VPaned.__init__(self)

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._software_model = None

        # CSCI-level Yes/No from WS2A (16 questions)
        # CSCI-level quantity from WS2A (6 questions)
        self.chkSRRAMQ5 = _widg.make_check_button()
        self.chkSRRAMQ8 = _widg.make_check_button()
        self.chkSRRAMQ9 = _widg.make_check_button()
        self.chkSRRAMQ10 = _widg.make_check_button()
        self.chkSRRAMQ11 = _widg.make_check_button()
        self.chkSRRAMQ12 = _widg.make_check_button()
        self.chkSRRAMQ13 = _widg.make_check_button()
        self.chkSRRAMQ14 = _widg.make_check_button()
        self.chkSRRAMQ15 = _widg.make_check_button()
        self.chkSRRAMQ16 = _widg.make_check_button()
        self.chkSRRAMQ17 = _widg.make_check_button()
        self.chkSRRAMQ18 = _widg.make_check_button()
        self.chkSRRAMQ19 = _widg.make_check_button()
        self.chkSRRAMQ20 = _widg.make_check_button()
        self.chkSRRAMQ21 = _widg.make_check_button()
        self.chkSRRAMQ22 = _widg.make_check_button()

        self.txtSRRAMQ1 = _widg.make_entry(width=50)
        self.txtSRRAMQ2 = _widg.make_entry(width=50)
        self.txtSRRAMQ3 = _widg.make_entry(width=50)
        self.txtSRRAMQ4 = _widg.make_entry(width=50)
        self.txtSRRAMQ6 = _widg.make_entry(width=50)
        self.txtSRRAMQ7 = _widg.make_entry(width=50)

        # CSCI-level Yes/No from WS3A (1 question)
        self.chkSRRSTQ1 = _widg.make_check_button()

        # CSCI-level Yes/No from WS4A (23 questions)
        # CSCI-level quantity from WS4A (4 questions)
        self.chkSRRQCQ1 = _widg.make_check_button()
        self.chkSRRQCQ2 = _widg.make_check_button()
        self.chkSRRQCQ3 = _widg.make_check_button()
        self.chkSRRQCQ4 = _widg.make_check_button()
        self.chkSRRQCQ5 = _widg.make_check_button()
        self.chkSRRQCQ6 = _widg.make_check_button()
        self.chkSRRQCQ7 = _widg.make_check_button()
        self.chkSRRQCQ8 = _widg.make_check_button()
        self.chkSRRQCQ13 = _widg.make_check_button()
        self.chkSRRQCQ14 = _widg.make_check_button()
        self.chkSRRQCQ15 = _widg.make_check_button()
        self.chkSRRQCQ16 = _widg.make_check_button()
        self.chkSRRQCQ17 = _widg.make_check_button()
        self.chkSRRQCQ18 = _widg.make_check_button()
        self.chkSRRQCQ19 = _widg.make_check_button()
        self.chkSRRQCQ20 = _widg.make_check_button()
        self.chkSRRQCQ21 = _widg.make_check_button()
        self.chkSRRQCQ22 = _widg.make_check_button()
        self.chkSRRQCQ23 = _widg.make_check_button()
        self.chkSRRQCQ24 = _widg.make_check_button()
        self.chkSRRQCQ25 = _widg.make_check_button()
        self.chkSRRQCQ26 = _widg.make_check_button()
        self.chkSRRQCQ27 = _widg.make_check_button()

        self.txtSRRQCQ9 = _widg.make_entry(width=50)
        self.txtSRRQCQ10 = _widg.make_entry(width=50)
        self.txtSRRQCQ11 = _widg.make_entry(width=50)
        self.txtSRRQCQ12 = _widg.make_entry(width=50)

    def create_risk_analysis_page(self, notebook):
        """
        Method to create the SRR risk analysis page and add it to the risk
        analysis gtk.Notebook().

        :param gtk.Notebook notebook: the gtk.Notebook() instance that will
                                      hold the development environment analysis
                                      questions.
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the anomaly management risk pane.
        _fixed1 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed1)

        _frame = _widg.make_frame(label=_(u"Anomaly Management"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack1(_frame, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u" 1. Number of instances of different processes (or "
                     u"functions, subfunctions) which are required to be\n"
                     u"executed at the same time (i.e., concurrent "
                     u"processing):"),
                   _(u" 2. Number of instances of concurrent processing "
                     u"required to be centrally controlled:"),
                   _(u" 3. Number of error conditions required to be "
                     u"recognized/identified:"),
                   _(u" 4. Number of recognized error conditions that "
                     u"require recovery or repair:"),
                   _(u" 5. There is a standard for handling recognized "
                     u"errors such that all error conditions are passed "
                     u"to\nthe calling function."),
                   _(u" 6. Number of instances of the same process (or "
                     u"function, subfunction) being required to execute\n"
                     u"more than once for comparison purposes (i.e., "
                     u"polling of parallel or redundant\nprocessing "
                     u"results):"),
                   _(u" 7. Number of instances of parallel/redundant "
                     u"processing that are required to be centrally "
                     u"controlled:"),
                   _(u" 8. Error tolerances are specified for all "
                     u"applicable external input data\n(i.e., range of "
                     u"numerical values, legal  combinations of "
                     u"alphanumerical values)."),
                   _(u" 9. There are requirements for detection of and/or "
                     u"recovery from all computational failures."),
                   _(u"10. There are requirements to range test all "
                     u"critical loop and multiple transfer index "
                     u"parameters before used."),
                   _(u"11. There are requirements to range test all "
                     u"critical subscript values before use."),
                   _(u"12. There are requirements to range test all "
                     u"critical output data before final outputting."),
                   _(u"13. There are requirements for recovery from all "
                     u"detected hardware faults."),
                   _(u"14. There are requirements for recovery from all "
                     u"I/O divide errors."),
                   _(u"15. There are requirements for recovery from all "
                     u"communication transmission errors."),
                   _(u"16. There are requirements for recovery from all "
                     u"failures to communicate with other nodes or other "
                     u"systems."),
                   _(u"17. There are requirements to periodically check "
                     u"adjacent nodes or operating system for operational "
                     u"status."),
                   _(u"18. There are requirements to provide a strategy "
                     u"for alternating routing of messages."),
                   _(u"19. There are requirements to ensure communication "
                     u"paths to all remaining\nnodes/communication links "
                     u"in the event of a failure of one node/link."),
                   _(u"20. There are requirements for maintaining the "
                     u"integrity of all data values following the\n"
                     u"occurence of anomalous conditions."),
                   _(u"21. There are requirements to enable all "
                     u"disconnected nodes to rejoin the network after "
                     u"recovery, such\nthat the processing functions of "
                     u"the system are not interrupted."),
                   _(u"22. There are requirements to replicate all "
                     u"critical data at two or more distinct nodes.")]
        (_x_pos, _y_pos1) = _widg.make_labels(_labels, _fixed1,
                                              5, 5, wrap=False)

        # Create the quality control risk pane.
        _fixed2 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed2)

        _frame = _widg.make_frame(label=_(u"Software Quality Control"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack2(_frame, resize=True, shrink=True)

        _labels = [_(u" 1. There is a table(s) tracing all requirements "
                     u"to the parent system or subsystem specification."),
                   _(u" 2. There are quantitative accuracy requirements "
                     u"for all inputs associated with each function."),
                   _(u" 3. There are quantitative accuracy requirements "
                     u"for all outputs associated with each function."),
                   _(u" 4. There are quantitative accuracy requirements "
                     u"for all constants associated with each function."),
                   _(u" 5. The existing math library routines which are "
                     u"planned for use provide enough precision to "
                     u"support\naccuracy objectives."),
                   _(u" 6. All processes and functions are partitioned to "
                     u"be logically complete and self contained so as to\n"
                     u"minimize interface complexity."),
                   _(u" 7. There are requirements for each operational "
                     u"CPU/System to have a separate power source."),
                   _(u" 8. There are requirements for the executive "
                     u"software to perform testing of its own operation "
                     u"and of\nthecommunication links, memory devices, "
                     u"and peripheral devices."),
                   _(u" 9. All inputs, processing, and outputs are "
                     u"clearly and precisely defined."),
                   _(u"10. Number of data references that are identified:"),
                   _(u"11. Number of identified data references that are "
                     u"documented with regard to source, meaning, and "
                     u"format:"),
                   _(u"12. Number of data items that are identified "
                     u"(e.g., documented with regard to source, meaning, "
                     u"and format):"),
                   _(u"13. Number of data items that are referenced:"),
                   _(u"14. All defined functions have been referenced."),
                   _(u"15. All system functions allocated to this module "
                     u"have been allocated to software functions "
                     u"within\nthis module."),
                   _(u"16. All referenced functions have been defined "
                     u"(i.e., documented with precise inputs, processing,"
                     u"\nand output requirements)."),
                   _(u"17. The flow of processing (algorithms) and all "
                     u"decision points (conditions and alternate paths) "
                     u"in the flow\nis described for all functions."),
                   _(u"18. Specific standards have been established for "
                     u"design representations (e.g., HIPO charts, program "
                     u"\ndesign language, flow charts, data flow "
                     u"diagrams)."),
                   _(u"19. Specific standards have been established for "
                     u"calling sequence protocol between software units."),
                   _(u"20. Specific standards have been established for "
                     u"external I/O protocol and format for all software "
                     u"units."),
                   _(u"21. Specific standards have been established for "
                     u"error handling for all software units."),
                   _(u"22. All references to the same function use a "
                     u"single, unique name."),
                   _(u"23. Specific standards have been established for "
                     u"all data representation in the design."),
                   _(u"24. Specific standards have been established for "
                     u"the naming of all data."),
                   _(u"25. Specific standards have been established for "
                     u"the definition and use of global variables."),
                   _(u"26. There are procedures for establishing "
                     u"consistency and concurrency of multiple copies\n"
                     u"(e.g., copies at different nodes) of the same "
                     u"software or database version."),
                   _(u"27. There are procedures for verifying consistency "
                     u"and concurrency of multiple copies\n(e.g., copies "
                     u"at different nodes) of the same software or "
                     u"database version."),
                   _(u"28. All references to the same data use a single, "
                     u"unique name.")]
        (_x_pos2, _y_pos2) = _widg.make_labels(_labels, _fixed2,
                                               5, 5, wrap=False)
        _x_pos = max(_x_pos, _x_pos2) + 125

        # Place the anomaly management widgets.
        _fixed1.put(self.txtSRRAMQ1, _x_pos, _y_pos1[0])
        _fixed1.put(self.txtSRRAMQ2, _x_pos, _y_pos1[1])
        _fixed1.put(self.txtSRRAMQ3, _x_pos, _y_pos1[2])
        _fixed1.put(self.txtSRRAMQ4, _x_pos, _y_pos1[3])
        _fixed1.put(self.chkSRRAMQ5, _x_pos, _y_pos1[4])
        _fixed1.put(self.txtSRRAMQ6, _x_pos, _y_pos1[5])
        _fixed1.put(self.txtSRRAMQ7, _x_pos, _y_pos1[6])
        _fixed1.put(self.chkSRRAMQ8, _x_pos, _y_pos1[7])
        _fixed1.put(self.chkSRRAMQ9, _x_pos, _y_pos1[8])
        _fixed1.put(self.chkSRRAMQ10, _x_pos, _y_pos1[9])
        _fixed1.put(self.chkSRRAMQ11, _x_pos, _y_pos1[10])
        _fixed1.put(self.chkSRRAMQ12, _x_pos, _y_pos1[11])
        _fixed1.put(self.chkSRRAMQ13, _x_pos, _y_pos1[12])
        _fixed1.put(self.chkSRRAMQ14, _x_pos, _y_pos1[13])
        _fixed1.put(self.chkSRRAMQ15, _x_pos, _y_pos1[14])
        _fixed1.put(self.chkSRRAMQ16, _x_pos, _y_pos1[15])
        _fixed1.put(self.chkSRRAMQ17, _x_pos, _y_pos1[16])
        _fixed1.put(self.chkSRRAMQ18, _x_pos, _y_pos1[17])
        _fixed1.put(self.chkSRRAMQ19, _x_pos, _y_pos1[18])
        _fixed1.put(self.chkSRRAMQ20, _x_pos, _y_pos1[19])
        _fixed1.put(self.chkSRRAMQ21, _x_pos, _y_pos1[20])
        _fixed1.put(self.chkSRRAMQ22, _x_pos, _y_pos1[21])

        # Place the quality control widgets.
        _fixed2.put(self.chkSRRSTQ1, _x_pos, _y_pos2[0])
        _fixed2.put(self.chkSRRQCQ1, _x_pos, _y_pos2[1])
        _fixed2.put(self.chkSRRQCQ2, _x_pos, _y_pos2[2])
        _fixed2.put(self.chkSRRQCQ3, _x_pos, _y_pos2[3])
        _fixed2.put(self.chkSRRQCQ4, _x_pos, _y_pos2[4])
        _fixed2.put(self.chkSRRQCQ5, _x_pos, _y_pos2[5])
        _fixed2.put(self.chkSRRQCQ6, _x_pos, _y_pos2[6])
        _fixed2.put(self.chkSRRQCQ7, _x_pos, _y_pos2[7])
        _fixed2.put(self.chkSRRQCQ8, _x_pos, _y_pos2[8])
        _fixed2.put(self.txtSRRQCQ9, _x_pos, _y_pos2[9])
        _fixed2.put(self.txtSRRQCQ10, _x_pos, _y_pos2[10])
        _fixed2.put(self.txtSRRQCQ11, _x_pos, _y_pos2[11])
        _fixed2.put(self.txtSRRQCQ12, _x_pos, _y_pos2[12])
        _fixed2.put(self.chkSRRQCQ13, _x_pos, _y_pos2[13])
        _fixed2.put(self.chkSRRQCQ14, _x_pos, _y_pos2[14])
        _fixed2.put(self.chkSRRQCQ15, _x_pos, _y_pos2[15])
        _fixed2.put(self.chkSRRQCQ16, _x_pos, _y_pos2[16])
        _fixed2.put(self.chkSRRQCQ17, _x_pos, _y_pos2[17])
        _fixed2.put(self.chkSRRQCQ18, _x_pos, _y_pos2[18])
        _fixed2.put(self.chkSRRQCQ19, _x_pos, _y_pos2[19])
        _fixed2.put(self.chkSRRQCQ20, _x_pos, _y_pos2[20])
        _fixed2.put(self.chkSRRQCQ21, _x_pos, _y_pos2[21])
        _fixed2.put(self.chkSRRQCQ22, _x_pos, _y_pos2[22])
        _fixed2.put(self.chkSRRQCQ23, _x_pos, _y_pos2[23])
        _fixed2.put(self.chkSRRQCQ24, _x_pos, _y_pos2[24])
        _fixed2.put(self.chkSRRQCQ25, _x_pos, _y_pos2[25])
        _fixed2.put(self.chkSRRQCQ26, _x_pos, _y_pos2[26])
        _fixed2.put(self.chkSRRQCQ27, _x_pos, _y_pos2[27])

        # Connect the anomaly management widgets to callback methods.
        self._lst_handler_id.append(
            self.txtSRRAMQ1.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtSRRAMQ2.connect('focus-out-event', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.txtSRRAMQ3.connect('focus-out-event', self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.txtSRRAMQ4.connect('focus-out-event', self._on_focus_out, 3))
        self._lst_handler_id.append(
            self.chkSRRAMQ5.connect('toggled', self._on_toggled, 4))
        self._lst_handler_id.append(
            self.txtSRRAMQ6.connect('focus-out-event', self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtSRRAMQ7.connect('focus-out-event', self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.chkSRRAMQ8.connect('toggled', self._on_toggled, 7))
        self._lst_handler_id.append(
            self.chkSRRAMQ9.connect('toggled', self._on_toggled, 8))
        self._lst_handler_id.append(
            self.chkSRRAMQ10.connect('toggled', self._on_toggled, 9))
        self._lst_handler_id.append(
            self.chkSRRAMQ11.connect('toggled', self._on_toggled, 10))
        self._lst_handler_id.append(
            self.chkSRRAMQ12.connect('toggled', self._on_toggled, 11))
        self._lst_handler_id.append(
            self.chkSRRAMQ13.connect('toggled', self._on_toggled, 12))
        self._lst_handler_id.append(
            self.chkSRRAMQ14.connect('toggled', self._on_toggled, 13))
        self._lst_handler_id.append(
            self.chkSRRAMQ15.connect('toggled', self._on_toggled, 14))
        self._lst_handler_id.append(
            self.chkSRRAMQ16.connect('toggled', self._on_toggled, 15))
        self._lst_handler_id.append(
            self.chkSRRAMQ17.connect('toggled', self._on_toggled, 16))
        self._lst_handler_id.append(
            self.chkSRRAMQ18.connect('toggled', self._on_toggled, 17))
        self._lst_handler_id.append(
            self.chkSRRAMQ19.connect('toggled', self._on_toggled, 18))
        self._lst_handler_id.append(
            self.chkSRRAMQ20.connect('toggled', self._on_toggled, 19))
        self._lst_handler_id.append(
            self.chkSRRAMQ21.connect('toggled', self._on_toggled, 20))
        self._lst_handler_id.append(
            self.chkSRRAMQ22.connect('toggled', self._on_toggled, 21))

        # Connect the quality control widgets to callback methods.
        self._lst_handler_id.append(
            self.chkSRRSTQ1.connect('toggled', self._on_toggled, 22))
        self._lst_handler_id.append(
            self.chkSRRQCQ1.connect('toggled', self._on_toggled, 23))
        self._lst_handler_id.append(
            self.chkSRRQCQ2.connect('toggled', self._on_toggled, 24))
        self._lst_handler_id.append(
            self.chkSRRQCQ3.connect('toggled', self._on_toggled, 25))
        self._lst_handler_id.append(
            self.chkSRRQCQ4.connect('toggled', self._on_toggled, 26))
        self._lst_handler_id.append(
            self.chkSRRQCQ5.connect('toggled', self._on_toggled, 27))
        self._lst_handler_id.append(
            self.chkSRRQCQ6.connect('toggled', self._on_toggled, 28))
        self._lst_handler_id.append(
            self.chkSRRQCQ7.connect('toggled', self._on_toggled, 29))
        self._lst_handler_id.append(
            self.chkSRRQCQ8.connect('toggled', self._on_toggled, 30))
        self._lst_handler_id.append(
            self.txtSRRQCQ9.connect('focus-out-event',
                                    self._on_focus_out, 31))
        self._lst_handler_id.append(
            self.txtSRRQCQ10.connect('focus-out-event',
                                     self._on_focus_out, 32))
        self._lst_handler_id.append(
            self.txtSRRQCQ11.connect('focus-out-event',
                                     self._on_focus_out, 33))
        self._lst_handler_id.append(
            self.txtSRRQCQ12.connect('focus-out-event',
                                     self._on_focus_out, 34))
        self._lst_handler_id.append(
            self.chkSRRQCQ13.connect('toggled', self._on_toggled, 35))
        self._lst_handler_id.append(
            self.chkSRRQCQ14.connect('toggled', self._on_toggled, 36))
        self._lst_handler_id.append(
            self.chkSRRQCQ15.connect('toggled', self._on_toggled, 37))
        self._lst_handler_id.append(
            self.chkSRRQCQ16.connect('toggled', self._on_toggled, 38))
        self._lst_handler_id.append(
            self.chkSRRQCQ17.connect('toggled', self._on_toggled, 39))
        self._lst_handler_id.append(
            self.chkSRRQCQ18.connect('toggled', self._on_toggled, 40))
        self._lst_handler_id.append(
            self.chkSRRQCQ19.connect('toggled', self._on_toggled, 41))
        self._lst_handler_id.append(
            self.chkSRRQCQ20.connect('toggled', self._on_toggled, 42))
        self._lst_handler_id.append(
            self.chkSRRQCQ21.connect('toggled', self._on_toggled, 43))
        self._lst_handler_id.append(
            self.chkSRRQCQ22.connect('toggled', self._on_toggled, 44))
        self._lst_handler_id.append(
            self.chkSRRQCQ23.connect('toggled', self._on_toggled, 45))
        self._lst_handler_id.append(
            self.chkSRRQCQ24.connect('toggled', self._on_toggled, 46))
        self._lst_handler_id.append(
            self.chkSRRQCQ25.connect('toggled', self._on_toggled, 47))
        self._lst_handler_id.append(
            self.chkSRRQCQ26.connect('toggled', self._on_toggled, 48))
        self._lst_handler_id.append(
            self.chkSRRQCQ27.connect('toggled', self._on_toggled, 49))

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _("Requirements\nReview") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_angle(0)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows assessment of the reliability risk "
                                  u"at the requirements review phase."))

        notebook.insert_page(self, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Requirements Review Risk Analysis answers.

        :param `rtk.software.Software` model: the Software data model to load
                                              the gtk.ToggleButton() from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = model

        self.txtSRRAMQ1.set_text(str(model.lst_anomaly_mgmt[0][0]))
        self.txtSRRAMQ2.set_text(str(model.lst_anomaly_mgmt[0][1]))
        self.txtSRRAMQ3.set_text(str(model.lst_anomaly_mgmt[0][2]))
        self.txtSRRAMQ4.set_text(str(model.lst_anomaly_mgmt[0][3]))
        self.chkSRRAMQ5.set_active(model.lst_anomaly_mgmt[0][4])
        self.txtSRRAMQ6.set_text(str(model.lst_anomaly_mgmt[0][5]))
        self.txtSRRAMQ7.set_text(str(model.lst_anomaly_mgmt[0][6]))
        self.chkSRRAMQ8.set_active(model.lst_anomaly_mgmt[0][7])
        self.chkSRRAMQ9.set_active(model.lst_anomaly_mgmt[0][8])
        self.chkSRRAMQ10.set_active(model.lst_anomaly_mgmt[0][9])
        self.chkSRRAMQ11.set_active(model.lst_anomaly_mgmt[0][10])
        self.chkSRRAMQ12.set_active(model.lst_anomaly_mgmt[0][11])
        self.chkSRRAMQ13.set_active(model.lst_anomaly_mgmt[0][12])
        self.chkSRRAMQ14.set_active(model.lst_anomaly_mgmt[0][13])
        self.chkSRRAMQ15.set_active(model.lst_anomaly_mgmt[0][14])
        self.chkSRRAMQ16.set_active(model.lst_anomaly_mgmt[0][15])
        self.chkSRRAMQ17.set_active(model.lst_anomaly_mgmt[0][16])
        self.chkSRRAMQ18.set_active(model.lst_anomaly_mgmt[0][17])
        self.chkSRRAMQ19.set_active(model.lst_anomaly_mgmt[0][18])
        self.chkSRRAMQ20.set_active(model.lst_anomaly_mgmt[0][19])
        self.chkSRRAMQ21.set_active(model.lst_anomaly_mgmt[0][20])
        self.chkSRRAMQ22.set_active(model.lst_anomaly_mgmt[0][21])

        self.chkSRRSTQ1.set_active(model.lst_traceability[0][0])

        self.chkSRRQCQ1.set_active(model.lst_sftw_quality[0][0])
        self.chkSRRQCQ2.set_active(model.lst_sftw_quality[0][1])
        self.chkSRRQCQ3.set_active(model.lst_sftw_quality[0][2])
        self.chkSRRQCQ4.set_active(model.lst_sftw_quality[0][3])
        self.chkSRRQCQ5.set_active(model.lst_sftw_quality[0][4])
        self.chkSRRQCQ6.set_active(model.lst_sftw_quality[0][5])
        self.chkSRRQCQ7.set_active(model.lst_sftw_quality[0][6])
        self.chkSRRQCQ8.set_active(model.lst_sftw_quality[0][7])
        self.txtSRRQCQ9.set_text(str(model.lst_sftw_quality[0][8]))
        self.txtSRRQCQ10.set_text(str(model.lst_sftw_quality[0][9]))
        self.txtSRRQCQ11.set_text(str(model.lst_sftw_quality[0][10]))
        self.txtSRRQCQ12.set_text(str(model.lst_sftw_quality[0][11]))
        self.chkSRRQCQ13.set_active(model.lst_sftw_quality[0][12])
        self.chkSRRQCQ14.set_active(model.lst_sftw_quality[0][13])
        self.chkSRRQCQ15.set_active(model.lst_sftw_quality[0][14])
        self.chkSRRQCQ16.set_active(model.lst_sftw_quality[0][15])
        self.chkSRRQCQ17.set_active(model.lst_sftw_quality[0][16])
        self.chkSRRQCQ18.set_active(model.lst_sftw_quality[0][17])
        self.chkSRRQCQ19.set_active(model.lst_sftw_quality[0][18])
        self.chkSRRQCQ20.set_active(model.lst_sftw_quality[0][19])
        self.chkSRRQCQ21.set_active(model.lst_sftw_quality[0][20])
        self.chkSRRQCQ22.set_active(model.lst_sftw_quality[0][21])
        self.chkSRRQCQ23.set_active(model.lst_sftw_quality[0][22])
        self.chkSRRQCQ24.set_active(model.lst_sftw_quality[0][23])
        self.chkSRRQCQ25.set_active(model.lst_sftw_quality[0][24])
        self.chkSRRQCQ26.set_active(model.lst_sftw_quality[0][25])
        self.chkSRRQCQ27.set_active(model.lst_sftw_quality[0][26])

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

        if index in [0, 1, 2, 3, 5, 6]:
            self._software_model.lst_anomaly_mgmt[0][index] = int(entry.get_text())
        elif index in [31, 32, 33, 34]:
            self._software_model.lst_sftw_quality[0][index - 23] = int(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_toggled(self, check, index):
        """
        Callback function for gtk.CheckButton() 'toggled' event.

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the index of the Development Environment question
                          associated with the gtk.CheckButton() that was
                          toggled.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        check.handler_block(self._lst_handler_id[index])

        if index in [4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                     21]:
            self._software_model.lst_anomaly_mgmt[0][index] = int(check.get_active())
        elif index == 22:
            self._software_model.lst_traceability[0][index - 22] = int(check.get_active())
        elif index in [23, 24, 25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40,
                       41, 42, 43, 44, 45, 46, 47, 48, 49]:
            self._software_model.lst_sftw_quality[0][index - 23] = int(check.get_active())

        check.handler_unblock(self._lst_handler_id[index])

        return False
