#!/usr/bin/env python
"""
###############################
Survival Package Work Book View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.WorkBook.py is part of The RTK Project
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
try:
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg
import gui.gtk.Exponential
import gui.gtk.Gaussian
import gui.gtk.KaplanMeier
import gui.gtk.LogNormal
import gui.gtk.MCF
import gui.gtk.NHPP
import gui.gtk.Weibull

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.VBox):                   # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected
    Survival item.  The attributes of a Work Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Survival attribute.

    :ivar _workview: the RTK top level :py:class:`rtk.gui.gtk.WorkBook` window
                     to embed the Survival Work Book into.
    :ivar _model: the Survival :py:class:`rtk.survival.Survival.Model`
                  whose attributes are being displayed.
    :ivar dtcSurvival: the :py:class:`rtk.survival.Survival.Survival`
                         to use with this Work Book.

    :ivar gtk.Button btnCalculate: gtk.Button() to calculate the interarrival
                                   times of the dataset.
    :ivar gtk.Button btnSaveRecord: gtk.Button() to save the records in the
                                    dataset.
    :ivar gtk.Button btnStartDate: gtk.Button() to launch the calendar widget
                                   for selecting the start date.
    :ivar gtk.Button btnEndDate: gtk.Button() to launch the calendar widget
                                 for selecting the end date.
    :ivar gtk.Button btnAssign: gtk.Button() to assign analysis results to
                                the selected assembly.
    :ivar gtk.Button btnCancel: gtk.Button() to
    :ivar gtk.CheckButton chkGroup: gtk.CheckButton() to indicate the analysis
                                    results should be decomposed to child
                                    assemblies.
    :ivar gtk.CheckButton chkParts: gtk.CheckButton() to indicate the analysis
                                    results should be decomposed to child
                                    components.
    :ivar gtk.ComboBox cmbAssembly: gtk.ComboBox() to select the affected
                                    Assembly.
    :ivar gtk.ComboBox cmbConfType: gtk.ComboBox() to select the type of
                                    confidence bounds (lower one-sided,
                                    two-sided, upper one-sided)
    :ivar gtk.ComboBox cmbConfMethod: gtk.ComboBox() to select the method for
                                      calculating the confidence bounds.
    :ivar gtk.ComboBox cmbDistribution: gtk.ComboBox() to select the
                                        statistical distribution to fit the
                                        dataset to.
    :ivar gtk.ComboBox cmbFitMethod: gtk.ComboBox() to select the method for
                                     fitting the dataset to a statistical
                                     distribution.
    :ivar gtk.ComboBox cmbSource: gtk.ComboBox() to select the source of the
                                  dataset.
    :ivar gtk.TreeView tvwDataset: gtk.TreeView() to display the dataset
                                   records.
    :ivar gtk.TreeView tvwNevadaChart: gtk.TreeView() to display the dataset
                                       records as a Nevada Chart.
    :ivar gtk.TreeView tvwResultsByChildAssembly: gtk.TreeView() to display the
                                                  decomposed analysis results
                                                  to the next level child
                                                  assemblies.
    :ivar gtk.TreeView tvwResultsByPart: gtk.TreeView() to display the
                                         decomposed analysis results to the
                                         components.
    :ivar gtk.Entry txtConfidence: gtk.Entry() to display the confidence level.
    :ivar gtk.Entry txtDescription: gtk.Entry() to display the description of
                                    the Survival analysis.
    :ivar gtk.Entry txtStartTime: gtk.Entry() to display the first time at
                                  which to calculate various characteristics of
                                  a statistical model (e.g., hazard rate, mtbf,
                                  reliability function).
    :ivar gtk.Entry txtEndTime: gtk.Entry() to display the last time at which
                                to calculate various characteristics of a
                                statistical model (e.g., hazard rate, mtbf,
                                reliability function).
    :ivar gtk.Entry txtRelPoints: gtk.Entry() to display the number of points
                                  to calculate various characteristics of a
                                  statistical model (e.g., hazard rate, mtbf,
                                  reliability function).
    :ivar gtk.Entry txtStartDate: gtk.Entry() to display the first date to
                                  include in the dataset used in the analysis.
    :ivar gtk.Entry txtEndDate: gtk.Entry() to display the last date to
                                include in the dataset used in the analysis.
    :ivar gtk.Entry txtNumSuspensions: gtk.Entry() to display the number of
                                       suspensions in the dataset.
    :ivar gtk.Entry txtNumFailures: gtk.Entry() to display the number of
                                    failures in the dataset.

    +----------+--------------------------------------------+
    | Position | Widget - Signal                            |
    +==========+============================================+
    |     0    | btnAddRecord - 'clicked'                   |
    +----------+--------------------------------------------+
    |     1    | btnRemoveRecord - 'clicked'                |
    +----------+--------------------------------------------+
    |     2    | btnCalculate - 'clicked'                   |
    +----------+--------------------------------------------+
    |     3    | btnSaveRecord - 'clicked'                  |
    +----------+--------------------------------------------+
    |     4    | cmbAssembly - 'changed'                    |
    +----------+--------------------------------------------+
    |     5    | cmbSource - 'changed'                      |
    +----------+--------------------------------------------+
    |     6    | cmbDistribution - 'changed'                |
    +----------+--------------------------------------------+
    |     7    | cmbConfType - 'changed'                    |
    +----------+--------------------------------------------+
    |     8    | cmbConfMethod - 'changed'                  |
    +----------+--------------------------------------------+
    |     9    | cmbFitMethod - 'changed'                   |
    +----------+--------------------------------------------+
    |    10    | txtDescription - 'focus-out-event'         |
    +----------+--------------------------------------------+
    |    11    | txtConfidence - 'focus-out-event'          |
    +----------+--------------------------------------------+
    |    12    | txtStartTime - 'focus-out-event'           |
    +----------+--------------------------------------------+
    |    13    | txtEndTime - 'focus-out-event'             |
    +----------+--------------------------------------------+
    |    14    | txtRelPoints - 'focus-out-event'           |
    +----------+--------------------------------------------+
    |    15    | txtStartDate - 'focus-out-event'           |
    +----------+--------------------------------------------+
    |    15    | txtStartDate - 'changed'                   |
    +----------+--------------------------------------------+
    |    16    | txtEndDate - 'focus-out-event'             |
    +----------+--------------------------------------------+
    |    16    | txtEndDate - 'changed'                     |
    +----------+--------------------------------------------+
    |    17    | btnStartDate - 'button-release-event'      |
    +----------+--------------------------------------------+
    |    18    | btnEndDate - 'button-release-event'        |
    +----------+--------------------------------------------+
    |    19    | chkGroup - 'toggled'                       |
    +----------+--------------------------------------------+
    |    20    | chkParts - 'toggled'                       |
    +----------+--------------------------------------------+
    """

    def __init__(self, workview, modulebook):
        """
        Initializes the Work Book view for the Survival package.

        :param workview: the :py:class:`rtk.gui.gtk.mwi.WorkView` container to
                         insert this Work Book into.
        :param modulebook: the :py:class:`rtk.survival.ModuleBook` to
                           associate with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []
        self._lst_results = [gui.gtk.MCF.Results(),
                             gui.gtk.KaplanMeier.Results(),
                             gui.gtk.NHPP.Results(), gui.gtk.NHPP.Results(),
                             gui.gtk.Exponential.Results(),
                             gui.gtk.LogNormal.Results(),
                             gui.gtk.Gaussian.Results(),
                             gui.gtk.Weibull.Results()]
        self._lst_plots = [gui.gtk.MCF.Plots(), gui.gtk.KaplanMeier.Plots(),
                           gui.gtk.NHPP.Plots(), gui.gtk.NHPP.Plots(),
                           gui.gtk.Exponential.Plots(),
                           gui.gtk.LogNormal.Plots(), gui.gtk.Gaussian.Plots(),
                           gui.gtk.Weibull.Plots()]
        self._lst_status = [_(u"Event"), _(u"Right Censored"),
                            _(u"Left Censored"), _(u"Interval Censored")]

        # Initialize private scalar attributes.
        self._workview = workview
        self._modulebook = modulebook
        self._model = None
        self._record_id = None
        self._obj_results = None
        self._obj_plots = None

        # Initialize public scalar attributes.
        # Create the Analyses Input page widgets.
        self.btnAddRecord = _widg.make_button(width=35, image='add')
        self.btnRemoveRecord = _widg.make_button(width=35, image='remove')
        self.btnCalculate = _widg.make_button(width=35, image='calculate')
        self.btnSaveRecord = _widg.make_button(width=35, image='save')

        self.chkGrouped = _widg.make_check_button(label=_(u"Failure data is "
                                                          u"grouped"))
        self.chkGroup = _widg.make_check_button(label=_(u"Decompose results "
                                                        u"to children "
                                                        u"assemblies"))
        self.chkParts = _widg.make_check_button(label=_(u"Decompose results "
                                                        u"to parts"))

        self.cmbAssembly = _widg.make_combo(simple=False)
        self.cmbConfType = _widg.make_combo()
        self.cmbConfMethod = _widg.make_combo()
        self.cmbDistribution = _widg.make_combo()
        self.cmbFitMethod = _widg.make_combo()
        self.cmbSource = _widg.make_combo()

        self.tvwDataset = gtk.TreeView()
        self.tvwDataset.set_search_column(0)
        self.tvwDataset.set_reorderable(True)
        self.tvwDataset.connect('row_activated', self._on_record_select)
        self.tvwDataset.connect('cursor_changed', self._on_record_select,
                                None, None)

        self.tvwNevadaChart = gtk.TreeView()

        self.txtConfidence = _widg.make_entry(width=50)
        self.txtDescription = _widg.make_entry(width=200)
        self.txtStartTime = _widg.make_entry(width=100)
        self.txtEndTime = _widg.make_entry(width=100)
        self.txtRelPoints = _widg.make_entry(width=100)

        self.txtStartDate = _widg.make_entry(width=100)
        self.txtEndDate = _widg.make_entry(width=100)

        self.btnStartDate = _widg.make_button(height=25, width=25,
                                              label="...", image=None)
        self.btnEndDate = _widg.make_button(height=25, width=25,
                                            label="...", image=None)

        # Create the analysis results breakdown page widgets.
        self.tvwResultsByChildAssembly = gtk.TreeView()
        self.tvwResultsByPart = gtk.TreeView()

        self.btnAssign = _widg.make_button(width=100, label="Assign",
                                           image=None)
        self.btnCancel = _widg.make_button(width=100, label="Cancel",
                                           image=None)

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        self._notebook = self._create_notebook()
        self.pack_end(self._notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Survival class Work Book.
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 4)
        _button.set_tooltip_text(_(u"Add a new Survival analysis to the open "
                                   u"RTK Program database for the selected "
                                   u"revision."))
        _toolbar.insert(_button, _position)
        _position += 1

        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 5)
        _button.set_tooltip_text(_(u"Remove the selected Survival analysis "
                                   u"from the open RTK Program database."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Consolidate results.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert-assembly.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 6)
        _button.set_tooltip_text(_(u"Consolidates the records in the selected "
                                   u"data set."))
        # _toolbar.insert(_button, _position)
        # _position += 1

        # Calculate button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 7)
        _button.set_tooltip_text(_(u"Analyzes the selected data set."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Save button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 8)
        _button.set_tooltip_text(_(u"Saves the selected data set and it's "
                                   u"records."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Assign results to affected assembly.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/import.png')
        _button.set_icon_widget(_image)
        #_button.connect('clicked', AssignMTBFResults, self._app)
        _button.set_tooltip_text(_(u"Assigns MTBF and hazard rate results to "
                                   u"the selected assembly."))
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Survival class gtk.Notebook().
        """
