#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related
to the revision of the Program.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

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
import calculations as _calc
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

    _ar_tab_labels = [[_(u"Active h(t):"), _(u"Dormant h(t):"),
                       _(u"Software h(t):"), _(u"Predicted h(t):"),
                       _(u"Mission h(t):"), _(u"MTBF:"), _(u"Mission MTBF:"),
                       _(u"Reliability:"), _(u"Mission R(t):")],
                      [_(u"MPMT:"), _(u"MCMT:"), _(u"MTTR:"), _(u"MMT:"),
                       _(u"Availability:"), _(u"Mission A(t):")], [], []]

    n_attributes = 23

    def __init__(self, application):
        """
        Initializes the REVISION Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._app = application

# Create global variables.
        self.treeview = None
        self.model = None
        self.selected_row = None
        self.revision_id = 0

# Create local disctionaries.
        # For mission information.  Mission noun name is the key.  The value is
        # a list [Mission ID, Mission Time, Time Units, Mission Name]
        self._dic_missions = {}
        # For environmental profile information.  Environment noun name is the
        # key.  The value is a list [Condition ID, Phase Name, Measurement
        #                            Units, Minimum Value, Maximum Value,
        #                            Mean, Variance]
        self._dic_environments = {}

# Create local list variables.
        self._lst_col_order = []

# Create local scalar variables.
        self._int_mission_id = -1

        self.vbxRevision = gtk.VBox()
        toolbar = self._toolbar_create()

# Find the user's preferred gtk.Notebook tab position.
        if(_conf.TABPOS[2] == 'left'):
            _position = gtk.POS_LEFT
        elif(_conf.TABPOS[2] == 'right'):
            _position = gtk.POS_RIGHT
        elif(_conf.TABPOS[2] == 'top'):
            _position = gtk.POS_TOP
        else:
            _position = gtk.POS_BOTTOM

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(_position)

        self.vbxRevision.pack_start(toolbar, expand=False)
        self.vbxRevision.pack_start(self.notebook)

# Create the General Data tab.
        self.txtCode = _widg.make_entry()
        self.txtName = _widg.make_entry()
        self.txtTotalCost = _widg.make_entry(editable=False)
        self.txtCostFailure = _widg.make_entry(editable=False)
        self.txtCostHour = _widg.make_entry(editable=False)
        self.txtPartCount = _widg.make_entry(editable=False)
        self.txtRemarks = gtk.TextBuffer()
        if self._general_data_tab_create():
            self._app.debug_log.error("revision.py: Failed to create General Data tab.")

# Create the Use Profile tab.
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
        if self._use_profile_tab_create():
            self._app.debug_log.error("revision.py: Failed to create Use Profile tab.")

# Create the failure definition tab.
        self.btnAddDefinition = _widg.make_button(_width_=40, _image_='add')
        self.btnRemoveDefinition = _widg.make_button(_width_=40,
                                                     _image_='remove')
        self.tvwFailureDefinitions = gtk.TreeView()
        if self._failure_definition_tab_create():
            self._app.debug_log.error("revision.py: Failed to create Failue Definition tab.")

# Create the Assessment Results tab.
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
        if self._assessment_results_tab_create():
            self._app.debug_log.error("revision.py: Failed to create Assessment Results tab.")

    def _toolbar_create(self):
        """
        Method to create the toolbar for the REVISION Object work book.
        """

        toolbar = gtk.Toolbar()

        _pos = 0

# Add requirement button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Adds a new revision to the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.connect('clicked', AddRevision, self._app)
        toolbar.insert(button, _pos)
        _pos += 1

# Delete requirement button
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Removes the currently selected revision from the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.revision_delete)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Calculate requirement button
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Calculate the currently selected revision."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        button.connect('clicked', _calc.calculate_revision, self._app)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Save requirement button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_(u"Saves the currently selected revision to the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.revision_save)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.show()

        return(toolbar)

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it
        with the appropriate widgets for the REVISION object.
        """

        _labels_ = [_(u"Revision Code:"), _(u"Revision Name:"),
                    _(u"Total Cost:"), _(u"Cost/Failure:"), _(u"Cost/Hour:"),
                    _(u"Total Part Count:"), _(u"Remarks:")]

        def _general_data_widgets_create(self):
            """
            Method to create General Data widgets for the REVISION object.
            """

            self.txtCode.set_tooltip_text(_("A unique code for the selected revision."))
            self.txtCode.connect('focus-out-event',
                                 self._callback_entry, 'text', 22)

            self.txtName.set_tooltip_text(_("The name of the selected revision."))
            self.txtName.connect('focus-out-event',
                                 self._callback_entry, 'text', 17)

            self.txtTotalCost.set_tooltip_text(_("Displays the total cost of the selected revision."))
            self.txtCostFailure.set_tooltip_text(_("Displays the cost per failure of the selected revision."))
            self.txtCostHour.set_tooltip_text(_("Displays the failure cost per operating hour for the selected revision."))
            self.txtPartCount.set_tooltip_text(_("Displays the total part count for the selected revision."))

            return False

        if _general_data_widgets_create(self):
            self._app.debug_log.error("revision.py: Failed to create General Data tab widgets.")

