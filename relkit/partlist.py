#!/usr/bin/env python
""" This is the Parts List window for RelKit. """

__author__ = 'Andrew Rowland <darowland@ieee.org>'
__copyright__ = 'Copyright 2007 - 2012 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       partlist.py is part of the RelKit Project
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


class PartsListWindow(gtk.Window):
    """
    This class is the windows containing the lists associated with the
    selected Revision, Function, or Assembly in the upper window.
    """

    # TODO: Write code to update notebook widgets when editing the Partslist treeview.
    # TODO: Create GUI to set/edit user-defined column headings for all trees.

    def __init__(self, application):
        """
        Initializes the List Object.

        Keyword Arguments:
        application -- the RelKit application.
        """

        self._app = application

        self._VISIBLE_PARTS_ = []
        self.parttreepaths = {}
        self._treepaths = {}

        self.model = None
        self.selected_row = None
        self.full_model = None
        self._assembly_model = None
        self._function_model = None

        self._assembly_id = 0

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_title(_("RelKit Parts List"))
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        width = gtk.gdk.screen_width() / n_screens
        height = gtk.gdk.screen_height()

        self.set_default_size((width / 3) - 10, (2 * height / 7))
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((2 * width / 3), 0)

        # Create the gtk.Notebook widget to hold the parts list, RG incidents
        # list and field incidents list.
        self.notebook = gtk.Notebook()

        # Find the user's preferred gtk.Notebook tab position.
        if(_conf.TABPOS[1] == 'left'):
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif(_conf.TABPOS[1] == 'right'):
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif(_conf.TABPOS[1] == 'top'):
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

        self.notebook.connect('switch-page', self.notebook_page_switched)

# Create the parts list tab for the LIST Object.
        bg_color = _conf.RELIAFREE_COLORS[14]
        fg_color = _conf.RELIAFREE_COLORS[15]
        (self.tvwPartsList, self._col_order) = _widg.make_treeview('Parts', 7,
                                                                   self._app,
                                                                   None,
                                                                   bg_color,
                                                                   fg_color)
        if self._parts_list_tab_create():
            self._app.debug_log.error("partlist.py: Failed to create Parts List tab.")

# Create the reliability testing tab for the LIST Object.
        bg_color = _conf.RELIAFREE_COLORS[14]
        fg_color = _conf.RELIAFREE_COLORS[15]
        (self.tvwRG, self._rg_col_order) = _widg.make_treeview('RGIncidents',
                                                               13,
                                                               self._app,
                                                               None,
                                                               bg_color,
                                                               fg_color)
        if self._rel_testing_tab_create():
            self._app.debug_log.error("partlist.py: Failed to create Reliability Test tab.")

# Create the program incidents tab for the LIST object.
        bg_color = _conf.RELIAFREE_COLORS[12]
        fg_color = _conf.RELIAFREE_COLORS[13]
        (self.tvwIncidents,
         self._incident_col_order) = _widg.make_treeview('Incidents',
                                                         14,
                                                         self._app,
                                                         None,
                                                         bg_color,
                                                         fg_color)
        #self.tvwIncidents.connect('cursor_changed', self._treeview_row_changed,
        #                          None, None)
        self.tvwIncidents.connect('row_activated',
                                  self._treeview_row_changed, 1)

        if self._incidents_tab_create():
            self._app.debug_log.error("partlist.py: Failed to create Program Incidents tab.")

# Create the dataset tab for the LIST object.
        bg_color = _conf.RELIAFREE_COLORS[12]
        fg_color = _conf.RELIAFREE_COLORS[13]
        (self.tvwDatasets,
         self._dataset_col_order) = _widg.make_treeview('Dataset', 16,
                                                        self._app,
                                                        None,
                                                        bg_color,
                                                        fg_color)
        #self.tvwIncidents.connect('cursor_changed', self._treeview_row_changed,
        #                          None, None)
        self.tvwDatasets.connect('row_activated',
                                 self._treeview_row_changed, 2)

        if self._survival_tab_create():
            self._app.debug_log.error("partlist.py: Failed to create Datasets tab.")

