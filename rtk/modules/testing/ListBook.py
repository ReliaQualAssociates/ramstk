#!/usr/bin/env python
"""
##############################
Testing Package List Book View
##############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.testing.ListBook.py is part of the RTK Project
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
from datetime import datetime

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
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
    from testing.Assistants import AddRGRecord
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets
    from rtk.testing.Assistants import AddRGRecord

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ListView(gtk.VBox):
    """
    The List Book view displays all the matrices and lists associated with the
    Testing Class.  The attributes of a Testing List Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Testing attribute.

    +----------+--------------------------------------------+
    | Position | Widget - Signal                            |
    +==========+============================================+
    |     0    | btnCalcRisk - 'clicked'                    |
    +----------+--------------------------------------------+
    |     1    | btnSaveTest - 'clicked'                    |
    +----------+--------------------------------------------+

    :ivar _mdcRTK: the :py:class:`rtk.RTK.RTK` master data controller.
    :ivar _model: the :py:class:`rtk.testing.Testing.Model` data model to
                  display.
    :ivar gtk.Button btnCalcRisk: the gtk.Button() to request the Testing risk
                                  matrix be calculated.
    :ivar gtk.Button btnSaveTest: the gtk.Button() to request the Testing test
                                  technique selections be saved.
    :ivar gtk.Frame fraTestSelection: the gtk.Frame() to hold the Testing test
                                      technique selection gtk.ScrolledWindow()
                                      for the selected Testing module.
    :ivar gtk.ScrolledWindow scwCSCITestSelection: the gtk.ScrolledWindow() to
                                                   hold the gtk.TreeView() for
                                                   the Testing CSCI test
                                                   selection matrix.
    :ivar gtk.ScrolledWindow scwUnitTestSelection: the gtk.ScrolledWindow() to
                                                   hold the gtk.TreeView() for
                                                   the Testing unit test
                                                   selection matrix.
    :ivar gtk.TreeView tvwRiskMap: the gtk.TreeView() to display the Testing
                                   risk matrix.
    """

    def __init__(self, modulebook):
        """
        Method to initialize the List Book view for the Testing package.

        :param modulebook: the :py:class:`rtk.testing.ModuleBook` to associate
                           with this List Book.
        """

        gtk.VBox.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._mdcRTK = modulebook.mdcRTK
        self._testing_model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.btnAddRecord = Widgets.make_button(width=35, image='add')
        self.btnDeleteRecord = Widgets.make_button(width=35, image='remove')
        self.btnSave = Widgets.make_button(width=35, image='save')

        self.tvwRGTestPlan = gtk.TreeView()
        self.tvwRGTestFeasibility = gtk.TreeView()
        self.tvwRGTestAssessment = gtk.TreeView()

        # Set tooltips for the gtk.Widgets().
        self.btnAddRecord.set_tooltip_markup(
            _(u"Launches the Add Record "
              u"wizard to allow the user to "
              u"add a new incident record to "
              u"the selected reliability "
              u"growth test."))
        self.btnDeleteRecord.set_tooltip_markup(
            _(u"Deletes the selected "
              u"records from the list of "
              u"incidents associated with "
              u"the selected reliability "
              u"growth test."))
        self.btnSave.set_tooltip_markup(_(u"Saves the selected record set."))
        self.tvwRGTestPlan.set_tooltip_markup(
            _(u"Displays the details of the "
              u"reliability growth plan.  "
              u"Right click any date field "
              u"to show the calendar."))
        self.tvwRGTestFeasibility.set_tooltip_markup(
            _(u"Displays the "
              u"feasibility of the "
              u"reliability growth "
              u"plan.  Right click "
              u"any date field to "
              u"show the calendar."))
        self.tvwRGTestAssessment.set_tooltip_text(
            _(u"Displays the incidents "
              u"associated with the "
              u"selected test plan."))

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.btnAddRecord.connect('button-release-event',
                                      self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnDeleteRecord.connect('button-release-event',
                                         self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnSave.connect('button-release-event',
                                 self._on_button_clicked, 2))

        # self.tvwRGTestPlan.connect('button_press_event',
        #                            self._on_button_clicked, 0)
        # self.tvwRGTestFeasibility.connect('button_press_event',
        #                                   self.on_button_clicked, 1)
        # self.tvwRGAssessment.connect('button_press_event',
        #                              self.on_button_clicked, 2)

        # Put it all together.
        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_notebook(self):
        """
        Method to create the Testing class List View gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[1] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_rg_test_plan_page(_notebook)
        self._create_rg_feasibility_page(_notebook)
        self._create_rg_assessment_page(_notebook)

        return _notebook

    def _create_rg_test_plan_page(self, notebook):
        """
        Method to create the Reliability Growth Test plan details page in the
        List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Testing Risk matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        # _bbox.pack_start(self.btnCalcRisk, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwRGTestPlan)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Create the Growth Testing gtk.TreeView().  Fields listed as
        # calculated are calculated using the ideal growth model.
        # =============================================================== #
        # Reliability Growth Testing Detailed Inputs
        #    0. Test Phase
        #    1. Calendar Start Date (editable)
        #    2. Calendar End Date (editable)
        #    3. Total Test Time During Phase (editable)
        #    4. Cumulative Test Time Through Phase
        #    5. Ideal Initial Phase MTBF (calculated)
        #    6. Ideal Average Phase MTBF (calculated)
        #    7. Ideal Final Phase MTBF (calculated)
        #    8. Expected Number of Failures During Phase (calculated)
        #    9. Number of Test Articles (editable)
        #   10. Planned Initial Phase MTBF (editable)
        #   11. Planned Average Phase MTBF (editable)
        #   12. Planned Final Phase MTBF (editable)
        # =============================================================== #
        _labels = [
            _(u"Phase"),
            _(u"Start Date"),
            _(u"End Date"),
            _(u"Phase\nTest\nTime"),
            _(u"Cumulative\nTest Time"),
            _(u"Ideal\nInitial\nMTBF"),
            _(u"Ideal\nAverage\nMTBF"),
            _(u"Ideal\nFinal\nMTBF"),
            _(u"Expected\nNumber of\nFailures"),
            _(u"Test\nArticles"),
            _(u"Planned\nInitial\nMTBF"),
            _(u"Planned\nAverage\nMTBF"),
            _(u"Planned\nFinal\nMTBF")
        ]
        _model = gtk.ListStore(
            gobject.TYPE_INT, gobject.TYPE_STRING, gobject.TYPE_STRING,
            gobject.TYPE_FLOAT, gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
            gobject.TYPE_FLOAT, gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
            gobject.TYPE_INT, gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
            gobject.TYPE_FLOAT)
        self.tvwRGTestPlan.set_model(_model)

        for _index, _label in enumerate(_labels):
            if _index in [0, 4, 5, 6, 7, 8]:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'light gray')
            else:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.connect('edited', self._on_plan_edited, _index)

            _column = gtk.TreeViewColumn()
            _column.set_widget(Widgets.make_column_heading(_label))
            _column.pack_start(_cell, True)
            _column.set_resizable(True)
            if _index in [0, 8, 9]:
                _datatype = (_index, 'gint')
            elif _index in [1, 2]:
                _datatype = (_index, 'gchararray')
            else:
                _datatype = (_index, 'gfloat')
            _column.set_attributes(_cell, text=_index)
            _column.set_cell_data_func(_cell, Widgets.format_cell,
                                       (_index, _datatype))
            _column.connect('notify::width', Widgets.resize_wrap, _cell)

            self.tvwRGTestPlan.append_column(_column)

        # Add the RG Test Plan page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Test\nPlan\nDetails</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the reliability growth test "
              u"plan details."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_rg_feasibility_page(self, notebook):
        """
        Method to create the Reliability Growth Test plan feasibility page in
        the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Testing Risk matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        # _bbox.pack_start(self.btnCalcRisk, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwRGTestFeasibility)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Create the RG Test Feasibility gtk.TreeView().  Fields listed as
        # calculated are calculated using the ideal growth model.
        # =============================================================== #
        # Reliability Growth Test Feasibility
        #    0. Test Phase
        #    1. Calendar Start Date (editable)
        #    2. Calendar End Date (editable)
        #    3. Number of Test Articles (editable)
        #    4. Expected Number of Failures During Phase (calculated)
        #    5. Management Strategy Required During Phase (editable)
        #    6. Average FEF Required During Phase (editable)
        #    7. Probability of Observing at Least One Failure (editable)
        #    8. Test Time per Test Unit (calculated)
        #    9. Test Time per Test Unit per Week (calculated)
        # =============================================================== #
        _labels = [
            _(u"Phase"),
            _(u"Start Date"),
            _(u"End Date"),
            _(u"Number of\nTest\nArticles"),
            _(u"Expected\nNumber\nof\nFailures"),
            _(u"Required\nManagement\nStrategy"),
            _(u"Required\nAverage\nFEF"),
            _(u"Probability\nof Observing\nFailure"),
            _(u"Test Time\nper Unit"),
            _(u"Test Time\nper Unit\nper Week")
        ]
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwRGTestFeasibility.set_model(_model)

        for _index, _label in enumerate(_labels):
            _cell = gtk.CellRendererText()
            if _index in [0, 4, 8, 9]:
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'light gray')
            else:
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.connect('edited', self._on_feasibility_edited, _index)

            _column = gtk.TreeViewColumn()
            _column.set_widget(Widgets.make_column_heading(_label))
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)
            _column.set_resizable(True)
            if _index > 3:
                _datatype = (_index, 'gfloat')
            else:
                _datatype = (_index, 'gint')
            _column.set_cell_data_func(_cell, Widgets.format_cell,
                                       (_index, _datatype))
            _column.connect('notify::width', Widgets.resize_wrap, _cell)
            self.tvwRGTestFeasibility.append_column(_column)

        # Add the RG Test Feasibility page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(
            _(u"<span weight='bold'>" + "Test\nPlan\nFeasibility</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the reliability growth test "
              u"plan feasibility."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_rg_assessment_page(self, notebook):
        """
        Method to create the Reliability Growth Test assessment page in the
        List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Testing Risk matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnAddRecord, False, False)
        _bbox.pack_start(self.btnDeleteRecord, False, False)
        _bbox.pack_end(self.btnSave, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwRGTestAssessment)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Create the RG Test Feasibility gtk.TreeView().  Fields listed as
        # calculated are calculated using the ideal growth model.
        # =============================================================== #
        # Reliability Growth Test Feasibility
        #    0. Record Number
        #    1. Incident Date (editable)
        #    2. Start of Interval (editable)
        #    3. End of Interval (editable)
        #    4. Number of Failures During Interval (editable)
        # =============================================================== #
        _labels = [
            _(u"Record\nNumber"),
            _(u"Date"),
            _(u"Interval\nStart"),
            _(u"Interval\nEnd"),
            _(u"Number\nof\nFailures")
        ]
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_INT)
        self.tvwRGTestAssessment.set_model(_model)

        for i in range(5):
            _cell = gtk.CellRendererText()
            if i == 0:
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'light gray')
            else:
                _cell.set_property('editable', 1)
                _cell.set_property('background', 'white')
                _cell.connect('edited', self._on_assessment_edited, i, _model)

            _column = gtk.TreeViewColumn()
            _column.set_widget(Widgets.make_column_heading(_labels[i]))
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i)
            _column.set_resizable(True)
            if i in [2, 3]:
                _datatype = (i, 'gfloat')
            elif i == 4:
                _datatype = (i, 'gint')
            else:
                _datatype = (i, 'gstring')
            _column.set_cell_data_func(_cell, Widgets.format_cell,
                                       (i, _datatype))
            _column.connect('notify::width', Widgets.resize_wrap, _cell)

            self.tvwRGTestAssessment.append_column(_column)

        # Add the RG Test Feasibility page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(
            _(u"<span weight='bold'>" + "Test\nIncidents</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the reliability growth test "
              u"incidents."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def add_test_phase(self, phase_id):
        """
        Method to add a test phase to the Reliability Growth plan details
        gtk.TreeView() and the Reliability Growth feasibility gtk.TreeView().

        :param int phase_id: the ID of the newly added phase.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _date = datetime.today().strftime('%Y-%m-%d')

        # Add the test phase to the RG plan details.
        _data = [
            phase_id, _date, _date, 0.0,
            sum(self._testing_model.lst_p_test_time), 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ]
        _model = self.tvwRGTestPlan.get_model()
        _model.append(_data)

        # Add the test phase to the RG plan feasibility table.
        _data = [phase_id, _date, _date, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        _model = self.tvwRGTestFeasibility.get_model()
        _model.append(_data)

        return _return

    def delete_test_phase(self, phase_id):
        """
        Method to delete the last test phase from the Reliability Growth plan
        details gtk.TreeView() and the Reliability Growth feasibility
        gtk.TreeView().

        :param int phase_id: the ID of the phase to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # Delete the test phase from the RG plan details.
        _model = self.tvwRGTestPlan.get_model()
        _row = _model.get_iter_root()
        while _row is not None:
            if _model.get_value(_row, 0) == phase_id:
                _model.remove(_row)
                _row = None
            else:
                _row = _model.iter_next(_row)

        # Delete the test phase from the RG plan feasibility table.
        _model = self.tvwRGTestFeasibility.get_model()
        _row = _model.get_iter_root()
        while _row is not None:
            if _model.get_value(_row, 0) == phase_id:
                _model.remove(_row)
                _row = None
            else:
                _row = _model.iter_next(_row)

        return _return

    def load(self, model):
        """
        Method to load the Testing List Book.

        :param model: the :py:class:`rtk.testing.growth.Growth.Model` whose
                      attributes are loaded.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._testing_model = model

        self._load_rg_plan_details()
        self._load_rg_feasibility_details()
        self.load_rg_assessment_details()

        return False

    def _load_rg_plan_details(self):
        """
        Method to load the Reliability Growth Plan details into the
        gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwRGTestPlan.get_model()
        _model.clear()
        for i in range(self._testing_model.n_phases):
            try:
                _dt_start = str(
                    datetime.fromordinal(
                        int(self._testing_model.lst_p_start_date[i])).strftime(
                            '%Y-%m-%d'))
            except (TypeError, ValueError):
                _dt_start = datetime.today().strftime('%Y-%m-%d')
                _dt_start = datetime.strptime(_dt_start,
                                              "%Y-%m-%d").toordinal()
                self._testing_model.lst_p_start_date[i] = _dt_start
            try:
                _dt_end = str(
                    datetime.fromordinal(
                        int(self._testing_model.lst_p_end_date[i])).strftime(
                            '%Y-%m-%d'))
            except (TypeError, ValueError):
                _dt_end = datetime.today().strftime('%Y-%m-%d')
                _dt_end = datetime.strptime(_dt_end, "%Y-%m-%d").toordinal()
                self._testing_model.lst_p_end_date[i] = _dt_end

            _data = [
                i + 1, _dt_start, _dt_end,
                self._testing_model.lst_p_test_time[i],
                sum(self._testing_model.lst_p_test_time[:i + 1]),
                self._testing_model.lst_i_mtbfi[i],
                self._testing_model.lst_i_mtbfa[i],
                self._testing_model.lst_i_mtbff[i],
                self._testing_model.lst_i_n_failures[i],
                self._testing_model.lst_p_n_test_units[i],
                self._testing_model.lst_p_mtbfi[i],
                self._testing_model.lst_p_mtbfa[i],
                self._testing_model.lst_p_mtbff[i]
            ]
            _model.append(_data)

        return False

    def _load_rg_feasibility_details(self):
        """
        Method to load the Reliability Growth Feasibility details into the
        gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwRGTestFeasibility.get_model()
        _model.clear()

        for i in range(self._testing_model.n_phases):
            try:
                _dt_start = str(
                    datetime.fromordinal(
                        int(self._testing_model.lst_p_start_date[i])).strftime(
                            '%Y-%m-%d'))
            except TypeError:
                _dt_start = datetime.today().strftime('%Y-%m-%d')
            try:
                _dt_end = str(
                    datetime.fromordinal(
                        int(self._testing_model.lst_p_end_date[i])).strftime(
                            '%Y-%m-%d'))
            except TypeError:
                _dt_end = datetime.today().strftime('%Y-%m-%d')

            _data = [
                i + 1, _dt_start, _dt_end,
                self._testing_model.lst_p_n_test_units[i],
                self._testing_model.lst_i_n_failures[i],
                self._testing_model.lst_p_ms[i],
                self._testing_model.lst_p_fef[i],
                self._testing_model.lst_p_prob[i],
                self._testing_model.lst_p_tpu[i],
                self._testing_model.lst_p_tpupw[i]
            ]
            _model.append(_data)

        self.tvwRGTestFeasibility.expand_all()
        self.tvwRGTestFeasibility.set_cursor('0', None, False)
        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            _col = self.tvwRGTestFeasibility.get_column(0)
            self.tvwRGTestFeasibility.row_activated(_path, _col)

        return False

    def load_rg_assessment_details(self):
        """
        Method to load the Reliability Growth Test assessment gtk.TreeView()
        with the actual test incidents.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _model = self.tvwRGTestAssessment.get_model()
        _model.clear()
        for _key in self._testing_model.dic_test_data.keys():
            _record = self._testing_model.dic_test_data[_key]
            _date = str(datetime.fromordinal(_record[1]).strftime('%Y-%m-%d'))
            _model.append(
                [_key + 1, _date, _record[2], _record[3], _record[4]])

        self.tvwRGTestAssessment.set_cursor('0', None, False)
        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            _col = self.tvwRGTestAssessment.get_column(0)
            self.tvwRGTestAssessment.row_activated(_path, _col)

        return False

    def _on_plan_edited(self, cell, path, new_text, index):
        """
        Method to respond to gtk.CellRenderer() 'edited' signals in the
        Reliability Growth plan details gtk.TreeView().

        :param gtk.CellRenderer cell:
        :param str path:
        :param str new_text:
        :param int index:
        :return: False if successful or True if an error is encountered
        :rtype: bool
        """

        _model = self.tvwRGTestPlan.get_model()
        _row = _model.get_iter_from_string(path)

        Widgets.edit_tree(cell, path, new_text, index, _model)

        if _row is not None:
            _dt_start = datetime.strptime(
                _model.get_value(_row, 1), "%Y-%m-%d").toordinal()
            _dt_end = datetime.strptime(_model.get_value(_row, 2),
                                        "%Y-%m-%d").toordinal()
            _test_time = _model.get_value(_row, 3)
            _articles = _model.get_value(_row, 9)
            _mtbfi = _model.get_value(_row, 10)
            _mtbfa = _model.get_value(_row, 11)
            _mtbff = _model.get_value(_row, 12)

            # Update the lists containing the Reliability Growth Plan details.
            _phase_id = _model.get_value(_row, 0) - 1
            self._testing_model.lst_p_start_date[_phase_id] = _dt_start
            self._testing_model.lst_p_end_date[_phase_id] = _dt_end
            self._testing_model.lst_p_test_time[_phase_id] = _test_time
            self._testing_model.lst_p_n_test_units[_phase_id] = _articles
            self._testing_model.lst_p_mtbfi[_phase_id] = _mtbfi
            self._testing_model.lst_p_mtbfa[_phase_id] = _mtbfa
            self._testing_model.lst_p_mtbff[_phase_id] = _mtbff

            _row2 = _row
            while _row2 is not None:
                _phase_id = _model.get_value(_row2, 0) - 1
                _cum_time = sum(
                    self._testing_model.lst_p_test_time[:_phase_id + 1])
                _model.set_value(_row2, 4, _cum_time)
                _row2 = _model.iter_next(_row2)

            self._testing_model.ttt = _cum_time

        return False

    def _on_feasibility_edited(self, cell, path, new_text, index):
        """
        Method to respond to gtk.CellRenderer() 'edited' signals in the
        Reliability Growth plan feasibility gtk.TreeView().

        :param gtk.CellRenderer cell:
        :param str path:
        :param str new_text:
        :param int index:
        :return: False if successful or True if an error is encountered
        :rtype: bool
        """

        _model = self.tvwRGTestFeasibility.get_model()
        _row = _model.get_iter_from_string(path)

        Widgets.edit_tree(cell, path, new_text, index, _model)

        if _row is not None:
            _dt_start = datetime.strptime(
                _model.get_value(_row, 1), "%Y-%m-%d").toordinal()
            _dt_end = datetime.strptime(_model.get_value(_row, 2),
                                        "%Y-%m-%d").toordinal()
            _articles = _model.get_value(_row, 3)
            _ms = _model.get_value(_row, 5)
            _fef = _model.get_value(_row, 6)
            _prob = _model.get_value(_row, 7)

            # Update the lists containing the RG Plan feasibility attributes.
            _phase_id = _model.get_value(_row, 0) - 1
            self._testing_model.lst_p_start_date[_phase_id] = _dt_start
            self._testing_model.lst_p_end_date[_phase_id] = _dt_end
            self._testing_model.lst_p_n_test_units[_phase_id] = _articles
            self._testing_model.lst_p_ms[_phase_id] = _ms
            self._testing_model.lst_p_fef[_phase_id] = _fef
            self._testing_model.lst_p_prob[_phase_id] = _prob

        return False

    def _on_assessment_edited(self, cell, path, new_text, position, model):
        """
        Method to respond to gtk.CellRenderer() 'edited' signals in the
        Reliability Growth assessment gtk.TreeView().

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

        if position == 1:  # Date
            _date = datetime.strptime(new_text, "%Y-%m-%d").toordinal()
            self._testing_model.dic_test_data[_record_id - 1][1] = _date
        elif position == 2:  # Failure start time
            self._testing_model.dic_test_data[_record_id -
                                              1][2] = float(new_text)
        elif position == 3:  # Failure end time
            self._testing_model.dic_test_data[_record_id -
                                              1][3] = float(new_text)
        elif position == 4:  # Number of failures
            self._testing_model.dic_test_data[_record_id -
                                              1][4] = int(new_text)

        return False

    def _on_button_clicked(self, button, __event, index):
        """
        Method to respond to gtk.Button() 'button-release-event' signals and
        call the correct function or method, passing any parameters as needed.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if index == 0:
            AddRGRecord(self._mdcRTK.dtcGrowth, self._testing_model, self)
        elif index == 1:
            (_model,
             _row) = self.tvwRGTestAssessment.get_selection().get_selected()
            _record_id = _model.get_value(_row, 0)
            _test_id = self._testing_model.test_id
            self._mdcRTK.dtcGrowth.delete_test_record(_record_id - 1, _test_id)
            self._testing_model.dic_test_data.pop(_record_id - 1)
            _model.remove(_row)
        elif index == 2:
            self._mdcRTK.dtcGrowth.save_test_data(self._testing_model.test_id)

        button.handler_unblock(self._lst_handler_id[index])

        return False