# Place the input/output widgets.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

# Create and place the labels.
        _max1_ = 0
        _max2_ = 0
        (_max1_, _y_pos_) = _widg.make_labels(_labels_, fixed, 5, 5)
        _x_pos_ = max(_max1_, _max2_) + 20

        fixed.put(self.txtCode, _x_pos_, _y_pos_[0])
        fixed.put(self.txtName, _x_pos_, _y_pos_[1])
        fixed.put(self.txtTotalCost, _x_pos_, _y_pos_[2])
        fixed.put(self.txtCostFailure, _x_pos_, _y_pos_[3])
        fixed.put(self.txtCostHour, _x_pos_, _y_pos_[4])
        fixed.put(self.txtPartCount, _x_pos_, _y_pos_[5])

        textview = _widg.make_text_view(buffer_=self.txtRemarks, width=400)
        textview.set_tooltip_text(_("Enter any remarks associated with the selected revision."))
        _view_ = textview.get_children()[0].get_children()[0]
        _view_.connect('focus-out-event', self._callback_entry, 'text', 20)
        fixed.put(textview, _x_pos_, _y_pos_[6])

        fixed.show_all()

# Insert the tab.
        _label_ = gtk.Label()
        _heading_ = _("General\nData")
        _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.show_all()
        _label_.set_tooltip_text(_(u"Displays general information for the selected revision."))
        self.notebook.insert_page(frame,
                                  tab_label=_label_,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the REVISION
        Object.
        """

        # Display data in the widgets.
        self.txtTotalCost.set_text(str(locale.currency(self.model.get_value(self.selected_row, 3))))
        self.txtCostFailure.set_text(str(locale.currency(self.model.get_value(self.selected_row, 4))))
        self.txtCostHour.set_text(str(locale.currency(self.model.get_value(self.selected_row, 5))))
        self.txtName.set_text(self.model.get_value(self.selected_row, 17))
        self.txtRemarks.set_text(self.model.get_value(self.selected_row, 20))
        self.txtPartCount.set_text(str('{0:0.0f}'.format(self.model.get_value(self.selected_row, 21))))
        self.txtCode.set_text(str(self.model.get_value(self.selected_row, 22)))

        return False

    def _use_profile_tab_create(self):
        """
        Method to create the Usage Profile gtk.Notebook tab and populate it
        with the appropriate widgets for the REVISION object.
        """

        _labels_ = [_(u"Mission:"), _(u"Mission Time:")]

        def _use_profile_widgets_create(self):
            """
            Method to create the Use Profile widgets.
            """

            _units_ = [[_(u"Seconds")], [_(u"Minutes")],
                       [_(u"Hours")], [_(u"Cycles")]]
            _mission_headings_ = [_(u"Phase ID"), _(u"Start"), _(u"End"),
                                  _(u"Code"), _(u"Description")]
            _environ_headings_ = [_(u"Condition ID"),
                                  _(u"Environmental\nCondition"),
                                  _(u"Mission\nPhase"), _(u"Units"),
                                  _(u"Minimum"), _(u"Maximum"), _(u"Mean"),
                                  _(u"Variance")]

            self.btnAddMission.set_tooltip_text(_(u"Adds a new mission to the selected program."))
            self.btnAddMission.connect('released', self._mission_add)

            self.btnRemoveMission.set_tooltip_text(_(u"Removes the currently selected mission from the program."))
            self.btnRemoveMission.connect('released', self._mission_remove)

            self.btnAddPhase.set_tooltip_text(_(u"Adds a new phase to the selected mission."))
            self.btnAddPhase.connect('released', self._mission_add_phase)

            self.btnRemovePhase.set_tooltip_text(_(u"Removes the currently selected phase from the mission."))
            self.btnRemovePhase.connect('released', self._mission_remove_phase)

            self.btnAddEnvironment.set_tooltip_text(_(u"Adds a new environmental condition to the environmental profile."))
            self.btnAddEnvironment.connect('released', self._environment_add)

            self.btnRemoveEnvironment.set_tooltip_text(_(u"Removes the currently selected environmental condition from the environmental profile."))
            self.btnRemoveEnvironment.connect('released', self._environment_remove)

            self.cmbMission.set_tooltip_text(_(u"Selects and displays the current mission profile."))
            self.cmbMission.connect('changed', self._callback_combo, 0)

            self.cmbTimeUnit.set_tooltip_text(_(u"Select and displays the time units for the selected mission."))
            _widg.load_combo(self.cmbTimeUnit, _units_)
            self.cmbTimeUnit.connect('changed', self._callback_combo, 1)

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

            self.txtMission.set_tooltip_text(_(u"Displays the mission name."))
            self.txtMission.connect('focus-out-event',
                                    self._callback_entry, 'text', 100)
            self.txtMissionTime.set_tooltip_text(_(u"Displays the total mission time."))
            self.txtMissionTime.connect('focus-out-event',
                                        self._callback_entry, 'float', 101)

            return False

        if _use_profile_widgets_create(self):
            self._app.debug_log.error("revision.py: Failed to create Use Profile tab widgets.")

        hpaned = gtk.HPaned()

# Create the left half.
        vbox = gtk.VBox()
        hpaned.pack1(vbox, resize=False)

        fixed = gtk.Fixed()

        _max1_ = 0
        _max2_ = 0
        (_max1_, _y_pos_) = _widg.make_labels(_labels_, fixed, 5, 5, y_inc=35)
        _x_pos_ = max(_max1_, _max2_) + 20

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_(u""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        fixed.put(self.cmbMission, _x_pos_, _y_pos_[0])
        fixed.put(self.txtMission, _x_pos_+205, _y_pos_[0])
        fixed.put(self.btnAddMission, _x_pos_+410, _y_pos_[0])
        fixed.put(self.btnRemoveMission, _x_pos_+455, _y_pos_[0])
        fixed.put(self.btnAddPhase, _x_pos_+510, _y_pos_[0])
        fixed.put(self.btnRemovePhase, _x_pos_+555, _y_pos_[0])
        fixed.put(self.txtMissionTime, _x_pos_, _y_pos_[1])
        fixed.put(self.cmbTimeUnit, _x_pos_+100, _y_pos_[1])

        vbox.pack_start(frame, expand=False)

        # Add the mission profile gtk.TreeView().
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwMissionProfile)

        frame = _widg.make_frame(_label_=_(u"Mission Profile"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_end(frame, expand=True)

# Create the right half.
        vbox = gtk.VBox()
        hpaned.pack2(vbox, resize=False)

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_(u""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        fixed.put(self.btnAddEnvironment, 5, 5)
        fixed.put(self.btnRemoveEnvironment, 50, 5)

        vbox.pack_start(frame, expand=False)

        # Add the environmental profile gtk.TreeView()
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add(self.tvwEnvironmentProfile)

        frame = _widg.make_frame(_label_=_(u"Environmental Profile"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_end(frame, expand=True)

# Insert the tab.
        _label_ = gtk.Label()
        _heading_ = _("Usage\nProfiles")
        _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.show_all()
        _label_.set_tooltip_text(_(u"Displays usage profiles for the selected revision."))
        self.notebook.insert_page(hpaned,
                                  tab_label=_label_,
                                  position=-1)

        return False

    def _use_profile_tab_load(self):
        """
        Method to load the Usage Profile tab widgets.
        """

# Load the list of missions.
        _query_ = "SELECT * FROM tbl_missions \
                   WHERE fld_revision_id=%d" % self.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        _missions_ = len(_results_)
        self.cmbMission.get_model().clear()
        self.cmbMission.append_text("")
        for i in range(_missions_):
            self._dic_missions[_results_[i][4]] = [_results_[i][1],
                                                   _results_[i][2],
                                                   _results_[i][3],
                                                   _results_[i][4]]
            self.cmbMission.append_text(_results_[i][4])

        self.cmbMission.set_active(0)

        return False

    def _failure_definition_tab_create(self):
        """
        Method to create the Usage Profile gtk.Notebook tab and populate it
        with the appropriate widgets for the REVISION object.
        """

        def _failure_definition_widgets_create(self):
            """
            Method to create the Failure Definition widgets.
            """

            self.btnAddDefinition.set_tooltip_text(_("Adds a new failure definition to the list."))
            self.btnAddDefinition.connect('released', self._definition_add)

            self.btnRemoveDefinition.set_tooltip_text(_("Removes the currently selected failure definition from the list."))
            self.btnRemoveDefinition.connect('released', self._definition_remove)

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

            return False

        if _failure_definition_widgets_create(self):
            self._app.debug_log.error("revision.py: Failed to create Failure Definition tab widgets.")

# Create the top half.
        _vbox_ = gtk.VBox()

        _fixed_ = gtk.Fixed()
        _fixed_.put(self.btnAddDefinition, 5, 5)
        _fixed_.put(self.btnRemoveDefinition, 50, 5)

        _vbox_.pack_start(_fixed_, expand=False)

# Create the bottom half.
        _scrollwindow_ = gtk.ScrolledWindow()
        _scrollwindow_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow_.add(self.tvwFailureDefinitions)

        _frame_ = _widg.make_frame(_label_=_(u"Failure Definitions List"))
        _frame_.set_shadow_type(gtk.SHADOW_IN)
        _frame_.add(_scrollwindow_)

        _vbox_.pack_end(_frame_)

# Insert the tab.
        _label_ = gtk.Label()
        _heading_ = _("Failure\nDefintions")
        _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.show_all()
        _label_.set_tooltip_text(_(u"Displays usage profiles for the selected revision."))
        self.notebook.insert_page(_vbox_,
                                  tab_label=_label_,
                                  position=-1)

        return False

    def _failure_definition_tab_load(self):
        """
        Method to the load the list of failure definitions.
        """

        _query_ = "SELECT fld_definition_id, fld_definition \
                   FROM tbl_failure_definitions \
                   WHERE fld_revision_id=%d" % self.revision_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(_results_ == '' or _results_ is None or not _results_):
            self._app.debug_log.error("revision.py: Failed to retrieve failure definition list.")
            return True

        _model_ = self.tvwFailureDefinitions.get_model()
        _model_.clear()
        for i in range(len(_results_)):
            _model_.append(_results_[i])

        return False

    def _assessment_results_tab_create(self):
        """
        Method to create the Assessment Results gtk.Notebook tab and
        populate is with the appropriate widgets for the REVISION object.
        """

        def _assessment_results_widgets_create(self):
            """
            Method to create the Assessment Results widgets for the
            REVISION object.
            """

    # Quadrant 1 (left) widgets.
            self.txtActiveHt.set_tooltip_text(_("Displays the active failure intensity for the selected revision."))
            self.txtDormantHt.set_tooltip_text(_("Displays the dormant failure intensity for the selected revision."))
            self.txtSoftwareHt.set_tooltip_text(_("Displays the software failure intensity for the selected revision."))
            self.txtPredictedHt.set_tooltip_text(_("Displays the predicted failure intensity for the selected revision.  This is the sum of the active, dormant, and software hazard rates."))
            self.txtMissionHt.set_tooltip_text(_("Displays the mission failure intensity for the selected revision."))
            self.txtMTBF.set_tooltip_text(_("Displays the limiting mean time between failure (MTBF) for the selected revision."))
            self.txtMissionMTBF.set_tooltip_text(_("Displays the mission mean time between failure (MTBF) for the selected revision."))
            self.txtReliability.set_tooltip_text(_("Displays the limiting reliability for the selected revision."))
            self.txtMissionRt.set_tooltip_text(_("Displays the mission reliability for the selected revision."))

            # Quadrant #2 (right) widgets.
            self.txtMPMT.set_tooltip_text(_("Displays the mean preventive maintenance time (MPMT) for the selected revision."))
            self.txtMCMT.set_tooltip_text(_("Displays the mean corrective maintenance time (MCMT) for the selected revision."))
            self.txtMTTR.set_tooltip_text(_("Displays the mean time to repair (MTTR) for the selected revision."))
            self.txtMMT.set_tooltip_text(_("Displays the mean maintenance time (MMT) for the selected revision.  This includes preventive and corrective maintenance."))
            self.txtAvailability.set_tooltip_text(_("Displays the limiting availability for the selected revision."))
            self.txtMissionAt.set_tooltip_text(_("Displays the mission availability for the selected revision."))

            return False

        if _assessment_results_widgets_create(self):
            self._app.debug_log.error("revision.py: Failed to create Assessment Results widgets.")

        hbox = gtk.HBox()

        # Construct the left half of the page.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Reliability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        y_pos = 5
        for i in range(len(self._ar_tab_labels[0])):
            label = _widg.make_label(self._ar_tab_labels[0][i],
                                     150, 25)
            fixed.put(label, 5, (i * 30) + y_pos)

        fixed.put(self.txtActiveHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtDormantHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtSoftwareHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtPredictedHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionHt, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMTBF, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionMTBF, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtReliability, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionRt, 155, y_pos)

        fixed.show_all()

# Construct the right half of the page.
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Maintainability Results"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        y_pos = 5
        for i in range(len(self._ar_tab_labels[1])):
            label = _widg.make_label(self._ar_tab_labels[1][i],
                                     150, 25)
            fixed.put(label, 5, (i * 30) + y_pos)

        fixed.put(self.txtMPMT, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMCMT, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMTTR, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMMT, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtAvailability, 155, y_pos)
        y_pos += 30
        fixed.put(self.txtMissionAt, 155, y_pos)

        fixed.show_all()

# Insert the tab.
        _label_ = gtk.Label()
        _heading_ = _("Assessment\nResults")
        _label_.set_markup("<span weight='bold'>" + _heading_ + "</span>")
        _label_.set_alignment(xalign=0.5, yalign=0.5)
        _label_.set_justify(gtk.JUSTIFY_CENTER)
        _label_.show_all()
        _label_.set_tooltip_text(_(u"Displays reliability, maintainability, and availability assessment results for the selected revision."))
        self.notebook.insert_page(hbox,
                                  tab_label=_label_,
                                  position=-1)

        return False

    def _assessment_results_tab_load(self):
        """
        Loads the widgets with assessment results for the REVISION Object.
        """

        fmt = '{0:0.' + str(_conf.PLACES) + 'g}'

        # Display data in the widgets.
        self.txtAvailability.set_text(str(fmt.format(self.model.get_value(self.selected_row, 1))))
        self.txtMissionAt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 2))))

        self.txtActiveHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 6))))
        self.txtDormantHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 7))))
        self.txtMissionHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 8))))
        self.txtPredictedHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 9))))
        self.txtSoftwareHt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 10))))

        self.txtMMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 11))))
        self.txtMCMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 12))))
        self.txtMPMT.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 13))))

        self.txtMissionMTBF.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 14))))
        self.txtMTBF.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 15))))
        self.txtMTTR.set_text(str('{0:0.2g}'.format(self.model.get_value(self.selected_row, 16))))

        self.txtMissionRt.set_text(str(fmt.format(self.model.get_value(self.selected_row, 18))))
        self.txtReliability.set_text(str(fmt.format(self.model.get_value(self.selected_row, 19))))

        return False

    def create_tree(self):
        """
        Creates the REVISION treeview and connects it to callback functions
        to handle editting.  Background and foreground colors can be set
        using the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[0]
        fg_color = _conf.RTK_COLORS[1]
        (self.treeview, self._lst_col_order) = _widg.make_treeview('Revision', 0,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)

        self.treeview.set_tooltip_text(_("Displays the list of revisions."))
        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)
        self.treeview.connect('button_press_event', self._treeview_clicked)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the REVISION Object gtk.TreeModel with revision information.
        This information can be stored either in a MySQL or SQLite3
        database.
        """

        query = "SELECT * FROM tbl_revisions"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        n_records = len(results)

        self.model.clear()
        for i in range(n_records):
            self.model.append(None, results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        root = self.model.get_iter_root()
        if(root is not None):
            path = self.model.get_path(root)
            column = self.treeview.get_column(0)
            self.treeview.row_activated(path, column)

        self.revision_id = self.model.get_value(self.selected_row, 0)

        return False

    def _load_mission_profile(self):
        """
        Method to load the mission profile gtk.TreeView().
        """

        _model_ = self.tvwMissionProfile.get_model()
        _model_.clear()

        _query_ = "SELECT fld_phase_id, fld_phase_start, fld_phase_end, \
                          fld_phase_name, fld_phase_description \
                   FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d" % self._int_mission_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(_results_ == '' or not _results_):
            self._app.debug_log.error("revision.py: Failed to load mission profile.")
        else:
            _n_phases_ = len(_results_)
            for i in range(_n_phases_):
                _model_.append(_results_[i])

# Set the selected mission to the first in the list and then load the
# remaining widgets appropriately.
        _mission_ = self.cmbMission.get_active_text()
        try:
            self.txtMissionTime.set_text(str(self._dic_missions[_mission_][1]))
            self.cmbTimeUnit.set_active(self._dic_missions[_mission_][2])
        except KeyError:
            self.txtMissionTime.set_text("0.0")
            self.cmbTimeUnit.set_active(0)

        self.txtMission.set_text(str(_mission_))

        return False

    def _load_environmental_profile(self):
        """
        Method to load the environmental profile gtk.TreeView().
        """

# Load the mission phase gtk.CellRendererCombo in the environmental profile
# gtk.TreeView().
        _query_ = "SELECT fld_phase_name \
                   FROM tbl_mission_phase \
                   WHERE fld_mission_id=%d" % self._int_mission_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        _phases_ = len(_results_)
        _column_ = self.tvwEnvironmentProfile.get_column(2)
        _cell_ = _column_.get_cell_renderers()
        _cellmodel_ = _cell_[0].get_property('model')
        _cellmodel_.clear()
        _cellmodel_.append(["All"])
        for i in range(_phases_):
            _cellmodel_.append([_results_[i][0]])

# Load the environmental profile gtk.TreeView().
        _model_ = self.tvwEnvironmentProfile.get_model()
        _model_.clear()

        _query_ = "SELECT t1.fld_condition_id, t1.fld_condition_name, \
                          t2.fld_phase_name, t1.fld_units, t1.fld_minimum, \
                          t1.fld_maximum, t1.fld_mean, t1.fld_variance \
                   FROM tbl_environmental_profile AS t1 \
                   INNER JOIN tbl_mission_phase AS t2 \
                   ON t2.fld_mission_id=t1.fld_mission_id \
                   WHERE t1.fld_mission_id=%d \
                   AND t2.fld_phase_id=t1.fld_phase_id" % self._int_mission_id
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)

        if(_results_ == '' or not _results_):
            self._app.debug_log.error("revision.py: Failed to retrieve environmental profile.")
            return True

        _n_conditions_ = len(_results_)
        for i in range(_n_conditions_):
            self._dic_environments[_results_[i][1]] = [_results_[i][0],
                                                       _results_[i][2],
                                                       _results_[i][3],
                                                       _results_[i][4],
                                                       _results_[i][5],
                                                       _results_[i][6],
                                                       _results_[i][7]]
            _model_.append(_results_[i])

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

        if(event.button == 1):
            self._treeview_row_changed(treeview, None, 0)
        elif(event.button == 3):
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, treeview, path, column):
        """
        Callback function to handle events for the REVISION Object
        TreeView.  It is called whenever the REVISION Object TreeView row
        is activated.  It will save the previously selected row in the
        REVISION Object TreeView.

        Keyword Arguments:
        treeview -- the Revision Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        selection = self.treeview.get_selection()
        (self.model, self.selected_row) = selection.get_selected()