# TODO: Add the results breakdown page.
        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_analyses_input_page(_notebook)
        #self._create_results_breakdown_page(_notebook)

        for __, _dist in enumerate(self._lst_results):
            _dist.create_results_page()
        for __, _dist in enumerate(self._lst_plots):
            _dist.create_plot_page()

        return _notebook

    def _create_analyses_input_page(self, notebook):    # pylint: disable=R0914
        """
        Method to create the Dataset class gtk.Notebook() page for displaying
        assessment inputs for the selected data set.

        :param gtk.Notebook notebook: the Dataset class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HPaned()
        _hbox2 = gtk.HBox()
        _vbox = gtk.VBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _bbox.pack_start(self.btnAddRecord, False, False)
        _bbox.pack_start(self.btnRemoveRecord, False, False)
        _bbox.pack_start(self.btnCalculate, False, False)
        _bbox.pack_start(self.btnSaveRecord, False, False)

        self.btnAddRecord.set_tooltip_text(_(u"Adds a record to the selected "
                                             u"dataset."))
        self.btnRemoveRecord.set_tooltip_text(_(u"Removes the selected record "
                                                u"from the dataset."))
        self.btnCalculate.set_tooltip_text(_(u"Calculates interarrival times "
                                             u"for the selected dataset."))
        self.btnSaveRecord.set_tooltip_text(_(u"Saves the selected dataset "
                                              u"to the open RTK Prject "
                                              u"database."))

        self._lst_handler_id.append(
            self.btnAddRecord.connect('clicked', self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnRemoveRecord.connect('clicked',
                                         self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnCalculate.connect('clicked', self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.btnSaveRecord.connect('clicked', self._on_button_clicked, 3))

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwDataset)

        _hbox2.pack_start(_bbox, False, False)
        _hbox2.pack_end(_scrollwindow)

        _fixed = gtk.Fixed()
        _fixed.put(self.chkGrouped, 10, 5)
        # _label = _widg.make_label(_(u"Select dataset:"))
        # _fixed.put(_label, 10, 5)
        # _fixed.put(self.cmbDatasets, 135, 5)
        # _fixed.put(self.btnAddDataset, 205, 5)
        # _fixed.put(self.btnRemoveDataset, 240, 5)

        _frame = gtk.Frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        _vbox.pack_start(_frame, False, False)

        _frame = _widg.make_frame(label=_(u"Dataset Records"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_hbox2)

        _vbox.pack_end(_frame, True, True)
        _hbox.pack1(_vbox, True, False)

        _fixed = gtk.Fixed()

        _frame = _widg.make_frame(label=_(u"Analysis Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        _frame.add(_fixed)

        _hbox.pack2(_frame, True, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis input information. #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets.
        _results = [["ALT"], [_(u"Reliability Growth")],
                    [_(u"Reliability Demonstration")], [_(u"Field")]]
        _widg.load_combo(self.cmbSource, _results)
        _results = [[u"MCF"], [u"Kaplan-Meier"], [_(u"NHPP - Power Law")],
                    [u"NHPP - Loglinear"], [_(u"Exponential")],
                    [_(u"Lognormal")], [_(u"Normal")], [u"Weibull"],
                    ["WeiBayes"]]
        _widg.load_combo(self.cmbDistribution, _results)
        _results = [[_(u"Lower One-Sided")], [_(u"Upper One-Sided")],
                    [_(u"Two-Sided")]]
        _widg.load_combo(self.cmbConfType, _results)
        _results = [[_(u"Crow (NHPP Only)")], [_(u"Duane (NHPP Only)")],
                    [_(u"Fisher Matrix")], [_(u"Likelihood")],
                    [_(u"Bootstrap")]]
        _widg.load_combo(self.cmbConfMethod, _results)
        _results = [["MLE"], [_(u"Regression")]]
        _widg.load_combo(self.cmbFitMethod, _results)

        # Create the Dataset treeview on the left side.
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_INT, gobject.TYPE_STRING)
        self.tvwDataset.set_model(_model)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('visible', 1)
        _cell.set_property('background', 'gray')
        _column = gtk.TreeViewColumn()
        _label = _widg.make_column_heading(_(u"Record\nID"))
        _column.set_widget(_label)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        _column.set_visible(1)
        self.tvwDataset.append_column(_column)

        _headings = [_(u"Event\nDate"), _(u"Affected\nHardware"),
                     _(u"Left of\nInterval"), _(u"Right of\nInterval"),
                     _(u"Interarrival\nTime"), _(u"Quantity")]
        for _index, _heading in enumerate(_headings):
            if _index == 1:
                _cell = gtk.CellRendererCombo()
                _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
                _cell.set_property('has-entry', False)
                _cell.set_property('model', _cellmodel)
                _cell.set_property('text-column', 0)
            else:
                _cell = gtk.CellRendererText()
            _cell.set_property('editable', 1)
            _cell.set_property('background', 'white')
            _cell.connect('edited', self._on_cellrenderer_edited, _index + 1,
                          _model)
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index + 1)
            _column.set_sort_column_id(_index + 1)
            self.tvwDataset.append_column(_column)

        _cell = gtk.CellRendererCombo()
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
        _cellmodel.append([""])
        _cellmodel.append([_(u"Event")])
        _cellmodel.append([_(u"Right Censored")])
        _cellmodel.append([_(u"Left Censored")])
        _cellmodel.append([_(u"Interval Censored")])
        _cell.set_property('editable', True)
        _cell.set_property('has-entry', False)
        _cell.set_property('model', _cellmodel)
        _cell.set_property('text-column', 0)
        _cell.connect('changed', self._on_cellrenderer_edited, 7, _model)
        _column = gtk.TreeViewColumn()
        _label = _widg.make_column_heading(_(u"Status"))
        _column.set_widget(_label)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=7)
        _column.set_visible(1)
        self.tvwDataset.append_column(_column)

        # Create the labels for the left half of the right side.
        _labels = [_(u"Assembly:"), _(u"Description:"), _(u"Data Source:"),
                   _(u"Distribution:"), _("Fit Method:"), _(u"Confidence:"),
                   _(u"Confidence Type:"), _("Confidence Method:")]
        (_x_pos1, _y_pos1) = _widg.make_labels(_labels, _fixed, 5, 5)
        _x_pos1 += 55

        # Create the labels for the right half of the right side.
        _labels = [_(u"Start Time:"), _(u"End Time:"), _(u"Step Interval:"),
                   _(u"Start Date:"), _(u"End Date:")]
        (_x_pos2,
         _y_pos2) = _widg.make_labels(_labels, _fixed, _x_pos1 + 215, 5)
        _x_pos2 += _x_pos1
        _x_pos2 += 275

        self.cmbAssembly.set_tooltip_text(_(u"Selects and displays the "
                                            u"assembly associated with the "
                                            u"data set."))
        self.txtDescription.set_tooltip_text(_(u"Description of the selected "
                                               u"data set."))
        self.cmbSource.set_tooltip_text(_(u"Selects and displays the source "
                                          u"of the selected data set."))
        self.cmbDistribution.set_tooltip_text(_(u"Selects and displays the "
                                                u"statistical distribution "
                                                u"used to fit the data."))
        self.cmbFitMethod.set_tooltip_text(_(u"Selects and displays the "
                                             u"method used to fit the data to "
                                             u"the selected distribution."))
        self.txtConfidence.set_tooltip_text(_(u"Desired statistical "
                                              u"confidence"))
        self.cmbConfType.set_tooltip_text(_(u"Selects and displays the type "
                                            u"of confidence bounds."))
        self.cmbConfMethod.set_tooltip_text(_(u"Selects and displays the "
                                              u"method for developing "
                                              u"confidence bounds."))
        self.txtStartTime.set_tooltip_text(_(u"Earliest failure time to use "
                                             u"for calculating reliability "
                                             u"metrics."))
        self.txtEndTime.set_tooltip_text(_(u"Latest failure time to use for "
                                           u"calculating reliability "
                                           u"metrics."))
        self.txtRelPoints.set_tooltip_text(_(u"Number of points at which to "
                                             u"calculate reliability "
                                             u"metrics."))
        self.txtStartDate.set_tooltip_text(_(u"Earliest failure date to use "
                                             u"for calculating reliability "
                                             u"metrics."))
        self.txtEndDate.set_tooltip_text(_(u"Latest failure date to use for "
                                           u"calculating reliability "
                                           u"metrics."))
        self.btnStartDate.set_tooltip_text(_(u"Launches the calendar to "
                                             u"select the start date."))
        self.btnEndDate.set_tooltip_text(_(u"Launches the calendar to select "
                                           u"the end date."))
        self.chkGrouped.set_tooltip_text(_(u"Indicates whether the failure "
                                           u"suspension data is grouped."))
        self.chkGroup.set_tooltip_text(_(u"When checked, the MTBF and failure "
                                         u"intensity results will be "
                                         u"distributed to all next-level "
                                         u"child assemblies according to the "
                                         u"percentage of records each "
                                         u"assembly contributes.  This "
                                         u"assumes failure times are "
                                         u"exponentially distributed."))
        self.chkParts.set_tooltip_text(_(u"When checked, the MTBF and failure "
                                         u"intensity results will be "
                                         u"distributed to all components "
                                         u"according to the percentage of "
                                         u"records each component "
                                         u"contributes.  This assumes failure "
                                         u"times are exponentially "
                                         u"distributed."))

        # Place widgets on the left side.
        _fixed.put(self.cmbAssembly, _x_pos1, _y_pos1[0])
        _fixed.put(self.txtDescription, _x_pos1, _y_pos1[1])
        _fixed.put(self.cmbSource, _x_pos1, _y_pos1[2])
        _fixed.put(self.cmbDistribution, _x_pos1, _y_pos1[3])
        _fixed.put(self.cmbFitMethod, _x_pos1, _y_pos1[4])
        _fixed.put(self.txtConfidence, _x_pos1, _y_pos1[5])
        _fixed.put(self.cmbConfType, _x_pos1, _y_pos1[6])
        _fixed.put(self.cmbConfMethod, _x_pos1, _y_pos1[7])

        # Place widgets on the right side.
        _fixed.put(self.txtStartTime, _x_pos2, _y_pos2[0])
        _fixed.put(self.txtEndTime, _x_pos2, _y_pos2[1])
        _fixed.put(self.txtRelPoints, _x_pos2, _y_pos2[2])
        _fixed.put(self.txtStartDate, _x_pos2, _y_pos2[3])
        _fixed.put(self.btnStartDate, _x_pos2 + 105, _y_pos2[3])
        _fixed.put(self.txtEndDate, _x_pos2, _y_pos2[4])
        _fixed.put(self.btnEndDate, _x_pos2 + 105, _y_pos2[4])
        #_fixed.put(self.chkGroup, _x_pos2, _y_pos2[4] + 30)
        #_fixed.put(self.chkParts, _x_pos2, _y_pos2[4] + 60)

        _fixed.show_all()

        self._lst_handler_id.append(
            self.cmbAssembly.connect('changed', self._on_combo_changed, 4))
        self._lst_handler_id.append(
            self.cmbSource.connect('changed', self._on_combo_changed, 5))
        self._lst_handler_id.append(
            self.cmbDistribution.connect('changed', self._on_combo_changed, 6))
        self._lst_handler_id.append(
            self.cmbConfType.connect('changed', self._on_combo_changed, 7))
        self._lst_handler_id.append(
            self.cmbConfMethod.connect('changed', self._on_combo_changed, 8))
        self._lst_handler_id.append(
            self.cmbFitMethod.connect('changed', self._on_combo_changed, 9))
        self._lst_handler_id.append(
            self.txtDescription.connect('focus-out-event',
                                        self._on_focus_out, 10))
        self._lst_handler_id.append(
            self.txtConfidence.connect('focus-out-event',
                                       self._on_focus_out, 11))
        self._lst_handler_id.append(
            self.txtStartTime.connect('focus-out-event',
                                      self._on_focus_out, 12))
        self._lst_handler_id.append(
            self.txtEndTime.connect('focus-out-event',
                                    self._on_focus_out, 13))
        self._lst_handler_id.append(
            self.txtRelPoints.connect('focus-out-event',
                                      self._on_focus_out, 14))
        self._lst_handler_id.append(
            self.txtStartDate.connect('focus-out-event',
                                      self._on_focus_out, 15))
        self.txtStartDate.connect('changed', self._on_focus_out, None, 15)
        self._lst_handler_id.append(
            self.txtEndDate.connect('focus-out-event', self._on_focus_out, 16))
        self.txtEndDate.connect('changed', self._on_focus_out, None, 16)
        self.btnStartDate.connect('button-release-event',
                                  _util.date_select, self.txtStartDate)
        self.btnEndDate.connect('button-release-event', _util.date_select,
                                self.txtEndDate)
        self._lst_handler_id.append(
            self.chkGrouped.connect('toggled', self._on_toggled, 17))

        self.chkGroup.hide()
        self.chkParts.hide()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Analysis\nInputs") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays analysis inputs for the selected "
                                  u"dataset."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_results_breakdown_page(self, notebook):
        """
        Method to create the Dataset class gtk.Notebook() page for displaying
        results decomposed to child assemblies and/or components for the
        selected data set.

        :param gtk.Notebook notebook: the Dataset class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HPaned()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResultsByChildAssembly)

        _frame = _widg.make_frame(_(u"Summary of Results By Child Assembly"))
        _frame.add(_scrollwindow)

        _hpaned.pack1(_frame, True, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResultsByPart)

        _frame = _widg.make_frame(_(u"Summary of Results By Component"))
        _frame.add(_scrollwindow)

        _hpaned.pack2(_frame, True, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Table of results allocated to each assembly.
        _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_STRING)
        self.tvwResultsByChildAssembly.set_model(_model)

        _headings = [_(u"Hardware\nItem"), _(u"Number of\nFailures"), _(u""),
                     _(u"MTBF\nLower Bound"), _(u"MTBF"),
                     _(u"MTBF\nUpper Bound"),
                     _(u"Failure Intensity\nLower Bound"),
                     _(u"Failure\nIntensity"),
                     _(u"Failure Intensity\nUpper Bound")]
        for _index, _heading in enumerate(_headings):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index, background=9)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            self.tvwResultsByChildAssembly.append_column(_column)

        # Table of results allocated to each part.
        _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_STRING)
        self.tvwResultsByPart.set_model(_model)

        self.tvwResultsByPart.columns_autosize()
        self.tvwResultsByPart.set_headers_clickable(True)
        self.tvwResultsByPart.set_reorderable(True)

        _headings = [_(u"Part\nNumber"), _(u"Number of\nFailures"), _(u""),
                     _(u"MTBF\nLower Bound"), _(u"MTBF"),
                     _(u"MTBF\nUpper Bound"),
                     _(u"Failure Intensity\nLower Bound"),
                     _(u"Failure\nIntensity"),
                     _(u"Failure Intensity\nUpper Bound")]
        for _index, _heading in enumerate(_headings):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index, background=8)
            _column.set_clickable(True)
            _column.set_sort_column_id(_index)
            self.tvwResultsByPart.append_column(_column)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Results\nBreakdowns") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays analysis results for the "
                                  u"selected data set broken down by child "
                                  u"assembly and part number."))
        notebook.insert_page(_hpaned, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Survival class gtk.Notebook().

        :param model: the :py:class:`rtk.survival.Survival.Model` whose
                      attributes will be loaded into the display widgets.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Load dataset records into a Nevada chart.
# TODO: Load the results breakdown page.
        self._model = model

        self._load_analysis_inputs_page()
        self._load_dataset_records()

        # Remove existing results and plots pages.
        if self._obj_results is not None:
            self._notebook.remove_page(1)
        if self._obj_plots is not None:
            self._notebook.remove_page(1)

        # Get the correct results and plots object for the selected s-model.
        self._obj_results = self._lst_results[self._model.distribution_id - 1]
        self._obj_plots = self._lst_plots[self._model.distribution_id - 1]

        # Insert the s-model results and plots pages.
        self._notebook.insert_page(self._obj_results,
                                   tab_label=self._obj_results.lblPage,
                                   position=1)
        self._notebook.insert_page(self._obj_plots,
                                   tab_label=self._obj_plots.lblPage,
                                   position=2)

        # Load the s-model results and plots pages.
        self._obj_results.load_results_page(self._model)
        self._obj_plots.load_plots(self._model)

        self._notebook.show_all()
        self._notebook.set_current_page(0)

        return False

    def _load_analysis_inputs_page(self):
        """
        Method to load the gtk.Widgets() on the analysis inputs page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Load the gtk.ComboBox() with system hardware names.
        self.cmbAssembly.handler_block(self._lst_handler_id[4])
        _widg.load_combo(self.cmbAssembly, _conf.RTK_HARDWARE_LIST,
                         simple=False)
        self.cmbAssembly.handler_unblock(self._lst_handler_id[4])

        # Load the dataset gtk.TreeView() column with system hardware names.
        _column = self.tvwDataset.get_column(2)
        _cell = _column.get_cell_renderers()[0]
        _cellmodel = _cell.get_property('model')
        _cellmodel.clear()
        for j in range(len(_conf.RTK_HARDWARE_LIST)):
            _cellmodel.append([_conf.RTK_HARDWARE_LIST[j][0]])

        self.cmbAssembly.set_active(self._model.assembly_id)
        self.cmbSource.set_active(self._model.source)
        self.cmbDistribution.set_active(self._model.distribution_id)
        self.cmbConfType.set_active(self._model.confidence_type)
        self.cmbConfMethod.set_active(self._model.confidence_method)
        self.cmbFitMethod.set_active(self._model.fit_method)

        self.txtDescription.set_text(self._model.description)
        if self._model.confidence < 1.0:
            _confidence = self._model.confidence * 100.0
        else:
            _confidence = self._model.confidence
        self.txtConfidence.set_text(str(_confidence))
        self.txtStartTime.set_text(str(self._model.start_time))
        self.txtEndTime.set_text(str(self._model.rel_time))
        self.txtRelPoints.set_text(str(self._model.n_rel_points))

        _start_date = _util.ordinal_to_date(self._model.start_date)
        _end_date = _util.ordinal_to_date(self._model.end_date)
        self.txtStartDate.set_text(str(_start_date))
        self.txtEndDate.set_text(str(_end_date))

        # if self._nevada_chart != 0:
        #     self._load_nevada_chart()

        return False

    def _load_dataset_records(self):
        """
        Method to load the Survival analysis records into the dataset
        gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwDataset.get_model()
        _model.clear()

        _results = self._modulebook.request_load_records(self._model.survival_id)

        try:
            _n_events = len(_results)
        except TypeError:
            _n_events = 0

        for i in range(_n_events):
            _date = _util.ordinal_to_date(_results[i][2])
            _status = self._lst_status[_results[i][5]]
            _model.append([_results[i][0], _date, _results[i][1],
                           _results[i][3], _results[i][4], _results[i][7],
                           _results[i][6], _status])

        return False

    def _load_nevada_chart(self):
        """
        Method to load the Survival analysis records into the Nevada chart
        gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        import pango
        from datetime import date, datetime

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
        _gobject_types = [gobject.TYPE_STRING, gobject.TYPE_STRING,
                          gobject.TYPE_INT, gobject.TYPE_STRING]
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
            _cell = gtk.CellRendererText()       # Value to be displayed.
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
            _label.set_markup("<span weight='bold'>" +
                              _headings[i] + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=j, background=j + 1)
            _column.set_resizable(True)
            _column.set_alignment(0.5)

            _cell = gtk.CellRendererText()       # Cell background color.
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
            _data = [_date_ship[_index], 'light gray',
                     _nevada[_date_ship[_index]][0], 'light gray']
            for _jndex, _rdate in enumerate(_date_return):
                if _date_return[_jndex] not in _returns:
                    _data.append(0)
                    _data.append('light gray')
                else:
                    _data.append(_nevada[_date_ship[_index]][1][_date_return[_jndex]])
                    _data.append('#FFFFFF')
            _model.append(_data)

        return False

    def update(self):
        """
        Updates the Work Book widgets with changes to the Survival data model
        attributes.  Called by other views when the Survival data model
        attributes are edited via their gtk.Widgets().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbAssembly.handler_block(self._lst_handler_id[4])
        self.cmbAssembly.set_active(self._model.assembly_id)
        self.cmbAssembly.handler_unblock(self._lst_handler_id[4])

        self.cmbSource.handler_block(self._lst_handler_id[5])
        self.cmbSource.set_active(self._model.source)
        self.cmbSource.handler_unblock(self._lst_handler_id[5])

        self.cmbDistribution.handler_block(self._lst_handler_id[6])
        self.cmbDistribution.set_active(self._model.distribution_id)
        self.cmbDistribution.handler_unblock(self._lst_handler_id[6])

        self.cmbConfType.handler_block(self._lst_handler_id[7])
        self.cmbConfType.set_active(self._model.confidence_type)
        self.cmbConfType.handler_unblock(self._lst_handler_id[7])

        self.cmbConfMethod.handler_block(self._lst_handler_id[8])
        self.cmbConfMethod.set_active(self._model.confidence_method)
        self.cmbConfMethod.handler_unblock(self._lst_handler_id[8])

        self.cmbFitMethod.handler_block(self._lst_handler_id[9])
        self.cmbFitMethod.set_active(self._model.fit_method)
        self.cmbFitMethod.handler_unblock(self._lst_handler_id[9])

        self.txtDescription.handler_block(self._lst_handler_id[10])
        self.txtDescription.set_text(self._model.description)
        self.txtDescription.handler_unblock(self._lst_handler_id[10])

        self.txtConfidence.handler_block(self._lst_handler_id[11])
        if self._model.confidence < 1.0:
            _confidence = self._model.confidence * 100.0
        else:
            _confidence = self._model.confidence
        self.txtConfidence.set_text(str(_confidence))
        self.txtConfidence.handler_unblock(self._lst_handler_id[11])

        self.txtStartTime.handler_block(self._lst_handler_id[12])
        self.txtStartTime.set_text(str(self._model.start_time))
        self.txtStartTime.handler_unblock(self._lst_handler_id[12])

        self.txtEndTime.handler_block(self._lst_handler_id[13])
        self.txtEndTime.set_text(str(self._model.rel_time))
        self.txtEndTime.handler_unblock(self._lst_handler_id[13])

        self.txtRelPoints.handler_block(self._lst_handler_id[14])
        self.txtRelPoints.set_text(str(self._model.n_rel_points))
        self.txtRelPoints.handler_unblock(self._lst_handler_id[14])

        self.txtStartDate.handler_block(self._lst_handler_id[15])
        _start_date = _util.ordinal_to_date(self._model.start_date)
        self.txtStartDate.set_text(str(_start_date))
        self.txtStartDate.handler_unblock(self._lst_handler_id[15])

        self.txtEndDate.handler_block(self._lst_handler_id[16])
        _end_date = _util.ordinal_to_date(self._model.end_date)
        self.txtEndDate.set_text(str(_end_date))
        self.txtEndDate.handler_unblock(self._lst_handler_id[16])

        return False

    def _on_button_clicked(self, __button, index):
        """
        Method to respond to gtk.Button() clicked signals and call the correct
        function or method, passing any parameters as needed.

        :param gtk.Button __button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if index == 0:
            self._modulebook.request_add_record(self._model.survival_id)
            self._load_dataset_records()
        elif index == 1:
            self._modulebook.request_delete_record(self._model.survival_id,
                                                   self._record_id)
            self._load_dataset_records()
        elif index == 2:
            self._modulebook.request_calculate_tbf(self._model.survival_id)
            self._modulebook.request_save_records(self._model.survival_id)
            self._load_dataset_records()
        elif index == 3:
            self._modulebook.request_save_records(self._model.survival_id)
        elif index == 4:
            self._modulebook.request_add_survival(self._model.revision_id)
        elif index == 5:
            self._modulebook.request_delete_survival(self._model.survival_id)
        #elif index == 6:
        #    self._modulebook.request_consolidate_dataset(
        #        self._model.survival_id)
        elif index == 7:
            self._model.estimate_parameters()
            self.load(self._model)
        elif index == 8:
            self._modulebook.request_save_survival(self._model.survival_id)

        return False

    def _on_cellrenderer_edited(self, cell, path, new_text, position, model):
        """
        Method to respond to dataset list gtk.TreeView() gtk.CellRenderer()
        editing.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that
                         was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().  Where position is:
                             0 = record ID
                             1 = event date
                             2 = affected hardware
                             3 = left of failure interval
                             4 = right of failure interval
                             5 = interarrival time
                             6 = quantity
                             7 = status
        :param gtk.TreeModel model: the gtk.TreeModel() the edited
                                    gtk.CellRenderer() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _record = self._model.dicRecords[self._record_id]

        if position == 2:
            model[path][position] = new_text
            _record.assembly_id = new_text
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
        elif position == 7:
            _model = cell.get_property('model')
            _new_text = _model.get_value(new_text, 0)
            for j in (i for i, x in enumerate(self._lst_status)
                      if x == _new_text):
                _record.status = int(j)
            model[path][position] = _record.status

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() changed signals.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 4:                    # Assembly ID
            self._model.assembly_id = combo.get_active()
        #    _new_text = _conf.RTK_HARDWARE_LIST[combo.get_active() - 1][0]
        #    self._modulebook.update(index, _new_text)
        elif index == 5:                    # Source of records
            self._model.source = combo.get_active()
            self._modulebook.update(index - 2, self._model.source)
        elif index == 6:                    # Statistical distribution
            self._model.distribution_id = combo.get_active()
            self._modulebook.update(index - 2, self._model.distribution_id)
        elif index == 7:                   # Confidence type
            self._model.confidence_type = combo.get_active()
            self._modulebook.update(index - 1, self._model.confidence_type)
        elif index == 8:                   # Confidence method
            self._model.confidence_method = combo.get_active()
            self._modulebook.update(index - 1, self._model.confidence_method)
        elif index == 9:                   # Fit method
            self._model.fit_method = combo.get_active()
            self._modulebook.update(index - 1, self._model.fit_method)

        combo.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_focus_out(self, entry, __event, index):     # pylint: disable=R0912
        """
        Method to respond to gtk.Entry() focus_out signals.

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

        if index == 10:
            self._model.description = entry.get_text()
            self._modulebook.update(index - 8, self._model.description)
        elif index == 11:
            _new_text = float(entry.get_text())
            if _new_text > 1.0:
                _new_text = _new_text / 100.0
            self._model.confidence = _new_text
            self._modulebook.update(index - 6, self._model.confidence)
        elif index == 12:
            self._model.start_time = float(entry.get_text())
            self._modulebook.update(index + 22, self._model.start_time)
        elif index == 13:
            self._model.rel_time = float(entry.get_text())
            self._modulebook.update(index - 4, self._model.rel_time)
        elif index == 14:
            self._model.n_rel_points = int(entry.get_text())
            self._modulebook.update(index - 4, self._model.n_rel_points)
        elif index == 15:
            self._model.start_date = _util.date_to_ordinal(entry.get_text())
            self._modulebook.update(index + 20, self._model.start_date)
        elif index == 16:
            self._model.end_date = _util.date_to_ordinal(entry.get_text())
            self._modulebook.update(index + 20, self._model.end_date)

        entry.handler_unblock(self._lst_handler_id[index])

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

        if index == 17:
            self._model.grouped = button.get_active()

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_record_select(self, treeview, __path, __column):
        """
        Method to respond to the Survival dataset record gtk.TreeView() mouse
        clicks.

        :param gtk.TreeView treeview: the Dataset gtk.TreeView().
        :param str __path: the path in the Dataset gtk.TreeView() of the
                           selected record.
        :param gtk.TreeColumn __column: the selected column in the Dataset
                                        gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = treeview.get_selection().get_selected()

        self._record_id = _model.get_value(_row, 0)

        return False
