#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
the functions of the Program.
"""

# -*- coding: utf-8 -*-
__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014'

import gettext
import locale
import sys

import configuration as _conf
import utilities as _util
import widgets as _widg

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gtk.glade  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")

_ = gettext.gettext


class Function(object):
    """
    The Function class is used to represent a function in a system being
    analyzed.

    :ivar revision_id: initial_value: 0
    :ivar function_id: initial_value: 0
    :ivar availability: initial_value: 0.0
    :ivar mission_availability: initial_value: 0.0
    :ivar code: initial_value: ''
    :ivar cost: initial_value: 0.0
    :ivar mission_hazard_rate: initial_value: 0.0
    :ivar hazard_rate: initial_value: 0.0
    :ivar mmt: initial_value: 0.0
    :ivar mcmt: initial_value: 0.0
    :ivar mpmt: initial_value: 0.0
    :ivar mission_mtbf: initial_value: 0.0
    :ivar mtbf: initial_value: 0.0
    :ivar mttr: initial_value: 0.0
    :ivar name: initial_value: ''
    :ivar remarks: initial_value: ''
    :ivar n_modes: initial_value: 0
    :ivar n_parts: initial_value: 0
    :ivar type: initial_value: 0
    :ivar parent_id: initial_value: ''
    :ivar level: initial_value: 0
    :ivar safety_critical: initial_value: 1
    """

    def __init__(self, application):
        """
        Initializes the Function class.

        :param application: the current instance of the RTK application.
        """

        # Define private Function class attributes.
        self._app = application

        # Define private Function class dictionary attributes.

        # Define private Function class list attributes.
        self._lst_handler_id = []

        # Define public Function class attributes.
        self.revision_id = 0
        self.function_id = 0
        self.availability = 0.0
        self.mission_availability = 0.0
        self.code = ''
        self.cost = 0.0
        self.mission_hazard_rate = 0.0
        self.hazard_rate = 0.0
        self.mmt = 0.0
        self.mcmt = 0.0
        self.mpmt = 0.0
        self.mission_mtbf = 0.0
        self.mtbf = 0.0
        self.mttr = 0.0
        self.name = ''
        self.remarks = ''
        self.n_modes = 0
        self.n_parts = 0
        self.type = 0
        self.parent_id = ''
        self.level = 0
        self.safety_critical = 1

        # Create the main Function class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Function', 1, self._app,
                                                    None, _conf.RTK_COLORS[2],
                                                    _conf.RTK_COLORS[3])

        # Toolbar widgets.
        self.btnAddSibling = gtk.ToolButton()
        self.btnAddChild = gtk.ToolButton()
        self.btnAddMode = gtk.ToolButton()
        self.btnRemoveFunction = gtk.ToolButton()
        self.btnRemoveMode = gtk.ToolButton()
        self.btnCalculate = gtk.ToolButton()
        self.btnSave = gtk.ToolButton()

        # General data tab widgets.
        self.chkSafetyCritical = _widg.make_check_button(label=_(u"Function "
                                                                 u"is safety "
                                                                 u"critical."))
        self.txtCode = _widg.make_entry()
        self.txtTotalCost = _widg.make_entry(width=75, editable=False,
                                             bold=True)
        self.txtName = _widg.make_text_view(width=400)
        self.txtModeCount = _widg.make_entry(width=75, editable=False,
                                             bold=True)
        self.txtPartCount = _widg.make_entry(width=75, editable=False,
                                             bold=True)
        self.txtRemarks = _widg.make_text_view(width=400)

        # Functional matrix tab widgets.
        self.chkParts = _widg.make_check_button(label=_(u"Show components."))
        self.chkAssemblies = _widg.make_check_button(label=_(u"Show "
                                                             u"assemblies."))
        self.tvwFunctionMatrix = gtk.TreeView()

        # Diagram tab widgets.
# TODO: Implement Diagram Worksheet for the Function Class.

        # Assessment results tab widgets.
        self.txtPredictedHt = _widg.make_entry(editable=False, bold=True)
        self.txtMissionHt = _widg.make_entry(editable=False, bold=True)
        self.txtMTBF = _widg.make_entry(editable=False, bold=True)
        self.txtMissionMTBF = _widg.make_entry(editable=False, bold=True)
        self.txtMPMT = _widg.make_entry(editable=False, bold=True)
        self.txtMCMT = _widg.make_entry(editable=False, bold=True)
        self.txtMTTR = _widg.make_entry(editable=False, bold=True)
        self.txtMMT = _widg.make_entry(editable=False, bold=True)
        self.txtAvailability = _widg.make_entry(editable=False, bold=True)
        self.txtMissionAt = _widg.make_entry(editable=False, bold=True)

        # FMECA worksheet tab widgets.
        (self.tvwFMECA,
         self._FMECA_col_order) = _widg.make_treeview('FFMECA', 18, self._app,
                                                      None,
                                                      _conf.RTK_COLORS[6],
                                                      _conf.RTK_COLORS[7])

        # Put it all together.
        _toolbar = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxFunction = gtk.VBox()
        self.vbxFunction.pack_start(_toolbar, expand=False)
        self.vbxFunction.pack_end(self.notebook)

        self.notebook.connect('switch-page', self._notebook_page_switched)

    def create_tree(self):
        """
        Creates the FUNCTION gtk.TreeView() and connects it to callback
        functions to handle editting.  Background and foreground colors can be
        set using the user-defined values in the RTK configuration file.
        """

        self.treeview.set_tooltip_text(_(u"Displays an indented list (tree) "
                                         u"of functions."))
        self.treeview.set_enable_tree_lines(True)
        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        # Connect the cells to the callback function.
        for i in [4, 14, 15]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._function_tree_edit, i,
                             self.treeview.get_model())

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)

        return _scrollwindow

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Function class work book.
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add sibling function button.
        self.btnAddSibling.set_tooltip_text(_(u"Adds a new function at the "
                                              u"same indenture level as the "
                                              u"selected function (i.e., a "
                                              u"sibling function)."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        self.btnAddSibling.set_icon_widget(_image)
        self.btnAddSibling.connect('clicked', self._add_function, 0)
        _toolbar.insert(self.btnAddSibling, _position)
        _position += 1

        # Add child function button.
        self.btnAddChild.set_tooltip_text(_(u"Adds a new function one "
                                            u"indenture level subordinate to "
                                            u"the selected function (i.e., a "
                                            u"child function)."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        self.btnAddChild.set_icon_widget(_image)
        self.btnAddChild.connect('clicked', self._add_function, 1)
        _toolbar.insert(self.btnAddChild, _position)
        _position += 1

        # Add a failure mode button.
        self.btnAddMode.set_tooltip_text(_(u"Adds a failure mode to the "
                                           u"currently selected function."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAddMode.set_icon_widget(_image)
        self.btnAddMode.connect('clicked', self._add_failure_mode)
        _toolbar.insert(self.btnAddMode, _position)
        _position += 1

        # Delete function button
        self.btnRemoveFunction.set_tooltip_text(_(u"Removes the currently "
                                                  u"selected function."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveFunction.set_icon_widget(_image)
        self.btnRemoveFunction.connect('clicked', self._delete_function)
        _toolbar.insert(self.btnRemoveFunction, _position)
        _position += 1

        # Delete a failure mode button.
        self.btnRemoveMode.set_tooltip_text(_(u"Removes the currently "
                                              u"selected failure mode."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemoveMode.set_icon_widget(_image)
        self.btnRemoveMode.connect('clicked', self._delete_failure_mode)
        _toolbar.insert(self.btnRemoveMode, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Calculate function button
        self.btnCalculate.set_tooltip_text(_(u"Calculate the functions."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        self.btnCalculate.set_icon_widget(_image)
        self.btnCalculate.connect('clicked', self.calculate)
        _toolbar.insert(self.btnCalculate, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save function button.
        self.btnSave.set_tooltip_text(_(u"Saves changes to the selected "
                                        u"function."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSave.set_icon_widget(_image)
        self.btnSave.set_name('Save')
        self.btnSave.connect('clicked', self._toolbutton_pressed)
        _toolbar.insert(self.btnSave, _position)

        _toolbar.show()

        self.btnAddMode.hide()
        self.btnRemoveMode.hide()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Function class gtk.Notebook().
        """

        def _create_general_data_tab(self, notebook):
            """
            Function to create the Function class gtk.Notebook() page for
            displaying general data about the selected Function.

            :param rtk.Function self: the current instance of a Function class.
            :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _fixed_ = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed_)

            _frame = _widg.make_frame(label=_(u"General Information"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information about   #
            # the function.                                                 #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _labels = [_(u"Function Code:"), _(u"Function Name:")]
            (_max1, _y_pos1) = _widg.make_labels(_labels, _fixed_, 5, 5)

            _labels = [_(u"Total Cost:"), _(u"Total Mode Count:"),
                       _(u"Total Part Count:"), _(u"Remarks:")]
            _y_start = self.txtName.size_request()[1] + _y_pos1[1] + 5
            (_max2, _y_pos2) = _widg.make_labels(_labels, _fixed_, 5, _y_start)
            _x_pos = max(_max1, _max2) + 20

            # Set the tooltips.
            self.txtCode.set_tooltip_text(_(u"Enter a unique code for the "
                                            u"selected function."))
            self.txtName.set_tooltip_text(_(u"Enter the name of the selected "
                                            u"function."))
            self.txtTotalCost.set_tooltip_text(_(u"Displays the total cost of "
                                                 u"the selected function."))
            self.txtModeCount.set_tooltip_text(_(u"Displays the total number "
                                                 u"of failure modes "
                                                 u"associated with the "
                                                 u"selected function."))
            self.txtPartCount.set_tooltip_text(_(u"Displays the total number "
                                                 u"of components associated "
                                                 u"with the selected "
                                                 u"function."))
            self.txtRemarks.set_tooltip_text(_(u"Enter any remarks related to "
                                               u"the selected function."))
            self.chkSafetyCritical.set_tooltip_text(_(u"Indicates whether or "
                                                      u"not the selected "
                                                      u"function is safety "
                                                      u"critical."))

            # Place the widgets.
            _fixed_.put(self.txtCode, _x_pos, _y_pos1[0])
            _fixed_.put(self.txtName, _x_pos, _y_pos1[1])
            _fixed_.put(self.txtTotalCost, _x_pos, _y_pos2[0])
            _fixed_.put(self.txtModeCount, _x_pos, _y_pos2[1])
            _fixed_.put(self.txtPartCount, _x_pos, _y_pos2[2])
            _fixed_.put(self.txtRemarks, _x_pos, _y_pos2[3])
            _fixed_.put(self.chkSafetyCritical, 5, _y_pos2[3] + 110)

            # Connect to callback functions.
            self._lst_handler_id.append(
                self.txtCode.connect('focus-out-event',
                                     self._callback_entry, 'text', 4))
            _textview = self.txtName.get_child().get_child()
            self._lst_handler_id.append(
                _textview.connect('focus-out-event', self._callback_entry,
                                  'text', 14))
            _textview = self.txtRemarks.get_child().get_child()
            self._lst_handler_id.append(
                _textview.connect('focus-out-event', self._callback_entry,
                                  'text', 15))

            _fixed_.show_all()

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"General\nData") +
                              "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_tooltip_text(_(u"Displays general information for the "
                                      u"selected function."))
            _label.show_all()
            notebook.insert_page(_frame, tab_label=_label, position=-1)

            return False

        def _create_functional_matrix_tab(self, notebook):
            """
            Function to create the hardware-function matrix tab.

            :param rtk.Function self: the current instance of a Function class.
            :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _vbox_ = gtk.VBox()

            _fixed_ = gtk.Fixed()
            _vbox_.pack_start(_fixed_, expand=False)

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add(self.tvwFunctionMatrix)

            _vbox_.pack_end(_scrollwindow_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display and control the functional  #
            # matrix.                                                       #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            self.tvwFunctionMatrix.set_grid_lines(
                gtk.TREE_VIEW_GRID_LINES_BOTH)

            self.chkParts.set_tooltip_text(_(u"Include components in the "
                                             u"functional matrix."))
            self.chkParts.connect('toggled', self._callback_check)
            self.chkParts.set_active(True)
            _fixed_.put(self.chkParts, 5, 5)

            self.chkAssemblies.set_tooltip_text(_(u"Include assemblies in the "
                                                  u"functional matrix."))
            self.chkAssemblies.connect('toggled', self._callback_check)
            self.chkAssemblies.set_active(True)
            _fixed_.put(self.chkAssemblies, 5, 35)

            # Insert the tab.
            _label_ = gtk.Label()
            _label_.set_markup("<span weight='bold'>" +
                               _(u"Hardware-\nFunction\nMatrix") +
                               "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.set_tooltip_text(_(u"Displays the hardware/function "
                                       U"cross-reference matrix."))
            _label_.show_all()
            notebook.insert_page(_vbox_, tab_label=_label_,
                                 position=-1)

            return False

        def _create_assessment_results_tab(self, notebook):
            """
            Function to create the Function class gtk.Notebook() page for
            displaying assessment results for teh selected Function.

            :param rtk.Function self: the current instance of a Function class.
            :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox_ = gtk.HBox()

            # Construct the left half of the page.
            _fxdLeft_ = gtk.Fixed()

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add_with_viewport(_fxdLeft_)

            _frame_ = _widg.make_frame(label=_(u"Reliability Results"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            _hbox_.pack_start(_frame_)

            # Construct the right half of the page.
            _fxdRight_ = gtk.Fixed()

            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add_with_viewport(_fxdRight_)

            _frame_ = _widg.make_frame(label=_(u"Maintainability Results"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            _hbox_.pack_end(_frame_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information about   #
            # the function.                                                 #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the left half of the page.
            _labels_ = [_(u"Predicted h(t):"), _(u"Mission h(t):"),
                        _(u"MTBF:"), _(u"Mission MTBF:")]
            _max1_ = 0
            _max2_ = 0
            (_max1_, _y_pos_) = _widg.make_labels(_labels_, _fxdLeft_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 20

            self.txtPredictedHt.set_tooltip_text(_(u"Displays the predicted "
                                                   u"failure intensity for "
                                                   u"the selected function."))
            self.txtMissionHt.set_tooltip_text(_(u"Displays the mission "
                                                 u"failure intensity for the "
                                                 u"selected function."))
            self.txtMTBF.set_tooltip_text(_(u"Displays the limiting mean time "
                                            u"between failure (MTBF) for the "
                                            u"selected function."))
            self.txtMissionMTBF.set_tooltip_text(_(u"Displays the mission "
                                                   u"mean time between "
                                                   u"failure (MTBF) for the "
                                                   u"selected function."))

            _fxdLeft_.put(self.txtPredictedHt, _x_pos_, _y_pos_[0])
            _fxdLeft_.put(self.txtMissionHt, _x_pos_, _y_pos_[1])
            _fxdLeft_.put(self.txtMTBF, _x_pos_, _y_pos_[2])
            _fxdLeft_.put(self.txtMissionMTBF, _x_pos_, _y_pos_[3])

            _fxdLeft_.show_all()

            # Create the right half of the page.
            _labels_ = [_(u"MPMT:"), _(u"MCMT:"), _(u"MTTR:"), _(u"MMT:"),
                        _(u"Availability:"), _(u"Mission Availability:")]
            _max1_ = 0
            _max2_ = 0
            (_max1_, _y_pos_) = _widg.make_labels(_labels_, _fxdRight_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 20

            self.txtMPMT.set_tooltip_text(_(u"Displays the mean preventive "
                                            u"maintenance time (MPMT) for the "
                                            u"selected function."))
            self.txtMCMT.set_tooltip_text(_(u"Displays the mean corrective "
                                            u"maintenance time (MCMT) for the "
                                            u"selected function."))
            self.txtMTTR.set_tooltip_text(_(u"Displays the mean time to "
                                            u"repair (MTTR) for the selected "
                                            u"function."))
            self.txtMMT.set_tooltip_text(_(u"Displays the mean maintenance "
                                           u"time (MMT) for the selected "
                                           u"function."))
            self.txtAvailability.set_tooltip_text(_(u"Displays the limiting "
                                                    u"availability for the "
                                                    u"selected function."))
            self.txtMissionAt.set_tooltip_text(_(u"Displays the mission "
                                                 u"availability for the "
                                                 u"selected function."))

            _fxdRight_.put(self.txtMPMT, _x_pos_, _y_pos_[0])
            _fxdRight_.put(self.txtMCMT, _x_pos_, _y_pos_[1])
            _fxdRight_.put(self.txtMTTR, _x_pos_, _y_pos_[2])
            _fxdRight_.put(self.txtMMT, _x_pos_, _y_pos_[3])
            _fxdRight_.put(self.txtAvailability, _x_pos_, _y_pos_[4])
            _fxdRight_.put(self.txtMissionAt, _x_pos_, _y_pos_[5])

            _fxdRight_.show_all()

            # Insert the tab.
            _label_ = gtk.Label()
            _label_.set_markup("<span weight='bold'>" +
                               _(u"Assessment\nResults") +
                               "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.set_tooltip_text(_(u"Displays reliability, "
                                       u"maintainability, and availability "
                                       u"assessment results for the selected "
                                       u"function."))
            _label_.show_all()
            notebook.insert_page(_hbox_, tab_label=_label_, position=-1)

            return False

        def _create_fmeca_tab(self, notebook):
            """
            Function to create the FMECA gtk.Notebook() page and populate it
            with the appropriate widgets.

            :param rtk.Function self: the current instance of a Function class.
            :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _scrollwindow_ = gtk.ScrolledWindow()
            _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC,
                                      gtk.POLICY_AUTOMATIC)
            _scrollwindow_.add(self.tvwFMECA)

            _frame_ = _widg.make_frame(label=_(u"Failure Mode, Effects, and "
                                               U"Criticality Analysis"))
            _frame_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame_.add(_scrollwindow_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display the functional FMECA.       #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the severity classification gtk.CellRendererCombo.
            _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[11])
            _cell_ = _column_.get_cell_renderers()
            _cellmodel_ = _cell_[0].get_property('model')
            _cellmodel_.clear()
            _query_ = "SELECT fld_criticality_id, fld_criticality_name, \
                              fld_criticality_cat \
                       FROM tbl_criticality"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_crit_ = len(_results_)
            except TypeError:
                _n_crit_ = 0

            _cellmodel_.append([""])
            for i in range(_n_crit_):
                _cellmodel_.append([_results_[i][2] + " - " + _results_[i][1]])

            # Load the qualitative failure probability gtk.CellRendererCombo.
            _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[13])
            _cell_ = _column_.get_cell_renderers()
            _cellmodel_ = _cell_[0].get_property('model')
            _cellmodel_.clear()
            _query_ = "SELECT * FROM tbl_failure_probability"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_probs_ = len(_results_)
            except TypeError:
                _n_probs_ = 0

            _cellmodel_.append([""])
            for i in range(_n_probs_):
                _cellmodel_.append([_results_[i][1]])

            # Load the RPN severity and RPN severity new gtk.CellRendererCombo.
            _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[20])
            _cell_ = _column_.get_cell_renderers()
            _cellmodel1_ = _cell_[0].get_property('model')
            _cellmodel1_.clear()
            _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[21])
            _cell_ = _column_.get_cell_renderers()
            _cellmodel2_ = _cell_[0].get_property('model')
            _cellmodel2_.clear()
            _query_ = "SELECT fld_severity_name \
                       FROM tbl_rpn_severity \
                       WHERE fld_fmeca_type=0"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            try:
                _n_sev_ = len(_results_)
            except TypeError:
                _n_sev_ = 0

            _cellmodel1_.append([""])
            _cellmodel2_.append([""])
            for i in range(_n_sev_):
                _cellmodel1_.append([_results_[i][0]])
                _cellmodel2_.append([_results_[i][0]])

            #self.tvwFMECA.connect('cursor_changed',
            #                      self._fmeca_treeview_row_changed, None, None)
            #self.tvwFMECA.connect('row_activated',
            #                      self._fmeca_treeview_row_changed)

            # Insert the tab.
            _label_ = gtk.Label()
            _label_.set_markup("<span weight='bold'>" +
                               _(u"FMEA/FMECA\nWorksheet") +
                               "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.set_tooltip_text(_(u"Failure mode, effects, and "
                                       u"criticality analysis (FMECA) for the "
                                       u"selected function."))
            _label_.show_all()

            notebook.insert_page(_frame_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        _notebook_ = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook_.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook_.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook_.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook_.set_tab_pos(gtk.POS_BOTTOM)

        _create_general_data_tab(self, _notebook_)
        _create_functional_matrix_tab(self, _notebook_)
        _create_assessment_results_tab(self, _notebook_)
        _create_fmeca_tab(self, _notebook_)

        return _notebook_

    def load_tree(self):
        """
        Method to load the Function Class gtk.TreeView().
        """

        # Select everything from the function table.
        _query = "SELECT * FROM tbl_functions \
                  WHERE fld_revision_id=%d \
                  ORDER BY fld_parent_id" % self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        try:
            _n_functions = len(_results)
        except TypeError:
            _n_functions = 0

        # Clear the gtk.TreeView() of any existing information.
        _model = self.treeview.get_model()
        _model.clear()

        # Load the gtk.TreeView() with the new function information.
        for i in range(_n_functions):
            if _results[i][self._lst_col_order[19]] == '-':
                _piter = None
            else:
                _piter = _model.get_iter_from_string(
                    _results[i][self._lst_col_order[19]])

            _model.append(_piter, _results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        _root = _model.get_iter_root()
        if _root is not None:
            _path = _model.get_path(_root)
            _col = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _col)

            self.function_id = _model.get_value(_root, 1)

        self._load_functional_matrix()

        return False

    def _load_functional_matrix(self):
        """
        Creates the gtk.TreeView() widget to display the Hardware-Function
        relationship matrix.
        """

        import pango

        _query = "SELECT fld_function_id, fld_code, fld_name \
                  FROM tbl_functions \
                  WHERE fld_revision_id=%d" % self.revision_id
        _functions_ = self._app.DB.execute_query(_query, None,
                                                 self._app.ProgCnx,
                                                 commit=False)
        try:
            _n_functions_ = len(_functions_)
        except TypeError:
            _n_functions_ = 0

        # Make the treeview to display the functional matrix.
        _types = ['gint']
        for i in range(_n_functions_ + 1):
            _types.append('gchararray')
        _types = [gobject.type_from_name(_types[i])
                   for i in range(len(_types))]
        _model = gtk.TreeStore(*_types)

        self.tvwFunctionMatrix.set_model(_model)

        # Add the column to display the assembly/component name.
        _column_ = self.tvwFunctionMatrix.get_column(0)
        while _column_ is not None:
            self.tvwFunctionMatrix.remove_column(_column_)
            _column_ = self.tvwFunctionMatrix.get_column(0)

        # Add a column to store the assembly ID.
        _cell_ = gtk.CellRendererText()
        _cell_.set_property('editable', 0)
        _cell_.set_property('cell_background_gdk', gtk.gdk.Color('grey'))
        _cell_.set_property('font_desc', pango.FontDescription("bold 10"))
        _cell_.set_property('xalign', 0.5)
        _cell_.set_property('yalign', 0.1)
        _column_ = gtk.TreeViewColumn()
        _column_.set_resizable(False)
        _column_.pack_start(_cell_, True)
        _column_.add_attribute(_cell_, 'text', 0)
        _label_ = gtk.Label()
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.set_markup(_(u"<span weight='bold'>Assembly\nID</span>"))
        _label_.show_all()
        _column_.set_widget(_label_)
        self.tvwFunctionMatrix.append_column(_column_)

        # Add a column to store the assembly name.
        _cell_ = gtk.CellRendererText()
        _cell_.set_property('editable', 0)
        _cell_.set_property('cell_background_gdk', gtk.gdk.Color('grey'))
        _cell_.set_property('font_desc', pango.FontDescription("bold 10"))
        _column_ = gtk.TreeViewColumn()
        _column_.set_resizable(True)
        _column_.pack_start(_cell_, True)
        _column_.add_attribute(_cell_, 'text', 1)
        _label_ = gtk.Label()
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.set_markup(_(u"<span weight='bold'>Name\n</span>"))
        _label_.show_all()
        _column_.set_widget(_label_)
        self.tvwFunctionMatrix.append_column(_column_)

        # List store for cell renderer.
        _cellmodel_ = gtk.ListStore(gobject.TYPE_STRING)
        _cellmodel_.append([""])
        _cellmodel_.append(["X"])

        _dic_functions_ = {}
        for i in range(_n_functions_):
            _dic_functions_[i + 2] = _functions_[i][0]
            _cell_ = gtk.CellRendererCombo()
            _cell_.set_property('editable', True)
            _cell_.set_property('has-entry', False)
            _cell_.set_property('model', _cellmodel_)
            _cell_.set_property('text-column', 0)
            _cell_.set_property('xalign', 0.5)
            _cell_.set_property('yalign', 0.5)
            _cell_.connect('edited', self._edit_functional_matrix, i + 2,
                           _dic_functions_)
            _column_ = gtk.TreeViewColumn()
            _column_.set_resizable(True)
            _column_.pack_end(_cell_)
            _column_.set_attributes(_cell_, markup=i + 2)
            _label_ = gtk.Label(_column_.get_title())
            _label_.set_property('angle', 90)
            _label_.set_tooltip_text(_functions_[i][2])
            _label_.set_markup("<span weight='bold'>" +
                               _functions_[i][1] + "</span>")
            _label_.show_all()
            _column_.set_widget(_label_)
            _column_.connect('notify::width', _widg.resize_wrap, _cell_)
            self.tvwFunctionMatrix.append_column(_column_)

        _column_ = gtk.TreeViewColumn()
        self.tvwFunctionMatrix.append_column(_column_)

        # Select the assembly id and name for only components, only assemblies,
        # or both components and assemblies.  The default is to select both.
        if self.chkParts.get_active() and not self.chkAssemblies.get_active():
            _query = "SELECT fld_assembly_id, fld_name, fld_parent_assembly \
                      FROM tbl_system \
                      WHERE fld_revision_id=%d \
                      AND fld_part=1" % \
                     self.revision_id
        elif (not self.chkParts.get_active() and
              self.chkAssemblies.get_active()):
            _query = "SELECT fld_assembly_id, fld_name, fld_parent_assembly \
                      FROM tbl_system \
                      WHERE fld_revision_id=%d \
                      AND fld_part=0" % \
                     self.revision_id
        elif self.chkParts.get_active() and self.chkAssemblies.get_active():
            _query = "SELECT fld_assembly_id, fld_name, fld_parent_assembly \
                      FROM tbl_system \
                      WHERE fld_revision_id=%d" % \
                     self.revision_id
        else:
            _query = ""

        _assemblies = self._app.DB.execute_query(_query, None,
                                                 self._app.ProgCnx,
                                                 commit=False)

        try:
            _n_items = len(_assemblies)
        except TypeError:
            _n_items = 0

        # Select the assembly id, function id, and the relationship between the
        # two for the selected revision.
        _query = "SELECT fld_assembly_id, fld_function_id, fld_relationship \
                  FROM tbl_functional_matrix \
                  WHERE fld_revision_id=%d" % self.revision_id
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=False)
        try:
            _n_functions = len(_results)
        except TypeError:
            _n_functions = 0

        # Add a line to the functional matrix for every assembly ID.  Set the
        # cell under each function column to the appropriate relationship
        # value for each assembly.
        for i in range(_n_items):           # Loop through all the hardware.
            if _assemblies[i][2] == '-':    # Its the top level element.
                _piter = None
            elif _assemblies[i][2] != '-':  # Its a child element.
                _piter = _model.get_iter_from_string(_assemblies[i][2])

            _data = []
            _data.append(_assemblies[i][0])
            _data.append(_assemblies[i][1])

            if _n_functions > 0:
                # Loop through all the hardware/function relationships.
                for j in range(_n_functions):
                    if _results[j][2] == '':
                        _color = '#E5E5E5'
                    else:
                        _color = 'black'

                    if _results[j][0] == _assemblies[i][0]:
                        _data.append("<span foreground='%s' background='%s'> "
                                     "%s </span>" %
                                     (_color, _color, _results[j][2]))

            _model.append(_piter, _data)

        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            self.tvwFunctionMatrix.set_cursor(_path, None, False)
            self.tvwFunctionMatrix.row_activated(_path,
                                                 self.treeview.get_column(0))
            self.tvwFunctionMatrix.expand_all()

        return False

    def _load_fmeca(self):
        """
        Method to load the FMECA tab information.
        """

        _model_ = self.tvwFMECA.get_model()
        _model_.clear()

        # Load the mission phase gtk.CellRendererCombo.
        _column_ = self.tvwFMECA.get_column(self._FMECA_col_order[2])
        _cell_ = _column_.get_cell_renderers()
        _cellmodel_ = _cell_[0].get_property('model')
        _cellmodel_.clear()

        _query_ = "SELECT fld_phase_id, fld_phase_name, fld_phase_start, \
                          fld_phase_end \
                   FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d" % 0
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _phases_ = len(_results_)
        except TypeError:
            _phases_ = 0

        _cellmodel_.append([""])
        for i in range(_phases_):
            _cellmodel_.append([_results_[i][1]])

        # Load the FMEA/FMECA worksheet.
        _query_ = "SELECT fld_mode_id, fld_mode_description, \
                          fld_mission_phase, fld_local_effect, \
                          fld_next_effect, fld_end_effect, \
                          fld_detection_method, fld_other_indications, \
                          fld_isolation_method, fld_design_provisions, \
                          fld_operator_actions, fld_severity_class, \
                          fld_hazard_rate_source, fld_failure_probability, \
                          fld_effect_probability, fld_mode_ratio, \
                          fld_mode_failure_rate, fld_mode_op_time, \
                          fld_mode_criticality, fld_rpn_severity, \
                          fld_rpn_severity_new, fld_critical_item, \
                          fld_single_point, fld_remarks \
                   FROM tbl_fmeca \
                   WHERE fld_revision_id=%d \
                   AND fld_assembly_id=0 \
                   AND fld_function_id=%d" % (self._app.REVISION.revision_id,
                                              self.function_id)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_modes_ = len(_results_)
        except TypeError:
            _n_modes_ = 0

        _icon_ = _conf.ICON_DIR + '32x32/mode.png'
        _icon_ = gtk.gdk.pixbuf_new_from_file_at_size(_icon_, 16, 16)
        for i in range(_n_modes_):
            _data_ = [_results_[i][0],
                      _util.none_to_string(_results_[i][1]),
                      _util.none_to_string(_results_[i][2]),
                      _util.none_to_string(_results_[i][3]),
                      _util.none_to_string(_results_[i][4]),
                      _util.none_to_string(_results_[i][5]),
                      _util.none_to_string(_results_[i][6]),
                      _util.none_to_string(_results_[i][7]),
                      _util.none_to_string(_results_[i][8]),
                      _util.none_to_string(_results_[i][9]),
                      _util.none_to_string(_results_[i][10]),
                      _util.none_to_string(_results_[i][11]),
                      _util.none_to_string(_results_[i][12]),
                      _util.none_to_string(_results_[i][13]),
                      _util.none_to_string(_results_[i][14]),
                      str(_results_[i][15]), str(_results_[i][16]),
                      str(_results_[i][17]), str(_results_[i][18]), "",
                      str(_results_[i][19]), str(_results_[i][20]),
                      _results_[i][21], _results_[i][22],
                      _util.none_to_string(_results_[i][23]),
                      0, '#FFFFFF', True, _icon_]

            # Load the FMECA gtk.TreeView with the data.
            try:
                _model_.append(None, _data_)
            except TypeError:
                _util.rtk_error(_(u"Failed to load FMEA/FMECA failure "
                                  u"mode %d" % _results_[i][0]))

        return False

    def load_notebook(self):
        """
        Method to load the Function class gtk.Notebook().
        """

        def _load_general_data_tab(self):
            """
            Function to load the widgets on the general data page.

            :param rtk.Function self: the current instance of the Function
                                      class.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            self.txtCode.set_text(self.code)
            self.txtTotalCost.set_text(str(locale.currency(self.cost)))

            _textbuffer_ = self.txtName.get_child().get_child().get_buffer()
            _textbuffer_.set_text(self.name)

            _textbuffer_ = self.txtRemarks.get_child().get_child().get_buffer()
            _textbuffer_.set_text(self.remarks)

            self.txtModeCount.set_text(str('{0:0.0f}'.format(self.n_modes)))
            self.txtPartCount.set_text(str('{0:0.0f}'.format(self.n_parts)))

            return False

        def _load_assessment_results_tab(self):
            """
            Loads the widgets with calculation results for the Function Object.

            :param rtk.Function self: the current instance of the Function
                                      class.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

            self.txtAvailability.set_text(str(fmt.format(self.availability)))
            self.txtMissionAt.set_text(str(
                fmt.format(self.mission_availability)))
            self.txtMissionHt.set_text(str(
                fmt.format(self.mission_hazard_rate)))
            self.txtPredictedHt.set_text(str(fmt.format(self.hazard_rate)))

            self.txtMMT.set_text(str(fmt.format(self.mmt)))
            self.txtMCMT.set_text(str(fmt.format(self.mcmt)))
            self.txtMPMT.set_text(str(fmt.format(self.mpmt)))

            self.txtMissionMTBF.set_text(str(
                fmt.format(self.mission_mtbf)))
            self.txtMTBF.set_text(str(fmt.format(self.mtbf)))
            self.txtMTTR.set_text(str(fmt.format(self.mttr)))

            return False

        (__, _row) = self.treeview.get_selection().get_selected()

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxFunction)
        self._app.winWorkBook.show_all()

        if _row is not None:
            _load_general_data_tab(self)
            self._load_functional_matrix()
            _load_assessment_results_tab(self)
            self._load_fmeca()

        self._app.winWorkBook.set_title(_(u"RTK Work Book: Function"))

        self.btnAddSibling.show()
        self.btnAddChild.show()
        self.btnAddMode.hide()
        self.btnRemoveFunction.show()
        self.btnRemoveMode.hide()
        self.btnCalculate.show()
        self.btnSave.show()

        #self.notebook.set_current_page(0)

        return False

    def _update_attributes(self):
        """
        Method to update the Function class attributes.
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        if _row is not None:
            self.revision_id = _model.get_value(_row, self._lst_col_order[0])
            self.function_id = _model.get_value(_row, self._lst_col_order[1])
            self.availability = _model.get_value(_row, self._lst_col_order[2])
            self.mission_availability = _model.get_value(_row,
                                                    self._lst_col_order[3])
            self.code = _model.get_value(_row, self._lst_col_order[4])
            self.cost = _model.get_value(_row, self._lst_col_order[5])
            self.mission_hazard_rate = _model.get_value(_row,
                                                        self._lst_col_order[6])
            self.hazard_rate = _model.get_value(_row, self._lst_col_order[7])
            self.mmt = _model.get_value(_row, self._lst_col_order[8])
            self.mcmt = _model.get_value(_row, self._lst_col_order[9])
            self.mpmt = _model.get_value(_row, self._lst_col_order[10])
            self.mission_mtbf = _model.get_value(_row, self._lst_col_order[11])
            self.mtbf = _model.get_value(_row, self._lst_col_order[12])
            self.mttr = _model.get_value(_row, self._lst_col_order[13])
            self.name = _model.get_value(_row, self._lst_col_order[14])
            self.remarks = _model.get_value(_row, self._lst_col_order[15])
            self.n_modes = _model.get_value(_row, self._lst_col_order[16])
            self.n_parts = _model.get_value(_row, self._lst_col_order[17])
            self.type = _model.get_value(_row, self._lst_col_order[18])
            self.parent_id = _model.get_value(_row, self._lst_col_order[19])
            self.level = _model.get_value(_row, self._lst_col_order[20])
            self.safety_critical = _model.get_value(_row,
                                                    self._lst_col_order[21])

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Hardware Object
        treeview.

        :param gtk.TreeView treeview: the Function class gtk.TreeView().
        :param gtk.gdk.Event event: the gtk.gdk.Event() that called this
                                    method (the important attribute is which
                                    mouse button was clicked).
                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if event.button == 1:
            self._treeview_row_changed(treeview, None, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, treeview, __path, __column):
        """
        Callback function to handle events for the Function class
        gtk.TreeView().  It is called whenever the Function Object treeview is
        clicked or a row is activated.  It will save the previously selected
        row in the Function class gtk.TreeView().

        :param gtk.TreeView treeview: the Function class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the activated gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model_, _row_) = treeview.get_selection().get_selected()

        if _row_ is not None:
            self.function_id = int(_model_.get_value(_row_, 1))
            self.availability = float(_model_.get_value(_row_, 2))
            self.mission_availability = float(_model_.get_value(_row_, 3))
            self.code = str(_model_.get_value(_row_, 4))
            self.cost = float(_model_.get_value(_row_, 5))
            self.mission_hazard_rate = float(_model_.get_value(_row_, 6))
            self.hazard_rate = float(_model_.get_value(_row_, 7))
            self.mmt = float(_model_.get_value(_row_, 8))
            self.mcmt = float(_model_.get_value(_row_, 9))
            self.mpmt = float(_model_.get_value(_row_, 10))
            self.mission_mtbf = float(_model_.get_value(_row_, 11))
            self.mtbf = float(_model_.get_value(_row_, 12))
            self.mttr = float(_model_.get_value(_row_, 12))
            self.name = _util.none_to_string(_model_.get_value(_row_, 14))
            self.remarks = _util.none_to_string(_model_.get_value(_row_, 15))
            self.n_modes = int(_model_.get_value(_row_, 16))
            self.n_parts = int(_model_.get_value(_row_, 17))
            self.type = int(_model_.get_value(_row_, 18))
            self.parent_id = str(_model_.get_value(_row_, 19))
            self.level = int(_model_.get_value(_row_, 20))
            self.safety_critical = int(_model_.get_value(_row_, 21))

            self.load_notebook()

        return False

    def _function_tree_edit(self, __cell, path, new_text, position, model):
        """
        Method called whenever a Function Class gtk.Treeview()
        gtk.CellRenderer() is edited.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        """

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        # Now update the associated gtk.Widget() in the Work Book with the
        # new value.  We block and unblock the signal handlers for the widgets
        # so a race condition does not ensue.
        if self._lst_col_order[position] == 4:
            self.txtCode.handler_block(self._lst_handler_id[0])
            self.txtCode.set_text(str(new_text))
            self.txtCode.handler_unblock(self._lst_handler_id[0])
        elif self._lst_col_order[position] == 14:
            _textview = self.txtName.get_child().get_child()
            _textview.handler_block(self._lst_handler_id[1])
            _textview.get_buffer().set_text(str(new_text))
            _textview.handler_unblock(self._lst_handler_id[1])
        elif self._lst_col_order[position] == 15:
            _textview = self.txtRemarks.get_child().get_child()
            _textview.handler_block(self._lst_handler_id[2])
            _textview.get_buffer().set_text(str(new_text))
            _textview.handler_unblock(self._lst_handler_id[2])

        return False

    def _add_function(self, __widget, level):
        """
        Adds a new Function to the Program's database.

        :param gtk.Widget __widget: the gtk.Widget() that called this method.
        :param int level: the level of function to add.
                          * 0 = sibling
                          * 1 = child
        """

        # Find the selected function.
        (_model_, _row_) = self.treeview.get_selection().get_selected()

        if level == 0:
            _parent_ = "-"
            if _row_ is not None:
                _prow_ = _model_.iter_parent(_row_)
                if _prow_ is not None:
                    _parent_ = _model_.get_string_from_iter(_prow_)

            _title_ = _(u"RTK - Add Sibling Functions")
            _prompt_ = _(u"How many sibling functions to add?")

        elif level == 1:
            _parent_ = "-"
            if _row_ is not None:
                _parent_ = _model_.get_string_from_iter(_row_)

            _title_ = _(u"RTK - Add Child Functions")
            _prompt_ = _(u"How many child functions to add?")

        _n_functions_ = _util.add_items(_title_, _prompt_)

        _query_ = "SELECT fld_assembly_id \
                   FROM tbl_system \
                   WHERE fld_revision_id=%d" % self.revision_id
        _assembly_id_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx)

        for i in range(_n_functions_):
            _code = str(_conf.RTK_PREFIX[2]) + ' ' + str(_conf.RTK_PREFIX[3])

            _conf.RTK_PREFIX[3] = _conf.RTK_PREFIX[3] + 1

            _values_ = (self.revision_id,
                        "New Function_" + str(i), '', _code, _parent_)

            _query_ = "INSERT INTO tbl_functions \
                       (fld_revision_id, fld_name, fld_remarks, fld_code, \
                        fld_parent_id) \
                       VALUES (%d, '%s', '%s', '%s', '%s')" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if _results_ == '' or not _results_ or _results_ is None:
                self._app.debug_log.error("function.py: Failed to add new "
                                          "function to function table.")
                return True

            if _conf.BACKEND == 'mysql':
                _query_ = "SELECT LAST_INSERT_ID()"
            elif _conf.BACKEND == 'sqlite3':
                _query_ = "SELECT seq \
                           FROM sqlite_sequence \
                           WHERE name='tbl_functions'"
            _function_id_ = self._app.DB.execute_query(_query_,
                                                       None,
                                                       self._app.ProgCnx)

            try:
                for i in range(len(_assembly_id_)):
                    _query = "INSERT INTO tbl_functional_matrix \
                              (fld_assembly_id, fld_function_id, \
                               fld_revision_id) \
                              VALUES (%d, %d, %d)" % \
                             (_assembly_id_[i][0], _function_id_[0][0],
                              self.revision_id)
                    _results = self._app.DB.execute_query(_query, None,
                                                          self._app.ProgCnx,
                                                          commit=True)
            except TypeError:
                self._app.debug_log.error("function.py: Failed to add new "
                                          "function %d to the functional "
                                          "matrix." % _function_id_[0][0])

        self.load_tree()
        self._load_functional_matrix()

        return False

    def _add_failure_mode(self, __button):
        """
        Method to add a failure mode to the FMEA/FMECA for the selected
        function.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        function.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        # Save any changes that have been made recently.
        self._save_fmeca()

        # Find the id of the next failure mode.
        _query = "SELECT seq FROM sqlite_sequence \
                  WHERE name='tbl_fmeca'"
        _last_id = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        try:
            _last_id = _last_id[0][0] + 1
        except IndexError:
            _last_id = 0

        # Insert the new failure mode.
        _query = "INSERT INTO tbl_fmeca \
                  (fld_revision_id, fld_assembly_id, \
                   fld_function_id, fld_mode_id) \
                  VALUES (%d, 0, %d, %d)" % \
                 (self._app.REVISION.revision_id,
                  self.function_id, _last_id)
        if self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                      commit=True):
            self._load_fmeca()

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _delete_function(self, __button):
        """
        Deletes the currently selected Function from the Program's MySQL or
        SQLite3 database.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        function.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        _query = "DELETE FROM tbl_functions \
                  WHERE fld_parent_id='%s'" % \
                 _model.get_string_from_iter(_row)
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            self._app.user_log.error("function.py: Failed to delete function "
                                     "from function table.")
            return True

        _query = "DELETE FROM tbl_functions \
                  WHERE fld_revision_id=%d \
                  AND fld_function_id=%d" % \
                 (self._app.REVISION.revision_id, _model.get_value(_row, 1))
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            self._app.user_log.error("function.py: Failed to delete function "
                                     "from function table.")
            return True

        self.load_tree()

        return False

    def _delete_failure_mode(self, __button):
        """
        Method to delete the currently selected failure mode from the
        FMEA/FMECA for the selected function.

        :param gtk.Button __button: the gtk.ToolButton() that called this
                                    function.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        (_model, _row) = self.tvwFMECA.get_selection().get_selected()

        _mode_id = _model.get_value(_row, 0)

        _query = "DELETE FROM tbl_fmeca \
                  WHERE fld_function_id=%d \
                  AND fld_mode_id=%d" % (self.function_id, _mode_id)
        if self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                      commit=True):
            self._save_fmeca()
            self._load_fmeca()

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def save_function(self):
        """
        Saves the Function class gtk.TreeView() information to the Program's
        MySQL or SQLite3 database.
        """

        def _save_line(model, __path, row, self):
            """
            Function to save each row in the Function class gtk.TreeModel() to
            the RTK database.

            :param gtk.TreeModel model: the Function class gtk.TreeModel().
            :param str __path: the path of the active row in the Function class
                               gtk.TreeModel().
            :param gtk.TreeIter row: the selected gtk.TreeIter() in the
                                     Function class gtk.TtreeView().
            :param rtk.Function self: the current instance of a Function class.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _values_ = (model.get_value(row, self._lst_col_order[2]),
                        model.get_value(row, self._lst_col_order[3]),
                        model.get_value(row, self._lst_col_order[4]),
                        model.get_value(row, self._lst_col_order[5]),
                        model.get_value(row, self._lst_col_order[6]),
                        model.get_value(row, self._lst_col_order[7]),
                        model.get_value(row, self._lst_col_order[8]),
                        model.get_value(row, self._lst_col_order[9]),
                        model.get_value(row, self._lst_col_order[10]),
                        model.get_value(row, self._lst_col_order[11]),
                        model.get_value(row, self._lst_col_order[12]),
                        model.get_value(row, self._lst_col_order[13]),
                        model.get_value(row, self._lst_col_order[14]),
                        model.get_value(row, self._lst_col_order[15]),
                        model.get_value(row, self._lst_col_order[16]),
                        model.get_value(row, self._lst_col_order[17]),
                        model.get_value(row, self._lst_col_order[18]),
                        model.get_value(row, self._lst_col_order[19]),
                        self._app.REVISION.revision_id,
                        model.get_value(row, self._lst_col_order[1]))

            _query = "UPDATE tbl_functions \
                      SET fld_availability=%f, fld_availability_mission=%f, \
                          fld_code='%s', fld_cost=%f, \
                          fld_failure_rate_mission=%f, \
                          fld_failure_rate_predicted=%f, fld_mmt=%f, \
                          fld_mcmt=%f, fld_mpmt=%f, fld_mtbf_mission=%f, \
                          fld_mtbf_predicted=%f, fld_mttr=%f, fld_name='%s', \
                          fld_remarks='%s', fld_total_mode_quantity=%d, \
                          fld_total_part_quantity=%d, \
                          fld_type=%d, fld_parent_id='%s' \
                      WHERE fld_revision_id=%d \
                      AND fld_function_id=%d" % _values_
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                self._app.debug_log.error("function.py: Failed to save "
                                          "function to function table.")
                return True

            return False

        _model = self.treeview.get_model()
        _model.foreach(_save_line, self)

        return False

    def _save_fmeca(self):
        """
        Saves the Function class FMECA gtk.TreeView() information to the
        Program's MySQL or SQLite3 database.
        """

        def _save_line(model, __path, row, self):
            """
            Saves each row in the Function class FMEA/FMECA gtk.TreeModel() to
            the open RTK database.

            :param gtk.TreeModel model: the Function class FMECA
                                        gtk.TreeModel().
            :param str __path: the path of the active row in the Function class
                               FMECA gtk.TreeModel().
            :param gtk.TreeIter row: the selected gtk.TreeIter() in the
                                     Function class FMECA gtk.TreeView().
            :param rtk.Function self: the current instance of a Function class.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _values_ = (model.get_value(row, self._FMECA_col_order[1]),
                        model.get_value(row, self._FMECA_col_order[2]),
                        model.get_value(row, self._FMECA_col_order[3]),
                        model.get_value(row, self._FMECA_col_order[4]),
                        model.get_value(row, self._FMECA_col_order[5]),
                        model.get_value(row, self._FMECA_col_order[6]),
                        model.get_value(row, self._FMECA_col_order[7]),
                        model.get_value(row, self._FMECA_col_order[8]),
                        model.get_value(row, self._FMECA_col_order[9]),
                        model.get_value(row, self._FMECA_col_order[10]),
                        model.get_value(row, self._FMECA_col_order[11]),
                        model.get_value(row, self._FMECA_col_order[12]),
                        model.get_value(row, self._FMECA_col_order[13]),
                        float(model.get_value(row, self._FMECA_col_order[14])),
                        float(model.get_value(row, self._FMECA_col_order[15])),
                        float(model.get_value(row, self._FMECA_col_order[16])),
                        float(model.get_value(row, self._FMECA_col_order[17])),
                        float(model.get_value(row, self._FMECA_col_order[18])),
                        model.get_value(row, self._FMECA_col_order[20]),
                        model.get_value(row, self._FMECA_col_order[21]),
                        int(model.get_value(row, self._FMECA_col_order[22])),
                        int(model.get_value(row, self._FMECA_col_order[23])),
                        model.get_value(row, self._FMECA_col_order[24]),
                        int(model.get_value(row, self._FMECA_col_order[0])))

            _query_ = "UPDATE tbl_fmeca \
                       SET fld_mode_description='%s', fld_mission_phase='%s', \
                           fld_local_effect='%s', fld_next_effect='%s', \
                           fld_end_effect='%s', fld_detection_method='%s', \
                           fld_other_indications='%s', \
                           fld_isolation_method='%s', \
                           fld_design_provisions='%s', \
                           fld_operator_actions='%s', \
                           fld_severity_class='%s', \
                           fld_hazard_rate_source='%s', \
                           fld_failure_probability='%s', \
                           fld_effect_probability=%f, \
                           fld_mode_ratio=%f, fld_mode_failure_rate=%f, \
                           fld_mode_op_time=%f, fld_mode_criticality=%f, \
                           fld_rpn_severity='%s', fld_rpn_severity_new='%s', \
                           fld_critical_item=%d, fld_single_point=%d, \
                           fld_remarks='%s' \
                       WHERE fld_mode_id=%d" % _values_
            self._app.DB.execute_query(_query_,
                                       None,
                                       self._app.ProgCnx,
                                       commit=True)

            return False

        _model_ = self.tvwFMECA.get_model()
        _model_.foreach(_save_line, self)

        return False

    def _edit_functional_matrix(self, __cell, __path, new_text, column,
                                functions):
        """
        Callback function to save changes made to the functional matrix
        gtk.TreeView().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str __path: the path to the gtk.CellRenderer() being edited.
        :param str new_text: the new text in the gtk.CellRenderer() being
                             edited.
        :param int column: the column number of the gtk.CellRenderer() being
                           edited.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model,
         _row) = self.tvwFunctionMatrix.get_selection().get_selected()

        _query = "UPDATE tbl_functional_matrix \
                  SET fld_relationship='%s' \
                  WHERE fld_assembly_id=%d \
                  AND fld_function_id=%d \
                  AND fld_revision_id=%d" % \
                 (new_text, _model.get_value(_row, 0), functions[column],
                  self._app.REVISION.revision_id)
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            self._app.debug_log.error("function.py: Failed to save Functional "
                                      "Matrix changes.")
            return True

        if new_text == 'X':
            new_text = "<span foreground='#0BB213' background='#0BB213'> X </span>"
        else:
            new_text = "<span foreground='#FD0202' background='#FD0202'>     </span>"

        _model.set_value(_row, column, new_text)

        return False

    def _callback_check(self, __check):
        """
        Callback function to retrieve and save gtk.CheckButton() changes.

        :param gtk.CheckButton __check: the gtk.CheckButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._load_functional_matrix()

        return False

    def _callback_entry(self, entry, __event, convert, index):
        """
        Callback function to retrieve and save gtk.Entry() changes.

        :param gtk.Entry entry: the gtk.Entry() that called the function.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param str convert: the data type to convert the gtk.Entry() contents.
        :param int index: the position in the Function class gtk.TreeView()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if convert == 'text':
            if index == 14:
                _textbuffer = self.txtName.get_child().get_child().get_buffer()
                _text = _textbuffer.get_text(*_textbuffer.get_bounds())
            elif index == 15:
                _textbuffer = self.txtRemarks.get_child().get_child().get_buffer()
                _text = _textbuffer.get_text(*_textbuffer.get_bounds())
            else:
                _text = entry.get_text()

        elif convert == 'int':
            _text = int(entry.get_text())

        elif convert == 'float':
            _text = float(entry.get_text().replace('$', ''))

        # Get the Function Class gtk.TreeModel() and selected gtk.TreeIter()
        # and update the Function Class gtk.TreeView().
        (_model, _row) = self.treeview.get_selection().get_selected()
        _model.set_value(_row, index, _text)

        # Update the Function class public and private attributes.
        self._update_attributes()

        return False

    def _notebook_page_switched(self, __notebook, __page, page_num):
        """
        Called whenever the Work Book gtk.Notebook() page is changed.

        :param gtk.Notebook __notebook: the Function class gtk.Notebook().
        :param gtk.Widget __page: the newly selected page widget.
        :param int page_num: the newly selected page number.
                             * 0 = General Data
                             * 1 = Functional Matrix
                             * 2 = Assessment Results
                             * 3 = FMEA/FMECA
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if page_num == 3:                   # FMEA/FMECA tab
            self.btnAddSibling.hide()
            self.btnAddChild.hide()
            self.btnAddMode.show()
            self.btnRemoveFunction.hide()
            self.btnRemoveMode.show()
            self.btnCalculate.show()
            self.btnSave.show()
            self.btnSave.set_tooltip_text(_(u"Saves changes to Functional "
                                            u"FMEA/FMECA for the selected "
                                            u"function."))
        else:
            self.btnAddSibling.show()
            self.btnAddChild.show()
            self.btnAddMode.hide()
            self.btnRemoveFunction.show()
            self.btnRemoveMode.hide()
            self.btnCalculate.show()
            self.btnSave.show()
            self.btnSave.set_tooltip_text(_(u"Saves changes to the selected "
                                            u"function."))

        return False

    def _toolbutton_pressed(self, button):
        """
        Method to react to the Function class toolbar button clicked events.

        :param gtk.ToolButton button: the gtk.ToolButton() button that was
                                      pressed.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # FMEA roll-up lower level FMEA.
        # FMEA calculate criticality.
        # V&V add new task
        # V&V assign existing task
        # Maintenance planning
        # Maintenance planning save changes to selected maintenance policy
        if self.notebook.get_current_page() == 0:    # General data tab.
            if button.get_name() == 'Save':
                self.save_function()
        elif self.notebook.get_current_page() == 1:  # Functional matrix tab.
            if button.get_name() == 'Save':
                self.save_function()
        elif self.notebook.get_current_page() == 2:  # Assessment results tab.
            if button.get_name() == 'Save':
                self.save_function()
        elif self.notebook.get_current_page() == 3:  # FMECA/FMECA tab.
            if button.get_name() == 'Save':
                self._save_fmeca()

        return False

    def calculate(self, __button=None):
        """
        Calculates active hazard rate, dormant hazard rate, software hazard
        rate, predicted hazard rate, mission MTBF, limiting MTBF, mission
        reliability, limiting reliability, total cost, cost per failure, and
        cost per operating hour.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        if _model_.iter_has_child(_row_):
            for j in range(_model_.iter_n_children(_row_)):
                self.calculate(None)
        else:
            if _conf.MODE == 'developer':
                _results_ = ([29.32, 0.000147762, 0.00014542, 5, 0.05,
                              0.4762, 0.41667, 0.08929],)
            else:
                _query = "SELECT SUM(t2.fld_cost), \
                                 SUM(t2.fld_failure_rate_predicted), \
                                 SUM(t2.fld_failure_rate_mission), \
                                 COUNT(t2.fld_assembly_id), \
                                 SUM(1.0 / fld_mpmt), SUM(1.0 / fld_mcmt), \
                                 SUM(1.0 / mttr), SUM(1.0 / fld_mmt) \
                          FROM tbl_system AS t2 \
                          INNER JOIN tbl_functional_matrix AS t1 \
                          ON t2.fld_assembly_id = t1.fld_assembly_id \
                          WHERE t1.fld_function_id=%d \
                          AND t2.fld_part=1" % (_model_.get_value(_row_, 1),)
                _results_ = self._app.DB.execute_query(_query, None,
                                                       self._app.ProgCnx)

                if _results_ == '' or not _results_ or _results_ is None:
                    return True

            self.cost = float(_results_[0][0])
            self.hazard_rate = float(_results_[0][1])
            self.mission_hazard_rate = float(_results_[0][2])
            self.n_parts = int(_results_[0][3])

            try:
                self.mpmt = 1.0 / float(_results_[0][4])
            except ZeroDivisionError:
                self.mpmt = 0.0

            try:
                self.mcmt = 1.0 / float(_results_[0][5])
            except ZeroDivisionError:
                self.mcmt = 0.0

            try:
                self.mttr = 1.0 / float(_results_[0][6])
            except ZeroDivisionError:
                self.mttr = 0.0

            try:
                self.mmt = 1.0 / float(_results_[0][7])
            except ZeroDivisionError:
                self.mmt = 0.0

            # Calculate the logistics MTBF.
            try:
                self.mtbf = 1.0 / self.hazard_rate
            except ZeroDivisionError:
                self.mtbf = 0.0
                self._app.user_log.error(_("Attempted to divide by zero when "
                                           "calculating function logistics "
                                           "MTBF.\n"
                                           "function id %s: lambdap = %f") %
                                         (self._app.FUNCTION.function_id,
                                          self.hazard_rate))

            # Calculate the mission MTBF.
            try:
                self.mission_mtbf = 1.0 / self.mission_hazard_rate
            except ZeroDivisionError:
                self.mission_mtbf = 0.0
                self._app.user_log.error(_("Attempted to divide by zero when "
                                           "calculating function mission "
                                           "MTBF.\n"
                                           "function id %s: lambdap = %f") %
                                         (self._app.FUNCTION.function_id,
                                          self.mission_hazard_rate))

            # Calculate the logistics availability.
            try:
                self.availability = self.mtbf / (self.mtbf + self.mttr)
            except ZeroDivisionError:
                self.availability = 1.0
            except OverflowError:
                self.availability = 1.0

            # Calculate mission availability.
            try:
                self.mission_availability = self.mission_mtbf / \
                    (self.mission_mtbf + self.mttr)
            except ZeroDivisionError:
                self.mission_availability = 1.0
            except OverflowError:
                self.mission_availability = 1.0

        _model_.set_value(_row_, self._lst_col_order[2], self.availability)
        _model_.set_value(_row_, self._lst_col_order[3],
                          self.mission_availability)
        _model_.set_value(_row_, self._lst_col_order[5], self.cost)
        _model_.set_value(_row_, self._lst_col_order[6],
                          self.mission_hazard_rate)
        _model_.set_value(_row_, self._lst_col_order[7], self.hazard_rate)
        _model_.set_value(_row_, self._lst_col_order[8], self.mmt)
        _model_.set_value(_row_, self._lst_col_order[9], self.mcmt)
        _model_.set_value(_row_, self._lst_col_order[10], self.mpmt)
        _model_.set_value(_row_, self._lst_col_order[11], self.mission_mtbf)
        _model_.set_value(_row_, self._lst_col_order[12], self.mtbf)
        _model_.set_value(_row_, self._lst_col_order[13], self.mttr)
        _model_.set_value(_row_, self._lst_col_order[17], self.n_parts)

        self.load_notebook()

        return False
