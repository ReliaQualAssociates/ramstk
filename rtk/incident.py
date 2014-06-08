#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
Program incidents.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       incident.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
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

# Import other RTK modules.
from _assistants_.adds import AddIncident, CreateDataSet
from _assistants_.filters import FilterIncident
from _assistants_.imports import ImportIncident
#from _assistants_.exports import ExportIncident
import configuration as _conf
import utilities as _util
import widgets as _widg

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _component_list_edit(cell, path, __new_text, position, model):
    """
    Function to respond to component list gtk.TreeView() gtk.CellRenderer()
    editing.

    @param cell: the gtk.CellRenderer() that was edited.
    @type cell: gtk.CellRenderer
    @param path: the gtk.TreeView() path of the gtk.CellRenderer() that was
                 edited.
    @type path: string
    @param __new_text: the new text in the edited gtk.CellRenderer().
    @type __new_text: string
    @param position: the column position of the edited gtk.CellRenderer().
    @type position: integer
    @param model: the gtk.TreeModel() the edited gtk.CellRenderer() belongs to.
    @type model: gtk.TreeModel
    @return: False if successful or True if an error is encountered.
    @rtype: boolean
    """

    value = not cell.get_active()
    model[path][position] = value

    if position == 1:                   # Initial installation.
        model[path][2] = 0
        model[path][3] = 0
        model[path][4] = 0
        model[path][5] = 0
        model[path][6] = 0
    elif position == 2:                 # Failure.
        model[path][1] = 0
        model[path][3] = 0
        model[path][4] = 0
        model[path][5] = 0
        model[path][6] = 0
    elif position == 3:                 # Suspension (right).
        model[path][1] = 0
        model[path][2] = 0
        model[path][4] = 0
        model[path][5] = 0
        model[path][6] = 0
    elif position == 4:                 # OCC fault.
        model[path][1] = 0
        model[path][2] = 0
        model[path][3] = 0
        model[path][5] = 0
        model[path][6] = 0
    elif position == 5:                 # CND/NFF fault.
        model[path][1] = 0
        model[path][2] = 0
        model[path][3] = 0
        model[path][4] = 0
        model[path][6] = 0
    elif position == 6:                 # Interval censored.
        model[path][1] = 0
        model[path][2] = 0
        model[path][3] = 0
        model[path][4] = 0
        model[path][5] = 0
    elif position == 7:                 # Use operating time.
        model[path][8] = 0
    elif position == 8:                 # Use calendar time.
        model[path][7] = 0

    return False


