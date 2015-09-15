#!/usr/bin/env python
"""
#################################
Validation Package Work Book View
#################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.validation.WorkBook.py is part of The RTK Project
#
# All rights reserved.

import sys
from datetime import date

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

# Import plotting modules.
import matplotlib
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
    from analyses.statistics.Bounds import calculate_beta_bounds
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg
    from rtk.analyses.statistics.Bounds import calculate_beta_bounds
# from Assistants import AddTask

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class WorkView(gtk.VBox):                   # pylint: disable=R0902, R0904
    """
    The Work Book view displays all the attributes for the selected
    Validation item.  The attributes of a Work Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Validation attribute.

    :ivar :py:class:`rtk.gui.gtk.WorkBook` _workview: the RTK top level Work
                                                      View window to embed the
                                                      Validation Work Book
                                                      into.
    :ivar :py:class:`rtk.validation.Validation.Model` _model: the Validation
                                                              data model whose
                                                              attributes are
                                                              being displayed.

    +----------+-------------------------------------------+
    | Position | Widget - Signal                           |
    +==========+===========================================+
    |     0    | txtTask `focus_out_event`                 |
    +----------+-------------------------------------------+
    |     1    | cmbTaskType `changed`                     |
    +----------+-------------------------------------------+
    |     2    | txtSpecification `focus_out_event`        |
    +----------+-------------------------------------------+
    |     3    | cmbMeasurementUnit `changed`              |
    +----------+-------------------------------------------+
    |     4    | txtMinAcceptable `focus_out_event`        |
    +----------+-------------------------------------------+
    |     5    | txtMeanAcceptable `focus_out_event`       |
    +----------+-------------------------------------------+
    |     6    | txtMaxAcceptable `focus_out_event`        |
    +----------+-------------------------------------------+
    |     7    | txtVarAcceptable `focus_out_event`        |
    +----------+-------------------------------------------+
    |     8    | txtStartDate `changed` `focus_out_event`  |
    +----------+-------------------------------------------+
    |     9    | txtEndDate `changed` `focus_out_event`    |
    +----------+-------------------------------------------+
    |    10    | spnStatus `value_changed`                 |
    +----------+-------------------------------------------+
    |    11    | txtMinTime `focus_out_event`              |
    +----------+-------------------------------------------+
    |    12    | txtExpTime `focus_out_event`              |
    +----------+-------------------------------------------+
    |    13    | txtMaxTime `focus_out_event`              |
    +----------+-------------------------------------------+
    |    14    | txtMinCost `focus_out_event`              |
    +----------+-------------------------------------------+
    |    15    | txtExpCost `focus_out_event`              |
    +----------+-------------------------------------------+
    |    16    | txtMaxCost `focus_out_event`              |
    +----------+-------------------------------------------+

    :ivar :py:class:`rtk.validation.Validation.Validation` dtcValidation: the
        data controller to use with this Work Book.

    :ivar gtk.Button btnEndDate:
    :ivar gtk.Button btnStartDate:
    :ivar gtk.Combo cmbTaskType:
    :ivar gtk.Combo cmbMeasurementUnit:
    :ivar gtk.SpinButton spnStatus:
    :ivar gtk.Entry txtID:
    :ivar gtk.Entry txtMaxAcceptable:
    :ivar gtk.Entry txtMeanAcceptable:
    :ivar gtk.Entry txtMinAcceptable:
    :ivar gtk.Entry txtVarAcceptable:
    :ivar gtk.Entry txtSpecification:
    :ivar gtk.Entry txtTask:
    :ivar gtk.Entry txtEndDate:
    :ivar gtk.Entry txtStartDate:
    :ivar gtk.Entry txtMinTime:
    :ivar gtk.Entry txtExpTime:
    :ivar gtk.Entry txtMaxTime:
    :ivar gtk.Entry txtMinCost:
    :ivar gtk.Entry txtExpCost:
    :ivar gtk.Entry txtMaxCost:
    :ivar gtk.Entry txtMeanTimeLL:
    :ivar gtk.Entry txtMeanTime:
    :ivar gtk.Entry txtMeanTimeUL:
    :ivar gtk.Entry txtMeanCostLL:
    :ivar gtk.Entry txtMeanCost:
    :ivar gtk.Entry txtMeanCostUL:
    :ivar gtk.Entry txtProjectTimeLL:
    :ivar gtk.Entry txtProjectTime:
    :ivar gtk.Entry txtProjectTimeUL:
    :ivar gtk.Entry txtProjectCostLL:
    :ivar gtk.Entry txtProjectCost:
    :ivar gtk.Entry txtProjectCostUL:
    :ivar mpl.FigureCanvas pltPlot1:
    :ivar mpl.Axes axAxis1:
    """

    def __init__(self, workview, modulebook):
        """
        Initializes the Work Book view for the Validation package.

        :param workview: the :py:class:`rtk.gui.gtk.mwi.WorkView` container to
                         insert this Work Book into.
        :param modulebook: the :py:class:`rtk.validation.ModuleBook` to
                           associate with this Work Book.
        """

        gtk.VBox.__init__(self)

        # Initialize private dict attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._workview = workview
        self._modulebook = modulebook
        self._model = None

        # Initialize public scalar attributes.
        self.dtcValidation = modulebook.dtcValidation

        # General Data tab widgets.
        self.btnEndDate = _widg.make_button(height=25, width=25,
                                            label="...", image=None)
        self.btnStartDate = _widg.make_button(height=25, width=25,
                                              label="...", image=None)

        self.cmbTaskType = _widg.make_combo()
        self.cmbMeasurementUnit = _widg.make_combo()
        self.spnStatus = gtk.SpinButton()
        self.txtID = _widg.make_entry(width=50, editable=False)
        self.txtMaxAcceptable = _widg.make_entry(width=100)
        self.txtMeanAcceptable = _widg.make_entry(width=100)
        self.txtMinAcceptable = _widg.make_entry(width=100)
        self.txtVarAcceptable = _widg.make_entry(width=100)
        self.txtSpecification = _widg.make_entry()
        self.txtTask = _widg.make_text_view(width=400)
        self.txtEndDate = _widg.make_entry(width=100)
        self.txtStartDate = _widg.make_entry(width=100)
        self.txtMinTime = _widg.make_entry(width=100)
        self.txtExpTime = _widg.make_entry(width=100)
        self.txtMaxTime = _widg.make_entry(width=100)
        self.txtMinCost = _widg.make_entry(width=100)
        self.txtExpCost = _widg.make_entry(width=100)
        self.txtMaxCost = _widg.make_entry(width=100)
        self.txtMeanTimeLL = _widg.make_entry(width=100, editable=False)
        self.txtMeanTime = _widg.make_entry(width=100, editable=False)
        self.txtMeanTimeUL = _widg.make_entry(width=100, editable=False)
        self.txtMeanCostLL = _widg.make_entry(width=100, editable=False)
        self.txtMeanCost = _widg.make_entry(width=100, editable=False)
        self.txtMeanCostUL = _widg.make_entry(width=100, editable=False)

        # These widgets are for the Project Effort.
        self.txtProjectTimeLL = _widg.make_entry(width=100, editable=False)
        self.txtProjectTime = _widg.make_entry(width=100, editable=False)
        self.txtProjectTimeUL = _widg.make_entry(width=100, editable=False)
        self.txtProjectCostLL = _widg.make_entry(width=100, editable=False)
        self.txtProjectCost = _widg.make_entry(width=100, editable=False)
        self.txtProjectCostUL = _widg.make_entry(width=100, editable=False)

        # Create the Plot tab widgets.
        _figure = Figure()
        self.pltPlot1 = FigureCanvas(_figure)
        self.axAxis1 = _figure.add_subplot(111)

        # Put it all together.
        _toolbar = self._create_toolbar()
        self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_end(_notebook)

        self.show_all()

    def _create_toolbar(self):
        """
        Method to create the toolbar for the VALIDATAION class Work Book.
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add item button.  Depending on the notebook page selected will
        # determine what type of item is added.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _button.set_name('Add')
        _button.connect('clicked', self._on_button_clicked, 0)
        _button.set_tooltip_text(_(u"Adds a new V&V activity."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Remove item button.  Depending on the notebook page selected will
        # determine what type of item is removed.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.set_name('Remove')
        _button.connect('clicked', self._on_button_clicked, 1)
        _button.set_tooltip_text(_(u"Deletes the selected V&V activity."))
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Calculate button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        _button.set_icon_widget(_image)
        _button.set_name('Analyze')
        _button.connect('clicked', self._on_button_clicked, 2)
        _button.set_tooltip_text(_(u"Calculates program Verification & "
                                   u"Validation effort and plots the "
                                   u"results."))
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save results button.  Depending on the notebook page selected will
        # determine which results are saved.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.set_name('Save')
        _button.connect('clicked', self._on_button_clicked, 3)
        _button.set_tooltip_text(_(u"Saves all Verification & Validation "
                                   u"tasks."))
        _toolbar.insert(_button, _position)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Validation class gtk.Notebook().
        """

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

        self._create_general_data_tab(_notebook)
        self._create_plot_tab(_notebook)

        return _notebook

    def _create_general_data_tab(self, notebook):
        """
        Method to create the Validation class gtk.Notebook() page for
        displaying general data about the selected Validation.

        :param gtk.Notebook notebook: the Validation class gtk.Notebook()
                                      widget.
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        # Build the quadrant 1 (upper left) containers.
        _fxdGenDataQuad1 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdGenDataQuad1)

        _frame = _widg.make_frame(label=_(u"Task Description"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_start(_frame, True, True)

        # Build the quadrant 2 (upper right) containers.
        _vpaned = gtk.VPaned()

        _fxdGenDataQuad2 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdGenDataQuad2)

        _frame = _widg.make_frame(label=_(u"Task Effort"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack1(_frame, True, True)

        # Build the quadrant 4 (lower right) containers.
        _fxdGenDataQuad4 = gtk.Fixed()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fxdGenDataQuad4)

        _frame = _widg.make_frame(label=_(u"Project Effort"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vpaned.pack2(_frame, True, True)

        _hbox.pack_end(_vpaned)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the gtk.ComboBox() widgets.
        _model = self.cmbTaskType.get_model()
        _model.clear()

        self.cmbTaskType.append_text("")
        for i in range(len(_conf.RTK_TASK_TYPE)):
            self.cmbTaskType.append_text(_conf.RTK_TASK_TYPE[i])

        _model = self.cmbMeasurementUnit.get_model()
        _model.clear()

        self.cmbMeasurementUnit.append_text("")
        for i in range(len(_conf.RTK_MEASUREMENT_UNITS)):
            self.cmbMeasurementUnit.append_text(_conf.RTK_MEASUREMENT_UNITS[i])

        # Create the labels for quadrant #1.
        _labels = [_(u"Task ID:"), _(u"Task Description:"), _(u"Task Type:"),
                   _(u"Specification:"), _(u"Measurement Unit:"),
                   _(u"Minimum Acceptable:"), _(u"Maximum Acceptable:"),
                   _(u"Mean Acceptable:"), _(u"Variance:")]

        _max1 = 0
        _max2 = 0
        (_max1, _y_pos) = _widg.make_labels(_labels[2:],
                                            _fxdGenDataQuad1, 5, 140)

        _label = _widg.make_label(_labels[0], -1, 25)
        _fxdGenDataQuad1.put(_label, 5, 5)
        _max2 = _label.size_request()[0]
        _x_pos = max(_max1, _max2) + 20

        _label = _widg.make_label(_labels[1], 150, 25)
        _fxdGenDataQuad1.put(_label, 5, 35)
        _max2 = _label.size_request()[0]
        _x_pos = max(_x_pos, _max2) + 20

        # Place the quadrant #1 widgets.
        self.txtID.set_tooltip_text(_(u"Displays the unique code for the "
                                      u"selected V&V activity."))
        self.txtTask.set_tooltip_text(_(u"Displays the description of the "
                                        u"selected V&V activity."))
        self.cmbTaskType.set_tooltip_text(_(u"Selects and displays the type "
                                            u"of task for the selected V&V "
                                            u"activity."))
        self.txtSpecification.set_tooltip_text(_(u"Displays the internal or "
                                                 u"industry specification or "
                                                 u"procedure governing the "
                                                 u"selected V&V activity."))
        self.cmbMeasurementUnit.set_tooltip_text(_(u"Selects and displays the "
                                                   u"measurement unit for the "
                                                   u"selected V&V activity "
                                                   u"acceptance parameter."))
        self.txtMinAcceptable.set_tooltip_text(_(u"Displays the minimum "
                                                 u"acceptable value for the "
                                                 u"selected V&V activity."))
        self.txtMeanAcceptable.set_tooltip_text(_(u"Displays the mean "
                                                  u"acceptable value for the "
                                                  u"selected V&V activity."))
        self.txtMaxAcceptable.set_tooltip_text(_(u"Displays the maximum "
                                                 u"acceptable value for the "
                                                 u"selected V&V activity."))
        self.txtVarAcceptable.set_tooltip_text(_(u"Displays the acceptable "
                                                 u"variance for the selected "
                                                 u"V&V activity."))
        self.btnEndDate.set_tooltip_text(_(u"Launches the calendar to select "
                                           u"the date the task was "
                                           u"completed."))
        self.btnStartDate.set_tooltip_text(_(u"Launches the calendar to "
                                             u"select the date the task was "
                                             u"started."))
        self.txtStartDate.set_tooltip_text(_(u"Displays the date the selected "
                                             u"V&V activity is scheduled to "
                                             u"start."))
        self.txtEndDate.set_tooltip_text(_(u"Displays the date the selected "
                                           u"V&V activity is scheduled to "
                                           u"end."))
        self.spnStatus.set_tooltip_text(_(u"Displays % complete of the "
                                          u"selected V&V activity."))
        self.txtMinTime.set_tooltip_text(_(u"Minimum person-time needed to "
                                           u"complete the selected task."))
        self.txtExpTime.set_tooltip_text(_(u"Most likely person-time needed "
                                           u"to complete the selected task."))
        self.txtMaxTime.set_tooltip_text(_(u"Maximum person-time needed to "
                                           u"complete the selected task."))
        self.txtMinCost.set_tooltip_text(_(u"Minimim cost of the selected "
                                           u"task."))
        self.txtExpCost.set_tooltip_text(_(u"Most likely cost of the selected "
                                           u"task."))
        self.txtMaxCost.set_tooltip_text(_(u"Maximum cost of the selected "
                                           u"task."))
        # self.txtMeanCost.set_tooltip_text(_(u"Average estimated cost to "
        #                                    u"complete the project."))
        # self.txtMeanTime.set_tooltip_text(_(u"Average estimated time "
        #                                    u"needed to complete the "
        #                                    u"project."))

        _fxdGenDataQuad1.put(self.txtID, _x_pos, 5)
        _fxdGenDataQuad1.put(self.txtTask, _x_pos, 35)
        _buffer = self.txtTask.get_child().get_child()
        _fxdGenDataQuad1.put(self.cmbTaskType, _x_pos, _y_pos[0])
        _fxdGenDataQuad1.put(self.txtSpecification, _x_pos, _y_pos[1])
        _fxdGenDataQuad1.put(self.cmbMeasurementUnit, _x_pos, _y_pos[2] - 3)
        _fxdGenDataQuad1.put(self.txtMinAcceptable, _x_pos, _y_pos[3])
        _fxdGenDataQuad1.put(self.txtMaxAcceptable, _x_pos, _y_pos[4])
        _fxdGenDataQuad1.put(self.txtMeanAcceptable, _x_pos, _y_pos[5])
        _fxdGenDataQuad1.put(self.txtVarAcceptable, _x_pos, _y_pos[6])

        _fxdGenDataQuad1.show_all()

        # Create the labels for quadrant #2.
        _labels = [_(u"Start Date:"), _(u"End Date:"), _(u"% Complete:"),
                   _(u"Minimum Task Time:"), _(u"Most Likely Task Time:"),
                   _(u"Maximum Task Time:"), _(u"Task Time (95% Confidence):"),
                   _(u"Minimum Task Cost:"), _(u"Most Likely Task Cost:"),
                   _(u"Maximum Task Cost:"), _(u"Task Cost (95% Confidence):")]
        (_max1, _y_pos1) = _widg.make_labels(_labels, _fxdGenDataQuad2, 5, 5)

        # Create the labels for quadrant #4.
        _labels = [_(u"Project Time (95% Confidence):"),
                   _(u"Project Cost (95% Confidence):")]
        (_max2, _y_pos2) = _widg.make_labels(_labels, _fxdGenDataQuad4, 5, 5)
        _x_pos = max(_max1, _max2) + 40

        # Place the quadrant #2 widgets.
        _fxdGenDataQuad2.put(self.btnEndDate, _x_pos + 105, _y_pos1[1])
        _fxdGenDataQuad2.put(self.btnStartDate, _x_pos + 105, _y_pos1[0])
        _fxdGenDataQuad2.put(self.txtStartDate, _x_pos, _y_pos1[0])
        _fxdGenDataQuad2.put(self.txtEndDate, _x_pos, _y_pos1[1])
        _fxdGenDataQuad2.put(self.spnStatus, _x_pos, _y_pos1[2])
        _fxdGenDataQuad2.put(self.txtMinTime, _x_pos, _y_pos1[3])
        _fxdGenDataQuad2.put(self.txtExpTime, _x_pos, _y_pos1[4])
        _fxdGenDataQuad2.put(self.txtMaxTime, _x_pos, _y_pos1[5])
        _fxdGenDataQuad2.put(self.txtMeanTimeLL, _x_pos, _y_pos1[6])
        _fxdGenDataQuad2.put(self.txtMeanTime, _x_pos + 105, _y_pos1[6])
        _fxdGenDataQuad2.put(self.txtMeanTimeUL, _x_pos + 210, _y_pos1[6])
        _fxdGenDataQuad2.put(self.txtMinCost, _x_pos, _y_pos1[7])
        _fxdGenDataQuad2.put(self.txtExpCost, _x_pos, _y_pos1[8])
        _fxdGenDataQuad2.put(self.txtMaxCost, _x_pos, _y_pos1[9])
        _fxdGenDataQuad2.put(self.txtMeanCostLL, _x_pos, _y_pos1[10])
        _fxdGenDataQuad2.put(self.txtMeanCost, _x_pos + 105, _y_pos1[10])
        _fxdGenDataQuad2.put(self.txtMeanCostUL, _x_pos + 210, _y_pos1[10])

        _fxdGenDataQuad2.show_all()

        # Place the quadrant #4 widgets.
        _fxdGenDataQuad4.put(self.txtProjectTimeLL, _x_pos, _y_pos2[0])
        _fxdGenDataQuad4.put(self.txtProjectTime, _x_pos + 105, _y_pos2[0])
        _fxdGenDataQuad4.put(self.txtProjectTimeUL, _x_pos + 210, _y_pos2[0])
        _fxdGenDataQuad4.put(self.txtProjectCostLL, _x_pos, _y_pos2[1])
        _fxdGenDataQuad4.put(self.txtProjectCost, _x_pos + 105, _y_pos2[1])
        _fxdGenDataQuad4.put(self.txtProjectCostUL, _x_pos + 210, _y_pos2[1])

        _fxdGenDataQuad4.show_all()

        self._lst_handler_id.append(_buffer.connect('focus-out-event',
                                                    self._on_focus_out, 0))
        self._lst_handler_id.append(self.cmbTaskType.connect(
            'changed', self._on_combo_changed, 1))
        self._lst_handler_id.append(
            self.txtSpecification.connect('focus-out-event',
                                          self._on_focus_out, 2))
        self._lst_handler_id.append(
            self.cmbMeasurementUnit.connect('changed',
                                            self._on_combo_changed, 3))
        self._lst_handler_id.append(
            self.txtMinAcceptable.connect('focus-out-event',
                                          self._on_focus_out, 4))
        self._lst_handler_id.append(
            self.txtMeanAcceptable.connect('focus-out-event',
                                           self._on_focus_out, 5))
        self._lst_handler_id.append(
            self.txtMaxAcceptable.connect('focus-out-event',
                                          self._on_focus_out, 6))
        self._lst_handler_id.append(
            self.txtVarAcceptable.connect('focus-out-event',
                                          self._on_focus_out, 7))
        self.btnEndDate.connect('button-release-event', _util.date_select,
                                self.txtEndDate)
        self.btnStartDate.connect('button-release-event', _util.date_select,
                                  self.txtStartDate)
        self.txtStartDate.connect('changed', self._on_focus_out, None, 8)
        self._lst_handler_id.append(
            self.txtStartDate.connect('focus-out-event',
                                      self._on_focus_out, 8))
        self.txtEndDate.connect('changed', self._on_focus_out, None, 9)
        self._lst_handler_id.append(self.txtEndDate.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            9))
        self._lst_handler_id.append(self.spnStatus.connect(
            'value-changed', self._on_value_changed, 10))
        self._lst_handler_id.append(self.txtMinTime.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            11))
        self._lst_handler_id.append(self.txtExpTime.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            12))
        self._lst_handler_id.append(self.txtMaxTime.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            13))
        self._lst_handler_id.append(self.txtMinCost.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            14))
        self._lst_handler_id.append(self.txtExpCost.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            15))
        self._lst_handler_id.append(self.txtMaxCost.connect('focus-out-event',
                                                            self._on_focus_out,
                                                            16))

        # Set the spin button to be a 0-100 in steps of 0.1 spinner.  Only
        # update if value is numeric and within range.
        self.spnStatus.set_adjustment(gtk.Adjustment(0, 0, 100, 1, 0.1))
        self.spnStatus.set_update_policy(gtk.UPDATE_IF_VALID)
        self.spnStatus.set_numeric(True)
        self.spnStatus.set_snap_to_ticks(True)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"General\nData") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays general information about the "
                                  u"selected V&V task."))
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

    def _create_plot_tab(self, notebook):
        """
        Method to create the gtk.Notebook() tab and populate it with the
        appropriate widgets for the plot showing the planned and actual
        burndown of V&V tasks.
        """

        _hbox = gtk.HBox()

        _frame = _widg.make_frame(label=_(u""))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_hbox)
        _frame.show_all()

        _hbox.pack_start(self.pltPlot1)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Program\nProgress") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Shows a plot of the total expected time "
                                  u"to complete all V&amp;V tasks and the "
                                  u"current progress."))
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Validation class gtk.Notebook().

        :param :py:class:`rtk.validation.Validation.Model` model: the data
                                                                  model to
                                                                  load.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        from math import sqrt
        from scipy.stats import norm        # pylint: disable=E0611

        self._model = model

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Load the General Data information.                            #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _start_date = _util.ordinal_to_date(model.start_date)
        _end_date = _util.ordinal_to_date(model.end_date)

        self.txtID.set_text(str(model.validation_id))
        _textbuffer = self.txtTask.get_child().get_child().get_buffer()
        _textbuffer.set_text(model.task_description)
        self.cmbTaskType.set_active(model.task_type)
        self.txtSpecification.set_text(str(model.task_specification))
        self.cmbMeasurementUnit.set_active(model.measurement_unit)
        self.txtMinAcceptable.set_text(str(fmt.format(model.min_acceptable)))
        self.txtMeanAcceptable.set_text(str(fmt.format(model.mean_acceptable)))
        self.txtMaxAcceptable.set_text(str(fmt.format(model.max_acceptable)))
        self.txtVarAcceptable.set_text(
            str(fmt.format(model.variance_acceptable)))
        self.txtStartDate.set_text(str(_start_date))
        self.txtEndDate.set_text(str(_end_date))
        self.spnStatus.set_value(model.status)
        self.txtMinTime.set_text(str(fmt.format(model.minimum_time)))
        self.txtExpTime.set_text(str(fmt.format(model.average_time)))
        self.txtMaxTime.set_text(str(fmt.format(model.maximum_time)))
        self.txtMinCost.set_text(str(fmt.format(model.minimum_cost)))
        self.txtExpCost.set_text(str(fmt.format(model.average_cost)))
        self.txtMaxCost.set_text(str(fmt.format(model.maximum_cost)))

        _z_norm = norm.ppf(1.0 - ((1.0 - model.confidence / 100.0) / 2.0))

        # Calculate expected task time confidence limits assuming a beta
        # distribution.
        _std_err = sqrt(model.time_variance)
        _meanll = model.mean_time - _z_norm * _std_err
        _meanul = model.mean_time + _z_norm * _std_err

        self.txtMeanTimeLL.set_text(str(fmt.format(_meanll)))
        self.txtMeanTime.set_text(str(fmt.format(model.mean_time)))
        self.txtMeanTimeUL.set_text(str(fmt.format(_meanul)))

        # Calculate expected task cost confidence limits assuming a beta
        # distribution.
        _std_err = sqrt(model.cost_variance)
        _meanll = model.mean_cost - _z_norm * _std_err
        _meanul = model.mean_cost + _z_norm * _std_err

        self.txtMeanCostLL.set_text(str(fmt.format(_meanll)))
        self.txtMeanCost.set_text(str(fmt.format(model.mean_cost)))
        self.txtMeanCostUL.set_text(str(fmt.format(_meanul)))

        # Calculate expected project time confidence limits assuming a beta
        # distribution.
        _min = sum([x.minimum_time
                    for x in self.dtcValidation.dicTasks.values()])
        _avg = sum([x.average_time
                    for x in self.dtcValidation.dicTasks.values()])
        _max = sum([x.maximum_time
                    for x in self.dtcValidation.dicTasks.values()])

        (_meanll,
         _mean,
         _meanul,
         __) = calculate_beta_bounds(_min, _avg, _max, model.confidence)

        self.txtProjectTimeLL.set_text(str(fmt.format(_meanll)))
        self.txtProjectTime.set_text(str(fmt.format(_mean)))
        self.txtProjectTimeUL.set_text(str(fmt.format(_meanul)))

        # Calculate expected project cost confidence limits assuming a beta
        # distribution.
        _min = sum([x.minimum_cost
                    for x in self.dtcValidation.dicTasks.values()])
        _avg = sum([x.average_cost
                    for x in self.dtcValidation.dicTasks.values()])
        _max = sum([x.maximum_cost
                    for x in self.dtcValidation.dicTasks.values()])

        (_meanll,
         _mean,
         _meanul,
         __) = calculate_beta_bounds(_min, _avg, _max, model.confidence)

        self.txtProjectCostLL.set_text(str(fmt.format(_meanll)))
        self.txtProjectCost.set_text(str(fmt.format(_mean)))
        self.txtProjectCostUL.set_text(str(fmt.format(_meanul)))

        self.get_children()[1].set_current_page(0)

        return False

    def _load_progress_plot(self):
        """
        Method to load the Validation class effort progress plot.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _assess_dates = []
        _targets = []

        for _task in self.dtcValidation.dicTasks.values():
            if _conf.RTK_TASK_TYPE[_task.task_type] == 'Reliability, Assessment':
                _assess_dates.append(_util.date_to_ordinal(_task.end_date))
            _targets.append([_task.min_acceptable, _task.max_acceptable])

        # Find the earliest start date, the total number of hours for minimum,
        # most likely, and maximum task time.
        try:
            _x = [min([_task.start_date
                       for _task in self.dtcValidation.dicTasks.values()])]
            _y1 = [sum([_task.minimum_time
                        for _task in self.dtcValidation.dicTasks.values()])]
            _y2 = [sum([_task.average_time
                        for _task in self.dtcValidation.dicTasks.values()])]
            _y3 = [sum([_task.maximum_time
                        for _task in self.dtcValidation.dicTasks.values()])]
            _y4 = [sum([_task.average_time
                        for _task in self.dtcValidation.dicTasks.values()])]
        except ValueError:
            _x = [719163]
            _y1 = [0]
            _y2 = [0]
            _y3 = [0]
            _y4 = [0]

        # Add the first status update to be on the first start date with the
        # total project average time.
        self.dtcValidation.dicStatus[min(_x)] = _y2[0]

        # Get a sorted list of unique end dates and then find the total number
        # of hours that should be completed on each unique end date.
        _uniq_end = sorted(list(set([_task.end_date for _task in
                                     self.dtcValidation.dicTasks.values()])))

        for i in range(len(_uniq_end)):
            _sum_time = [0.0, 0.0, 0.0, 0.0]
            for _task in self.dtcValidation.dicTasks.values():
                if _task.end_date == _uniq_end[i]:
                    _sum_time[0] += _task.minimum_time
                    _sum_time[1] += _task.average_time
                    _sum_time[2] += _task.maximum_time
                    _sum_time[3] += _task.average_time * _task.status / 100.0
            _x.append(_uniq_end[i])
            _y1.append(_y1[i] - _sum_time[0])
            _y2.append(_y2[i] - _sum_time[1])
            _y3.append(_y3[i] - _sum_time[2])
            _y4.append(_y4[i] - _sum_time[3])

        # Plot the expected time and expected time limits.
        _widg.load_plot(self.axAxis1, self.pltPlot1, _x, _y3, _y2, _y1,
                        None, _title_=_(u"Total Validation Effort"),
                        _xlab_=_(u"Date"),
                        _ylab_=_(u"Total Time for All Tasks "),
                        _marker_=['r--', 'b-', 'g--'],
                        _type_=[4, 4, 4, 4])

        # Plot the actual burn-down of total hours.
        self.dtcValidation.dicStatus[date.today().toordinal()] = _y4[len(_y4) - 1]

        _x = self.dtcValidation.dicStatus.keys()
        _y4 = self.dtcValidation.dicStatus.values()

        _line = matplotlib.lines.Line2D(_x, _y4, lw=0.0, color='k',
                                        marker='^', markersize=10)
        self.axAxis1.add_line(_line)

        # Plot a vertical line at the scheduled end-date for each task
        # identified as a Reliability Assessment.  Add an annotation box
        # showing the minimum required and goal values for each milestone.
        if len(_assess_dates) > 0:
            for i in range(len(_assess_dates)):
                self.axAxis1.axvline(x=_assess_dates[i], ymin=0,
                                     ymax=1.05 * _y3[0], color='m',
                                     linewidth=2.5, linestyle=':')

            for i in range(len(_targets)):
                self.axAxis1.annotate(str(fmt.format(_targets[i][0])) + "\n" +
                                      str(fmt.format(_targets[i][1])),
                                      xy=(_assess_dates[i], 0.95 * max(_y3)),
                                      xycoords='data',
                                      xytext=(-55, 0),
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
                                          relpos=(0.2, 0.5)))

        # Create the plot legend.
        _text = (_(u"Maximum Expected Time"), _(u"Expected Time"),
                 _(u"Minimum Expected Time"), _(u"Actual Remaining Time"))
        _widg.create_legend(self.axAxis1, _text, fontsize='medium',
                            legframeon=True, location='lower left',
                            legshadow=True)

        self.axAxis1.set_ylim(bottom=0.0, top=1.05 * _y3[0])

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
            self.dtcValidation.add_task(self._model.revision_id)

        elif index == 1:
            self.dtcValidation.delete_task(self._model.validation_id)

        elif index == 2:
            for _task in self.dtcValidation.dicTasks.values():
                _task.calculate()
            self.load(self._model)
            self._load_progress_plot()

        elif index == 3:
            self.dtcValidation.save_all_tasks()
            self.dtcValidation.save_status(self._model.revision_id)

        return False

    def _on_combo_changed(self, combo, index):
        """
        Method to respond to gtk.ComboBox() changed signals.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.ComboBox() that
                          called this method.
        :return: False if successful or True is an error is encountered.
        :rtype: bool
        """

        combo.handler_block(self._lst_handler_id[index])

        if index == 1:
            self._model.task_type = combo.get_active()
            _new_text = _conf.RTK_TASK_TYPE[combo.get_active() - 1]
            self._modulebook.update(index + 2, _new_text)
        elif index == 3:
            self._model.measurement_unit = combo.get_active()
            _new_text = _conf.RTK_MEASUREMENT_UNITS[combo.get_active() - 1]

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

        if index == 0:
            _textbuffer = entry.get_buffer()
            _new_text = _textbuffer.get_text(*_textbuffer.get_bounds())
            self._model.task_description = _new_text
        elif index == 2:
            _new_text = entry.get_text()
            self._model.task_specification = _new_text
        elif index == 4:
            _new_text = float(entry.get_text())
            self._model.min_acceptable = _new_text
        elif index == 5:
            _new_text = float(entry.get_text())
            self._model.mean_acceptable = _new_text
        elif index == 6:
            _new_text = float(entry.get_text())
            self._model.max_acceptable = _new_text
        elif index == 7:
            _new_text = float(entry.get_text())
            self._model.variance_acceptable = _new_text
        elif index == 8:
            _new_text = entry.get_text()
            self._model.start_date = _util.date_to_ordinal(_new_text)
        elif index == 9:
            _new_text = entry.get_text()
            self._model.end_date = _util.date_to_ordinal(_new_text)
        elif index == 11:
            _new_text = float(entry.get_text())
            self._model.minimum_time = _new_text
        elif index == 12:
            _new_text = float(entry.get_text())
            self._model.average_time = _new_text
        elif index == 13:
            _new_text = float(entry.get_text())
            self._model.maximum_time = _new_text
        elif index == 14:
            _new_text = float(entry.get_text())
            self._model.minimum_cost = _new_text
        elif index == 15:
            _new_text = float(entry.get_text())
            self._model.average_cost = _new_text
        elif index == 16:
            _new_text = float(entry.get_text())
            self._model.maximum_cost = _new_text

        self._modulebook.update(index + 2, _new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_value_changed(self, spinbutton, index):
        """
        Method to respond to gtk.SpinButton() changed signals.

        :param gtk.SpinButton spinbutton: the gtk.SpinButton() that called this
                                          method.
        :param int index: the position in the Validation class attribute list
                          associated with the data from the calling
                          spinbutton.
        """

        spinbutton.handler_block(self._lst_handler_id[index])

        if index == 10:
            _new_text = float(spinbutton.get_value())
            self._model.status = _new_text

        self._modulebook.update(index + 2, _new_text)

        spinbutton.handler_unblock(self._lst_handler_id[index])

        return False
