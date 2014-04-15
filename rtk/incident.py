#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
Program incidents.
"""

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'
__updated__ = "2014-03-22 17:34"

# -*- coding: utf-8 -*-
#
#       incident.py is part of The RTK Project
#
# All rights reserved.

import gettext
import locale
import sys

from _assistants_.adds import AddIncident, CreateDataSet
from _assistants_.filters import FilterIncident
from _assistants_.imports import ImportIncident
import configuration as _conf
import imports as _impt
import utilities as _util
import widgets as _widg


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

#from _assistants_.exports import ExportIncident

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Incident:
    """
    The Incident class is used to represent the field incidents tasks logged
    against a system being analyzed.
    """

    # TODO: Write code to update notebook widgets when editing the Validation treeview.
    # TODO: Add tooltips to all widgets.
    _fi_tab_labels = [[_("Incident ID:"), _("Incident Category:"),
                       _("Incident Type:"), _("Incident Criticality:"),
                       _("Life Cycle:"), _("Date Opened:"),
                       _("Date Closed:"), _("Incident Age:"),
                       _("Reported By:"), _("Incident Status:"),
                       _("Accepted"), _("Reviewed"), _("Affected System:"),
                       _("Affected Software:")],
                      [_("Brief Description:"), _("Long Description:"),
                       _("Closure Remarks:")],
                      [_("Found in Test:"), _("Found in Test Case:"),
                       _("Reviewed By:"), _("Date Reviewed:"),
                       _("Approved By:"), _("Date Approved:")]]

    def __init__(self, application):
        """
        Initializes the Incident Object.

        Keyword Arguments:
        application -- the RTK application.
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
        self.btnIncidentDate = _widg.make_button(height=25, width=25,
                                                 label="...", image=None)
        self.btnClosureDate = _widg.make_button(height=25, width=25,
                                                label="...", image=None)

        self.chkAccepted = _widg.make_check_button(label=self._fi_tab_labels[0][10])
        self.chkReviewed = _widg.make_check_button(label=self._fi_tab_labels[0][11])

        self.cmbHardware = _widg.make_combo()
        self.cmbSoftware = _widg.make_combo()
        self.cmbCategory = _widg.make_combo()
        self.cmbType = _widg.make_combo()
        self.cmbStatus = _widg.make_combo()
        self.cmbCriticality = _widg.make_combo()
        self.cmbLifeCycle = _widg.make_combo()
        self.cmbRequestBy = _widg.make_combo()

        self.tvwComponentList = gtk.TreeView()

        self.txtID = _widg.make_entry(width=100)
        self.txtRequestDate = _widg.make_entry(width=100)
        self.txtCloseDate = _widg.make_entry(width=100)
        self.txtAge = _widg.make_entry(width=100)
        self.txtShortDescription = _widg.make_entry(width=550)
        self.txtLongDescription = gtk.TextBuffer()
        self.txtRemarks = gtk.TextBuffer()

        self.txtTest = _widg.make_entry(width=100)
        self.txtTestCase = _widg.make_entry(width=100)
        if self._field_incident_widgets_create():
            self.debug_app._log.error("incident.py: Failed to create Incident widgets.")
        if self._field_incident_tab_create():
            self.debug_app._log.error("incident.py: Failed to create Incident tab.")

        self.cmbReviewBy = _widg.make_combo()
        self.cmbApproveBy = _widg.make_combo()
        self.cmbCloseBy = _widg.make_combo()

        self.txtAnalysis = gtk.TextBuffer()
        self.txtReviewDate = _widg.make_entry(width=100)
        self.txtApproveDate = _widg.make_entry(width=100)
        self.txtCloseDate = _widg.make_entry(width=100)
        if self._incident_analysis_widgets_create():
            self.debug_app._log.error("incident.py: Failed to create Incident Analysis widgets.")
        if self._incident_analysis_tab_create():
            self.debug_app._log.error("incident.py: Failed to create Incident Analysis tab.")

        self.vbxIncident = gtk.VBox()
        toolbar = self._toolbar_create()

        self.vbxIncident.pack_start(toolbar, expand=False)
        self.vbxIncident.pack_start(self.notebook)

        #self.notebook.connect('switch-page', self._notebook_page_switched)

        self._ready = True

    def _toolbar_create(self):
        """
        Method to create the toolbar for the INCIDENT Object work book.
        """

        toolbar = gtk.Toolbar()

