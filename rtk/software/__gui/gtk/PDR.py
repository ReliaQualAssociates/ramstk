#!/usr/bin/env python
"""
################################################################################
Software Package Risk Analysis Preliminary Design Review Specific Work Book View
################################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.gui.gtk.PDR.py is part of The RTK Project
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
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
<<<<<<< HEAD
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
=======
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class RiskAnalysis(gtk.VPaned):
    """
    The Work Book view for analyzing and displaying the risk at the Preliminary
    Design Review phase.  The attributes of a PDR Work Book view are:
<<<<<<< HEAD
=======

    :ivar list _lst_handler_id: the list of gtk.Widget() signal handler IDs.
    :ivar _software_model: the :py:class:`rtk.software.Software.Model` to
                           display.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    """

    def __init__(self):
        """
<<<<<<< HEAD
        Creates an input vertical paned for the PDR risk analysis questions.
=======
        Method to create the PDR risk analysis questions.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        gtk.VPaned.__init__(self)

<<<<<<< HEAD
        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._software_model = None

        # CSCI-level Yes/No from WS2B (14 questions)
        self.chkPDRAMQ1 = _widg.make_check_button()
        self.chkPDRAMQ2 = _widg.make_check_button()
        self.chkPDRAMQ3 = _widg.make_check_button()
        self.chkPDRAMQ4 = _widg.make_check_button()
        self.chkPDRAMQ5 = _widg.make_check_button()
        self.chkPDRAMQ6 = _widg.make_check_button()
        self.chkPDRAMQ7 = _widg.make_check_button()
        self.chkPDRAMQ8 = _widg.make_check_button()
        self.chkPDRAMQ9 = _widg.make_check_button()
        self.chkPDRAMQ10 = _widg.make_check_button()
        self.chkPDRAMQ11 = _widg.make_check_button()
        self.chkPDRAMQ12 = _widg.make_check_button()
        self.chkPDRAMQ13 = _widg.make_check_button()
        self.chkPDRAMQ14 = _widg.make_check_button()

        # CSCI-level Yes/No from WS3B (1 question)
        self.chkPDRSTQ1 = _widg.make_check_button()

        # CSCI-level Yes/No from WS4B (14 questions)
        # CSCI-level quantity from WS4B (10 questions)
        self.chkPDRQCQ1 = _widg.make_check_button()
        self.chkPDRQCQ2 = _widg.make_check_button()
        self.chkPDRQCQ5 = _widg.make_check_button()
        self.chkPDRQCQ6 = _widg.make_check_button()
        self.chkPDRQCQ13 = _widg.make_check_button()
        self.chkPDRQCQ14 = _widg.make_check_button()
        self.chkPDRQCQ17 = _widg.make_check_button()
        self.chkPDRQCQ18 = _widg.make_check_button()
        self.chkPDRQCQ19 = _widg.make_check_button()
        self.chkPDRQCQ20 = _widg.make_check_button()
        self.chkPDRQCQ21 = _widg.make_check_button()
        self.chkPDRQCQ22 = _widg.make_check_button()
        self.chkPDRQCQ23 = _widg.make_check_button()
        self.chkPDRQCQ24 = _widg.make_check_button()

        self.txtPDRQCQ3 = _widg.make_entry(width=50)
        self.txtPDRQCQ4 = _widg.make_entry(width=50)
        self.txtPDRQCQ7 = _widg.make_entry(width=50)
        self.txtPDRQCQ8 = _widg.make_entry(width=50)
        self.txtPDRQCQ9 = _widg.make_entry(width=50)
        self.txtPDRQCQ10 = _widg.make_entry(width=50)
        self.txtPDRQCQ11 = _widg.make_entry(width=50)
        self.txtPDRQCQ12 = _widg.make_entry(width=50)
        self.txtPDRQCQ15 = _widg.make_entry(width=50)
        self.txtPDRQCQ16 = _widg.make_entry(width=50)

    def create_risk_analysis_page(self, notebook):
        """
        Method to create the development environment risk analysis page and add
        it to the risk analysis gtk.Notebook().

        :param gtk.Notebook notebook: the gtk.Notebook() instance that will
                                      hold the development environment analysis
                                      questions.
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._software_model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        # CSCI-level Yes/No from WS2B (14 questions)
        self.chkPDRAMQ1 = Widgets.make_check_button()
        self.chkPDRAMQ2 = Widgets.make_check_button()
        self.chkPDRAMQ3 = Widgets.make_check_button()
        self.chkPDRAMQ4 = Widgets.make_check_button()
        self.chkPDRAMQ5 = Widgets.make_check_button()
        self.chkPDRAMQ6 = Widgets.make_check_button()
        self.chkPDRAMQ7 = Widgets.make_check_button()
        self.chkPDRAMQ8 = Widgets.make_check_button()
        self.chkPDRAMQ9 = Widgets.make_check_button()
        self.chkPDRAMQ10 = Widgets.make_check_button()
        self.chkPDRAMQ11 = Widgets.make_check_button()
        self.chkPDRAMQ12 = Widgets.make_check_button()
        self.chkPDRAMQ13 = Widgets.make_check_button()
        self.chkPDRAMQ14 = Widgets.make_check_button()

        # CSCI-level Yes/No from WS3B (1 question)
        self.chkPDRSTQ1 = Widgets.make_check_button()

        # CSCI-level Yes/No from WS4B (14 questions)
        # CSCI-level quantity from WS4B (10 questions)
        self.chkPDRQCQ1 = Widgets.make_check_button()
        self.chkPDRQCQ2 = Widgets.make_check_button()
        self.chkPDRQCQ5 = Widgets.make_check_button()
        self.chkPDRQCQ6 = Widgets.make_check_button()
        self.chkPDRQCQ13 = Widgets.make_check_button()
        self.chkPDRQCQ14 = Widgets.make_check_button()
        self.chkPDRQCQ17 = Widgets.make_check_button()
        self.chkPDRQCQ18 = Widgets.make_check_button()
        self.chkPDRQCQ19 = Widgets.make_check_button()
        self.chkPDRQCQ20 = Widgets.make_check_button()
        self.chkPDRQCQ21 = Widgets.make_check_button()
        self.chkPDRQCQ22 = Widgets.make_check_button()
        self.chkPDRQCQ23 = Widgets.make_check_button()
        self.chkPDRQCQ24 = Widgets.make_check_button()

        self.txtPDRQCQ3 = Widgets.make_entry(width=50)
        self.txtPDRQCQ4 = Widgets.make_entry(width=50)
        self.txtPDRQCQ7 = Widgets.make_entry(width=50)
        self.txtPDRQCQ8 = Widgets.make_entry(width=50)
        self.txtPDRQCQ9 = Widgets.make_entry(width=50)
        self.txtPDRQCQ10 = Widgets.make_entry(width=50)
        self.txtPDRQCQ11 = Widgets.make_entry(width=50)
        self.txtPDRQCQ12 = Widgets.make_entry(width=50)
        self.txtPDRQCQ15 = Widgets.make_entry(width=50)
        self.txtPDRQCQ16 = Widgets.make_entry(width=50)

        # Connect the gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.chkPDRAMQ1.connect('toggled', self._on_toggled, 0))
        self._lst_handler_id.append(
            self.chkPDRAMQ2.connect('toggled', self._on_toggled, 1))
        self._lst_handler_id.append(
            self.chkPDRAMQ3.connect('toggled', self._on_toggled, 2))
        self._lst_handler_id.append(
            self.chkPDRAMQ4.connect('toggled', self._on_toggled, 3))
        self._lst_handler_id.append(
            self.chkPDRAMQ5.connect('toggled', self._on_toggled, 4))
        self._lst_handler_id.append(
            self.chkPDRAMQ6.connect('toggled', self._on_toggled, 5))
        self._lst_handler_id.append(
            self.chkPDRAMQ7.connect('toggled', self._on_toggled, 6))
        self._lst_handler_id.append(
            self.chkPDRAMQ8.connect('toggled', self._on_toggled, 7))
        self._lst_handler_id.append(
            self.chkPDRAMQ9.connect('toggled', self._on_toggled, 8))
        self._lst_handler_id.append(
            self.chkPDRAMQ10.connect('toggled', self._on_toggled, 9))
        self._lst_handler_id.append(
            self.chkPDRAMQ11.connect('toggled', self._on_toggled, 10))
        self._lst_handler_id.append(
            self.chkPDRAMQ12.connect('toggled', self._on_toggled, 11))
        self._lst_handler_id.append(
            self.chkPDRAMQ13.connect('toggled', self._on_toggled, 12))
        self._lst_handler_id.append(
            self.chkPDRAMQ14.connect('toggled', self._on_toggled, 13))
        self._lst_handler_id.append(
            self.chkPDRSTQ1.connect('toggled', self._on_toggled, 14))
        self._lst_handler_id.append(
            self.chkPDRQCQ1.connect('toggled', self._on_toggled, 15))
        self._lst_handler_id.append(
            self.chkPDRQCQ2.connect('toggled', self._on_toggled, 16))
        self._lst_handler_id.append(
            self.txtPDRQCQ3.connect('focus-out-event', self._on_focus_out, 17))
        self._lst_handler_id.append(
            self.txtPDRQCQ4.connect('focus-out-event', self._on_focus_out, 18))
        self._lst_handler_id.append(
            self.chkPDRQCQ5.connect('toggled', self._on_toggled, 19))
        self._lst_handler_id.append(
            self.chkPDRQCQ6.connect('toggled', self._on_toggled, 20))
        self._lst_handler_id.append(
            self.txtPDRQCQ7.connect('focus-out-event', self._on_focus_out, 21))
        self._lst_handler_id.append(
            self.txtPDRQCQ8.connect('focus-out-event', self._on_focus_out, 22))
        self._lst_handler_id.append(
            self.txtPDRQCQ9.connect('focus-out-event', self._on_focus_out, 23))
        self._lst_handler_id.append(
            self.txtPDRQCQ10.connect('focus-out-event',
                                     self._on_focus_out, 24))
        self._lst_handler_id.append(
            self.txtPDRQCQ11.connect('focus-out-event',
                                     self._on_focus_out, 25))
        self._lst_handler_id.append(
            self.txtPDRQCQ12.connect('focus-out-event',
                                     self._on_focus_out, 26))
        self._lst_handler_id.append(
            self.chkPDRQCQ13.connect('toggled', self._on_toggled, 27))
        self._lst_handler_id.append(
            self.chkPDRQCQ14.connect('toggled', self._on_toggled, 28))
        self._lst_handler_id.append(
            self.txtPDRQCQ15.connect('focus-out-event',
                                     self._on_focus_out, 29))
        self._lst_handler_id.append(
            self.txtPDRQCQ16.connect('focus-out-event',
                                     self._on_focus_out, 30))
        self._lst_handler_id.append(
            self.chkPDRQCQ17.connect('toggled', self._on_toggled, 31))
        self._lst_handler_id.append(
            self.chkPDRQCQ18.connect('toggled', self._on_toggled, 32))
        self._lst_handler_id.append(
            self.chkPDRQCQ19.connect('toggled', self._on_toggled, 33))
        self._lst_handler_id.append(
            self.chkPDRQCQ20.connect('toggled', self._on_toggled, 34))
        self._lst_handler_id.append(
            self.chkPDRQCQ21.connect('toggled', self._on_toggled, 35))
        self._lst_handler_id.append(
            self.chkPDRQCQ22.connect('toggled', self._on_toggled, 36))
        self._lst_handler_id.append(
            self.chkPDRQCQ23.connect('toggled', self._on_toggled, 37))
        self._lst_handler_id.append(
            self.chkPDRQCQ24.connect('toggled', self._on_toggled, 38))

    def create_risk_analysis_page(self, notebook):
        """
        Method to create the Preliminary Design Review risk analysis page and
        add it to the risk analysis gtk.Notebook().

        :param gtk.Notebook notebook: the gtk.Notebook() instance that will
                                      hold the PDR risk analysis questions.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the anomaly management risk pane.
        _fixed1 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed1)