# Create a statusbar for the list/matrix window.
        self.statusbar = gtk.Statusbar()

        vbox = gtk.VBox()
        vbox.pack_start(self.notebook, expand=True, fill=True)
        vbox.pack_start(self.statusbar, expand=False, fill=False)

        self.add(vbox)
        self.show_all()

        self.statusbar.push(1, _("Ready"))

    def _parts_list_tab_create(self):
        """
        Method to create the parts list gtk.TreeView.
        """

        self.tvwPartsList.connect('button_release_event', self._tree_clicked)
        self.tvwPartsList.connect('row_activated', self._row_activated)

        # Get the treemodel that contains the full list of parts.
        self.full_model = self.tvwPartsList.get_model()
        self.model = self.full_model
        self.selected_row = None

        # Create a filtered model for functions and hardware.
        self._function_model = self.full_model.filter_new()
        self._function_model.set_visible_func(self.get_function_parts,
                                              self._VISIBLE_PARTS_)

        self._assembly_model = self.full_model.filter_new()
        self._assembly_model.set_visible_func(self.get_assembly_parts,
                                              self._VISIBLE_PARTS_)

        # Create the Parts list.
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwPartsList)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _("Parts List")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the list of parts for the selected Revision, Requirement, Function, or Assembly."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _rel_testing_tab_create(self):
        """
        Method to create the tab containing the list of reliability growth
        and reliability demonstration plans for the Program.
        """

        # Create the Reliability Test list.
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwRG)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _("Reliability\nTests")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the list of HALT, HASS, ALT, ESS, reliability growth and reliability demonstration tests for the selected Assembly."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _incidents_tab_create(self):
        """
        Method to create the tab containing the list of program incidents.
        """

        # Create the Program Incidents list.
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwIncidents)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _("Program\nIncidents")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the list of program incidents for the selected Assembly."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def _survival_tab_create(self):
        """
        Method to create the tab containing the list of survival analyses.
        """

        # Create the Program Incidents list.
        scrollwindow = gtk.ScrolledWindow()
        scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrollwindow.add_with_viewport(self.tvwDatasets)

        frame = _widg.make_frame()
        frame.set_shadow_type(gtk.SHADOW_NONE)
        frame.add(scrollwindow)

        label = gtk.Label()
        _heading = _("Survival\nAnalyses")
        label.set_markup("<span weight='bold'>" + _heading + "</span>")
        label.set_alignment(xalign=0.5, yalign=0.5)
        label.set_justify(gtk.JUSTIFY_CENTER)
        label.show_all()
        label.set_tooltip_text(_("Displays the list of survival (Weibull) analyses."))

        self.notebook.insert_page(frame,
                                  tab_label=label,
                                  position=-1)

        return False

    def create_toolbar(self):
        """
        Creates the toolbar for the PartsList.
        """

        toolbar = gtk.Toolbar()

        # Add part button.
        button = gtk.ToolButton(stock_id = gtk.STOCK_ADD)
        button.set_tooltip_text(_("Add a component to the currently selected assembly"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.connect('clicked', self._app.COMPONENT.component_add, None)
        toolbar.insert(button, 0)

        # Delete part button
        button = gtk.ToolButton(stock_id = gtk.STOCK_DELETE)
        button.set_tooltip_text(_("Delete the currently selected component."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/delete.png')
        button.set_icon_widget(image)
        button.set_property('name', 'part')
        button.connect('clicked', self._app.COMPONENT.component_delete)
        toolbar.insert(button, 1)

        toolbar.insert(gtk.SeparatorToolItem(), 2)

        # Cut button
        button = gtk.ToolButton(stock_id = gtk.STOCK_CUT)
        button.set_tooltip_text(_("Cut the currently selected component."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/cut.png')
        button.set_icon_widget(image)
        button.set_label(_("Cut"))
        button.connect('clicked', _util.cut_copy_paste, 0)
        button.show()
        toolbar.insert(button, 3)

        # Copy button
        button = gtk.ToolButton(stock_id = gtk.STOCK_COPY)
        button.set_tooltip_text(_("Copy the currently selected component."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/copy.png')
        button.set_icon_widget(image)
        button.set_label(_("Copy"))
        button.connect('clicked', _util.cut_copy_paste, 1)
        button.show()
        toolbar.insert(button, 4)

        # Paste button
        button = gtk.ToolButton(stock_id = gtk.STOCK_PASTE)
        button.set_tooltip_text(_("Paste the contents of the clipboard."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/paste.png')
        button.set_icon_widget(image)
        button.set_label(_("Paste"))
        button.connect('clicked', _util.cut_copy_paste, 2)
        button.show()
        toolbar.insert(button, 5)

        toolbar.insert(gtk.SeparatorToolItem(), 6)

        # Undo button
        button = gtk.ToolButton(stock_id = gtk.STOCK_UNDO)
        button.set_tooltip_text(_("Undo the last change"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/undo.png')
        button.set_icon_widget(image)
        button.set_label(_("Undo"))
        button.connect('clicked', _util.undo, self)
        button.show()
        toolbar.insert(button, 7)

        # Redo button
        button = gtk.ToolButton(stock_id = gtk.STOCK_REDO)
        button.set_tooltip_text(_("Redo the last change"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/redo.png')
        button.set_icon_widget(image)
        button.set_label(_("Redo"))
        button.connect('clicked', _util.redo, self)
        button.show()
        toolbar.insert(button, 8)

        toolbar.insert(gtk.SeparatorToolItem(), 9)

        # Calculate button
        button = gtk.ToolButton(label=_("Calculate"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        #button.connect('clicked', self._app.COMPONENT.calculate)
        button.show()
        toolbar.insert(button, 10)

        toolbar.show()

        return(toolbar)

    def load_part_tree(self, query, values):
        """
        Populates the part list treeview with the parts associated with the
        currently selected Revision, Function, or Assembly.

        Keyword Arguments:
        query  -- the SQL query to execute to retrieve the list of parts
                  associated with the calling Revision, Function, or
                  Assembly.
        values -- the tuple of values to pass with the query.
        """

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx)

        self.full_model.clear()

        # Create an empty dictionary to hold the Assembly ID/Hardware Tree
        # treemodel paths.  This is used to keep the Hardware Tree and the
        # Parts List in sync.
        self._treepaths = {}

        n_parts = len(results)
        if(n_parts == 0):
            return True

        for i in range(n_parts):
            row = self.full_model.append(None, results[i])
            self._treepaths[results[i][1]] = self.full_model.get_path(row)

        self.tvwPartsList.set_model(self.full_model)

        return False

    def load_test_tree(self, _query_, _values_):
        """
        Populates the test list treeview with the tests associated with the
        currently selected Assembly.

        Keyword Arguments:
        query -- the SQL query to execute to retrieve the list of parts
                 associated with the calling Assembly.
        """

        return False

    def load_incident_tree(self, _query_, _values_):
        """
        Populates the part list treeview with the parts associated with the
        currently selected Assembly.

        Keyword Arguments:
        _query_  -- the SQL query to execute to retrieve the list of parts
                    associated with the calling Revision, Assembly, or Software
                    module.
        _values_ -- the tuple of values to pass with the query.
        """

        model = self.tvwIncidents.get_model()
        model.clear()

        results = self._app.DB.execute_query(_query_,
                                             _values_,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        n_incidents = len(results)

        # Load the model with the returned results.
        for i in range(n_incidents):
            model.append(None, results[i])

        return False

    def load_dataset_tree(self, _query_, _values_):
        """
        Populates the part list treeview with the parts associated with the
        currently selected Assembly.

        Keyword Arguments:
        _query_  -- the SQL query to execute to retrieve the list of parts
                    associated with the calling Revision, Assembly, or Software
                    module.
        _values_ -- the tuple of values to pass with the query.
        """

        model = self.tvwDatasets.get_model()
        model.clear()

        results = self._app.DB.execute_query(_query_,
                                             _values_,
                                             self._app.ProgCnx)

        if(results == '' or not results):
            return True

        n_datasets = len(results)

        # Load the model with the returned results.
        for i in range(n_datasets):
            model.append(None, results[i])

        return False

    def _tree_clicked(self, treeview, event):
        """
        Called whenever the Parts List tree is clicked.

        Keyword Arguments:
        treeview -- the TreeView that was clicked.
        event    -- a gtk.gdk.Event that called this function.
        """

        self._treeview_row_changed()

    def _row_activated(self, treeview, path_, column):
        """
        Called whenever a row in one of the trees is activated.

        Keyword Arguments:
        treeview -- the TreeView that recieved the signal.
        path_    -- the path of the row activated in the treeview.
        column   -- the column in the activated row that was selected.
        """

        self._treeview_row_changed()

    def _treeview_row_changed(self, treeview, path, column, _index_):
        """
        Called when a row in the Hardware object treeview is changed due to
        being clicked or activated.
        """

        # First save the previously selected row.
        #if self.selected_row is not None:
        #    path = self.model.get_path(self.selected_row)
        #    self.save_line_item(self.model, path, self.selected_row)

        # Now set the new selection.
        #selection = self.tvwPartsList.get_selection()
        #(self.model, self.selected_row) = selection.get_selected()

        #if self.selected_row is not None:
        #    self._assembly_id = self.model.get_value(self.selected_row, 1)
        #    self._app.HARDWARE.model.foreach(self.find_hardware_tree_row)
        #    self._app.HARDWARE.ispart = True
        #    self._app.COMPONENT.load_notebook()
        #    return False
        #else:
        #    return True
        import notebook as _note
        if(_index_ == 1):                   # Incident list
            self.winWorkBook2 = _note.WorkBookWindow(self._app)

        return False

    def find_hardware_tree_row(self, model, path_, row):
        """
        Finds the corresponding row in the Hardware TreeView and sets that
        Hardware TreeView row active.  Called whenever the Parts List is
        clicked or row is activated.

        Keyword Arguments:
        model -- the HARDWARE object tree model.
        path_ -- the path of the row activated in the Hardware Object
                 TreeModel.
        row   -- the row activated in the HARDWARE object
                 tree model.
        """

        if(model.get_value(row, 1) == self._assembly_id):
            self._app.HARDWARE.selected_row = row
            self._app.HARDWARE.treeview.set_cursor(model.get_path(row),
                                                   None, False)

        return False

    def get_function_parts(self, model, row, parts):
        """
        Filters the Parts List TreeView to show only the components associated
        with the currently selected Function Object.

        Keyword Arguments:
        model -- the Parts List filtered model.
        row   -- the row in the filtered model.
        parts -- the list of part assembly ids.
        """

        return model.get_value(row, 1) in parts

    def get_assembly_parts(self, model, row, parts):
        """
        Filters the Parts List TreeView to show only the components associated
        with the currently selected Assembly Object.

        Keyword Arguments:
        model -- the Parts List filtered model.
        row   -- the row in the filtered model.
        parts -- the list of part assembly ids.
        """

        return model.get_value(row, 1) in parts

    def save_component(self):
        """
        Saves the Hardware Tree information to the project's MySQL or SQLite3
        database.
        """

        self.full_model.foreach(self.save_line_item)

        return False

    def save_line_item(self, model, path_, row):
        """
        Called for each row in the PartsList Object TreeView when the
        gtk.TreeView data is saved.

        Keyword Arguments:
        model -- the Parts List object tree model.
        path_ -- the treeview path of the active row.
        row   -- the active row.
        """

        try:
            values = (model.get_value(row, self._col_order[2]),
                      model.get_value(row, self._col_order[3]),
                      model.get_value(row, self._col_order[4]),
                      model.get_value(row, self._col_order[5]),
                      model.get_value(row, self._col_order[6]),
                      model.get_value(row, self._col_order[7]),
                      model.get_value(row, self._col_order[8]),
                      model.get_value(row, self._col_order[9]),
                      model.get_value(row, self._col_order[10]),
                      model.get_value(row, self._col_order[11]),
                      model.get_value(row, self._col_order[12]),
                      model.get_value(row, self._col_order[13]),
                      model.get_value(row, self._col_order[14]),
                      model.get_value(row, self._col_order[15]),
                      model.get_value(row, self._col_order[16]),
                      model.get_value(row, self._col_order[17]),
                      model.get_value(row, self._col_order[18]),
                      model.get_value(row, self._col_order[19]),
                      model.get_value(row, self._col_order[20]),
                      model.get_value(row, self._col_order[21]),
                      model.get_value(row, self._col_order[22]),
                      model.get_value(row, self._col_order[23]),
                      model.get_value(row, self._col_order[24]),
                      model.get_value(row, self._col_order[25]),
                      model.get_value(row, self._col_order[26]),
                      model.get_value(row, self._col_order[27]),
                      model.get_value(row, self._col_order[28]),
                      model.get_value(row, self._col_order[29]),
                      model.get_value(row, self._col_order[30]),
                      model.get_value(row, self._col_order[31]),
                      model.get_value(row, self._col_order[32]),
                      model.get_value(row, self._col_order[33]),
                      model.get_value(row, self._col_order[34]),
                      model.get_value(row, self._col_order[35]),
                      model.get_value(row, self._col_order[36]),
                      model.get_value(row, self._col_order[37]),
                      model.get_value(row, self._col_order[38]),
                      model.get_value(row, self._col_order[39]),
                      model.get_value(row, self._col_order[40]),
                      model.get_value(row, self._col_order[41]),
                      model.get_value(row, self._col_order[42]),
                      model.get_value(row, self._col_order[43]),
                      model.get_value(row, self._col_order[44]),
                      model.get_value(row, self._col_order[45]),
                      model.get_value(row, self._col_order[46]),
                      model.get_value(row, self._col_order[47]),
                      model.get_value(row, self._col_order[48]),
                      model.get_value(row, self._col_order[49]),
                      model.get_value(row, self._col_order[50]),
                      model.get_value(row, self._col_order[51]),
                      model.get_value(row, self._col_order[52]),
                      model.get_value(row, self._col_order[53]),
                      model.get_value(row, self._col_order[54]),
                      model.get_value(row, self._col_order[55]),
                      model.get_value(row, self._col_order[56]),
                      model.get_value(row, self._col_order[57]),
                      model.get_value(row, self._col_order[58]),
                      model.get_value(row, self._col_order[59]),
                      model.get_value(row, self._col_order[60]),
                      model.get_value(row, self._col_order[61]),
                      model.get_value(row, self._col_order[62]),
                      model.get_value(row, self._col_order[63]),
                      model.get_value(row, self._col_order[64]),
                      model.get_value(row, self._col_order[65]),
                      model.get_value(row, self._col_order[66]),
                      model.get_value(row, self._col_order[67]),
                      model.get_value(row, self._col_order[68]),
                      model.get_value(row, self._col_order[69]),
                      model.get_value(row, self._col_order[70]),
                      model.get_value(row, self._col_order[71]),
                      model.get_value(row, self._col_order[72]),
                      model.get_value(row, self._col_order[73]),
                      model.get_value(row, self._col_order[74]),
                      model.get_value(row, self._col_order[75]),
                      model.get_value(row, self._col_order[76]),
                      model.get_value(row, self._col_order[77]),
                      model.get_value(row, self._col_order[78]),
                      model.get_value(row, self._col_order[79]),
                      model.get_value(row, self._col_order[80]),
                      model.get_value(row, self._col_order[81]),
                      model.get_value(row, self._col_order[82]),
                      model.get_value(row, self._col_order[83]),
                      model.get_value(row, self._col_order[84]),
                      model.get_value(row, self._col_order[85]),
                      model.get_value(row, self._col_order[86]),
                      model.get_value(row, self._col_order[87]),
                      model.get_value(row, self._col_order[88]),
                      model.get_value(row, self._col_order[89]),
                      model.get_value(row, self._col_order[90]),
                      model.get_value(row, self._col_order[91]),
                      model.get_value(row, self._col_order[92]),
                      model.get_value(row, self._col_order[93]),
                      model.get_value(row, self._col_order[94]),
                      model.get_value(row, self._col_order[95]),
                      model.get_value(row, self._col_order[96]),
                      model.get_value(row, self._col_order[97]),
                      model.get_value(row, self._col_order[98]),
                      model.get_value(row, self._col_order[99]),
                      model.get_value(row, self._col_order[100]),
                      model.get_value(row, self._col_order[101]),
                      model.get_value(row, self._col_order[102]),
                      model.get_value(row, self._col_order[103]),
                      model.get_value(row, self._col_order[104]),
                      model.get_value(row, self._col_order[105]),
                      model.get_value(row, self._col_order[106]),
                      model.get_value(row, self._col_order[107]),
                      model.get_value(row, self._col_order[108]),
                      model.get_value(row, self._col_order[109]),
                      model.get_value(row, self._col_order[110]),
                      model.get_value(row, self._col_order[111]),
                      model.get_value(row, self._col_order[112]),
                      model.get_value(row, self._col_order[0]),
                      model.get_value(row, self._col_order[1]))
        except TypeError:
            return True
        except IndexError:
            print self._col_order
            return True

        if(_conf.BACKEND == 'mysql'):
            query = "UPDATE tbl_prediction \
                     SET fld_function_id=%d, fld_a1=%f, fld_a2=%f, \
                         fld_application_id=%d, fld_burnin_temperature=%f, \
                         fld_burnin_time=%f, fld_c1=%f, fld_c2=%f, fld_c3=%f, \
                         fld_c4=%f, fld_c5=%f, fld_c6=%f, fld_c7=%f, \
                         fld_capacitance=%f, fld_construction_id=%d, \
                         fld_current_ratio=%f, fld_cycles_id=%d, \
                         fld_cycling_rate=%f, fld_devices_lab=%d, fld_die_area=%f, \
                         fld_ea=%f, fld_ecc_id=%d, fld_element_id=%d, \
                         fld_esd_voltage=%f, fld_failures_field=%d, \
                         fld_failures_lab=%d, fld_family_id=%d, fld_feature_size=%f, \
                         fld_func_id=%d, fld_i1=%f, fld_i2=%f, fld_i3=%f, fld_i4=%f, \
                         fld_i5=%f, fld_i6=%f, fld_initial_temperature=%f, \
                         fld_insulation_id=%d, fld_junction_temperature=%f, \
                         fld_k1=%f, fld_k2=%f, fld_k3=%f, fld_knee_temperature=%f, \
                         fld_l1=%f, fld_l2=%f, fld_lambda_b=%f, fld_lambda_b0=%f, \
                         fld_lambda_b1=%f, fld_lambda_b2=%f, fld_lambda_bd=%f, \
                         fld_lambda_eos=%f, fld_lambda_g=%d, fld_lambda_o=%f, \
                         fld_manufacturing_id=%d, fld_max_rated_temperature=%f, \
                         fld_min_rated_temperature=%f, fld_number_contacts=%d, \
                         fld_number_elements=%d, fld_number_hand=%d, fld_number_pins=%d, \
                         fld_number_wave=%d, fld_operating_current=%f, \
                         fld_operating_freq=%f, fld_operating_power=%f, \
                         fld_operating_time_field=%f, fld_operating_voltage=%f, \
                         fld_package_id=%d, fld_pi_a=%f, fld_pi_c=%f, fld_pi_cf=%f, \
                         fld_pi_cyc=%f, fld_pi_e=%f, fld_pi_ecc=%f, fld_pi_f=%f, \
                         fld_pi_k=%f, fld_pi_m=%f, fld_pi_mfg=%f, fld_pi_pt=%f, \
                         fld_pi_q=%f, fld_pi_r=%f, fld_pi_sr=%f, fld_pi_u=%f, \
                         fld_pi_v=%f, fld_power_ratio=%f, fld_quality_id=%d, \
                         fld_r1=%f, fld_r2=%d, fld_r3=%f, fld_r4=%f, fld_r5=%f, \
                         fld_r6=%f, fld_rated_current=%f, fld_rated_power=%f, \
                         fld_rated_voltage=%f, fld_resistance=%f, fld_resistance_id=%d, \
                         fld_s1=%f, fld_s2=%f, fld_s3=%f, fld_s4=%f, \
                         fld_specification_id=%d, fld_specsheet_id=%d, fld_tbase=%f, \
                         fld_technology_id=%d, fld_temperature=%f, \
                         fld_temperature_lab=%f, fld_temperature_rise=%f, \
                         fld_test_time_lab=%f, fld_thermal_resistance=%f, fld_tref=%f, \
                         fld_voltage_ratio=%f, fld_years=%d \
                    WHERE fld_revision_id=%d AND fld_assembly_id=%d"
        elif(_conf.BACKEND == 'sqlite3'):
            query = "UPDATE tbl_prediction \
                     SET fld_function_id=?, fld_a1=?, fld_a2=?, \
                         fld_application_id=?, fld_burnin_temperature=?, \
                         fld_burnin_time=?, fld_c1=?, fld_c2=?, fld_c3=?, \
                         fld_c4=?, fld_c5=?, fld_c6=?, fld_c7=?, \
                         fld_capacitance=?, fld_construction_id=?, \
                         fld_current_ratio=?, fld_cycles_id=?, \
                         fld_cycling_rate=?, fld_devices_lab=?, fld_die_area=?, \
                         fld_ea=?, fld_ecc_id=?, fld_element_id=?, \
                         fld_esd_voltage=?, fld_failures_field=?, \
                         fld_failures_lab=?, fld_family_id=?, fld_feature_size=?, \
                         fld_func_id=?, fld_i1=?, fld_i2=?, fld_i3=?, fld_i4=?, \
                         fld_i5=?, fld_i6=?, fld_initial_temperature=?, \
                         fld_insulation_id=?, fld_junction_temperature=?, \
                         fld_k1=?, fld_k2=?, fld_k3=?, fld_knee_temperature=?, \
                         fld_l1=?, fld_l2=?, fld_lambda_b=?, fld_lambda_b0=?, \
                         fld_lambda_b1=?, fld_lambda_b2=?, fld_lambda_bd=?, \
                         fld_lambda_eos=?, fld_lambda_g=?, fld_lambda_o=?, \
                         fld_manufacturing_id=?, fld_max_rated_temperature=?, \
                         fld_min_rated_temperature=?, fld_number_contacts=?, \
                         fld_number_elements=?, fld_number_hand=?, fld_number_pins=?, \
                         fld_number_wave=?, fld_operating_current=?, \
                         fld_operating_freq=?, fld_operating_power=?, \
                         fld_operating_time_field=?, fld_operating_voltage=?, \
                         fld_package_id=?, fld_pi_a=?, fld_pi_c=?, fld_pi_cf=?, \
                         fld_pi_cyc=?, fld_pi_e=?, fld_pi_ecc=?, fld_pi_f=?, \
                         fld_pi_k=?, fld_pi_m=?, fld_pi_mfg=?, fld_pi_pt=?, \
                         fld_pi_q=?, fld_pi_r=?, fld_pi_sr=?, fld_pi_u=?, \
                         fld_pi_v=?, fld_power_ratio=?, fld_quality_id=?, \
                         fld_r1=?, fld_r2=?, fld_r3=?, fld_r4=?, fld_r5=?, \
                         fld_r6=?, fld_rated_current=?, fld_rated_power=?, \
                         fld_rated_voltage=?, fld_resistance=?, fld_resistance_id=?, \
                         fld_s1=?, fld_s2=?, fld_s3=?, fld_s4=?, \
                         fld_specification_id=?, fld_specsheet_id=?, fld_tbase=?, \
                         fld_technology_id=?, fld_temperature=?, \
                         fld_temperature_lab=?, fld_temperature_rise=?, \
                         fld_test_time_lab=?, fld_thermal_resistance=?, fld_tref=?, \
                         fld_voltage_ratio=?, fld_years=? \
                    WHERE fld_revision_id=? AND fld_assembly_id=?"

        results = self._app.DB.execute_query(query,
                                             values,
                                             self._app.ProgCnx,
                                             commit=True)

        if not results:
            self._app.debug_log.error("partlist.py: Failed to save part list information to RelKit Program database.")
            return True

        return False

    def filter_parts_list(self, _index_):
        """
        Filters the PartsList TreeView to include only those parts associated
        with the currently selected Revision, Function, or Assembly

        Keyword Arguments:
        _index_ - the index of the TreeView that was clicked.
                  0 = Revision Tree
                  1 = Function Tree
                  2 = Requirements Tree
                  3 = Hardware Tree
                  4 = Validation Tree
                  5 = Reliability Growth Test Tree
                  6 = Fielded Units List
                  7 = Field Incidents Tree
                  8 = Parts List
        """

        del self._VISIBLE_PARTS_[:]

        # Select everything from the Parts table conditioned on the
        # Tree Book tree that was selected.
        if(_index_ == 0):                   # Selected the Revision Tree.
            self.tvwPartsList.set_model(self.full_model)
            self.model = self.full_model
            return False

        elif(_index_ == 1):                 # Selected the Function Tree.
            model = self._app.FUNCTION.model
            row = self._app.FUNCTION.selected_row

            if row is not None:
                function = model.get_value(row, 1)
            else:
                return True
            row = self.full_model.get_iter_first()
            while row is not None:
                if(self.full_model.get_value(row, 2) == function):
                    self._VISIBLE_PARTS_.append(self.full_model.get_value(row, 1))
                row = self.full_model.iter_next(row)

            self._function_model.refilter()
            self.tvwPartsList.set_model(self._function_model)
            self.model = self._function_model

            return False

        elif(_index_ == 3):                 # Selected the Hardware Tree.
            model = self._app.HARDWARE.model

            if not self._app.HARDWARE.ispart:
                row = self._app.HARDWARE.selected_row
            else:
                row = model.get_iter_from_string(self._app.HARDWARE.assembly)

            # Create an empty dictionary to hold the Assembly ID/Parts List
            # treemodel paths.  This is used to keep the Hardware Tree and the
            # Parts List in sync.
            self.parttreepaths = {}

            for i in range(model.iter_n_children(row)):
                child_row = model.iter_nth_child(row, i)
                if(model.get_value(child_row, 62) == self._app.HARDWARE.assembly):
                    self._VISIBLE_PARTS_.append(model.get_value(child_row, 1))

            self._assembly_model.refilter()
            self.tvwPartsList.set_model(self._assembly_model)
            self.model = self._assembly_model

            return False

        else:
            return True

    def notebook_page_switched(self, notebook, page, page_num):
        """
        Called whenever the Lists notebook page is changed.

        Keyword Arguments:
        notebook -- the Parts List notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = Parts List
                    1 = Reliability Tests List
                    2 = Field Incident List
        """

        if(page_num == 0):
            self.set_title(_("RelKit Parts List"))
        elif(page_num == 1):
            self.set_title(_("RelKit Reliability Tests List"))
        elif(page_num == 2):
            self.set_title(_("RelKit Program Incidents List"))
        else:
            self.set_title(_("RelKit Lists"))
