#!/usr/bin/env python
"""
###############################
Survival Package Work Book View
###############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.survival.WorkBook.py is part of The RTK Project
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
try:
    import gobject
except ImportError:
    sys.exit(1)

# Plotting package.
import matplotlib
matplotlib.use('GTK')
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import utilities as _util
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg
#from Assistants import AddSurvival, AddComponents, FilterSurvival, ImportSurvival

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

    :ivar btnCalculate:
    :ivar btnSave:
    :ivar chkGroup:
    :ivar chkParts:
    :ivar cmbAssembly:
    :ivar cmbConfType:
    :ivar cmbConfMethod:
    :ivar cmbDistribution:
    :ivar cmbFitMethod:
    :ivar cmbSource:
    :ivar fraDataset:
    :ivar fraNevadaChart:
    :ivar lblFitMethod:
    :ivar lblConfMethod:
    :ivar tvwDataset:
    :ivar tvwNevadaChart:
    :ivar txtConfidence:
    :ivar txtDescription:
    :ivar txtStartTime:
    :ivar txtEndTime:
    :ivar txtRelPoints:
    :ivar txtStartDate:
    :ivar txtEndDate:
    :ivar btnStartDate:
    :ivar btnEndDate:
    :ivar fraSummary:
    :ivar fraNonParStats:
    :ivar fraNonParEst:
    :ivar fraParStats:
    :ivar hpnAnalysisResults:
    :ivar vpnAnalysisResults:
    :ivar lblCumMTBF:
    :ivar lblMTBFi:
    :ivar lblCumFI:
    :ivar lblFIi:
    :ivar txtNumSuspensions:
    :ivar txtNumFailures:
    :ivar txtMTBF:
    :ivar txtMTBFLL:
    :ivar txtMTBFUL:
    :ivar txtMTBFi:
    :ivar txtMTBFiLL:
    :ivar txtMTBFiUL:
    :ivar txtHazardRate:
    :ivar txtHazardRateLL:
    :ivar txtHazardRateUL:
    :ivar txtHazardRatei:
    :ivar txtHazardRateiLL:
    :ivar txtHazardRateiUL:
    :ivar lblMHBResult:
    :ivar lblZLPResult:
    :ivar lblZLRResult:
    :ivar lblRhoResult:
    :ivar txtMHB:
    :ivar txtChiSq:
    :ivar txtMHBPValue:
    :ivar txtLP:
    :ivar txtZLPNorm:
    :ivar txtZLPPValue:
    :ivar txtLR:
    :ivar txtZLRNorm:
    :ivar txtZLRPValue:
    :ivar txtRho:
    :ivar txtRhoNorm:
    :ivar txtRhoPValue:
    :ivar lblScale:
    :ivar lblShape:
    :ivar lblLocation:
    :ivar lblRowScale:
    :ivar lblRowShape:
    :ivar lblRowLocation:
    :ivar lblColScale:
    :ivar lblColShape:
    :ivar lblColLocation:
    :ivar lblModel:
    :ivar lblAIC:
    :ivar lblBIC:
    :ivar lblMLE:
    :ivar txtScale:
    :ivar txtScaleLL:
    :ivar txtScaleUL:
    :ivar txtShape:
    :ivar txtShapeLL:
    :ivar txtShapeUL:
    :ivar txtLocation:
    :ivar txtLocationLL:
    :ivar txtLocationUL:
    :ivar txtShapeShape:
    :ivar txtShapeScale:
    :ivar txtShapeLocation:
    :ivar txtScaleShape:
    :ivar txtScaleScale:
    :ivar txtScaleLocation:
    :ivar txtLocationShape:
    :ivar txtLocationScale:
    :ivar txtLocationLocation:
    :ivar txtAIC:
    :ivar txtBIC:
    :ivar txtMLE:
    :ivar tvwNonParResults:
    :ivar figFigure1:
    :ivar pltPlot1:
    :ivar axAxis1:
    :ivar figFigure2:
    :ivar pltPlot2:
    :ivar axAxis2:
    :ivar figFigure3:
    :ivar pltPlot3:
    :ivar axAxis3:
    :ivar figFigure4:
    :ivar pltPlot4:
    :ivar axAxis4:
    :ivar vbxPlot1:
    :ivar vbxPlot2:
    :ivar fraResultsByChildAssembly:
    :ivar fraResultsByPart:
    :ivar hpnResultsBreakdown:
    :ivar tvwResultsByChildAssembly:
    :ivar tvwResultsByPart:
    :ivar btnAssign:
    :ivar btnCancel:

    +----------+--------------------------------------------+
    | Position | Widget - Signal                            |
    +==========+============================================+
    |     0    | chkGroup - 'toggled'                       |
    +----------+--------------------------------------------+
    |     1    | chkParts - 'toggled'                       |
    +----------+--------------------------------------------+
    |     2    | cmbAssembly - 'changed'                    |
    +----------+--------------------------------------------+
    |     3    | cmbConfType - 'changed'                    |
    +----------+--------------------------------------------+
    |     4    | cmbConfMethod - 'changed'                  |
    +----------+--------------------------------------------+
    |     5    | cmbDistribution - 'changed'                |
    +----------+--------------------------------------------+
    |     6    | cmbFitMethod - 'changed'                   |
    +----------+--------------------------------------------+
    |     7    | cmbSource - 'changed'                      |
    +----------+--------------------------------------------+
    |     8    | txtConfidence - 'focus_out_event'          |
    +----------+--------------------------------------------+
    |     9    | txtDescription - 'focus_out_event'         |
    +----------+--------------------------------------------+
    |    10    | txtStartTime - 'focus_out_event'           |
    +----------+--------------------------------------------+
    |    11    | txtEndTime - 'focus_out_event'             |
    +----------+--------------------------------------------+
    |    12    | txtRelPoints - 'focus_out_event'           |
    +----------+--------------------------------------------+
    |    13    | txtStartDate - 'focus_out_event'           |
    +----------+--------------------------------------------+
    |    14    | txtEndDate - 'focus_out_event'             |
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
        self._lst_status = [_(u"Event"), _(u"Right Censored"),
                            _(u"Left Censored"), _(u"Interval Censored")]

        # Initialize private scalar attributes.
        self._workview = workview
        self._modulebook = modulebook
        self._model = None
        self._record_id = None

        # Initialize public scalar attributes.
        # Create the Analyses Input page widgets.
        self.btnAddRecord = _widg.make_button(width=35, image='add')
        self.btnRemoveRecord = _widg.make_button(width=35, image='remove')
        self.btnCalculate = _widg.make_button(width=35, image='calculate')
        self.btnSaveRecord = _widg.make_button(width=35, image='save')

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

        self.fraDataset = _widg.make_frame(label=_(u"Dataset Records"))
        self.fraNevadaChart = _widg.make_frame(label=_(u"Nevada Chart "
                                                       u"Records"))

        self.lblFitMethod = _widg.make_label(_(u"Fit Method:"), 150, 25)
        self.lblConfMethod = _widg.make_label(_(u"Confidence Method:"),
                                              150, 25)

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

        # Create the Analyses Results page widgets.
        self.fraSummary = _widg.make_frame(label=_(u"Summary of Results"))
        self.fraNonParStats = _widg.make_frame(label=_(u"Non-Parametric "
                                                       u"Statistics"))
        self.fraNonParEst = _widg.make_frame(label=_(u"Parameter Estimates"))
        self.fraParStats = _widg.make_frame(label=_(u"Parameter Estimates"))

        self.hpnAnalysisResults = gtk.HPaned()

        self.vpnAnalysisResults = gtk.VPaned()

        # Upper left quadrant widgets.
        self.lblCumMTBF = _widg.make_label(_(u"Cumulative MTBF:"), width=-1)
        self.lblMTBFi = _widg.make_label(_(u"Instantaneous MTBF:"), width=-1)
        self.lblCumFI = _widg.make_label(_(u"Cumulative Failure Intensity:"),
                                         width=-1)
        self.lblFIi = _widg.make_label(_(u"Instantaneous Failure Intensity:"),
                                       width=-1)

        self.txtNumSuspensions = _widg.make_entry(width=50, editable=False)
        self.txtNumFailures = _widg.make_entry(width=50, editable=False)

        self.txtMTBF = _widg.make_entry(width=100, editable=False)
        self.txtMTBFLL = _widg.make_entry(width=100, editable=False)
        self.txtMTBFUL = _widg.make_entry(width=100, editable=False)
        self.txtMTBFi = _widg.make_entry(width=100, editable=False)
        self.txtMTBFiLL = _widg.make_entry(width=100, editable=False)
        self.txtMTBFiUL = _widg.make_entry(width=100, editable=False)
        self.txtHazardRate = _widg.make_entry(width=100, editable=False)
        self.txtHazardRateLL = _widg.make_entry(width=100, editable=False)
        self.txtHazardRateUL = _widg.make_entry(width=100, editable=False)
        self.txtHazardRatei = _widg.make_entry(width=100, editable=False)
        self.txtHazardRateiLL = _widg.make_entry(width=100, editable=False)
        self.txtHazardRateiUL = _widg.make_entry(width=100, editable=False)

        # Lower left quadrant non-parametric widgets.
        self.lblMHBResult = _widg.make_label(_(u""), width=150)
        self.lblZLPResult = _widg.make_label(_(u""), width=150)
        self.lblZLRResult = _widg.make_label(_(u""), width=150)
        self.lblRhoResult = _widg.make_label(_(u""), width=150)

        self.txtMHB = _widg.make_entry(width=100)
        self.txtChiSq = _widg.make_entry(width=100)
        self.txtMHBPValue = _widg.make_entry(width=100)
        self.txtLP = _widg.make_entry(width=100)
        self.txtZLPNorm = _widg.make_entry(width=100)
        self.txtZLPPValue = _widg.make_entry(width=100)
        self.txtLR = _widg.make_entry(width=100)
        self.txtZLRNorm = _widg.make_entry(width=100)
        self.txtZLRPValue = _widg.make_entry(width=100)
        self.txtRho = _widg.make_entry(width=100)
        self.txtRhoNorm = _widg.make_entry(width=100)
        self.txtRhoPValue = _widg.make_entry(width=100)

        # Lower left quadrant parametric widgets.
        self.lblScale = _widg.make_label(_(u"Scale"), width=150)
        self.lblShape = _widg.make_label(_(u"Shape"), width=150)
        self.lblLocation = _widg.make_label(_(u"Location"), width=150)
        self.lblRowScale = _widg.make_label(_(u"Scale"), width=150)
        self.lblRowShape = _widg.make_label(_(u"Shape"), width=150)
        self.lblRowLocation = _widg.make_label(_(u"Location"), width=150)
        self.lblColScale = _widg.make_label(_(u"Scale"), width=150)
        self.lblColShape = _widg.make_label(_(u"Shape"), width=150)
        self.lblColLocation = _widg.make_label(_(u"Location"), width=150)
        self.lblModel = _widg.make_label("", width=350)
        self.lblAIC = _widg.make_label("AIC", width=150)
        self.lblBIC = _widg.make_label("BIC", width=150)
        self.lblMLE = _widg.make_label("MLE", width=150)

        self.txtScale = _widg.make_entry(width=100, editable=False)
        self.txtScaleLL = _widg.make_entry(width=100, editable=False)
        self.txtScaleUL = _widg.make_entry(width=100, editable=False)
        self.txtShape = _widg.make_entry(width=100, editable=False)
        self.txtShapeLL = _widg.make_entry(width=100, editable=False)
        self.txtShapeUL = _widg.make_entry(width=100, editable=False)
        self.txtLocation = _widg.make_entry(width=100, editable=False)
        self.txtLocationLL = _widg.make_entry(width=100, editable=False)
        self.txtLocationUL = _widg.make_entry(width=100, editable=False)

        self.txtShapeShape = _widg.make_entry(width=100, editable=False)
        self.txtShapeScale = _widg.make_entry(width=100, editable=False)
        self.txtShapeLocation = _widg.make_entry(width=100, editable=False)
        self.txtScaleShape = _widg.make_entry(width=100, editable=False)
        self.txtScaleScale = _widg.make_entry(width=100, editable=False)
        self.txtScaleLocation = _widg.make_entry(width=100, editable=False)
        self.txtLocationShape = _widg.make_entry(width=100, editable=False)
        self.txtLocationScale = _widg.make_entry(width=100, editable=False)
        self.txtLocationLocation = _widg.make_entry(width=100, editable=False)
        self.txtAIC = _widg.make_entry(width=100, editable=False)
        self.txtBIC = _widg.make_entry(width=100, editable=False)
        self.txtMLE = _widg.make_entry(width=100, editable=False)

        self.tvwNonParResults = gtk.TreeView()

        # Create the Plot page widgets.
        _height = 100 #(self._app.winWorkBook.height * 0.01) / 2.0
        _width = 200 #(self._app.winWorkBook.width * 0.01) / 2.0
        self.figFigure1 = Figure(figsize=(_width, _height))
        self.pltPlot1 = FigureCanvas(self.figFigure1)
        self.pltPlot1.mpl_connect('button_press_event', _widg.expand_plot)
        self.axAxis1 = self.figFigure1.add_subplot(111)
        self.figFigure2 = Figure(figsize=(_width, _height))
        self.pltPlot2 = FigureCanvas(self.figFigure2)
        self.pltPlot2.mpl_connect('button_press_event', _widg.expand_plot)
        self.axAxis2 = self.figFigure2.add_subplot(111)
        self.figFigure3 = Figure(figsize=(_width, _height))
        self.pltPlot3 = FigureCanvas(self.figFigure3)
        self.pltPlot3.mpl_connect('button_press_event', _widg.expand_plot)
        self.axAxis3 = self.figFigure3.add_subplot(111)
        self.figFigure4 = Figure(figsize=(_width, _height))
        self.pltPlot4 = FigureCanvas(self.figFigure4)
        self.pltPlot4.mpl_connect('button_press_event', _widg.expand_plot)
        self.axAxis4 = self.figFigure4.add_subplot(111)
        self.vbxPlot1 = gtk.VBox()
        self.vbxPlot2 = gtk.VBox()

        # Create the analysis results breakdown page widgets.
        self.fraResultsByChildAssembly = _widg.make_frame(label=_(u"Summary "
                                                                  u"of "
                                                                  u"Results "
                                                                  u"By Child "
                                                                  u"Assembly"))
        self.fraResultsByPart = _widg.make_frame(label=_(u"Summary of Results "
                                                         u"By Part"))

        self.hpnResultsBreakdown = gtk.HPaned()

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
        _button.set_name('Assign')
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
        _button.set_name('Assign')
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
        _button.set_name('Assign')
        _button.connect('clicked', self._on_button_clicked, 6)
        _button.set_tooltip_text(_(u"Consolidates the records in the selected "
                                   u"data set."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Calculate button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        _button.set_icon_widget(_image)
        _button.set_name('Calculate')
        _button.connect('clicked', self._on_button_clicked, 7)
        _button.set_tooltip_text(_(u"Analyzes the selected data set."))
        _toolbar.insert(_button, _position)
        _position += 1

        # Save button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.set_name('Save')
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
        _button.set_name('Assign')
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
        self._create_analyses_results_page(_notebook)
        self._create_plot_page(_notebook)
        self._create_results_breakdown_page(_notebook)

        return _notebook

    def _create_analyses_input_page(self, notebook):
        """
        Method to create the Dataset class gtk.Notebook() page for
        displaying assessment inputs for the selected data set.

        :param rtk.Dataset self: the current instance of a Dataset class.
        :param gtk.Notebook notebook: the Dataset class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
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

        #self.tvwDataset.set_rubber_banding(True)
        #self.tvwDataset.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwDataset)

        _hbox2.pack_start(_bbox, False, False)
        _hbox2.pack_end(_scrollwindow)

        self.fraDataset.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        self.fraDataset.add(_hbox2)

        _fixed = gtk.Fixed()
        #_label = _widg.make_label(_(u"Select dataset:"))
        #_fixed.put(_label, 10, 5)
        #_fixed.put(self.cmbDatasets, 135, 5)
        #_fixed.put(self.btnAddDataset, 205, 5)
        #_fixed.put(self.btnRemoveDataset, 240, 5)

        _frame = gtk.Frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_fixed)

        _vbox.pack_start(_frame, False, False)
        _vbox.pack_end(self.fraDataset)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwNevadaChart)

        self.fraNevadaChart.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        self.fraNevadaChart.add(_scrollwindow)

        _hbox.pack1(_vbox, True, True)

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
        _results = [["MLE"], [_(u"Rank Regression")]]
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

        _labels = [_(u"Event Date"), _(u"Affected\nHardware"), _(u"Left"),
                   _(u"Right"), _(u"Interarrival\nTime"), _(u"Quantity")]
        for i in range(len(_labels)):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 1)
            _cell.set_property('background', 'white')
            _cell.connect('edited', self._on_cellrenderer_edited, i+1, _model)
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_labels[i])
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i+1)
            _column.set_sort_column_id(i+1)
            self.tvwDataset.append_column(_column)

        _cell = gtk.CellRendererCombo()
        _cellmodel = gtk.ListStore(gobject.TYPE_STRING)
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
                   _(u"Distribution:"), _(""), _(u"Confidence:"),
                   _(u"Confidence Type:"), _("")]
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
        _fixed.put(self.lblFitMethod, 5, _y_pos1[4])
        _fixed.put(self.cmbFitMethod, _x_pos1, _y_pos1[4])
        _fixed.put(self.txtConfidence, _x_pos1, _y_pos1[5])
        _fixed.put(self.cmbConfType, _x_pos1, _y_pos1[6])
        _fixed.put(self.lblConfMethod, 5, _y_pos1[7])
        _fixed.put(self.cmbConfMethod, _x_pos1, _y_pos1[7])

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

    def _create_analyses_results_page(self, notebook):
        """
        Method to create the Dataset class gtk.Notebook() page for
        displaying assessment results for the selected data set.

        :param gtk.Notebook notebook: the Dataset class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.hpnAnalysisResults.pack1(self.vpnAnalysisResults)

        self.fraSummary.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        self.vpnAnalysisResults.pack1(self.fraSummary)

        self.fraNonParStats.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        self.vpnAnalysisResults.pack2(self.fraNonParStats)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwNonParResults)
        self.fraNonParEst.add(_scrollwindow)
        self.fraNonParEst.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        self.hpnAnalysisResults.pack2(self.fraNonParEst)

        self.fraParStats.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

        self.lblScale.set_use_markup(True)
        self.lblShape.set_use_markup(True)
        self.lblLocation.set_use_markup(True)
        self.lblMHBResult.set_use_markup(True)
        self.lblZLPResult.set_use_markup(True)
        self.lblZLRResult.set_use_markup(True)
        self.lblRhoResult.set_use_markup(True)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display analysis results.           #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        self.txtMHB.set_tooltip_markup(_(u"Displays the value of the "
                                         u"MIL-HDBK test for trend."))
        self.txtChiSq.set_tooltip_markup(_(u"Displays the chi square "
                                           u"critical value for the "
                                           u"MIL-HDBK test for trend."))
        self.txtMHBPValue.set_tooltip_markup(_(u"Displays the p-value for "
                                               u"the MIL-HDBK test for "
                                               u"trend."))
        self.txtLP.set_tooltip_markup(_(u"Displays the value of the "
                                        u"LaPlace test for trend."))
        self.txtZLPNorm.set_tooltip_markup(_(u"Displays the standard "
                                             u"normal critical value for "
                                             u"the LaPlace test for "
                                             u"trend."))
        self.txtZLPPValue.set_tooltip_markup(_(u"Displays the p-value for "
                                               u"the Laplace test for "
                                               u"trend."))
        self.txtLR.set_tooltip_markup(_(u"Displays the value of the "
                                        u"Lewis-Robinson test for trend."))
        self.txtZLRNorm.set_tooltip_markup(_(u"Displays the standard "
                                             u"normal critical value for "
                                             u"the Lewis-Robinson test "
                                             u"for trend."))
        self.txtZLRPValue.set_tooltip_markup(_(u"Displays the p-value for "
                                               u"the Lewis-Robinson test "
                                               u"for trend."))
        self.txtRho.set_tooltip_markup(_(u"Displays the value of the lag "
                                         u"1 sample serial correlation "
                                         u"coefficient."))
        self.txtRhoNorm.set_tooltip_markup(_(u"Displays the standard "
                                             u"normal critical value for "
                                             u"the lag 1 sample serial "
                                             u"correlation coefficient."))
        self.txtRhoPValue.set_tooltip_markup(_(u"Displays the p-value for "
                                               u"the lag 1 sample serial "
                                               u"correlation "
                                               u"coefficient."))
        self.txtScale.set_tooltip_markup(_(u"Displays the point estimate "
                                           u"of the scale parameter."))
        self.txtScaleLL.set_tooltip_markup(_(u"Displays the lower "
                                             u"<span>\u03B1</span>% bound "
                                             u"on the scale parameter."))
        self.txtScaleUL.set_tooltip_markup(_(u"Displays the upper "
                                             u"<span>\u03B1</span>% bound "
                                             u"on the scale parameter."))
        self.txtShape.set_tooltip_markup(_(u"Displays the point estimate "
                                           u"of the shape parameter."))
        self.txtShapeLL.set_tooltip_markup(_(u"Displays the lower "
                                             u"<span>\u03B1</span>% bound "
                                             u"on the shape parameter."))
        self.txtShapeUL.set_tooltip_markup(_(u"Displays the upper "
                                             u"<span>\u03B1</span>% bound "
                                             u"on the shape parameter."))
        self.txtLocation.set_tooltip_markup(_(u"Displays the point "
                                              u"estimate of the location "
                                              u"parameter."))
        self.txtLocationLL.set_tooltip_markup(_(u"Displays the lower "
                                                u"<span>\u03B1</span>% "
                                                u"bound on the location "
                                                u"parameter."))
        self.txtLocationUL.set_tooltip_markup(_(u"Displays the upper "
                                                u"<span>\u03B1</span>% "
                                                u"bound on the location "
                                                u"parameter."))
        self.txtShapeShape.set_tooltip_markup(_(u"Displays the variance "
                                                u"of the shape "
                                                u"parameter."))
        self.txtShapeScale.set_tooltip_markup(_(u"Displays the covariance "
                                                u"of the shape and scale "
                                                u"parameters."))
        self.txtShapeLocation.set_tooltip_markup(_(u"Displays the "
                                                   u"covariance of the "
                                                   u"shape and location"
                                                   u" parameters."))
        self.txtScaleShape.set_tooltip_markup(_(u"Displays the covariance "
                                                u"of the scale and shape "
                                                u"parameters."))
        self.txtScaleScale.set_tooltip_markup(_(u"Displays the variance "
                                                u"of the scale "
                                                u"parameter."))
        self.txtScaleLocation.set_tooltip_markup(_(u"Displays the "
                                                   u"covariance of the "
                                                   u"scale and location "
                                                   u"parameters."))
        self.txtLocationShape.set_tooltip_markup(_(u"Displays the "
                                                   u"covariance of the "
                                                   u"location and shape "
                                                   u"parameters."))
        self.txtLocationScale.set_tooltip_markup(_(u"Displays the "
                                                   u"covariance of the "
                                                   u"location and scale "
                                                   u"parameters."))
        self.txtLocationLocation.set_tooltip_markup(_(u"Displays the "
                                                      u"variance of the "
                                                      u"location "
                                                      u"parameter."))
        self.txtAIC.set_tooltip_markup(_(u"Displays the value of Aikike's "
                                         u"information criterion."))
        self.txtBIC.set_tooltip_markup(_(u"Displays the value of Bayes' "
                                         u"information criterion."))
        self.txtMLE.set_tooltip_markup(_(u"Displays the likelihood "
                                         u"value."))
        self.txtNumSuspensions.set_tooltip_markup(_(u"Displays the number "
                                                    u"of suspensions in "
                                                    u"the data set."))
        self.txtNumFailures.set_tooltip_markup(_(u"Displays the number of "
                                                 u"failures in the dat "
                                                 u"set."))
        self.txtMTBF.set_tooltip_markup(_(u"Displays the point estimate "
                                          u"of the MTBF."))
        self.txtMTBFLL.set_tooltip_markup(_(u"Displays the lower "
                                            u"<span>\u03B1</span>% bound "
                                            u"on the MTBF."))
        self.txtMTBFUL.set_tooltip_markup(_(u"Displays the upper "
                                            u"<span>\u03B1</span>% bound "
                                            u"on the MTBF."))
        self.txtHazardRate.set_tooltip_markup(_(u"Displays the point "
                                                u"estimate of the hazard "
                                                u"rate."))
        self.txtHazardRateLL.set_tooltip_markup(_(u"Displays the lower "
                                                  u"<span>\u03B1</span>% "
                                                  u"bound on the hazard "
                                                  u"rate."))
        self.txtHazardRateUL.set_tooltip_markup(_(u"Displays the upper "
                                                  u"<span>\u03B1</span>% "
                                                  u"bound on the hazard "
                                                  u"rate."))
        self.txtMTBFi.set_tooltip_markup(_(u"Displays the point estimate "
                                           u"of the instantaneous MTBF."))
        self.txtMTBFiLL.set_tooltip_markup(_(u"Displays the lower "
                                             u"<span>\u03B1</span>% bound "
                                             u"on the instantaneous "
                                             u"MTBF."))
        self.txtMTBFiUL.set_tooltip_markup(_(u"Displays the upper "
                                             u"<span>\u03B1</span>% bound "
                                             u"on the instantaneous "
                                             u"MTBF."))
        self.txtHazardRatei.set_tooltip_markup(_(u"Displays the point "
                                                 u"estimate the "
                                                 u"instantaneous failure "
                                                 u"intensity."))
        self.txtHazardRateiLL.set_tooltip_markup(_(u"Displays the lower "
                                                   u"<span>\u03B1</span>% "
                                                   u"bound on the "
                                                   u"instantaneous "
                                                   u"failure intensity."))
        self.txtHazardRateiUL.set_tooltip_markup(_(u"Displays the upper "
                                                   u"<span>\u03B1</span>% "
                                                   u"bound on the "
                                                   u"instantaneous "
                                                   u"failure intensity."))

        # Build the summary of results container.  The summary is used for
        # all analyses.
        _fixed = gtk.Fixed()
        _labels = [_(u"Number of Suspensions:"), _(u"Number of Failures:"),
                   _(u"LCL"), _(u"Estimate"), _(u"UCL")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels[0:2], _fixed, 5, 5)
        _x_pos = max(_x_pos, self.lblCumMTBF.size_request()[0])
        _x_pos = max(_x_pos, self.lblMTBFi.size_request()[0])
        _x_pos = max(_x_pos, self.lblCumFI.size_request()[0])
        _x_pos = max(_x_pos, self.lblFIi.size_request()[0])
        _x_pos += 25

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)
        self.fraSummary.add(_scrollwindow)

        _fixed.put(self.txtNumSuspensions, _x_pos, _y_pos[0])
        _fixed.put(self.txtNumFailures, _x_pos, _y_pos[1])

        _label = _widg.make_label(_labels[2], width=150)
        _fixed.put(_label, _x_pos, _y_pos[1] + 30)
        _label = _widg.make_label(_labels[3], width=150)
        _fixed.put(_label, _x_pos + 105, _y_pos[1] + 30)
        _label = _widg.make_label(_labels[4], width=150)
        _fixed.put(_label, _x_pos + 210, _y_pos[1] + 30)

        _fixed.put(self.lblCumMTBF, 5, _y_pos[1] + 60)
        _fixed.put(self.txtMTBFLL, _x_pos, _y_pos[1] + 60)
        _fixed.put(self.txtMTBF, _x_pos + 105, _y_pos[1] + 60)
        _fixed.put(self.txtMTBFUL, _x_pos + 210, _y_pos[1] + 60)
        _fixed.put(self.lblModel, _x_pos + 315, _y_pos[1] + 60)

        _fixed.put(self.lblMTBFi, 5, _y_pos[1] + 90)
        _fixed.put(self.txtMTBFiLL, _x_pos, _y_pos[1] + 90)
        _fixed.put(self.txtMTBFi, _x_pos + 105, _y_pos[1] + 90)
        _fixed.put(self.txtMTBFiUL, _x_pos + 210, _y_pos[1] + 90)

        _fixed.put(self.lblCumFI, 5, _y_pos[1] + 120)
        _fixed.put(self.txtHazardRateUL, _x_pos, _y_pos[1] + 120)
        _fixed.put(self.txtHazardRate, _x_pos + 105, _y_pos[1] + 120)
        _fixed.put(self.txtHazardRateLL, _x_pos + 210, _y_pos[1] + 120)

        _fixed.put(self.lblFIi, 5, _y_pos[1] + 150)
        _fixed.put(self.txtHazardRateiLL, _x_pos, _y_pos[1] + 150)
        _fixed.put(self.txtHazardRatei, _x_pos + 105, _y_pos[1] + 150)
        _fixed.put(self.txtHazardRateiUL, _x_pos + 210, _y_pos[1] + 150)

        # Build the non-parametric goodness of fit statistics container.
        _fixed = gtk.Fixed()
        _labels = [_(u"MIL\nHandbook"), _(u"Laplace"),
                   _(u"Lewis\nRobinson"),
                   _(u"Serial\nCorrelation\nCoefficient")]
        (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed, 5, 30)
        _x_pos += 20

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)
        self.fraNonParStats.add(_scrollwindow)

        _label = _widg.make_label(_(u"Test Statistic"), width=150)
        _fixed.put(_label, _x_pos + 5, 5)
        _fixed.put(self.txtMHB, _x_pos + 5, _y_pos[0])
        _fixed.put(self.txtLP, _x_pos + 5, _y_pos[1])
        _fixed.put(self.txtLR, _x_pos + 5, _y_pos[2])
        _fixed.put(self.txtRho, _x_pos + 5, _y_pos[3])

        _label = _widg.make_label(_(u"Critical Value"), width=150)
        _fixed.put(_label, _x_pos + 105, 5)
        _fixed.put(self.txtChiSq, _x_pos + 105, _y_pos[0])
        _fixed.put(self.txtZLPNorm, _x_pos + 105, _y_pos[1])
        _fixed.put(self.txtZLRNorm, _x_pos + 105, _y_pos[2])
        _fixed.put(self.txtRhoNorm, _x_pos + 105, _y_pos[3])

        _label = _widg.make_label(_(u"p-Value"), width=150)
        _fixed.put(_label, _x_pos + 210, 5)
        _fixed.put(self.txtMHBPValue, _x_pos + 210, _y_pos[0])
        _fixed.put(self.txtZLPPValue, _x_pos + 210, _y_pos[1])
        _fixed.put(self.txtZLRPValue, _x_pos + 210, _y_pos[2])
        _fixed.put(self.txtRhoPValue, _x_pos + 210, _y_pos[3])

        _fixed.put(self.lblMHBResult, _x_pos + 315, _y_pos[0])
        _fixed.put(self.lblZLPResult, _x_pos + 315, _y_pos[1])
        _fixed.put(self.lblZLRResult, _x_pos + 315, _y_pos[2])
        _fixed.put(self.lblRhoResult, _x_pos + 315, _y_pos[3])

        # Build the parametric statistics container.
        _fixed = gtk.Fixed()
        _x_pos = max(self.lblScale.size_request()[0],
                     self.lblShape.size_request()[0])
        _x_pos = max(_x_pos, self.lblLocation.size_request()[0])
        _x_pos = max(_x_pos, self.lblRowScale.size_request()[0])
        _x_pos = max(_x_pos, self.lblRowShape.size_request()[0])
        _x_pos = max(_x_pos, self.lblRowLocation.size_request()[0])
        _x_pos += 20

        _y_inc = max(self.lblScale.size_request()[1], 25) + 5
        _y_pos = [_y_inc]
        _y_inc += max(self.lblShape.size_request()[1], 25) + 5
        _y_pos.append(_y_inc)
        _y_inc += max(self.lblLocation.size_request()[1], 25) + 5
        _y_pos.append(_y_inc)
        _y_inc += max(self.lblRowScale.size_request()[1], 55) + 5
        _y_pos.append(_y_inc)
        _y_inc += max(self.lblRowShape.size_request()[1], 25) + 5
        _y_pos.append(_y_inc)
        _y_inc += max(self.lblRowLocation.size_request()[1], 25) + 5
        _y_pos.append(_y_inc)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(_fixed)
        self.fraParStats.add(_scrollwindow)

        # Place the parameter estimates widgets.
        _label = _widg.make_label(_(u"LCL"), width=150)
        _fixed.put(_label, _x_pos, 5)
        _label = _widg.make_label(_(u"Estimate"), width=150)
        _fixed.put(_label, _x_pos + 105, 5)
        _label = _widg.make_label(_(u"UCL"), width=150)
        _fixed.put(_label, _x_pos + 210, 5)

        _fixed.put(self.lblScale, 5, _y_pos[0])
        _fixed.put(self.txtScaleLL, _x_pos, _y_pos[0])
        _fixed.put(self.txtScale, _x_pos + 105, _y_pos[0])
        _fixed.put(self.txtScaleUL, _x_pos + 210, _y_pos[0])

        _fixed.put(self.lblShape, 5, _y_pos[1])
        _fixed.put(self.txtShapeLL, _x_pos, _y_pos[1])
        _fixed.put(self.txtShape, _x_pos + 105, _y_pos[1])
        _fixed.put(self.txtShapeUL, _x_pos + 210, _y_pos[1])

        _fixed.put(self.lblLocation, 5, _y_pos[2])
        _fixed.put(self.txtLocationLL, _x_pos, _y_pos[2])
        _fixed.put(self.txtLocation, _x_pos + 105, _y_pos[2])
        _fixed.put(self.txtLocationUL, _x_pos + 210, _y_pos[2])

        # Place the variance-covariance matrix.
        _fixed.put(self.lblColScale, _x_pos, _y_pos[2] + 30)
        _fixed.put(self.lblColShape, _x_pos + 105, _y_pos[2] + 30)
        _fixed.put(self.lblColLocation, _x_pos + 210, _y_pos[2] + 30)

        _fixed.put(self.lblRowScale, 5, _y_pos[3])
        _fixed.put(self.txtScaleScale, _x_pos, _y_pos[3])
        _fixed.put(self.txtScaleShape, _x_pos + 105, _y_pos[3])
        _fixed.put(self.txtScaleLocation, _x_pos + 210, _y_pos[3])

        _fixed.put(self.lblRowShape, 5, _y_pos[4])
        _fixed.put(self.txtShapeScale, _x_pos, _y_pos[4])
        _fixed.put(self.txtShapeShape, _x_pos + 105, _y_pos[4])
        _fixed.put(self.txtShapeLocation, _x_pos + 210, _y_pos[4])

        _fixed.put(self.lblRowLocation, 5, _y_pos[5])
        _fixed.put(self.txtLocationScale, _x_pos, _y_pos[5])
        _fixed.put(self.txtLocationShape, _x_pos + 105, _y_pos[5])
        _fixed.put(self.txtLocationLocation, _x_pos + 210, _y_pos[5])

        # Place the parametric goodness of fit statistics.
        _fixed.put(self.lblAIC, 5, _y_pos[5] + 30)
        _fixed.put(self.lblBIC, 5, _y_pos[5] + 60)
        _fixed.put(self.lblMLE, 5, _y_pos[5] + 90)
        _fixed.put(self.txtAIC, _x_pos, _y_pos[5] + 30)
        _fixed.put(self.txtBIC, _x_pos, _y_pos[5] + 60)
        _fixed.put(self.txtMLE, _x_pos, _y_pos[5] + 90)

        _fixed.show_all()

        self.lblModel.hide()

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Analysis\nResults") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays analysis results for the "
                                  u"selected dataset."))
        notebook.insert_page(self.hpnAnalysisResults, tab_label=_label,
                             position=-1)

        return False

    def _create_plot_page(self, notebook):
        """
        Method to create the Dataset class gtk.Notebook() page for
        displaying plots for the selected data set.

        :param gtk.Notebook notebook: the Dataset class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        _frame = _widg.make_frame(label=_(u"Survival Analysis Plots"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_hbox)
        _frame.show_all()

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display general information.        #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox.pack_start(self.vbxPlot1)

        self.vbxPlot1.pack_start(self.pltPlot1)
        self.vbxPlot1.pack_start(self.pltPlot3)

        _hbox.pack_start(self.vbxPlot2)

        self.vbxPlot2.pack_start(self.pltPlot2)
        self.vbxPlot2.pack_start(self.pltPlot4)

        # Insert the page.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>Analysis\nPlots</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays survival analyses plots."))
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_results_breakdown_page(self, notebook):
        """
        Method to create the Dataset class gtk.Notebook() page for
        displaying results decomposed to child assemblies and/or components
        for the selected data set.

        :param gtk.Notebook notebook: the Dataset class gtk.Notebook() widget.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hpaned = gtk.HPaned()

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResultsByChildAssembly)

        self.fraResultsByChildAssembly.add(_scrollwindow)

        _hpaned.pack1(self.fraResultsByChildAssembly, True, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwResultsByPart)

        self.fraResultsByPart.add(_scrollwindow)

        _hpaned.pack2(self.fraResultsByPart, True, True)

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

        _labels = [_(u"Hardware\nItem"), _(u"Number of\nFailures"), _(u""),
                   _(u"MTBF\nLower Bound"), _(u"MTBF"),
                   _(u"MTBF\nUpper Bound"),
                   _(u"Failure Intensity\nLower Bound"),
                   _(u"Failure\nIntensity"),
                   _(u"Failure Intensity\nUpper Bound")]
        for i in range(len(_labels)):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_labels[i])
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i, background=9)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(i)
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

        _labels = [_(u"Part\nNumber"), _(u"Number of\nFailures"), _(u""),
                   _(u"MTBF\nLower Bound"), _(u"MTBF"),
                   _(u"MTBF\nUpper Bound"),
                   _(u"Failure Intensity\nLower Bound"),
                   _(u"Failure\nIntensity"),
                   _(u"Failure Intensity\nUpper Bound")]
        for i in range(len(_labels)):
            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _column = gtk.TreeViewColumn()
            _label = _widg.make_column_heading(_labels[i])
            _column.set_widget(_label)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=i, background=8)
            _column.set_clickable(True)
            _column.set_sort_column_id(i)
            self.tvwResultsByPart.append_column(_column)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Results\nBreakdowns") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays analysis results for the "
                                  u"selected data set broken down by "
                                  u"child assembly and part number."))
        notebook.insert_page(_hpaned, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Survival class gtk.Notebook().

        :param model: the :py:class:`rtk.survival.Survival.Model` whose
                      attributes will be loaded into the display widgets.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._model = model

        self._load_analysis_inputs_page()
        self._load_dataset_records()
        self._load_analysis_results_page()

        self._notebook.set_current_page(0)

        return False

    def _load_analysis_inputs_page(self):
        """
        Method to load the gtk.Widgets() on the analysis inputs page.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        _index = 0
        _model = self.cmbAssembly.get_model()
        _row = _model.get_iter_root()
        while _row is not None:
            if _model.get_value(_row, 1) == str(self._model.assembly_id):
                break
            else:
                _row = _model.iter_next(_row)
                _index += 1

        self.cmbAssembly.set_active(_index)
        if _index in [1, 2, 3, 4]:
            self.chkGroup.show()
            self.chkParts.show()
        else:
            self.chkGroup.hide()
            self.chkParts.hide()

        self.cmbSource.set_active(self._model.source)
        self.cmbDistribution.set_active(self._model.distribution_id)
        self.cmbConfType.set_active(self._model.confidence_type)
        self.cmbConfMethod.set_active(self._model.confidence_method)
        self.cmbFitMethod.set_active(self._model.fit_method)

        self.txtDescription.set_text(self._model.description)
        self.txtConfidence.set_text(str(self._model.confidence))
        self.txtStartTime.set_text(str(self._model.start_time))
        self.txtEndTime.set_text(str(self._model.end_time))
        self.txtRelPoints.set_text(str(self._model.n_rel_points))

        _start_date = _util.ordinal_to_date(self._model.start_date)
        _end_date = _util.ordinal_to_date(self._model.end_date)
        self.txtStartDate.set_text(str(_start_date))
        self.txtEndDate.set_text(str(_end_date))

        #if self._nevada_chart != 0:
        #    self._load_nevada_chart()

        return False

    def _load_analysis_results_page(self):
        """
        Method to load the gtk.Widgets() on the analysis results page.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Clear the page.
        for _child in self.hpnAnalysisResults.get_children():
            self.hpnAnalysisResults.remove(_child)
        for _child in self.vpnAnalysisResults.get_children():
            self.vpnAnalysisResults.remove(_child)

        # Hide widgets that are not used for all analyses.  These will be
        # shown as appropriate for the analysis results being loaded.
        self.lblMTBFi.hide()
        self.lblFIi.hide()
        self.lblRhoResult.hide()
        self.txtMTBFiLL.hide()
        self.txtMTBFi.hide()
        self.txtMTBFiUL.hide()
        self.txtHazardRateiLL.hide()
        self.txtHazardRatei.hide()
        self.txtHazardRateiUL.hide()
        self.lblModel.hide()

        # Hide the parameter estimate widgets.
        self.lblLocation.hide()
        self.txtLocation.hide()
        self.txtLocationLL.hide()
        self.txtLocationUL.hide()

        # Hide the variance-covariance matrix widgets.
        self.lblRowScale.hide()
        self.lblRowShape.hide()
        self.lblRowLocation.hide()
        self.lblColScale.hide()
        self.lblColShape.hide()
        self.lblColLocation.hide()
        self.txtScaleScale.hide()
        self.txtShapeShape.hide()
        self.txtLocationLocation.hide()
        self.txtShapeScale.hide()
        self.txtScaleShape.hide()
        self.txtScaleLocation.hide()
        self.txtLocationScale.hide()
        self.txtShapeLocation.hide()
        self.txtLocationShape.hide()

        # Hide the non-parametric GoF statistic widgets.
        self.lblRhoResult.hide()
        self.txtRho.hide()
        self.txtRhoNorm.hide()
        self.txtRhoPValue.hide()

        # Hide the parametric GoF statistic widgets.
        self.lblAIC.hide()
        self.lblBIC.hide()
        self.lblMLE.hide()
        self.txtAIC.hide()
        self.txtBIC.hide()
        self.txtMLE.hide()

        self.hpnAnalysisResults.pack1(self.vpnAnalysisResults, True, True)
        self.vpnAnalysisResults.pack1(self.fraSummary, True, True)

        # Update summary information.
        self.txtNumSuspensions.set_text(str(self._model.n_suspensions))
        self.txtNumFailures.set_text(str(self._model.n_failures))

        # Update mean cumulative function information.
        if self._model.distribution_id == 1:
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)
            self.vpnAnalysisResults.pack2(self.fraNonParStats, True, True)

            self.txtMHB.set_text(str(fmt.format(self._model.mhb)))
            self.txtLP.set_text(str(fmt.format(self._model.lp)))
            self.txtLR.set_text(str(fmt.format(self._model.lr)))

            self.lblCumMTBF.set_markup(_(u"<span>MTBF:</span>"))
            self.lblCumFI.set_markup(_(u"<span>Failure Intensity:</span>"))

            # Show widgets specific to MCF.
            self.lblRhoResult.show()
            self.txtRho.show()
            self.txtRhoNorm.show()
            self.txtRhoPValue.show()

        # Update Kaplan-Meier analysis information.
        elif self._model.distribution_id == 2:
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)

            self.lblMTBFi.set_markup(_(u"<span>MTBF:</span>"))
            self.lblFIi.set_markup(_(u"<span>Failure Intensity:</span>"))

            # Show widgets necessary for Kaplan-Meier results.
            self.lblMTBFi.show()
            self.txtMTBFiLL.show()
            self.txtMTBFi.show()
            self.txtMTBFiUL.show()
            self.lblFIi.show()
            self.txtHazardRateiLL.show()
            self.txtHazardRatei.show()
            self.txtHazardRateiUL.show()

            # Hide the cumulative MTBF and failure intensity results.
            self.lblCumMTBF.hide()
            self.lblCumFI.hide()
            self.lblModel.hide()
            self.txtMTBFLL.hide()
            self.txtMTBF.hide()
            self.txtMTBFUL.hide()
            self.txtHazardRateLL.hide()
            self.txtHazardRate.hide()
            self.txtHazardRateUL.hide()

        # Update NHPP Power Law analysis information.
        elif self._model.distribution_id == 3:
            self.hpnAnalysisResults.pack2(self.fraNonParEst, True, True)
            self.vpnAnalysisResults.pack2(self.fraParStats, True, True)

            _b_hat = str(fmt.format(self._model.scale[1]))
            _alpha_hat = str(fmt.format(self._model.shape[1]))
            self.lblModel.set_markup(_(u"<span>MTBF<sub>C</sub> = "
                                       u"%s T<sup>%s</sup></span>") %
                                     (_b_hat, _alpha_hat))

            self.txtScaleLL.set_text(str(fmt.format(self._model.scale[0])))
            self.txtScale.set_text(str(fmt.format(self._model.scale[1])))
            self.txtScaleUL.set_text(str(fmt.format(self._model.scale[2])))
            self.txtShapeLL.set_text(str(fmt.format(self._model.shape[0])))
            self.txtShape.set_text(str(fmt.format(self._model.shape[1])))
            self.txtShapeUL.set_text(str(fmt.format(self._model.shape[2])))

            self.lblCumMTBF.set_markup(_(u"<span>Cumulative MTBF:</span>"))
            self.lblMTBFi.set_markup(_(u"<span>Instantaneous MTBF:</span>"))
            self.lblCumFI.set_markup(_(u"<span>Cumulative Failure Intensity:"
                                       u"</span>"))
            self.lblFIi.set_markup(_(u"<span>Instantaneous Failure Intensity:"
                                     u"</span>"))
            self.lblScale.set_markup(_(u"b"))
            self.lblShape.set_markup(_(u"\u03B1"))

            # Show labels necessary for NHPP Power Law results.
            self.lblCumMTBF.show()
            self.lblCumFI.show()
            self.lblModel.show()
            self.lblMTBFi.show()
            self.lblFIi.show()

            # Show gtk.Entry() necessary for NHPP Power Law results.
            self.txtMTBFLL.show()
            self.txtMTBF.show()
            self.txtMTBFUL.show()
            self.txtHazardRateLL.show()
            self.txtHazardRate.show()
            self.txtHazardRateUL.show()
            self.txtMTBFiLL.show()
            self.txtMTBFi.show()
            self.txtMTBFiUL.show()
            self.txtHazardRateiLL.show()
            self.txtHazardRatei.show()
            self.txtHazardRateiUL.show()

        # Update parametric analysis information.
        else:
            self.vpnAnalysisResults.pack2(self.fraParStats, True, True)

            self.txtScaleLL.set_text(str(fmt.format(self._model.scale[0])))
            self.txtScale.set_text(str(fmt.format(self._model.scale[1])))
            self.txtScaleUL.set_text(str(fmt.format(self._model.scale[2])))
            self.txtShapeLL.set_text(str(fmt.format(self._model.shape[0])))
            self.txtShape.set_text(str(fmt.format(self._model.shape[1])))
            self.txtShapeUL.set_text(str(fmt.format(self._model.shape[2])))
            self.txtLocationLL.set_text(
                str(fmt.format(self._model.location[0])))
            self.txtLocation.set_text(
                str(fmt.format(self._model.location[1])))
            self.txtLocationUL.set_text(
                str(fmt.format(self._model.location[2])))
            # Scale variance.
            self.txtScaleScale.set_text(
                str(fmt.format(self._model.variance[0])))
            # Shape variance.
            self.txtShapeShape.set_text(
                str(fmt.format(self._model.variance[1])))
            # Location variance.
            self.txtLocationLocation.set_text(
                str(fmt.format(self._model.variance[2])))
            # Shape-scale covariance.
            self.txtShapeScale.set_text(
                str(fmt.format(self._model.covariance[0])))
            # Scale-shape covariance.
            self.txtScaleShape.set_text(
                str(fmt.format(self._model.covariance[0])))
            # Scale-location covariance.
            self.txtScaleLocation.set_text(
                str(fmt.format(self._model.covariance[1])))
            # Location-scale covariance.
            self.txtLocationScale.set_text(
                str(fmt.format(self._model.covariance[1])))
            # Shape-location covariance.
            self.txtShapeLocation.set_text(
                str(fmt.format(self._model.covariance[2])))
            # Location-shape covariance.
            self.txtLocationShape.set_text(
                str(fmt.format(self._model.covariance[2])))
            self.txtAIC.set_text(str(fmt.format(self._model.aic)))
            self.txtBIC.set_text(str(fmt.format(self._model.bic)))
            self.txtMLE.set_text(str(fmt.format(self._model.mle)))

            self.lblMTBFi.set_markup(_(u"<span>MTBF:</span>"))
            self.lblFIi.set_markup(_(u"<span>Failure Intensity:</span>"))
            self.lblScale.set_markup(_(u"<span>Scale</span>"))
            self.lblShape.set_markup(_(u"<span>Shape</span>"))
            self.lblLocation.set_markup(_(u"<span></span>"))

            self.vpnAnalysisResults.show_all()

            # Show the instantaneous MTBF and failure intensity results.
            self.lblMTBFi.show()
            self.lblFIi.show()
            self.txtMTBFiLL.show()
            self.txtMTBFi.show()
            self.txtMTBFiUL.show()
            self.txtHazardRateiLL.show()
            self.txtHazardRatei.show()
            self.txtHazardRateiUL.show()

            # Show the variance-covariance matrix for the parameters.
            if self._model.distribution_id == 5:    # Exponential
                self.lblShape.hide()
                self.txtShape.hide()
                self.txtShapeLL.hide()
                self.txtShapeUL.hide()
                self.lblRowShape.hide()
                self.lblColShape.hide()
                self.txtShapeShape.hide()
                self.txtShapeScale.hide()
                self.txtScaleShape.hide()
            else:
                self.lblShape.show()
                self.txtShape.show()
                self.txtShapeLL.show()
                self.txtShapeUL.show()
                self.lblRowShape.show()
                self.lblColShape.show()
                self.txtShapeShape.show()
                self.txtShapeScale.show()
                self.txtScaleShape.show()

            self.lblRowLocation.hide()
            self.lblColLocation.hide()
            self.lblLocation.hide()
            self.txtLocation.hide()
            self.txtLocationLL.hide()
            self.txtLocationUL.hide()
            self.txtLocationLocation.hide()
            self.txtScaleLocation.hide()
            self.txtLocationScale.hide()
            self.txtShapeLocation.hide()
            self.txtLocationShape.hide()

            # Hide the cumulative MTBF and failure intensity results.
            self.lblCumMTBF.hide()
            self.lblCumFI.hide()
            self.txtMTBFLL.hide()
            self.txtMTBF.hide()
            self.txtMTBFUL.hide()
            self.txtHazardRateLL.hide()
            self.txtHazardRate.hide()
            self.txtHazardRateUL.hide()

        return False

    def _load_dataset_records(self):
        """
        Method to load the Survival analysis records into the dataset
        gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
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
            _model.append([_results[i][0], _date, _results[i][20],
                           _results[i][3], _results[i][4], _results[i][7],
                           _results[i][6], _status])

        return False

    def update(self):
        """
        Updates the Work Book widgets with changes to the Survival data model
        attributes.  Called by other views when the Survival data model
        attributes are edited via their gtk.Widgets().
        """

        self.cmbCategory.handler_block(self._lst_handler_id[2])
        self.cmbCategory.set_active(self._model.survival_category)
        self.cmbCategory.handler_unblock(self._lst_handler_id[2])

        self.cmbType.handler_block(self._lst_handler_id[3])
        self.cmbType.set_active(self._model.survival_type)
        self.cmbType.handler_unblock(self._lst_handler_id[3])

        self.cmbCriticality.handler_block(self._lst_handler_id[4])
        self.cmbCriticality.set_active(self._model.criticality)
        self.cmbCriticality.handler_unblock(self._lst_handler_id[4])

        self.cmbStatus.handler_block(self._lst_handler_id[5])
        self.cmbStatus.set_active(self._model.status)
        self.cmbStatus.handler_unblock(self._lst_handler_id[5])

        self.cmbLifeCycle.handler_block(self._lst_handler_id[9])
        self.cmbLifeCycle.set_active(self._model.life_cycle)
        self.cmbLifeCycle.handler_unblock(self._lst_handler_id[9])

        self.cmbDetectionMethod.handler_block(self._lst_handler_id[14])
        self.cmbDetectionMethod.set_active(self._model.detection_method)
        self.cmbDetectionMethod.handler_unblock(self._lst_handler_id[14])

        self.txtTest.set_text(_util.none_to_string(self._model.test))
        self.txtTestCase.set_text(_util.none_to_string(self._model.test_case))
        self.txtExecutionTime.set_text(str(self._model.execution_time))

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
            print "Add Survival analysis"
        elif index == 5:
            print "Remove Survival analysis"
        elif index == 6:
            print "Consolidate dataset"
        elif index == 7:
            self._model.estimate_parameters()
            self._load_analysis_results_page()
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
        :rtype: boolean
        """

        _record = self._model.dicRecords[self._record_id]

        if position == 2:
            model[path][position] = new_text
            #_record[0] = new_text
        elif position == 3:
            model[path][position] = float(new_text)
            _record[2] = float(new_text)
        elif position == 4:
            model[path][position] = float(new_text)
            _record[3] = float(new_text)
        elif position == 5:
            model[path][position] = float(new_text)
            _record[6] = float(new_text)
        elif position == 6:
            model[path][position] = int(new_text)
            _record[5] = int(new_text)
        elif position == 7:
            _model = cell.get_property('model')
            _new_text = _model.get_value(new_text, 0)
            model[path][position] = _new_text
            for j in (i for i,x in enumerate(self._lst_status)
                      if x == _new_text):
                _record[4] = int(j)

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
        #    _new_text = _conf.RTK_INCIDENT_TYPE[combo.get_active() - 1]
        #    self._modulebook.update(index, _new_text)
        elif index == 5:                    # Source of records
            self._model.source = combo.get_active()
        #    _new_text = _conf.RTK_INCIDENT_CRITICALITY[combo.get_active() - 1]
        #    self._modulebook.update(index + 2, _new_text)
        elif index == 6:                    # Statistical distribution
            self._model.distribution_id = combo.get_active()
        #    _new_text = _conf.RTK_INCIDENT_STATUS[combo.get_active() - 1]
        #    self._modulebook.update(index + 4, _new_text)
        elif index == 7:                   # Confidence type
            self._model.confidence_type = combo.get_active()
        elif index == 8:                   # Confidence method
            self._model.confidence_method = combo.get_active()
        #    _row = combo.get_active_iter()
        #    try:
        #        self._model.software_id = int(_model.get_value(_row, 1))
        #    except ValueError:
        #        self._model.software_id = 0
        elif index == 9:                   # Fit method
            self._model.fit_method = combo.get_active()
        #    _new_text = _conf.RTK_USERS[combo.get_active() - 1]
        #    self._modulebook.update(index + 10, _new_text)

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
            _new_text = _util.date_to_ordinal(entry.get_text())
            self._model.description = entry.get_text()
            #self._modulebook.update(index + 18, _new_text)
        elif index == 11:
            _new_text = float(entry.get_text())
            self._model.confidence = _new_text
            #self._modulebook.update(index - 7, _new_text)
        elif index == 12:
            _new_text = float(entry.get_text())
            self._model.start_time = _new_text
            #self._modulebook.update(index - 7, _new_text)
        elif index == 13:
            _new_text = float(entry.get_text())
            self._model.end_time = _new_text
            #self._modulebook.update(index - 5, _new_text)
        elif index == 14:
            _new_text = int(entry.get_text())
            self._model.n_rel_points = _new_text
            #self._modulebook.update(index - 5, _new_text)
        elif index == 15:
            _new_text = _util.date_to_ordinal(entry.get_text())
            self._model.start_date = _new_text
            #self._modulebook.update(index - 5, _new_text)
        elif index == 16:
            _new_text = _util.date_to_ordinal(entry.get_text())
            self._model.end_date = _new_text
            #self._modulebook.update(index - 5, _new_text)

        entry.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_record_select(self, treeview, __path, __column):
        """
        Method to respond to the Dataset record gtk.TreeView() mouse clicks.

        :param gtk.TreeView treeview: the Dataset gtk.TreeView().
        :param str __path: the path in the Dataset gtk.TreeView() of the
                           selected record.
        :param gtk.TreeColumn __column: the selected column in the Dataset
                                        gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = treeview.get_selection().get_selected()

        self._record_id = _model.get_value(_row, 0)

        return False