<<<<<<< HEAD
        _frame = _widg.make_frame(label=_(u"Anomaly Management"))
=======
        _frame = Widgets.make_frame(label=_(u"Anomaly Management"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack1(_frame, resize=True, shrink=True)

        # Create the software quality control risk pane.
        _fixed2 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed2)

<<<<<<< HEAD
        _frame = _widg.make_frame(label=_(u"Software Quality Control"))
=======
        _frame = Widgets.make_frame(label=_(u"Software Quality Control"))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack2(_frame, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _labels = [_(u" 1. There are provisions for recovery from all "
                     u"computational errors."),
                   _(u" 2. There are provisions for recovery from all "
                     u"detected hardware faults (e.g., arithmetic faults, "
                     u"\npower failure, clock interrupt)."),
                   _(u" 3. There are provisions for recovery from all I/O "
                     u"device errors."),
                   _(u" 4. There are provisions for recovery from all "
                     u"communication transmission errors."),
                   _(u" 5. Error checking information (e.g., checksum, parity "
                     u"bit) is computed and transmitted with all messages."),
                   _(u" 6. Error checking information is computed and "
                     u"compared with all message receptions."),
                   _(u" 7. Transmission retries are limited for all "
                     u"transmissions."),
                   _(u" 8. There are provisions for recovery from all "
                     u"failures to communicate with other nodes or other "
                     u"systems."),
                   _(u" 9. There are provisions to periodically check all "
                     u"adjacent nodes or operating systems for operational "
                     u"status."),
                   _(u"10. There are provisions for alternate routing of "
                     u"messages."),
                   _(u"11. Communication paths exist to all remaining "
                     u"nodes/links in the event of a failure of one "
                     u"node/link."),
                   _(u"12. The integrity of all data values is maintained "
                     u"following the occurence of anomalous conditions."),
                   _(u"13. All disconnected nodes can rejoin the network "
                     u"after recovery, such that the processing functions "
                     u"\nof the system are not interrupted."),
                   _(u"14. All critical data in the module is replicated "
                     u"at two or more distinct nodes")]
<<<<<<< HEAD
        (_x_pos, _y_pos1) = _widg.make_labels(_labels, _fixed1,
                                              5, 5, wrap=False)
=======
        (_x_pos,
         _y_pos1) = Widgets.make_labels(_labels, _fixed1, 5, 5, wrap=False)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        _labels = [_(u" 1. There is a table tracing all the top-level CSC "
                     u"allocated requirements to the parent CSCI "
                     u"specification."),
                   _(u" 2. The numerical techniques used in implementing "
                     u"applicable functions provide enough precision to "
                     u"support\naccuracy objectives."),
                   _(u" 3. All processes and functions are partitioned to be "
                     u"logically complete and self-contained so as to "
                     u"minimize\ninterface complexity."),
                   _(u" 4. Estimated process time typically spent executing "
                     u"the entire module:"),
                   _(u" 5. Estimated process time typically spent in "
                     u"execution of hardware and device interface protocol:"),
                   _(u" 6. The executive software performs testing of its "
                     u"own operation and of the communication links, "
                     u"memory\ndevices, and peripheral devices."),
                   _(u" 7. All inputs, processing, and outputs are clearly "
                     u"and precisely defined."),
                   _(u" 8. Number of data references that are defined:"),
                   _(u" 9. Number of identified data references that are "
                     u"documented with regard to source, meaning, and "
                     u"format:"),
                   _(u"10. Number of data items that are defined (i.e., "
                     u"documented with regard to source, meaning, and "
                     u"format):"),
                   _(u"11. Number of data items that are referenced:"),
                   _(u"12. Number of data references that are identified:"),
                   _(u"13. Number of identified data references that are "
                     u"computed or obtained from an external source\n"
                     u"(e.g., referencing global data with preassigned "
                     u"values, input parameters with preassigned values):"),
                   _(u"14. Number of software discrepancy reports have been "
                     u"recorded, to date:"),
                   _(u"15. Number of software discrepancy reports have been "
                     u"closed, to date:"),
                   _(u"16. All functions of this module been allocated to "
                     u"top-level module."),
                   _(u"17. All conditions and alternative processing options "
                     u"are defined for each decision point."),
                   _(u"18. Design representations are in the formats of the "
                     u"established standard."),
                   _(u"19. All references to the same top-level module use a "
                     u"single, unique name."),
                   _(u"20. All data representation complies with the "
                     u"established standard."),
                   _(u"21. The naming of all data complies with the "
                     u"established standard."),
                   _(u"22. The definition and use of all global variables is "
                     u"in accordange with the established standard."),
                   _(u"23. There are procedures for establishing consistency"
                     u"and concurrency of multiple copies of the\nsame "
                     u"software or database version."),
                   _(u"24. There are procedures for verifying the consistency "
                     u"and concurrency of multiples copies of the\nsame "
                     u"software or database version."),
                   _(u"25. All references to the same data use a single, "
                     u"unique name.")]
<<<<<<< HEAD
        (_x_pos2, _y_pos2) = _widg.make_labels(_labels, _fixed2,
                                               5, 5, wrap=False)
=======
        (_x_pos2,
         _y_pos2) = Widgets.make_labels(_labels, _fixed2, 5, 5, wrap=False)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _x_pos = max(_x_pos, _x_pos2) + 125

        # Place the anomaly management widgets.
        _fixed1.put(self.chkPDRAMQ1, _x_pos, _y_pos1[0])
        _fixed1.put(self.chkPDRAMQ2, _x_pos, _y_pos1[1])
        _fixed1.put(self.chkPDRAMQ3, _x_pos, _y_pos1[2])
        _fixed1.put(self.chkPDRAMQ4, _x_pos, _y_pos1[3])
        _fixed1.put(self.chkPDRAMQ5, _x_pos, _y_pos1[4])
        _fixed1.put(self.chkPDRAMQ6, _x_pos, _y_pos1[5])
        _fixed1.put(self.chkPDRAMQ7, _x_pos, _y_pos1[6])
        _fixed1.put(self.chkPDRAMQ8, _x_pos, _y_pos1[7])
        _fixed1.put(self.chkPDRAMQ9, _x_pos, _y_pos1[8])
        _fixed1.put(self.chkPDRAMQ10, _x_pos, _y_pos1[9])
        _fixed1.put(self.chkPDRAMQ11, _x_pos, _y_pos1[10])
        _fixed1.put(self.chkPDRAMQ12, _x_pos, _y_pos1[11])
        _fixed1.put(self.chkPDRAMQ13, _x_pos, _y_pos1[12])
        _fixed1.put(self.chkPDRAMQ14, _x_pos, _y_pos1[13])

        # Place the quality control widgets.
        _fixed2.put(self.chkPDRSTQ1, _x_pos, _y_pos2[0])
        _fixed2.put(self.chkPDRQCQ1, _x_pos, _y_pos2[1])
        _fixed2.put(self.chkPDRQCQ2, _x_pos, _y_pos2[2])
        _fixed2.put(self.txtPDRQCQ3, _x_pos, _y_pos2[3])
        _fixed2.put(self.txtPDRQCQ4, _x_pos, _y_pos2[4])
        _fixed2.put(self.chkPDRQCQ5, _x_pos, _y_pos2[5])
        _fixed2.put(self.chkPDRQCQ6, _x_pos, _y_pos2[6])
        _fixed2.put(self.txtPDRQCQ7, _x_pos, _y_pos2[7])
        _fixed2.put(self.txtPDRQCQ8, _x_pos, _y_pos2[8])
        _fixed2.put(self.txtPDRQCQ9, _x_pos, _y_pos2[9])
        _fixed2.put(self.txtPDRQCQ10, _x_pos, _y_pos2[10])
        _fixed2.put(self.txtPDRQCQ11, _x_pos, _y_pos2[11])
        _fixed2.put(self.txtPDRQCQ12, _x_pos, _y_pos2[12])
        _fixed2.put(self.chkPDRQCQ13, _x_pos, _y_pos2[13])
        _fixed2.put(self.chkPDRQCQ14, _x_pos, _y_pos2[14])
        _fixed2.put(self.txtPDRQCQ15, _x_pos, _y_pos2[15])
        _fixed2.put(self.txtPDRQCQ16, _x_pos, _y_pos2[16])
        _fixed2.put(self.chkPDRQCQ17, _x_pos, _y_pos2[17])
        _fixed2.put(self.chkPDRQCQ18, _x_pos, _y_pos2[18])
        _fixed2.put(self.chkPDRQCQ19, _x_pos, _y_pos2[19])
        _fixed2.put(self.chkPDRQCQ20, _x_pos, _y_pos2[20])
        _fixed2.put(self.chkPDRQCQ21, _x_pos, _y_pos2[21])
        _fixed2.put(self.chkPDRQCQ22, _x_pos, _y_pos2[22])
        _fixed2.put(self.chkPDRQCQ23, _x_pos, _y_pos2[23])
        _fixed2.put(self.chkPDRQCQ24, _x_pos, _y_pos2[24])

<<<<<<< HEAD
        # Connect the anomaly management widgets to callback methods.
        self._lst_handler_id.append(
            self.chkPDRAMQ1.connect('toggled', self._on_toggled, 0))
        self._lst_handler_id.append(
            self.chkPDRAMQ2.connect('toggled', self._on_toggled, 1))
        self._lst_handler_id.append(
            self.chkPDRAMQ3.connect('toggled', self._on_toggled, 2))
        self._lst_handler_id.append(
            self.chkPDRAMQ4.connect('toggled', self._on_toggled, 3))
        self._lst_handler_id.append(
            self.chkPDRAMQ5.connect('toggled', self._on_toggled, 4))
        self._lst_handler_id.append(
            self.chkPDRAMQ6.connect('toggled', self._on_toggled, 5))
        self._lst_handler_id.append(
            self.chkPDRAMQ7.connect('toggled', self._on_toggled, 6))
        self._lst_handler_id.append(
            self.chkPDRAMQ8.connect('toggled', self._on_toggled, 7))
        self._lst_handler_id.append(
            self.chkPDRAMQ9.connect('toggled', self._on_toggled, 8))
        self._lst_handler_id.append(
            self.chkPDRAMQ10.connect('toggled', self._on_toggled, 9))
        self._lst_handler_id.append(
            self.chkPDRAMQ11.connect('toggled', self._on_toggled, 10))
        self._lst_handler_id.append(
            self.chkPDRAMQ12.connect('toggled', self._on_toggled, 11))
        self._lst_handler_id.append(
            self.chkPDRAMQ13.connect('toggled', self._on_toggled, 12))
        self._lst_handler_id.append(
            self.chkPDRAMQ14.connect('toggled', self._on_toggled, 13))

        # Connect the quality control widgets to callback methods.
        self._lst_handler_id.append(
            self.chkPDRSTQ1.connect('toggled', self._on_toggled, 14))
        self._lst_handler_id.append(
            self.chkPDRQCQ1.connect('toggled', self._on_toggled, 15))
        self._lst_handler_id.append(
            self.chkPDRQCQ2.connect('toggled', self._on_toggled, 16))
        self._lst_handler_id.append(
            self.txtPDRQCQ3.connect('focus-out-event', self._on_focus_out, 17))
        self._lst_handler_id.append(
            self.txtPDRQCQ4.connect('focus-out-event', self._on_focus_out, 18))
        self._lst_handler_id.append(
            self.chkPDRQCQ5.connect('toggled', self._on_toggled, 19))
        self._lst_handler_id.append(
            self.chkPDRQCQ6.connect('toggled', self._on_toggled, 20))
        self._lst_handler_id.append(
            self.txtPDRQCQ7.connect('focus-out-event', self._on_focus_out, 21))
        self._lst_handler_id.append(
            self.txtPDRQCQ8.connect('focus-out-event', self._on_focus_out, 22))
        self._lst_handler_id.append(
            self.txtPDRQCQ9.connect('focus-out-event', self._on_focus_out, 23))
        self._lst_handler_id.append(
            self.txtPDRQCQ10.connect('focus-out-event',
                                     self._on_focus_out, 24))
        self._lst_handler_id.append(
            self.txtPDRQCQ11.connect('focus-out-event',
                                     self._on_focus_out, 25))
        self._lst_handler_id.append(
            self.txtPDRQCQ12.connect('focus-out-event',
                                     self._on_focus_out, 26))
        self._lst_handler_id.append(
            self.chkPDRQCQ13.connect('toggled', self._on_toggled, 27))
        self._lst_handler_id.append(
            self.chkPDRQCQ14.connect('toggled', self._on_toggled, 28))
        self._lst_handler_id.append(
            self.txtPDRQCQ15.connect('focus-out-event',
                                     self._on_focus_out, 29))
        self._lst_handler_id.append(
            self.txtPDRQCQ16.connect('focus-out-event',
                                     self._on_focus_out, 30))
        self._lst_handler_id.append(
            self.chkPDRQCQ17.connect('toggled', self._on_toggled, 31))
        self._lst_handler_id.append(
            self.chkPDRQCQ18.connect('toggled', self._on_toggled, 32))
        self._lst_handler_id.append(
            self.chkPDRQCQ19.connect('toggled', self._on_toggled, 33))
        self._lst_handler_id.append(
            self.chkPDRQCQ20.connect('toggled', self._on_toggled, 34))
        self._lst_handler_id.append(
            self.chkPDRQCQ21.connect('toggled', self._on_toggled, 35))
        self._lst_handler_id.append(
            self.chkPDRQCQ22.connect('toggled', self._on_toggled, 36))
        self._lst_handler_id.append(
            self.chkPDRQCQ23.connect('toggled', self._on_toggled, 37))
        self._lst_handler_id.append(
            self.chkPDRQCQ24.connect('toggled', self._on_toggled, 38))

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _("Preliminary\nDesign\nReview") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_angle(0)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows assessment of the reliability risk "
                                  u"at the preliminary design review."))
        notebook.insert_page(self, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Preliminary Design Review Risk Analysis answers.

<<<<<<< HEAD
        :param `rtk.software.Software` model: the Software data model to load
                                              the gtk.ToggleButton() from.
=======
        :param model: the :py:class:`rtk.software.Software.Model` data model to
                      load the gtk.ToggleButton() from.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = model

        self.chkPDRAMQ1.set_active(model.lst_anomaly_mgmt[1][0])
        self.chkPDRAMQ2.set_active(model.lst_anomaly_mgmt[1][1])
        self.chkPDRAMQ3.set_active(model.lst_anomaly_mgmt[1][2])
        self.chkPDRAMQ4.set_active(model.lst_anomaly_mgmt[1][3])
        self.chkPDRAMQ5.set_active(model.lst_anomaly_mgmt[1][4])
        self.chkPDRAMQ6.set_active(model.lst_anomaly_mgmt[1][5])
        self.chkPDRAMQ7.set_active(model.lst_anomaly_mgmt[1][6])
        self.chkPDRAMQ8.set_active(model.lst_anomaly_mgmt[1][7])
        self.chkPDRAMQ9.set_active(model.lst_anomaly_mgmt[1][8])
        self.chkPDRAMQ10.set_active(model.lst_anomaly_mgmt[1][9])
        self.chkPDRAMQ11.set_active(model.lst_anomaly_mgmt[1][10])
        self.chkPDRAMQ12.set_active(model.lst_anomaly_mgmt[1][11])
        self.chkPDRAMQ13.set_active(model.lst_anomaly_mgmt[1][12])
        self.chkPDRAMQ14.set_active(model.lst_anomaly_mgmt[1][13])

        self.chkPDRSTQ1.set_active(model.lst_traceability[1][0])

        self.chkPDRQCQ1.set_active(model.lst_sftw_quality[1][0])
        self.chkPDRQCQ2.set_active(model.lst_sftw_quality[1][1])
        self.txtPDRQCQ3.set_text(str(model.lst_sftw_quality[1][2]))
        self.txtPDRQCQ4.set_text(str(model.lst_sftw_quality[1][3]))
        self.chkPDRQCQ5.set_active(model.lst_sftw_quality[1][4])
        self.chkPDRQCQ6.set_active(model.lst_sftw_quality[1][5])
        self.txtPDRQCQ7.set_text(str(model.lst_sftw_quality[1][6]))
        self.txtPDRQCQ8.set_text(str(model.lst_sftw_quality[1][7]))
        self.txtPDRQCQ9.set_text(str(model.lst_sftw_quality[1][8]))
        self.txtPDRQCQ10.set_text(str(model.lst_sftw_quality[1][9]))
        self.txtPDRQCQ11.set_text(str(model.lst_sftw_quality[1][10]))
        self.txtPDRQCQ12.set_text(str(model.lst_sftw_quality[1][11]))
        self.chkPDRQCQ13.set_active(model.lst_sftw_quality[1][12])
        self.chkPDRQCQ14.set_active(model.lst_sftw_quality[1][13])
        self.txtPDRQCQ15.set_text(str(model.lst_sftw_quality[1][14]))
        self.txtPDRQCQ16.set_text(str(model.lst_sftw_quality[1][15]))
        self.chkPDRQCQ17.set_active(model.lst_sftw_quality[1][16])
        self.chkPDRQCQ18.set_active(model.lst_sftw_quality[1][17])
        self.chkPDRQCQ19.set_active(model.lst_sftw_quality[1][18])
        self.chkPDRQCQ20.set_active(model.lst_sftw_quality[1][19])
        self.chkPDRQCQ21.set_active(model.lst_sftw_quality[1][20])
        self.chkPDRQCQ22.set_active(model.lst_sftw_quality[1][21])
        self.chkPDRQCQ23.set_active(model.lst_sftw_quality[1][22])
        self.chkPDRQCQ24.set_active(model.lst_sftw_quality[1][23])

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

        self._software_model.lst_sftw_quality[1][index - 15] = int(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_toggled(self, check, index):
        """
<<<<<<< HEAD
        Callback function for gtk.CheckButton() 'toggled' signals.
=======
        Callback method for gtk.CheckButton() 'toggled' signals.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the index of the Development Environment question
                          associated with the gtk.CheckButton() that was
                          toggled.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        check.handler_block(self._lst_handler_id[index])

        if index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
            self._software_model.lst_anomaly_mgmt[1][index] = int(check.get_active())
        elif index == 14:
            self._software_model.lst_traceability[1][index - 14] = int(check.get_active())
        elif index in [15, 16, 19, 20, 27, 28, 31, 32, 33, 34, 35, 36, 37, 38]:
            self._software_model.lst_sftw_quality[1][index - 15] = int(check.get_active())

        check.handler_unblock(self._lst_handler_id[index])

        return False
