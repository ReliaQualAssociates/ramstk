#!/usr/bin/env python
"""
##############################
Survival Package List Book View
##############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.ListBook.py is part of the RTK Project
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
from datetime import date, datetime

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
import pango
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
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets

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
    Survival Class.  The attributes of a Survival List Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Survival attribute.

    +----------+--------------------------------------------+
    | Position | Widget - Signal                            |
    +==========+============================================+
    |     0    | btnCalcRisk - 'clicked'                    |
    +----------+--------------------------------------------+
    |     1    | btnSaveTest - 'clicked'                    |
    +----------+--------------------------------------------+

    :ivar _mdcRTK: the :py:class:`rtk.RTK.RTK` master data controller.
    :ivar _model: the :py:class:`rtk.survival.Survival.Model` data model to
                  display.
    :ivar gtk.Button btnCalcRisk: the gtk.Button() to request the Survival risk
                                  matrix be calculated.
    :ivar gtk.Button btnSaveTest: the gtk.Button() to request the Survival test
                                  technique selections be saved.
    :ivar gtk.Frame fraTestSelection: the gtk.Frame() to hold the Survival test
                                      technique selection gtk.ScrolledWindow()
                                      for the selected Survival module.
    :ivar gtk.ScrolledWindow scwCSCITestSelection: the gtk.ScrolledWindow() to
                                                   hold the gtk.TreeView() for
                                                   the Survival CSCI test
                                                   selection matrix.
    :ivar gtk.ScrolledWindow scwUnitTestSelection: the gtk.ScrolledWindow() to
                                                   hold the gtk.TreeView() for
                                                   the Survival unit test
                                                   selection matrix.
    :ivar gtk.TreeView tvwRiskMap: the gtk.TreeView() to display the Survival
                                   risk matrix.
    """

    def __init__(self, modulebook):
        """
        Method to initialize the List Book view for the Survival package.

        :param modulebook: the :py:class:`rtk.survival.ModuleBook` to associate
                           with this List Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_status = [
            "",
            _(u"Event"),
            _(u"Right Censored"),
            _(u"Left Censored"),
            _(u"Interval Censored")
        ]
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRTK = modulebook.mdcRTK
        self._survival_model = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnAddRecord = Widgets.make_button(width=35, image='add')
        self.btnDeleteRecord = Widgets.make_button(width=35, image='remove')
        self.btnConsolidate = Widgets.make_button(
            width=35, image='insert-assembly')
        self.btnCalculate = Widgets.make_button(width=35, image='calculate')
        self.btnSave = Widgets.make_button(width=35, image='save')
        self.btnAssignAssembly = Widgets.make_button(width=35, image="assign")
        self.btnAssignComponent = Widgets.make_button(width=35, image="assign")

        self.chkGrouped = Widgets.make_check_button(
            label=_(u"Failure data is "
                    u"grouped"))

        self.tvwSurvivalRecords = gtk.TreeView()
        self.tvwNevadaChart = gtk.TreeView()
        self.tvwResultsByChildAssembly = gtk.TreeView()
        self.tvwResultsByPart = gtk.TreeView()

        # Set tooltips for the gtk.Widgets().
        self.btnAddRecord.set_tooltip_markup(
            _(u"Launches the Add Record "
              u"wizard to allow the user to "
              u"add a new incident record to "
              u"the selected survival "
              u"analysis."))
        self.btnDeleteRecord.set_tooltip_markup(
            _(u"Deletes the selected "
              u"records from the list of "
              u"incidents associated with "
              u"the selected survival "
              u"analysis."))
        self.btnCalculate.set_tooltip_text(
            _(u"Calculates interarrival times "
              u"for the selected dataset."))
        self.btnSave.set_tooltip_markup(_(u"Saves the selected record set."))
        self.btnAssignAssembly.set_tooltip_markup(
            _(u"Assigns results to "
              u"assemblies in the "
              u"Hardware module."))
        self.btnAssignComponent.set_tooltip_markup(
            _(u"Assigns results to "
              u"components in the "
              u"Hardware module."))

        self.chkGrouped.set_tooltip_text(
            _(u"Indicates whether the failure "
              u"and suspension data is grouped."))
        self.tvwSurvivalRecords.set_tooltip_markup(
            _(u"Displays the list of "
              u"records associated "
              u"with the selected "
              u"survival analysis."))

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.btnAddRecord.connect('clicked', self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnDeleteRecord.connect('clicked', self._on_button_clicked,
                                         1))
        self._lst_handler_id.append(
            self.btnConsolidate.connect('clicked', self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.btnCalculate.connect('clicked', self._on_button_clicked, 3))
        self._lst_handler_id.append(
            self.btnSave.connect('clicked', self._on_button_clicked, 4))
        self._lst_handler_id.append(
            self.btnAssignAssembly.connect('clicked', self._on_button_clicked,
                                           5))
        self._lst_handler_id.append(
            self.btnAssignComponent.connect('clicked', self._on_button_clicked,
                                            6))
        self._lst_handler_id.append(
            self.chkGrouped.connect('toggled', self._on_toggled, 7))

        # self.tvwSurvivalRecords.connect('button_press_event',
        #                            self._on_button_clicked, 0)

        # Put it all together.
        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_notebook(self):
        """
        Method to create the Survival class List View gtk.Notebook().

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

        self._create_survival_records_page(_notebook)
        # self._create_nevada_chart_page(_notebook)
        # self._create_results_by_child_assembly_page(_notebook)
        # self._create_results_by_component_page(_notebook)

        return _notebook

    def _create_survival_records_page(self, notebook):
        """
        Method to create the Survival analysis list of records page in the
        List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Survival Risk matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnAddRecord, False, False)
        _bbox.pack_start(self.btnDeleteRecord, False, False)
        _bbox.pack_start(self.btnConsolidate, False, False)
        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_end(self.btnSave, False, False)

        _hbox.pack_start(_bbox, False, False)

        _vbox = gtk.VBox()

        _fixed = gtk.Fixed()
        _vbox.pack_start(_fixed, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwSurvivalRecords)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame, True, True)

        _hbox.pack_end(_vbox, True, True)

        _fixed.put(self.chkGrouped, 5, 5)

        # Create the Survival analysis records gtk.TreeView().
        # =============================================================== #
        # Survival Analysis Records
        #    0. Record Number
        #    1. Incident Date (editable)
        #    2. Affected Hardware Assembly (editable)
        #    3. Start of Interval (editable)
        #    4. End of Interval (editable)
        #    5. Interarrival Time
        #    6. Number of Failures During Interval (editable)
        #    7. Status of Incident (editable)
        # =============================================================== #
        _labels = [
            _(u"Record\nID"),
            _(u"Event\nDate"),
            _(u"Affected\nAssembly"),
            _(u"Left of\nInterval"),
            _(u"Right of\nInterval"),
            _(u"Interarrival\nTime"),
            _(u"Quantity"),
            _(u"Status")
        ]
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_INT, gobject.TYPE_STRING)
        self.tvwSurvivalRecords.set_model(_model)

        for _index, _label in enumerate(_labels):
            if _index == 0:
                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('visible', 1)
            elif _index == 2:
                _cell = gtk.CellRendererCombo()
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cell.set_property('editable', 1)
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
            elif _index == 7:
                _cell = gtk.CellRendererCombo()
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cellmodel.append([""])
                _cellmodel.append([_(u"Event")])
                _cellmodel.append([_(u"Right Censored")])
                _cellmodel.append([_(u"Left Censored")])
                _cellmodel.append([_(u"Interval Censored")])
                _cell.set_property('editable', 1)
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
            else:
                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'white')
                _cell.set_property('editable', 1)
                _cell.set_property('visible', 1)

            _cell.connect('edited', self._on_cellrenderer_edited, _index,
                          _model)
            _column = gtk.TreeViewColumn()
            _label = Widgets.make_column_heading(_label)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)
            _column.set_sort_column_id(_index + 1)

            # _column.set_cell_data_func(_cell, Widgets.format_cell,
            #                            (_index, _datatype))
            _column.connect('notify::width', Widgets.resize_wrap, _cell)

            self.tvwSurvivalRecords.append_column(_column)

        # Add the Survival records page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Dataset\nRecords</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the survival analysis records."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_results_by_child_assembly_page(self, notebook):
        """
        Method to create the Survival analysis results by child assembly page
        in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Survival Risk matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnAssignAssembly, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResultsByChildAssembly)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Create the results by child assembly gtk.TreeView().
        # =============================================================== #
        # Results by Child Assembly
        #    0. Child Hardware Assembly
        #    1. Number of Failures
        #    2.
        #    3. MTBF Lower Bound
        #    4. MTBF Point Estimate
        #    5. MTBF Upper Bound
        #    6. Failure Intensity Lower Bound
        #    7. Failure Intensity Point Estimate
        #    8. Failure Intensity Upper Bound
        #    9. Cell background color
        # =============================================================== #
        # Table of results allocated to each assembly.
        _labels = [
            _(u"Hardware\nItem"),
            _(u"Number of\nFailures"),
            _(u""),
            _(u"MTBF\nLower Bound"),
            _(u"MTBF"),
            _(u"MTBF\nUpper Bound"),
            _(u"Failure Intensity\nLower Bound"),
            _(u"Failure\nIntensity"),
            _(u"Failure Intensity\nUpper Bound")
        ]
        _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_STRING)
        self.tvwResultsByChildAssembly.set_model(_model)

        for _index, _label in enumerate(_labels):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = Widgets.make_column_heading(_label)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index, background=9)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            self.tvwResultsByChildAssembly.append_column(_column)

        # Add the results breakdown by child assembly page to the
        # gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(
            _(u"<span weight='bold'>"
              u"Results by\nChild Assembly</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays analysis results for the "
              u"selected data set broken down by child "
              u"assembly."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_results_by_component_page(self, notebook):
        """
        Method to create the Survival analysis results by component page in the
        List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Survival Risk matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnAssignComponent, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResultsByPart)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Create the results by child assembly gtk.TreeView().
        # =============================================================== #
        # Results by Child Assembly
        #    0. Part Number
        #    1. Number of Failures
        #    2.
        #    3. MTBF Lower Bound
        #    4. MTBF Point Estimate
        #    5. MTBF Upper Bound
        #    6. Failure Intensity Lower Bound
        #    7. Failure Intensity Point Estimate
        #    8. Failure Intensity Upper Bound
        #    9. Cell background color
        # =============================================================== #
        # Table of results allocated to each part.
        _labels = [
            _(u"Part\nNumber"),
            _(u"Number of\nFailures"),
            _(u""),
            _(u"MTBF\nLower Bound"),
            _(u"MTBF"),
            _(u"MTBF\nUpper Bound"),
            _(u"Failure Intensity\nLower Bound"),
            _(u"Failure\nIntensity"),
            _(u"Failure Intensity\nUpper Bound")
        ]
        _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_STRING)
        self.tvwResultsByPart.set_model(_model)

        self.tvwResultsByPart.columns_autosize()
        self.tvwResultsByPart.set_headers_clickable(True)
        self.tvwResultsByPart.set_reorderable(True)

        for _index, _label in enumerate(_labels):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = Widgets.make_column_heading(_label)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index, background=9)
            _column.set_clickable(True)
            _column.set_sort_column_id(_index)
            self.tvwResultsByPart.append_column(_column)

        # Add the results breakdown by child assembly page to the
        # gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(
            _(u"<span weight='bold'>"
              u"Results by\nPart Number</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays analysis results for the "
              u"selected data set broken down by "
              u"part number."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Survival List Book.

        :param model: the :py:class:`rtk.survival.growth.Growth.Model` whose
                      attributes are loaded.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._survival_model = model

        # Load the Survival records gtk.TreeView() column with system hardware
        # names.
        _column = self.tvwSurvivalRecords.get_column(2)
        _cell = _column.get_cell_renderers()[0]
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for j in range(len(Configuration.RTK_HARDWARE_LIST)):
            _cellmodel.append([Configuration.RTK_HARDWARE_LIST[j][0]])

        self.load_survival_records()

        return False

    def load_survival_records(self):
        """
        Method to load the Reliability Growth Test assessment gtk.TreeView()
        with the actual test incidents.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _model = self.tvwSurvivalRecords.get_model()
        _model.clear()
        for _key in self._survival_model.dicRecords.keys():
            _record = self._survival_model.dicRecords[_key]
            _date = str(
                datetime.fromordinal(
                    _record.failure_date).strftime('%Y-%m-%d'))
            _status = self._lst_status[_record.status]
            try:
                _record.assembly_id = [
                    x[1] for x in Configuration.RTK_HARDWARE_LIST
                    if x[0] == _record.assembly_name
                ][0]
            except IndexError:
                _record.assembly_name = ''
                _record.assembly_id = 0

            _data = [
                _key, _date, _record.assembly_name, _record.left_interval,
                _record.right_interval, _record.interarrival_time,
                _record.n_failures, _status
            ]
            _model.append(_data)

        self.tvwSurvivalRecords.set_cursor('0', None, False)
        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            _col = self.tvwSurvivalRecords.get_column(0)
            self.tvwSurvivalRecords.row_activated(_path, _col)

        self.chkGrouped.set_active(self._survival_model.grouped)

        return False

    def _load_nevada_chart(self):  # pylint: disable=R0914
        """
        Method to load the Survival analysis records into the Nevada chart
        gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _nevada = {}

        _query = "SELECT DISTINCT(fld_ship_date), fld_number_shipped \
                  FROM tbl_nevada_chart \
                  WHERE fld_dataset_id=%d \
                  ORDER BY fld_ship_date" % self.dataset_id
        _ships = self._dao.execute_query(_query, commit=False)

        _query = "SELECT fld_ship_date, fld_return_date, fld_number_returned \
                  FROM tbl_nevada_chart \
                  WHERE fld_dataset_id=%d \
                  ORDER BY fld_ship_date, fld_return_date" % self.dataset_id
        _returns = self._dao.execute_query(_query, commit=False)

        try:
            _n_periods = len(_ships)
        except TypeError:
            _n_periods = 0

        try:
            _n_returns = len(_returns)
        except TypeError:
            _n_returns = 0

        # Create a dictionary with the following:
        #
        #     Key = shipment date (month-year).
        #   Value = list with each position containing:
        #       0 = the number of units shipped.
        #       1 = dictionary of returned units where the key is the return
        #           date and the value is the number of units returned.
        #
        #   {u'Jan-08': [32, {u'Mar-08': 0, u'Feb-08': 0}]}
        #
        # Create a list of GObject types to use for creating the gtkListStore()
        # used to display the Nevada chart.
        _gobject_types = [
            gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_INT,
            gobject.TYPE_STRING
        ]
        for i in range(_n_periods):
            _date_ship = datetime.strftime(
                date.fromordinal(_ships[i][0]), '%b-%y')
            _nevada[_date_ship] = [_ships[i][1], {}]

        _n_cols = 2
        _headings = [_(u"Ship Date"), _(u"Number\nShipped")]
        for i in range(_n_returns):
            _date_ship = datetime.strftime(
                date.fromordinal(_returns[i][0]), '%b-%y')
            _date_return = datetime.strftime(
                date.fromordinal(_returns[i][1]), '%b-%y')
            _nevada[_date_ship][1][_date_return] = _returns[i][2]
            _n_cols = max(_n_cols, len(_nevada[_date_ship][1]) + 2)
            if _date_return not in _headings:
                _headings.append(_date_return)
                _gobject_types.append(gobject.TYPE_INT)
                _gobject_types.append(gobject.TYPE_STRING)

        # Create the gtk.ListStore() and columns for the Nevada chart
        # gtk.TreeView().
        j = 0
        _model = gtk.ListStore(*_gobject_types)
        for i in range(_n_cols):
            _cell = gtk.CellRendererText()  # Value to be displayed.
            _cell.set_property('editable', 0)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.1)

            _column = gtk.TreeViewColumn("")
            _label = gtk.Label(_column.get_title())
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _headings[i] +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column.setWidgetset(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=j, background=j + 1)
            _column.set_resizable(True)
            _column.set_alignment(0.5)

            _cell = gtk.CellRendererText()  # Cell background color.
            _cell.set_property('visible', False)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=j + 1)

            self.tvwNevadaChart.append_column(_column)

            j += 2

        self.tvwNevadaChart.set_model(_model)

        # Load the Nevada chart gtk.ListStore() with the data.
        _date_ship = _nevada.keys()
        _date_return = _headings[2:]
        for _index, _sdate in enumerate(_date_ship):
            _returns = _nevada[_date_ship[_index]][1].keys()
            _data = [
                _date_ship[_index], 'light gray',
                _nevada[_date_ship[_index]][0], 'light gray'
            ]
            for _jndex, _rdate in enumerate(_date_return):
                if _date_return[_jndex] not in _returns:
                    _data.append(0)
                    _data.append('light gray')
                else:
                    _data.append(
                        _nevada[_date_ship[_index]][1][_date_return[_jndex]])
                    _data.append('#FFFFFF')
            _model.append(_data)

        return False

    def _on_button_clicked(self, button, index):
        """
        Method to respond to gtk.Button() 'clicked' signals and call the
        correct function or method, passing any parameters as needed.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if index == 0:
            _survival_id = self._survival_model.survival_id
            self._mdcRTK.dtcSurvival.add_record(_survival_id)
            self.load_survival_records()
        elif index == 1:
            (_model,
             _row) = self.tvwSurvivalRecords.get_selection().get_selected()
            _record_id = _model.get_value(_row, 0)
            _survival_id = self._survival_model.survival_id
            self._mdcRTK.dtcSurvival.delete_record(_survival_id, _record_id)
            _model.remove(_row)
        elif index == 2:
            _survival_id = self._survival_model.survival_id
            self._mdcRTK.dtcSurvival.consolidate_dataset(_survival_id)
            self._mdcRTK.dtcSurvival.request_records(_survival_id)
            self.load_survival_records()
        elif index == 3:
            _survival_id = self._survival_model.survival_id
            self._mdcRTK.dtcSurvival.request_calculate_tbf(_survival_id)
            self.load_survival_records()
        elif index == 4:
            _survival_id = self._survival_model.survival_id
            for _record_id in self._survival_model.dicRecords.keys():
                _record = self._survival_model.dicRecords[_record_id]
                (_results, _error_code) = self._mdcRTK.dtcSurvival.save_record(
                    _survival_id, _record_id, _record)
        elif index == 5:
            print "Assign results to assemblies"
        elif index == 6:
            print "Assign results to components"

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_cellrenderer_edited(self, __cell, path, new_text, position, model):
        """
        Method to respond to gtk.CellRenderer() 'edited' signals in the
        Reliability Growth assessment gtk.TreeView().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
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
        # WARNING: Refactor _on_cellrenderer_edited; current McCabe Complexity metric=13.
        _record_id = model[path][0]

        _record = self._survival_model.dicRecords[_record_id]

        if position == 1:  # Failure date.
            _date = Utilities.date_to_ordinal(new_text)
            _record.failure_date = _date
            model[path][position] = new_text
        elif position == 2:  # Affected assembly.
            _record.assembly_id = [
                x[1] for x in Configuration.RTK_HARDWARE_LIST
                if x[0] == new_text
            ][0]
            _record.assembly_name = new_text
            model[path][position] = _record.assembly_name
        elif position == 3:
            _record.left_interval = float(new_text)
            model[path][position] = _record.left_interval
        elif position == 4:
            _record.right_interval = float(new_text)
            model[path][position] = _record.right_interval
        elif position == 5:
            _record.interarrival_time = float(new_text)
            model[path][position] = _record.interarrival_time
        elif position == 6:
            _record.n_failures = int(new_text)
            model[path][position] = _record.n_failures
        elif position == 7:  # Event status.
            for j in (i for i, x in enumerate(self._lst_status)
                      if x == new_text):
                _record.status = int(j)
            model[path][position] = new_text

        return False

    def _on_toggled(self, button, index):
        """
        Method to respond to gtk.CheckButton() toggled signals.

        :param gtk.CheckButton button: the gtk.CheckButton() that called this
                                       method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.CheckButton() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if index == 7:
            self._survival_model.grouped = button.get_active()

        button.handler_unblock(self._lst_handler_id[index])

        return False
