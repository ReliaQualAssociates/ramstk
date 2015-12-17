#!/usr/bin/env python
"""
################################################
Reliability Growth Testing Module Work Book View
################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.testing.gui.gtk.Growth.py is part of The RTK Project
#
# All rights reserved.

import sys
from datetime import datetime

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

# Import modules for localization support.
import gettext
import locale

# Modules used for plotting.
import matplotlib
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
matplotlib.use('GTK')

import numpy as np

# Import other RTK modules.
try:
    import Configuration as _conf
    import Utilities as _util
    import gui.gtk.Widgets as _widg
    from testing.Assistants import MTTFFCalculator, AddRGRecord
except ImportError:
    import rtk.Configuration as _conf
    import rtk.Utilities as _util
    import rtk.gui.gtk.Widgets as _widg
    from rtk.testing.Assistants import MTTFFCalculator, AddRGRecord

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _expand_plot(event):
    """
    Function to display a plot in it's own window.

    :param event: the matplotlib MouseEvent that called this function.
    :return: False if successful or True if an error is encountered.
    :rtype: boolean
    """

    _plot = event.canvas
    _parent = _plot.get_parent()

    #_height = int(self._app.winWorkBook.height)
    #_width = int(self._app.winWorkBook.width / 2.0)

    if event.button == 3:               # Right click.
        _window = gtk.Window()
        _window.set_skip_pager_hint(True)
        _window.set_skip_taskbar_hint(True)
        _window.set_default_size(1000, 700)
        _window.set_border_width(5)
        _window.set_position(gtk.WIN_POS_NONE)
        _window.set_title(_(u"RTK Plot"))

        _window.connect('delete_event', _close_plot, _plot, _parent)

        _plot.reparent(_window)

        _window.show_all()

    return False


def _close_plot(__window, __event, plot, parent):
    """
    Function to close the plot and return it to its original parent widget.

    :param gtk.Window __window: the gtk.Window() that is being destroyed.
    :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                  function.
    :param matplotlib.FigureCanvas plot: the matplotlib FigureCanvas that was
                                         expanded.
    :param gtk.Widget parent: the original parent widget for the plot.
    :return: False if successful or True if an error is encountered
    :rtype: boolean
    """

    plot.reparent(parent)

    return False

# TODO: Fix all docstrings; copy-paste errors.
class Planning(gtk.HPaned):                 # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected Reliability
    Growth Test Plan.  The attributes of a Reliability Growth Test Planning
    Work Book view are:

    :ivar list _lst_handler_id: default value: []
    :ivar _testing_model: :py:class:`rtk.testing.growth.Model`
    :ivar gtk.Button btnFindMTBFI:
    :ivar gtk.Button btnFindTTFF:
    :ivar gtk.CheckButton chkFixMTBFI:
    :ivar gtk.CheckButton chkFixMTBFG:
    :ivar gtk.CheckButton chkFixTTT:
    :ivar gtk.CheckButton chkFixAverageGR:
    :ivar gtk.CheckButton chkFixProgramMS:
    :ivar gtk.CheckButton chkFixAverageFEF:
    :ivar gtk.CheckButton chkFixProgramProb:
    :ivar gtk.CheckButton chkFixTTFF:
    :ivar gtk.ComboBox cmbPlanModel: selects and displays the planning model.
    :ivar gtk.ComboBox cmbAssessModel:
    :ivar dtcGrowth: :py:class:`rtk.testing.growth.Growth`
    :ivar gtk.SpinButton spnNumPhases:
    :ivar gtk.TreeView tvwRGPlanDetails:
    :ivar gtk.Entry txtTechReq:
    :ivar gtk.Entry txtMTBFG:
    :ivar gtk.Entry txtMTBFGP:
    :ivar gtk.Entry txtMTBFI:
    :ivar gtk.Entry txtTTT:
    :ivar gtk.Entry txtAverageGR:
    :ivar gtk.Entry txtProgramMS:
    :ivar gtk.Entry txtAverageFEF:
    :ivar gtk.Entry txtProgramProb:
    :ivar gtk.Entry txtTTFF:
    """

    def __init__(self, controller):
        """
        Initializes the Work Book view for the Reliability Growth Test
        Planning.

        :param :py:class:`rtk.testing.growth.Growth` controller: the Growth
                                                                 data
                                                                 controller.
        """

        gtk.HPaned.__init__(self)

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._testing_model = None

        # Initialize public scalar attributes.
        self.btnFindMTBFI = _widg.make_button(height=25, width=25,
                                              label=u"...", image=None)
        self.btnFindTTFF = _widg.make_button(height=25, width=25,
                                             label=u"...", image=None)

        self.chkFixMTBFI = _widg.make_check_button()
        self.chkFixMTBFG = _widg.make_check_button()
        self.chkFixTTT = _widg.make_check_button()
        self.chkFixAverageGR = _widg.make_check_button()
        self.chkFixProgramMS = _widg.make_check_button()
        self.chkFixAverageFEF = _widg.make_check_button()
        self.chkFixProgramProb = _widg.make_check_button()
        self.chkFixTTFF = _widg.make_check_button()

        self.cmbPlanModel = _widg.make_combo()
        self.cmbAssessModel = _widg.make_combo()

        self.dtcGrowth = controller

        self.spnNumPhases = gtk.SpinButton()
        self.spnNumPhases.set_tooltip_text(_(u"Sets the number of test phases "
                                             u"for the selected test."))

        self.spnNumPhases.set_digits(0)
        self.spnNumPhases.set_increments(1, 5)
        self.spnNumPhases.set_range(0, 100)

        self.tvwRGPlanDetails = gtk.TreeView()

        self.txtTechReq = _widg.make_entry(width=100)
        self.txtMTBFG = _widg.make_entry(width=100)
        self.txtMTBFGP = _widg.make_entry(width=100)
        self.txtMTBFI = _widg.make_entry(width=100)
        self.txtTTT = _widg.make_entry(width=100)
        self.txtAverageGR = _widg.make_entry(width=100)
        self.txtProgramMS = _widg.make_entry(width=100)
        self.txtAverageFEF = _widg.make_entry(width=100)
        self.txtProgramProb = _widg.make_entry(width=100)
        self.txtTTFF = _widg.make_entry(width=100)

        self.show_all()

    def create_page(self):
        """
        Creates the page for displaying the Reliability Growth Test Phase
        details for the selected Growth Test.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                 gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.pack1(_scrollwindow, True, True)

        self.pack2(self.tvwRGPlanDetails, False, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox()
        _results = [["AMSAA-Crow"], ["SPLAN"], ["SSPLAN"]]
        _widg.load_combo(self.cmbPlanModel, _results)

        _results = [[_(u"AMSAA/Crow Continuous")], [_(u"AMSAA/Crow Discrete")],
                    ["SSTRACK"], [_(u"AMSAA/Crow Projection")],
                    [_(u"Crow Extended")]]
        _widg.load_combo(self.cmbAssessModel, _results)

        # Create the labels.
        _labels = [_(u"RG Planning Model:"), _(u"RG Assessment Model:"),
                   _(u"Initial Program MTBF (MTBF<sub>I</sub>):"),
                   _(u"Program Required MTBF (MTBF<sub>TR</sub>):"),
                   _(u"Program Goal MTBF (MTBF<sub>G</sub>):"),
                   _(u"Potential Mature MTBF (MTBF<sub>GP</sub>):"),
                   _(u"Number of Phases:"),
                   _(u"Time to First Fix (t<sub>1</sub>):"),
                   _(u"Total Test Time:"), _(u"Average Growth Rate:"),
                   _(u"Average FEF:"), _(u"Program MS:"),
                   _(u"Program Probability:")]

        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5, 30)
        _x_pos += 40

        _label = _widg.make_label(_(u"Fix\nValue"), 150, 50)

        # Set the tooltips for the gtk.Widget().
        _fixed.put(_label, _x_pos + 230, _y_pos[0])

        self.cmbPlanModel.set_tooltip_text(_(u"Selects and displays the "
                                             u"reliability growth planning "
                                             u"model to be used."))
        self.cmbAssessModel.set_tooltip_text(_(u"Selects and displays the "
                                               u"reliability growth "
                                               u"assessment model to be "
                                               u"used."))
        self.btnFindMTBFI.set_tooltip_text(_(u"Launches the initial MTBF "
                                             u"calculator."))
        self.btnFindTTFF.set_tooltip_text(_(u"Launches the time to first fix "
                                            u"calculator."))
        self.txtMTBFI.set_tooltip_text(_(u"The initial MTBF for the seleceted "
                                         u"reliability growth plan."))
        self.chkFixMTBFI.set_tooltip_text(_(u"Fixes the value of the initial "
                                            u"MTBF when creating the selected "
                                            u"reliability growth plan."))
        self.txtMTBFG.set_tooltip_text(_(u"The goal MTBF for the selected "
                                         u"reliability growth plan."))
        self.chkFixMTBFG.set_tooltip_text(_(u"Fixes the value of the program "
                                            u"goal MTBF when creating the "
                                            u"selected reliability growth "
                                            u"plan."))
        self.txtMTBFGP.set_tooltip_text(_(u"The potential MTBF at maturity "
                                          u"for the assembly associated with "
                                          u"the selected reliability growth "
                                          u"plan."))
        self.txtTechReq.set_tooltip_text(_(u"The MTBF require by the "
                                           u"developmental program associated "
                                           u"with the selected reliability "
                                           u"growth plan."))
        self.spnNumPhases.set_tooltip_text(_(u"The number of reliability "
                                             u"growth phases."))
        self.txtTTFF.set_tooltip_text(_(u"The estimated time to the first fix "
                                        u"during the reliability growth "
                                        u"program."))
        self.chkFixTTFF.set_tooltip_text(_(u"Fixes the value of the time to "
                                           u"first fix when calculating the "
                                           u"selected reliability growth "
                                           u"plan."))
        self.txtTTT.set_tooltip_text(_(u"The total test time."))
        self.chkFixTTT.set_tooltip_text(_(u"Fixes the value of the total "
                                          u"program test time when "
                                          u"calculating the selected "
                                          u"reliability growth plan."))
        self.txtAverageGR.set_tooltip_text(_(u"The average growth rate over "
                                             u"the entire reliability growth "
                                             u"program."))
        self.chkFixAverageGR.set_tooltip_text(_(u"Fixes the value of the "
                                                u"average growth rate when "
                                                u"calculating the selected "
                                                u"reliability growth plan."))
        self.txtAverageFEF.set_tooltip_text(_(u"The average fix effectiveness "
                                              u"factor (FEF) over the entire "
                                              u"reliability growth program."))
        self.chkFixAverageFEF.set_tooltip_text(_(u"Fixes the value of the "
                                                 u"average fix effectiveness "
                                                 u"factor (FEF) when "
                                                 u"calculating the selected "
                                                 u"reliability growth plan."))
        self.txtProgramMS.set_tooltip_text(_(u"The percentage of failures "
                                             u"that will be addressed by "
                                             u"corrective action over the "
                                             u"entire reliability growth "
                                             u"program."))
        self.chkFixProgramMS.set_tooltip_text(_(u"Fixes the value of the "
                                                u"management strategy when "
                                                u"creating the selected "
                                                u"reliability growth plan."))
        self.txtProgramProb.set_tooltip_text(_(u"The probability of seeing a "
                                               u"failure during the first "
                                               u"phase of the reliability "
                                               u"growth program."))
        self.chkFixProgramProb.set_tooltip_text(_(u"Fixes the value of the "
                                                  u"probability of seeing a "
                                                  u"failure when creating the "
                                                  u"selected reliability "
                                                  u"growth plan."))

        # Position the gtk.Widget() on the page.
        _fixed.put(self.cmbPlanModel, _x_pos, _y_pos[0])
        _fixed.put(self.cmbAssessModel, _x_pos, _y_pos[1])
        _fixed.put(self.btnFindMTBFI, _x_pos + 125, _y_pos[2])
        _fixed.put(self.txtMTBFI, _x_pos, _y_pos[2])
        _fixed.put(self.chkFixMTBFI, _x_pos + 240, _y_pos[2])
        _fixed.put(self.txtTechReq, _x_pos, _y_pos[3])
        _fixed.put(self.txtMTBFG, _x_pos, _y_pos[4])
        _fixed.put(self.chkFixMTBFG, _x_pos + 240, _y_pos[4])
        _fixed.put(self.txtMTBFGP, _x_pos, _y_pos[5])
        _fixed.put(self.spnNumPhases, _x_pos, _y_pos[6])
        _fixed.put(self.txtTTFF, _x_pos, _y_pos[7])
        _fixed.put(self.btnFindTTFF, _x_pos + 125, _y_pos[7])
        _fixed.put(self.chkFixTTFF, _x_pos + 240, _y_pos[7])
        _fixed.put(self.txtTTT, _x_pos, _y_pos[8])
        _fixed.put(self.chkFixTTT, _x_pos + 240, _y_pos[8])
        _fixed.put(self.txtAverageGR, _x_pos, _y_pos[9])
        _fixed.put(self.chkFixAverageGR, _x_pos + 240, _y_pos[9])
        _fixed.put(self.txtAverageFEF, _x_pos, _y_pos[10])
        _fixed.put(self.chkFixAverageFEF, _x_pos + 240, _y_pos[10])
        _fixed.put(self.txtProgramMS, _x_pos, _y_pos[11])
        _fixed.put(self.chkFixProgramMS, _x_pos + 240, _y_pos[11])
        _fixed.put(self.txtProgramProb, _x_pos, _y_pos[12])
        _fixed.put(self.chkFixProgramProb, _x_pos + 240, _y_pos[12])

        # Connect gtk.Widget() signals to callback functions.
        self._lst_handler_id.append(
            self.cmbPlanModel.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbAssessModel.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(self.txtMTBFI.connect('focus-out-event',
                                                          self._on_focus_out,
                                                          2))
        self._lst_handler_id.append(self.txtMTBFG.connect('focus-out-event',
                                                          self._on_focus_out,
                                                          3))
        self._lst_handler_id.append(self.txtMTBFGP.connect('focus-out-event',
                                                           self._on_focus_out,
                                                           4))
        self._lst_handler_id.append(self.txtTechReq.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            5))
        self._lst_handler_id.append(
            self.spnNumPhases.connect('focus-out-event',
                                      self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.spnNumPhases.connect('value-changed',
                                      self._on_spin_value_changed))
        self._lst_handler_id.append(self.txtTTFF.connect('focus-out-event',
                                                         self._on_focus_out,
                                                         8))
        self._lst_handler_id.append(self.txtTTT.connect('focus-out-event',
                                                        self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.txtAverageGR.connect('focus-out-event',
                                      self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtAverageFEF.connect('focus-out-event',
                                       self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtProgramMS.connect('focus-out-event',
                                      self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtProgramProb.connect('focus-out-event',
                                        self._on_focus_out, 13))

        self._lst_handler_id.append(
            self.btnFindTTFF.connect('button-release-event',
                                     self.on_button_clicked, 14))

        self._lst_handler_id.append(
            self.chkFixMTBFI.connect('toggled', self._on_check_toggled, 15))
        self._lst_handler_id.append(
            self.chkFixMTBFG.connect('toggled', self._on_check_toggled, 16))
        self._lst_handler_id.append(
            self.chkFixTTFF.connect('toggled', self._on_check_toggled, 17))
        self._lst_handler_id.append(
            self.chkFixTTT.connect('toggled', self._on_check_toggled, 18))
        self._lst_handler_id.append(
            self.chkFixAverageGR.connect('toggled',
                                         self._on_check_toggled, 19))
        self._lst_handler_id.append(
            self.chkFixAverageFEF.connect('toggled',
                                          self._on_check_toggled, 20))
        self._lst_handler_id.append(
            self.chkFixProgramMS.connect('toggled',
                                         self._on_check_toggled, 21))
        self._lst_handler_id.append(
            self.chkFixProgramProb.connect('toggled',
                                           self._on_check_toggled, 22))

        # Create the Growth Testing gtk.TreeView().
        # =============================================================== #
        # Reliability Growth Testing Detailed Inputs
        #   0. Test Phase
        #   1. Number of Test Articles for the test phase
        #   2. Phase Start Date
        #   3. Phase End Date
        #   4. Cumulative test time at end of the test phase
        #   5. Growth Rate for the test phase
        #   6. Number of failures during test phase
        #   7. Average MTBF for the test phase
        #   8. Initial MTBF for the test phase (calculated from the model)
        #   9. Final MTBF for the test phase (calculated from the model)
        # =============================================================== #
        self.tvwRGPlanDetails.set_tooltip_markup(_(u"Displays the details of "
                                                   u"the reliability growth "
                                                   u"plan.  Right click any "
                                                   u"date field to show the "
                                                   u"calendar."))
        _labels = [_(u"Phase"), _(u"Test\nArticles"), _(u"Start Date"),
                   _(u"End Date"), _(u"Cumulative\nTest Time"),
                   _(u"Minimum\nRequired\nGrowth Rate"),
                   _(u"Expected\nNumber of\nFailures"),
                   _(u"Average\nMTBF"), _(u"Initial\nMTBF"), _(u"Final\nMTBF")]
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_INT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwRGPlanDetails.set_model(_model)

        for i in range(10):
            if i == 0:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'light gray')
            else:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.connect('edited', self._on_plan_edited, i)

            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_labels[i])
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_resizable(True)
            if i in [0, 1, 6]:
                _datatype = (i, 'gint')
            elif i in [2, 3]:
                _datatype = (i, 'gchararray')
# TODO: Unhide the growth rate column after figuring out a good way to calculate test phase specific growth rates.
            elif i == 5:
                _datatype = (i, 'gfloat')
            #    _column.set_visible(False)
            else:
                _datatype = (i, 'gfloat')
            _column.set_attributes(_cell, text=i)
            _column.set_cell_data_func(_cell, _widg.format_cell,
                                       (i, _datatype))
            _column.connect('notify::width', _widg.resize_wrap, _cell)

            self.tvwRGPlanDetails.append_column(_column)

        #self.tvwRGPlanDetails.connect('button_press_event',
        #                              self._on_button_clicked, 1)

        return False

    def load_page(self, model):
        """
        Method to load the Reliability Growth Test Plan gtk.Notebook() page.

        :param model: the :py:class:`rtk.testing.Testing.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._testing_model = model

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Load the individual widgets.
        self.cmbPlanModel.set_active(model.rg_plan_model)
        self.cmbAssessModel.set_active(model.rg_assess_model)
        self.txtMTBFI.set_text(str(fmt.format(model.lst_p_mtbfi[0])))
        self.txtMTBFG.set_text(str(fmt.format(model.mtbfg)))
        self.txtMTBFGP.set_text(str(fmt.format(model.mtbfgp)))
        self.txtTechReq.set_text(str(fmt.format(model.tr)))
        self.spnNumPhases.set_value(model.n_phases)
        self.txtTTT.set_text(str(fmt.format(model.ttt)))
        self.txtAverageGR.set_text(str(fmt.format(model.avg_growth)))
        self.txtAverageFEF.set_text(str(fmt.format(model.avg_fef)))
        self.txtProgramMS.set_text(str(fmt.format(model.avg_ms)))
        self.txtProgramProb.set_text(str(fmt.format(model.probability)))
        self.txtTTFF.set_text(str(fmt.format(model.ttff)))

        # Load the Growth Plan phase-specific information.
        self._load_plan_details()

        return False

    def _load_plan_details(self):
        """
        Method to load the Reliability Growth Plan details into the
        gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwRGPlanDetails.get_model()
        _model.clear()
        for i in range(self._testing_model.n_phases):
            try:
                _dt_start = str(datetime.fromordinal(
                    int(self._testing_model.lst_p_start_date[i])).strftime('%Y-%m-%d'))
            except(TypeError, ValueError):
                _dt_start = datetime.today().strftime('%Y-%m-%d')
                self._testing_model.lst_p_start_date[i] = datetime.strptime(_dt_start, "%Y-%m-%d").toordinal()
            try:
                _dt_end = str(datetime.fromordinal(
                    int(self._testing_model.lst_p_end_date[i])).strftime('%Y-%m-%d'))
            except(TypeError, ValueError):
                _dt_end = datetime.today().strftime('%Y-%m-%d')
                self._testing_model.lst_p_end_date[i] = datetime.strptime(_dt_end, "%Y-%m-%d").toordinal()

            _data = [i + 1, self._testing_model.lst_p_n_test_units[i],
                     _dt_start, _dt_end,
                     self._testing_model.lst_p_test_time[i],
                     self._testing_model.lst_p_growth_rate[i],
                     self._testing_model.lst_p_n_failures[i],
                     self._testing_model.lst_p_mtbfa[i],
                     self._testing_model.lst_p_mtbfi[i],
                     self._testing_model.lst_p_mtbff[i]]
            _model.append(_data)

        return False

    def on_button_clicked(self, __button, __event, index):
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if index == 14:
            MTTFFCalculator()
        elif index == 50:
            _results = self.dtcGrowth.request_calculate(self._testing_model.test_id)

            if _results[0]:
                _util.rtk_error(_(u"To calculate the minimum inital MTBF, you "
                                  u"must provide the following inputs with "
                                  u"values greater than zero:\n\n"
                                  u"1. Total test time (TTT): %f\n"
                                  u"2. Length of first test phase (t1): %f\n"
                                  u"3. Final MTBF (MTBFF): %f\n"
                                  u"4. Growth rate (GR): %f\n\n")
                                % (self._testing_model.ttt,
                                   self._testing_model.lst_p_test_time[0],
                                   self._testing_model.lst_p_mtbff[self._testing_model.n_phases - 1],
                                   self._testing_model.avg_growth))
            if _results[1]:
                _util.rtk_error(_(u"To calculate the final MTBF, you must "
                                  u"provide the following inputs with values "
                                  u"greater than zero:\n\n"
                                  u"1. Total test time (TTT): %f\n"
                                  u"2. Length of the first test phase (t1): %f\n"
                                  u"3. Intial program MTBF (MI): %f\n"
                                  u"4. Growth rate (GR): %f\n\n")
                                % (self._testing_model.ttt,
                                   self._testing_model.lst_p_test_time[0],
                                   self._testing_model.lst_p_mtbfi[0],
                                   self._testing_model.avg_growth))
            if _results[2]:
                _util.rtk_error(_(u"To calculate the minimum length of the "
                                  u"first phase, you must provide the "
                                  u"following inputs with values greater than "
                                  u"zero:\n\n"
                                  u"1. Final MTBF (MF): %f\n"
                                  u"2. Average growth rate (GR): %f\n"
                                  u"3. Average MTBF of the first phase: %f\n\n")
                                % (self._testing_model.lst_p_mtbff[self._testing_model.n_phases - 1],
                                   self._testing_model.avg_growth,
                                   self._testing_model.lst_p_mtbfa[0]))
            if _results[4]:
                _util.rtk_error(_(u"To calculate the minimum required program "
                                  u"growth rate, you must provide the "
                                  u"following inputs with values greater than "
                                  u"zero:\n\n"
                                  u"1. Total test time (TTT): %f\n"
                                  u"2. Length of the first test phase (t1): %f\n"
                                  u"3. Initial program MTBF (MI): %f\n"
                                  u"4. Final program MTBF (MF): %f\n\n")
                                % (self._testing_model.ttt,
                                   self._testing_model.lst_p_test_time[0],
                                   self._testing_model.lst_p_mtbfi[0],
                                   self._testing_model.lst_p_mtbff[self._testing_model.n_phases - 1]))
            if _results[6]:
                _util.rtk_error(_(u"To calculate the required management "
                                  u"strategy, you must provide the following "
                                  u"inputs with values greater than zero:\n\n"
                                  u"1. Initial MTBF (MI): %f\n"
                                  u"2. Growth Potential MTBF (MGP): %f\n"
                                  u"3. Fix Effectiveness Factor (FEF): %f\n\n")
                                % (self._testing_model.lst_p_mtbfi[0],
                                   self._testing_model.mtbfgp,
                                   self._testing_model.avg_fef))
            if _results[7]:
                _util.rtk_error(_(u"To calculate the probability of observing "
                                  u"a failure, you must provide the following "
                                  u"inputs with values greater than zero:\n\n"
                                  u"1. Growth start time (ti): %f\n"
                                  u"2. Initial MTBF (MI): %f\n"
                                  u"3. Management strategy (MS): %f\n\n")
                                % (self._testing_model.ttff,
                                   self._testing_model.lst_p_mtbfi[0],
                                   self._testing_model.avg_ms))
            if _results[8]:
                _util.rtk_error(_(u"To calculate the growth potential MTBF, "
                                  u"you must provide the following inputs "
                                  u"with values greater than zero:\n\n"
                                  u"1. Initial MTBF (MI): %f\n"
                                  u"2. Management strategy (MS): %f\n"
                                  u"3. Fix Effectiveness Factor (FEF): %f\n\n")
                                % (self._testing_model.lst_p_mtbfi[0],
                                   self._testing_model.avg_ms,
                                   self._testing_model.avg_fef))

            self.load_page(self._testing_model)

        return False

    def _on_check_toggled(self, checkbutton, index):
        """
        Callback function to update and save gtk.CheckButton() changes for
        the Growth class.

        :param gtk.CheckButton checkbutton: the gtk.CheckButton() that called
                                            this method.
        :param int index: the index of the gtk.CheckButton() that called this
                          method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        checkbutton.handler_block(self._lst_handler_id[index])

        self._testing_model.lst_fixed_values[index - 15] = checkbutton.get_active()

        checkbutton.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_combo_changed(self, combo, index):
        """
        Callback function to retrieve and save gtk.ComboBox() changes for the
        Testing class.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called the function.
        :param int index: the position in the Testing class gtk.TreeModel()
                          associated with the data from the calling combobox.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 0:                      # Planning Model
            self._testing_model.rg_plan_model = combo.get_active()
        elif index == 1:                    # Assessment Model
            self._testing_model.rg_assess_model = combo.get_active()

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):     # pylint: disable=R0912
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

        if index == 2:                      # Initial MTBF
            self._testing_model.lst_p_mtbfi[0] = float(entry.get_text())
        elif index == 3:                    # Goal MTBF
            self._testing_model.mtbfg = float(entry.get_text())
        elif index == 4:                    # Growth potential MTBF
            self._testing_model.mtbfgp = float(entry.get_text())
        elif index == 5:                    # Technical requirement
            self._testing_model.tr = float(entry.get_text())
        elif index == 6:                    # Number of phases
            self._testing_model.num_phases = float(entry.get_text())
        elif index == 8:                    # Time to first failure
            self._testing_model.ttff = float(entry.get_text())
        elif index == 9:                    # Total time on test
            self._testing_model.ttt = float(entry.get_text())
        elif index == 10:                   # Average program growth rate
            self._testing_model.avg_growth = float(entry.get_text())
        elif index == 11:                   # Average program FEF
            self._testing_model.avg_fef = float(entry.get_text())
        elif index == 12:                   # Average program management strategy
            self._testing_model.avg_ms = float(entry.get_text())
        elif index == 13:                   # Program probability
            self._testing_model.probability = float(entry.get_text())

        # Update the Testing class public and private attributes.
        #self._update_attributes()

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_spin_value_changed(self, button):
        """
        Callback function when the gtk.SpinButton() value changes.

        :param gtk.SpinButton button: the gtk.SpinButton() that called this
                                      method
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[7])

        _n_phases = int(self.spnNumPhases.get_value())
        _new_phases = _n_phases - self._testing_model.n_phases
        if _new_phases > 0:
            for i in range(_new_phases):
                _phase_id = self._testing_model.n_phases + i
                self.dtcGrowth.add_test_phase(self._testing_model.test_id,
                                              _phase_id)
                self._testing_model.lst_p_growth_rate.append(0.0)
                self._testing_model.lst_p_ms.append(0.0)
                self._testing_model.lst_p_fef.append(0.0)
                self._testing_model.lst_p_prob.append(0.0)
                self._testing_model.lst_p_mtbfi.append(0.0)
                self._testing_model.lst_p_mtbff.append(0.0)
                self._testing_model.lst_p_mtbfa.append(0.0)
                self._testing_model.lst_p_test_time.append(0.0)
                self._testing_model.lst_p_n_failures.append(0)
                self._testing_model.lst_p_start_date.append(0)
                self._testing_model.lst_p_end_date.append(0)
                self._testing_model.lst_p_weeks.append(0.0)
                self._testing_model.lst_p_n_test_units.append(0)
                self._testing_model.lst_p_tpu.append(0.0)
                self._testing_model.lst_p_tpupw.append(0.0)
                self._testing_model.lst_o_growth_rate.append(0.0)
                self._testing_model.lst_o_ms.append(0.0)
                self._testing_model.lst_o_fef.append(0.0)
                self._testing_model.lst_o_mtbfi.append(0.0)
                self._testing_model.lst_o_mtbff.append(0.0)
                self._testing_model.lst_o_mtbfa.append(0.0)
                self._testing_model.lst_o_test_time.append(0.0)

        elif _new_phases < 0:
            for i in range(abs(_new_phases)):
                _phase_id = self._testing_model.n_phases - (i + 1)
                self.dtcGrowth.delete_test_phase(self._testing_model.test_id,
                                                 _phase_id)
                self._testing_model.lst_p_growth_rate.pop(_phase_id)
                self._testing_model.lst_p_ms.pop(_phase_id)
                self._testing_model.lst_p_fef.pop(_phase_id)
                self._testing_model.lst_p_prob.pop(_phase_id)
                self._testing_model.lst_p_mtbfi.pop(_phase_id)
                self._testing_model.lst_p_mtbff.pop(_phase_id)
                self._testing_model.lst_p_mtbfa.pop(_phase_id)
                self._testing_model.lst_p_test_time.pop(_phase_id)
                self._testing_model.lst_p_n_failures.pop(_phase_id)
                self._testing_model.lst_p_start_date.pop(_phase_id)
                self._testing_model.lst_p_end_date.pop(_phase_id)
                self._testing_model.lst_p_weeks.pop(_phase_id)
                self._testing_model.lst_p_n_test_units.pop(_phase_id)
                self._testing_model.lst_p_tpu.pop(_phase_id)
                self._testing_model.lst_p_tpupw.pop(_phase_id)
                self._testing_model.lst_o_growth_rate.pop(_phase_id)
                self._testing_model.lst_o_ms.pop(_phase_id)
                self._testing_model.lst_o_fef.pop(_phase_id)
                self._testing_model.lst_o_mtbfi.pop(_phase_id)
                self._testing_model.lst_o_mtbff.pop(_phase_id)
                self._testing_model.lst_o_mtbfa.pop(_phase_id)
                self._testing_model.lst_o_test_time.pop(_phase_id)

        self._testing_model.n_phases = _n_phases

        # Update the Reliability Growth Plan gtk.TreeView().
        self._load_plan_details()

        button.handler_unblock(self._lst_handler_id[7])

        return False

    def _on_plan_edited(self, cell, path, new_text, index):
        """
        Callback function when editing a gtkCellRenderer() in the Reliability
        Growth plan details gtk.TreeView()
        """

        _model = self.tvwRGPlanDetails.get_model()
        _row = _model.get_iter_from_string(path)

        _widg.edit_tree(cell, path, new_text, index, _model)

        if _row is not None:
            _dt_start = datetime.strptime(_model.get_value(_row, 2),
                                          "%Y-%m-%d").toordinal()
            _dt_end = datetime.strptime(_model.get_value(_row, 3),
                                        "%Y-%m-%d").toordinal()

            # Update the lists containing the Reliability Growth Plan details.
            _phase_id = _model.get_value(_row, 0) - 1
            self._testing_model.lst_p_n_test_units[_phase_id] = _model.get_value(_row, 1)
            self._testing_model.lst_p_start_date[_phase_id] = _dt_start
            self._testing_model.lst_p_end_date[_phase_id] = _dt_end
            self._testing_model.lst_p_test_time[_phase_id] = _model.get_value(_row, 4)
            self._testing_model.lst_p_growth_rate[_phase_id] = _model.get_value(_row, 5)
            self._testing_model.lst_p_n_failures[_phase_id] = _model.get_value(_row, 6)
            self._testing_model.lst_p_mtbfa[_phase_id] = _model.get_value(_row, 7)
            self._testing_model.lst_p_mtbfi[_phase_id] = _model.get_value(_row, 8)
            self._testing_model.lst_p_mtbff[_phase_id] = _model.get_value(_row, 9)

            # Now update the RG plan feasibility gtk.TreeModel().
            #_model = self.tvwTestFeasibility.get_model()
            #_row = _model.get_iter_from_string(self._dic_rg_plan[_phase_id][8])
            #_model.set_value(_row, 1, self._dic_rg_plan[_phase_id][0])
            #_model.set_value(_row, 2, self._dic_rg_plan[_phase_id][1])
            #_model.set_value(_row, 3, self._dic_rg_plan[_phase_id][2])

        return False


class Feasibility(gtk.HPaned):              # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected Reliability
    Growth Test Plan feasibility.  The attributes of a Reliability Growth Test
    Feasibility Work Book view are:

    :ivar list _lst_handler_id: default value: []

    :ivar :py:class:`rtk.testing.growth.Model` _testing_model: default value: None
    :ivar :py:class:`rtk.testing.growth.Growth` dtcGrowth:

    :ivar gtk.CheckButton chkMIMGP:
    :ivar gtk.CheckButton chkFEF:
    :ivar gtk.CheckButton chkMGMGP:
    :ivar gtk.CheckButton chkGR:
    :ivar Figure figFigureOC:
    :ivar gtk.Frame fraTestRisk:
    :ivar gtk.Frame fraTestFeasibility:
    :ivar gtk.Frame fraOCCurve:
    :ivar gtk.Label lblMIMGP:
    :ivar gtk.Label lblFEF:
    :ivar gtk.Label lblMGMGP:
    :ivar gtk.Label lblGR:
    :ivar FigureCanvas pltPlotOC:
    :ivar Axis axAxisOC:
    :ivar gtk.ScrolledWindow scwTestFeasibility:
    :ivar gtk.TreeView tvwTestFeasibility:
    :ivar gtk.Entry txtMIMGP:
    :ivar gtk.Entry txtFEF:
    :ivar gtk.Entry txtMGMGP:
    :ivar gtk.Entry txtGR:
    """

    def __init__(self, controller):
        """
        Initializes the Work Book view for the Reliability Growth Test
        Feasibility.

        :param :py:class:`rtk.testing.growth.Growth` controller: the Growth
                                                                 data
                                                                 controller.
        """

        gtk.HPaned.__init__(self)

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._testing_model = None

        # Initialize public scalar attributes.
        self.chkMIMGP = _widg.make_check_button(label=_(u"Acceptable "
                                                        u"MTBF<sub>I</sub> "
                                                        u"/ MTBF<sub>GP"
                                                        u"</sub>."))
        self.chkFEF = _widg.make_check_button(label=_(u"Acceptable average "
                                                      u"fix effectiveness "
                                                      u"factor (FEF)."))
        self.chkMGMGP = _widg.make_check_button(label=_(u"Acceptable "
                                                        u"MTBF<sub>G</sub> "
                                                        u"/ MTBF<sub>GP"
                                                        u"</sub>."))
        self.chkGR = _widg.make_check_button(label=_(u"Acceptable "
                                                     u"average growth rate."))

        self.dtcGrowth = controller

        self.figFigureOC = Figure()

        self.lblMIMGP = _widg.make_label("", width=150)
        self.lblFEF = _widg.make_label("", width=150)
        self.lblMGMGP = _widg.make_label("", width=150)
        self.lblGR = _widg.make_label("", width=150)

        self.pltPlotOC = FigureCanvas(self.figFigureOC)

        self.axAxisOC = self.figFigureOC.add_subplot(111)

        self.tvwTestFeasibility = gtk.TreeView()

        self.txtMIMGP = _widg.make_entry(width=75)
        self.txtFEF = _widg.make_entry(width=75)
        self.txtMGMGP = _widg.make_entry(width=75)
        self.txtGR = _widg.make_entry(width=75)

        self.show_all()

    def create_page(self):
        """
        Creates the page for displaying the Reliability Growth Test Phase
        details for the selected Growth Test.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _fixed = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                 gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)

        self.pack1(_scrollwindow, True, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                 gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwTestFeasibility)

        self.pack2(_scrollwindow, True, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the labels.
        _labels = [_(u"MTBF<sub>I</sub> / MTBF<sub>GP</sub> should fall in "
                     u"the range of 0.15 - 0.47.  On average this ratio is "
                     u"0.30."),
                   _(u"Program MTBF<sub>I</sub> / MTBF<sub>GP</sub>:"), "", "",
                   _(u"MTBF<sub>G</sub> / MTBF<sub>GP</sub> should fall in "
                     u"the range of 0.60 - 0.80."),
                   _(u"Program MTBF<sub>G</sub> / MTBF<sub>GP</sub>:"), "", "",
                   _(u"Average growth rate should fall in the range of "
                     u"0.23 - 0.64."),
                   _(u"Program average growth rate:"), "", "",
                   _(u"The Fix Effectiveness Factor should fall in the range "
                     u"of 0.55 - 0.85.  On average the FEF is 0.70."),
                   _(u"Program average FEF:"), "", ""]

        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 5, 30)
        _x_pos += 40

        # Set the tooltips for the gtk.Widget().
        self.chkMIMGP.set_tooltip_text(_(u"Indicates whether or not the "
                                         u"initial MTBF to mature MTBF ratio "
                                         u"is within reasonable limits."))
        self.chkFEF.set_tooltip_text(_(u"Indicates whether or not the average "
                                       u"fix effectiveness factor (FEF) is "
                                       u"within reasonable limits."))
        self.chkMGMGP.set_tooltip_text(_(u"Indicates whether or not the goal "
                                         u"MTBF to mature MTBF ratio is "
                                         u"within reasonable limits."))
        self.chkGR.set_tooltip_text(_(u"Indicates whether or not the average "
                                      u"growth rate is within reasonable "
                                      u"limits."))
        self.pltPlotOC.set_tooltip_text(_(u"Displays the Reliability Growth "
                                          u"Plan Operating Characteristic "
                                          u"(OC) curve."))

        self.tvwTestFeasibility.set_tooltip_markup(_(u"Displays the details "
                                                     u"of the reliability "
                                                     u"growth plan.  Right "
                                                     u"click any date field "
                                                     u"to show the calendar."))

        # Position the gtk.Widget() on the page.
        _fixed.put(self.txtMIMGP, _x_pos, _y_pos[1])
        _fixed.put(self.lblMIMGP, _x_pos, _y_pos[2])
        _fixed.put(self.chkMIMGP, 5, _y_pos[3])

        _fixed.put(self.txtMGMGP, _x_pos, _y_pos[5])
        _fixed.put(self.lblMGMGP, _x_pos, _y_pos[6])
        _fixed.put(self.chkMGMGP, 5, _y_pos[7])

        _fixed.put(self.txtGR, _x_pos, _y_pos[9])
        _fixed.put(self.lblGR, _x_pos, _y_pos[10])
        _fixed.put(self.chkGR, 5, _y_pos[11])

        _fixed.put(self.txtFEF, _x_pos, _y_pos[13])
        _fixed.put(self.lblFEF, _x_pos, _y_pos[14])
        _fixed.put(self.chkFEF, 5, _y_pos[15])

        _labels = [_(u"Phase"), _(u"Number of\nTest\nArticles"),
                   _(u"Start Date"), _(u"End Date"),
                   _(u"Expected\nNumber\nof\nFailures"),
                   _(u"Required\nManagement\nStrategy"), _(u"Average\nFEF"),
                   _(u"Test Time\nper Unit"),
                   _(u"Test Time\nper Unit\nper Week")]
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_INT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT)
        self.tvwTestFeasibility.set_model(_model)

        for i in range(9):
            _cell = gtk.CellRendererText()
            if i == 1 or i == 2 or i == 3:
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.connect('edited', self._on_plan_edited, i)
            else:
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'grey')

            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_labels[i])
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i)
            _column.set_resizable(True)
            if i > 3:
                _datatype = (i, 'gfloat')
            else:
                _datatype = (i, 'gint')
            _column.set_cell_data_func(_cell, _widg.format_cell,
                                       (i, _datatype))
            _column.connect('notify::width', _widg.resize_wrap, _cell)
            self.tvwTestFeasibility.append_column(_column)

        # Connect gtk.Widget() signals to callback functions.
        self.pltPlotOC.mpl_connect('button_press_event', _expand_plot)
        self.tvwTestFeasibility.connect('button_press_event',
                                        self.on_button_clicked, 0)

        return False

    def load_page(self, model):
        """
        Method to load the Reliability Growth Test Feasibility gtk.Notebook()
        page.

        :param model: the :py:class:`rtk.testing.Testing.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._testing_model = model

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Load the individual widgets.
        # Initial MTBF to growth potential MTBF ratio is high enough.  Too
        # low means growth testing is probably being started too early.
        try:
            self.txtMIMGP.set_text(str(fmt.format(model.lst_p_mtbfi[0] /
                                                  model.mtbfgp)))
        except ZeroDivisionError:
            self.txtMIMGP.set_text("0.0")

        try:
            _ratio = model.lst_p_mtbfi[0] / model.mtbfgp
        except ZeroDivisionError:
            _ratio = 0.0
        if _ratio >= 0.15 and _ratio <= 0.47:
            self.chkMIMGP.set_active(True)
        else:
            self.chkMIMGP.set_active(False)

        if _ratio >= 0.35:
            self.lblMIMGP.set_markup(u"<span foreground='#00CC00'>"
                                     u"Low Risk</span>")
        elif _ratio < 0.35 and _ratio >= 0.2:
            self.lblMIMGP.set_markup(u"<span foreground='#FFFF00'>"
                                     u"Medium Risk</span>")
        else:
            self.lblMIMGP.set_markup(u"<span foreground='red'>"
                                     u"High Risk</span>")

        # Goal MTBF to growth potential MTBF ratio is high enough.  Too
        # high means there is a low probability of achieving the goal MTBF.
        # Too low means the system may be over designed.
        try:
            _ratio = model.mtbfg / model.mtbfgp
        except ZeroDivisionError:
            _ratio = 0.0
        self.txtMGMGP.set_text(str(fmt.format(_ratio)))
        if _ratio >= 0.6 and _ratio <= 0.8:
            self.chkMGMGP.set_active(True)
        else:
            self.chkMGMGP.set_active(False)

        if _ratio <= 0.7:
            self.lblMGMGP.set_markup(u"<span foreground='#00CC00'>"
                                     u"Low Risk</span>")
        elif _ratio > 0.7 and _ratio <= 0.8:
            self.lblMGMGP.set_markup(u"<span foreground='#FFFF00'>"
                                     u"Medium Risk</span>")
        else:
            self.lblMGMGP.set_markup(u"<span foreground='red'>"
                                     u"High Risk</span>")

        # Program average growth rate.
        self.txtGR.set_text(str(model.avg_growth))
        if model.avg_growth >= 0.23 and model.avg_growth <= 0.64:
            self.chkGR.set_active(True)
        else:
            self.chkGR.set_active(False)

        if model.avg_growth < 0.35:
            self.lblGR.set_markup(u"<span foreground='#00CC00'>"
                                  u"Low Risk</span>")
        elif model.avg_growth >= 0.35 and model.avg_growth <= 0.55:
            self.lblGR.set_markup(u"<span foreground='#FFFF00'>"
                                  u"Medium Risk</span>")
        else:
            self.lblGR.set_markup(u"<span foreground='red'>"
                                  u"High Risk</span>")

        # Fix effectiveness factor is low enough, but not too low.  Too low
        # means many failures will not be corrected, too high means it may
        # not be possible to remove enough failures from the system.
        self.txtFEF.set_text(str(fmt.format(model.avg_fef)))
        if model.avg_fef >= 0.55 and model.avg_fef <= 0.85:
            self.chkFEF.set_active(True)
        else:
            self.chkFEF.set_active(False)

        if model.avg_fef <= 0.7:
            self.lblFEF.set_markup(u"<span foreground='#00CC00'>"
                                   u"Low Risk</span>")
        elif model.avg_fef > 0.7 and model.avg_fef <= 0.8:
            self.lblFEF.set_markup(u"<span foreground='#FFFF00'>"
                                   u"Medium Risk</span>")
        else:
            self.lblFEF.set_markup(u"<span foreground='red'>"
                                   u"High Risk</span>")

        self._load_feasibility_details()

        return False

    def _load_feasibility_details(self):
        """
        Method to load the Reliability Growth Feasibility details into the
        gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwTestFeasibility.get_model()
        _model.clear()
        for i in range(self._testing_model.n_phases):
            try:
                _dt_start = str(datetime.fromordinal(
                    int(self._testing_model.lst_p_start_date[i])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_start = datetime.today().strftime('%Y-%m-%d')
            try:
                _dt_end = str(datetime.fromordinal(
                    int(self._testing_model.lst_p_end_date[i])).strftime('%Y-%m-%d'))
            except TypeError:
                _dt_end = datetime.today().strftime('%Y-%m-%d')
            _data = [i + 1, self._testing_model.lst_p_n_test_units[i],
                     _dt_start, _dt_end,
                     self._testing_model.lst_p_n_failures[i],
                     self._testing_model.lst_p_ms[i],
                     self._testing_model.lst_p_fef[i],
                     self._testing_model.lst_p_tpu[i],
                     self._testing_model.lst_p_tpupw[i]]
            _model.append(_data)

        self.tvwTestFeasibility.expand_all()
        self.tvwTestFeasibility.set_cursor('0', None, False)
        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            _col = self.tvwTestFeasibility.get_column(0)
            self.tvwTestFeasibility.row_activated(_path, _col)

        return False

    def on_button_clicked(self, __button, __event, index):
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if index == 0:
            pass
        elif index == 50:
            _results = self._testing_model.assess_plan_feasibility()

            if _results[0]:
                _util.rtk_warning(_(u"You have not entered the number of test "
                                    u"units for test phase %d.  Unable to "
                                    u"calculate the average test time per "
                                    u"test unit.  Please enter the number of "
                                    u"test units for test phase %d and try "
                                    u"again.") % (_results[2], _results[2]))
            if _results[1]:
                _util.rtk_warning(_(u"Start date and end date are the same "
                                    u"for test phase %d.  Unable to calculate "
                                    u"the average test time per week for a "
                                    u"test unit.  Please correct one or both "
                                    u"dates and try again.") % _results[3])

            self.load_page(self._testing_model)

        return False

    def _on_plan_edited(self, cell, path, new_text, position):
        """
        Callback function when editing a gtk.CellRenderer() in the Reliability
        Growth Plan Feasibility details gtk.TreeView()
        """

        _model = self.tvwTestFeasibility.get_model()
        _row = _model.get_iter_from_string(path)

        _widg.edit_tree(cell, path, new_text, position, _model)

        if _row is not None:
            _dt_start = datetime.strptime(_model.get_value(_row, 2),
                                          "%Y-%m-%d").toordinal()
            _dt_end = datetime.strptime(_model.get_value(_row, 3),
                                        "%Y-%m-%d").toordinal()

            # Update the lists containing the Reliability Growth Plan details.
            _phase_id = _model.get_value(_row, 0) - 1
            self._testing_model.lst_p_n_test_units[_phase_id] = _model.get_value(_row, 1)
            self._testing_model.lst_p_start_date[_phase_id] = _dt_start
            self._testing_model.lst_p_end_date[_phase_id] = _dt_end

        return False


class Assessment(gtk.HPaned):               # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected Reliability
    Growth Test Plan assessment.  The attributes of a Reliability Growth Test
    Assessment Work Book view are:

    :ivar list _lst_handler_id: default value: []

    :ivar :py:class:`rtk.testing.growth.Model` _testing_model: default value: None
    :ivar float _cvm_critical: default value: 0.0
    :ivar :py:class:`rtk.testing.growth.Growth` dtcGrowth:

    """

    def __init__(self, controller):
        """
        Initializes the Work Book view for the Reliability Growth Test
        Assessment.

        :param :py:class:`rtk.testing.growth.Growth` controller: the Growth
                                                                 data
                                                                 controller.
        """

        gtk.HPaned.__init__(self)

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._testing_model = None

        # Initialize public scalar attributes.
        self.dtcGrowth = controller

        self.optIndividual = gtk.RadioButton(label=_(u"Individual Failure "
                                                     u"Time Data"))
        self.optIndividual.set_name('individual')
        self.optIndividual.set_active(True)

        self.optGrouped = gtk.RadioButton(group=self.optIndividual,
                                          label=_(u"Grouped Failure Time "
                                                  u"Data"))
        self.optGrouped.set_name('grouped')

        self.optMTBF = gtk.RadioButton(label=_(u"Display results as MTBF"))

        self.optMTBF.set_name('mtbf')
        self.optMTBF.set_active(True)

        self.optFailureIntensity = gtk.RadioButton(group=self.optMTBF,
                                                   label=_(u"Display results "
                                                           u"as failure "
                                                           u"intensity"))
        self.optFailureIntensity.set_name('failureintensity')

        self.optLinear = gtk.RadioButton(label=_(u"Use Linear Scales"))
        self.optLinear.set_name('linear')
        self.optLinear.set_active(True)
        self.optLogarithmic = gtk.RadioButton(group=self.optLinear,
                                              label=_(u"Use Logarithmic "
                                                      u"Scales"))
        self.optLogarithmic.set_name('log')

        self.spnConfidence = gtk.SpinButton()

        self.tvwTestAssessment = gtk.TreeView()

        # Widgets to display the estimated parameters for the selected model.
        self.txtCumTestTime = _widg.make_entry(width=100, editable=False)
        self.txtCumFailures = _widg.make_entry(width=100, editable=False)
        self.txtScale = _widg.make_entry(width=100, editable=False)
        self.txtScalell = _widg.make_entry(width=100, editable=False)
        self.txtScaleul = _widg.make_entry(width=100, editable=False)
        self.txtShape = _widg.make_entry(width=100, editable=False)
        self.txtShapell = _widg.make_entry(width=100, editable=False)
        self.txtShapeul = _widg.make_entry(width=100, editable=False)
        self.txtGRActual = _widg.make_entry(width=100, editable=False)
        self.txtGRActualll = _widg.make_entry(width=100, editable=False)
        self.txtGRActualul = _widg.make_entry(width=100, editable=False)
        self.txtRhoInst = _widg.make_entry(width=100, editable=False)
        self.txtRhoInstll = _widg.make_entry(width=100, editable=False)
        self.txtRhoInstul = _widg.make_entry(width=100, editable=False)
        self.txtRhoC = _widg.make_entry(width=100, editable=False)
        self.txtRhoCll = _widg.make_entry(width=100, editable=False)
        self.txtRhoCul = _widg.make_entry(width=100, editable=False)
        self.txtMTBFInst = _widg.make_entry(width=100, editable=False)
        self.txtMTBFInstll = _widg.make_entry(width=100, editable=False)
        self.txtMTBFInstul = _widg.make_entry(width=100, editable=False)
        self.txtMTBFC = _widg.make_entry(width=100, editable=False)
        self.txtMTBFCll = _widg.make_entry(width=100, editable=False)
        self.txtMTBFCul = _widg.make_entry(width=100, editable=False)
        self.txtGoFTrend = _widg.make_entry(width=100, editable=False)
        self.lblGoFModel = _widg.make_label("", width=100)
        self.txtGoFModel = _widg.make_entry(width=100, editable=False)
        self.txtTestTermTime = _widg.make_entry(width=100)

        self.figFigure1 = Figure()
        self.pltPlot1 = FigureCanvas(self.figFigure1)
        self.axAxis1 = self.figFigure1.add_subplot(111)

        self.show_all()

    def create_page(self):                  # pylint: disable=R0914
        """
        Creates the page for displaying the Reliability Growth Test Phase
        details for the selected Growth Test.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HPaned()

        _vbox = gtk.VBox()
        self.pack1(_vbox)
        self.pack2(_hpaned)

        _fxdDataSet = gtk.Fixed()

        _frame = _widg.make_frame(label=_(u""))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fxdDataSet)
        _frame.show_all()

        _vbox.pack_start(_frame, expand=False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwTestAssessment)

        _frame = _widg.make_frame(label=_(u"Reliability Test Data"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)
        _frame.show_all()

        _vbox.pack_end(_frame)

        _fxdNumericalResults = gtk.Fixed()

        _frame = _widg.make_frame(label=_(u"Estimated Parameters"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fxdNumericalResults)
        _frame.show_all()

        _hpaned.pack1(_frame)

        _vbox = gtk.VBox()
        _hpaned.pack2(_vbox)

        _fxdGraphicalResults = gtk.Fixed()

        _vbox.pack_start(_fxdGraphicalResults, expand=False)

        _frame = _widg.make_frame(label=_(u"Reliability Test Plot"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(self.pltPlot1)
        _frame.show_all()

        _vbox.pack_end(_frame)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the labels.
        _labels = [_(u"Cum. Test Time:"), _(u"Cum. Failures:")]
        (_x_max, _y_pos1) = _widg.make_labels(_labels, _fxdNumericalResults,
                                              5, 5)
        _labels = [_(u"Lambda:"), _(u"Beta:"), _(u"Observed Growth Rate:"),
                   _(u"Instantaneous Failure Rate:"),
                   _(u"Cumulative Failure Rate:"), _(u"Instantaneous MTBF:"),
                   _(u"Cumulative MTBF:"), _(u"GoF for Model:")]
        (_x_pos, _y_pos2) = _widg.make_labels(_labels, _fxdNumericalResults, 5,
                                              _y_pos1[1] + 70)
        _x_pos = max(_x_max, _x_pos) + 40
        _y_pos = _y_pos1 + _y_pos2

        # Set the tooltips for the gtk.Widget().
        self.optIndividual.set_tooltip_text(_(u"Estimate parameters based on "
                                              u"individual failure times."))
        self.optGrouped.set_tooltip_text(_(u"Estimate parameters based on "
                                           u"grouped failures times."))
        self.spnConfidence.set_tooltip_text(_(u"Displays the confidence level "
                                              u"level to use for failure "
                                              u"rate/MTBF bounds and goodness "
                                              u"of fit (GoF) tests."))
        self.txtTestTermTime.set_tooltip_text(_(u"For time terminated "
                                                u"(Type II) tests, enter the "
                                                u"test termination time."))

        self.tvwTestAssessment.set_tooltip_text(_(u"Displays the incidents "
                                                  u"associated with the "
                                                  u"selected test plan."))

        self.txtCumTestTime.set_tooltip_text(_(u"Displays the cumulative test "
                                               u"time to date for the "
                                               u"selected test."))
        self.txtCumFailures.set_tooltip_text(_(u"Displays the cumulative "
                                               u"number of failures to date "
                                               u"for the selected test."))
        self.txtScale.set_tooltip_text(_(u"Displays the reliability growth "
                                         u"model estimated scale parameter."))
        self.txtScalell.set_tooltip_text(_(u"Displays the lower bound on the "
                                           u"reliability growth model scale "
                                           u"parameter."))
        self.txtScaleul.set_tooltip_text(_(u"Displays the upper bound on the "
                                           u"reliability growth model scale "
                                           u"parameter."))
        self.txtShape.set_tooltip_text(_(u"Displays the reliability growth "
                                         u"model estimated shape parameter."))
        self.txtShapell.set_tooltip_text(_(u"Displays the lower bound on the "
                                           u"reliability growth model shape "
                                           u"parameter."))
        self.txtShapeul.set_tooltip_text(_(u"Displays the upper bound on the "
                                           u"reliability growth model shape "
                                           u"parameter."))
        self.txtGRActual.set_tooltip_text(_(u"Displays the average growth "
                                            u"rate over the reliability "
                                            u"growth program to date."))
        self.txtGRActualll.set_tooltip_text(_(u"Displays the lower bound "
                                              u"on the average growth "
                                              u"rate over the reliability "
                                              u"growth program to date."))
        self.txtGRActualul.set_tooltip_text(_(u"Displays the upper bound on "
                                              u"the average growth rate over "
                                              u"the reliability growth "
                                              u"program to date."))
        self.txtRhoInst.set_tooltip_text(_(u"Displays the currently assessed "
                                           u"instantaneous failure intensity "
                                           u"(failure rate) of the item under "
                                           u"test."))
        self.txtRhoInstll.set_tooltip_text(_(u"Displays the lower bound on "
                                             u"the instantaneous failure "
                                             u"intensity (failure rate) of "
                                             u"the item under test."))
        self.txtRhoInstul.set_tooltip_text(_(u"Displays the upper bound on "
                                             u"the instantaneous failure "
                                             u"intensity (failure rate) of "
                                             u"the item under test."))
        self.txtRhoC.set_tooltip_text(_(u"Displays the currently assessed "
                                        u"cumulative failure intensity "
                                        u"(failure rate) of the item under "
                                        u"test."))
        self.txtRhoCll.set_tooltip_text(_(u"Displays the lower bound on the "
                                          u"cumulative failure intensity "
                                          u"(failure rate) of the item under "
                                          u"test."))
        self.txtRhoCul.set_tooltip_text(_(u"Displays the upper bound on the "
                                          u"cumulative failure intensity "
                                          u"(failure rate) of the item under "
                                          u"test."))
        self.txtMTBFInst.set_tooltip_text(_(u"Displays the currently assessed "
                                            u"instantaneous MTBF of the item "
                                            u"under test."))
        self.txtMTBFInstll.set_tooltip_text(_(u"Displays the lower bound on "
                                              u"the instantaneous MTBF of the "
                                              u"item under test."))
        self.txtMTBFInstul.set_tooltip_text(_(u"Displays the upper bound on "
                                              u"the instantaneous MTBF of the "
                                              u"item under test."))
        self.txtMTBFC.set_tooltip_text(_(u"Displays the currently assessed "
                                         u"cumulative MTBF of the item under "
                                         u"test."))
        self.txtMTBFCll.set_tooltip_text(_(u"Displays the lower bound on the "
                                           u"cumulative MTBF of the item "
                                           u"under test."))
        self.txtMTBFCul.set_tooltip_text(_(u"Displays the upper bound on the "
                                           u"cumulative MTBF of the item "
                                           u"under test."))
        self.txtGoFTrend.set_tooltip_text(_(u"Displays the critical value for "
                                            u"testing the hypothesis of a "
                                            u"good fit to the selected growth "
                                            u"model."))
        self.txtGoFModel.set_tooltip_text(_(u"Displays the goodness of fit "
                                            u"test statistic for assessing "
                                            u"fit to the selected growth "
                                            u"model.  If this value is less "
                                            u"than the critical value, the "
                                            u"model is a good fit to the "
                                            u"data."))

        self.optMTBF.set_tooltip_text(_(u"If selected, test results will be "
                                        u"displayed as MTBF.  This is the "
                                        u"default."))
        self.optFailureIntensity.set_tooltip_text(_(u"If selected, test "
                                                    u"results will be "
                                                    u"displayed as failure "
                                                    u"intensity (failure "
                                                    u"rate)."))
        self.optLinear.set_tooltip_text(_(u"Select this option to use linear "
                                          u"scales on the reliability growth "
                                          u"plot."))
        self.optLogarithmic.set_tooltip_text(_(u"Select this option to use "
                                               u"logarithmic scales on the "
                                               u"reliability growth plot."))
        self.pltPlot1.set_tooltip_text(_(u"Displays the selected test plan "
                                         u"and observed results."))

        # Position the gtk.Widget() on the page.
        # Place the widgets used to describe the format of the dataset.
        _fxdDataSet.put(self.optIndividual, 5, 5)
        _fxdDataSet.put(self.optGrouped, 5, 35)

        _adjustment = gtk.Adjustment(75.0, 50.0, 100.0, 0.5, 0, 0)
        self.spnConfidence.set_adjustment(_adjustment)
        self.spnConfidence.set_digits(1)

        _label = _widg.make_label(_(u"Confidence:"))
        _fxdDataSet.put(_label, 5, 60)
        _fxdDataSet.put(self.spnConfidence, 250, 60)

        _label = _widg.make_label(_(u"Test Termination Time:"))
        _fxdDataSet.put(_label, 5, 90)
        _fxdDataSet.put(self.txtTestTermTime, 250, 90)

        _label = _widg.make_label(u"")
        _fxdDataSet.put(_label, 5, 115)

        # Place the gtk.TreeView() that will display the reliability test data.
        _labels = [_(u"Record\nNumber"), _(u"Date"), _(u"Interval\nStart"),
                   _(u"Interval\nEnd"), _(u"Number\nof\nFailures")]
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_INT)
        self.tvwTestAssessment.set_model(_model)

        for i in range(5):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 1)
            _cell.set_property('background', 'white')
            _cell.connect('edited', self._on_tree_edited, i, _model)

            _column = gtk.TreeViewColumn()
            _column.set_widget(_widg.make_column_heading(_labels[i]))
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i)
            _column.set_resizable(True)
            if i == 1 or i == 2:
                _datatype = (i, 'gfloat')
            else:
                _datatype = (i, 'gint')
            _column.set_cell_data_func(_cell, _widg.format_cell,
                                       (i, _datatype))
            _column.connect('notify::width', _widg.resize_wrap, _cell)

            self.tvwTestAssessment.append_column(_column)

        # Place the widgets use to display the numerical results of the test
        # data assessment.
        _fxdNumericalResults.put(self.txtCumTestTime, _x_pos, _y_pos[0])
        _fxdNumericalResults.put(self.txtCumFailures, _x_pos, _y_pos[1])

        _label = _widg.make_label(_(u"Lower\nBound"), height=-1, wrap=True,
                                  justify=gtk.JUSTIFY_CENTER)
        _fxdNumericalResults.put(_label, _x_pos + 5, _y_pos[1] + 35)
        _label = _widg.make_label(_(u"\nEstimate"), height=-1, wrap=True,
                                  justify=gtk.JUSTIFY_CENTER)
        _fxdNumericalResults.put(_label, _x_pos + 105, _y_pos[1] + 35)
        _label = _widg.make_label(_(u"Upper\nBound"), height=-1, wrap=True,
                                  justify=gtk.JUSTIFY_CENTER)
        _fxdNumericalResults.put(_label, _x_pos + 205, _y_pos[1] + 35)
        _fxdNumericalResults.put(self.txtScalell, _x_pos, _y_pos[2])
        _fxdNumericalResults.put(self.txtScale, _x_pos + 100, _y_pos[2])
        _fxdNumericalResults.put(self.txtScaleul, _x_pos + 200, _y_pos[2])
        _fxdNumericalResults.put(self.txtShapell, _x_pos, _y_pos[3])
        _fxdNumericalResults.put(self.txtShape, _x_pos + 100, _y_pos[3])
        _fxdNumericalResults.put(self.txtShapeul, _x_pos + 200, _y_pos[3])
        _fxdNumericalResults.put(self.txtGRActualll, _x_pos, _y_pos[4])
        _fxdNumericalResults.put(self.txtGRActual, _x_pos + 100, _y_pos[4])
        _fxdNumericalResults.put(self.txtGRActualul, _x_pos + 200, _y_pos[4])
        _fxdNumericalResults.put(self.txtRhoInstll, _x_pos, _y_pos[5])
        _fxdNumericalResults.put(self.txtRhoInst, _x_pos + 100, _y_pos[5])
        _fxdNumericalResults.put(self.txtRhoInstul, _x_pos + 200, _y_pos[5])
        _fxdNumericalResults.put(self.txtRhoCll, _x_pos, _y_pos[6])
        _fxdNumericalResults.put(self.txtRhoC, _x_pos + 100, _y_pos[6])
        _fxdNumericalResults.put(self.txtRhoCul, _x_pos + 200, _y_pos[6])
        _fxdNumericalResults.put(self.txtMTBFInstll, _x_pos, _y_pos[7])
        _fxdNumericalResults.put(self.txtMTBFInst, _x_pos + 100, _y_pos[7])
        _fxdNumericalResults.put(self.txtMTBFInstul, _x_pos + 200, _y_pos[7])
        _fxdNumericalResults.put(self.txtMTBFCll, _x_pos, _y_pos[8])
        _fxdNumericalResults.put(self.txtMTBFC, _x_pos + 100, _y_pos[8])
        _fxdNumericalResults.put(self.txtMTBFCul, _x_pos + 200, _y_pos[8])
        _fxdNumericalResults.put(self.txtGoFTrend, _x_pos, _y_pos[9])
        _fxdNumericalResults.put(self.txtGoFModel, _x_pos + 100, _y_pos[9])
        _fxdNumericalResults.put(self.lblGoFModel, _x_pos + 205, _y_pos[9])

        # Place the widgets use to display the graphical results of the test
        # data assessment.
        _fxdGraphicalResults.put(self.optLinear, 5, 5)
        _fxdGraphicalResults.put(self.optMTBF, 205, 5)
        _fxdGraphicalResults.put(self.optLogarithmic, 5, 40)
        _fxdGraphicalResults.put(self.optFailureIntensity, 205, 40)

        _label = _widg.make_label(u"")
        _fxdGraphicalResults.put(_label, 5, 75)

        # Connect gtk.Widget() signals to callback functions.
        #self.optIndividual.connect('toggled', self._on_toggled, 22)
        #self.optGrouped.connect('toggled', self._on_toggled, 22)
        self._lst_handler_id.append(
            self.spnConfidence.connect('focus-out-event',
                                       self._on_focus_out, 0))
        #self.spnConfidence.connect('value-changed',
        #                           self._on_spin_value_changed, 26)
        self._lst_handler_id.append(
            self.txtTestTermTime.connect('focus-out-event',
                                         self._on_focus_out, 1))
        #self.optMTBF.connect('toggled', self._on_toggled)
        #self.optFailureIntensity.connect('toggled', self._on_toggled)
        #self.optLinear.connect('toggled', self._on_toggled)
        #self.optLogarithmic.connect('toggled', self._on_toggled)
        self.pltPlot1.mpl_connect('button_press_event', _expand_plot)

        return False

    def load_page(self, model):
        """
        Method to load the Reliability Growth Test Assessment gtk.Notebook()
        page.

        :param model: the :py:class:`rtk.testing.Testing.Model` to load.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._testing_model = model

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Load the individual widgets.
        if model.grouped == 1:
            self.optGrouped.set_active(True)
        else:
            self.optIndividual.set_active(True)

        self.spnConfidence.set_value(model.confidence)
        self.txtCumTestTime.set_text(str(model.cum_time))
        self.txtCumFailures.set_text(str(model.cum_failures))
        self.txtTestTermTime.set_text(str(model.test_termination_time))

        self.txtScalell.set_text(str(fmt.format(model.alpha_hat[0])))
        self.txtScale.set_text(str(fmt.format(model.alpha_hat[1])))
        self.txtScaleul.set_text(str(fmt.format(model.alpha_hat[2])))
        self.txtShapell.set_text(str(fmt.format(model.beta_hat[0])))
        self.txtShape.set_text(str(fmt.format(model.beta_hat[1])))
        self.txtShapeul.set_text(str(fmt.format(model.beta_hat[2])))
        self.txtGRActualll.set_text(str(fmt.format(
            model.lst_o_growth_rate[0])))
        self.txtGRActual.set_text(str(fmt.format(model.lst_o_growth_rate[1])))
        self.txtGRActualul.set_text(str(fmt.format(
            model.lst_o_growth_rate[2])))
        self.txtMTBFInstll.set_text(str(fmt.format(
            model.instantaneous_mean[-1][0])))
        self.txtMTBFInst.set_text(str(fmt.format(
            model.instantaneous_mean[-1][1])))
        self.txtMTBFInstul.set_text(str(fmt.format(
            model.instantaneous_mean[-1][2])))
        self.txtMTBFCll.set_text(str(fmt.format(model.cum_mean[-1][0])))
        self.txtMTBFC.set_text(str(fmt.format(model.cum_mean[-1][1])))
        self.txtMTBFCul.set_text(str(fmt.format(model.cum_mean[-1][2])))
        self.txtGoFTrend.set_text(str(fmt.format(model.cvm_critical_value)))
        self.txtGoFModel.set_text(str(fmt.format(model.cramer_vonmises)))

        try:
            self.txtRhoInstll.set_text(str(
                fmt.format(1.0 / model.instantaneous_mean[-1][2])))
        except ZeroDivisionError:
            self.txtRhoInstll.set_text("0.0")

        try:
            self.txtRhoInst.set_text(str(
                fmt.format(1.0 / model.instantaneous_mean[-1][1])))
        except ZeroDivisionError:
            self.txtRhoInst.set_text("0.0")

        try:
            self.txtRhoInstul.set_text(str(
                fmt.format(1.0 / model.instantaneous_mean[-1][0])))
        except ZeroDivisionError:
            self.txtRhoInstul.set_text("0.0")

        try:
            self.txtRhoCll.set_text(str(
                fmt.format(1.0 / model.cum_mean[-1][2])))
        except ZeroDivisionError:
            self.txtRhoCll.set_text("0.0")

        try:
            self.txtRhoC.set_text(str(
                fmt.format(1.0 / model.cum_mean[-1][1])))
        except ZeroDivisionError:
            self.txtRhoC.set_text("0.0")

        try:
            self.txtRhoCul.set_text(str(
                fmt.format(1.0 / model.cum_mean[-1][0])))
        except ZeroDivisionError:
            self.txtRhoCul.set_text("0.0")

        self._load_treeview()
        #self._load_plot()

        return False

    def _load_treeview(self):
        """
        Method to load the Testing class actual test data gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        try:
            _n_records = len(self._testing_model.dic_test_data.keys())
        except TypeError:
            _n_records = 0

        _model = self.tvwTestAssessment.get_model()
        _model.clear()
        for i in range(_n_records):
            _date = str(datetime.fromordinal(
                int(self._testing_model.dic_test_data[i][0])).strftime('%Y-%m-%d'))
            _model.append([i, _date, self._testing_model.dic_test_data[i][1],
                           self._testing_model.dic_test_data[i][2],
                           self._testing_model.dic_test_data[i][3]])

        self.tvwTestAssessment.set_cursor('0', None, False)
        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            _col = self.tvwTestAssessment.get_column(0)
            self.tvwTestAssessment.row_activated(_path, _col)

        return False

    def _load_plot(self):                   # pylint: disable=R0914
        """
        Method to load the Reliability Growth plot.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        if self._testing_model.ttt <= 0.0:
            self._testing_model.ttt = [x[2] for x in
                                       self._testing_model.dic_test_data.values()][-1]

        _ideal = self._testing_model.calculate_idealized_growth_curve()
        _plan = []
        for i in range(self._testing_model.n_phases):
            _plan = _plan + self._testing_model.create_planned_values(i)

        if self.optMTBF.get_active():
            _targets = self._testing_model.lst_p_mtbfa
        elif self.optFailureIntensity.get_active():
            _ideal = [1.0 / _mtbf for _mtbf in _ideal]
            _plan = [1.0 / _mtbf for _mtbf in _plan]
            _targets = [1.0 / _mtbfa
                        for _mtbfa in self._testing_model.lst_p_mtbfa]

        # Plot all the information.
        self.axAxis1.cla()

        # Plot the observed instantaneous MTBF values and bounds if there are
        # any observed values.
        if len([x[2] for x in self._testing_model.dic_test_data.values()]) > 3:
            # Update the left interval time using the previous record's right
            # interval value if the data is grouped.  Create a list of observed
            # cumulative failure times to use when plotting the results.
            _f_time = 0.0
            _obs_times = []
            _model = self.tvwTestAssessment.get_model()
            _row = _model.get_iter_root()
            while _row is not None:
                if self.optGrouped.get_active():
                    _model.set_value(_row, 2, _f_time)
                    _f_time = _model.get_value(_row, 3)
                    _obs_times.append(_f_time)
                else:
                    _record_id = _model.get_value(_row, 0)
                    _f_time = _model.get_value(_row, 3)
                    _model.set_value(_row, 2, _f_time)
                    _obs_times.append(_f_time)
                    self._testing_model.dic_test_data[_record_id][1] = _f_time

                _row = _model.iter_next(_row)

            if self.optMTBF.get_active():
                _obsll = np.array([y[1] - y[0]
                                   for y in self._testing_model.cum_mean])
                _obspt = np.array([y[1]
                                   for y in self._testing_model.cum_mean])
                _obsul = np.array([y[2] - y[1]
                                   for y in self._testing_model.cum_mean])
            elif self.optFailureIntensity.get_active():
                _obsll = np.array([1.0 / y[0] - 1.0 / y[1]
                                   for y in self._testing_model.cum_mean])
                _obspt = np.array([1.0 / y[1]
                                   for y in self._testing_model.cum_mean])
                _obsul = np.array([1.0 / y[1] - 1.0 / y[2]
                                   for y in self._testing_model.cum_mean])

            _obsll[np.isnan(_obsll)] = 0.0
            _obsll[np.isinf(_obsll)] = 0.0
            _obsll[np.where(_obsll) < 0.0] = 0.0
            _obspt[np.isnan(_obspt)] = 0.0
            _obspt[np.isinf(_obspt)] = 0.0
            _obsul[np.isnan(_obsul)] = 0.0
            _obsul[np.isinf(_obsul)] = 0.0

            # Find the minimum and maximum y-value.
            _y_min = max(0.0, min(_obsll), min(_obsul))
            _y_max = max(max(_targets), max(_obsll), max(_obspt),
                         max(_obsul), max(_ideal), max(_plan))

            # Plot the observed values with error bars indicating bounds at
            # each observation.
            self.axAxis1.errorbar(_obs_times, _obspt, yerr=[_obsll, _obsul],
                                  fmt='o', ecolor='k', color='k')

            # Create the legend text.
            _legend = tuple([_(u"Observed w/ {0:0.1f}% Error "
                               u"Bars".format(self._testing_model.confidence)),
                             _(u"Idealized Growth Curve"),
                             _(u"Planned Growth Curve"), _(u"Target Values")])

        else:
            # Create the legend text.
            _legend = tuple([_(u"Idealized Growth Curve"),
                             _(u"Planned Growth Curve"), _(u"Target Values")])

            # Find the minimum and maximum y-value.
            _y_min = min(0.0, min(_targets), min(_ideal), min(_plan))
            _y_max = max(max(_targets), max(_ideal), max(_plan))

        # Add the _idealized growth curve.
        _times = [_t for _t in range(int(self._testing_model.ttt))]
        _line = matplotlib.lines.Line2D(_times, _ideal, lw=1.5, color='b')
        self.axAxis1.add_line(_line)

        # Add the _planned growth curve.
        _line = matplotlib.lines.Line2D(_times, _plan, lw=1.5, color='r')
        self.axAxis1.add_line(_line)

        # Show the target values on the plot.
        for i in range(len(_targets)):
            self.axAxis1.axhline(y=_targets[i], xmin=0, color='m',
                                 linewidth=2.5, linestyle=':')
        if self.optLogarithmic.get_active():
            self.axAxis1.set_xscale('log')
            self.axAxis1.set_yscale('log')
        else:
            self.axAxis1.set_xscale('linear')
            self.axAxis1.set_yscale('linear')

        for i in range(len(_targets)):
            self.axAxis1.annotate(str(fmt.format(_targets[i])),
                                  xy=(self._testing_model.ttt, _targets[i]),
                                  xycoords='data',
                                  xytext=(25, -25),
                                  textcoords='offset points',
                                  size=12, va="center",
                                  bbox=dict(boxstyle="round",
                                            fc='#E5E5E5',
                                            ec='None',
                                            alpha=0.5),
                                  arrowprops=dict(
                                      arrowstyle="wedge,tail_width=1.",
                                      fc='#E5E5E5', ec='None',
                                      alpha=0.5,
                                      patchA=None,
                                      patchB=Ellipse((2, -1), 0.5, 0.5),
                                      relpos=(0.5, 0.5)))

        # Create and place the legend.
        _leg = self.axAxis1.legend(_legend, 'upper left', shadow=True)
        for _text in _leg.get_texts():
            _text.set_fontsize('small')
        for _line in _leg.get_lines():
            _line.set_linewidth(0.5)

        # Add labels to the axes and adjust them slightly for readability.
        self.axAxis1.set_xlabel(_(u"Cumulative Test Time"))
        if self.optMTBF.get_active():
            self.axAxis1.set_ylabel(u"MTBF")
        elif self.optFailureIntensity.get_active():
            self.axAxis1.set_ylabel(_(u"Failure Intensity"))
        self.axAxis1.set_xlim(right=1.1 * self._testing_model.ttt)
        self.axAxis1.set_ylim(bottom=0.0, top=1.05 * _y_max)
        self.pltPlot1.draw()

        return False

    def _on_tree_edited(self, cell, path, new_text, position, model):
        """
        Called whenever a gtk.TreeView() gtk.CellRenderer() is edited.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that
                         was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _convert = gobject.type_name(model.get_column_type(position))

        if new_text is None:
            model[path][position] = not cell.get_active()
        elif _convert == 'gchararray':
            model[path][position] = str(new_text)
        elif _convert == 'gint':
            model[path][position] = int(new_text)
        elif _convert == 'gfloat':
            model[path][position] = float(new_text)

        _record_id = model[path][0]
        if position == 1:                   # Date
            _date = datetime.strptime(new_text, "%Y-%m-%d").toordinal()
            self._testing_model.dic_test_data[_record_id][0] = _date
        elif position == 2:                 # Failure start time
            self._testing_model.dic_test_data[_record_id][1] = float(new_text)
        elif position == 3:                 # Failure end time
            self._testing_model.dic_test_data[_record_id][2] = float(new_text)
        elif position == 4:                 # Number of failures
            self._testing_model.dic_test_data[_record_id][3] = int(new_text)

        return False

    def on_button_clicked(self, __button, __event, index):
        """
        Responds to gtk.Button() clicked signals and calls the correct function
        or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if index == 0:
            AddRGRecord(self.dtcGrowth, self._testing_model)
        elif index == 1:
            (_model,
             _row) = self.tvwTestAssessment.get_selection().get_selected()
            _record_id = _model.get_value(_row, 0)
            self.dtcGrowth.delete_test_record(_record_id,
                                              self._testing_model.test_id)
            self._testing_model.dic_test_data.pop(_record_id)
            self._load_treeview()
        elif index == 2:
            self._testing_model.estimate_crow_amsaa()
            self._testing_model.calculate_crow_amsaa_mean()
            self._testing_model.assess_growth_rate()
            if not self.optGrouped.get_active():
                self._testing_model.calculate_cramer_vonmises()
                if(self._testing_model.cramer_vonmises <
                   self._testing_model.cvm_critical_value):
                    self.lblGoFModel.set_markup(_(u"<span foreground='green'>"
                                                  u"Good Fit</span>"))
                else:
                    self.lblGoFModel.set_markup(_(u"<span foreground='red'>"
                                                  u"Poor Fit</span>"))
            if self.optGrouped.get_active():
                self._testing_model.calculate_chi_square()
                if(self._testing_model.chi_square >
                   self._testing_model.chi2_critical_value[0] and
                   self._testing_model.chi_square <
                   self._testing_model.chi2_critical_value[1]):
                    self.lblGoFModel.set_markup(_(u"<span foreground='green'>"
                                                  u"Good Fit</span>"))
                else:
                    self.lblGoFModel.set_markup(_(u"<span foreground='red'>"
                                                  u"Poor Fit</span>"))

            self.load_page(self._testing_model)
            self._load_plot()

        return False

    def _on_focus_out(self, entry, __event, index):     # pylint: disable=R0912
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

        if index == 0:                      # Statistical confidence
            self._testing_model.confidence = float(entry.get_text())
        elif index == 1:
            self._testing_model.test_termination_time = float(entry.get_text())

        entry.handler_unblock(self._lst_handler_id[index])

        return False
