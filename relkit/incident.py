#!/usr/bin/env python
""" This is the Class that is used to represent and hold information related
    to Program incidents. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       incident.py is part of The RelKit Project
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

# Import other RelKit modules.
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg

# Add localization support.
import locale
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

import gettext
_ = gettext.gettext


class Incident:
    """
    The Incident class is used to represent the field incidents tasks logged
    against a system being analyzed.
    """

    # TODO: Write code to update notebook widgets when editing the Validation treeview.
    # TODO: Add tooltips to all widgets.
    _fi_tab_labels = [[_("Incident ID:"), _("Incident Type:"),
                       _("Incident Status:"), _("Date Opened:"),
                       _("Date Closed:"), _("Incident Age:"),
                       _("Affected Unit:"), _("Affected System:"),
                       _("Accepted"), _("Reviewed")],
                      [_("Brief Description:"), _("Long Description:"),
                       _("Closure Remarks:")],
                      [],
                      [_("Incident ID"), _("Incident Type"),
                       _("Short Description"), _("Long Description"),
                       _("Remarks"), _("Incident Date"), _("Closure Date"),
                       _("Incident Age"), _("Status"), _("Affected Unit"),
                       _("Affected System"), _("Is Accepted"),
                       _("Is Reviewed")]]

    n_attributes = 13

    def __init__(self, application):
        """
        Initializes the Incident Object.

        Keyword Arguments:
        application -- the RelKit application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.incident_id = 0
        self.n_incidents = 0
        self._col_order = []