# Add item button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.set_name('Add')
        button.connect('clicked', self._component_add)
        button.set_tooltip_text(_("Adds a component to the selected field incident."))
        toolbar.insert(button, 0)

# Remove item button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.set_name('Remove')
        button.connect('clicked', self._component_delete)
        button.set_tooltip_text(_("Deletes the selected component from the selected field incident."))
        toolbar.insert(button, 1)

# Save results button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        button.set_icon_widget(image)
        button.set_name('Save')
        button.connect('clicked', self._component_save)
        button.set_tooltip_text(_("Saves the list of components."))
        toolbar.insert(button, 2)

# Create a filter button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/filter.png')
        button.set_icon_widget(image)
        button.set_name('Filter')
        button.connect('clicked', FilterIncident, self._app)
        button.set_tooltip_text(_("Launches the Program Incident filter assistant."))
        toolbar.insert(button, 3)

# Create an import button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/db-import.png')
        button.set_icon_widget(image)
        button.set_name('Import')
        button.connect('clicked', ImportIncident, self._app)
        button.set_tooltip_text(_("Launches the Program Incident import assistant."))
        toolbar.insert(button, 4)

# Create an export button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/db-export.png')
        button.set_icon_widget(image)
        button.set_name('Export')
        #button.connect('clicked', ExportIncident, self._app)
        button.set_tooltip_text(_("Launches the Program Incident export assistant."))
        toolbar.insert(button, 5)