# If not selecting the same revision, load everything associated with the new
# revision.  Otherwise simply load the Revision Object notebook.
        #if(self.model.get_value(self.selected_row, 0) != self.revision_id):
        self.revision_id = self.model.get_value(self.selected_row, 0)

# Build the queries to select the components, reliability tests, and program
# incidents associated with the selected REVISION.
        qryParts = "SELECT t1.*, t2.fld_part_number, t2.fld_ref_des \
                    FROM tbl_prediction AS t1 \
                    INNER JOIN tbl_system AS t2 \
                    ON t1.fld_assembly_id=t2.fld_assembly_id \
                    WHERE t2.fld_revision_id=%d"
        qryIncidents = "SELECT * FROM tbl_incident\
                        WHERE fld_revision_id=%d"

        if self.selected_row is not None:
            self._app.REQUIREMENT.requirement_save(None)
            self._app.REQUIREMENT.load_tree()
            self._app.FUNCTION.function_save()
            self._app.FUNCTION.load_tree()
            self._app.HARDWARE.hardware_save()
            self._app.HARDWARE.load_tree()
            self._app.SOFTWARE.software_save()
            self._app.SOFTWARE.load_tree()
            self._app.VALIDATION.validation_save()
            self._app.VALIDATION.load_tree()
            self._app.winParts.load_part_tree(qryParts, self.revision_id)
            #self._app.winParts.load_test_tree(qryTests, values)
            #self._app.winParts.load_incident_tree(qryIncidents, self.revision_id)

        self.load_notebook()

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the REVISION Object gtk.TreeModel.

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the REVISION Object
                   gtk.TreeModel.
        """

        for i in columns:
            self.model.set_value(self.selected_row, i, values[i])

        return False

    def revision_delete(self, menuitem, event):
        """
        Deletes the currently selected Revision from the Program's
        MySQL database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        event    -- the gtk.Button event that called this function.
        """

# First delete the hardware items associated with the revision.
        values = (self.revision_id,)
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_system \
                     WHERE fld_revision_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_system \
                     WHERE fld_revision_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("revision.py: Failed to delete revision from tbl_system.")
            return True

# Then delete the revision iteself.
        values = (self.revision_id,)
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_revisions \
                     WHERE fld_revision_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_revisions \
                     WHERE fld_revision_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("revision.py: Failed to delete revision from tbl_revisions.")
            return True

        self.load_tree()

        return False

    def revision_save(self, button=None):
        """
        Saves the REVISION Object gtk.TreeModel information to the
        program's MySQL or SQLite3 database.

        Keyword Argumesnts:
        button -- the gtk.Button widgets that called this method.
        """

        self.model.foreach(self._save_line_item)

        self._use_profile_save()
        self._failure_definition_save()

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the REVISION Object gtk.TreeModel to the
        program's MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the REVISION Object gtk.TreeModel.
        path_ -- the path of the active row in the REVISION Object
                 gtk.TreeModel.
        row   -- the selected row in the REVISION Object gtk.TreeModel.
        """

        _values_ = (model.get_value(row, self._lst_col_order[1]), \
                    model.get_value(row, self._lst_col_order[2]), \
                    model.get_value(row, self._lst_col_order[3]), \
                    model.get_value(row, self._lst_col_order[4]), \
                    model.get_value(row, self._lst_col_order[5]), \
                    model.get_value(row, self._lst_col_order[6]), \
                    model.get_value(row, self._lst_col_order[7]), \
                    model.get_value(row, self._lst_col_order[8]), \
                    model.get_value(row, self._lst_col_order[9]), \
                    model.get_value(row, self._lst_col_order[10]), \
                    model.get_value(row, self._lst_col_order[11]), \
                    model.get_value(row, self._lst_col_order[12]), \
                    model.get_value(row, self._lst_col_order[13]), \
                    model.get_value(row, self._lst_col_order[14]), \
                    model.get_value(row, self._lst_col_order[15]), \
                    model.get_value(row, self._lst_col_order[16]), \
                    model.get_value(row, self._lst_col_order[17]), \
                    model.get_value(row, self._lst_col_order[18]), \
                    model.get_value(row, self._lst_col_order[19]), \
                    model.get_value(row, self._lst_col_order[20]), \
                    model.get_value(row, self._lst_col_order[21]), \
                    model.get_value(row, self._lst_col_order[22]), \
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

    def _use_profile_save(self):
        """
        Method to save teh mission, mission phase, and environmental profile
        information.
        """

        def _save_mission_phase(model, path, row, self):
            """
            Method to save each line item in the mission profile gtk.TreeBiew()

            Keyword Arguments:
            model -- the Mission Profile gtk.TreeModel().
            path  -- the selected path in the Mission Profile gtk.TreeModel().
            row   -- the selected row in the Mission Profile gtk.TreeModel().
            self  -- the current REVISION object.
            """

            _values_ = (model.get_value(row, 1), model.get_value(row, 2),
                        model.get_value(row, 3), model.get_value(row, 4),
                        self._int_mission_id, model.get_value(row, 0))
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

        def _save_environment_profile(model, path, row, self):
            """
            Method to save each line item in the environmental profile
            gtk.TreeBiew()

            Keyword Arguments:
            model -- the Environmental Profile gtk.TreeModel().
            path  -- the selected path in the Environmental Profile
                     gtk.TreeModel().
            row   -- the selected row in the Environmental Profile
                     gtk.TreeModel().
            self  -- the current REVISION object.
            """

            _values_ = (model.get_value(row, 1), model.get_value(row, 3),
                        model.get_value(row, 4), model.get_value(row, 5),
                        model.get_value(row, 6), model.get_value(row, 7),
                        self._int_mission_id, model.get_value(row, 0))
            _query_ = "UPDATE tbl_environmental_profile \
                       SET fld_condition_name='%s', fld_units='%s', \
                           fld_minimum=%f, fld_maximum=%f, fld_mean=%f, \
                           fld_variance=%f \
                       WHERE fld_mission_id=%d \
                       AND fld_condition_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("revision.py: Failed to save environmental profile.")

# Save the currently selected mission.
        _mission_ = self.cmbMission.get_active_text()
        try:
            _values_ = (self._dic_missions[_mission_][1],
                        self._dic_missions[_mission_][2],
                        self._dic_missions[_mission_][3],
                        self._int_mission_id)
            _query_ = "UPDATE tbl_missions \
                       SET fld_mission_time=%f, fld_mission_units=%d, \
                           fld_mission_description='%s' \
                       WHERE fld_mission_id=%d" % _values_
            _results_ = self._app.DB.execute_query(_query_,
                                                   None,
                                                   self._app.ProgCnx,
                                                   commit=True)

            if not _results_:
                self._app.debug_log.error("revision.py: Failed to save mission.")
        except KeyError:
            pass

# Save the phase information for the currently selected mission.
        _model_ = self.tvwMissionProfile.get_model()
        _model_.foreach(_save_mission_phase, self)

# Save the environmenatl profile information for the currently selected
# mission.
        _model_ = self.tvwEnvironmentProfile.get_model()
        _model_.foreach(_save_environment_profile, self)

        return False

    def _failure_definition_save(self):
        """
        Method to save the failure definitions.
        """

        def _save_line(model, path, row, self):
            """
            Method to save each line item in the failure definition
            gtk.TreeView()

            Keyword Arguments:
            model -- the Failure Definition gtk.TreeModel().
            path  -- the selected path in the Failure Definition
                     gtk.TreeModel().
            row   -- the selected row in the Failure Definition
                     gtk.TreeModel().
            self  -- the current REVISION object.
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

    def load_notebook(self):
        """
        Method to load the REVISION Object gtk.Notebook.
        """

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxRevision)
        self._app.winWorkBook.show_all()

        self._general_data_tab_load()
        self._assessment_results_tab_load()
        self._use_profile_tab_load()
        self._failure_definition_tab_load()

        _title = _("RTK Work Book: Revision (Analyzing Revision %d)") % \
                 self.revision_id
        self._app.winWorkBook.set_title(_title)

        return False

    def _mission_add(self, button=None):
        """
        Method to add a new mission to the open program.

        Keyword Arguments
        button -- the gtk.Button widget that called this method.
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

        if(_conf.BACKEND == 'mysql'):
            _query_ = "SELECT LAST_INSERT_ID()"
        elif(_conf.BACKEND == 'sqlite3'):
            _query_ = "SELECT seq FROM sqlite_sequence \
                       WHERE name='tbl_missions'"
        self._int_mission_id = self._app.DB.execute_query(_query_,
                                                          None,
                                                          self._app.ProgCnx)

        self._dic_missions['New Mission'] = [self._int_mission_id, 0.0, 0,
                                             "New Mission"]
        self._use_profile_tab_load()

        return False

    def _mission_add_phase(self, button=None):
        """
        Method to add a new phase to the selected mission.

        Keyword Arguments
        button -- the gtk.Button widget that called this method.
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

        _values_ = (self._int_mission_id, _last_id_)
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

    def _mission_remove(self, button=None):
        """
        Method to remove the currently selected mission from the program.

        Keyword Arguments
        button -- the gtk.Button widget that called this method.
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

        self._use_profile_tab_load()

        return False

    def _mission_remove_phase(self, button=None):
        """
        Method to remove the currently selected phase from the mission.

        Keyword Arguments
        button -- the gtk.Button widget that called this method.
        """

        _selection_ = self.tvwMissionProfile.get_selection()
        (_model_, _row_) = _selection_.get_selected()

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

    def _environment_add(self, button=None):
        """
        Function to add an environmental condition to the environmental profile.

        Keyword Arguments:
        button -- the gtk.Button() that called this function.
        """

# Find the last used condition ID.
        _query_ = "SELECT MAX(fld_condition_id) \
                   FROM tbl_environmental_profile \
                   WHERE fld_mission_id=%d" % self._int_mission_id
        _last_id_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        try:
            _last_id_ = _last_id_[0][0] + 1
        except TypeError:
            _last_id_ = 0

# Add the new environmental condition.
        _values_ = (self._int_mission_id, 0, _last_id_, '', '',
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

    def _environment_remove(self, button=None):
        """
        Method to remove the selected environmental condition from the
        environmental profile.

        Keyword Arguments:
        button -- the gtk.Button() that called this function.
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

    def _definition_add(self, button=None):
        """
        Method to add a failure definition to the revision.

        Keyword Arguments:
        button -- the gtk.Button() that called this function.
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

        self._failure_definition_tab_load()

        return False

    def _definition_remove(self, button=None):
        """
        Method to the currently selected failure definition from the revision.

        Keyword Arguments:
        button -- the gtk.Button() that called this function.
        """

# Find the currently selected definition id.
        _selection_ = self.tvwFailureDefinitions.get_selection()
        (_model_, _row_) = _selection_.get_selected()
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

        if not _results_:
            self._app.debug_log.error("revision.py: Failed to delete failure definition.")
            return True

        self._failure_definition_tab_load()

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the gtk.Combo that called the function.
        _index_ -- the position in the applicable treeview associated with the
                   data from the calling gtk.Combo.
        """

        i = combo.get_active()

        if(_index_ == 0):                   # Mission list
            _mission_ = combo.get_active_text()
            try:
                self._int_mission_id = self._dic_missions[_mission_][0]
            except KeyError:
                self._int_mission_id = -1

            self._load_mission_profile()
            self._load_environmental_profile()

        elif(_index_ == 1):                 # Time units
            _mission_ = self.cmbMission.get_active_text()
            try:
                self._dic_missions[_mission_][2] = i
            except KeyError:
                pass

        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        event   -- the gtk.gdk.Event that called this function.
        convert -- the data type to convert the entry contents to.
        index_  -- the position in the REVISION Object gtk.TreeModel
                   associated with the data from the calling entry.
        """

        if(convert == 'text'):
            if(_index_ == 20):
                _text_ = self.txtRemarks.get_text(*self.txtRemarks.get_bounds())
            else:
                _text_ = entry.get_text()

        elif(convert == 'int'):
            _text_ = int(entry.get_text())

        elif(convert == 'float'):
            _text_ = float(entry.get_text().replace('$', ''))

# Update the Revision tree.
        if(_index_ < 100):
            self.model.set_value(self.selected_row, _index_, _text_)
        elif(_index_ == 100):
            _mission_ = self.cmbMission.get_active_text()
            self._dic_missions[_mission_][3] = _text_
        elif(_index_ == 101):
            _mission_ = self.cmbMission.get_active_text()
            self._dic_missions[_mission_][1] = _text_
        return False