# Create the Notebook for the SOFTWARE object.
        self.notebook = gtk.Notebook()
        if(_conf.TABPOS[2] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[2] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[2] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

# Create the Program Incident tab.
        self.btnIncidentDate = _widg.make_button(_height_=25, _width_=25,
                                                 _label_="...", _image_=None)
        self.btnClosureDate = _widg.make_button(_height_=25, _width_=25,
                                                _label_="...", _image_=None)

        self.chkAccepted = _widg.make_check_button(_label_=self._fi_tab_labels[0][8])
        self.chkReviewed = _widg.make_check_button(_label_=self._fi_tab_labels[0][9])

        self.cmbIncidentStatus = _widg.make_combo()
        self.cmbSystem = _widg.make_combo(simple=True)
        self.cmbFilterIncidentID = _widg.make_combo(_width_=100)

        self.tvwComponentList = gtk.TreeView()

        self.txtID = _widg.make_entry(_width_=100)
        self.txtIncidentType = _widg.make_entry(_width_=100)
        self.txtIncidentDate = _widg.make_entry(_width_=100)
        self.txtClosureDate = _widg.make_entry(_width_=100)
        self.txtIncidentAge = _widg.make_entry(_width_=100)
        self.txtUnit = _widg.make_entry(_width_=100)
        self.txtShortDescription = _widg.make_entry(_width_=550)
        self.txtTask = gtk.TextBuffer()
        self.txtLongDescription = gtk.TextBuffer()
        self.txtClosureRemarks = gtk.TextBuffer()
        if self._field_incident_widgets_create():
            self.debug_app._log.error("incident.py: Failed to create Field Incident widgets.")
        if self._field_incident_tab_create():
            self.debug_app._log.error("incident.py: Failed to create Field Incident tab.")

        self.vbxIncident = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxIncident.pack_start(toolbar, expand=False)
        self.vbxIncident.pack_start(self.notebook)

        #self.notebook.connect('switch-page', self._notebook_page_switched)

        self._ready = True

    def _toolbar_create(self):
        """
        Method to create the toolbar for the VALIDATAION Object work book.
        """

        toolbar = gtk.Toolbar()

        # Add item button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        button.connect('clicked', self._component_add)
        button.set_tooltip_text(_("Adds a component to the selected field incident."))
        toolbar.insert(button, 0)

        # Remove item button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_REMOVE)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.set_name('Remove')
        button.connect('clicked', self._component_delete)
        button.set_tooltip_text(_("Deletes the selected component from the selected field incident."))
        toolbar.insert(button, 1)

        # Save results button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.set_name('Save')
        button.connect('clicked', self._component_save)
        button.set_tooltip_text(_("Saves the list of components."))
        toolbar.insert(button, 2)

        # Create a filter button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_SAVE)
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/filter.png')
        button.set_icon_widget(image)
        button.set_name('Filter')
        button.connect('clicked', self._filter_incidents)
        button.set_tooltip_text(_("Applies the selected filter criteria."))
        toolbar.insert(button, 3)

        toolbar.show()

        return(toolbar)

    def _field_incident_widgets_create(self):
        """ Method to create the Field Incident widgets. """

        # Quadrant 1 (upper left) widgets.
        self.txtID.set_tooltip_text(_("Displays the unique code for the selected field incident."))

        self.txtIncidentType.set_tooltip_text(_("Selects and displays the type of incident for the selected field incident."))

        self.cmbIncidentStatus.set_tooltip_text(_("Displays the status of the field incident."))
        query = "SELECT fld_status_name \
                 FROM tbl_status"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)
        _widg.load_combo(self.cmbIncidentStatus, results)
        self.cmbIncidentStatus.connect('changed', self._callback_combo, 9)

        self.txtIncidentDate.set_tooltip_text(_("Displays the date the incident was opened."))
        self.btnIncidentDate.set_tooltip_text(_("Select the date the incident occurred."))
        self.btnIncidentDate.connect('released', _util.date_select,
                                     self.txtIncidentDate)

        self.txtClosureDate.set_tooltip_text(_("Displays the date the incident was closed."))
        self.btnClosureDate.set_tooltip_text(_("Select the date the incident was closed."))
        self.btnClosureDate.connect('released', _util.date_select,
                                    self.txtClosureDate)

        self.txtIncidentAge.set_tooltip_text(_("Displays the age of the incident in days."))
        self.txtUnit.set_tooltip_text(_("Displays the affected unit."))

        self.cmbSystem.set_tooltip_text(_("Allows selection of the affected system."))
        self.cmbSystem.connect('changed', self._callback_combo, 16)

        self.chkAccepted.set_tooltip_text(_("Displays whether the field incident has been accepted by the responsible owner."))
        self.chkAccepted.connect('toggled', self._callback_check, 31)

        self.chkReviewed.set_tooltip_text(_("Displays whether the field incident has been reviewed by the responsible owner."))
        self.chkReviewed.connect('toggled', self._callback_check, 20)

        # Quadrant 2 (upper right) widgets.
        self.txtShortDescription.set_tooltip_text(_("Short problem description."))

        # Quadrant 3 (lower left) widgets.
        self._component_list_create()

        return False

    def _field_incident_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it with
        the appropriate widgets.
        """

        hbox = gtk.HBox()

        vpaned = gtk.VPaned()

        # Populate quadrant 1 (upper left).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Field Incident Details"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack1(frame, True, True)

        y_pos = 5
        for i in range(len(self._fi_tab_labels[0])-2):
            label = _widg.make_label(self._fi_tab_labels[0][i], 150, 25)
            fixed.put(label, 5, (30 * i + y_pos))

        fixed.put(self.txtID, 155, y_pos)
        fixed.put(self.chkAccepted, 370, y_pos)
        fixed.put(self.chkReviewed, 475, y_pos)
        y_pos += 30

        fixed.put(self.txtIncidentType, 155, y_pos)
        y_pos += 30

        fixed.put(self.cmbIncidentStatus, 155, y_pos)
        y_pos += 30

        fixed.put(self.txtIncidentDate, 155, y_pos)
        fixed.put(self.btnIncidentDate, 265, y_pos)
        y_pos += 30

        fixed.put(self.txtClosureDate, 155, y_pos)
        fixed.put(self.btnClosureDate, 265, y_pos)
        y_pos += 30

        fixed.put(self.txtIncidentAge, 155, y_pos)
        y_pos += 30

        fixed.put(self.txtUnit, 155, y_pos)
        y_pos += 30

        fixed.put(self.cmbSystem, 155, y_pos)

        fixed.show_all()

        # Populate quadrant 2 (lower left).
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwComponentList)

        frame = _widg.make_frame(_label_=_("Component Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vpaned.pack2(frame, True, True)

        hbox.pack_start(vpaned)

        # Populate quadrant 3 (upper right).
        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("Incident Descriptions"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        hbox.pack_start(frame)

        y_pos = 5
        label = _widg.make_label(self._fi_tab_labels[1][0],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        y_pos += 30

        fixed.put(self.txtShortDescription, 5, y_pos)
        y_pos += 30

        label = _widg.make_label(self._fi_tab_labels[1][1],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        y_pos += 30

        textview = _widg.make_text_view(buffer_=self.txtLongDescription,
                                        width=550, height=200)
        fixed.put(textview, 5, y_pos)
        y_pos += 205

        label = _widg.make_label(self._fi_tab_labels[1][2],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        y_pos += 30

        textview = _widg.make_text_view(buffer_=self.txtClosureRemarks,
                                        width=550, height=200)
        fixed.put(textview, 5, y_pos)

        fixed.show_all()

        # Insert the tab.
        label = gtk.Label()
        _heading = _("Field\nIncident")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays details about the selected incident."))

        self.notebook.insert_page(hbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _field_incident_tab_load(self):
        """
        Loads the widgets with general information about the INCIDENT Object.
        """

        if(self.selected_row is None):
            return True

        query = "SELECT fld_name FROM tbl_system WHERE fld_part=0"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ProgCnx)
        _widg.load_combo(self.cmbSystem, results)

        self.txtID.set_text(str(self.model.get_value(self.selected_row, 0)))
        self.txtIncidentType.set_text(str(self.model.get_value(self.selected_row, 3)))
        self.txtShortDescription.set_text(self.model.get_value(self.selected_row, 4))
        self.txtLongDescription.set_text(self.model.get_value(self.selected_row, 5))
        self.txtClosureRemarks.set_text(self.model.get_value(self.selected_row, 8))
        #self.txtIncidentStatus.set_text(self.model.get_value(self.selected_row, 9))
        self.txtIncidentAge.set_text(str(self.model.get_value(self.selected_row, 15)))
        self.txtIncidentDate.set_text(str(self.model.get_value(self.selected_row, 19)))
        self.chkReviewed.set_active(self.model.get_value(self.selected_row, 20))
        self.txtClosureDate.set_text(str(self.model.get_value(self.selected_row, 28)))
        self.chkAccepted.set_active(self.model.get_value(self.selected_row, 31))

        values = (str(self.model.get_value(self.selected_row, 0)),)

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT t2.fld_ref_des, t2.fld_name, \
                            t1.fld_initial_installation, t1.fld_failure, \
                            t1.fld_suspension, t1.fld_occ_fault, \
                            t1.fld_cnd_nff, t1.fld_interval_censored, \
                            t1.fld_use_op_time, t1.fld_use_cal_time, \
                            t1.fld_ttf, t1.fld_age_at_incident \
                     FROM tbl_incident_detail AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t1.fld_part_num=t2.fld_ref_des \
                     WHERE t2.fld_incident_id='%s'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT t2.fld_ref_des, t2.fld_name, \
                            t1.fld_initial_installation, t1.fld_failure, \
                            t1.fld_suspension, t1.fld_occ_fault, \
                            t1.fld_cnd_nff, t1.fld_interval_censored, \
                            t1.fld_use_op_time, t1.fld_use_cal_time, \
                            t1.fld_ttf, t1.fld_age_at_incident \
                     FROM tbl_incident_detail AS t1 \
                     INNER JOIN tbl_system AS t2 \
                     ON t1.fld_part_num=t2.fld_ref_des \
                     WHERE t1.fld_incident_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        model = self.tvwComponentList.get_model()
        model.clear()

        if not results:
            return True

        n_assemblies = len(results)

        for i in range(n_assemblies):
            try:
                model.append(results[i])
            except TypeError:
                print results[i]

        return False

    def _component_list_create(self):
        """
        Method to create the component list gtk.Treeview.  This is for listing
        the component information associated with a field incident.
        """

        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwComponentList.set_model(model)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn(_("Reference\nDesignator"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn(_("Description"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 2, model)
        column = gtk.TreeViewColumn(_("Initial\nInstall"))
        column.pack_start(cell, True)
        column.set_attributes(cell, active=2)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 3, model)
        column = gtk.TreeViewColumn(_("Failure"))
        column.pack_start(cell, True)
        column.set_attributes(cell, active=3)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 4, model)
        column = gtk.TreeViewColumn(_("Suspension"))
        column.pack_start(cell, True)
        column.set_attributes(cell, active=4)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 5, model)
        column = gtk.TreeViewColumn(_("OOT\nFailure"))
        column.pack_start(cell, True)
        column.set_attributes(cell, active=5)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 6, model)
        column = gtk.TreeViewColumn(_("CND/NFF"))
        column.pack_start(cell, True)
        column.set_attributes(cell, active=6)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 7, model)
        column = gtk.TreeViewColumn(_("Interval\nCensored"))
        column.pack_start(cell, True)
        column.set_attributes(cell, active=7)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 8, model)
        column = gtk.TreeViewColumn(_("Use\nOperating\nTime"))
        column.pack_start(cell, True)
        column.set_attributes(cell, active=8)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 9, model)
        column = gtk.TreeViewColumn(_("Use\nCalendar\nTime"))
        column.pack_start(cell, True)
        column.set_attributes(cell, active=9)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn(_("Time to\nFailure"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=10)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn(_("Age at\nFailure"))
        column.pack_start(cell, True)
        column.set_attributes(cell, text=11)
        column.set_visible(0)
        self.tvwComponentList.append_column(column)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Validation Object
        treeview.

        Keyword Arguments:
        treeview -- the Validation Object treeview.
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
        Callback function to handle events for the INCIDENT Object
        gtk.Treeview.  It is called whenever the Incident Object treeview is
        clicked or a row is activated.

        Keyword Arguments:
        treeview -- the Incident Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        selection = self.treeview.get_selection()
        (self.model, self.selected_row) = selection.get_selected()

        if self.selected_row is not None:
            self.load_notebook()

            return False
        else:
            return True

    def _component_list_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a TreeView CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        value = not cell.get_active()
        model[path][position] = value

        if(position == 3):
            model[path][4] = -1 * (value - 1)

        elif(position == 4):
            model[path][3] = -1 * (value - 1)

        # If selecting "Use operating time", set the time to failure
        # equal to age at incident.  Otherwise set the time to failure
        # equal to zero.
        elif(position == 8):
            if(value == 1):
                ttf = model[path][11]
            elif(value == 0):
                ttf = 0

            model[path][9] = -1 * (value - 1)
            model[path][10] = ttf

        elif(position == 9):

            from datetime import datetime

            model[path][8] = -1 * (value - 1)

            # Calculate the time to failure.  This is based on the elapsed
            # calendar time since the last failure of this component.
            _incident_id = self.model.get_value(self.selected_row, 0)
            values = (model[path][0],)
            if(_conf.BACKEND == 'mysql'):
                query = "SELECT t1.fld_incident_id, t1.fld_request_date \
                         FROM tbl_incident AS t1 \
                         INNER JOIN tbl_incident_detail AS t2 \
                         ON t1.fld_incident_id=t2.fld_incident_id \
                         WHERE t2.fld_part_num='%s'"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "SELECT t1.fld_incident_id, t1.fld_request_date \
                         FROM tbl_incident AS t1 \
                         INNER JOIN tbl_incident_detail AS t2 \
                         ON t1.fld_incident_id=t2.fld_incident_id \
                         WHERE t2.fld_part_num=? \
                         ORDER BY t1.fld_request_date"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx)

            for i in range(len(results)):
                if(results[i][0] == _incident_id):
                    _incident_date = results[i][1]
                    # If this is the first incident for this component,
                    # find the warranty start date.
                    if(i == 0):
                        values = (self.model.get_value(self.selected_row, 11),)
                        if(_conf.BACKEND == 'mysql'):
                            query = "SELECT fld_warranty_date \
                                     FROM tbl_units \
                                     WHERE fld_serial_no='%s'"
                        elif(_conf.BACKEND == 'sqlite3'):
                            query = "SELECT fld_warranty_date \
                                     FROM tbl_units \
                                     WHERE fld_serial_no=?"

                        results = self._app.DB.execute_query(query,
                                                             values,
                                                             self._app.ProgCnx)
                        _prev_date = results[0][0]
                    else:
                        _prev_date = results[i-1][1]

                    break

            # Calculate the difference in days between events.
            _incident_date = datetime.strptime(_incident_date, '%Y-%m-%d')
            _prev_date = datetime.strptime(_prev_date, '%Y-%m-%d')
            ttf = (_incident_date - _prev_date).days
            model[path][10] = ttf

        return False

    def _component_add(self, widget):
        """
        Adds a new hardware item to the selected field incident.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        n_tasks = _util.add_items(_("Components to Program Incident"))

        if(n_tasks < 1):
            return True

        if(_conf.RELIAFREE_MODULES[0] == 1):
            _revision_id = self._app.REVISION.revision_id
        else:
            _revision_id = 0

        _incident_id = self.model.get_value(self.selected_row, 0)

        for i in range(n_tasks):
            component_name = "Component " + str(i)
            values = (_revision_id, _incident_id, component_name)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_incident_detail \
                         (fld_revision_id, fld_incident_id, fld_part_num) \
                         VALUES (%d, '%s', '%s')"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_incident_detail \
                         (fld_revision_id, fld_incident_id, fld_part_num) \
                         VALUES (?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if(results == '' or not results):
                self._app.user_log.error("incident.py: Failed to add component to field incident.")
                return True

        self._field_incident_tab_load()

        return False

    def _component_delete(self, button):
        """
        Deletes the currently selected component from the RelKit Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        """

        selection = self.tvwComponentList.get_selection()
        (model, row) = selection.get_selected()

        values = (self.model.get_value(self.selected_row, 0), \
                  model.get_value(row, 0))

        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_incident_detail \
                     WHERE fld_incident_id='%s' \
                     AND fld_part_num='%s'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_incident_detail \
                     WHERE fld_incident_id=? \
                     AND fld_part_num=?"
        print query, values
        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.user_log.error("incident.py: Failed to delete component from field incident.")
            return True

        self.load_field_incident_tab()

        return False

    def _component_save(self, widget):
        """
        Saves the Validation Object treeview information to the Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        model = self.tvwComponentList.get_model()
        model.foreach(self._save_line_item)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the Incident Object treeview model to the RelKit's
        Program MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the Field Incident component list treemodel.
        path_ -- the path of the active row in the Field Incident
                 component list treemodel.
        row   -- the selected row in the Field Incident component list
                 treeview.
        """

        values = (model.get_value(row, 2), \
                  model.get_value(row, 3), \
                  model.get_value(row, 4), \
                  model.get_value(row, 5), \
                  model.get_value(row, 6), \
                  model.get_value(row, 7), \
                  model.get_value(row, 8), \
                  model.get_value(row, 9), \
                  model.get_value(row, 10), \
                  self.model.get_value(self.selected_row, 0))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_incident_detail \
                     SET fld_initial_installation=%d, \
                         fld_failure=%d, fld_suspension=%d, \
                         fld_occ_fault=%d, fld_cnd_nff=%d, \
                         fld_interval_censored=%d, \
                         fld_use_op_time=%d, fld_use_cal_time=%d, \
                         fld_ttf=%f \
                     WHERE fld_incident_id='%s'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_incident_detail \
                     SET fld_initial_installation=?, \
                         fld_failure=?, fld_suspension=?, \
                         fld_occ_fault=?, fld_cnd_nff=?, \
                         fld_interval_censored=?, \
                         fld_use_op_time=?, fld_use_cal_time=?, \
                         fld_ttf=? \
                     WHERE fld_incident_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("incident.py: Failed to save field incident component list.")
            return True

        values = (self.model.get_value(self.selected_row, 10),
                  self.model.get_value(self.selected_row, 0))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_incident \
                     SET fld_reviewed=%d \
                     WHERE fld_incident_id='%s'"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_incident \
                     SET fld_reviewed=? \
                     WHERE fld_incident_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("incident.py: Failed to save field incident.")
            return True

        return False

    def _callback_check(self, check, _index_):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check   -- the checkbutton that called the function.
        _index_ -- the position in the component list model.
        """

        if(check.get_active()):
            value = 1
        else:
            value = 0

        # Update the Incident Component List Tree.
        self.model.set_value(self.selected_row, _index_, value)

        return False

    def _callback_combo(self, combo, _index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo   -- the combobox that called the function.
        _index_ -- the position in the INCIDENT Object _attribute list
                   associated with the data from the calling combobox.
        """

        if(_index_ == 9):                   # Incident status
            _text_ = combo.get_active()
        elif(_index_ == 16):                # Affected system
            _text_ = combo.get_active()

        self.model.set_value(self.selected_row, _index_, _text_)

        return False

    def _filter_incidents(self, button):
        """
        Filters the list of field incidents based on user-provided criteria.

        Keyword Arguments:
        button -- the gtk.Button widget that called this function.
        """

        # Lists of search criteria to use.
        _criteria0 = [["="], ["!="], [">"], ["<"], [">="], ["<="],
                      [_("LIKE")], [_("NOT LIKE")]]
        _criteria1 = [[_("LIKE")], [_("NOT LIKE")]]
        _criteria2 = [["="], ["!="], [">"], ["<"], [">="], ["<="]]
        _criteria3 = [["="], ["!="]]

        _compound = [[_("OR")], [_("AND")]]

        # Widgets used to create filters.
        chkFilterAccepted = _widg.make_check_button(self._fi_tab_labels[3][11])
        chkFilterAccepted.set_tooltip_text(_("Deletes the selected component from the selected field incident."))

        chkFilterReviewed = _widg.make_check_button(self._fi_tab_labels[3][12])
        chkFilterReviewed.set_tooltip_text(_("Deletes the selected component from the selected field incident."))

        cmbCompound1 = _widg.make_combo(_width_=50)
        cmbCompound2 = _widg.make_combo(_width_=50)
        cmbCompound3 = _widg.make_combo(_width_=50)
        cmbCompound4 = _widg.make_combo(_width_=50)
        cmbCompound5 = _widg.make_combo(_width_=50)
        cmbCompound6 = _widg.make_combo(_width_=50)
        cmbCompound7 = _widg.make_combo(_width_=50)
        cmbCompound8 = _widg.make_combo(_width_=50)
        cmbCompound9 = _widg.make_combo(_width_=50)
        cmbCompound10 = _widg.make_combo(_width_=50)
        cmbCompound11 = _widg.make_combo(_width_=50)
        _widg.load_combo(cmbCompound1, _compound)
        _widg.load_combo(cmbCompound2, _compound)
        _widg.load_combo(cmbCompound3, _compound)
        _widg.load_combo(cmbCompound4, _compound)
        _widg.load_combo(cmbCompound5, _compound)
        _widg.load_combo(cmbCompound6, _compound)
        _widg.load_combo(cmbCompound7, _compound)
        _widg.load_combo(cmbCompound8, _compound)
        _widg.load_combo(cmbCompound9, _compound)
        _widg.load_combo(cmbCompound10, _compound)
        _widg.load_combo(cmbCompound11, _compound)

        cmbFilterIncidentID = _widg.make_combo(_width_=100)
        cmbFilterIncidentID.set_tooltip_text(_("Sets the field incident ID filter criterion."))
        _widg.load_combo(cmbFilterIncidentID, _criteria0)

        cmbFilterIncidentType = _widg.make_combo(_width_=100)
        cmbFilterIncidentType.set_tooltip_text(_("Sets the field incident type filter criterion."))
        _widg.load_combo(cmbFilterIncidentType, _criteria3)

        cmbFilterIncidentTypeList = _widg.make_combo(_width_=100)
        cmbFilterIncidentTypeList.set_tooltip_text(_("Sets the field incident type filter criterion."))
        query = "SELECT DISTINCT(fld_incident_type) \
                 FROM tbl_incident"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        _widg.load_combo(cmbFilterIncidentTypeList, results, simple=True)

        cmbFilterShortDesc = _widg.make_combo(_width_=100)
        cmbFilterShortDesc.set_tooltip_text(_("Sets the field incident short description filter criterion."))
        _widg.load_combo(cmbFilterShortDesc, _criteria1)

        cmbFilterLongDesc = _widg.make_combo(_width_=100)
        cmbFilterLongDesc.set_tooltip_text(_("Sets the field incident long description filter criterion."))
        _widg.load_combo(cmbFilterLongDesc, _criteria1)

        cmbFilterRemarks = _widg.make_combo(_width_=100)
        cmbFilterRemarks.set_tooltip_text(_("Sets the field incident closure remarks filter criterion."))
        _widg.load_combo(cmbFilterRemarks, _criteria1)

        cmbFilterIncidentDate = _widg.make_combo(_width_=100)
        cmbFilterIncidentDate.set_tooltip_text(_("Sets the field incident occurrence date filter criterion."))
        _widg.load_combo(cmbFilterIncidentDate, _criteria2)

        cmbFilterClosureDate = _widg.make_combo(_width_=100)
        cmbFilterClosureDate.set_tooltip_text(_("Sets the field incident closure date filter criterion."))
        _widg.load_combo(cmbFilterClosureDate, _criteria2)

        cmbFilterIncidentAge = _widg.make_combo(_width_=100)
        cmbFilterIncidentAge.set_tooltip_text(_("Sets the field incident age filter criterion."))
        _widg.load_combo(cmbFilterIncidentAge, _criteria2)

        cmbFilterStatus = _widg.make_combo(_width_=100)
        cmbFilterStatus.set_tooltip_text(_("Sets the field incident status filter criterion."))
        _widg.load_combo(cmbFilterStatus, _criteria3)

        cmbFilterMachine = _widg.make_combo(_width_=100)
        cmbFilterMachine.set_tooltip_text(_("Sets the field incident unit serial number filter criterion."))
        _widg.load_combo(cmbFilterMachine, _criteria2)

        cmbFilterSystem = _widg.make_combo(_width_=100)
        cmbFilterSystem.set_tooltip_text(_("Sets the field incident affected system filter criterion."))
        _widg.load_combo(cmbFilterSystem, _criteria3)

        cmbFilterSystemList = _widg.make_combo(_width_=100)
        cmbFilterSystemList.set_tooltip_text(_("Sets the field incident affected system filter criterion."))
        query = "SELECT fld_name \
                 FROM tbl_system \
                 WHERE fld_parent_assembly='0' \
                 AND fld_part=0"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        _widg.load_combo(cmbFilterSystemList, results, simple=True)

        txtFilterIncidentID = _widg.make_entry(_width_=100)
        txtFilterIncidentID.set_tooltip_text(_("Sets the field incident ID filter criterion."))

        txtFilterShortDesc = _widg.make_entry(_width_=100)
        txtFilterShortDesc.set_tooltip_text(_("Sets the field incident short description filter criterion."))

        txtFilterLongDesc = _widg.make_entry(_width_=100)
        txtFilterLongDesc.set_tooltip_text(_("Sets the field incident long description filter criterion."))

        txtFilterRemarks = _widg.make_entry(_width_=100)
        txtFilterRemarks.set_tooltip_text(_("Sets the field incident closure remarks filter criterion."))

        txtFilterIncidentDate = _widg.make_entry(_width_=100)
        txtFilterIncidentDate.set_tooltip_text(_("Sets the field incident occurrence date filter criterion."))

        txtFilterClosureDate = _widg.make_entry(_width_=100)
        txtFilterClosureDate.set_tooltip_text(_("Sets the field incident closure date filter criterion."))

        txtFilterIncidentAge = _widg.make_entry(_width_=100)
        txtFilterIncidentAge.set_tooltip_text(_("Sets the field incident age filter criterion."))

        txtFilterStatus = _widg.make_entry(_width_=100)
        txtFilterStatus.set_tooltip_text(_("Sets the field incident status filter criterion."))

        txtFilterMachine = _widg.make_entry(_width_=100)
        txtFilterMachine.set_tooltip_text(_("Sets the field incident unit serial number filter criterion."))

        dialog = _widg.make_dialog(_("Create filter for Program Incidents"))

        fixed = gtk.Fixed()

        frame = _widg.make_frame(_label_=_(""))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(fixed)

        dialog.vbox.pack_start(frame)

        y_pos = 5
        for i in range(len(self._fi_tab_labels[3]) - 2):
            label = _widg.make_label(self._fi_tab_labels[3][i], 150, 25)
            fixed.put(label, 5, (35 * i + y_pos))

        fixed.put(cmbFilterIncidentID, 190, y_pos)
        fixed.put(txtFilterIncidentID, 300, y_pos)
        fixed.put(cmbCompound1, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterIncidentType, 190, y_pos)
        fixed.put(cmbFilterIncidentTypeList, 300, y_pos)
        fixed.put(cmbCompound2, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterShortDesc, 190, y_pos)
        fixed.put(txtFilterShortDesc, 300, y_pos)
        fixed.put(cmbCompound3, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterLongDesc, 190, y_pos)
        fixed.put(txtFilterLongDesc, 300, y_pos)
        fixed.put(cmbCompound4, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterRemarks, 190, y_pos)
        fixed.put(txtFilterRemarks, 300, y_pos)
        fixed.put(cmbCompound5, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterIncidentDate, 190, y_pos)
        fixed.put(txtFilterIncidentDate, 300, y_pos)
        fixed.put(cmbCompound6, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterClosureDate, 190, y_pos)
        fixed.put(txtFilterClosureDate, 300, y_pos)
        fixed.put(cmbCompound7, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterIncidentAge, 190, y_pos)
        fixed.put(txtFilterIncidentAge, 300, y_pos)
        fixed.put(cmbCompound8, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterStatus, 190, y_pos)
        fixed.put(txtFilterStatus, 300, y_pos)
        fixed.put(cmbCompound9, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterMachine, 190, y_pos)
        fixed.put(txtFilterMachine, 300, y_pos)
        fixed.put(cmbCompound10, 410, y_pos)
        y_pos += 35

        fixed.put(cmbFilterSystem, 190, y_pos)
        fixed.put(cmbFilterSystemList, 300, y_pos)
        fixed.put(cmbCompound11, 410, y_pos)
        y_pos += 35

        fixed.put(chkFilterAccepted, 15, y_pos)
        y_pos += 35

        fixed.put(chkFilterReviewed, 15, y_pos)

        dialog.vbox.show_all()

        response = dialog.run()

        if(response == gtk.RESPONSE_ACCEPT):
            _criteria = []
            _inputs = []
            _connectors = []

            # Read the user inputs for the different fields that can be used to
            # filter with.
            _criteria.append(cmbFilterIncidentID.get_active_text())
            _inputs.append(txtFilterIncidentID.get_text())
            _connectors.append(cmbCompound1.get_active_text())

            _criteria.append(cmbFilterIncidentType.get_active_text())
            _inputs.append(cmbFilterIncidentTypeList.get_active_text())
            _connectors.append(cmbCompound2.get_active_text())

            _criteria.append(cmbFilterShortDesc.get_active_text())
            _inputs.append(txtFilterShortDesc.get_text())
            _connectors.append(cmbCompound3.get_active_text())

            _criteria.append(cmbFilterLongDesc.get_active_text())
            _inputs.append(txtFilterLongDesc.get_text())
            _connectors.append(cmbCompound4.get_active_text())

            _criteria.append(cmbFilterRemarks.get_active_text())
            _inputs.append(txtFilterRemarks.get_text())
            _connectors.append(cmbCompound5.get_active_text())

            _criteria.append(cmbFilterIncidentDate.get_active_text())
            _inputs.append(txtFilterIncidentDate.get_text())
            _connectors.append(cmbCompound6.get_active_text())

            _criteria.append(cmbFilterClosureDate.get_active_text())
            _inputs.append(txtFilterClosureDate.get_text())
            _connectors.append(cmbCompound7.get_active_text())

            _criteria.append(cmbFilterIncidentAge.get_active_text())
            _inputs.append(txtFilterIncidentAge.get_text())
            _connectors.append(cmbCompound8.get_active_text())

            _criteria.append(cmbFilterStatus.get_active_text())
            _inputs.append(txtFilterStatus.get_text())
            _connectors.append(cmbCompound9.get_active_text())

            _criteria.append(cmbFilterMachine.get_active_text())
            _inputs.append(txtFilterMachine.get_text())
            _connectors.append(cmbCompound10.get_active_text())

            _criteria.append(cmbFilterSystem.get_active_text())
            _inputs.append(cmbFilterSystemList.get_active())
            _connectors.append(cmbCompound11.get_active_text())

            _inputs.append(chkFilterAccepted.get_active())
            _inputs.append(chkFilterReviewed.get_active())

            # Build the query from the user-provided inputs.
            if(_conf.RELIAFREE_MODULES[0] == 1):
                query = "SELECT * FROM tbl_incident \
                         WHERE fld_revision_id=%d AND " % \
                _app.REVISION.revision_id
            else:
                query = "SELECT * FROM tbl_incident \
                         WHERE fld_revision_id=0 AND "

            if(_criteria[0] is not None and _criteria[0] != ''):
                query = query + "fld_incident_id" + _criteria[0] + _inputs[0]
            if(_connectors[0] is not None and _connectors[0] != ''):
                query = query + " " + _connectors[0] + " "

            if(_criteria[1] is not None and _criteria[1] != ''):
                query = query + "fld_incident_type" + _criteria[1] + \
                        "'" + _inputs[1] + "'"
            if(_connectors[1] is not None and _connectors[1] != ''):
                query = query + " " + _connectors[1] + " "

            if(_criteria[2] is not None and _criteria[2] != ''):
                query = query + "fld_short_description " + _criteria[2] + \
                        " '%" + _inputs[2] + "%'"
            if(_connectors[2] is not None and _connectors[2] != ''):
                query = query + " " + _connectors[2] + " "

            if(_criteria[3] is not None and _criteria[3] != ''):
                query = query + "fld_long_description " + _criteria[3] + \
                        " '%" + _inputs[3] + "%'"
            if(_connectors[3] is not None and _connectors[3] != ''):
                query = query + " " + _connectors[3] + " "

            if(_criteria[4] is not None and _criteria[4] != ''):
                query = query + "fld_remarks " + _criteria[4] + \
                        " '%" + _inputs[4] + "%'"
            if(_connectors[4] is not None and _connectors[4] != ''):
                query = query + " " + _connectors[4] + " "

            if(_criteria[5] is not None and _criteria[5] != ''):
                query =  query + "fld_request_date" + _criteria[5] + \
                         "'" + _inputs[5] + "'"
            if(_connectors[5] is not None and _connectors[5] != ''):
                query = query + " " + _connectors[5] + " "

            if(_criteria[6] is not None and _criteria[6] != ''):
                query = query + "fld_complete_date" + _criteria[6] + \
                        "'" + _inputs[6] + "'"
            if(_connectors[6] is not None and _connectors[6] != ''):
                query = query + " " + _connectors[6] + " "

            if(_criteria[7] is not None and _criteria[7] != ''):
                query = query + "fld_incident_age" + _criteria[7]
                query = query + "%d" % int(_inputs[7])
            if(_connectors[7] is not None and _connectors[7] != ''):
                query = query + " " + _connectors[7] + " "

            if(_criteria[8] is not None and _criteria[8] != ''):
                query = query + "fld_status" + _criteria[8] + \
                        "'" + _inputs[8] + "'"
            if(_connectors[8] is not None and _connectors[8] != ''):
                query = query + " " + _connectors[8] + " "

            if(_criteria[9] is not None and _connectors[9] != ''):
                query = query + "fld_machine" + _criteria[9] + \
                        "'" + _inputs[9] + "'"
            if(_connectors[9] is not None and _connectors[9] != ''):
                query = query + " " + _connectors[9] + " "

            if(_inputs[10]):
                query = query + " AND fld_reviewed=%d" % 1
            else:
                query = query + " AND fld_reviewed=%d" % 0

            results = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            if(results == '' or not results):
                dialog.destroy()
                return True

            n_incidents = len(results)

            self.model.clear()
            for i in range(n_incidents):
                self.model.append(None, results[i])

            root = self.model.get_iter_root()
            if root is not None:
                path = self.model.get_path(root)
                self.treeview.expand_all()
                self.treeview.set_cursor('0', None, False)
                col = self.treeview.get_column(0)
                self.treeview.row_activated(path, col)

            _title = _("RelKit Work Book: %d Field Incidents") % \
                     self.n_incidents
            self._app.winWorkBook.set_title(_title)

        dialog.destroy()

    def create_tree(self):
        """
        Creates the Field Incident TreeView and connects it to callback
        functions to handle editting.  Background and foreground colors can be
        set using the user-defined values in the RelKit configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RELIAFREE_COLORS[12]
        fg_color = _conf.RELIAFREE_COLORS[13]
        (self.treeview, self._col_order) = _widg.make_treeview('Incidents', 14,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)
        self.treeview.set_enable_tree_lines(True)

        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

    def load_tree(self):
        """
        Loads the Incident treeview model with the list of unaccepted field
        incidents.
        """

        # Find the current revision if using the revision module, otherwise
        # set this to the default value.
        if(_conf.RELIAFREE_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,)
        else:
            values = (0,)

        # Select all the unaccepted field incidents from the open RelKit
        # Program database.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_incident \
                     WHERE fld_revision_id=%d \
                     ORDER BY fld_incident_id"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_incident \
                     WHERE fld_revision_id=? \
                     ORDER BY fld_incident_id"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        self.n_incidents = len(results)
        self.model.clear()
        for i in range(self.n_incidents):
            self.model.append(None, results[i])

        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            self.treeview.expand_all()
            self.treeview.set_cursor('0', None, False)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        query = "SELECT fld_name \
                 FROM tbl_system \
                 WHERE fld_parent_assembly='0' \
                 AND fld_part=0"
        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)
        _widg.load_combo(self.cmbSystem, results, simple=True)

        return False

    def load_notebook(self):
        """ Method to load the INCIDENT Object gtk.Notebook. """

        self._field_incident_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxIncident)
        self._app.winWorkBook.show_all()

        _title = _("RelKit Work Bench: Field Incident (%d Field Incidents)") % \
                   self._app.INCIDENT.n_incidents
        self._app.winWorkBook.set_title(_title)

        return False
