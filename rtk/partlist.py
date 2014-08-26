#!/usr/bin/env python
"""
This is the List Book for RTK.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       partlist.py is part of the RTK Project
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


class ListWindow(gtk.Window):
    """
    This class is the windows containing the lists associated with the selected
    Revision, Function, or Assembly in the upper window.
    """

    def __init__(self, application):
        """
        Initializes the List Class.

        :param RTK application: the current instance of the RTK application.
        """

        self._app = application

        # Define private dictionary variables.
        # Dictionary to hold the Assembly ID/Hardware Tree treemodel paths.
        # This is used to keep the Hardware Tree and the Parts List in sync.
        self._treepaths = {}

        # Define private list variables.
        self._VISIBLE_PARTS_ = []

        # Define private scalar variables.
        self._assembly_id = 0

        # Define public dictionary variables.
        self.parttreepaths = {}
        self.dicPartValues = {}

        # Define public object variables.
        self.objPartModel = None

        # Create a new window and set its properties.
        gtk.Window.__init__(self)
        self.set_title(_(u"RTK Lists"))
        self.set_resizable(True)
        self.set_deletable(False)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)

        _n_screens = gtk.gdk.screen_get_default().get_n_monitors()
        _width = gtk.gdk.screen_width() / _n_screens
        _height = gtk.gdk.screen_height()

        self.set_default_size((_width / 3) - 10, (2 * _height / 7))
        self.set_border_width(5)
        self.set_position(gtk.WIN_POS_NONE)
        self.move((2 * _width / 3), 0)

        self.connect('delete_event', self.delete_event)

        # Create the gtk.Notebook widget to hold the parts list, RG tests list,
        # program incidents, and survival analyses list.
        self.notebook = gtk.Notebook()

        # Find the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[1] == 'left':
            self.notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[1] == 'right':
            self.notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[1] == 'top':
            self.notebook.set_tab_pos(gtk.POS_TOP)
        else:
            self.notebook.set_tab_pos(gtk.POS_BOTTOM)

        self.notebook.connect('switch-page', self.notebook_page_switched)

        # Create the parts list tab for the LIST Object.
        (self.tvwPartsList,
         self._col_order) = _widg.make_treeview('Parts', 7, self._app,
                                                None, _conf.RTK_COLORS[14],
                                                _conf.RTK_COLORS[15])
        self.objPartModel = self.tvwPartsList.get_model()
        if self._parts_list_tab_create():
            self._app.debug_log.error("partlist.py: Failed to create Parts "
                                      "List tab.")

        # Create the reliability testing tab for the List class.
        (self.tvwTesting,
         self._rg_col_order) = _widg.make_treeview('Testing', 11, self._app,
                                                   None, _conf.RTK_COLORS[14],
                                                   _conf.RTK_COLORS[15])
        if self._rel_testing_tab_create():
            self._app.debug_log.error("partlist.py: Failed to create "
                                      "Reliability Test tab.")

        # Create the program incidents tab for the LIST object.
        (self.tvwIncidents,
         self._incident_col_order) = _widg.make_treeview('Incidents', 14,
                                                         self._app, None,
                                                         _conf.RTK_COLORS[12],
                                                         _conf.RTK_COLORS[13])
        self.tvwIncidents.connect('row_activated',
                                  self._treeview_row_changed, 1)

        if self._incidents_tab_create():
            self._app.debug_log.error("partlist.py: Failed to create Program "
                                      "Incidents tab.")

        # Create the dataset tab for the LIST object.
        (self.tvwDatasets,
         self._dataset_col_order) = _widg.make_treeview('Dataset', 16,
                                                        self._app, None,
                                                        _conf.RTK_COLORS[12],
                                                        _conf.RTK_COLORS[13])
        self.tvwDatasets.connect('row_activated',
                                 self._treeview_row_changed, 2)

        if self._survival_tab_create():
            self._app.debug_log.error("partlist.py: Failed to create Datasets "
                                      "tab.")

        # Create a statusbar for the list/matrix window.
        self.statusbar = gtk.Statusbar()

        _vbox = gtk.VBox()
        _vbox.pack_start(self.notebook, expand=True, fill=True)
        _vbox.pack_start(self.statusbar, expand=False, fill=False)

        self.add(_vbox)
        self.show_all()

        self.statusbar.push(1, _(u"Ready"))

    def _parts_list_tab_create(self):
        """
        Method to create the parts list gtk.TreeView.
        """

        self.tvwPartsList.connect('button_release_event', self._tree_clicked)
        self.tvwPartsList.connect('row_activated', self._row_activated)

        # Create the Parts list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwPartsList)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Parts List</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of parts for the "
                                  u"selected Revision, Function, or "
                                  u"Hardware item."))

        self.notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _rel_testing_tab_create(self):
        """
        Method to create the tab containing the list of reliability growth
        and reliability demonstration plans for the Program.
        """

        # Create the Reliability Test list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.tvwTesting)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Reliability\nTests</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of HALT, HASS, ALT, "
                                  u"ESS, reliability growth and reliability "
                                  u"demonstration tests for the selected "
                                  u"Revision or Hardware item."))

        self.notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _incidents_tab_create(self):
        """
        Method to create the tab containing the list of program incidents.
        """

        # Create the Program Incidents list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.tvwIncidents)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Program\nIncidents</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of program incidents "
                                  u"for the selected Revision, Hardware item, "
                                  u"or Software item."))

        self.notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _survival_tab_create(self):
        """
        Method to create the tab containing the list of survival analyses.
        """

        # Create the Program Incidents list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add_with_viewport(self.tvwDatasets)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Survival\nAnalyses</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of survival (Weibull) "
                                  u"analyses for the selected Revision or "
                                  u"Hardware item."))

        self.notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def create_toolbar(self):
        """
        Creates the toolbar for the PartsList.
        """

        _toolbar = gtk.Toolbar()

        # Add part button.
        button = gtk.ToolButton(stock_id=gtk.STOCK_ADD)
        button.set_tooltip_text(_("Add a component to the currently selected assembly"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        button.set_icon_widget(image)
        button.connect('clicked', self._app.COMPONENT.component_add, None)
        _toolbar.insert(button, 0)

        # Delete part button
        button = gtk.ToolButton(stock_id=gtk.STOCK_DELETE)
        button.set_tooltip_text(_("Delete the currently selected component."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/delete.png')
        button.set_icon_widget(image)
        button.set_property('name', 'part')
        button.connect('clicked', self._app.COMPONENT.component_delete)
        _toolbar.insert(button, 1)

        _toolbar.insert(gtk.SeparatorToolItem(), 2)

        # Cut button
        button = gtk.ToolButton(stock_id=gtk.STOCK_CUT)
        button.set_tooltip_text(_("Cut the currently selected component."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/cut.png')
        button.set_icon_widget(image)
        button.set_label(_("Cut"))
        button.connect('clicked', _util.cut_copy_paste, 0)
        button.show()
        _toolbar.insert(button, 3)

        # Copy button
        button = gtk.ToolButton(stock_id=gtk.STOCK_COPY)
        button.set_tooltip_text(_("Copy the currently selected component."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/copy.png')
        button.set_icon_widget(image)
        button.set_label(_("Copy"))
        button.connect('clicked', _util.cut_copy_paste, 1)
        button.show()
        _toolbar.insert(button, 4)

        # Paste button
        button = gtk.ToolButton(stock_id=gtk.STOCK_PASTE)
        button.set_tooltip_text(_("Paste the contents of the clipboard."))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/paste.png')
        button.set_icon_widget(image)
        button.set_label(_("Paste"))
        button.connect('clicked', _util.cut_copy_paste, 2)
        button.show()
        _toolbar.insert(button, 5)

        _toolbar.insert(gtk.SeparatorToolItem(), 6)

        # Undo button
        button = gtk.ToolButton(stock_id=gtk.STOCK_UNDO)
        button.set_tooltip_text(_("Undo the last change"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/undo.png')
        button.set_icon_widget(image)
        button.set_label(_("Undo"))
        button.connect('clicked', _util.undo, self)
        button.show()
        _toolbar.insert(button, 7)

        # Redo button
        button = gtk.ToolButton(stock_id=gtk.STOCK_REDO)
        button.set_tooltip_text(_("Redo the last change"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/redo.png')
        button.set_icon_widget(image)
        button.set_label(_("Redo"))
        button.connect('clicked', _util.redo, self)
        button.show()
        _toolbar.insert(button, 8)

        _toolbar.insert(gtk.SeparatorToolItem(), 9)

        # Calculate button
        button = gtk.ToolButton(label=_("Calculate"))
        image = gtk.Image()
        image.set_from_file(_conf.ICON_DIR + '32x32/calculate.png')
        button.set_icon_widget(image)
        # button.connect('clicked', self._app.COMPONENT.calculate)
        button.show()
        _toolbar.insert(button, 10)

        _toolbar.show()

        return _toolbar

    def load_part_tree(self, query):
        """
        Populates the part list treeview with the parts associated with the
        currently selected Revision, Function, or Assembly.

        :param str query: the SQL query to execute to retrieve the list of
                          parts associated with the calling Revision, Function,
                          or Assembly.
        """

        _results = self._app.DB.execute_query(query, None, self._app.ProgCnx)
        try:
            _n_parts = len(_results)
        except TypeError:
            _n_parts = 0

        self.objPartModel.clear()
        for i in range(_n_parts):
            _row = self.objPartModel.append(None, _results[i])
            self._treepaths[_results[i][1]] = self.objPartModel.get_path(_row)

        self.tvwPartsList.set_model(model=self.objPartModel)

        return False

    def load_test_tree(self, query):
        """
        Populates the test list treeview with the tests associated with the
        currently selected Assembly.

        :param str query: the SQL query to execute to retrieve the list of
                          reliability tests associated with the selected
                          revision, hardware item, or software item.
        """

        _model = self.tvwTesting.get_model()
        _model.clear()

        _results = self._app.DB.execute_query(query, None, self._app.ProgCnx)
        try:
            _n_tests = len(_results)
        except TypeError:
            _n_tests = 0

        # Load the model with the returned results.
        for i in range(_n_tests):
            _model.append(None, _results[i])

        return False

    def load_incident_tree(self, query):
        """
        Populates the part list treeview with the parts associated with the
        currently selected Assembly.

        :param str query: the SQL query to execute to retrieve the list of
                          incidents associated with the selected revision,
                          hardware item, or software item.
        """

        _model = self.tvwIncidents.get_model()
        _model.clear()

        _results = self._app.DB.execute_query(query, None, self._app.ProgCnx)
        try:
            _n_incidents = len(_results)
        except TypeError:
            _n_incidents = 0

        # Load the model with the returned results.
        for i in range(_n_incidents):
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
            _model.append(None, _data)

        return False

    def load_dataset_tree(self, query):
        """
        Populates the part list treeview with the parts associated with the
        currently selected Assembly.

        :param str query: the SQL query to execute to retrieve the list of
                          survival analysis data sets associated with the
                          selected revision or hardware item.
        """

        _model = self.tvwDatasets.get_model()
        _model.clear()

        _results = self._app.DB.execute_query(query, None, self._app.ProgCnx)

        try:
            _n_datasets = len(_results)
        except TypeError:
            _n_datasets = 0

        # Load the model with the returned results.
        for i in range(_n_datasets):
            _model.append(None, _results[i])

        return False

    def _tree_clicked(self, __treeview, __event):
        """
        Called whenever the Parts List tree is clicked.

        :param gtk.TreeView __treeview: the gtk.TreeView() that was clicked.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        """

        self._treeview_row_changed()

    def _row_activated(self, __treeview, __path, __column):
        """
        Called whenever a row in one of the trees is activated.

        treeview -- the TreeView that recieved the signal.
        path_    -- the path of the row activated in the treeview.
        column   -- the column in the activated row that was selected.
        """

        self._treeview_row_changed()

    def _treeview_row_changed(self):
        """
        Called when a row in the Hardware object treeview is changed due to
        being clicked or activated.
        """

        # Now set the new selection.
        (_model, _row) = self.tvwPartsList.get_selection().get_selected()

        if _row is not None:
            self._assembly_id = _model.get_value(_row, 1)
            self._app.HARDWARE.model.foreach(self.find_hardware_tree_row)
            self._app.HARDWARE.part = True
            self._app.COMPONENT.load_notebook()

            return False
        else:
            return True

    def find_hardware_tree_row(self, model, __path, row):
        """
        Finds the corresponding row in the Hardware TreeView and sets that
        Hardware TreeView row active.  Called whenever the Parts List is
        clicked or row is activated.

        :param gtk.TreeModel model: the Hardware class gtk.TreeModel().
        path_ -- the path of the row activated in the Hardware Object
                 TreeModel.
        row   -- the row activated in the HARDWARE object
                 tree model.
        """

        if model.get_value(row, 1) == self._assembly_id:
            self._app.HARDWARE.selected_row = row
            self._app.HARDWARE.treeview.set_cursor(model.get_path(row),
                                                   None, False)

        return False

    def save_component(self):
        """
        Saves the List Tree information to the RTK Program database.
        """

        _model = self.tvwPartsList.get_model()

        if _model is not None:
            _model.foreach(self.save_line_item)

        return False

    def save_line_item(self, model, __path, row):
        """
        Called for each row in the PartsList Object TreeView when the
        gtk.TreeView data is saved.

        Keyword Arguments:
        model -- the Parts List object tree model.
        path_ -- the treeview path of the active row.
        row   -- the active row.
        """

        _values_ = (model.get_value(row, self._col_order[2]),
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

        _query_ = "UPDATE tbl_prediction \
                   SET fld_function_id=%d, fld_a1=%f, fld_a2=%f, \
                       fld_application_id=%d, fld_burnin_temperature=%f, \
                       fld_burnin_time=%f, fld_c1=%f, fld_c2=%f, fld_c3=%f, \
                       fld_c4=%f, fld_c5=%f, fld_c6=%f, fld_c7=%f, \
                       fld_capacitance=%f, fld_construction_id=%d, \
                       fld_current_ratio=%f, fld_cycles_id=%d, \
                       fld_cycling_rate=%f, fld_devices_lab=%d, \
                       fld_die_area=%f, fld_ea=%f, fld_ecc_id=%d, \
                       fld_element_id=%d, fld_esd_voltage=%f, \
                       fld_failures_field=%d, fld_failures_lab=%d, \
                       fld_family_id=%d, fld_feature_size=%f, fld_func_id=%d, \
                       fld_i1=%f, fld_i2=%f, fld_i3=%f, fld_i4=%f, \
                       fld_i5=%f, fld_i6=%f, fld_initial_temperature=%f, \
                       fld_insulation_id=%d, fld_junction_temperature=%f, \
                       fld_k1=%f, fld_k2=%f, fld_k3=%f, \
                       fld_knee_temperature=%f, fld_l1=%f, fld_l2=%f, \
                       fld_lambda_b=%f, fld_lambda_b0=%f, fld_lambda_b1=%f, \
                       fld_lambda_b2=%f, fld_lambda_bd=%f, fld_lambda_eos=%f, \
                       fld_lambda_g=%d, fld_lambda_o=%f, \
                       fld_manufacturing_id=%d, fld_max_rated_temperature=%f, \
                       fld_min_rated_temperature=%f, fld_number_contacts=%d, \
                       fld_number_elements=%d, fld_number_hand=%d, \
                       fld_number_pins=%d, fld_number_wave=%d, \
                       fld_operating_current=%f, fld_operating_freq=%f, \
                       fld_operating_power=%f, fld_operating_time_field=%f, \
                       fld_operating_voltage=%f, fld_package_id=%d, \
                       fld_pi_a=%f, fld_pi_c=%f, fld_pi_cf=%f, fld_pi_cyc=%f, \
                       fld_pi_e=%f, fld_pi_ecc=%f, fld_pi_f=%f, fld_pi_k=%f, \
                       fld_pi_m=%f, fld_pi_mfg=%f, fld_pi_pt=%f, fld_pi_q=%f, \
                       fld_pi_r=%f, fld_pi_sr=%f, fld_pi_u=%f, fld_pi_v=%f, \
                       fld_power_ratio=%f, fld_quality_id=%d, fld_r1=%f, \
                       fld_r2=%d, fld_r3=%f, fld_r4=%f, fld_r5=%f, fld_r6=%f, \
                       fld_rated_current=%f, fld_rated_power=%f, \
                       fld_rated_voltage=%f, fld_resistance=%f, \
                       fld_resistance_id=%d, fld_s1=%f, fld_s2=%f, fld_s3=%f, \
                       fld_s4=%f, fld_specification_id=%d, \
                       fld_specsheet_id=%d, fld_tbase=%f, \
                       fld_technology_id=%d, fld_temperature=%f, \
                       fld_temperature_lab=%f, fld_temperature_rise=%f, \
                       fld_test_time_lab=%f, fld_thermal_resistance=%f, \
                       fld_tref=%f, fld_voltage_ratio=%f, fld_years=%d \
                   WHERE fld_revision_id=%d AND fld_assembly_id=%d" % _values_
        if not self._app.DB.execute_query(_query_, None, self._app.ProgCnx,
                                          commit=True):
            self._app.debug_log.error("partlist.py:save_line_item - Failed to save part list information for Assembly ID %d to RTK Program database." % model.get_value(row, self._col_order[1]))
            return True

        return False

    def notebook_page_switched(self, __notebook, __page, page_num):
        """
        Called whenever the Lists notebook page is changed.

        Keyword Arguments:
        notebook -- the Parts List notebook widget.
        page     -- the newly selected page widget.
        page_num -- the newly selected page number.
                    0 = Parts List
                    1 = Reliability Tests List
                    2 = Field Incident List
                    3 = Survival Analyses List
        """

        if page_num == 0:
            self.set_title(_(u"RTK Parts List"))
        elif page_num == 1:
            self.set_title(_(u"RTK Reliability Tests List"))
        elif page_num == 2:
            self.set_title(_(u"RTK Program Incidents List"))
        elif page_num == 3:
            self.set_title(_(u"RTK Survival Analyses Lists"))
        else:
            self.set_title(_(u"RTK List Book"))

    def delete_event(self, __widget, __event):
        """
        Used to quit the RTK application when the X in the upper right corner
        is pressed.

        :param rtk.winTree winmain: the RTK application main window widget.
        "param gtk.gdk.Event event: the gtk.gdk.Event() that called this
                                    method.
        """

        gtk.main_quit()

        return False
