#!/usr/bin/env python
""" This is the Class that is used to represent and hold information related
    to the requirements of the Program. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2013 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       requirement.py is part of the RTK Project
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

# Import other RTK modules.
import configuration as _conf
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


class Requirement:
    """
    The Requirement class is used to represent the requirements in a
    system being analyzed.
    """

    # TODO: Write code to update notebook widgets when editing the Requirements treeview.
    # TODO: Add tooltips to all widgets.
    _gd_tab_labels = [[_("Requirement ID:"), _("Requirement:"),
                       _("Requirement Type:"), _("Specification:"),
                       _("Page Number:"), _("Figure Number:"), _("Derived?:"),
                       _("Parent Requirement:"), _("Validated?:"),
                       _("Validated Date:"), _("Owner:")],
                      [], [], []]

    n_attributes = 13

    def __init__(self, application):
        """
        Initializes the Requirements Object.

        Keyword Arguments:
        application -- the RTK application.
        """

        self._ready = False

        self._app = application

        self.treeview = None
        self.model = None
        self.selected_row = None
        self.requirement_id = 0
        self._col_order = []

        self.vbxRequirement = gtk.VBox()

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
        self.notebook.connect('switch-page', self._notebook_page_switched)

# Create the General Data tab widgets for the REQUIREMENT object.
        self.fxdGenDataQuad1 = gtk.Fixed()
        self.txtCode = _widg.make_entry(_width_=100)
        self.txtRequirement = gtk.TextBuffer()
        self.cmbRqmtType = _widg.make_combo(simple=False)
        self.txtSpecification = _widg.make_entry()
        self.txtPageNumber = _widg.make_entry()
        self.txtFigureNumber = _widg.make_entry()
        self.chkDerived = _widg.make_check_button()
        self.chkValidated = _widg.make_check_button()
        self.txtValidatedDate = _widg.make_entry(_width_=100)
        self.txtOwner = _widg.make_entry()
        if self._general_data_widgets_create():
            self._app.debug_log.error("requirement.py: Failed to create General Data widgets.")
        if self._general_data_tab_create():
            self._app.debug_log.error("requirement.py: Failed to create General Data tab.")

# Create the V & V tab widgets for the REQUIREMENT object.
        self.tvwValidation = gtk.TreeView()
        self.scwValidation = gtk.ScrolledWindow()
        self.btnSaveVandVTask = gtk.ToolButton()
        self.btnAddVandVTask = gtk.ToolButton()
        self.btnAssignVandVTask = gtk.ToolButton()
        self.cmbVandVTasks = _widg.make_combo(simple=False)
        if self._vandv_widgets_create():
            self._app.debug_log.error("requirement.py: Failed to create V & V widgets.")
        if self._vandv_tab_create():
            self._app.debug_log.error("requirement.py: Failed to create V & V tab.")

        toolbar = self._toolbar_create()
        self.vbxRequirement.pack_start(toolbar, expand=False)
        self.vbxRequirement.pack_start(self.notebook)

        self._ready = True

    def _toolbar_create(self):
        """ Method to create a toolbar for the REQUIREMENT Object work book. """

        toolbar = gtk.Toolbar()

        _pos = 0

# Add sibling requirement button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_("Adds a new requirement at the same indenture level as the selected requirement."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.requirement_add, 0)
        toolbar.insert(button, _pos)
        _pos += 1

# Add child (derived) requirement button.
        button = gtk.ToolButton()
        button.set_tooltip_text(_("Adds a new requirement one indenture level subordinate to the selected requirement."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.requirement_add, 1)
        toolbar.insert(button, _pos)
        _pos += 1

# Delete requirement button
        button = gtk.ToolButton()
        button.set_tooltip_text(_("Removes the currently selected requirement from the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        button.set_icon_widget(image)
        button.connect('clicked', self.requirement_delete)
        toolbar.insert(button, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Save requirement button.
        self.btnSaveRequirement = gtk.ToolButton()
        self.btnSaveRequirement.set_tooltip_text(_("Saves requirement changes to the RTK Program Database."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveRequirement.set_icon_widget(image)
        self.btnSaveRequirement.connect('clicked', self.requirement_save)
        toolbar.insert(self.btnSaveRequirement, _pos)
        _pos += 1

# Save V&V tasks button
        self.btnSaveVandVTask.set_tooltip_text(_("Saves all the Verification and Validation (V&V) tasks for the selected requirement."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSaveVandVTask.set_icon_widget(image)
        self.btnSaveVandVTask.connect('clicked', self._vandv_tasks_save)
        toolbar.insert(self.btnSaveVandVTask, _pos)
        _pos += 1

        toolbar.insert(gtk.SeparatorToolItem(), _pos)
        _pos += 1

# Add new V&V task button
        self.btnAddVandVTask.set_tooltip_text(_("Adds a new Verification and Validation (V&V) task for the selected requirement."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAddVandVTask.set_icon_widget(image)
        self.btnAddVandVTask.connect('clicked', self._vandv_task_add, 0)
        toolbar.insert(self.btnAddVandVTask, _pos)
        _pos += 1

# Assign existing V&V task button
        self.btnAssignVandVTask.set_tooltip_text(_("Assigns an exisiting Verification and Validation (V&V) task to the selected requirement."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/assign.png')
        self.btnAssignVandVTask.set_icon_widget(image)
        self.btnAssignVandVTask.connect('clicked', self._vandv_task_add, 1)
        toolbar.insert(self.btnAssignVandVTask, _pos)
        _pos += 1

        self.cmbVandVTasks.set_tooltip_text(_("List of existing V&V activities available to assign to selected requirement."))
        alignment = gtk.Alignment(xalign=0.5, yalign=0.5)
        alignment.add(self.cmbVandVTasks)
        toolitem = gtk.ToolItem()
        toolitem.add(alignment)
        toolbar.insert(toolitem, _pos)
        _pos += 1

        toolbar.show()

# Hide the toolbar items associated with the V&V tab.
        self.btnAddVandVTask.hide()
        self.btnAssignVandVTask.hide()
        self.btnSaveVandVTask.hide()
        self.cmbVandVTasks.hide()

        return(toolbar)

    def _general_data_widgets_create(self):
        """ Method to create the General Data widgets. """

# Create quadrant 1 (upper left) widgets.
        self.txtCode.set_tooltip_text(_("Displays the unique code for the selected requirement."))
        self.txtCode.connect('focus-out-event',
                             self._callback_entry, 'text', 5)

        self.cmbRqmtType.set_tooltip_text(_("Selects and displays the type of requirement for the selected requirement."))

        query = "SELECT fld_requirement_type_desc, \
                        fld_requirement_type_code, \
                        fld_requirement_type_id \
                 FROM tbl_requirement_type"
        results = self._app.COMDB.execute_query(query,
                                                None,
                                                self._app.ComCnx)

        _widg.load_combo(self.cmbRqmtType, results, False)
        self.cmbRqmtType.connect('changed', self._callback_combo, 4)

        self.txtSpecification.set_tooltip_text(_("Displays the internal or industry specification associated with the selected requirement."))
        self.txtSpecification.connect('focus-out-event',
                                      self._callback_entry, 'text', 11)

        self.txtPageNumber.set_tooltip_text(_("Displays the specification page number associated with the selected requirement."))
        self.txtPageNumber.connect('focus-out-event',
                                   self._callback_entry, 'text', 12)

        self.txtFigureNumber.set_tooltip_text(_("Displays the specification figure number associated with the selected requirement."))
        self.txtFigureNumber.connect('focus-out-event',
                                     self._callback_entry, 'text', 13)

        self.chkDerived.set_tooltip_text(_("Whether or not the selected requirement is derived."))
        self.chkDerived.connect('toggled', self._callback_check, 6)

        self.chkValidated.set_tooltip_text(_("Whether or not the selected requirement has been verified and validated."))
        self.chkValidated.connect('toggled', self._callback_check, 8)

        self.txtValidatedDate.set_tooltip_text(_("Displays the date the selected requirement was verified and validated."))
        self.txtValidatedDate.connect('focus-out-event',
                                      self._callback_entry, 'text', 9)

        self.txtOwner.set_tooltip_text(_("Displays the responsible organization or individual for the selected requirement."))
        self.txtOwner.connect('focus-out-event',
                              self._callback_entry, 'text', 10)

        return False

    def _general_data_tab_create(self):
        """
        Method to create the General Data gtk.Notebook tab and populate it
        with the appropriate widgets.
        """

        fixed = gtk.Fixed()

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(fixed)

        frame = _widg.make_frame(_label_=_("General Information"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        y_pos = 5

        label = _widg.make_label(self._gd_tab_labels[0][0],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtCode, 155, y_pos)
        y_pos += 30
        label = _widg.make_label(self._gd_tab_labels[0][1],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        textview = _widg.make_text_view(buffer_=self.txtRequirement, width=400)
        textview.set_tooltip_text(_(u"Detailed description of the requirement."))
        textview.connect('focus-out-event', self._callback_entry, 'text', 3)
        fixed.put(textview, 155, y_pos)
        y_pos += 105

        label = _widg.make_label(self._gd_tab_labels[0][2],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.cmbRqmtType, 155, y_pos)
        y_pos += 35
        label = _widg.make_label(self._gd_tab_labels[0][3],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtSpecification, 155, y_pos)
        y_pos += 30
        label = _widg.make_label(self._gd_tab_labels[0][4],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtPageNumber, 155, y_pos)
        y_pos += 30
        label = _widg.make_label(self._gd_tab_labels[0][5],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtFigureNumber, 155, y_pos)
        y_pos += 30
        label = _widg.make_label(self._gd_tab_labels[0][6],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.chkDerived, 155, y_pos)
        y_pos += 30
        label = _widg.make_label(self._gd_tab_labels[0][8],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.chkValidated, 155, y_pos)

        label = _widg.make_label(self._gd_tab_labels[0][9],
                                 150, 25)
        fixed.put(label, 205, y_pos)
        fixed.put(self.txtValidatedDate, 355, y_pos)
        y_pos += 30
        label = _widg.make_label(self._gd_tab_labels[0][10],
                                 150, 25)
        fixed.put(label, 5, y_pos)
        fixed.put(self.txtOwner, 155, y_pos)
        y_pos += 60

        fixed.show_all()

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("General\nData") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_("Displays general information about the selected requirement."))
        label.show_all()
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _general_data_tab_load(self):
        """
        Loads the widgets with general information about the Requirement
        Object.
        """

        self.txtCode.set_text(str(self.model.get_value(self.selected_row, 5)))
        self.txtRequirement.set_text(str(self.model.get_value(self.selected_row, 3)))
        self.cmbRqmtType.set_active(int(self.model.get_value(self.selected_row, 4)))
        self.chkDerived.set_active(int(self.model.get_value(self.selected_row, 6)))
        self.chkValidated.set_active(int(self.model.get_value(self.selected_row, 8)))
        self.txtValidatedDate.set_text(str(self.model.get_value(self.selected_row, 9)))
        self.txtOwner.set_text(str(self.model.get_value(self.selected_row, 10)))
        self.txtSpecification.set_text(str(self.model.get_value(self.selected_row, 11)))
        self.txtPageNumber.set_text(str(self.model.get_value(self.selected_row, 12)))
        self.txtFigureNumber.set_text(str(self.model.get_value(self.selected_row, 13)))

        return False

    def _vandv_widgets_create(self):
        """ Method to create the Verification and Validation Task widgets. """

        model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT)
        self.tvwValidation.set_model(model)
        self.tvwValidation.set_tooltip_text(_("Provides read-only list of basic information for Verfication and Validation (V&V) tasks associated with the selected Requirement."))

    def _vandv_tab_create(self):
        """
        Method to create the Verification and Validation Plan gtk.Notebook tab
        and populate it with the appropriate widgets.
        """

        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC,
                                gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwValidation)

        frame = gtk.Frame(_("Verification and Validation Task List"))
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        column = gtk.TreeViewColumn(_("Task ID"))
        column.set_visible(0)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=0)
        self.tvwValidation.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.connect('edited', self._vandv_tree_edit, 1,
                     self.tvwValidation.get_model())
        column = gtk.TreeViewColumn(_("Task Description"))
        column.set_visible(1)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        column.set_resizable(True)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=1)
        self.tvwValidation.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.connect('edited', self._vandv_tree_edit, 2,
                     self.tvwValidation.get_model())
        column = gtk.TreeViewColumn(_("Start Date"))
        column.set_visible(1)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=2)
        self.tvwValidation.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.connect('edited', self._vandv_tree_edit, 3,
                     self.tvwValidation.get_model())
        column = gtk.TreeViewColumn(_("Due Date"))
        column.set_visible(1)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=3)
        self.tvwValidation.append_column(column)

        cell = gtk.CellRendererText()
        cell.set_property('editable', 0)
        cell.connect('edited', self._vandv_tree_edit, 4,
                     self.tvwValidation.get_model())
        column = gtk.TreeViewColumn(_("% Complete"))
        column.set_visible(1)
        column.pack_start(cell, True)
        column.set_attributes(cell, text=4)
        self.tvwValidation.append_column(column)

# Insert the tab.
        label = gtk.Label()
        label.set_markup("<span weight='bold'>" +
                         _("V &amp; V Tasks") +
                         "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.set_tooltip_text(_("Displays the list of V&V tasks for the selected requirement."))
        label.show_all()
        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _vandv_tab_load(self):
        """
        Creates the TreeView widget to display the Requirement/Validation task
        relationship matrix.
        """

        values = (self.model.get_value(self.selected_row, self._col_order[0]),
                  self.model.get_value(self.selected_row, self._col_order[1]))

        if(_conf.BACKEND == 'mysql'):
            query = "SELECT t1.fld_validation_id, t1.fld_task_desc, \
                            t1.fld_start_date, t1.fld_end_date, t1.fld_status \
                     FROM tbl_validation AS t1 \
                     INNER JOIN tbl_validation_matrix AS t2 \
                     ON t2.fld_validation_id=t1.fld_validation_id \
                     WHERE t1.fld_revision_id=%d \
                     AND t2.fld_requirement_id=%d \
                     GROUP BY t1.fld_validation_id"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "SELECT t1.fld_validation_id, t1.fld_task_desc, \
                            t1.fld_start_date, t1.fld_end_date, t1.fld_status \
                     FROM tbl_validation AS t1 \
                     INNER JOIN tbl_validation_matrix AS t2 \
                     ON t2.fld_validation_id=t1.fld_validation_id \
                     WHERE t1.fld_revision_id=? \
                     AND t2.fld_requirement_id=? \
                     GROUP BY t1.fld_validation_id"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == ''):
            return True

        n_records = len(results)
        model = self.tvwValidation.get_model()
        model.clear()
        for i in range(n_records):
            model.append(None, results[i])

        root = model.get_iter_root()
        if root is not None:
            path = model.get_path(root)
            self.tvwValidation.expand_all()
            self.tvwValidation.set_cursor('0', None, False)
            col = self.tvwValidation.get_column(0)
            self.tvwValidation.row_activated(path, col)

        # Load the list of V&V task to the gtk.ComboBox used to
        # associate existing V&V tasks with requirements.
        query = "SELECT DISTINCT(fld_validation_id), \
                 fld_task_desc, fld_task_type \
                 FROM tbl_validation"

        results = self._app.DB.execute_query(query,
                                             None,
                                             self._app.ProgCnx)

        tasks = []
        for i in range(len(results)):
            tasks.append((results[i][1], results[i][0], results[i][2]))

        _widg.load_combo(self.cmbVandVTasks, tasks, simple=False)

        return False

    def create_tree(self):
        """
        Creates the Requirements TreeView and connects it to callback
        functions to handle editting.  Background and foreground colors can be
        set using the user-defined values in the RTK configuration file.
        """

        scrollwindow = gtk.ScrolledWindow()
        bg_color = _conf.RTK_COLORS[4]
        fg_color = _conf.RTK_COLORS[5]
        (self.treeview, self._col_order) = _widg.make_treeview('Requirement',
                                                               2,
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
        Loads the Requirements treeview model with system information.
        This information can be stored either in a MySQL or SQLite3 database.
        """

        if(_conf.RTK_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id,)
        else:
            values = (0,)

        # Select everything from the requirements table.
        if(_conf.BACKEND == 'mysql'):
            query = "SELECT * FROM tbl_requirements \
                     WHERE fld_revision_id=%d \
                     ORDER BY fld_requirement_id"
        if(_conf.BACKEND == 'sqlite3'):
            query = "SELECT * FROM tbl_requirements \
                     WHERE fld_revision_id=? \
                     ORDER BY fld_requirement_id"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        if(results == ''):
            return True

        n_records = len(results)
        self.model.clear()
        for i in range(n_records):
            if (results[i][self._col_order[7]] == '-'):
                piter = None
            else:
                piter = self.model.get_iter_from_string(results[i][self._col_order[7]])

            self.model.append(piter, results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)

        root = self.model.get_iter_root()
        if root is not None:
            path = self.model.get_path(root)
            col = self.treeview.get_column(0)
            self.treeview.row_activated(path, col)

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Requirement
        Object treeview.

        Keyword Arguments:
        treeview -- the Requirement Object treeview.
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
        Callback function to handle events for the REQUIREMENT Object treeview.
        It is called whenever the REQUIREMENT Object treeview is clicked or a
        row is activated.  It will save the previously selected row in the
        REQUIREMENT Object treeview.

        Keyword Arguments:
        treeview -- the Requirement Object gtk.TreeView.
        path     -- the actived row gtk.TreeView path.
        column   -- the actived gtk.TreeViewColumn.
        """

        selection = self.treeview.get_selection()
        (self.model, self.selected_row) = selection.get_selected()

        if self.selected_row is not None:
            self.load_notebook()

        return False

    def _update_tree(self, columns, values):
        """
        Updates the values in the Requirement Object TreeView.

        Keyword Arguments:
        columns -- a list of integers representing the column numbers to
                   update.
        values  -- a list of new values for the Requirement Object
                   TreeView.
        """

        for i in columns:
            self.model.set_value(self.selected_row, i, values[i])

        return False

    def _vandv_tree_edit(self, cell, path, new_text, position, model):
        """
        Called whenever a TreeView CellRenderer is edited.

        Keyword Arguments:
        cell     -- the CellRenderer that was edited.
        path     -- the TreeView path of the CellRenderer that was edited.
        new_text -- the new text in the edited CellRenderer.
        position -- the column position of the edited CellRenderer.
        model    -- the TreeModel the CellRenderer belongs to.
        """

        if(position == 4):
            model[path][position] = float(new_text)
        else:
            model[path][position] = new_text

    def requirement_add(self, widget, type_):
        """
        Adds a new Requirement to the Program's database.

        Keyword Arguments:
        widget -- the widget that called this function.
        type_  -- the type of Requirement to add; 0 = sibling, 1 = child.
        """

        # Find the selected requirement.
        selection = self.treeview.get_selection()
        (model, self.selected_row) = selection.get_selected()

        if(type_ == 0):
            _parent = "-"
            if self.selected_row is not None:
                prow = self.model.iter_parent(self.selected_row)
                if prow is not None:
                    _parent = self.model.get_string_from_iter(prow)

            n_requirements = _util.add_items(_("Derived Requirement"))

        elif(type_ == 1):
            _parent = "-"
            if self.selected_row is not None:
                _parent = self.model.get_string_from_iter(self.selected_row)

            n_requirements = _util.add_items(_("Sibling Requirement"))

        for i in range(n_requirements):

            requirement_name = "New Requirement_" + str(i)
            if self.selected_row is not None:
                _revision = self.model.get_value(self.selected_row, 0)
                _assembly = self.model.get_value(self.selected_row, 2)
            else:
                if(_conf.RTK_MODULES[0] == 1):
                    _revision = self._app.REVISION.revision_id
                else:
                    _revision = 0
                _assembly = self._app.ASSEMBLY.assembly_id

            values = (_revision, _assembly, requirement_name, _parent)
            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_requirements \
                        (fld_revision_id, fld_assembly_id, \
                         fld_requirement_desc, fld_parent_requirement) \
                        VALUES (%d, %d, '%s', '%s')"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_requirements \
                        (fld_revision_id, fld_assembly_id, \
                         fld_requirement_desc, fld_parent_requirement) \
                        VALUES (?, ?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("requirement.py: Failed to add requirement.")
                return True

        self._app.REVISION.load_tree()
        self.load_tree()

        return False

    def requirement_delete(self, menuitem):
        """
        Deletes the currently selected Requirement from the Program's MySQL or
        SQLite3 database.

        Keyword Arguments:
        menuitem -- the gtk.MenuItem that called this function.
        """

        selection = self.treeview.get_selection()
        (model, row) = selection.get_selected()

        values = (model.get_string_from_iter(row),)
        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_requirements \
                     WHERE fld_parent_requirement=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_requirements \
                     WHERE fld_parent_requirement=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.user_log.error("requirement.py: Failed to delete derived requirement.")
            return True

        if(_conf.RTK_MODULES[0] == 1):
            values = (self._app.REVISION.revision_id, \
                      model.get_value(row, 1))
        else:
            values = (0, model.get_value(row, 1))

        if(_conf.BACKEND == 'mysql'):
            query = "DELETE FROM tbl_requirements \
                 WHERE fld_revision_id=%d \
                 AND fld_requirement_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "DELETE FROM tbl_requirements \
                 WHERE fld_revision_id=? \
                 AND fld_requirement_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.user_log.error("requirement.py: Failed to delete requirement.")
            return True

        self.load_tree()

        return False

    def requirement_save(self, widget=None):
        """
        Saves the Requirement Object treeview information to the Program's
        database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        self.model.foreach(self._save_line_item)

        return False

    def _save_line_item(self, model, path_, row):
        """
        Saves each row in the Requirement Object treeview model to the MySQL
        or SQLite3 database.

        Keyword Arguments:
        model -- the Requirement Object treemodel.
        path_ -- the path of the active row in the Requirement Object
                 treemodel.
        row   -- the selected row in the Requirement Object treeview.
        """

        values = (model.get_value(row, self._col_order[2]), \
                  model.get_value(row, self._col_order[3]), \
                  model.get_value(row, self._col_order[4]), \
                  model.get_value(row, self._col_order[5]), \
                  model.get_value(row, self._col_order[6]), \
                  model.get_value(row, self._col_order[7]), \
                  model.get_value(row, self._col_order[8]), \
                  model.get_value(row, self._col_order[9]), \
                  model.get_value(row, self._col_order[10]), \
                  model.get_value(row, self._col_order[11]), \
                  model.get_value(row, self._col_order[12]), \
                  model.get_value(row, self._col_order[13]), \
                  model.get_value(row, self._col_order[14]), \
                  model.get_value(row, self._col_order[0]), \
                  model.get_value(row, self._col_order[1]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_requirements \
                     SET fld_assembly_id=%d, fld_requirement_desc='%s', \
                         fld_requirement_type=%d, fld_requirement_code='%s', \
                         fld_derived=%d, fld_parent_requirement='%s', \
                         fld_validated=%d, fld_validated_date='%s', \
                         fld_owner='%s', fld_specification='%s', \
                         fld_page_number='%s', fld_figure_number='%s', \
                         fld_parent_id=%d \
                     WHERE fld_revision_id=%d \
                     AND fld_requirement_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_requirements \
                     SET fld_assembly_id=?, fld_requirement_desc=?, \
                         fld_requirement_type=?, fld_requirement_code=?, \
                         fld_derived=?, fld_parent_requirement=?, \
                         fld_validated=?, fld_validated_date=?, \
                         fld_owner=?, fld_specification=?, \
                         fld_page_number=?, fld_figure_number=?, \
                         fld_parent_id=? \
                     WHERE fld_revision_id=? \
                     AND fld_requirement_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("requirement.py: Failed to save requirement.")
            return True

        return False

    def _vandv_task_add(self, widget, type_=0):
        """
        Adds a new Verification and Validation task to the selected
        Requirement to the Program's MySQL or SQLite3 database.

        Keyword Arguments:
        widget -- the widget that called this function.
        type_  -- type of add; 0 = add new task, 1 = add existing task
        """

        if(type_ == 0):
            task_name = _("New V & V Task")

            if(_conf.RTK_MODULES[0] == 1):
                values = (self._app.REVISION.revision_id, task_name)
            else:
                values = (0, task_name)

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_validation \
                         (fld_revision_id, fld_task_desc) \
                         VALUES (%d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_validation \
                         (fld_revision_id, fld_task_desc) \
                         VALUES (?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)
            if not results:
                self._app.debug_log.error("requirement.py: Failed to add V&V task.")
                return True

            if(_conf.BACKEND == 'mysql'):
                query = "SELECT LAST_INSERT_ID()"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "SELECT seq \
                         FROM sqlite_sequence \
                         WHERE name='tbl_validation'"

            task_id = self._app.DB.execute_query(query,
                                                 None,
                                                 self._app.ProgCnx)

            if(_conf.RTK_MODULES[0] == 1):
                values = (self._app.REVISION.revision_id, task_id[0][0],
                          self.model.get_value(self.selected_row, 1))
            else:
                values = (0, task_id[0][0],
                          self.model.get_value(self.selected_row, 1))

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_validation_matrix \
                         (fld_revision_id, fld_validation_id, \
                          fld_requirement_id) \
                         VALUES (%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_validation_matrix \
                         (fld_revision_id, fld_validation_id, \
                          fld_requirement_id) \
                         VALUES (?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("requirement.py: Failed to add V&V task.")
                return True

        elif(type_ == 1):
            model = self.cmbVandVTasks.get_model()
            row = self.cmbVandVTasks.get_active_iter()
            task_id = int(model.get_value(row, 1))

            if(_conf.RTK_MODULES[0] == 1):
                values = (self._app.REVISION.revision_id, task_id,
                          self.model.get_value(self.selected_row, 1))
            else:
                values = (0, task_id,
                          self.model.get_value(self.selected_row, 1))

            if(_conf.BACKEND == 'mysql'):
                query = "INSERT INTO tbl_validation_matrix \
                         (fld_revision_id, fld_validation_id, \
                          fld_requirement_id) \
                         VALUES (%d, %d, %d)"
            elif(_conf.BACKEND == 'sqlite3'):
                query = "INSERT INTO tbl_validation_matrix \
                         (fld_revision_id, fld_validation_id, \
                          fld_requirement_id) \
                         VALUES (?, ?, ?)"

            results = self._app.DB.execute_query(query,
                                                 values,
                                                 self._app.ProgCnx,
                                                 commit=True)

            if not results:
                self._app.debug_log.error("requirement.py: Failed to associate V&V task.")
                return True

        self._vandv_tab_load()

        return False

    def _vandv_tasks_save(self, widget):
        """
        Saves the Validation Task list treeview information to the Program's
        MySQL or SQLite3 database.

        Keyword Arguments:
        widget -- the widget that called this function.
        """

        model = self.tvwValidation.get_model()
        model.foreach(self._vandv_line_item_save)

        return False

    def _vandv_line_item_save(self, model, path_, row):
        """
        Saves each task associated with the selected Requirement to the
        program's MySQL or SQLite3 database.

        Keyword Arguments:
        model -- the Validation Task list treemodel.
        path_ -- the path of the active row in the Validation Task list
                 treemodel.
        row   -- the selected row in the Validation Task list treeview.
        """

        values = (model.get_value(row, self._col_order[1]),
                  model.get_value(row, self._col_order[2]),
                  model.get_value(row, self._col_order[3]),
                  model.get_value(row, self._col_order[4]),
                  model.get_value(row, self._col_order[0]))

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_validation \
                     SET fld_task_desc='%s', fld_start_date='%s', \
                         fld_end_date='%s', fld_status=%f \
                     WHERE fld_validation_id=%d"
        if(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_validation \
                     SET fld_task_desc=?, fld_start_date=?, \
                         fld_end_date=?, fld_status=? \
                     WHERE fld_validation_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("requirement.py: Failed to save V&V task.")
            return True

        return False

    def load_notebook(self):
        """
        Method to load the gtk.Notebook widgets for the selected REQUIREMENT
        object.
        """

        if self.selected_row is not None:
            self._general_data_tab_load()
            self._vandv_tab_load()

        if(self._app.winWorkBook.get_child() is not None):
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())

        self._app.winWorkBook.add(self.vbxRequirement)
        self._app.winWorkBook.show_all()

        self._app.winWorkBook.set_title(_("RTK Work Book: Requirement"))

        self.btnAddVandVTask.hide()
        self.btnAssignVandVTask.hide()
        self.btnSaveVandVTask.hide()
        self.cmbVandVTasks.hide()

        return False

    def _callback_check(self, check, index_):
        """
        Callback function to retrieve and save checkbutton changes.

        Keyword Arguments:
        check  -- the checkbutton that called the function.
        index_ -- the position in the Requirement Object _attribute list
                  associated with the data from the calling checkbutton.
        """

        # Update the Requirement Tree.
        self.model.set_value(self.selected_row, index_, check.get_active())

        return False

    def _callback_combo(self, combo, index_):
        """
        Callback function to retrieve and save combobox changes.

        Keyword Arguments:
        combo  -- the combobox that called the function.
        index_ -- the position in the Requirement Object _attribute list
                  associated with the data from the calling combobox.
        """

        # Update the Requirement Tree.
        self.model.set_value(self.selected_row, index_,
                             int(combo.get_active()))

        if(index_ == 4):                    # Requirement type.
            self._create_code()

        return False

    def _callback_entry(self, entry, event, convert, _index_):
        """
        Callback function to retrieve and save entry changes.

        Keyword Arguments:
        entry   -- the entry that called the function.
        event   -- the gtk.gdk.Event that called this function.
        convert -- the data type to convert the entry contents to.
        _index_ -- the position in the Requirement Object _attribute list
                   associated with the data from the calling entry.
        """

        if(convert == 'text'):
            if(_index_ == 3):
                text_ = self.txtRequirement.get_text(*self.txtRequirement.get_bounds())
            else:
                text_ = entry.get_text()

        elif(convert == 'int'):
            text_ = int(entry.get_text())

        elif(convert == 'float'):
            text_ = float(entry.get_text().replace('$', ''))

        # Update the Requirement Tree.
        try:
            self.model.set_value(self.selected_row, _index_, text_)
        except TypeError:                   # There are no requirements.
            pass

        return False

    def _create_code(self):
        """
        This function creates the Requirement code based on the type of
        requirement it is and it's index in the database.
        """

        cmbmodel = self.cmbRqmtType.get_model()
        cmbrow = self.cmbRqmtType.get_active_iter()

        prefix = cmbmodel.get_value(cmbrow, 1)
        suffix = str(self.model.get_value(self.selected_row, 1))

        zeds = 4 - len(suffix)
        pad = '0' * zeds

        code = '%s-%s%s' % (prefix, pad, suffix)

        self.model.set_value(self.selected_row, 5, code)
        self.txtCode.set_text(code)

        return False

    def _notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the Tree Book notebook page is changed.

        Keyword Arguments:
        notebook -- the Tree Book notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = Revision Tree
                    1 = Function Tree
                    2 = Requirements Tree
                    3 = Hardware Tree
                    4 = Software Tree
                    4 = Validation Tree
                    5 = Reliability Growth Test Tree
                    6 = Field Incident Tree
        """

        if(page_num == 0):
            try:
                self.btnSaveRequirement.show()
                self.btnAddVandVTask.hide()
                self.btnAssignVandVTask.hide()
                self.btnSaveVandVTask.hide()
                self.cmbVandVTasks.hide()
            except AttributeError:
                pass
        elif(page_num == 1):
            try:
                self.btnSaveRequirement.hide()
                self.btnAddVandVTask.show()
                self.btnAssignVandVTask.show()
                self.btnSaveVandVTask.show()
                self.cmbVandVTasks.show()
            except AttributeError:
                pass
