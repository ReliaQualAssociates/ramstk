#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.ListBook.py is part of the RTK Project
#
# All rights reserved.

"""
###############################
Hardware Package List Book View
###############################
"""

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
import pango
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
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
    from gui.gtk.Matrix import Matrix as rtkMatrix
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets
    from rtk.gui.gtk.Matrix import Matrix as rtkMatrix

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ListView(gtk.VBox):
    """
    The List Book view displays all the matrices and lists associated with the
    Hardware Class.  The attributes of a Hardware List Book view are:

    :ivar _dtc_matrices: the :py:class:`rtk.datamodels.Matrix.Matrix` data
                         controller instance.
    :ivar _lst_handler_id: list containing the signal handler ID's for each of
                           the gtk.Widget()s who have a callback method.
    :ivar gtk.Button btnSaveFuncHard: the gtk.Button() to save the Hardware/
                                      Hardware Matrix.
    :ivar gtk.Button btnSaveFuncSoft: the gtk.Button() to save the Hardware/
                                      Software Matrix.
    :ivar gtk.Button btnSaveFuncTest: the gtk.Button() to save the Hardware/
                                      Testing Matrix.
    :ivar mtxHardware: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that displays
                       the Hardware/Hardware Matrix.
    :ivar mtxSoftware: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that displays
                       the Hardware/Software Matrix.
    :ivar mtxTesting: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that displays
                      the Hardware/Testing Matrix.
    :ivar gtk.TreeView tvwPartsList: the gtk.TreeView() that displays the list
                                     of components/parts directly comprising
                                     the selected Hardware Assembly.
    :ivar gtk.TreeView tvwIncidentsList: the gtk.TreeView() that displays the
                                         list of program incidents related to
                                         the selected Hardware Assembly.
    """

    def __init__(self, modulebook):
        """
        Initializes the List Book view for the Hardware package.

        :param modulebook: the :py:class:`rtk.function.ModuleBook` to associate
                           with this List Book.
        """

        gtk.VBox.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._dtc_matrices = modulebook.mdcRTK.dtcMatrices
        self._mdcRTK = modulebook.mdcRTK

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        # Parts List page widgets.
        self.tvwPartsList = gtk.TreeView()
        self.tvwPartsList.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        # Incidents List page widgets.
        self.tvwIncidentList = gtk.TreeView()
        self.tvwIncidentList.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

        # Testing Matrix page widgets.
        self.btnSaveHardTest = Widgets.make_button(width=35, image='save')

        self.mtxTesting = rtkMatrix()
        self.mtxTesting.n_fixed_columns = 3

        # Validation Matrix page widgets.
        self.btnSaveHardVal = Widgets.make_button(width=35, image='save')

        self.mtxValidation = rtkMatrix()
        self.mtxValidation.n_fixed_columns = 3

        # Set tooltips for the gtk.Widgets().
        self.tvwPartsList.set_tooltip_markup(_(u"Displays the list of "
                                               u"components/parts directly "
                                               u"comprising the selected "
                                               u"Hardware assembly."))
        self.tvwIncidentList.set_tooltip_markup(_(u"Displays the list of "
                                                  u"incidents associated with "
                                                  u"the selected Hardware "
                                                  u"assembly."))
        self.mtxTesting.treeview.set_tooltip_markup(_(u"Displays the "
                                                      u"relationship between "
                                                      u"system Hardware and "
                                                      u"system development "
                                                      u"tests.  This matrix "
                                                      u"shows which tests "
                                                      u"partially (P) or "
                                                      u"completely (C) "
                                                      u"test a Hardware item, "
                                                      u"if at all."))
        self.mtxValidation.treeview.set_tooltip_markup(_(u"Displays the "
                                                         u"relationship "
                                                         u"between system "
                                                         u"Hardware and "
                                                         u"program Validation "
                                                         u"tasks.  This "
                                                         u"matrix shows which "
                                                         u"Validation task "
                                                         u"partially (P) or "
                                                         u"completely (C) "
                                                         u"validates a "
                                                         u"Hardware item, if "
                                                         u"at all."))

        # Connect widget signals to callback methods.  We do this here rather
        # than in each method so the _lst_handler_id index is the same as the
        # dicMatrix key for each Matrix.
        self._lst_handler_id.append(
            self.mtxTesting.connect('changed', self._on_matrix_changed, 0))
        self._lst_handler_id.append(
            self.mtxValidation.connect('changed', self._on_matrix_changed, 1))

        self._lst_handler_id.append(
            self.btnSaveHardTest.connect('clicked',
                                         self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.btnSaveHardVal.connect('clicked',
                                        self._on_button_clicked, 3))

        # Put it all together.
        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_notebook(self):
        """
        Method to create the Hardware class List View gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[1] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_parts_list_page(_notebook)
        self._create_incident_list_page(_notebook)
        self._create_testing_matrix_page(_notebook)
        self._create_validation_matrix_page(_notebook)

        return _notebook

    def _create_parts_list_page(self, notebook):
        """
        Method to create the Parts List page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Parts List page.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwPartsList)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _model = gtk.TreeStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.tvwPartsList.set_model(_model)

        _headings = [_(u"Reference\nDesignator"), _(u"Name"),
                     _(u"Part Number")]

        for _index, _heading in enumerate(_headings):
            _cell = gtk.CellRendererText()
            _cell.set_property('background', 'light grey')
            _cell.set_property('editable', 0)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('yalign', 0.1)
            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _heading + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.set_widget(_label)
            _column.set_visible(True)
            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)
            self.tvwPartsList.append_column(_column)

        # Add the Parts List page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Parts\nList</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of components/parts "
                                  u"directly comprising the selected Hardware "
                                  u"assembly."))

        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_incident_list_page(self, notebook):
        """
        Method to create the Incident List page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Incident List page.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwIncidentList)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _model = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING)
        self.tvwIncidentList.set_model(_model)

        _headings = [_(u"Incident\nID"), _(u"Short\nDescription"),
                     _(u"Incident\nStatus")]

        for _index, _heading in enumerate(_headings):
            _cell = gtk.CellRendererText()
            _cell.set_property('background', 'light grey')
            _cell.set_property('editable', 0)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('yalign', 0.1)
            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _heading + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _column = gtk.TreeViewColumn()
            _column.set_widget(_label)
            _column.set_visible(True)
            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)
            self.tvwIncidentList.append_column(_column)

        # Add the Incident List page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Incident\nList</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of incidents associated "
                                  u"with the selected Hardware assembly or "
                                  u"Hardware component."))

        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_testing_matrix_page(self, notebook):
        """
        Method to create the Hardware/Testing matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Build up the containers for the Hardware/Testing matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveHardTest, False, False)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.mtxTesting.treeview)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Testing\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system hardware and system "
                                  u"tests."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_validation_matrix_page(self, notebook):
        """
        Method to create the Hardware/Validation matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Hardware/Validation matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveHardVal, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.mtxValidation.treeview)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Add the Hardware/Validation Matrix page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Validation\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system functions and system "
                                  u"hardware items."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, hardware_id):
        """
        Method to load the Hardware List Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._load_parts_list_page(hardware_id)
        self._load_incident_list_page(hardware_id)

        _matrix_ids = self._dtc_matrices.dicMatrices.keys()

        for __, _matrix_id in enumerate(_matrix_ids):
            # Retrieve the next matrix in the list.
            _matrix = self._dtc_matrices.dicMatrices[_matrix_id]

            if _matrix.matrix_type == 6:
                self._load_testing_matrix_page(_matrix)
            elif _matrix.matrix_type == 7:
                self._load_validation_matrix_page(_matrix)

        return False

    def _load_parts_list_page(self, hardware_id):
        """
        Method to load the Parts List page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _parts = [[_hardware.ref_des, _hardware.name, _hardware.part_number]
                  for _hardware
                  in self._mdcRTK.dtcHardwareBoM.dicHardware.values()
                  if _hardware.parent_id == hardware_id and
                  _hardware.part == 1]
        _model = self.tvwPartsList.get_model()
        _model.clear()

        # Load the Parts List.
        for __, _part in enumerate(_parts):
            _model.append(None, _part)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwPartsList.get_column(0)
            self.tvwPartsList.row_activated(_path, _column)

        return False

    def _load_incident_list_page(self, hardware_id):
        """
        Method to load the Incident List page.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _incidents = [[_incident.incident_id, _incident.short_description,
                       Configuration.RTK_INCIDENT_STATUS[_incident.status]]
                      for _incident
                      in self._mdcRTK.dtcIncident.dicIncidents.values()
                      if _incident.hardware_id == hardware_id]
        _model = self.tvwIncidentList.get_model()
        _model.clear()

        # Load the Incident List.
        for __, _incident in enumerate(_incidents):
            _model.append(None, _incident)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwIncidentList.get_column(0)
            self.tvwIncidentList.row_activated(_path, _column)

        return False

    def _load_testing_matrix_page(self, matrix):
        """
        Method to load the Hardware/Testing matrix page.

        :param matrix: the :py:class:`rtk.datamodels.matrix.Matrix.Model` data
                       model to load into the Matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Get the list of all Hardware and the list of top-level Hardware.
        _hardware = matrix.dicRows.values()
        _top_items = [_h for _h in _hardware if _h[0] == 0]

        # Load the Hardware/Testing matrix data.
        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * \
                         (matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.mtxTesting.treeview.set_model(_model)

        # Create the columns for the Hardware/Testing matrix.  First, remove
        # any exsting columns in the Matrix.
        for _column in self.mtxTesting.treeview.get_columns():
            self.mtxTesting.treeview.remove_column(_column)

        _headings = [_(u"Hardware\nID"), _(u"Reference\nDesignator"),
                     _(u"Hardware\nName")] + matrix.lstColumnHeaders
        _editable = [False, False, False] + [True, True] * (matrix.n_col)

        for _index, _heading in enumerate(_headings):
            self.mtxTesting.add_column(_heading, _index,
                                       editable=_editable[_index])

        # Load the Hardware/Testing matrix.
        self.mtxTesting.load_matrix(_top_items, _hardware, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.mtxTesting.treeview.expand_all()
        self.mtxTesting.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.mtxTesting.treeview.get_column(0)
            self.mtxTesting.treeview.row_activated(_path, _column)

        return False

    def _load_validation_matrix_page(self, matrix):
        """
        Method to load the Hardware/Validation matrix page.

        :param matrix: the :py:class:`rtk.datamodels.matrix.Matrix.Model` data
                       model to load into the Matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Get the list of all Hardware and the list of top-level Hardware.
        _hardware = matrix.dicRows.values()
        _top_items = [_h for _h in _hardware if _h[0] == 0]

        # Load the Hardware/Validation matrix data.
        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * \
                         (matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.mtxValidation.treeview.set_model(_model)

        # Create the columns for the Hardware/Validation matrix.  First, remove
        # any exsting columns in the Matrix.
        for _column in self.mtxValidation.treeview.get_columns():
            self.mtxValidation.treeview.remove_column(_column)

        _headings = [_(u"Hardware\nID"), _(u"Reference\nDesignator"),
                     _(u"Hardware\nName")] + matrix.lstColumnHeaders
        _editable = [False, False, False] + [True, True] * (matrix.n_col)
        for _index, _heading in enumerate(_headings):
            self.mtxValidation.add_column(_heading, _index,
                                          editable=_editable[_index])

        # Load the Hardware/Validation matrix.
        self.mtxValidation.load_matrix(_top_items, _hardware, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.mtxValidation.treeview.expand_all()
        self.mtxValidation.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.mtxValidation.treeview.get_column(0)
            self.mtxValidation.treeview.row_activated(_path, _column)

        return False

    def _on_matrix_changed(self, matrix, treeview, new_value, col_position,
                           index):
        """
        Callback method to handle changes to a Matrix cell.

        :param Matrix: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that called
                       this method.
        :param gtk.TreeView treeview: the gtk.TreeView() imbedded in the
                                      Matrix.
        :param new_value: the new value of the cell in the Matrix.
        :param int col_position: the position in the Matrix of the column the
                                 calling gtk.CellRenderer() is in.
        :param int index: the index in the signal handler list associated with
                          the Matrix calling this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        matrix.handler_block(self._lst_handler_id[index])

        # Retrieve the Matrix object.
        _matrix = self._dtc_matrices.dicMatrices[index + 6]

        # Retrieve the Matrix gtk.TreeView() gtk.TreeModel() and selected
        # gtk.TreeIter() (i.e., the selected row).
        (_model, _row) = treeview.get_selection().get_selected()

        # Get the key in the Matrix row dictionary corresponding to the
        # selected row.  This is done by selecting the Hardware ID from the
        # Matrix and using this to find the associated key.
        _function_id = _model.get_value(_row, 0)
        _row_num = next((_key for _key, _value in _matrix.dicRows.iteritems()
                         if _value[1] == _function_id), None)

        # Calculate the position in the Matrix row dictionary whose value needs
        # to be changed and then set it equal to the new_value.  The position
        # in the Matrix row dictionary value list that needs to be changed
        # depends on the number of non-x-reference columns at the beginning of
        # the Matrix.  Given the following row in the Matrix:
        #
        #    [(898), ('F-T'), ('Test Hardware #1'), (<Pixbuf>, '0'),
        #     (<Pixbuf>, '1')]
        #
        # And the corresponding value list in the Matrix row dictionary:
        #
        #    [-1, 898, u'F-T', u'Test Hardware #1', u'0', u'1']
        #
        # If the <Pixbuf> at position 3 is changed, the corresponding value
        # list position is 4.  If the <Pixbuf> at position 5 is changed, the
        # corresponding value list position is 5.
        #
        # The general function for translating the changed <Pixbuf> to list
        # position is:
        #
        #    _position = 0.5 * (col_postion + n_fixed_col + 2)
        #
        # For the two examples above:
        #
        #    _position = 0.5 * (3 + 3 + 2) = 4
        #    _position = 0.5 * (5 + 3 + 2) = 4
        _position = int(0.5 * (col_position + matrix.n_fixed_columns + 2))
        _matrix.dicRows[_row_num][_position] = str(new_value)

        matrix.handler_unblock(self._lst_handler_id[index])

        return False

    def _on_button_clicked(self, button, index):
        """
        Callback method to respond to button clicks.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the signal handler list associated with
                          the Matrix calling this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        self._dtc_matrices.save_matrix(index + 4)

        button.handler_unblock(self._lst_handler_id[index])

        return False
