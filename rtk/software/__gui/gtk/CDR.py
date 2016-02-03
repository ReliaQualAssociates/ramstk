#!/usr/bin/env python
"""
#############################################################################
Software Package Risk Analysis Critical Design Review Specific Work Book View
#############################################################################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.gui.gtk.CDR.py is part of The RTK Project
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
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class CSCIRiskAnalysis(gtk.VPaned):
    """
    The Work Book view for analyzing and displaying the risk at the Critical
    Design Review phase.  The attributes of a CDR Work Book view are:

    :ivar _lst_handler_id: default value: []
    """

    def __init__(self):
        """
        Creates an input vertical paned for the CDR risk analysis questions.
        """

        gtk.VPaned.__init__(self)

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._software_model = None

        self.chkCDRAMQ3 = _widg.make_check_button()
        self.chkCDRAMQ4 = _widg.make_check_button()
        self.chkCDRAMQ5 = _widg.make_check_button()
        self.chkCDRAMQ6 = _widg.make_check_button()
        self.chkCDRAMQ7 = _widg.make_check_button()
        self.chkCDRAMQ9 = _widg.make_check_button()
        self.chkCDRAMQ10 = _widg.make_check_button()
        self.chkCDRAMQ11 = _widg.make_check_button()
        self.chkCDRSTQ1 = _widg.make_check_button()
        self.chkCDRSTQ2 = _widg.make_check_button()

        self.txtCDRAMQ1 = _widg.make_entry(width=50)
        self.txtCDRAMQ2 = _widg.make_entry(width=50)
        self.txtCDRAMQ8 = _widg.make_entry(width=50)
        self.txtCDRQCQ1 = _widg.make_entry(width=50)
        self.txtCDRQCQ2 = _widg.make_entry(width=50)
        self.txtCDRQCQ3 = _widg.make_entry(width=50)
        self.txtCDRQCQ4 = _widg.make_entry(width=50)
        self.txtCDRQCQ5 = _widg.make_entry(width=50)
        self.txtCDRQCQ6 = _widg.make_entry(width=50)
        self.txtCDRQCQ7 = _widg.make_entry(width=50)
        self.txtCDRQCQ8 = _widg.make_entry(width=50)
        self.txtCDRQCQ9 = _widg.make_entry(width=50)
        self.txtCDRQCQ10 = _widg.make_entry(width=50)
        self.txtCDRQCQ11 = _widg.make_entry(width=50)
        self.txtCDRQCQ12 = _widg.make_entry(width=50)
        self.txtCDRQCQ13 = _widg.make_entry(width=50)
        self.txtCDRQCQ14 = _widg.make_entry(width=50)
        self.txtCDRQCQ15 = _widg.make_entry(width=50)
        self.txtCDRQCQ16 = _widg.make_entry(width=50)
        self.txtCDRQCQ17 = _widg.make_entry(width=50)
        self.txtCDRQCQ18 = _widg.make_entry(width=50)
        self.txtCDRQCQ19 = _widg.make_entry(width=50)
        self.txtCDRQCQ20 = _widg.make_entry(width=50)
        self.txtCDRQCQ21 = _widg.make_entry(width=50)
        self.txtCDRQCQ22 = _widg.make_entry(width=50)
        self.txtCDRQCQ23 = _widg.make_entry(width=50)
        self.txtCDRQCQ24 = _widg.make_entry(width=50)

    def create_risk_analysis_page(self, notebook):
        """
        Method to create the CDR risk analysis page and add it to the risk
        analysis gtk.Notebook().

        :param gtk.Notebook notebook: the gtk.Notebook() instance that will
                                      hold the development environment analysis
                                      questions.
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the module-level containers and include them in the page
        # by default.
        _fxdcsciam = gtk.Fixed()
        _fxdcsciqc = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdcsciam)

        _frame = _widg.make_frame(_(u"Software Module Anomaly Management"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack1(_frame, resize=True, shrink=True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdcsciqc)

        _frame = _widg.make_frame(_(u"Software Module Quality Control"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack2(_frame, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the anomaly management labels for CSCI.
        _labels = [_(u" 1. Number of units in this module:"),
                   _(u" 2. Number of units in this module, when an error "
                     u"condition is detected, in which resolution "
                     u"the error is not\ndetermined by the calling unit:"),
                   _(u" 3. The value of all external inputs with range "
                     u"specifications are checked with respect to the "
                     u"specified\nrange prior to use."),
                   _(u" 4. All external inputs are checked with respect "
                     u"to specified conflicting requests prior to use."),
                   _(u" 5. All external inputs are checked with respect "
                     u"to specified illegal combinations prior to use."),
                   _(u" 6. All external inputs are checked for "
                     u"reasonableness before processing begins."),
                   _(u" 7. All detected errors, with respect to "
                     u"applicable external inputs, are reported before "
                     u"processing begins."),
                   _(u" 8. Number of units in this module that do not "
                     u"perform a check to determine that all data is "
                     u"available before\nprocessing begins:"),
                   _(u" 9. Critical loop and multiple transfer index "
                     u"parameters (e.g., supporting a mission-critical "
                     u"system function)\nare checked for out-of-range "
                     u"values before use."),
                   _(u"10. All critical subscripts (e.g., supporting a "
                     u"mission-critical system function) are checked for "
                     u"out-of-range\nvalues before use."),
                   _(u"11. All critical output data (e.g., supporting a "
                     u"mission-critical system function) are checked for\n"
                     u"reasonable values prior to final outputting.")]
        (_x_pos, _y_pos1) = _widg.make_labels(_labels, _fxdcsciam,
                                              5, 5, wrap=False)

        # Create the software quality control labels for CSCI.
        _labels = [_(u" 1. The description of each software unit "
                     u"identifies all the requirements that the unit "
                     u"helps satisfy."),
                   _(u" 2. The decomposition of top-level modules into "
                     u"lower-level modules and software units is "
                     u"graphically depicted."),
                   _(u" 3. Estimated executable lines of source code in "
                     u"this module:"),
                   _(u" 4. Estimated executable lines of source code "
                     u"necessary to handle hardware and device interface "
                     u"protocol\nin this module:"),
                   _(u" 5. Number of units in this module that perform "
                     u"processing of hardware and/or device interface "
                     u"protocol:"),
                   _(u" 6. Estimated processing time typically spent "
                     u"executing this module:"),
                   _(u" 7. Estimated processing time typically spent in "
                     u"execution of hardware and device interface "
                     u"protocol in\nthis module:"),
                   _(u" 8. Number of units that clearly and precisely "
                     u"define all inputs, processing, and outputs:"),
                   _(u" 9. Data references identified in this module:"),
                   _(u"10. Identified data references that are documented "
                     u"with regard to source, meaning, and format in this "
                     u"module:"),
                   _(u"11. Data items that are defined (i.e., documented "
                     u"with regard to source, meaning, and format) in "
                     u"this module:"),
                   _(u"12. Data items are referenced in this module:"),
                   _(u"13. Data references identified in this module:"),
                   _(u"14. Identified data references that are computed "
                     u"or obtained from an external source\n(e.g., "
                     u"referencing global data with preassigned values, "
                     u"input parameters with preassigned values)\nin this "
                     u"module:"),
                   _(u"15. Number of units that define all conditions and "
                     u"alternative processing options for each decision "
                     u"point:"),
                   _(u"16. Number of units in which all parameters in the "
                     u"argument list are used:"),
                   _(u"17. Number of software discrepancy reports "
                     u"recorded, to date, for this module:"),
                   _(u"18. Number of software discrepancy reports "
                     u"recorded that have been closed, to date, for this "
                     u"module:"),
                   _(u"19. Number of units in which all design "
                     u"representations are in the formats of the "
                     u"established standard:"),
                   _(u"20. Number of units in which the inter-unit "
                     u"calling sequence protocol complies with the "
                     u"standard:"),
                   _(u"21. Number of units in which the I/O protocol and "
                     u"format complies with the established standard:"),
                   _(u"22. Number of units in which the handling of "
                     u"errors complies with the established standard:"),
                   _(u"23. Number of units in which all references to the "
                     u"unit use the same, unique name:"),
                   _(u"24. Number of units in which the naming of all "
                     u"data complies with the established standard:"),
                   _(u"25. Number of units in which is the definition and "
                     u"use of all global variables is in accordance with "
                     u"the\nestablished standard:"),
                   _(u"26. Number of units in which references to the "
                     u"same data use a single, unique name:")]
        (_x_pos2, _y_pos2) = _widg.make_labels(_labels, _fxdcsciqc,
                                               5, 5, wrap=False)
        _x_pos = max(_x_pos, _x_pos2) + 125

        # Place the anomaly management widgets for CSCI.
        _fxdcsciam.put(self.txtCDRAMQ1, _x_pos, _y_pos1[0])
        _fxdcsciam.put(self.txtCDRAMQ2, _x_pos, _y_pos1[1])
        _fxdcsciam.put(self.chkCDRAMQ3, _x_pos, _y_pos1[2])
        _fxdcsciam.put(self.chkCDRAMQ4, _x_pos, _y_pos1[3])
        _fxdcsciam.put(self.chkCDRAMQ5, _x_pos, _y_pos1[4])
        _fxdcsciam.put(self.chkCDRAMQ6, _x_pos, _y_pos1[5])
        _fxdcsciam.put(self.chkCDRAMQ7, _x_pos, _y_pos1[6])
        _fxdcsciam.put(self.txtCDRAMQ8, _x_pos, _y_pos1[7])
        _fxdcsciam.put(self.chkCDRAMQ9, _x_pos, _y_pos1[8])
        _fxdcsciam.put(self.chkCDRAMQ10, _x_pos, _y_pos1[9])
        _fxdcsciam.put(self.chkCDRAMQ11, _x_pos, _y_pos1[10])

        # Place the quality control widgets for CSCI.
        _fxdcsciqc.put(self.chkCDRSTQ1, _x_pos, _y_pos2[0])
        _fxdcsciqc.put(self.chkCDRSTQ2, _x_pos, _y_pos2[1])
        _fxdcsciqc.put(self.txtCDRQCQ1, _x_pos, _y_pos2[2])
        _fxdcsciqc.put(self.txtCDRQCQ2, _x_pos, _y_pos2[3])
        _fxdcsciqc.put(self.txtCDRQCQ3, _x_pos, _y_pos2[4])
        _fxdcsciqc.put(self.txtCDRQCQ4, _x_pos, _y_pos2[5])
        _fxdcsciqc.put(self.txtCDRQCQ5, _x_pos, _y_pos2[6])
        _fxdcsciqc.put(self.txtCDRQCQ6, _x_pos, _y_pos2[7])
        _fxdcsciqc.put(self.txtCDRQCQ7, _x_pos, _y_pos2[8])
        _fxdcsciqc.put(self.txtCDRQCQ8, _x_pos, _y_pos2[9])
        _fxdcsciqc.put(self.txtCDRQCQ9, _x_pos, _y_pos2[10])
        _fxdcsciqc.put(self.txtCDRQCQ10, _x_pos, _y_pos2[11])
        _fxdcsciqc.put(self.txtCDRQCQ11, _x_pos, _y_pos2[12])
        _fxdcsciqc.put(self.txtCDRQCQ12, _x_pos, _y_pos2[13])
        _fxdcsciqc.put(self.txtCDRQCQ13, _x_pos, _y_pos2[14])
        _fxdcsciqc.put(self.txtCDRQCQ14, _x_pos, _y_pos2[15])
        _fxdcsciqc.put(self.txtCDRQCQ15, _x_pos, _y_pos2[16])
        _fxdcsciqc.put(self.txtCDRQCQ16, _x_pos, _y_pos2[17])
        _fxdcsciqc.put(self.txtCDRQCQ17, _x_pos, _y_pos2[18])
        _fxdcsciqc.put(self.txtCDRQCQ18, _x_pos, _y_pos2[19])
        _fxdcsciqc.put(self.txtCDRQCQ19, _x_pos, _y_pos2[20])
        _fxdcsciqc.put(self.txtCDRQCQ20, _x_pos, _y_pos2[21])
        _fxdcsciqc.put(self.txtCDRQCQ21, _x_pos, _y_pos2[22])
        _fxdcsciqc.put(self.txtCDRQCQ22, _x_pos, _y_pos2[23])
        _fxdcsciqc.put(self.txtCDRQCQ23, _x_pos, _y_pos2[24])
        _fxdcsciqc.put(self.txtCDRQCQ24, _x_pos, _y_pos2[25])

        # Connect the anomaly management widgets to callback methods.
        self._lst_handler_id.append(
            self.txtCDRAMQ1.connect('focus-out-event', self._on_focus_out, 0))
        self._lst_handler_id.append(
            self.txtCDRAMQ2.connect('focus-out-event', self._on_focus_out, 1))
        self._lst_handler_id.append(
            self.chkCDRAMQ3.connect('toggled', self._on_toggled, 2))
        self._lst_handler_id.append(
            self.chkCDRAMQ4.connect('toggled', self._on_toggled, 3))
        self._lst_handler_id.append(
            self.chkCDRAMQ5.connect('toggled', self._on_toggled, 4))
        self._lst_handler_id.append(
            self.chkCDRAMQ6.connect('toggled', self._on_toggled, 5))
        self._lst_handler_id.append(
            self.chkCDRAMQ7.connect('toggled', self._on_toggled, 6))
        self._lst_handler_id.append(
            self.txtCDRAMQ8.connect('focus-out-event', self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.chkCDRAMQ9.connect('toggled', self._on_toggled, 8))
        self._lst_handler_id.append(
            self.chkCDRAMQ10.connect('toggled', self._on_toggled, 9))
        self._lst_handler_id.append(
            self.chkCDRAMQ11.connect('toggled', self._on_toggled, 10))

        # Connect the quality control widgets to callback methods.
        self._lst_handler_id.append(
            self.chkCDRSTQ1.connect('toggled', self._on_toggled, 11))
        self._lst_handler_id.append(
            self.chkCDRSTQ2.connect('toggled', self._on_toggled, 12))
        self._lst_handler_id.append(
            self.txtCDRQCQ1.connect('focus-out-event', self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtCDRQCQ2.connect('focus-out-event', self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtCDRQCQ3.connect('focus-out-event', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.txtCDRQCQ4.connect('focus-out-event', self._on_focus_out, 16))
        self._lst_handler_id.append(
            self.txtCDRQCQ5.connect('focus-out-event', self._on_focus_out, 17))
        self._lst_handler_id.append(
            self.txtCDRQCQ6.connect('focus-out-event', self._on_focus_out, 18))
        self._lst_handler_id.append(
            self.txtCDRQCQ7.connect('focus-out-event', self._on_focus_out, 19))
        self._lst_handler_id.append(
            self.txtCDRQCQ8.connect('focus-out-event', self._on_focus_out, 20))
        self._lst_handler_id.append(
            self.txtCDRQCQ9.connect('focus-out-event', self._on_focus_out, 21))
        self._lst_handler_id.append(
            self.txtCDRQCQ10.connect('focus-out-event',
                                     self._on_focus_out, 22))
        self._lst_handler_id.append(
            self.txtCDRQCQ11.connect('focus-out-event',
                                     self._on_focus_out, 23))
        self._lst_handler_id.append(
            self.txtCDRQCQ12.connect('focus-out-event',
                                     self._on_focus_out, 24))
        self._lst_handler_id.append(
            self.txtCDRQCQ13.connect('focus-out-event',
                                     self._on_focus_out, 25))
        self._lst_handler_id.append(
            self.txtCDRQCQ14.connect('focus-out-event',
                                     self._on_focus_out, 26))
        self._lst_handler_id.append(
            self.txtCDRQCQ15.connect('focus-out-event',
                                     self._on_focus_out, 27))
        self._lst_handler_id.append(
            self.txtCDRQCQ16.connect('focus-out-event',
                                     self._on_focus_out, 28))
        self._lst_handler_id.append(
            self.txtCDRQCQ17.connect('focus-out-event',
                                     self._on_focus_out, 29))
        self._lst_handler_id.append(
            self.txtCDRQCQ18.connect('focus-out-event',
                                     self._on_focus_out, 30))
        self._lst_handler_id.append(
            self.txtCDRQCQ19.connect('focus-out-event',
                                     self._on_focus_out, 31))
        self._lst_handler_id.append(
            self.txtCDRQCQ20.connect('focus-out-event',
                                     self._on_focus_out, 32))
        self._lst_handler_id.append(
            self.txtCDRQCQ21.connect('focus-out-event',
                                     self._on_focus_out, 33))
        self._lst_handler_id.append(
            self.txtCDRQCQ22.connect('focus-out-event',
                                     self._on_focus_out, 34))
        self._lst_handler_id.append(
            self.txtCDRQCQ23.connect('focus-out-event',
                                     self._on_focus_out, 35))
        self._lst_handler_id.append(
            self.txtCDRQCQ24.connect('focus-out-event',
                                     self._on_focus_out, 36))

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Critical\nDesign\nReview") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_angle(0)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows assessment of the reliability risk "
                                  u"for a CSCI at the critical design review "
                                  u"phase."))
        notebook.insert_page(self, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Critical Design Review Risk Analysis answers.

        :param `rtk.software.Software` model: the Software data model to load
                                              the gtk.ToggleButton() from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = model

        self.txtCDRAMQ1.set_text(str(model.lst_anomaly_mgmt[2][0]))
        self.txtCDRAMQ2.set_text(str(model.lst_anomaly_mgmt[2][1]))
        self.chkCDRAMQ3.set_active(model.lst_anomaly_mgmt[2][2])
        self.chkCDRAMQ4.set_active(model.lst_anomaly_mgmt[2][3])
        self.chkCDRAMQ5.set_active(model.lst_anomaly_mgmt[2][4])
        self.chkCDRAMQ6.set_active(model.lst_anomaly_mgmt[2][5])
        self.chkCDRAMQ7.set_active(model.lst_anomaly_mgmt[2][6])
        self.txtCDRAMQ8.set_text(str(model.lst_anomaly_mgmt[2][7]))
        self.chkCDRAMQ9.set_active(model.lst_anomaly_mgmt[2][8])
        self.chkCDRAMQ10.set_active(model.lst_anomaly_mgmt[2][9])
        self.chkCDRAMQ11.set_active(model.lst_anomaly_mgmt[2][10])

        self.chkCDRSTQ1.set_active(model.lst_traceability[2][0])
        self.chkCDRSTQ2.set_active(model.lst_traceability[2][1])

        self.txtCDRQCQ1.set_text(str(model.lst_sftw_quality[2][0]))
        self.txtCDRQCQ2.set_text(str(model.lst_sftw_quality[2][1]))
        self.txtCDRQCQ3.set_text(str(model.lst_sftw_quality[2][2]))
        self.txtCDRQCQ4.set_text(str(model.lst_sftw_quality[2][3]))
        self.txtCDRQCQ5.set_text(str(model.lst_sftw_quality[2][4]))
        self.txtCDRQCQ6.set_text(str(model.lst_sftw_quality[2][5]))
        self.txtCDRQCQ7.set_text(str(model.lst_sftw_quality[2][6]))
        self.txtCDRQCQ8.set_text(str(model.lst_sftw_quality[2][7]))
        self.txtCDRQCQ9.set_text(str(model.lst_sftw_quality[2][8]))
        self.txtCDRQCQ10.set_text(str(model.lst_sftw_quality[2][9]))
        self.txtCDRQCQ11.set_text(str(model.lst_sftw_quality[2][10]))
        self.txtCDRQCQ12.set_text(str(model.lst_sftw_quality[2][11]))
        self.txtCDRQCQ13.set_text(str(model.lst_sftw_quality[2][12]))
        self.txtCDRQCQ14.set_text(str(model.lst_sftw_quality[2][13]))
        self.txtCDRQCQ15.set_text(str(model.lst_sftw_quality[2][14]))
        self.txtCDRQCQ16.set_text(str(model.lst_sftw_quality[2][15]))
        self.txtCDRQCQ17.set_text(str(model.lst_sftw_quality[2][16]))
        self.txtCDRQCQ18.set_text(str(model.lst_sftw_quality[2][17]))
        self.txtCDRQCQ19.set_text(str(model.lst_sftw_quality[2][18]))
        self.txtCDRQCQ20.set_text(str(model.lst_sftw_quality[2][19]))
        self.txtCDRQCQ21.set_text(str(model.lst_sftw_quality[2][20]))
        self.txtCDRQCQ22.set_text(str(model.lst_sftw_quality[2][21]))
        self.txtCDRQCQ23.set_text(str(model.lst_sftw_quality[2][22]))
        self.txtCDRQCQ24.set_text(str(model.lst_sftw_quality[2][23]))

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

        if index in [0, 1, 7]:
            self._software_model.lst_anomaly_mgmt[2][index] = int(entry.get_text())
        elif index in [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                       27, 28, 29, 30, 31, 32, 33, 34, 35, 36]:
            self._software_model.lst_sftw_quality[2][index - 13] = int(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_toggled(self, check, index):
        """
        Callback function for gtk.CheckButton() 'toggled' signals.

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the index of the Development Environment question
                          associated with the gtk.CheckButton() that was
                          toggled.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        check.handler_block(self._lst_handler_id[index])

        if index in [2, 3, 4, 5, 6, 8, 9, 10]:
            self._software_model.lst_anomaly_mgmt[2][index] = int(check.get_active())
        elif index in [11, 12]:
            self._software_model.lst_traceability[2][index - 11] = int(check.get_active())

        check.handler_unblock(self._lst_handler_id[index])

        return False


class UnitRiskAnalysis(gtk.VPaned):
    """
    The Work Book view for analyzing and displaying the risk at the Critical
    Design Review phase for Units.  The attributes of a CDR Work Book view are:

    :ivar _lst_handler_id: default value: []
    """

    def __init__(self):
        """
        Creates an input vertical paned for the CDR risk analysis questions.
        """

        gtk.VPaned.__init__(self)

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._software_model = None

        self.chkCDRAMQ1 = _widg.make_check_button()
        self.chkCDRAMQ2 = _widg.make_check_button()
        self.chkCDRAMQ3 = _widg.make_check_button()
        self.chkCDRAMQ4 = _widg.make_check_button()
        self.chkCDRAMQ5 = _widg.make_check_button()
        self.chkCDRAMQ6 = _widg.make_check_button()
        self.chkCDRAMQ7 = _widg.make_check_button()
        self.chkCDRAMQ8 = _widg.make_check_button()
        self.chkCDRAMQ9 = _widg.make_check_button()
        self.chkCDRAMQ10 = _widg.make_check_button()
        self.chkCDRSTQ1 = _widg.make_check_button()
        self.chkCDRQCQ3 = _widg.make_check_button()
        self.chkCDRQCQ6 = _widg.make_check_button()
        self.chkCDRQCQ13 = _widg.make_check_button()
        self.chkCDRQCQ14 = _widg.make_check_button()
        self.chkCDRQCQ17 = _widg.make_check_button()
        self.chkCDRQCQ18 = _widg.make_check_button()
        self.chkCDRQCQ19 = _widg.make_check_button()
        self.chkCDRQCQ20 = _widg.make_check_button()
        self.chkCDRQCQ21 = _widg.make_check_button()
        self.chkCDRQCQ22 = _widg.make_check_button()
        self.chkCDRQCQ23 = _widg.make_check_button()
        self.chkCDRQCQ24 = _widg.make_check_button()

        self.txtCDRQCQ1 = _widg.make_entry(width=50)
        self.txtCDRQCQ2 = _widg.make_entry(width=50)
        self.txtCDRQCQ4 = _widg.make_entry(width=50)
        self.txtCDRQCQ5 = _widg.make_entry(width=50)
        self.txtCDRQCQ7 = _widg.make_entry(width=50)
        self.txtCDRQCQ8 = _widg.make_entry(width=50)
        self.txtCDRQCQ9 = _widg.make_entry(width=50)
        self.txtCDRQCQ10 = _widg.make_entry(width=50)
        self.txtCDRQCQ11 = _widg.make_entry(width=50)
        self.txtCDRQCQ12 = _widg.make_entry(width=50)
        self.txtCDRQCQ15 = _widg.make_entry(width=50)
        self.txtCDRQCQ16 = _widg.make_entry(width=50)

    def create_risk_analysis_page(self, notebook):
        """
        Method to create the CDR risk analysis page and add it to the risk
        analysis gtk.Notebook().

        :param gtk.Notebook notebook: the gtk.Notebook() instance that will
                                      hold the development environment analysis
                                      questions.
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build the unit-level containers.
        _fxdunitam = gtk.Fixed()
        _fxdunitqc = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdunitam)

        _frame = _widg.make_frame(_(u"Software Unit Anomaly Management"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack1(_frame, resize=True, shrink=True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdunitqc)

        _frame = _widg.make_frame(_(u"Software Unit Quality Control"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        self.pack2(_frame, resize=True, shrink=True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display risk analysis information.  #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the anomaly management labels for units.
        _labels = [_(u" 1. When an error condition is detected, the "
                     u"resolution of the error is not determined by this "
                     u"unit."),
                   _(u" 2. The values of all applicable external inputs "
                     u"with range specifications are checked with respect "
                     u"to specified range prior to use in this unit."),
                   _(u" 3. All applicable external inputs are checked "
                     u"with respect to specified conflicting requests "
                     u"prior to use in this unit."),
                   _(u" 4. All applicable external inputs are checked "
                     u"with respect to specified illegal combinations "
                     u"prior to use in this unit."),
                   _(u" 5. All applicable external inputs are checked for "
                     u"reasonableness before processing begins in this "
                     u"unit."),
                   _(u" 6. All detected errors, with respect to "
                     u"applicable external inputs, are reported before "
                     u"processing begins in this unit."),
                   _(u" 7. This unit does not perform a check to "
                     u"determine that all data is available before "
                     u"processing begins."),
                   _(u" 8. Critical loop and multiple transfer index "
                     u"parameters (e.g., supporting a mission-critical "
                     u"system function) are checked for out-of-range "
                     u"values before use in this unit."),
                   _(u" 9. All critical subscripts (e.g., supporting a "
                     u"mission-critical system function) are checked for "
                     u"out-of-range values before use in this unit."),
                   _(u"10. All critical output data (e.g., supporting a "
                     u"mission-critical system function) are checked for "
                     u"reasonable values prior to final outputting by "
                     u"this unit.")]
        (_x_pos, _y_pos1) = _widg.make_labels(_labels, _fxdunitam,
                                              5, 5, wrap=False)

        # Create the quality control labels for units.
        _labels = [_(u" 1. The description of this software unit "
                     u"identifies all the requirements that the unit "
                     u"helps satisfy."),
                   _(u" 2. Estimated executable lines of source code in "
                     u"this unit:"),
                   _(u" 3. Estimated executable lines of source code "
                     u"necessary to handle hardware and device interface "
                     u"protocol in this unit:"),
                   _(u" 4. This unit performs processing of hardware "
                     u"and/or device interface protocols."),
                   _(u" 5. Estimated processing time typically spent "
                     u"executing this unit:"),
                   _(u" 6. Estimated processing time typically spent in "
                     u"execution of hardware and device interface "
                     u"protocol in this unit:"),
                   _(u" 7. All inputs, processing, and outputs are "
                     u"clearly and precisely defined."),
                   _(u" 8. Data references identified in this unit:"),
                   _(u" 9. Identified data references that are documented "
                     u"with regard to source, meaning, and format in this "
                     u"unit:"),
                   _(u"10. Data items that are defined (i.e., documented "
                     u"with regard to source, meaning, and format) in "
                     u"this unit:"),
                   _(u"11. Data items are referenced in this unit:"),
                   _(u"12. Data references identified in this unit:"),
                   _(u"13. Identified data references that are computed "
                     u"or obtained from an external source (e.g., "
                     u"referencing global data with preassigned values, "
                     u"input parameters with preassigned values) in this "
                     u"unit:"),
                   _(u"14. All conditions and alternative processing "
                     u"options for each decision point are defined."),
                   _(u"15. All parameters in the argument list are used."),
                   _(u"16. Number of software discrepancy reports "
                     u"recorded, to date, for this unit:"),
                   _(u"17. Number of software discrepancy reports "
                     u"recorded that have been closed, to date, for this "
                     u"unit:"),
                   _(u"18. All design representations are in the formats "
                     u"of the established standard."),
                   _(u"19. The calling sequence protocol (between units) "
                     u"complies with the established standard."),
                   _(u"20. The I/O protocol and format complies with the "
                     u"established standard."),
                   _(u"21. The handling of errors complies with the "
                     u"established standard."),
                   _(u"22. All references to the unit use the same, "
                     u"unique name."),
                   _(u"23. The naming of all data complies with the "
                     u"established standard."),
                   _(u"24. The definition and use of all global variables "
                     u"is in accordance with the established standard."),
                   _(u"25. References to the same data use a single, "
                     u"unique name.")]
        (_x_pos2, _y_pos2) = _widg.make_labels(_labels, _fxdunitqc,
                                               5, 5, wrap=False)
        _x_pos = max(_x_pos, _x_pos2) + 125

        # Place the anomaly management widgets for units.
        _fxdunitam.put(self.chkCDRAMQ1, _x_pos, _y_pos1[0])
        _fxdunitam.put(self.chkCDRAMQ2, _x_pos, _y_pos1[1])
        _fxdunitam.put(self.chkCDRAMQ3, _x_pos, _y_pos1[2])
        _fxdunitam.put(self.chkCDRAMQ4, _x_pos, _y_pos1[3])
        _fxdunitam.put(self.chkCDRAMQ5, _x_pos, _y_pos1[4])
        _fxdunitam.put(self.chkCDRAMQ6, _x_pos, _y_pos1[5])
        _fxdunitam.put(self.chkCDRAMQ7, _x_pos, _y_pos1[6])
        _fxdunitam.put(self.chkCDRAMQ8, _x_pos, _y_pos1[7])
        _fxdunitam.put(self.chkCDRAMQ9, _x_pos, _y_pos1[8])
        _fxdunitam.put(self.chkCDRAMQ10, _x_pos, _y_pos1[9])

        # Place the quality control widgets for units.
        _fxdunitqc.put(self.chkCDRSTQ1, _x_pos, _y_pos2[0])
        _fxdunitqc.put(self.txtCDRQCQ1, _x_pos, _y_pos2[1])
        _fxdunitqc.put(self.txtCDRQCQ2, _x_pos, _y_pos2[2])
        _fxdunitqc.put(self.chkCDRQCQ3, _x_pos, _y_pos2[3])
        _fxdunitqc.put(self.txtCDRQCQ4, _x_pos, _y_pos2[4])
        _fxdunitqc.put(self.txtCDRQCQ5, _x_pos, _y_pos2[5])
        _fxdunitqc.put(self.chkCDRQCQ6, _x_pos, _y_pos2[6])
        _fxdunitqc.put(self.txtCDRQCQ7, _x_pos, _y_pos2[7])
        _fxdunitqc.put(self.txtCDRQCQ8, _x_pos, _y_pos2[8])
        _fxdunitqc.put(self.txtCDRQCQ9, _x_pos, _y_pos2[9])
        _fxdunitqc.put(self.txtCDRQCQ10, _x_pos, _y_pos2[10])
        _fxdunitqc.put(self.txtCDRQCQ11, _x_pos, _y_pos2[11])
        _fxdunitqc.put(self.txtCDRQCQ12, _x_pos, _y_pos2[12])
        _fxdunitqc.put(self.chkCDRQCQ13, _x_pos, _y_pos2[13])
        _fxdunitqc.put(self.chkCDRQCQ14, _x_pos, _y_pos2[14])
        _fxdunitqc.put(self.txtCDRQCQ15, _x_pos, _y_pos2[15])
        _fxdunitqc.put(self.txtCDRQCQ16, _x_pos, _y_pos2[16])
        _fxdunitqc.put(self.chkCDRQCQ17, _x_pos, _y_pos2[17])
        _fxdunitqc.put(self.chkCDRQCQ18, _x_pos, _y_pos2[18])
        _fxdunitqc.put(self.chkCDRQCQ19, _x_pos, _y_pos2[19])
        _fxdunitqc.put(self.chkCDRQCQ20, _x_pos, _y_pos2[20])
        _fxdunitqc.put(self.chkCDRQCQ21, _x_pos, _y_pos2[21])
        _fxdunitqc.put(self.chkCDRQCQ22, _x_pos, _y_pos2[22])
        _fxdunitqc.put(self.chkCDRQCQ23, _x_pos, _y_pos2[23])
        _fxdunitqc.put(self.chkCDRQCQ24, _x_pos, _y_pos2[24])

        # Connect the anomaly management widgets to callback methods.
        self._lst_handler_id.append(
            self.chkCDRAMQ1.connect('toggled', self._on_toggled, 0))
        self._lst_handler_id.append(
            self.chkCDRAMQ2.connect('toggled', self._on_toggled, 1))
        self._lst_handler_id.append(
            self.chkCDRAMQ3.connect('toggled', self._on_toggled, 2))
        self._lst_handler_id.append(
            self.chkCDRAMQ4.connect('toggled', self._on_toggled, 3))
        self._lst_handler_id.append(
            self.chkCDRAMQ5.connect('toggled', self._on_toggled, 4))
        self._lst_handler_id.append(
            self.chkCDRAMQ6.connect('toggled', self._on_toggled, 5))
        self._lst_handler_id.append(
            self.chkCDRAMQ7.connect('toggled', self._on_toggled, 6))
        self._lst_handler_id.append(
            self.chkCDRAMQ8.connect('toggled', self._on_toggled, 7))
        self._lst_handler_id.append(
            self.chkCDRAMQ9.connect('toggled', self._on_toggled, 8))
        self._lst_handler_id.append(
            self.chkCDRAMQ10.connect('toggled', self._on_toggled, 9))

        # Connect the quality control widgets to callback methods.
        self._lst_handler_id.append(
            self.chkCDRSTQ1.connect('toggled', self._on_toggled, 10))
        self._lst_handler_id.append(
            self.txtCDRQCQ1.connect('focus-out-event', self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtCDRQCQ2.connect('focus-out-event', self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.chkCDRQCQ3.connect('toggled', self._on_toggled, 13))
        self._lst_handler_id.append(
            self.txtCDRQCQ4.connect('focus-out-event', self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtCDRQCQ5.connect('focus-out-event', self._on_focus_out, 15))
        self._lst_handler_id.append(
            self.chkCDRQCQ6.connect('toggled', self._on_toggled, 16))
        self._lst_handler_id.append(
            self.txtCDRQCQ7.connect('focus-out-event', self._on_focus_out, 17))
        self._lst_handler_id.append(
            self.txtCDRQCQ8.connect('focus-out-event', self._on_focus_out, 18))
        self._lst_handler_id.append(
            self.txtCDRQCQ9.connect('focus-out-event', self._on_focus_out, 19))
        self._lst_handler_id.append(
            self.txtCDRQCQ10.connect('focus-out-event',
                                     self._on_focus_out, 20))
        self._lst_handler_id.append(
            self.txtCDRQCQ11.connect('focus-out-event',
                                     self._on_focus_out, 21))
        self._lst_handler_id.append(
            self.txtCDRQCQ12.connect('focus-out-event',
                                     self._on_focus_out, 22))
        self._lst_handler_id.append(
            self.chkCDRQCQ13.connect('toggled', self._on_toggled, 23))
        self._lst_handler_id.append(
            self.chkCDRQCQ14.connect('toggled', self._on_toggled, 24))
        self._lst_handler_id.append(
            self.txtCDRQCQ15.connect('focus-out-event',
                                     self._on_focus_out, 25))
        self._lst_handler_id.append(
            self.txtCDRQCQ16.connect('focus-out-event',
                                     self._on_focus_out, 26))
        self._lst_handler_id.append(
            self.chkCDRQCQ17.connect('toggled', self._on_toggled, 27))
        self._lst_handler_id.append(
            self.chkCDRQCQ18.connect('toggled', self._on_toggled, 28))
        self._lst_handler_id.append(
            self.chkCDRQCQ19.connect('toggled', self._on_toggled, 29))
        self._lst_handler_id.append(
            self.chkCDRQCQ20.connect('toggled', self._on_toggled, 30))
        self._lst_handler_id.append(
            self.chkCDRQCQ21.connect('toggled', self._on_toggled, 31))
        self._lst_handler_id.append(
            self.chkCDRQCQ22.connect('toggled', self._on_toggled, 32))
        self._lst_handler_id.append(
            self.chkCDRQCQ23.connect('toggled', self._on_toggled, 33))
        self._lst_handler_id.append(
            self.chkCDRQCQ24.connect('toggled', self._on_toggled, 34))

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Critical\nDesign\nReview") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_angle(90)
        _label.show_all()
        _label.set_tooltip_text(_(u"Allows assessment of the reliability risk "
                                  u"for a software unit at the critical "
                                  u"design review phase."))
        notebook.insert_page(self, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Critical Design Review Risk Analysis answers.

        :param `rtk.software.Software` model: the Software data model to load
                                              the gtk.ToggleButton() from.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._software_model = model

        self.chkCDRAMQ1.set_active(model.lst_anomaly_mgmt[2][0])
        self.chkCDRAMQ2.set_active(model.lst_anomaly_mgmt[2][1])
        self.chkCDRAMQ3.set_active(model.lst_anomaly_mgmt[2][2])
        self.chkCDRAMQ4.set_active(model.lst_anomaly_mgmt[2][3])
        self.chkCDRAMQ5.set_active(model.lst_anomaly_mgmt[2][4])
        self.chkCDRAMQ6.set_active(model.lst_anomaly_mgmt[2][5])
        self.chkCDRAMQ7.set_active(model.lst_anomaly_mgmt[2][6])
        self.chkCDRAMQ8.set_active(model.lst_anomaly_mgmt[2][7])
        self.chkCDRAMQ9.set_active(model.lst_anomaly_mgmt[2][8])
        self.chkCDRAMQ10.set_active(model.lst_anomaly_mgmt[2][9])

        self.chkCDRSTQ1.set_active(model.lst_traceability[2][0])

        self.txtCDRQCQ1.set_text(str(model.lst_sftw_quality[2][0]))
        self.txtCDRQCQ2.set_text(str(model.lst_sftw_quality[2][1]))
        self.chkCDRQCQ3.set_active(model.lst_sftw_quality[2][2])
        self.txtCDRQCQ4.set_text(str(model.lst_sftw_quality[2][3]))
        self.txtCDRQCQ5.set_text(str(model.lst_sftw_quality[2][4]))
        self.chkCDRQCQ6.set_active(model.lst_sftw_quality[2][5])
        self.txtCDRQCQ7.set_text(str(model.lst_sftw_quality[2][6]))
        self.txtCDRQCQ8.set_text(str(model.lst_sftw_quality[2][7]))
        self.txtCDRQCQ9.set_text(str(model.lst_sftw_quality[2][8]))
        self.txtCDRQCQ10.set_text(str(model.lst_sftw_quality[2][9]))
        self.txtCDRQCQ11.set_text(str(model.lst_sftw_quality[2][10]))
        self.txtCDRQCQ12.set_text(str(model.lst_sftw_quality[2][11]))
        self.chkCDRQCQ13.set_active(model.lst_sftw_quality[2][12])
        self.chkCDRQCQ14.set_active(model.lst_sftw_quality[2][13])
        self.txtCDRQCQ15.set_text(str(model.lst_sftw_quality[2][14]))
        self.txtCDRQCQ16.set_text(str(model.lst_sftw_quality[2][15]))
        self.chkCDRQCQ17.set_active(model.lst_sftw_quality[2][16])
        self.chkCDRQCQ18.set_active(model.lst_sftw_quality[2][17])
        self.chkCDRQCQ19.set_active(model.lst_sftw_quality[2][18])
        self.chkCDRQCQ20.set_active(model.lst_sftw_quality[2][19])
        self.chkCDRQCQ21.set_active(model.lst_sftw_quality[2][20])
        self.chkCDRQCQ22.set_active(model.lst_sftw_quality[2][21])
        self.chkCDRQCQ23.set_active(model.lst_sftw_quality[2][22])
        self.chkCDRQCQ24.set_active(model.lst_sftw_quality[2][23])

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

        self._software_model.lst_sftw_quality[2][index - 11] = int(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_toggled(self, check, index):
        """
        Callback function for gtk.CheckButton() 'toggled' signals.

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the index of the Development Environment question
                          associated with the gtk.CheckButton() that was
                          toggled.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        check.handler_block(self._lst_handler_id[index])

        if index in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            self._software_model.lst_anomaly_mgmt[2][index] = int(check.get_active())
        elif index == 10:
            self._software_model.lst_traceability[2][index - 10] = int(check.get_active())
        elif index in [13, 16, 23, 24, 27, 28, 29, 30, 31, 32, 33, 34]:
            self._software_model.lst_sftw_quality[2][index - 11] = int(check.get_active())

        check.handler_unblock(self._lst_handler_id[index])

        return False