# Create a data set creation button.
        button = gtk.ToolButton()
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/wizard.png')
        button.set_icon_widget(image)
        button.set_name('Data Set')
        button.connect('clicked', CreateDataSet, self._app)
        button.set_tooltip_text(_("Launches the Data Set creation assistant."))
        toolbar.insert(button, 6)

        toolbar.show()

        return(toolbar)

    def _field_incident_widgets_create(self):
        """ Method to create the Field Incident widgets. """

        # Quadrant 1 (upper left) widgets.
        self.txtID.set_tooltip_text(_("Displays the unique code for the selected incident."))

        self.cmbCategory.set_tooltip_text(_("Selects and displays the category of the selected incident."))
        query = "SELECT fld_incident_cat_name FROM tbl_incident_category"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)
        _widg.load_combo(self.cmbCategory, results)
        self.cmbCategory.connect('changed', self._callback_combo, 2)

        self.cmbType.set_tooltip_text(_("Selects and displays the type of incident for the selected incident."))
        query = "SELECT fld_incident_type_name FROM tbl_incident_type"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)
        _widg.load_combo(self.cmbType, results)
        self.cmbType.connect('changed', self._callback_combo, 3)

        self.cmbStatus.set_tooltip_text(_("Displays the status of the selected incident."))
        query = "SELECT fld_status_name FROM tbl_status"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)
        _widg.load_combo(self.cmbStatus, results)
        self.cmbStatus.connect('changed', self._callback_combo, 9)

        self.cmbCriticality.set_tooltip_text(_("Displays the criticality of the selected incident."))
        query = "SELECT fld_criticality_name FROM tbl_criticality"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)
        _widg.load_combo(self.cmbCriticality, results)
        self.cmbCriticality.connect('changed', self._callback_combo, 4)

        self.cmbLifeCycle.set_tooltip_text(_("Displays the product life cycle during which the incident occurred."))
        query = "SELECT fld_lifecycle_name FROM tbl_lifecycles"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)
        _widg.load_combo(self.cmbLifeCycle, results)
        self.cmbLifeCycle.connect('changed', self._callback_combo, 29)

        self.txtRequestDate.set_tooltip_text(_("Displays the date the incident was opened."))
        self.btnIncidentDate.set_tooltip_text(_("Select the date the incident occurred."))
        self.btnIncidentDate.connect('released', _util.date_select,
                                     self.txtRequestDate)

        self.txtCloseDate.set_tooltip_text(_("Displays the date the incident was closed."))
        self.btnClosureDate.set_tooltip_text(_("Select the date the incident was closed."))
        self.btnClosureDate.connect('released', _util.date_select,
                                    self.txtCloseDate)

        self.txtAge.set_tooltip_text(_("Displays the age of the incident in days."))

        self.cmbRequestBy.set_tooltip_text(_("Displays the name of the individual reporting the incident."))
        query = "SELECT fld_user_lname || ', ' || fld_user_fname \
                 FROM tbl_users ORDER BY fld_user_lname ASC"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)
        _widg.load_combo(self.cmbRequestBy, results)
        self.cmbRequestBy.connect('changed', self._callback_combo, 18)

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
        label = _widg.make_label(self._fi_tab_labels[0][0], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtID, 155, y_pos)
        fixed.put(self.chkAccepted, 355, y_pos)
        fixed.put(self.chkReviewed, 510, y_pos)
        y_pos += 30

        label = _widg.make_label(self._fi_tab_labels[0][1], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbCategory, 155, y_pos)
        label = _widg.make_label(self._fi_tab_labels[0][2], 150, 25)
        fixed.put(label, 360, y_pos)
        fixed.put(self.cmbType, 515, y_pos)
        y_pos += 35

        label = _widg.make_label(self._fi_tab_labels[0][3], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbCriticality, 155, y_pos)
        label = _widg.make_label(self._fi_tab_labels[0][4], 150, 25)
        fixed.put(label, 360, y_pos)
        fixed.put(self.cmbLifeCycle, 515, y_pos)
        y_pos += 35

        label = _widg.make_label(self._fi_tab_labels[0][5], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtRequestDate, 155, y_pos)
        fixed.put(self.btnIncidentDate, 265, y_pos)
        label = _widg.make_label(self._fi_tab_labels[0][6], 150, 25)
        fixed.put(label, 310, y_pos)
        fixed.put(self.txtCloseDate, 425, y_pos)
        fixed.put(self.btnClosureDate, 530, y_pos)
        label = _widg.make_label(self._fi_tab_labels[0][7], 150, 25)
        fixed.put(label, 575, y_pos)
        fixed.put(self.txtAge, 730, y_pos)
        y_pos += 30

        label = _widg.make_label(self._fi_tab_labels[0][8], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbRequestBy, 155, y_pos)
        y_pos += 35

        label = _widg.make_label(self._fi_tab_labels[0][9], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbStatus, 155, y_pos)
        y_pos += 35

        label = _widg.make_label(self._fi_tab_labels[0][12], 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbHardware, 155, y_pos)

        label = _widg.make_label(self._fi_tab_labels[0][13], 150, 25)
        fixed.put(label, 360, y_pos)
        fixed.put(self.cmbSoftware, 515, y_pos)

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

        textview = _widg.make_text_view(buffer_=self.txtRemarks,
                                        width=550, height=200)
        fixed.put(textview, 5, y_pos)

        fixed.show_all()

        # Insert the tab.
        label = gtk.Label()
        _heading = _("Incident\nDetails")
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

        from datetime import datetime

        if(self.selected_row is None):
            return True

        # Load the hardware combo with a list of the assemblies in the system.
        # TODO: Create code that will use either fld_description of fld_name depending on which the user uses.
        query = "SELECT DISTINCT fld_name \
                 FROM tbl_system \
                 WHERE fld_part=0 AND fld_level<2 AND fld_name != '' \
                 ORDER BY fld_assembly_id ASC"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ProgCnx)
        _widg.load_combo(self.cmbHardware, results)

        self.txtID.set_text(str(self.model.get_value(self.selected_row, 1)))
        self.cmbCategory.set_active(self.model.get_value(self.selected_row, 2))
        self.cmbType.set_active(self.model.get_value(self.selected_row, 3))
        self.cmbStatus.set_active(self.model.get_value(self.selected_row, 9))
        self.cmbCriticality.set_active(self.model.get_value(self.selected_row, 6))
        self.cmbLifeCycle.set_active(self.model.get_value(self.selected_row, 29))
        self.cmbHardware.set_active(self.model.get_value(self.selected_row, 16) + 1)
        self.txtAge.set_text(str(self.model.get_value(self.selected_row, 15)))
        self.cmbRequestBy.set_active(self.model.get_value(self.selected_row, 18))
        self.chkReviewed.set_active(self.model.get_value(self.selected_row, 20))
        self.chkAccepted.set_active(self.model.get_value(self.selected_row, 31))

        self.txtShortDescription.set_text(self.model.get_value(self.selected_row, 4))
        self.txtLongDescription.set_text(self.model.get_value(self.selected_row, 5))
        self.txtRemarks.set_text(self.model.get_value(self.selected_row, 8))

