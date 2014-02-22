#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related
to the revision of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2014 Andrew Rowland'

# -*- coding: utf-8 -*-
#
#       revision.py is part of the RTK Project
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

import pango

# Import other RTK modules.
import configuration as _conf
import widgets as _widg

from _assistants_.adds import AddRevision

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Revision:
    """ This is the REVISION Class for the RTK Project. """

    def __init__(self, application):
        """
        Initializes the REVISION Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        # Define private REVISION class attributes.
        self._app = application
        self._int_mission_id = -1

        # Define private REVISION class dictionary attributes.

        # For mission information.  Mission ID is the key.
        # The value is a list:
        # [Mission Time, Time Units, Mission Name]
        self._dic_missions = {}

        # For environmental profile information.  Environment noun name is the
        # key.
        # The value is a list:
        # [Condition ID, Phase Name, Measurement Units, Minimum Value,
        #  Maximum Value, Mean Value, Variance]
        self._dic_environments = {}

        # Define private REVISION class list attributes.

        # Define public REVISION class attributes.
        self.revision_id = 0
        self.name = ''
        self.n_parts = 0
        self.cost = 0.0
        self.cost_per_failure = 0.0
        self.cost_per_hour = 0.0
        self.active_hazard_rate = 0.0
        self.dormant_hazard_rate = 0.0
        self.software_hazard_rate = 0.0
        self.hazard_rate = 0.0
        self.mission_hazard_rate = 0.0
        self.mtbf = 0.0
        self.mission_mtbf = 0.0
        self.reliability = 0.0
        self.mission_reliability = 0.0
        self.mpmt = 0.0
        self.mcmt = 0.0
        self.mttr = 0.0
        self.mmt = 0.0
        self.availability = 0.0
        self.mission_availability = 0.0
        self.remarks = ''
        self.code = ''

        # Create the main REVISION class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Revision', 0, self._app,
                                                    None, _conf.RTK_COLORS[0],
                                                    _conf.RTK_COLORS[1])

        # General data tab widgets.
        self.txtCode = _widg.make_entry()
        self.txtName = _widg.make_entry()
        self.txtTotalCost = _widg.make_entry(editable=False)
        self.txtCostFailure = _widg.make_entry(editable=False)
        self.txtCostHour = _widg.make_entry(editable=False)
        self.txtPartCount = _widg.make_entry(editable=False)
        self.txtRemarks = gtk.TextBuffer()

        # Usage profile tab widgets.
        self.btnAddMission = _widg.make_button(_width_=40, _image_='add')
        self.btnRemoveMission = _widg.make_button(_width_=40, _image_='remove')
        self.btnAddPhase = _widg.make_button(_width_=40, _image_='add')
        self.btnRemovePhase = _widg.make_button(_width_=40, _image_='remove')
        self.btnAddEnvironment = _widg.make_button(_width_=40, _image_='add')
        self.btnRemoveEnvironment = _widg.make_button(_width_=40,
                                                      _image_='remove')
        self.cmbMission = _widg.make_combo()
        self.cmbTimeUnit = _widg.make_combo(_width_=100)
        self.tvwMissionProfile = gtk.TreeView()
        self.tvwEnvironmentProfile = gtk.TreeView()
        self.txtMission = _widg.make_entry()
        self.txtMissionTime = _widg.make_entry(_width_=90)

        # Failure definition tab widgets.
        self.btnAddDefinition = _widg.make_button(_width_=40, _image_='add')
        self.btnRemoveDefinition = _widg.make_button(_width_=40,
                                                     _image_='remove')
        self.tvwFailureDefinitions = gtk.TreeView()

        # Assessment results tab widgets.
        self.txtActiveHt = _widg.make_entry(_width_=100, editable=False,
                                            bold=True)
        self.txtDormantHt = _widg.make_entry(_width_=100, editable=False,
                                             bold=True)
        self.txtSoftwareHt = _widg.make_entry(_width_=100, editable=False,
                                              bold=True)
        self.txtPredictedHt = _widg.make_entry(_width_=100, editable=False,
                                               bold=True)
        self.txtMissionHt = _widg.make_entry(_width_=100, editable=False,
                                             bold=True)
        self.txtMTBF = _widg.make_entry(_width_=100, editable=False, bold=True)
        self.txtMissionMTBF = _widg.make_entry(_width_=100, editable=False,
                                               bold=True)
        self.txtReliability = _widg.make_entry(_width_=100, editable=False,
                                               bold=True)
        self.txtMissionRt = _widg.make_entry(_width_=100, editable=False,
                                             bold=True)
        self.txtMPMT = _widg.make_entry(_width_=100, editable=False, bold=True)
        self.txtMCMT = _widg.make_entry(_width_=100, editable=False, bold=True)
        self.txtMTTR = _widg.make_entry(_width_=100, editable=False, bold=True)
        self.txtMMT = _widg.make_entry(_width_=100, editable=False, bold=True)
        self.txtAvailability = _widg.make_entry(_width_=100, editable=False,
                                                bold=True)
        self.txtMissionAt = _widg.make_entry(_width_=100, editable=False,
                                             bold=True)

        # Put it all together.
        toolbar = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxRevision = gtk.VBox()
        self.vbxRevision.pack_start(toolbar, expand=False)
        self.vbxRevision.pack_start(self.notebook)

    def create_tree(self):
        """
        Method to create the REVISION gtk.TreeView() and connects it to
        callback functions to handle editting.
        """

        self.treeview.set_tooltip_text(_(u"Displays the list of revisions."))
        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)
        self.treeview.connect('button_press_event', self._treeview_clicked)

        _scrollwindow_ = gtk.ScrolledWindow()
        _scrollwindow_.add(self.treeview)

        return _scrollwindow_

    def _create_toolbar(self):
        """
        Method to create the gtk.ToolBar() for the REVISION class work book.
        """

        _toolbar_ = gtk.Toolbar()

        _position_ = 0

        # Add revision button.
        _button_ = gtk.ToolButton()
        _button_.set_tooltip_text(_(u"Adds a new revision to the RTK Program Database."))
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button_.set_icon_widget(_image_)
        _button_.connect('clicked', AddRevision, self._app)
        _toolbar_.insert(_button_, _position_)
        _position_ += 1

        # Delete revision button
        _button_ = gtk.ToolButton()
        _button_.set_tooltip_text(_(u"Removes the currently selected revision from the RTK Program Database."))
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button_.set_icon_widget(_image_)
        _button_.connect('clicked', self.delete_revision)
        _toolbar_.insert(_button_, _position_)
        _position_ += 1

        _toolbar_.insert(gtk.SeparatorToolItem(), _position_)
        _position_ += 1

        # Calculate revision _button_
        _button_ = gtk.ToolButton()
        _button_.set_tooltip_text(_(u"Calculate the currently selected revision."))
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        _button_.set_icon_widget(_image_)
        _button_.connect('clicked', self.calculate)
        _toolbar_.insert(_button_, _position_)
        _position_ += 1

        _toolbar_.insert(gtk.SeparatorToolItem(), _position_)
        _position_ += 1

        # Save revision _button_.
        _button_ = gtk.ToolButton()
        _button_.set_tooltip_text(_(u"Saves the currently selected revision to the RTK Program Database."))
        _image_ = gtk.Image()
        _image_.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button_.set_icon_widget(_image_)
        _button_.connect('clicked', self.save_revision)
        _toolbar_.insert(_button_, _position_)
        _position_ += 1

        _toolbar_.show()

        return _toolbar_

    def _create_notebook(self):
        """
        Method to create the REVISION class gtk.Notebook().
        """

        def _create_general_data_tab(self, notebook):
            """
            Function to create the REVISION class gtk.Notebook() page for
            displaying general data about the selected REVISION.

            Keyword Arguments:
            self     -- the current instance of a REVISION class.
            notebook -- the gtk.Notebook() to add the general data tab.
            """

            _labels_ = [_(u"Revision Code:"), _(u"Revision Name:"),
                        _(u"Total Cost:"), _(u"Cost/Failure:"),
                        _(u"Cost/Hour:"), _(u"Total Part Count:"),
                        _(u"Remarks:")]

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _fraGeneralData_ = _widg.make_frame(_label_=_(u"General Information"))
            _fraGeneralData_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)

            _fxdGeneralData_ = gtk.Fixed()

            _scwGeneralData_ = gtk.ScrolledWindow()
            _scwGeneralData_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            _scwGeneralData_.add_with_viewport(_fxdGeneralData_)

            _fraGeneralData_.add(_scwGeneralData_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _max1_ = 0
            _max2_ = 0
            (_max1_, _y_pos_) = _widg.make_labels(_labels_,
                                                  _fxdGeneralData_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 25

            self.txtCode.set_tooltip_text(_("A unique code for the selected revision."))
            self.txtCode.connect('focus-out-event', self._callback_entry, 22)
            _fxdGeneralData_.put(self.txtCode, _x_pos_, _y_pos_[0])

            self.txtName.set_tooltip_text(_("The name of the selected revision."))
            self.txtName.connect('focus-out-event', self._callback_entry, 17)
            _fxdGeneralData_.put(self.txtName, _x_pos_, _y_pos_[1])

            self.txtTotalCost.set_tooltip_text(_("Displays the total cost of the selected revision."))
            _fxdGeneralData_.put(self.txtTotalCost, _x_pos_, _y_pos_[2])

            self.txtCostFailure.set_tooltip_text(_("Displays the cost per failure of the selected revision."))
            _fxdGeneralData_.put(self.txtCostFailure, _x_pos_, _y_pos_[3])

            self.txtCostHour.set_tooltip_text(_("Displays the failure cost per operating hour for the selected revision."))
            _fxdGeneralData_.put(self.txtCostHour, _x_pos_, _y_pos_[4])

            self.txtPartCount.set_tooltip_text(_("Displays the total part count for the selected revision."))
            _fxdGeneralData_.put(self.txtPartCount, _x_pos_, _y_pos_[5])

            textview = _widg.make_text_view(buffer_=self.txtRemarks, width=400)
            textview.set_tooltip_text(_(u"Enter any remarks associated with the selected revision."))
            _view_ = textview.get_children()[0].get_children()[0]
            _view_.connect('focus-out-event', self._callback_entry, 20)
            _fxdGeneralData_.put(textview, _x_pos_, _y_pos_[6])

            _fxdGeneralData_.show_all()

            # Insert the tab.
            _label_ = gtk.Label()
            _heading_ = _("General\nData")
            _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(u"Displays general information for the selected revision."))
            notebook.insert_page(_fraGeneralData_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        def _create_usage_profile_tab(self, notebook):
            """
            Function to create the REVISION class gtk.Notebook() page for
            displaying usage profiles for the selected REVISION.

            Keyword Arguments:
            self     -- the current instance of a REVISION class.
            notebook -- the gtk.Notebook() to add the general data tab.
            """

            _labels_ = [_(u"Mission:"), _(u"Mission Time:")]
            _units_ = [[_(u"Seconds")], [_(u"Minutes")],
                       [_(u"Hours")], [_(u"Cycles")]]
            _mission_headings_ = [_(u"Phase ID"), _(u"Start"), _(u"End"),
                                  _(u"Code"), _(u"Description")]
            _environ_headings_ = [_(u"Condition ID"),
                                  _(u"Environmental\nCondition"),
                                  _(u"Mission\nPhase"), _(u"Units"),
                                  _(u"Minimum"), _(u"Maximum"), _(u"Mean"),
                                  _(u"Variance")]

            # Create the mission profile gtk.TreeView().
            self.tvwMissionProfile.set_tooltip_text(_(u"Displays the currently selected mission profile."))
            _model_ = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING)
            self.tvwMissionProfile.set_model(_model_)

            for i in range(len(_mission_headings_)):
                cell = gtk.CellRendererText()
                cell.set_property('editable', 1)
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                cell.set_property('yalign', 0.1)
                cell.connect('edited', _widg.edit_tree, i, _model_)
                label = gtk.Label()
                label.set_line_wrap(True)
                label.set_alignment(xalign=0.5, yalign=0.5)
                label.set_justify(gtk.JUSTIFY_CENTER)
                label.set_markup("<span weight='bold'>" + _mission_headings_[i] + "</span>")
                label.set_use_markup(True)
                label.show_all()
                column = gtk.TreeViewColumn()
                column.set_widget(label)
                column.set_visible(True)
                column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
                column.pack_start(cell, True)
                column.set_attributes(cell, text=i)
                self.tvwMissionProfile.append_column(column)

            self.tvwMissionProfile.get_column(0).set_visible(False)

            # Create the environmental profile gtk.TreeView().
            self.tvwEnvironmentProfile.set_tooltip_text(_(u"Displays the environmental profile for the selected mission."))
            _model_ = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                                    gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
            self.tvwEnvironmentProfile.set_model(_model_)

            _query_ = "SELECT fld_condition_name \
                       FROM tbl_environmental_conditions"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)

            cell = gtk.CellRendererText()
            cell.set_property('editable', 0)
            column = gtk.TreeViewColumn(_environ_headings_[0])
            column.set_visible(False)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=0)
            self.tvwEnvironmentProfile.append_column(column)

            cell = gtk.CellRendererCombo()
            cellmodel = gtk.ListStore(gobject.TYPE_STRING)
            cellmodel.append([""])
            for i in range(len(_results_)):
                cellmodel.append([_results_[i][0]])
            cell.set_property('editable', 1)
            cell.set_property('has-entry', True)
            cell.set_property('model', cellmodel)
            cell.set_property('text-column', 0)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', _widg.edit_tree, 1, _model_)
            label = gtk.Label()
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_markup("<span weight='bold'>" + _environ_headings_[1] + "</span>")
            label.set_use_markup(True)
            label.show_all()
            column = gtk.TreeViewColumn()
            column.set_widget(label)
            column.set_visible(True)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=1)
            self.tvwEnvironmentProfile.append_column(column)

            cell = gtk.CellRendererCombo()
            cellmodel = gtk.ListStore(gobject.TYPE_STRING)
            cell.set_property('editable', 1)
            cell.set_property('has-entry', False)
            cell.set_property('model', cellmodel)
            cell.set_property('text-column', 0)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', _widg.edit_tree, 2, _model_)
            label = gtk.Label()
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_markup("<span weight='bold'>" + _environ_headings_[2] + "</span>")
            label.set_use_markup(True)
            label.show_all()
            column = gtk.TreeViewColumn()
            column.set_widget(label)
            column.set_visible(True)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=2)
            self.tvwEnvironmentProfile.append_column(column)

            for i in range(3, 8):
                cell = gtk.CellRendererText()
                cell.set_property('editable', 1)
                cell.set_property('wrap-width', 250)
                cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                cell.set_property('yalign', 0.1)
                cell.connect('edited', _widg.edit_tree, i, _model_)
                label = gtk.Label()
                label.set_line_wrap(True)
                label.set_alignment(xalign=0.5, yalign=0.5)
                label.set_justify(gtk.JUSTIFY_CENTER)
                label.set_markup("<span weight='bold'>" + _environ_headings_[i] + "</span>")
                label.set_use_markup(True)
                label.show_all()
                column = gtk.TreeViewColumn()
                column.set_widget(label)
                column.set_visible(True)
                column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
                column.pack_start(cell, True)
                column.set_attributes(cell, text=i)
                self.tvwEnvironmentProfile.append_column(column)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbxUsage_ = gtk.HBox()

            # Mission description containers.
            _vbxMissionOuter_ = gtk.VBox()

            _vbxMissionInner_ = gtk.VBox()

            _bbxMission_ = gtk.HButtonBox()
            _bbxMission_.set_layout(gtk.BUTTONBOX_START)
            _vbxMissionInner_.pack_start(_bbxMission_)

            _fxdMission_ = gtk.Fixed()
            _vbxMissionInner_.pack_start(_fxdMission_, expand=False)

            _fraMission_ = _widg.make_frame(_label_=_(u"Mission Description"))
            _fraMission_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraMission_.add(_vbxMissionInner_)

            _vbxMissionOuter_.pack_start(_fraMission_, expand=False)

            # Mission profile containers.
            _vbxMissionProfile_ = gtk.VBox()

            _bbxMissionProfile_ = gtk.HButtonBox()
            _bbxMissionProfile_.set_layout(gtk.BUTTONBOX_START)
            _vbxMissionProfile_.pack_start(_bbxMissionProfile_, expand=False)

            _scwMissionProfile_ = gtk.ScrolledWindow()
            _scwMissionProfile_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

            _vbxMissionProfile_.pack_end(_scwMissionProfile_, expand=True)

            _fraMissionProfile_ = _widg.make_frame(_label_=_(u"Mission Profile"))
            _fraMissionProfile_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraMissionProfile_.add(_vbxMissionProfile_)

            _vbxMissionOuter_.pack_end(_fraMissionProfile_, expand=True)

            _hbxUsage_.pack_start(_vbxMissionOuter_)

            # Environmental profile containers.
            _vbxEnvironment_ = gtk.VBox()

            _fraEnvironment_ = _widg.make_frame(_label_=_(u"Environmental Profile"))
            _fraEnvironment_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraEnvironment_.add(_vbxEnvironment_)

            _bbxEnvironment_ = gtk.HButtonBox()
            _bbxEnvironment_.set_layout(gtk.BUTTONBOX_START)

            _vbxEnvironment_.pack_start(_bbxEnvironment_, expand=False)

            _scwEnvironment_ = gtk.ScrolledWindow()
            _scwEnvironment_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

            _vbxEnvironment_.pack_end(_scwEnvironment_, expand=True)

            _hbxUsage_.pack_end(_fraEnvironment_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display usage information.          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # Mission description widgets.
            self.btnAddMission.set_tooltip_text(_(u"Adds a new mission to the selected program."))
            self.btnAddMission.connect('released', self._add_mission)
            _bbxMission_.pack_start(self.btnAddMission)

            self.btnRemoveMission.set_tooltip_text(_(u"Removes the currently selected mission from the program."))
            self.btnRemoveMission.connect('released', self._delete_mission)
            _bbxMission_.pack_end(self.btnRemoveMission)

            _max1_ = 0
            _max2_ = 0
            (_max1_, _y_pos_) = _widg.make_labels(_labels_, _fxdMission_, 5, 5,
                                                  y_inc=35)
            _x_pos_ = max(_max1_, _max2_) + 20

            self.cmbMission.set_tooltip_text(_(u"Selects and displays the current mission profile."))
            self.cmbMission.connect('changed', self._callback_combo, 0)
            _fxdMission_.put(self.cmbMission, _x_pos_, _y_pos_[0])

            self.txtMission.set_tooltip_text(_(u"Displays the mission name."))
            self.txtMission.connect('focus-out-event',
                                    self._callback_entry, 100)
            _fxdMission_.put(self.txtMission, _x_pos_+205, _y_pos_[0])

            self.txtMissionTime.set_tooltip_text(_(u"Displays the total mission time."))
            self.txtMissionTime.connect('focus-out-event',
                                        self._callback_entry, 101)
            _fxdMission_.put(self.txtMissionTime, _x_pos_, _y_pos_[1])

            self.cmbTimeUnit.set_tooltip_text(_(u"Select and displays the time units for the selected mission."))
            _widg.load_combo(self.cmbTimeUnit, _units_)
            self.cmbTimeUnit.connect('changed', self._callback_combo, 1)
            _fxdMission_.put(self.cmbTimeUnit, _x_pos_+100, _y_pos_[1])

            # Mission profile widgets.
            self.btnAddPhase.set_tooltip_text(_(u"Adds a new phase to the selected mission."))
            self.btnAddPhase.connect('released', self._add_mission_phase)
            _bbxMissionProfile_.pack_start(self.btnAddPhase)

            self.btnRemovePhase.set_tooltip_text(_(u"Removes the currently selected phase from the mission."))
            self.btnRemovePhase.connect('released', self._delete_mission_phase)
            _bbxMissionProfile_.pack_end(self.btnRemovePhase)

            _scwMissionProfile_.add(self.tvwMissionProfile)

            # Environmental profile widgets.
            self.btnAddEnvironment.set_tooltip_text(_(u"Adds a new environmental condition to the environmental profile."))
            self.btnAddEnvironment.connect('released', self._add_environment)
            _bbxEnvironment_.pack_start(self.btnAddEnvironment)

            self.btnRemoveEnvironment.set_tooltip_text(_(u"Removes the currently selected environmental condition from the environmental profile."))
            self.btnRemoveEnvironment.connect('released',
                                              self._delete_environment)
            _bbxEnvironment_.pack_end(self.btnRemoveEnvironment)

            _scwEnvironment_.add(self.tvwEnvironmentProfile)

            # Insert the tab.
            _label_ = gtk.Label()
            _heading_ = _("Usage\nProfiles")
            _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(u"Displays usage profiles for the selected revision."))
            notebook.insert_page(_hbxUsage_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        def _create_failure_definition_tab(self, notebook):
            """
            Function to create the REVISION class gtk.Notebook() page for
            displaying failure definitions for the selected REVISION.

            Keyword Arguments:
            self     -- the current instance of a REVISION class.
            notebook -- the gtk.Notebook() to add the general data tab.
            """

            _model_ = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
            self.tvwFailureDefinitions.set_model(_model_)

            cell = gtk.CellRendererText()
            cell.set_property('editable', 0)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', _widg.edit_tree, 0, _model_)
            label = gtk.Label()
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_markup("<span weight='bold'>Definition\nNumber</span>")
            label.set_use_markup(True)
            label.show_all()
            column = gtk.TreeViewColumn()
            column.set_widget(label)
            column.set_visible(True)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=0)
            self.tvwFailureDefinitions.append_column(column)

            cell = _widg.CellRendererML()
            cell.set_property('editable', 1)
            cell.set_property('wrap-width', 250)
            cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            cell.set_property('yalign', 0.1)
            cell.connect('edited', _widg.edit_tree, 1, _model_)
            label = gtk.Label()
            label.set_line_wrap(True)
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_markup("<span weight='bold'>Failure Definition</span>")
            label.set_use_markup(True)
            label.show_all()
            column = gtk.TreeViewColumn()
            column.set_widget(label)
            column.set_visible(True)
            column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            column.pack_start(cell, True)
            column.set_attributes(cell, text=1)
            self.tvwFailureDefinitions.append_column(column)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _vbxFailureDefs_ = gtk.VBox()

            _bbxFailureDefs_ = gtk.HButtonBox()
            _bbxFailureDefs_.set_layout(gtk.BUTTONBOX_START)
            _vbxFailureDefs_.pack_start(_bbxFailureDefs_, expand=False)

            _scwFailureDefs_ = gtk.ScrolledWindow()
            _scwFailureDefs_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

            _fraFailureDefs_ = _widg.make_frame(_label_=_(u"Failure Definitions List"))
            _fraFailureDefs_.set_shadow_type(gtk.SHADOW_IN)
            _fraFailureDefs_.add(_scwFailureDefs_)

            _vbxFailureDefs_.pack_end(_fraFailureDefs_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Now place the wdigets used to display failure definitions.    #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            self.btnAddDefinition.set_tooltip_text(_(u"Adds a new failure definition to the list."))
            self.btnAddDefinition.connect('released',
                                          self._add_failure_definition)
            _bbxFailureDefs_.pack_start(self.btnAddDefinition)

            self.btnRemoveDefinition.set_tooltip_text(_(u"Removes the currently selected failure definition from the list."))
            self.btnRemoveDefinition.connect('released',
                                             self._delete_failure_definition)
            _bbxFailureDefs_.pack_end(self.btnRemoveDefinition)

            _scwFailureDefs_.add(self.tvwFailureDefinitions)

            # Insert the tab.
            _label_ = gtk.Label()
            _heading_ = _(u"Failure\nDefinitions")
            _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(u"Displays usage profiles for the selected revision."))
            notebook.insert_page(_vbxFailureDefs_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        def _create_assessment_results_tab(self, notebook):
            """
            Method to create the Assessment Results gtk.Notebook tab and
            populate is with the appropriate widgets for the REVISION object.
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbxResults_ = gtk.HBox()

            # Reliability results containers.
            _fxdReliability_ = gtk.Fixed()

            _scwReliability_ = gtk.ScrolledWindow()
            _scwReliability_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            _scwReliability_.add_with_viewport(_fxdReliability_)

            _fraReliability_ = _widg.make_frame(_label_=_(u"Reliability Results"))
            _fraReliability_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraReliability_.add(_scwReliability_)

            _hbxResults_.pack_start(_fraReliability_)

            # Maintainability results containters.
            _fxdMaintainability_ = gtk.Fixed()

            _scwMaintainability_ = gtk.ScrolledWindow()
            _scwMaintainability_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            _scwMaintainability_.add_with_viewport(_fxdMaintainability_)

            _fraMaintainability_ = _widg.make_frame(_label_=_(u"Maintainability Results"))
            _fraMaintainability_.set_shadow_type(gtk.SHADOW_NONE)
            _fraMaintainability_.add(_scwMaintainability_)

            _hbxResults_.pack_start(_fraMaintainability_)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display assessment results.         #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

            # Reliability results widgets.
            _labels_ = [_(u"Active Failure Intensity [\u039B(t)]:"),
                        _(u"Dormant \u039B(t):"),
                        _(u"Software \u039B(t):"),
                        _(u"Predicted \u039B(t):"),
                        _(u"Mission \u039B(t):"),
                        _(u"Mean Time Between Failure [MTBF]:"),
                        _(u"Mission MTBF:"), _(u"Reliability [R(t)]:"),
                        _(u"Mission R(t):")]

            _max1_ = 0
            _max2_ = 0
            (_max1_, _y_pos_) = _widg.make_labels(_labels_,
                                                  _fxdReliability_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 25

            self.txtActiveHt.set_tooltip_text(_(u"Displays the active failure intensity for the selected revision."))
            _fxdReliability_.put(self.txtActiveHt, _x_pos_, _y_pos_[0])

            self.txtDormantHt.set_tooltip_text(_(u"Displays the dormant failure intensity for the selected revision."))
            _fxdReliability_.put(self.txtDormantHt, _x_pos_, _y_pos_[1])

            self.txtSoftwareHt.set_tooltip_text(_(u"Displays the software failure intensity for the selected revision."))
            _fxdReliability_.put(self.txtSoftwareHt, _x_pos_, _y_pos_[2])

            self.txtPredictedHt.set_tooltip_text(_(u"Displays the predicted failure intensity for the selected revision.  This is the sum of the active, dormant, and software hazard rates."))
            _fxdReliability_.put(self.txtPredictedHt, _x_pos_, _y_pos_[3])

            self.txtMissionHt.set_tooltip_text(_(u"Displays the mission failure intensity for the selected revision."))
            _fxdReliability_.put(self.txtMissionHt, _x_pos_, _y_pos_[4])

            self.txtMTBF.set_tooltip_text(_(u"Displays the limiting mean time between failure (MTBF) for the selected revision."))
            _fxdReliability_.put(self.txtMTBF, _x_pos_, _y_pos_[5])

            self.txtMissionMTBF.set_tooltip_text(_(u"Displays the mission mean time between failure (MTBF) for the selected revision."))
            _fxdReliability_.put(self.txtMissionMTBF, _x_pos_, _y_pos_[6])

            self.txtReliability.set_tooltip_text(_(u"Displays the limiting reliability for the selected revision."))
            _fxdReliability_.put(self.txtReliability, _x_pos_, _y_pos_[7])

            self.txtMissionRt.set_tooltip_text(_(u"Displays the mission reliability for the selected revision."))
            _fxdReliability_.put(self.txtMissionRt, _x_pos_, _y_pos_[8])

            _fxdReliability_.show_all()

            # Maintainability results widgets.
            _labels_ = [_(u"Mean Preventive Maintenance Time [MPMT]:"),
                        _(u"Mean Corrective Maintenance Time [MCMT]:"),
                        _(u"Mean Time to Rrepair [MTTR]:"),
                        _(u"Mean Maintenance Time [MMT]:"),
                        _(u"Availability [A(t)]:"), _(u"Mission A(t):")]

            _max1_ = 0
            _max2_ = 0
            (_max1_, _y_pos_) = _widg.make_labels(_labels_,
                                                  _fxdMaintainability_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 25

            self.txtMPMT.set_tooltip_text(_(u"Displays the mean preventive maintenance time (MPMT) for the selected revision."))
            _fxdMaintainability_.put(self.txtMPMT, _x_pos_, _y_pos_[0])

            self.txtMCMT.set_tooltip_text(_(u"Displays the mean corrective maintenance time (MCMT) for the selected revision."))
            _fxdMaintainability_.put(self.txtMCMT, _x_pos_, _y_pos_[1])

            self.txtMTTR.set_tooltip_text(_(u"Displays the mean time to repair (MTTR) for the selected revision."))
            _fxdMaintainability_.put(self.txtMTTR, _x_pos_, _y_pos_[2])

            self.txtMMT.set_tooltip_text(_(u"Displays the mean maintenance time (MMT) for the selected revision.  This includes preventive and corrective maintenance."))
            _fxdMaintainability_.put(self.txtMMT, _x_pos_, _y_pos_[3])

            self.txtAvailability.set_tooltip_text(_(u"Displays the limiting availability for the selected revision."))
            _fxdMaintainability_.put(self.txtAvailability, _x_pos_, _y_pos_[4])

            self.txtMissionAt.set_tooltip_text(_(u"Displays the mission availability for the selected revision."))
            _fxdMaintainability_.put(self.txtMissionAt, _x_pos_, _y_pos_[5])

            _fxdMaintainability_.show_all()

            # Insert the tab.
            _label_ = gtk.Label()
            _label_.set_markup("<span weight='bold'>Assessment\nResults</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.show_all()
            _label_.set_tooltip_text(_(u"Displays reliability, maintainability, and availability assessment results for the selected revision."))
            notebook.insert_page(_hbxResults_,
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
        _create_usage_profile_tab(self, _notebook_)
        _create_failure_definition_tab(self, _notebook_)
        _create_assessment_results_tab(self, _notebook_)

        return _notebook_

    def load_tree(self):
        """
        Loads the REVISION Object gtk.TreeModel with revision information.
        This information can be stored either in a MySQL or SQLite3
        database.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _query_ = "SELECT * FROM tbl_revisions"
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if _results_ == '' or not _results_ or _results_ is None:
            return True

        _n_records_ = len(_results_)

        _model_.clear()
        for i in range(_n_records_):
            _model_.append(None, _results_[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _model_.get_iter_root() is not None:
            _path_ = _model_.get_path(_model_.get_iter_root())
            _column_ = self.treeview.get_column(0)
            self.treeview.row_activated(_path_, _column_)

        # Try to retrieve the Revision ID attribute.
        try:
            self.revision_id = _model_.get_value(_row_, 0)
        except TypeError:
            self.revision_id = 0

        return False

    def _load_mission_profile(self):
        """
        Method to load the mission profile gtk.TreeView().
        """

        # Load the mission profile tree.
        _model_ = self.tvwMissionProfile.get_model()
        _model_.clear()

        _mission_ = self.cmbMission.get_active() - 1
        _query_ = "SELECT fld_phase_id, fld_phase_start, fld_phase_end, \
                          fld_phase_name, fld_phase_description \
                   FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d" % _mission_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if _results_ == '' or not _results_ or _results_ is None:
            self._app.debug_log.error("revision.py: Failed to load mission profile.")
        else:
            _n_phases_ = len(_results_)
            for i in range(_n_phases_):
                _model_.append(_results_[i])

        # Set the selected mission to the first in the list and then load the
        # remaining widgets appropriately.
        try:
            self.txtMission.set_text(str(self._dic_missions[_mission_][2]))
            self.txtMissionTime.set_text(str(self._dic_missions[_mission_][0]))
            self.cmbTimeUnit.set_active(self._dic_missions[_mission_][1])
        except KeyError:
            self.txtMissionTime.set_text("0.0")
            self.cmbTimeUnit.set_active(0)

        return False

    def _load_environmental_profile(self):
        """
        Method to load the environmental profile gtk.TreeView().
        """

        # Load the mission phase gtk.CellRendererCombo in the environmental
        # profile gtk.TreeView().
        _dic_mission_phases = {}

        _mission_ = self.cmbMission.get_active() - 1
        _query_ = "SELECT fld_phase_name \
                   FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d" % _mission_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        _phases_ = len(_results_)
        _column_ = self.tvwEnvironmentProfile.get_column(2)
        _cell_ = _column_.get_cell_renderers()
        _cellmodel_ = _cell_[0].get_property('model')
        _cellmodel_.clear()
        _cellmodel_.append(["All"])
        _dic_mission_phases[0] = "All"
        for i in range(_phases_):
            _cellmodel_.append([_results_[i][0]])
            _dic_mission_phases[i + 1] = _results_[i][0]

        # Load the environmental profile gtk.TreeView().
        _model_ = self.tvwEnvironmentProfile.get_model()
        _model_.clear()

        _query_ = "SELECT fld_condition_id, fld_condition_name, \
                          fld_phase_id, fld_units, fld_minimum, \
                          fld_maximum, fld_mean, fld_variance \
                   FROM tbl_environmental_profile \
                   WHERE fld_mission_id=%d" % _mission_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if _results_ == '' or not _results_:
            self._app.debug_log.error("revision.py: Failed to retrieve environmental profile for mission %d." % _mission_)
            return True

        _n_conditions_ = len(_results_)
        for i in range(_n_conditions_):
            self._dic_environments[_results_[i][0]] = [_results_[i][1],
                                                       _results_[i][2],
                                                       _results_[i][3],
                                                       _results_[i][4],
                                                       _results_[i][5],
                                                       _results_[i][6],
                                                       _results_[i][7]]
            _model_.append([_results_[i][0], _results_[i][1],
                            _dic_mission_phases[_results_[i][2]],
                            _results_[i][3], _results_[i][4], _results_[i][5],
                            _results_[i][6], _results_[i][7]])

        return False

    def _load_failure_definitions(self):
        """
        Function to load the widgets on the Failure Definition tab.

        Keyword Arguments:
        self -- the current instance of a REVISION class.
        """

        _query_ = "SELECT fld_definition_id, fld_definition \
                   FROM tbl_failure_definitions \
                   WHERE fld_revision_id=%d" % self.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if _results_ == '' or _results_ is None or not _results_:
            self._app.debug_log.error("revision.py: Failed to retrieve failure definition list.")
            return True

        _model_ = self.tvwFailureDefinitions.get_model()
        _model_.clear()
        for i in range(len(_results_)):
            _model_.append(_results_[i])

        return False

    def load_notebook(self):
        """
        Method to load the REVISION Object gtk.Notebook.
        """

        def _load_general_data_tab(self):
            """
            Function to load the widgets on the General Data tab.

            Keyword Arguments:
            self -- the current instance of a REVISION class.
            """

            self.txtTotalCost.set_text(str(locale.currency(self.cost)))
            self.txtCostFailure.set_text(str(locale.currency(self.cost_per_failure)))
            self.txtCostHour.set_text(str(locale.currency(self.cost_per_hour)))
            self.txtName.set_text(self.name)
            self.txtRemarks.set_text(self.remarks)
            self.txtPartCount.set_text(str('{0:0.0f}'.format(self.n_parts)))
            self.txtCode.set_text(str(self.code))

            return False

        def _load_assessment_results_tab(self):
            """
            Function to load the widgets on the Assessment Results tab.

            Keyword Arguments:
            self -- the current instance of a REVISION class.
            """
            fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

            self.txtAvailability.set_text(str(fmt.format(self.availability)))
            self.txtMissionAt.set_text(
                str(fmt.format(self.mission_availability)))

            self.txtActiveHt.set_text(str(fmt.format(self.active_hazard_rate)))
            self.txtDormantHt.set_text(
                str(fmt.format(self.dormant_hazard_rate)))
            self.txtMissionHt.set_text(
                str(fmt.format(self.mission_hazard_rate)))
            self.txtPredictedHt.set_text(
                str(fmt.format(self.hazard_rate)))
            self.txtSoftwareHt.set_text(
                str(fmt.format(self.software_hazard_rate)))

            self.txtMMT.set_text(str('{0:0.2g}'.format(self.mmt)))
            self.txtMCMT.set_text(str('{0:0.2g}'.format(self.mcmt)))
            self.txtMPMT.set_text(str('{0:0.2g}'.format(self.mpmt)))

            self.txtMissionMTBF.set_text(
                str('{0:0.2g}'.format(self.mission_mtbf)))
            self.txtMTBF.set_text(str('{0:0.2g}'.format(self.mtbf)))
            self.txtMTTR.set_text(str('{0:0.2g}'.format(self.mttr)))

            self.txtMissionRt.set_text(
                str(fmt.format(self.mission_reliability)))
            self.txtReliability.set_text(str(fmt.format(self.reliability)))

            return False

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxRevision)
        self._app.winWorkBook.show_all()

        # Load the list of missions.
        _query_ = "SELECT * FROM tbl_missions \
                   WHERE fld_revision_id=%d" % self.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _n_missions_ = len(_results_)
        except TypeError:
            _n_missions_ = 0

        self.cmbMission.get_model().clear()
        self.cmbMission.append_text("")
        for i in range(_n_missions_):
            self._dic_missions[_results_[i][1]] = [_results_[i][2],
                                                   _results_[i][3],
                                                   _results_[i][4]]
            self.cmbMission.append_text(_results_[i][4])

        # Load the notebook tabs.
        _load_general_data_tab(self)
        _load_assessment_results_tab(self)
        self._load_mission_profile()
        self._load_environmental_profile()
        self._load_failure_definitions()

        _title = _(u"RTK Work Book: Revision (Analyzing Revision %d)") % \
            self.revision_id
        self._app.winWorkBook.set_title(_title)

        self.notebook.set_page(0)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the REVISION Object
        treeview.

        Keyword Arguments:
        treeview -- the Hardware Object treeview.
        event    -- a gtk.gdk.Event that called this function (the
                    important attribute is which mouse button was clicked).
                    1 = left
                    2 = scrollwheel
                    3 = right
                    4 = forward
                    5 = backward
                    8 =
                    9 =
        """

        if event.button == 1:
            self._treeview_row_changed(treeview, None, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, treeview, __path, __column):
        """
        Callback function to handle events for the REVISION Object
        TreeView.  It is called whenever the REVISION Object TreeView row
        is activated.  It will save the previously selected row in the
        REVISION Object TreeView.

        Keyword Arguments:
        treeview -- the Revision Object gtk.TreeView.
        __path   -- the actived row gtk.TreeView path.
        __column -- the actived gtk.TreeViewColumn.
        """

        (_model_, _row_) = treeview.get_selection().get_selected()

        # If selecting a revision, load everything associated with
        # the new revision.
        if _row_ is not None:
            self.revision_id = _model_.get_value(_row_, 0)
            self.availability = _model_.get_value(_row_, 1)
            self.mission_availability = _model_.get_value(_row_, 2)
            self.cost = _model_.get_value(_row_, 3)
            self.cost_per_failure = _model_.get_value(_row_, 4)
            self.cost_per_hour = _model_.get_value(_row_, 5)
            self.active_hazard_rate = _model_.get_value(_row_, 6)
            self.dormant_hazard_rate = _model_.get_value(_row_, 7)
            self.mission_hazard_rate = _model_.get_value(_row_, 8)
            self.hazard_rate = _model_.get_value(_row_, 9)
            self.software_hazard_rate = _model_.get_value(_row_, 10)
            self.mmt = _model_.get_value(_row_, 11)
            self.mcmt = _model_.get_value(_row_, 12)
            self.mpmt = _model_.get_value(_row_, 13)
            self.mission_mtbf = _model_.get_value(_row_, 14)
            self.mtbf = _model_.get_value(_row_, 15)
            self.mttr = _model_.get_value(_row_, 16)
            self.name = _model_.get_value(_row_, 17)
            self.mission_reliability = _model_.get_value(_row_, 18)
            self.reliability = _model_.get_value(_row_, 19)
            self.remarks = _model_.get_value(_row_, 20)
            self.n_parts = _model_.get_value(_row_, 21)
            self.code = _model_.get_value(_row_, 22)

            # Build the queries to select the components, reliability tests, and
            # program incidents associated with the selected REVISION.
            _qryParts_ = "SELECT t1.*, t2.fld_part_number, t2.fld_ref_des \
                          FROM tbl_prediction AS t1 \
                          INNER JOIN tbl_system AS t2 \
                          ON t1.fld_assembly_id=t2.fld_assembly_id \
                          WHERE t2.fld_revision_id=%d" % self.revision_id
            _qryIncidents_ = "SELECT * FROM tbl_incident\
                              WHERE fld_revision_id=%d" % self.revision_id

            self._app.REQUIREMENT.save_requirement()
            self._app.REQUIREMENT.load_tree()
            self._app.FUNCTION.save_function()
            self._app.FUNCTION.load_tree()
            self._app.HARDWARE.hardware_save()
            self._app.HARDWARE.load_tree()
            self._app.SOFTWARE.software_save()
            self._app.SOFTWARE.load_tree()
            self._app.VALIDATION.validation_save()
            self._app.VALIDATION.load_tree()
            self._app.TESTING.load_tree()
            self._app.winParts.load_part_tree(_qryParts_)
            #self._app.winParts.load_test_tree(_qryTests_, values)
            #self._app.winParts.load_incident_tree(_qryIncidents_, self.revision_id)

            self.load_notebook()

        return False

    def _add_mission(self, __button):
        """
        Method to add a new mission to the open program.

        Keyword Arguments
        __button -- the gtk.Button widget that called this method.
        """

        _values_ = (self.revision_id, "New Mission")
        _query_ = "INSERT INTO tbl_missions \
                               (fld_revision_id, fld_mission_description) \
                   VALUES (%d, '%s')" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to add new mission.")
            return True

        if _conf.BACKEND == 'mysql':
            _query_ = "SELECT LAST_INSERT_ID()"
        elif _conf.BACKEND == 'sqlite3':
            _query_ = "SELECT seq FROM sqlite_sequence \
                       WHERE name='tbl_missions'"
        self._int_mission_id = self._app.DB.execute_query(_query_,
                                                          None,
                                                          self._app.ProgCnx)

        self._dic_missions[self._int_mission_id] = [0.0, 0, "New Mission"]

        self.load_notebook()

        return False

    def _add_mission_phase(self, __button):
        """
        Method to add a new phase to the selected mission.

        Keyword Arguments
        __button -- the gtk.Button widget that called this method.
        """

        _query_ = "SELECT MAX(fld_phase_id) \
                   FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d" % self._int_mission_id
        _last_id_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        try:
            _last_id_ = _last_id_[0][0] + 1
        except TypeError:
            _last_id_ = 0

        _mission_ = self.cmbMission.get_active() - 1
        _values_ = (_mission_, _last_id_)
        _query_ = "INSERT INTO tbl_mission_phase \
                   (fld_mission_id, fld_phase_id, fld_phase_start, \
                    fld_phase_end, fld_phase_name, fld_phase_description) \
                   VALUES (%d, %d, 0.0, 0.0, '', '')" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to add new mission phase.")
            return True

        self._load_mission_profile()

        return False

    def _add_environment(self, __button):
        """
        Function to add an environmental condition to the environmental profile.

        Keyword Arguments:
        __button -- the gtk.Button() that called this function.
        """

        _mission_ = self.cmbMission.get_active() - 1

        # Find the last used condition ID.
        _query_ = "SELECT MAX(fld_condition_id) \
                   FROM tbl_environmental_profile \
                   WHERE fld_mission_id=%d" % _mission_
        _last_id_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        try:
            _last_id_ = _last_id_[0][0] + 1
        except TypeError:
            _last_id_ = 0

        # Add the new environmental condition.
        _values_ = (_mission_, 0, _last_id_, '', '',
                    0.0, 0.0, 0.0, 0.0)
        _query_ = "INSERT INTO tbl_environmental_profile \
                   (fld_mission_id, fld_phase_id, fld_condition_id, \
                    fld_condition_name, fld_units, fld_minimum, fld_maximum, \
                    fld_mean, fld_variance) \
                   VALUES (%d, %d, %d, '%s', '%s', %f, %f, %f, %f)" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to add new environmental condition.")
            return True

        self._load_environmental_profile()

        return False

    def _add_failure_definition(self, __button):
        """
        Method to add a failure definition to the revision.

        Keyword Arguments:
        __button -- the gtk.Button() that called this function.
        """

        _query_ = "INSERT INTO tbl_failure_definitions \
                               (fld_revision_id, fld_definition) \
                   VALUES (%d, '')" % self.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to add failure definition.")
            return True

        self._load_failure_definitions()

        return False

    def delete_revision(self, __menuitem, __event):
        """
        Deletes the currently selected Revision from the Program's
        MySQL database.

        Keyword Arguments:
        __menuitem -- the gtk.MenuItem that called this function.
        __event    -- the gtk.Button event that called this function.
        """

        # First delete the hardware items associated with the revision.
        _query_ = "DELETE FROM tbl_system \
                   WHERE fld_revision_id=%d" % self.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to delete revision from tbl_system.")
            return True

        # Then delete the revision iteself.
        _query_ = "DELETE FROM tbl_revisions \
                   WHERE fld_revision_id=%d" % self.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to delete revision from tbl_revisions.")
            return True

        self.load_tree()

        return False

    def _delete_mission(self, __button):
        """
        Method to remove the currently selected mission from the program.

        Keyword Arguments
        __button -- the gtk.Button widget that called this method.
        """

        _query_ = "DELETE FROM tbl_missions \
                   WHERE fld_mission_id=%d" % self._int_mission_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to remove the selected mission.")
            return True

        self.load_notebook()

        return False

    def _delete_mission_phase(self, __button):
        """
        Method to remove the currently selected phase from the mission.

        Keyword Arguments
        __button -- the gtk.Button widget that called this method.
        """

        (_model_, _row_) = self.tvwMissionProfile.get_selection().get_selected()

        _values_ = (self._int_mission_id, _model_.get_value(_row_, 0))
        _query_ = "DELETE FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d \
                   AND fld_phase_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to remove the selected mission phase.")
            return True

        self._load_mission_profile()

        return False

    def _delete_environment(self, __button):
        """
        Method to remove the selected environmental condition from the
        environmental profile.

        Keyword Arguments:
        __button -- the gtk.Button() that called this function.
        """

        _selection_ = self.tvwEnvironmentProfile.get_selection()
        (_model_, _row_) = _selection_.get_selected()
        _condition_id_ = _model_.get_value(_row_, 0)

        _values_ = (self._int_mission_id, _condition_id_)
        _query_ = "DELETE FROM tbl_environmental_profile \
                   WHERE fld_mission_id=%d \
                   AND fld_condition_id=%d" % _values_
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to delete selected environmental condition.")
            return True

        self._load_environmental_profile()

        return False

    def _delete_failure_definition(self, __button):
        """
        Method to the currently selected failure definition from the revision.

        Keyword Arguments:
        __button -- the gtk.Button() that called this function.
        """

        # Find the currently selected definition id.
        (_model_,
         _row_) = self.tvwFailureDefinitions.get_selection().get_selected()
        _definition_id_ = _model_.get_value(_row_, 0)

        # Now remove it from the database.
        _query_ = "DELETE FROM tbl_failure_definitions \
                   WHERE fld_revision_id=%d \
                   AND fld_definition_id=%d" % (self.revision_id,
                                                _definition_id_)
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=True)

        if _results_ == '' or not _results_ or _results_ is None:
            self._app.debug_log.error("revision.py: Failed to delete failure definition.")
            return True

        self._failure_definition_tab_load()

        return False

    def save_revision(self, __button):
        """
        Saves the REVISION Object gtk.TreeModel information to the
        program's MySQL or SQLite3 database.

        Keyword Argumesnts:
        __button -- the gtk.Button() that called this method.
        """

        def _save_line(model, __path, row, self):
            """
            Saves each row in the REVISION Object gtk.TreeModel to the
            program's MySQL or SQLite3 database.

            Keyword Arguments:
            model   -- the REVISION Object gtk.TreeModel.
            __path  -- the path of the active row in the REVISION Object
                       gtk.TreeModel.
            row     -- the selected row in the REVISION Object gtk.TreeModel.
            """

            _values_ = (model.get_value(row, self._lst_col_order[1]),
                        model.get_value(row, self._lst_col_order[2]),
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
                        model.get_value(row, self._lst_col_order[20]),
                        model.get_value(row, self._lst_col_order[21]),
                        model.get_value(row, self._lst_col_order[22]),
                        model.get_value(row, self._lst_col_order[0]))
            _query_ = "UPDATE tbl_revisions \
                       SET fld_availability=%f, fld_availability_mission=%f, \
                           fld_cost=%f, fld_cost_failure=%f, fld_cost_hour=%f, \
                           fld_failure_rate_active=%f, \
                           fld_failure_rate_dormant=%f, \
                           fld_failure_rate_mission=%f, \
                           fld_failure_rate_predicted=%f, \
                           fld_failure_rate_software=%f, fld_mmt=%f, \
                           fld_mcmt=%f, fld_mpmt=%f, fld_mtbf_mission=%f, \
                           fld_mtbf_predicted=%f, fld_mttr=%f, fld_name='%s', \
                           fld_reliability_mission=%f, \
                           fld_reliability_predicted=%f, fld_remarks='%s', \
                           fld_total_part_quantity=%d, fld_revision_code='%s' \
                       WHERE fld_revision_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("revision.py: Failed to save revision to tbl_revisions.")

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        _model_.foreach(_save_line, self)

        self._save_use_profile()
        self._save_failure_definition()

        return False

    def _save_use_profile(self):
        """
        Method to save the mission, mission phase, and environmental profile
        information.
        """

        def _save_mission_phase(model, __path, row, self):
            """
            Method to save each line item in the mission profile gtk.TreeBiew()

            Keyword Arguments:
            model   -- the Mission Profile gtk.TreeModel().
            __path  -- the selected path in the Mission Profile gtk.TreeModel().
            row     -- the selected row in the Mission Profile gtk.TreeModel().
            self    -- the current REVISION object.
            """

            _mission_ = self.cmbMission.get_active() - 1
            _values_ = (model.get_value(row, 1), model.get_value(row, 2),
                        model.get_value(row, 3), model.get_value(row, 4),
                        _mission_, model.get_value(row, 0))
            _query_ = "UPDATE tbl_mission_phase \
                       SET fld_phase_start=%f, fld_phase_end=%f, \
                           fld_phase_name='%s', fld_phase_description='%s' \
                       WHERE fld_mission_id=%d \
                       AND fld_phase_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("revision.py: Failed to save mission phase.")

        def _save_environment_profile(model, __path, row, self):
            """
            Method to save each line item in the environmental profile
            gtk.TreeBiew()

            Keyword Arguments:
            model   -- the Environmental Profile gtk.TreeModel().
            __path  -- the selected path in the Environmental Profile
                       gtk.TreeModel().
            row     -- the selected row in the Environmental Profile
                       gtk.TreeModel().
            self    -- the current REVISION object.
            """

            _mission_ = self.cmbMission.get_active() - 1
            _condition_ = self._dic_environments[model.get_value(row, 0)][0]
            _phase_ = self._dic_environments[model.get_value(row, 0)][1]
            _values_ = (_phase_, _condition_, model.get_value(row, 3),
                        model.get_value(row, 4), model.get_value(row, 5),
                        model.get_value(row, 6), model.get_value(row, 7),
                        _mission_, model.get_value(row, 0))
            _query_ = "UPDATE tbl_environmental_profile \
                       SET fld_phase_id=%d, fld_condition_name='%s', \
                           fld_units='%s', fld_minimum=%f, fld_maximum=%f, \
                           fld_mean=%f, fld_variance=%f \
                       WHERE fld_mission_id=%d \
                       AND fld_condition_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("revision.py: Failed to save environmental profile.")

        # Save the currently selected mission.
        _mission_ = self.cmbMission.get_active() - 1
        try:
            _values_ = (self._dic_missions[_mission_][0],
                        self._dic_missions[_mission_][1],
                        self._dic_missions[_mission_][2],
                        _mission_)
            _query_ = "UPDATE tbl_missions \
                       SET fld_mission_time=%f, fld_mission_units=%d, \
                           fld_mission_description='%s' \
                       WHERE fld_mission_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error(
                    "revision.py: Failed to save mission.")
        except KeyError:
            pass

        # Save the phase information for the currently selected mission.
        _model_ = self.tvwMissionProfile.get_model()
        _model_.foreach(_save_mission_phase, self)

        # Save the environmental profile information for the currently selected
        # mission.
        _model_ = self.tvwEnvironmentProfile.get_model()
        _model_.foreach(_save_environment_profile, self)

        return False

    def _save_failure_definition(self):
        """
        Method to save the failure definitions.
        """

        def _save_line(model, __path, row, self):
            """
            Method to save each line item in the failure definition
            gtk.TreeView()

            Keyword Arguments:
            model   -- the Failure Definition gtk.TreeModel().
            __path  -- the selected path in the Failure Definition
                       gtk.TreeModel().
            row     -- the selected row in the Failure Definition
                       gtk.TreeModel().
            self    -- the current REVISION object.
            """

            _values_ = (model.get_value(row, 1), self.revision_id,
                        model.get_value(row, 0))
            _query_ = "UPDATE tbl_failure_definitions \
                       SET fld_definition='%s' \
                       WHERE fld_revision_id=%d \
                       AND fld_definition_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("revision.py: Failed to save failure definition.")

        _model_ = self.tvwFailureDefinitions.get_model()
        _model_.foreach(_save_line, self)

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo -- the gtk.Combo that called the function.
        index -- the position in the applicable treeview associated with the
                 data from the calling gtk.Combo.
        """

        i = combo.get_active()

        if index == 0:                      # Mission list
            self._load_mission_profile()
            self._load_environmental_profile()

        elif index == 1:                    # Time units
            _mission_ = self.cmbMission.get_active() - 1
            try:
                self._dic_missions[_mission_][1] = i
            except KeyError:
                pass

        return False

    def _callback_entry(self, entry, __event, index):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry     -- the entry that called the function.
        __event   -- the gtk.gdk.Event that called this function.
        index     -- the position in the REVISION Object gtk.TreeModel
                     associated with the data from the calling entry.
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        if index == 17:
            self.name = entry.get_text()
            _model_.set_value(_row_, index, self.name)
        elif index == 20:
            self.remarks = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())
            _model_.set_value(_row_, index, self.remarks)
        elif index == 22:
            self.code = entry.get_text()
            _model_.set_value(_row_, index, self.code)
        elif index == 100:                  # Mission name.
            _model_ = self.cmbMission.get_model()
            _row_ = self.cmbMission.get_active_iter()
            _mission_ = self.cmbMission.get_active() - 1

            try:
                _model_.set_value(_row_, 0, entry.get_text())
            except TypeError:
                pass

            try:
                self._dic_missions[_mission_][2] = entry.get_text()
            except KeyError:
                pass
        elif index == 101:                  # Total mission time.
            _mission_ = self.cmbMission.get_active() - 1
            try:
                self._dic_missions[_mission_][0] = float(entry.get_text())
            except KeyError:
                pass

        return False

    def calculate(self, __button):
        """
        Calculates active hazard rate, dormant hazard rate, software hazard
        rate, predicted hazard rate, mission MTBF, limiting MTBF, mission
        reliability, limiting reliability, total cost, cost per failure, and
        cost per operating hour for the selected revision.

        Keyword Arguments:
        __button -- the gtk.ToolButton() that called this function.
        """

        from math import exp

        # First attempt to calculate results based on components associated
        # with the selected revision.
        _query_ = "SELECT SUM(fld_cost), \
                   SUM(fld_failure_rate_active), \
                   SUM(fld_failure_rate_dormant), \
                   SUM(fld_failure_rate_software), \
                   COUNT(fld_assembly_id) \
                   FROM tbl_system \
                   WHERE fld_revision_id=%d \
                   AND fld_part=1" % self.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx,
                                               commit=False)

        # If that doesn't work, attempt to calculate results based on the first
        # level of assemblies associated with the seletected revision.
        if _results_ == '' or not _results_ or _results_ is None:
            _query_ = "SELECT SUM(fld_cost), \
                       SUM(fld_failure_rate_active), \
                       SUM(fld_failure_rate_dormant), \
                       SUM(fld_failure_rate_software), \
                       COUNT(fld_assembly_id) \
                       FROM tbl_system \
                       WHERE fld_revision_id=%d \
                       AND fld_level=1 AND fld_part=0" % self.revision_id
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=False)
            if _results_ == '' or not _results_ or _results_ is None:
                return True

        try:
            self.cost = float(_results_[0][0])
        except TypeError:
            self.cost = 0.0

        try:
            self.active_hazard_rate = float(_results_[0][1])
        except TypeError:
            self.active_hazard_rate = 0.0

        try:
            self.dormant_hazard_rate = float(_results_[0][2])
        except TypeError:
            self.dormant_hazard_rate = 0.0

        try:
            self.software_hazard_rate = float(_results_[0][3])
        except TypeError:
            self.software_hazard_rate = 0.0

        try:
            self.n_parts = int(_results_[0][4])
        except TypeError:
            self.n_parts = 0

        # Predicted h(t).
        self.hazard_rate = self.active_hazard_rate + self.dormant_hazard_rate + self.software_hazard_rate

        # Calculate the MTBF.
        try:
            self.mtbf = 1.0 / self.hazard_rate
        except ZeroDivisionError:
            self.mtbf = 0.0

        # Calculate reliabilities.
        self.reliability = exp(-1.0 * self.hazard_rate / _conf.FRMULT)
        self.mission_reliability = exp(-1.0 * self.hazard_rate * _conf.MTIME / _conf.FRMULT)

        # Calculate availabilities.
        try:
            self.availability = self.mtbf / (self.mtbf + self.mttr)
        except ZeroDivisionError:
            self.availability = 1.0
        except OverflowError:
            self.availability = 1.0

        # Calculate costs.
        self.cost_per_failure = self.cost * self.hazard_rate
        self.cost_per_hour = self.cost / _conf.MTIME

        # Update the REVISION gtk.TreeView().
        (_model_, _row_) = self.treeview.get_selection().get_selected()

        _model_.set_value(_row_, 3, self.cost)
        _model_.set_value(_row_, 4, self.cost_per_failure)
        _model_.set_value(_row_, 5, self.cost_per_hour)
        _model_.set_value(_row_, 6, self.active_hazard_rate)
        _model_.set_value(_row_, 7, self.dormant_hazard_rate)
        #_model_.set_value(_row_, 8, self.mission_hazard_rate)
        _model_.set_value(_row_, 9, self.hazard_rate)
        _model_.set_value(_row_, 10, self.software_hazard_rate)
        #_model_.set_value(_row_, 11, self.mmt)
        #_model_.set_value(_row_, 12, self.mcmt)
        #_model_.set_value(_row_, 13, self.mpmt)
        #_model_.set_value(_row_, 14, self.mission_mtbf)
        _model_.set_value(_row_, 15, self.mtbf)
        _model_.set_value(_row_, 16, self.mttr)
        #_model_.set_value(_row_, 18, self.mission_reliability)
        _model_.set_value(_row_, 19, self.reliability)
        _model_.set_value(_row_, 21, self.n_parts)

        self.load_notebook()

        return False