class Incident(object):
    """
    The Incident class is used to represent the field incidents tasks logged
    against a system being analyzed.
    """

    def __init__(self, application):
        """
        Initializes the Incident class.

        @param application: the current instance of the RTK application.
        """

        # Define private Incident class scalar attributes.
        self._app = application

        # Define private Incident class dictionary attributes.
        self._dic_category = {"": 0}
        self._dic_type = {"": 0}
        self._dic_criticality = {"": 0}
        self._dic_detection_method = {"": 0}
        self._dic_status = {"": 0}
        self._dic_life_cycle = {"": 0}
        self._dic_users = {"": 0}

        # Define private Incident class list attributes.
        self._lst_col_order = []

        # Define public Incident class scalar attributes.
        self.revision_id = 0
        self.incident_id = 0
        self.incident_category = ''
        self.incident_type = ''
        self.short_description = ''
        self.detail_description = ''
        self.criticality = ''
        self.detection_method = ''
        self.remarks = ''
        self.status = ''
        self.test = ''
        self.test_case = ''
        self.execution_time = 0.0
        self.unit_id = ''
        self.cost = 0.0
        self.incident_age = 0.0
        self.hardware_id = 0
        self.software_id = 0
        self.request_by = ''
        self.request_date = 0
        self.reviewed = False
        self.review_by = ''
        self.review_date = 0
        self.approved = False
        self.approve_by = ''
        self.approve_date = 0
        self.closed = False
        self.close_by = ''
        self.close_date = 0
        self.life_cycle = ''
        self.analysis = ''
        self.accepted = False

        self.n_incidents = 0

        # Define public Incident class dictionary attributes.

        # Define public Incident class list attributes.

        # Create the main Incident class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Incidents', 14, self._app,
                                                    None, _conf.RTK_COLORS[12],
                                                    _conf.RTK_COLORS[13])

        # Dataset class Work Book toolbar widgets.
        self.chkAllRevisions = _widg.make_check_button(_(u"Include incidents "
                                                         u"from all "
                                                         u"revisions"))

        # Create the Program Incident page widgets.
        self.btnIncidentDate = _widg.make_button(height=25, width=25,
                                                 label="...", image='calendar')

        self.chkAccepted = _widg.make_check_button(label=_(u"Accepted"))
        self.chkReviewed = _widg.make_check_button(label=_(u"Reviewed"))

        self.cmbHardware = _widg.make_combo()
        self.cmbSoftware = _widg.make_combo()
        self.cmbCategory = _widg.make_combo()
        self.cmbType = _widg.make_combo()
        self.cmbStatus = _widg.make_combo()
        self.cmbCriticality = _widg.make_combo()
        self.cmbLifeCycle = _widg.make_combo()
        self.cmbRequestBy = _widg.make_combo()

        self.tvwComponentList = gtk.TreeView()

        self.txtID = _widg.make_entry(width=100, editable=False)
        self.txtRequestDate = _widg.make_entry(width=100, editable=False)
        self.txtAge = _widg.make_entry(width=100, editable=False)
        self.txtShortDescription = _widg.make_entry(width=550)

        self.txtLongDescription = _widg.make_text_view(width=550, height=200)
        self.txtRemarks = _widg.make_text_view(width=550, height=200)

        # Create the Incident Analysis page widgets.
        self.btnReviewDate = _widg.make_button(height=25, width=25,
                                               label="...", image='calendar')
        self.btnApproveDate = _widg.make_button(height=25, width=25,
                                                label="...", image='calendar')
        self.btnClosureDate = _widg.make_button(height=25, width=25,
                                                label="...", image='calendar')

        self.cmbDetectionMethod = _widg.make_combo()
        self.cmbReviewBy = _widg.make_combo()
        self.cmbApproveBy = _widg.make_combo()
        self.cmbCloseBy = _widg.make_combo()

        self.txtTest = _widg.make_entry()
        self.txtTestCase = _widg.make_entry()
        self.txtExecutionTime = _widg.make_entry(width=100)
        self.txtAnalysis = _widg.make_text_view(width=550, height=200)
        self.txtReviewDate = _widg.make_entry(width=100, editable=False)
        self.txtApproveDate = _widg.make_entry(width=100, editable=False)
        self.txtCloseDate = _widg.make_entry(width=100, editable=False)

        # Put it all together.
        _toolbar = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxIncident = gtk.VBox()
        self.vbxIncident.pack_start(_toolbar, expand=False)
        self.vbxIncident.pack_start(self.notebook)

        #self.notebook.connect('switch-page', self._notebook_page_switched)

    def create_tree(self):
        """
        Creates the Incident class gtk.TreeView() and connects it to callback
        functions to handle editing.

        @return _scrollwindow: the gtk.ScrolledWindow() container holding the
                               Dataset class gtk.TreeView().
        @rtype: gtk.ScrolledWindow
        """

        self.treeview.set_tooltip_text(_("Displays a list of Program "
                                         "incidents."))
        self.treeview.set_enable_tree_lines(True)
        self.treeview.set_search_column(0)
        self.treeview.set_reorderable(True)

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)

        return _scrollwindow

    def _create_toolbar(self):
        """
        Method to create the gtk.Toolbar() for the Incident class Work Book.

        @return: _toolbar
        @rtype: gtk.Toolbar
        """

        _toolbar = gtk.Toolbar()

        _pos = 0

        # Add item menu.
        _button = gtk.MenuToolButton(None, label="")
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Incident"))
        _menu_item.set_tooltip_text(_(u"Add a new incident to the open RTK "
                                      u"Program database."))
        _menu_item.connect('activate', AddIncident, self._app)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Component"))
        _menu_item.set_tooltip_text(_(u"Adds a component to the selected "
                                      u"incident."))
        _menu_item.connect('activate', self._add_component)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Remove item button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        _button.set_icon_widget(_image)
        _button.set_name('Remove')
        _button.connect('clicked', self._delete_component)
        _button.set_tooltip_text(_(u"Deletes the selected component from the "
                                   u"selected field incident."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Save results button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        _button.set_icon_widget(_image)
        _button.set_name('Save')
        _button.connect('clicked', self._save_incident)
        _button.set_tooltip_text(_(u"Saves the currently selected incident "
                                   u"to the open RTK Program database."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Create a filter button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/filter.png')
        _button.set_icon_widget(_image)
        _button.set_name('Filter')
        _button.connect('clicked', FilterIncident, self._app)
        _button.set_tooltip_text(_(u"Launches the Program Incident filter "
                                   u"assistant."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Create an import button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/db-import.png')
        _button.set_icon_widget(_image)
        _button.set_name('Import')
        _button.connect('clicked', ImportIncident, self._app)
        _button.set_tooltip_text(_(u"Launches the Program Incident import "
                                   u"assistant."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Create an export button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/db-export.png')
        _button.set_icon_widget(_image)
        _button.set_name('Export')
        #_button.connect('clicked', ExportIncident, self._app)
        _button.set_tooltip_text(_(u"Launches the Program Incident export "
                                   u"assistant."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Create a data set creation button.
        _button = gtk.ToolButton()
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/wizard.png')
        _button.set_icon_widget(_image)
        _button.set_name('Data Set')
        _button.connect('clicked', CreateDataSet, self._app)
        _button.set_tooltip_text(_(u"Launches the Data Set creation "
                                   u"assistant."))
        _toolbar.insert(_button, _pos)
        _pos += 1

        # Add a checkbutton to allow the user to load all incidents from all
        # revisions when checked.  The default will be to leave this unchecked.
        self.chkAllRevisions.set_tooltip_text(_(u"Whether or not to include "
                                                u"incidents from all "
                                                u"revisions (checked) or only "
                                                u"the currently selected "
                                                u"revision (un-checked)."))
        self.chkAllRevisions.set_active(False)
        _alignment = gtk.Alignment(xalign=0.5, yalign=0.5)
        _alignment.add(self.chkAllRevisions)
        _toolitem = gtk.ToolItem()
        _toolitem.add(_alignment)
        _toolbar.insert(_toolitem, _pos)
        self.chkAllRevisions.connect('toggled', self.load_tree)

        _toolbar.show()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Incident class gtk.Notebook().

        @return: _notebook
        @rtype: gtk.Notebook
        """

        def _create_incident_details_page(self, notebook):
            """
            Function to create the Incident class gtk.Notebook() page for
            displaying general information related to the selected incident.

            @param self: the current instance of a Incident class.
            @type rtk.Incident
            @param notebook: the Incident class gtk.Notebook() widget.
            @type notebook: gtk.Notebook
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox = gtk.HBox()

            _vpaned = gtk.VPaned()

            # Build quadrant 1 (upper left).
            _fixed1 = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed1)

            _frame = _widg.make_frame(label=_(u"Field Incident Details"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _vpaned.pack1(_frame, True, True)

            # Build quadrant 2 (lower left).
            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add(self.tvwComponentList)

            _frame = _widg.make_frame(label=_(u"Component Information"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _vpaned.pack2(_frame, True, True)

            _hbox.pack_start(_vpaned)

            # Build quadrant 3 (upper right).
            _fixed3 = gtk.Fixed()

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(_fixed3)

            _frame = _widg.make_frame(label=_(u"Incident Descriptions"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _hbox.pack_start(_frame)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display analysis input information. #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the gtk.ComboBox() widgets in quadrant #1.
            _query = "SELECT fld_incident_cat_name FROM tbl_incident_category"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbCategory, _results)
            for i in range(len(_results)):
                self._dic_category[_results[i][0]] = i + 1

            _query = "SELECT fld_incident_type_name FROM tbl_incident_type"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbType, _results)
            for i in range(len(_results)):
                self._dic_type[_results[i][0]] = i + 1

            _query = "SELECT fld_status_name FROM tbl_status"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbStatus, _results)
            for i in range(len(_results)):
                self._dic_status[_results[i][0]] = i + 1

            _query = "SELECT fld_criticality_name FROM tbl_criticality"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbCriticality, _results)
            for i in range(len(_results)):
                self._dic_criticality[_results[i][0]] = i + 1

            _query = "SELECT fld_lifecycle_name FROM tbl_lifecycles"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbLifeCycle, _results)
            for i in range(len(_results)):
                self._dic_life_cycle[_results[i][0]] = i + 1

            _query = "SELECT fld_user_lname || ', ' || fld_user_fname \
                      FROM tbl_users \
                      ORDER BY fld_user_lname ASC"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbRequestBy, _results)
            for i in range(len(_results)):
                self._dic_users[_results[i][0]] = i + 1

            # Set the labels on the left half.
            _labels = [_(u"Incident ID:"), _(u"Incident Category:"),
                       _(u"Incident Type:"), _(u"Life Cycle:"),
                       _(u"Incident Criticality:"), _(u"Affected Hardware:"),
                       _(u"Affected Software:")]
            (_x_pos11, _y_pos11) = _widg.make_labels(_labels, _fixed1, 5, 5)
            _x_pos11 += 20

            # Set the labels on the right half.
            _labels = [_(u"Reported By:"), _(u"Date Opened:"),
                       _(u"Incident Age:"), _(u"Incident Status:")]
            (_x_pos12, _y_pos12) = _widg.make_labels(_labels, _fixed1,
                                                     _x_pos11 + 205, 35)
            _x_pos12 += 380

            # Set the tooltips for the widgets in quedrant #1.
            self.btnIncidentDate.set_tooltip_text(_(u"Select the date the "
                                                    u"incident occurred."))

            self.chkAccepted.set_tooltip_text(_(u"Displays whether the field "
                                                u"incident has been accepted "
                                                u"by the responsible owner."))
            self.chkReviewed.set_tooltip_text(_(u"Displays whether the field "
                                                u"incident has been reviewed "
                                                u"by the responsible owner."))

            self.cmbCategory.set_tooltip_text(_(u"Selects and displays the "
                                                u"category of the selected "
                                                u"incident."))
            self.cmbType.set_tooltip_text(_(u"Selects and displays the type "
                                            u"of incident for the selected "
                                            u"incident."))
            self.cmbStatus.set_tooltip_text(_(u"Displays the status of the "
                                              u"selected incident."))
            self.cmbCriticality.set_tooltip_text(_(u"Displays the criticality "
                                                   u"of the selected "
                                                   u"incident."))
            self.cmbLifeCycle.set_tooltip_text(_(u"Displays the product life "
                                                 u"cycle during which the "
                                                 u"incident occurred."))
            self.cmbRequestBy.set_tooltip_text(_(u"Displays the name of the "
                                                 u"individual reporting the "
                                                 u"incident."))

            self.txtID.set_tooltip_text(_(u"Displays the unique code for the "
                                          u"selected incident."))
            self.txtRequestDate.set_tooltip_text(_(u"Displays the date the "
                                                   u"incident was opened."))
            self.txtAge.set_tooltip_text(_(u"Displays the age of the incident "
                                           u"in days."))

            # Place the quadrant #1 widgets.
            _fixed1.put(self.txtID, _x_pos11, _y_pos11[0])
            _fixed1.put(self.chkAccepted, _x_pos11 + 110, _y_pos11[0])
            _fixed1.put(self.chkReviewed, _x_pos11 + 220, _y_pos11[0])
            _fixed1.put(self.cmbCategory, _x_pos11, _y_pos11[1])
            _fixed1.put(self.cmbType, _x_pos11, _y_pos11[2])
            _fixed1.put(self.cmbLifeCycle, _x_pos11, _y_pos11[3])
            _fixed1.put(self.cmbCriticality, _x_pos11, _y_pos11[4])
            _fixed1.put(self.cmbHardware, _x_pos11, _y_pos11[5])
            _fixed1.put(self.cmbSoftware, _x_pos11, _y_pos11[6])

            _fixed1.put(self.cmbRequestBy, _x_pos12, _y_pos12[0])
            _fixed1.put(self.txtRequestDate, _x_pos12, _y_pos12[1])
            _fixed1.put(self.btnIncidentDate, _x_pos12 + 105, _y_pos12[1])
            _fixed1.put(self.txtAge, _x_pos12, _y_pos12[2])
            _fixed1.put(self.cmbStatus, _x_pos12, _y_pos12[3])

            _fixed1.show_all()

            # Connect the quadrant #1 widgets' signals to callback functions.
            self.btnIncidentDate.connect('button-release-event', _util.date_select,
                                         self.txtRequestDate)

            self.chkReviewed.connect('toggled', self._callback_check,
                                     self._lst_col_order[20])
            self.chkAccepted.connect('toggled', self._callback_check,
                                     self._lst_col_order[31])

            self.cmbCategory.connect('changed', self._callback_combo,
                                     self._lst_col_order[2])
            self.cmbType.connect('changed', self._callback_combo,
                                 self._lst_col_order[3])
            self.cmbCriticality.connect('changed', self._callback_combo,
                                        self._lst_col_order[6])
            self.cmbStatus.connect('changed', self._callback_combo,
                                   self._lst_col_order[9])
            self.cmbRequestBy.connect('changed', self._callback_combo,
                                      self._lst_col_order[18])
            self.cmbLifeCycle.connect('changed', self._callback_combo,
                                      self._lst_col_order[29])

            self.txtRequestDate.connect('focus-out-event',
                                        self._callback_entry, 'date',
                                        self._lst_col_order[19])

            # Place the quadrant 2 (lower left) widgets.
            _model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_INT,
                                   gobject.TYPE_INT, gobject.TYPE_FLOAT,
                                   gobject.TYPE_FLOAT)
            self.tvwComponentList.set_model(_model)

            _heading = [_(u"Part\nNumber"), _(u"Initial\nInstall"),
                        _(u"Failure"), _(u"Suspension"), _(u"OOT\nFailure"),
                        _("CND/NFF"), _(u"Interval\nCensored"),
                        _(u"Use\nOperating\nTime"), _(u"Use\nCalendar\nTime"),
                        _(u"Time to\nFailure"), _(u"Age at\nFailure")]
            for i in range(len(_heading)):
                _column = gtk.TreeViewColumn()

                if i in [0, 9, 10]:
                    _cell = gtk.CellRendererText()
                    _cell.set_property('editable', 0)
                    _cell.set_property('background', 'light gray')
                    _cell.set_property('foreground', 'black')
                    _column.set_attributes(_cell, text=i)
                else:
                    _cell = gtk.CellRendererToggle()
                    _cell.set_property('activatable', 1)
                    _cell.connect('toggled', _component_list_edit,
                                  None, i, _model)
                    _column.set_attributes(_cell, active=i)

                _label = _widg.make_column_heading(_heading[i])
                _column.set_widget(_label)
                _column.pack_start(_cell, True)
                _column.set_clickable(True)
                _column.set_resizable(True)
                _column.set_sort_column_id(i)
                self.tvwComponentList.append_column(_column)

            # Set the tooltips for the widgets in quedrant #3.
            self.txtShortDescription.set_tooltip_text(_(u"Short problem "
                                                        u"description."))

            # Place the quadrant #3 (upper right) widgets.
            _label = _widg.make_label(_(u"Brief Problem Description:"),
                                      width=225)
            _fixed3.put(_label, 5, 5)
            _fixed3.put(self.txtShortDescription, 5, 35)

            _label = _widg.make_label(_(u"Detailed Problem Description:"),
                                      width=225)
            _fixed3.put(_label, 5, 65)
            _fixed3.put(self.txtLongDescription, 5, 100)

            _label = _widg.make_label(_(u"Remarks:"))
            _fixed3.put(_label, 5, 305)
            _fixed3.put(self.txtRemarks, 5, 330)

            self.txtShortDescription.connect('focus-out-event',
                                             self._callback_entry, 'text',
                                             self._lst_col_order[4])
            self.txtLongDescription.get_child().get_child().connect(
                'focus-out-event', self._callback_entry, 'text',
                self._lst_col_order[5])
            self.txtRemarks.get_child().get_child().connect(
                'focus-out-event', self._callback_entry, 'text',
                self._lst_col_order[8])

            _fixed3.show_all()

            # Connect the quadrant #3 widgets' signals to callback functions.

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Incident\nDetails") + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays details about the selected "
                                      u"incident."))

            notebook.insert_page(_hbox, tab_label=_label, position=-1)

            return False

        def _create_incident_analysis_page(self, notebook):
            """
            Function to create the Incident class gtk.Notebook() page for
            displaying the analysis of the selected incident.

            @param self: the current instance of the Incident class.
            @type self: rtk.Incident
            @param notebook: the Incident class gtk.Notebook() widget.
            @type notebook: gtk.Notebook
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hbox = gtk.HBox()
            _hbox2 = gtk.HBox()
            _hbox.pack_start(_hbox2)

            _fixed1 = gtk.Fixed()
            _hbox2.pack_start(_fixed1, expand=False)

            _scrollwindow = gtk.ScrolledWindow()
            _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scrollwindow.add_with_viewport(self.txtAnalysis)

            _frame = _widg.make_frame(label=_(u"Incident Analysis"))
            _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _frame.add(_scrollwindow)

            _hbox2.pack_end(_frame)

            _fixed2 = gtk.Fixed()
            _hbox.pack_end(_fixed2, expand=False)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display analysis input information. #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the gtk.ComboBox() widgets in quadrant #1.
            _results = [[_(u"Code Review")], [_(u"Error/Anomaly Analysis")],
                        [_(u"Structure Analysis")], [_(u"Random Testing")],
                        [_(u"Functional Testing")], [_(u"Branch Testing")]]
            _widg.load_combo(self.cmbDetectionMethod, _results)
            for i in range(len(_results)):
                self._dic_detection_method[_results[i][0]] = i + 1

            # Load the gtk.ComboBox() widgets in quadrant #3.
            _query = "SELECT fld_user_lname || ', ' || fld_user_fname \
                      FROM tbl_users \
                      ORDER BY fld_user_lname ASC"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _widg.load_combo(self.cmbReviewBy, _results)
            _widg.load_combo(self.cmbApproveBy, _results)
            _widg.load_combo(self.cmbCloseBy, _results)

            # Set the tooltips for the widgets in quedrant #1.
            self.cmbDetectionMethod.set_tooltip_markup(_(u"Displays the "
                                                         u"method used to "
                                                         u"detect the "
                                                         u"reported problem."))

            self.txtTest.set_tooltip_markup(_(u"Displays the software test "
                                              u"being executed when the "
                                              u"reported problem was "
                                              u"discovered."))
            self.txtTestCase.set_tooltip_markup(_(u"Displays the software "
                                                  u"test case being executed "
                                                  u"when the reported problem "
                                                  u"was discovered."))
            self.txtExecutionTime.set_tooltip_markup(_(u"Displays the time "
                                                       u"(CPU or calendar "
                                                       u"time) into the test "
                                                       u"when the reported "
                                                       u"problem was "
                                                       u"discovered."))

            # Place the quadrant #1 widgets.
            _labels = [_(u"Detection Method:"), _(u"Found in Test:"),
                       _(u"Found in Test Case:"), _(u"Execution Time:")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed1, 5, 5)
            _x_pos += 20

            _fixed1.put(self.cmbDetectionMethod, _x_pos, _y_pos[0])
            _fixed1.put(self.txtTest, _x_pos, _y_pos[1])
            _fixed1.put(self.txtTestCase, _x_pos, _y_pos[2])
            _fixed1.put(self.txtExecutionTime, _x_pos, _y_pos[3])

            self.cmbDetectionMethod.connect('changed', self._callback_combo,
                                            self._lst_col_order[7])

            self.txtTest.connect('focus-out-event', self._callback_entry,
                                 'text', self._lst_col_order[10])
            self.txtTestCase.connect('focus-out-event', self._callback_entry,
                                     'text', self._lst_col_order[11])
            self.txtExecutionTime.connect('focus-out-event',
                                          self._callback_entry, 'text',
                                          self._lst_col_order[12])

            # Set the tooltips for the widgets in quedrant #3.
            self.btnClosureDate.set_tooltip_text(_(u"Select the date the "
                                                   u"incident analysis was "
                                                   u"reviewed."))
            self.btnApproveDate.set_tooltip_text(_(u"Select the date the "
                                                   u"incident analysis was "
                                                   u"approved."))
            self.btnClosureDate.set_tooltip_text(_(u"Select the date the "
                                                   u"incident was closed."))

            self.cmbReviewBy.set_tooltip_text(_(u"Displays the name of the "
                                                u"individual who reviewed the "
                                                u"incident analysis."))
            self.cmbApproveBy.set_tooltip_text(_(u"Displays the name of the "
                                                 u"individual who approved "
                                                 u"the analysis."))
            self.cmbCloseBy.set_tooltip_text(_(u"Displays the name of the "
                                               u"individual who closed the "
                                               u"incident."))

            self.txtReviewDate.set_tooltip_text(_(u"Displays the date the "
                                                  u"incident analysis was "
                                                  u"reviewed."))
            self.txtApproveDate.set_tooltip_text(_(u"Displays the date the "
                                                   u"analysis was approved."))
            self.txtCloseDate.set_tooltip_text(_(u"Displays the date the "
                                                 u"incident was closed."))

            # Place the quadrant #3 widgets.
            _labels = [_(u"Reviewed By:"), _(u"Date Reviewed:"),
                       _(u"Approved By:"), _(u"Date Approved:"),
                       _(u"Closed By:"), _(u"Date Closed:")]
            (_x_pos, _y_pos) = _widg.make_labels(_labels, _fixed2, 5, 5)
            _x_pos += 20

            _fixed2.put(self.cmbReviewBy, _x_pos, _y_pos[0])
            _fixed2.put(self.txtReviewDate, _x_pos, _y_pos[1])
            _fixed2.put(self.btnReviewDate, _x_pos + 105, _y_pos[1])
            _fixed2.put(self.cmbApproveBy, _x_pos, _y_pos[2])
            _fixed2.put(self.txtApproveDate, _x_pos, _y_pos[3])
            _fixed2.put(self.btnApproveDate, _x_pos + 105, _y_pos[3])
            _fixed2.put(self.cmbCloseBy, _x_pos, _y_pos[4])
            _fixed2.put(self.txtCloseDate, _x_pos, _y_pos[5])
            _fixed2.put(self.btnClosureDate, _x_pos + 105, _y_pos[5])

            # Connect the quadrant #1 widgets' signals to callback functions.
            self.btnReviewDate.connect('button-release-event',
                                       _util.date_select, self.txtReviewDate)
            self.btnApproveDate.connect('button-release-event',
                                        _util.date_select, self.txtApproveDate)
            self.btnClosureDate.connect('button-release-event',
                                        _util.date_select, self.txtCloseDate)

            self.cmbReviewBy.connect('changed', self._callback_combo,
                                     self._lst_col_order[21])
            self.cmbApproveBy.connect('changed', self._callback_combo,
                                      self._lst_col_order[24])
            self.cmbCloseBy.connect('changed', self._callback_combo,
                                    self._lst_col_order[27])

            self.txtAnalysis.get_child().get_child().connect(
                'focus-out-event', self._callback_entry, 'text',
                self._lst_col_order[30])

            # Insert the tab.
            _label = gtk.Label()
            _label.set_markup("<span weight='bold'>" +
                              _(u"Incident\nAnalysis") + "</span>")
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.show_all()
            _label.set_tooltip_text(_(u"Displays the analysis of the selected "
                                      u"incident."))

            notebook.insert_page(_hbox, tab_label=_label, position=-1)

            return False

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

        _create_incident_details_page(self, _notebook)
        _create_incident_analysis_page(self, _notebook)

        return _notebook

    def load_tree(self, __button=None):
        """
        Loads the Incident class gtk.TreeModel() with the list of Program
        incidents.

        @param __button: the gtkCheckButton() that called this method.  Needed
                         to allow the 'All Revisions' gtk.CheckButton() to
                         call this method.
        @type __button: gtk.CheckButton
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        # Select all the program incidents.  If the 'All Revisions'
        # gtk.CheckButton() is active, get all incidents regardless of
        # revision.  Otherwise, get only incidents associated with the
        # selected revision.
        if self.chkAllRevisions.get_active():
            _query = "SELECT * FROM tbl_incident \
                      ORDER BY fld_incident_id"
        else:
            _query = "SELECT * FROM tbl_incident \
                      WHERE fld_revision_id=%d \
                      ORDER BY fld_incident_id" % \
                     self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)
        try:
            self.n_incidents = len(_results)
        except ValueError:
            _util.rtk_information(_(u"There are no incidents matching the "
                                    u"specified criteria."))
            return True

        _model = self.treeview.get_model()
        _model.clear()
        for i in range(self.n_incidents):
            _data = [_results[i][0], _results[i][1], _results[i][2],
                     _results[i][3], _results[i][4], _results[i][5],
                     _results[i][6], _results[i][7], _results[i][8],
                     _results[i][9], _results[i][10], _results[i][11],
                     _results[i][12], _results[i][13], _results[i][14],
                     _results[i][15], _results[i][16], _results[i][17],
                     _results[i][18], _util.ordinal_to_date(_results[i][19]),
                     _results[i][20], _results[i][21],
                     _util.ordinal_to_date(_results[i][22]), _results[i][23],
                     _results[i][24], _util.ordinal_to_date(_results[i][25]),
                     _results[i][26], _results[i][27],
                     _util.ordinal_to_date(_results[i][28]), _results[i][29],
                     _results[i][30], _results[i][31]]
            try:
                _model.append(None, _data)
            except TypeError:
                pass

        if _model.get_iter_root() is not None:
            _path = _model.get_path(_model.get_iter_root())
            self.treeview.expand_all()
            self.treeview.set_cursor('0', None, False)
            _col = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _col)

        #query = "SELECT fld_name \
        #         FROM tbl_system \
        #         WHERE fld_parent_assembly='0' \
        #         AND fld_part=0"
        #results = self._app.DB.execute_query(query,
        #                                     None,
        #                                     self._app.ProgCnx)
        #_widg.load_combo(self.cmbSystem, results, simple=True)

        return False

    def load_notebook(self):
        """
        Method to load the Incident class gtk.Notebook().

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        def _load_incident_details_page(self):
            """
            Function to load the gtk.Widget() with information about the
            selected incident.
            """

            self.txtID.set_text(str(self.incident_id))
            self.chkReviewed.set_active(self.reviewed)
            self.chkAccepted.set_active(self.accepted)

            try:
                self.cmbCategory.set_active(
                    self._dic_category[self.incident_category])
            except KeyError:
                self.cmbCategory.set_active(0)
            try:
                self.cmbType.set_active(self._dic_type[self.incident_type])
            except KeyError:
                self.cmbType.set_active(0)
            try:
                self.cmbCriticality.set_active(
                    self._dic_criticality[self.criticality])
            except KeyError:
                self.cmbCriticality.set_active(0)
            try:
                self.cmbLifeCycle.set_active(
                    self._dic_life_cycle[self.life_cycle])
            except KeyError:
                self.cmbLifeCycle.set_active(0)
            self.cmbHardware.set_active(self.hardware_id)
            self.cmbSoftware.set_active(self.software_id)

            try:
                self.cmbRequestBy.set_active(self._dic_users[self.request_by])
            except KeyError:
                self.cmbRequestBy.set_active(0)
            _date = _util.ordinal_to_date(self.request_date)
            self.txtRequestDate.set_text(str(_date))
            try:
                self.cmbStatus.set_active(self._dic_status[self.status])
            except KeyError:
                self.cmbStatus.set_active(0)
            self.txtAge.set_text(str(self.incident_age))

            self.txtShortDescription.set_text(self.short_description)
            _buffer = self.txtLongDescription.get_child().get_child().get_buffer()
            _buffer.set_text(self.detail_description)
            _buffer = self.txtRemarks.get_child().get_child().get_buffer()
            _buffer.set_text(self.remarks)

            return False

        def _load_incident_analysis_page(self):
            """
            Function to load the gtk.Widget() with information about the
            analysis of the selected incident.
            """
# TODO: Change detection method from varchar to integer.
            #self.cmbDetectionMethod.set_active(self.detection_method)
            self.txtTest.set_text(self.test)
            self.txtTestCase.set_text(self.test_case)
            self.txtExecutionTime.set_text(str(self.execution_time))

            _buffer = self.txtAnalysis.get_child().get_child().get_buffer()
            _buffer.set_text(_util.none_to_string(self.analysis))

            try:
                self.cmbReviewBy.set_active(self._dic_users[self.review_by])
            except KeyError:
                self.cmbReviewBy.set_active(0)
            _date = _util.ordinal_to_date(self.review_date)
            self.txtReviewDate.set_text(str(_date))

            try:
                self.cmbApproveBy.set_active(self._dic_users[self.approve_by])
            except KeyError:
                self.cmbApproveBy.set_active(0)
            _date = _util.ordinal_to_date(self.approve_date)
            self.txtApproveDate.set_text(str(_date))

            try:
                self.cmbCloseBy.set_active(self._dic_users[self.close_by])
            except KeyError:
                self.cmbCloseBy.set_active(0)
            _date = _util.ordinal_to_date(self.close_date)
            self.txtCloseDate.set_text(str(_date))

            return False

        (_model, _row) = self.treeview.get_selection().get_selected()

        if _row is not None:
            _load_incident_details_page(self)
            _load_incident_analysis_page(self)
            self._load_component_list()

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxIncident)
        self._app.winWorkBook.show_all()

        _title = _(u"RTK Work Book: Program Incidents (%d Incidents)") % \
                   self.n_incidents
        self._app.winWorkBook.set_title(_title)

        return False

    def _load_component_list(self):
        """
        Method to load the component list for the selected incident.

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        _model = self.tvwComponentList.get_model()
        _model.clear()

        _query = "SELECT fld_part_num, fld_initial_installation, fld_failure, \
                         fld_suspension, fld_occ_fault, fld_cnd_nff, \
                         fld_interval_censored, fld_use_op_time, \
                         fld_use_cal_time, fld_ttf, fld_age_at_incident \
                  FROM tbl_incident_detail \
                  WHERE fld_incident_id='%s'" % self.incident_id
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        try:
            _n_components = len(_results)
        except TypeError:
            _n_components = 0

        for i in range(_n_components):
            _model.append(_results[i])

        return False

    def update_tree(self):
        """
        Method to update the Incident class gtk.TreeModel().

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        _model.set_value(_row, self._lst_col_order[2], self.incident_category)

        return False

    def _update_attributes(self):
        """
        Method to update the Incident class attributes.

        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        self.incident_id = _model.get_value(_row, self._lst_col_order[1])
        self.incident_category = _model.get_value(_row, self._lst_col_order[2])
        self.incident_type = _model.get_value(_row, self._lst_col_order[3])
        self.short_description = _model.get_value(_row, self._lst_col_order[4])
        self.detail_description = _model.get_value(_row, self._lst_col_order[5])
        self.criticality = _model.get_value(_row, self._lst_col_order[6])
        self.detection_method = _model.get_value(_row, self._lst_col_order[7])
        self.remarks = _model.get_value(_row, self._lst_col_order[8])
        self.status = _model.get_value(_row, self._lst_col_order[9])
        self.test = _model.get_value(_row, self._lst_col_order[10])
        self.test_case = _model.get_value(_row, self._lst_col_order[11])
        self.execution_time = _model.get_value(_row, self._lst_col_order[12])
        self.unit_id = _model.get_value(_row, self._lst_col_order[13])
        self.cost = _model.get_value(_row, self._lst_col_order[14])
        self.incident_age = _model.get_value(_row, self._lst_col_order[15])
        self.hardware_id = _model.get_value(_row, self._lst_col_order[16])
        self.software_id = _model.get_value(_row, self._lst_col_order[17])
        self.request_by = _model.get_value(_row, self._lst_col_order[18])
        self.request_date = _util.date_to_ordinal(
            _model.get_value(_row, self._lst_col_order[19]))
        self.reviewed = _model.get_value(_row, self._lst_col_order[20])
        self.review_by = _model.get_value(_row, self._lst_col_order[21])
        self.review_date = _util.date_to_ordinal(
            _model.get_value(_row, self._lst_col_order[22]))
        self.approved = _model.get_value(_row, self._lst_col_order[23])
        self.approve_by = _model.get_value(_row, self._lst_col_order[24])
        self.approve_date = _util.date_to_ordinal(
            _model.get_value(_row, self._lst_col_order[25]))
        self.closed = _model.get_value(_row, self._lst_col_order[26])
        self.close_by = _model.get_value(_row, self._lst_col_order[27])
        self.close_date = _util.date_to_ordinal(
            _model.get_value(_row, self._lst_col_order[28]))
        self.life_cycle = _model.get_value(_row, self._lst_col_order[29])
        self.analysis = _model.get_value(_row, self._lst_col_order[30])
        self.accepted = _model.get_value(_row, self._lst_col_order[31])

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Incident class
        treeview.

        @param treeview: the Incident class gtk.TreeView().
        @type treeview: gtk.TreeView
        @param event: a gtk.gdk.Event() that called this function (the
                      important attribute is which mouse button was clicked).
                      1 = left
                      2 = scrollwheel
                      3 = right
                      4 = forward
                      5 = backward
                      8 =
                      9 =
        @type event: gtk.gdk.Event
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        if event.button == 1:
            self._treeview_row_changed(treeview, None, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, __treeview, __path, __column):
        """
        Callback function to handle events for the Incident class
        gtk.Treeview().  It is called whenever the Incident class
        gtk.TreeView() is clicked or a row is activated.

        @param __treeview: the Incident class gtk.TreeView().
        @type __treeview: gtk.TreeView
        @param __path: the path of the activated gtk.TreeIter() in the Incident
                       class gtk.TreeView().
        @type __path: string
        @param __column: the activated gtk.TreeViewColumn().
        @type __column: gtk.TreeViewColumn
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        if _row is not None:
            self._update_attributes()
            self.load_notebook()
            return False
        else:
            return True

    def _add_component(self, __widget):
        """
        Adds a new hardware item to the selected incident.

        @param __widget: the gtk.Widget() that called this function.
        @type __widget: gtk.Widget
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        _n_components = _util.add_items(title=_(u"RTK - Add Components to "
                                                u"Program Incident"),
                                        prompt=_(u"How many components to add "
                                                 u"to the selected program "
                                                 u"incident?"))

        if _n_components < 1:
            return True

        for i in range(_n_components):
            _component_name = "Component " + str(i)

            _query = "INSERT INTO tbl_incident_detail \
                      (fld_revision_id, fld_incident_id, fld_part_num) \
                      VALUES (%d, '%s', '%s')" % \
                     (self._app.REVISION.revision_id, self.incident_id,
                      _component_name)
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error adding component to field "
                                  u"incident %d.") % self.incident_id)
                return True

        self._load_component_list()

        return False

    def _delete_component(self, __button):
        """
        Deletes the currently selected component from the selected Program
        incident.

        @param __button: the gtk.ToolButton() that called this function.
        @type __button: gtk.ToolButton
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        (_model, _row) = self.tvwComponentList.get_selection().get_selected()

        _query = "DELETE FROM tbl_incident_detail \
                  WHERE fld_incident_id='%s' \
                  AND fld_part_num='%s'" % \
                 (self.incident_id, _model.get_value(_row, 0))
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            _util.rtk_error(_(u"Failed to delete component %s from field "
                              u"incident %d.") %
                            (_model.get_value(_row, 0), self.incident_id))
            return True

        self._load_component_list()

        return False

    def _save_incident(self, __widget):
        """
        Saves the Incident class gtk.TreeView() information for the selected
        Program incident to the open RTK Program database.

        @param __widget: the gtk.Widget() that called this method.
        @type __widget: gtk.Widget
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        def _save_line_item(self):
            """
            Saves the currently selected row in the Incident class
            gtk.TreeModel() to the open RTK Program database.

            @param model: the current instance of the RTK application.
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            _query = "UPDATE tbl_incident \
                      SET fld_incident_category='%s', fld_incident_type='%s', \
                          fld_short_description='%s', \
                          fld_long_description='%s', fld_criticality='%s', \
                          fld_detection_method='%s', fld_remarks='%s', \
                          fld_status='%s', fld_test_found='%s', \
                          fld_test_case='%s', fld_execution_time=%f, \
                          fld_unit='%s', fld_cost=%f, fld_incident_age=%d, \
                          fld_hardware_id=%d, fld_software_id=%d, \
                          fld_request_by='%s', fld_request_date=%d, \
                          fld_reviewed=%d, fld_reviewed_by='%s', \
                          fld_reviewed_date=%d, fld_approved=%d, \
                          fld_approved_by='%s', fld_approved_date=%d, \
                          fld_complete=%d, fld_complete_by='%s', \
                          fld_complete_date=%d, fld_life_cycle='%s', \
                          fld_analysis='%s', fld_accepted=%d \
                      WHERE fld_incident_id=%d" % \
                     (self.incident_category, self.incident_type,
                      self.short_description, self.detail_description,
                      self.criticality, self.detection_method,
                      self.remarks, self.status, self.test, self.test_case,
                      self.execution_time, self.unit_id, self.cost,
                      self.incident_age, self.hardware_id,
                      self.software_id, self.request_by,
                      self.request_date, self.reviewed, self.review_by,
                      self.review_date, self.approved, self.approve_by,
                      self.approve_date, self.closed, self.close_by,
                      self.close_date, self.life_cycle, self.analysis,
                      self.accepted, self.incident_id)
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error saving Program incident."))
                return True

            return False

        def _save_component_line_item(model, __path, row, self):
            """
            Saves each row in the Incident class component list gtk.TreeModel()
            to the open RTK Program database.

            @param model: the Incident class component list gtk.TreeModel().
            @type model: gtk.TreeModel
            @param __path: the path of the active row in the Incident class
                           component list gtk.TreeModel().
            @type __path: string
            @param row: the selected gtk.TreeIter() in the Incident class
                        component list gtk.TreeView().
            @type row: gtk.TreeIter
            @return: False if successful or True if an error is encountered.
            @rtype: boolean
            """

            #datetime.strptime(dt,"%Y-%m-%d").toordinal()
            _query = "UPDATE tbl_incident_detail \
                      SET fld_initial_installation=%d, \
                          fld_failure=%d, fld_suspension=%d, \
                          fld_occ_fault=%d, fld_cnd_nff=%d, \
                          fld_interval_censored=%d, \
                          fld_use_op_time=%d, fld_use_cal_time=%d, \
                          fld_ttf=%f \
                      WHERE fld_incident_id='%s'" % \
                     (model.get_value(row, 1), model.get_value(row, 2),
                      model.get_value(row, 3), model.get_value(row, 4),
                      model.get_value(row, 5), model.get_value(row, 6),
                      model.get_value(row, 7), model.get_value(row, 8),
                      model.get_value(row, 9), self.incident_id)

            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error saving field incident component list."))
                return True

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        _save_line_item(self)

        _model = self.tvwComponentList.get_model()
        _model.foreach(_save_component_line_item, self)

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _callback_check(self, check, index):
        """
        Callback function to retrieve and save Incident class gtk.CheckButton()
        changes.

        @param check: the gtk.CheckButton() that called this method.
        @type check: gtk.CheckButton
        @param index: the position in the Incident class component list
                      gtk.TreeModel().
        @type index: integer
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        if check.get_active():
            _value = 1
        else:
            _value = 0

        (_model, _row) = self.treeview.get_selection().get_selected()
        _model.set_value(_row, index, _value)

        self._update_attributes()

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save gtk.ComboBox() changes.

        @param combo: the gtk.ComboBox() that called this method.
        @type combo: gtk.ComboBox
        @param index: the position in the Incident class component list
                      gtk.TreeModel().
        @type index: integer
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        # Index     Field
        #   2       Incident category
        #   3       Incident type
        #   6       Incident criticality
        #   7       Detection method
        #   9       Incident status
        #  13       Affected unit ID
        #  16       Affected hardware ID
        #  17       Affected software ID
        #  18       Request By
        #  21       Reviewed By
        #  24       Approved By
        #  27       Complete By
        #  29       Life cycle
        (_model, _row) = self.treeview.get_selection().get_selected()
        _model.set_value(_row, index, combo.get_active_text())

        self._update_attributes()

        return False

    def _callback_entry(self, entry, __event, convert, index):
        """
        Callback function to retrieve and save gtk.Entry() changes.

        @param entry: the gtk.Entry() that called the function.
        @type entry: gtk.Entry
        @param __event: the gtk.gdk.Event() that called the function.
        @type __event: gtk.gdk.Event
        @param convert: the data type to convert the gtk.Entry() contents to.
        @type convert: string
        @param index: the position in the applicable gtk.TreeModel() associated
                      with the data from the calling gtk.Entry().
        @type index: integer
        @return: False if successful or True if an error is encountered.
        @rtype: boolean
        """

        from datetime import datetime

        if convert == 'text':
            if index == 5:
                _buffer = self.txtLongDescription.get_child().get_child().get_buffer()
                _text = _buffer.get_text(*_buffer.get_bounds())
            elif index == 8:
                _buffer = self.txtRemarks.get_child().get_child().get_buffer()
                _text = _buffer.get_text(*_buffer.get_bounds())
            elif index == 30:
                _buffer = self.txtAnalysis.get_child().get_child().get_buffer()
                _text = _buffer.get_text(*_buffer.get_bounds())
            else:
                _text = entry.get_text()

        elif convert == 'int':
            _text = int(entry.get_text())

        elif convert == 'float':
            _text = float(entry.get_text().replace('$', ''))

        elif convert == 'date':
            _text = datetime.strptime(entry.get_text(), '%Y-%m-%d').toordinal()

        (_model, _row) = self.treeview.get_selection().get_selected()
        _model.set_value(_row, index, _text)

        self._update_attributes()

        return False