# Set dates.  If there is no date or the date is invalid, set it to
# January 1, 1970 as the default.
        dt = self.model.get_value(self.selected_row, 19)
        if(dt is not None and dt != '' and dt >= 1):
            self.txtRequestDate.set_text(str(dt))
        else:
            self.txtRequestDate.set_text('')

        dt = self.model.get_value(self.selected_row, 22)
        if(dt is not None and dt != '' and dt >= 1):
            self.txtReviewDate.set_text(str(dt))
        else:
            self.txtReviewDate.set_text('')

        dt = self.model.get_value(self.selected_row, 25)
        if(dt is not None and dt != '' and dt >= 1):
            self.txtApproveDate.set_text(str(dt))
        else:
            self.txtApproveDate.set_text('')

        dt = self.model.get_value(self.selected_row, 28)
        if(dt is not None and dt != '' and dt >= 1):
            self.txtCloseDate.set_text(str(dt))
        else:
            self.txtCloseDate.set_text('')

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

    def _incident_analysis_widgets_create(self):
        """ Method to create the Incident Analysis widgets. """

        self.cmbReviewBy.set_tooltip_text(_("Displays the name of the individual who reviewed the analysis."))
        query = "SELECT fld_user_lname || ', ' || fld_user_fname \
                 FROM tbl_users ORDER BY fld_user_lname ASC"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)
        _widg.load_combo(self.cmbReviewBy, results)
        self.cmbReviewBy.connect('changed', self._callback_combo, 21)

        self.txtReviewDate.set_tooltip_text(_("Displays the date the analysis was reviewed."))

        self.cmbApproveBy.set_tooltip_text(_("Displays the name of the individual who approved the analysis."))
        _widg.load_combo(self.cmbApproveBy, results)
        self.cmbApproveBy.connect('changed', self._callback_combo, 24)

        self.txtApproveDate.set_tooltip_text(_("Displays the date the analysis was approved."))

        return False

    def _incident_analysis_tab_create(self):
        """
        Method to create the Incident Analysis gtk.Notebook tab and populate
        it with the appropriate widgets.
        """

        vbox = gtk.VBox()

        fixed = gtk.Fixed()

        label = _widg.make_label(self._fi_tab_labels[2][0], 150, 25)
        fixed.put(label, 5, 5)
        fixed.put(self.txtTest, 160, 5)
        label = _widg.make_label(self._fi_tab_labels[2][1], 150, 25)
        fixed.put(label, 265, 5)
        fixed.put(self.txtTestCase, 420, 5)

        vbox.pack_start(fixed, expand=False)

        textview = _widg.make_text_view(buffer_=self.txtAnalysis,
                                        width=550, height=200)

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(textview)

        frame = _widg.make_frame(_label_=_("Incident Analysis"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        vbox.pack_start(frame)

        fixed = gtk.Fixed()

        label = _widg.make_label(self._fi_tab_labels[2][2], 150, 25)
        fixed.put(label, 5, 5)
        fixed.put(self.cmbReviewBy, 160, 5)
        label = _widg.make_label(self._fi_tab_labels[2][3], 150, 25)
        fixed.put(label, 365, 5)
        fixed.put(self.txtReviewDate, 520, 5)

        label = _widg.make_label(self._fi_tab_labels[2][4], 150, 25)
        fixed.put(label, 630, 5)
        fixed.put(self.cmbApproveBy, 785, 5)
        label = _widg.make_label(self._fi_tab_labels[2][5], 150, 25)
        fixed.put(label, 990, 5)
        fixed.put(self.txtApproveDate, 1145, 5)

        vbox.pack_start(fixed, expand=False)

        # Insert the tab.
        label = gtk.Label()
        _heading = _("Incident\nAnalysis")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the analysis of the selected incident."))

        self.notebook.insert_page(vbox,
                                  tab_label=label,
                                  position=-1)

        return False

    def _incident_analysis_tab_load(self):
        """
        Loads the widgets with analysis information about the INCIDENT Object.
        """

        from datetime import datetime

        if(self.selected_row is None):
            return True

        self.txtTest.set_text(self.model.get_value(self.selected_row, 10))
        self.txtTestCase.set_text(self.model.get_value(self.selected_row, 11))

        _string = _util.none_to_string(self.model.get_value(self.selected_row, 30))
        self.txtAnalysis.set_text(_string)

        self.cmbReviewBy.set_active(self.model.get_value(self.selected_row, 21))
        self.cmbApproveBy.set_active(self.model.get_value(self.selected_row, 24))

        dt = self.model.get_value(self.selected_row, 22)
        if(dt is not None and dt != ''):
            self.txtReviewDate.set_text(str(dt))
        else:
            self.txtReviewDate.set_text("")

        dt = self.model.get_value(self.selected_row, 25)
        if(dt is not None and dt != ''):
            self.txtApproveDate.set_text(str(dt))
        else:
            self.txtApproveDate.set_text("")

        return False

    def _component_list_create(self):
        """
        Method to create the component list gtk.Treeview.  This is for listing
        the component information associated with a field incident.
        """

        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_INT,
                              gobject.TYPE_INT, gobject.TYPE_FLOAT,
                              gobject.TYPE_FLOAT)
        self.tvwComponentList.set_model(model)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Reference\nDesignator"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 1, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Initial\nInstall"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, active=1)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 2, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Failure"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, active=2)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 3, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Suspension"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, active=3)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 4, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("OOT\nFailure"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, active=4)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 5, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("CND/NFF"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, active=5)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 6, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Interval\nCensored"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, active=6)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 7, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Use\nOperating\nTime"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, active=7)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererToggle()
        cell.set_property('activatable', 1)
        cell.connect('toggled', self._component_list_edit, None, 8, model)
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Use\nCalendar\nTime"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, active=8)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Time to\nFailure"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=9)
        self.tvwComponentList.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.set_property('background', 'light gray')
        column = gtk.TreeViewColumn()
        label = _widg.make_column_heading(_("Age at\nFailure"))
        column.set_widget(label)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=10)
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
        Called whenever a component list gtk.TreeView gtk.CellRenderer is
        edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        value = not cell.get_active()
        model[path][position] = value

        if(position == 1):                   # Initial installation.
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
        elif(position == 2):                 # Failure.
            model[path][1] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
        elif(position == 3):                 # Suspension (right).
            model[path][1] = 0
            model[path][2] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
        elif(position == 4):                 # OCC fault.
            model[path][1] = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][5] = 0
            model[path][6] = 0
        elif(position == 5):                 # CND/NFF fault.
            model[path][1] = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][6] = 0
        elif(position == 6):                 # Interval censored.
            model[path][1] = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
        elif(position == 7):                 # Use operating time.
            model[path][8] = 0
        elif(position == 8):                 # Use calendar time.
            model[path][7] = 0

        return False

    def _component_add(self, widget):
        """
        Adds a new hardware item to the selected field incident.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        n_tasks = _util.add_items(title=_(u"RTK - Add Components to Program Incident"),
                                  prompt=_(u"How many components to add to the selected program incident?"))

        if(n_tasks < 1):
            return True

        if(_conf.RTK_MODULES[0] == 1):
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
        Deletes the currently selected component from the RTK Program's
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
        Saves each row in the Incident Object treeview model to the RTK's
        Program MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the Field Incident component list treemodel.
        path_ -- the path of the active row in the Field Incident
                 component list treemodel.
        row   -- the selected row in the Field Incident component list
                 treeview.
        """

        #datetime.strptime(dt,"%Y-%m-%d").toordinal()

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

        # _index_   Field
        #   2       Incident ID
        #   3       Incident Category
        #   4       Incident Type
        #   9       Incident status
        #  16       Hardware ID
        #  17       Software ID
        #  18       Request By
        #  21       Reviewed By
        #  24       Approved By
        #  27       Complete By
        _text_ = combo.get_active()
        self.model.set_value(self.selected_row, _index_, _text_)

        return False

    def create_tree(self):
        """
        Creates the Field Incident TreeView and connects it to callback
        functions to handle editting.  Background and foreground colors can be
        set using the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[12]
        fg_color = _conf.RTK_COLORS[13]
        (self.treeview, self._col_order) = _widg.make_treeview('Incidents', 14,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)
        self.treeview.set_enable_tree_lines(True)

        # Allow sorting by the affected unit column.
        column = self.treeview.get_column(13)
        column.set_sort_column_id(13)

        self.treeview.set_tooltip_text(_("Displays a list of Program incidents."))

        scrollwindow.add(self.treeview)
        self.model = self.treeview.get_model()

        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        return(scrollwindow)

    def load_tree(self, query, values):
        """
        Loads the Incident treeview model with the list of unaccepted field
        incidents.

        Keyword Arguments:
        query  -- the SQL query to execute.
        values -- the values that are used in the SQL query.
        """

        from datetime import datetime

        self.model.clear()

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            _util.application_error(_(u"There are no incidents matching the specified criteria."))
            return True

        self.n_incidents = len(results)
        for i in range(self.n_incidents):
            _data = [results[i][0], results[i][1] ,results[i][2],
                     results[i][3], results[i][4], results[i][5],
                     results[i][6], results[i][7], results[i][8],
                     results[i][9], results[i][10], results[i][11],
                     results[i][12], results[i][13], results[i][14],
                     results[i][15], results[i][16], results[i][17],
                     results[i][18],
                     str(datetime.fromordinal(int(results[i][19])).strftime('%Y-%m-%d')),
                     results[i][20], results[i][21],
                     str(datetime.fromordinal(int(results[i][22])).strftime('%Y-%m-%d')),
                     results[i][23], results[i][24],
                     str(datetime.fromordinal(int(results[i][25])).strftime('%Y-%m-%d')),
                     results[i][26], results[i][27],
                     str(datetime.fromordinal(int(results[i][28])).strftime('%Y-%m-%d')),
                     results[i][29], results[i][30], results[i][31]]
            try:
                self.model.append(None, _data)
            except TypeError:
                pass

        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            self.treeview.expand_all()
            self.treeview.set_cursor('0', None, False)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        #query = "SELECT fld_name \
        #         FROM tbl_system \
        #         WHERE fld_parent_assembly='0' \
        #         AND fld_part=0"
        #results = self._app.DB.execute_query(query,
        #                                     None,
        #                                     self._app.ProgCnx)
        #_widg.load_combo(self.cmbSystem, results, simple=True)

        return False

    def _load_component_list(self):
        """ Method to load the component list. """

        selection = self.treeview.get_selection()
        (model, row) = selection.get_selected()
        _incident_id = model.get_value(row, 1)

        model = self.tvwComponentList.get_model()
        model.clear()

        query="SELECT fld_part_num, fld_initial_installation, \
                      fld_failure, fld_suspension, fld_occ_fault, \
                      fld_cnd_nff, fld_interval_censored, fld_use_op_time, \
                      fld_use_cal_time, fld_ttf, fld_age_at_incident \
                FROM tbl_incident_detail \
                WHERE fld_incident_id=%d" % _incident_id

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            self._app.debug_log.error("incident.py: Failed to load component list.")
            return True

        n_components = len(results)
        for i in range(n_components):
            model.append(results[i])

        return False

    def load_notebook(self):
        """ Method to load the INCIDENT Object gtk.Notebook. """

        if self.selected_row is not None:
            self._field_incident_tab_load()
            self._incident_analysis_tab_load()
            self._load_component_list()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxIncident)
        self._app.winWorkBook.show_all()

        _title = _("RTK Work Book: Program Incident (%d Incidents)") % \
                   self.n_incidents
        self._app.winWorkBook.set_title(_title)

        return False
