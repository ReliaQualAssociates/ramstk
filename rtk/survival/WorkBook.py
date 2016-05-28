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

# Import other RTK modules.
try:
    import Configuration
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
import __gui.gtk.Exponential as gExponential
import __gui.gtk.Gaussian as gGaussian
import __gui.gtk.KaplanMeier as gKaplanMeier
import __gui.gtk.LogNormal as gLogNormal
import __gui.gtk.MCF as gMCF
import __gui.gtk.NHPP as gNHPP
import __gui.gtk.Weibull as gWeibull

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
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

    def __init__(self, modulebook):
        """
        Initializes the Work Book view for the Survival package.

        :param workview: the :py:class:`rtk.gui.gtk.mwi.WorkView` container to
                         insert this Work Book into.
        :param modulebook: the :py:class:`rtk.survival.ModuleBook` to
                           associate with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.  The NHPP is listed twice because
        # there are two NHPP models.
        self._lst_handler_id = []
        self._lst_results = [gMCF.Results(), gKaplanMeier.Results(),
                             gNHPP.Results(), gNHPP.Results(),
                             gExponential.Results(), gLogNormal.Results(),
                             gGaussian.Results(), gWeibull.Results()]
        self._lst_plots = [gMCF.Plots(), gKaplanMeier.Plots(), gNHPP.Plots(),
                           gNHPP.Plots(), gExponential.Plots(),
                           gLogNormal.Plots(), gGaussian.Plots(),
                           gWeibull.Plots()]

        # Initialize private scalar attributes.
        self._modulebook = modulebook
        self._mdcRTK = modulebook.mdcRTK
        self._model = None
        self._record_id = None
        self._obj_results = None
        self._obj_plots = None

        # Initialize public scalar attributes.
        self.btnStartDate = Widgets.make_button(height=25, width=25,
                                                label="...", image=None)
        self.btnEndDate = Widgets.make_button(height=25, width=25,
                                              label="...", image=None)

        self.chkGroup = Widgets.make_check_button(label=_(u"Decompose results "
                                                          u"to children "
                                                          u"assemblies"))
        self.chkParts = Widgets.make_check_button(label=_(u"Decompose results "
                                                          u"to parts"))

        self.cmbAssembly = Widgets.make_combo(simple=False)
        self.cmbConfType = Widgets.make_combo()
        self.cmbConfMethod = Widgets.make_combo()
        self.cmbDistribution = Widgets.make_combo()
        self.cmbFitMethod = Widgets.make_combo()

        self.txtConfidence = Widgets.make_entry(width=50)
        self.txtDescription = Widgets.make_entry(width=200)
        self.txtStartTime = Widgets.make_entry(width=100)
        self.txtEndTime = Widgets.make_entry(width=100)
        self.txtRelPoints = Widgets.make_entry(width=100)

        self.txtStartDate = Widgets.make_entry(width=100)
        self.txtEndDate = Widgets.make_entry(width=100)

        # Set gtk.Widget() tooltips.
        self.btnStartDate.set_tooltip_text(_(u"Launches the calendar to "
                                             u"select the start date."))
        self.btnEndDate.set_tooltip_text(_(u"Launches the calendar to select "
                                           u"the end date."))
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

        self.cmbAssembly.set_tooltip_text(_(u"Selects and displays the "
                                            u"assembly associated with the "
                                            u"data set."))
        self.cmbDistribution.set_tooltip_text(_(u"Selects and displays the "
                                                u"statistical distribution "
                                                u"used to fit the data."))
        self.cmbFitMethod.set_tooltip_text(_(u"Selects and displays the "
                                             u"method used to fit the data to "
                                             u"the selected distribution."))
        self.cmbConfType.set_tooltip_text(_(u"Selects and displays the type "
                                            u"of confidence bounds."))
        self.cmbConfMethod.set_tooltip_text(_(u"Selects and displays the "
                                              u"method for developing "
                                              u"confidence bounds."))

        self.txtDescription.set_tooltip_text(_(u"Description of the selected "
                                               u"data set."))
        self.txtConfidence.set_tooltip_text(_(u"Desired statistical "
                                              u"confidence"))
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

        # Connect gtk.Widget() signals to callback methods.
        self.btnStartDate.connect('button-release-event',
                                  Utilities.date_select, self.txtStartDate)
        self.btnEndDate.connect('button-release-event', Utilities.date_select,
                                self.txtEndDate)

        self._lst_handler_id.append(
            self.cmbAssembly.connect('changed', self._on_combo_changed, 0))
        self._lst_handler_id.append(
            self.cmbDistribution.connect('changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.cmbConfType.connect('changed', self._on_combo_changed, 2))
        self._lst_handler_id.append(
            self.cmbConfMethod.connect('changed', self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.cmbFitMethod.connect('changed', self._on_combo_changed, 4))

        self._lst_handler_id.append(
            self.txtDescription.connect('focus-out-event',
                                        self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtConfidence.connect('focus-out-event',
                                       self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtStartTime.connect('focus-out-event',
                                      self._on_focus_out, 7))
        self._lst_handler_id.append(
            self.txtEndTime.connect('focus-out-event',
                                    self._on_focus_out, 8))
        self._lst_handler_id.append(
            self.txtRelPoints.connect('focus-out-event',
                                      self._on_focus_out, 9))
        self._lst_handler_id.append(
            self.txtStartDate.connect('focus-out-event',
                                      self._on_focus_out, 10))
        self.txtStartDate.connect('changed', self._on_focus_out, None, 10)
        self._lst_handler_id.append(
            self.txtEndDate.connect('focus-out-event', self._on_focus_out, 11))
        self.txtEndDate.connect('changed', self._on_focus_out, None, 11)

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
        _image.set_from_file(Configuration.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 0)
        _button.set_tooltip_text(_(u"Add a new survival analysis to the open "
                                   u"RTK Program database for the selected "
                                   u"revision."))
        _toolbar.insert(_button, _position)
        _position += 1

        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 1)
        _button.set_tooltip_text(_(u"Remove the selected survival analysis "
                                   u"from the open RTK Program database."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Calculate button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/calculate.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 2)
        _button.set_tooltip_text(_(u"Analyzes the selected survival "
                                   u"analysis."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Save button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 3)
        _button.set_tooltip_text(_(u"Saves the selected survival analysis and "
                                   u"it's records."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Save all button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(Configuration.ICON_DIR + '32x32/save-all.png')
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._on_button_clicked, 4)
        _button.set_tooltip_text(_(u"Saves all of the survival analyses and "
                                   u"their records."))
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Survival class gtk.Notebook().
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[2] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[2] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[2] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_analyses_input_page(_notebook)

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

        _fixed = gtk.Fixed()

        _frame = Widgets.make_frame(label=_(u"Analysis Inputs"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        _frame.add(_fixed)

        _hbox.pack1(_frame, True, True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis input information. #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets.
        _results = [[u"MCF"], [u"Kaplan-Meier"], [_(u"NHPP - Power Law")],
                    [u"NHPP - Loglinear"], [_(u"Exponential")],
                    [_(u"Lognormal")], [_(u"Normal")], [u"Weibull"],
                    ["WeiBayes"]]
        Widgets.load_combo(self.cmbDistribution, _results)
        _results = [[_(u"Lower One-Sided")], [_(u"Upper One-Sided")],
                    [_(u"Two-Sided")]]
        Widgets.load_combo(self.cmbConfType, _results)
        _results = [[_(u"Crow (NHPP Only)")], [_(u"Duane (NHPP Only)")],
                    [_(u"Fisher Matrix")], [_(u"Likelihood")],
                    [_(u"Bootstrap")]]
        Widgets.load_combo(self.cmbConfMethod, _results)
        _results = [["MLE"], [_(u"Regression")]]
        Widgets.load_combo(self.cmbFitMethod, _results)

        # Create the labels for the left half of the right side.
        _labels = [_(u"Assembly:"), _(u"Description:"), _(u"Distribution:"),
                   _("Fit Method:"), _(u"Confidence:"), _(u"Confidence Type:"),
                   _("Confidence Method:")]
        (_x_pos1, _y_pos1) = Widgets.make_labels(_labels, _fixed, 5, 5)
        _x_pos1 += 55

        # Create the labels for the right half of the right side.
        _labels = [_(u"Start Time:"), _(u"End Time:"), _(u"Step Interval:"),
                   _(u"Start Date:"), _(u"End Date:")]
        (_x_pos2,
         _y_pos2) = Widgets.make_labels(_labels, _fixed, _x_pos1 + 215, 5)
        _x_pos2 += _x_pos1
        _x_pos2 += 275

        # Place widgets on the left side.
        _fixed.put(self.cmbAssembly, _x_pos1, _y_pos1[0])
        _fixed.put(self.txtDescription, _x_pos1, _y_pos1[1])
        _fixed.put(self.cmbDistribution, _x_pos1, _y_pos1[2])
        _fixed.put(self.cmbFitMethod, _x_pos1, _y_pos1[3])
        _fixed.put(self.txtConfidence, _x_pos1, _y_pos1[4])
        _fixed.put(self.cmbConfType, _x_pos1, _y_pos1[5])
        _fixed.put(self.cmbConfMethod, _x_pos1, _y_pos1[6])

        # Place widgets on the right side.
        _fixed.put(self.txtStartTime, _x_pos2, _y_pos2[0])
        _fixed.put(self.txtEndTime, _x_pos2, _y_pos2[1])
        _fixed.put(self.txtRelPoints, _x_pos2, _y_pos2[2])
        _fixed.put(self.txtStartDate, _x_pos2, _y_pos2[3])
        _fixed.put(self.btnStartDate, _x_pos2 + 105, _y_pos2[3])
        _fixed.put(self.txtEndDate, _x_pos2, _y_pos2[4])
        _fixed.put(self.btnEndDate, _x_pos2 + 105, _y_pos2[4])
        _fixed.put(self.chkGroup, _x_pos2, _y_pos2[4] + 30)
        _fixed.put(self.chkParts, _x_pos2, _y_pos2[4] + 60)

        _fixed.show_all()

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

    def load(self, model):
        """
        Method to load the Survival class gtk.Notebook().

        :param model: the :py:class:`rtk.survival.Survival.Model` whose
                      attributes will be loaded into the display widgets.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model = model

        self._load_analysis_inputs_page()

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
        self.cmbAssembly.handler_block(self._lst_handler_id[0])
        Widgets.load_combo(self.cmbAssembly, Configuration.RTK_HARDWARE_LIST,
                           simple=False)
        self.cmbAssembly.handler_unblock(self._lst_handler_id[0])

        self.cmbAssembly.set_active(self._model.assembly_id)
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

        _start_date = Utilities.ordinal_to_date(self._model.start_date)
        _end_date = Utilities.ordinal_to_date(self._model.end_date)
        self.txtStartDate.set_text(str(_start_date))
        self.txtEndDate.set_text(str(_end_date))

        return False

    def update(self):
        """
        Updates the Work Book widgets with changes to the Survival data model
        attributes.  Called by other views when the Survival data model
        attributes are edited via their gtk.Widgets().

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.cmbAssembly.handler_block(self._lst_handler_id[0])
        self.cmbAssembly.set_active(self._model.assembly_id)
        self.cmbAssembly.handler_unblock(self._lst_handler_id[0])

        self.cmbDistribution.handler_block(self._lst_handler_id[1])
        self.cmbDistribution.set_active(self._model.distribution_id)
        self.cmbDistribution.handler_unblock(self._lst_handler_id[1])

        self.cmbConfType.handler_block(self._lst_handler_id[2])
        self.cmbConfType.set_active(self._model.confidence_type)
        self.cmbConfType.handler_unblock(self._lst_handler_id[2])

        self.cmbConfMethod.handler_block(self._lst_handler_id[3])
        self.cmbConfMethod.set_active(self._model.confidence_method)
        self.cmbConfMethod.handler_unblock(self._lst_handler_id[3])

        self.cmbFitMethod.handler_block(self._lst_handler_id[4])
        self.cmbFitMethod.set_active(self._model.fit_method)
        self.cmbFitMethod.handler_unblock(self._lst_handler_id[4])

        self.txtDescription.handler_block(self._lst_handler_id[5])
        self.txtDescription.set_text(self._model.description)
        self.txtDescription.handler_unblock(self._lst_handler_id[5])

        self.txtConfidence.handler_block(self._lst_handler_id[6])
        if self._model.confidence < 1.0:
            Configurationidence = self._model.confidence * 100.0
        else:
            Configurationidence = self._model.confidence
        self.txtConfidence.set_text(str(Configurationidence))
        self.txtConfidence.handler_unblock(self._lst_handler_id[6])

        self.txtStartTime.handler_block(self._lst_handler_id[7])
        self.txtStartTime.set_text(str(self._model.start_time))
        self.txtStartTime.handler_unblock(self._lst_handler_id[7])

        self.txtEndTime.handler_block(self._lst_handler_id[8])
        self.txtEndTime.set_text(str(self._model.rel_time))
        self.txtEndTime.handler_unblock(self._lst_handler_id[8])

        self.txtRelPoints.handler_block(self._lst_handler_id[9])
        self.txtRelPoints.set_text(str(self._model.n_rel_points))
        self.txtRelPoints.handler_unblock(self._lst_handler_id[9])

        self.txtStartDate.handler_block(self._lst_handler_id[10])
        _start_date = Utilities.ordinal_to_date(self._model.start_date)
        self.txtStartDate.set_text(str(_start_date))
        self.txtStartDate.handler_unblock(self._lst_handler_id[10])

        self.txtEndDate.handler_block(self._lst_handler_id[11])
        _end_date = Utilities.ordinal_to_date(self._model.end_date)
        self.txtEndDate.set_text(str(_end_date))
        self.txtEndDate.handler_unblock(self._lst_handler_id[11])

        return False

    def _on_button_clicked(self, __button, index):
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

        if index == 0:
            self._mdcRTK.dtcSurvival.add_survival(self._model.revision_id)
            self._modulebook.request_load_data()
        elif index == 1:
            self._mdcRTK.dtcSurvival.delete_survival(self._model.survival_id)
            self._modulebook.request_load_data()
        elif index == 2:
            _survival_id = self._model.survival_id
            if self._mdcRTK.dtcSurvival.request_calculate(_survival_id):
                Widgets.rtk_error(_(u"Error calculating survival analysis."))
            else:
                self.load(self._model)
        elif index == 3:
            self._mdcRTK.dtcSurvival.save_survival(self._model.survival_id)
        elif index == 4:
            self._mdcRTK.dtcSurvival.save_all_survivals()

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() 'changed' signals.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 0:                    # Assembly ID
            self._model.assembly_id = combo.get_active()
            try:
                _new_text = Configuration.RTK_HARDWARE_LIST[self._model.assembly_id][0]
            except IndexError:
                _new_text = ''
            self._modulebook.update(1, str(_new_text))
        elif index == 1:                    # Statistical distribution
            self._model.distribution_id = combo.get_active()
            self._modulebook.update(4, self._model.distribution_id)
        elif index == 2:                   # Confidence type
            self._model.confidence_type = combo.get_active()
            self._modulebook.update(6, self._model.confidence_type)
        elif index == 3:                   # Confidence method
            self._model.confidence_method = combo.get_active()
            self._modulebook.update(7, self._model.confidence_method)
        elif index == 4:                   # Fit method
            self._model.fit_method = combo.get_active()
            self._modulebook.update(8, self._model.fit_method)

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

        if index == 5:
            self._model.description = entry.get_text()
            self._modulebook.update(2, self._model.description)
        elif index == 6:
            _new_text = float(entry.get_text())
            if _new_text > 1.0:
                _new_text = _new_text / 100.0
            self._model.confidence = _new_text
            self._modulebook.update(5, self._model.confidence)
        elif index == 7:
            self._model.start_time = float(entry.get_text())
            self._modulebook.update(34, self._model.start_time)
        elif index == 8:
            self._model.end_time = float(entry.get_text())
            self._model.rel_time = float(entry.get_text())
            self._modulebook.update(9, self._model.rel_time)
        elif index == 9:
            self._model.n_rel_points = int(entry.get_text())
            self._modulebook.update(10, self._model.n_rel_points)
        elif index == 10:
            self._model.start_date = Utilities.date_to_ordinal(entry.get_text())
            self._modulebook.update(35, self._model.start_date)
        elif index == 11:
            self._model.end_date = Utilities.date_to_ordinal(entry.get_text())
            self._modulebook.update(36, self._model.end_date)

        entry.handler_unblock(self._lst_handler_id[index])

        return False
