#!/usr/bin/env python
"""
###############################
Function Package List Book View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.function.ListBook.py is part of the RTK Project
#
# All rights reserved.

import sys

# Import modules for localization support.
import gettext
import locale

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
<<<<<<< HEAD
import Configuration as _conf
import gui.gtk.Widgets as _widg
from gui.gtk.Matrix import Matrix as rtkMatrix
=======
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
    from gui.gtk.Matrix import Matrix as rtkMatrix
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets
    from rtk.gui.gtk.Matrix import Matrix as rtkMatrix
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
<<<<<<< HEAD
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
=======
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ListView(gtk.VBox):
    """
    The List Book view displays all the matrices and lists associated with the
<<<<<<< HEAD
    Function Class.  The attributes of a List Book view are:

    :ivar _listview:
    :ivar _modulebook:
    :ivar _dtc_matrices:
    :ivar _lst_matrix_icons: list of icons to use in the various Matrix views.
    :ivar gtk.TreeView tvwHardwareMatrix:
    :ivar gtk.TreeView tvwSoftwareMatrix:
    :ivar gtk.TreeView tvwTestMatrix:
=======
    Function Class.  The attributes of a Function List Book view are:

    :ivar _dtc_matrices: the :py:class:`rtk.datamodels.Matrix.Matrix` data
                         controller instance.
    :ivar _lst_handler_id: list containing the signal handler ID's for each of
                           the gtk.Widget()s who have a callback method.
    :ivar gtk.Button btnSaveFuncHard: the gtk.Button() to save the Function/
                                      Hardware Matrix.
    :ivar gtk.Button btnSaveFuncSoft: the gtk.Button() to save the Function/
                                      Software Matrix.
    :ivar gtk.Button btnSaveFuncTest: the gtk.Button() to save the Function/
                                      Testing Matrix.
    :ivar mtxHardware: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that displays
                       the Function/Hardware Matrix.
    :ivar mtxSoftware: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that displays
                       the Function/Software Matrix.
    :ivar mtxTesting: the :py:class:`rtk.gui.gtk.Matrix.Matrix` that displays
                      the Function/Testing Matrix.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
    :ivar gtk.TreeView tvwPartsList:
    :ivar gtk.TreeView tvwIncidentsList:
    """

    def __init__(self, modulebook):
        """
<<<<<<< HEAD
        Initializes the Work Book view for the Revision package.
=======
        Initializes the List Book view for the Function package.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param modulebook: the :py:class:`rtk.function.ModuleBook` to associate
                           with this List Book.
        """

        gtk.VBox.__init__(self)

<<<<<<< HEAD
        # Initialize private list attributes.
        _icon = _conf.ICON_DIR + '32x32/none.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self._lst_matrix_icons = [_icon]
        _icon = _conf.ICON_DIR + '32x32/partial.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self._lst_matrix_icons.append(_icon)
        _icon = _conf.ICON_DIR + '32x32/complete.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        self._lst_matrix_icons.append(_icon)

        # Initialize private scalar attributes.
        self._dtc_matrices = modulebook.mdcRTK.dtcMatrices

        # Hardware Matrix page widgets.
        self.tvwHardwareMatrix = rtkMatrix()    #gtk.TreeView()

        # Software Matrix page widgets.
        self.tvwSoftwareMatrix = gtk.TreeView()

        # Testing Matrix page widgets.
        self.tvwTestMatrix = gtk.TreeView()
=======
        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._dtc_matrices = modulebook.mdcRTK.dtcMatrices

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        # Hardware Matrix page widgets.
        self.btnSaveFuncHard = Widgets.make_button(width=35, image='save')

        self.mtxHardware = rtkMatrix()
        self.mtxHardware.n_fixed_columns = 3

        # Software Matrix page widgets.
        self.btnSaveFuncSoft = Widgets.make_button(width=35, image='save')

        self.mtxSoftware = rtkMatrix()
        self.mtxSoftware.n_fixed_columns = 3

        # Testing Matrix page widgets.
        self.btnSaveFuncTest = Widgets.make_button(width=35, image='save')

        self.mtxTesting = rtkMatrix()
        self.mtxTesting.n_fixed_columns = 3
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        # Parts List page widgets.
        self.tvwPartsList = gtk.TreeView()

        # Incidents List page widgets.
        self.tvwIncidentsList = gtk.TreeView()

        # Put it all together.
<<<<<<< HEAD
        # _toolbar = self._create_toolbar()
        # self.pack_start(_toolbar, expand=False)

=======
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_notebook(self):
        """
<<<<<<< HEAD
        Method to create the Revision class gtk.Notebook().
=======
        Method to create the Function class List View gtk.Notebook().
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
<<<<<<< HEAD
        if _conf.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[1] == 'top':
=======
        if Configuration.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[1] == 'top':
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_hardware_matrix_page(_notebook)
        self._create_software_matrix_page(_notebook)
        self._create_testing_matrix_page(_notebook)
<<<<<<< HEAD
        self._create_parts_list_page(_notebook)
        self._create_incidents_list_page(_notebook)
=======

        # Connect widget signals to callback methods.  We do this here rather
        # than in each method so the _lst_handler_id index is the same as the
        # dicMatrix key for each Matrix.
        self._lst_handler_id.append(
            self.mtxHardware.connect('changed', self._on_matrix_changed, 0))
        self._lst_handler_id.append(
            self.mtxSoftware.connect('changed', self._on_matrix_changed, 1))
        self._lst_handler_id.append(
            self.mtxTesting.connect('changed', self._on_matrix_changed, 2))

        self._lst_handler_id.append(
            self.btnSaveFuncHard.connect('clicked',
                                         self._on_button_clicked, 3))
        self._lst_handler_id.append(
            self.btnSaveFuncSoft.connect('clicked',
                                         self._on_button_clicked, 4))
        self._lst_handler_id.append(
            self.btnSaveFuncTest.connect('clicked',
                                         self._on_button_clicked, 5))
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        return _notebook

    def _create_hardware_matrix_page(self, notebook):
        """
        Method to create the Function/Hardware matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Build up the containers for the Function/Hardware matrix page.
<<<<<<< HEAD
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwHardwareMatrix)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

=======
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveFuncHard, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.mtxHardware.treeview)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Set tooltips for the Function/Hardware Matrix.
        self.mtxHardware.treeview.set_tooltip_markup(_(u"Displays the "
                                                       u"relationship between "
                                                       u"system Functions and "
                                                       u"system Hardware.  "
                                                       u"This matrix shows "
                                                       u"which Hardware item "
                                                       u"partially (P) or "
                                                       u"completely (C) "
                                                       u"provides a Function, "
                                                       u"if at all."))

        # Add the Function/Hardware Matrix page to the gtk.Notebook().
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Hardware\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system functions and system "
                                  u"hardware items."))

<<<<<<< HEAD
        notebook.insert_page(_frame, tab_label=_label, position=-1)
=======
        notebook.insert_page(_hbox, tab_label=_label, position=-1)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        return False

    def _create_software_matrix_page(self, notebook):
        """
<<<<<<< HEAD
        Creates the function-software matrix page in the List View.
=======
        Creates the Function/Software matrix page in the List View.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

<<<<<<< HEAD
        # Create the Parts list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwSoftwareMatrix)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

=======
        # Build up the containers for the Function/Software matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveFuncSoft, False, False)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.mtxSoftware.treeview)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Set tooltips for the Function/Software Matrix.
        self.mtxSoftware.treeview.set_tooltip_markup(_(u"Displays the "
                                                       u"relationship between "
                                                       u"system Functions and "
                                                       u"system Software.  "
                                                       u"This matrix shows "
                                                       u"which Software item "
                                                       u"partially (P) or "
                                                       u"completely (C) "
                                                       u"provides a Function, "
                                                       u"if at all."))

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Software\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system functions and system "
                                  u"software items."))

<<<<<<< HEAD
        notebook.insert_page(_frame, tab_label=_label, position=-1)
=======
        notebook.insert_page(_hbox, tab_label=_label, position=-1)
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        return False

    def _create_testing_matrix_page(self, notebook):
        """
<<<<<<< HEAD
        Creates the function-testing matrix page in the List View.
=======
        Creates the Function/Testing matrix page in the List View.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

<<<<<<< HEAD
        # Create the Parts list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwTestMatrix)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

=======
        # Build up the containers for the Function/Testing matrix page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnSaveFuncTest, False, False)

        _hbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.mtxTesting.treeview)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Set tooltips for the Function/Testing Matrix.
        self.mtxTesting.treeview.set_tooltip_markup(_(u"Displays the "
                                                      u"relationship between "
                                                      u"system Functions and "
                                                      u"system development "
                                                      u"tests.  This matrix "
                                                      u"shows which tests "
                                                      u"partially (P) or "
                                                      u"completely (C) "
                                                      u"test a Function, if "
                                                      u"at all."))

>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Testing\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system functions and system "
                                  u"tests."))

<<<<<<< HEAD
        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_parts_list_page(self, notebook):
        """
        Creates the parts list page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Create the Parts list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwPartsList)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Parts\nList</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of hardware components "
                                  u"that comprise the selected Function."))

        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_incidents_list_page(self, notebook):
        """
        Creates the parts list page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Create the Parts list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwIncidentsList)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Incidents\nList</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the list of incidents that have "
                                  u"impacted the selected Function."))

        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def load(self, revision_id):
        """
        Loads the Function List Book.

        :param int revision_id: the Revision ID to load the List Book for.
=======
        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self):
        """
        Method to load the Function List Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _matrix_ids = self._dtc_matrices.dicMatrices.keys()

        for _index, _matrix_id in enumerate(_matrix_ids):
            # Retrieve the next matrix in the list.
            _matrix = self._dtc_matrices.dicMatrices[_matrix_id]

            if _matrix.matrix_type == 0:
                self._load_hardware_matrix_page(_matrix)
            elif _matrix.matrix_type == 1:
                self._load_software_matrix_page(_matrix)
            elif _matrix.matrix_type == 2:
                self._load_testing_matrix_page(_matrix)

        return False

    def _load_hardware_matrix_page(self, matrix):
        """
        Method to load the Function/Hardware matrix page.

        :param matrix: the :py:class:`rtk.datamodels.matrix.Matrix.Model` data
                       model to load into the Matrix.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Get the list of all Functions and the list of top-level Functions.
        _functions = matrix.dicRows.values()
        _top_items = [_f for _f in _functions if _f[0] == -1]

        # Load the Function/Hardware matrix data.
        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * \
                         (matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.mtxHardware.treeview.set_model(_model)

        # Create the columns for the Function/Hardware matrix.  First, remove
        # any exsting columns in the Matrix.
        for _column in self.mtxHardware.treeview.get_columns():
            self.mtxHardware.treeview.remove_column(_column)

        _headings = [_(u"Function\nID"), _(u"Function\nCode"),
                     _(u"Function\nName")] + matrix.lstColumnHeaders
        _editable = [False, False, False] + [True, True] * (matrix.n_col)

        for _index, _heading in enumerate(_headings):
            self.mtxHardware.add_column(_heading, _index,
                                        editable=_editable[_index])

        # Load the Function/Hardware matrix.
        self.mtxHardware.load_matrix(_top_items, _functions, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.mtxHardware.treeview.expand_all()
        self.mtxHardware.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.mtxHardware.treeview.get_column(0)
            self.mtxHardware.treeview.row_activated(_path, _column)

        return False

    def _load_software_matrix_page(self, matrix):
        """
        Method to load the Function/Software matrix page.

        :param matrix: the :py:class:`rtk.datamodels.matrix.Matrix.Model` data
                       model to load into the Matrix.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

<<<<<<< HEAD
        self._load_hardware_matrix_page(revision_id)
        #self._load_software_matrix_page(revision_id)
        #self._load_testing_matrix_page(revision_id)
        # TODO: Create these pages when the appropriate tables exist in the test database.
        # self._load_parts_list_page(revision_id)
        # self._load_incident_list_page(revision_id)

        return False

    def _load_hardware_matrix_page(self, revision_id):
        """
        Method to load the Function/Hardware matrix page.

        :param int revision_id: the Revision ID to load the Function/Hardware
                                matrix for.
=======
        # Get the list of all Functions and the list of top-level Functions.
        _functions = matrix.dicRows.values()
        _top_items = [_f for _f in _functions if _f[0] == -1]

        # Load the Function/Software matrix data.
        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * \
                         (matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.mtxSoftware.treeview.set_model(_model)

        # Create the columns for the Function/Software matrix.  First, remove
        # any exsting columns in the Matrix.
        for _column in self.mtxSoftware.treeview.get_columns():
            self.mtxSoftware.treeview.remove_column(_column)

        _headings = [_(u"Function\nID"), _(u"Function\nCode"),
                     _(u"Function\nName")] + matrix.lstColumnHeaders
        _editable = [False, False, False] + [True, True] * (matrix.n_col)
        for _index, _heading in enumerate(_headings):
            self.mtxSoftware.add_column(_heading, _index,
                                        editable=_editable[_index])

        # Load the Function/Software matrix.
        self.mtxSoftware.load_matrix(_top_items, _functions, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.mtxSoftware.treeview.expand_all()
        self.mtxSoftware.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.mtxSoftware.treeview.get_column(0)
            self.mtxSoftware.treeview.row_activated(_path, _column)

        return False

    def _load_testing_matrix_page(self, matrix):
        """
        Method to load the Function/Testing matrix page.

        :param matrix: the :py:class:`rtk.datamodels.matrix.Matrix.Model` data
                       model to load into the Matrix.
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

<<<<<<< HEAD
        _matrix = self._dtc_matrices.dicMatrices[0]

        # Get the list of all Functions and the list of top-level Functions.
        _functions = _matrix.dicRows.values()
        _top_items = [_f for _f in _functions if _f[0] == -1]

        # Load the Function/Hardware matrix data.
        _gobject_types = [gobject.TYPE_STRING, gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * (_matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.tvwHardwareMatrix.set_model(_model)

        # Create the columns for the Function/Hardware matrix.
        for _column in self.tvwHardwareMatrix.get_columns():
            self.tvwHardwareMatrix.remove_column(_column)

        _types = [-1, -1] + [1, 2] * (_matrix.n_col)
        _headings = [_(u"Function\nCode"), _(u"Function\nName")] + \
                    ["", self._lst_matrix_icons[0]] * (_matrix.n_col)
        _editable = [False, False] + [True] * (_matrix.n_col)
        for _index, _heading in enumerate(_headings):
            self.tvwHardwareMatrix.insert_column(_types[_index], _heading,
                                                 _index,
                                                 editable=_editable[_index])

        self.tvwHardwareMatrix.load_matrix(_top_items, _functions, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.tvwHardwareMatrix.expand_all()
        self.tvwHardwareMatrix.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwHardwareMatrix.get_column(0)
            self.tvwHardwareMatrix.row_activated(_path, _column)

        return False

    def _load_software_matrix_page(self, revision_id):
        """
        Loads the Software-Function matrix page.

        :param int revision_id: the Revision ID to load the Software-Function
                                matrix for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Update query when software table exists in database.
        _query = "SELECT fld_matrix_id, fld_row_id, fld_col_id, fld_value \
                  FROM rtk_matrices \
                  WHERE fld_revision_id={0:d} \
                  AND fld_matrix_type=1".format(revision_id)

        self._dtc_matrices.request_matrix(revision_id, _query, 1)
        #_rows = self._dtc_matrices.request_rows(revision_id, 1)
        _n_row = 0 #len(_rows)
        try:
            _n_col = len(_rows[0])
        except KeyError:
            _n_col = 0

        for i in range(_n_col):
            _column = gtk.TreeViewColumn("Column {0:d}".format(i))

            _cell = gtk.CellRendererPixbuf()
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.5)
            # _cell.connect('edited', edit_tree, int(position[i].text), model)

            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, pixbuf=i)

            _column.set_visible(1)
            self.tvwHardwareMatrix.append_column(_column)

        try:
            gobject_types = [gtk.gdk.Pixbuf] * (_n_col)
            _model = gtk.TreeStore(*gobject_types)
            self.tvwHardwareMatrix.set_model(_model)
            for i in range(_n_row):
                _data = []
                for j in range(_n_col):
                    _data.append(self._lst_matrix_icons[_rows[i][j]])
                _model.append(None, _data)
        except TypeError:
            pass

        return False

    def _load_testing_matrix_page(self, revision_id):
        """
        Loads the Testing-Function matrix page.

        :param int revision_id: the Revision ID to load the Testing-Function
                                matrix for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Update query when testing table exists in database.
        _query = "SELECT fld_matrix_id, fld_row_id, fld_col_id, fld_value \
                  FROM rtk_matrices \
                  WHERE fld_revision_id={0:d} \
                  AND fld_matrix_type=2".format(revision_id)

        self._dtc_matrices.request_matrix(revision_id, _query, 1)
        #_rows = self._dtc_matrices.request_rows(revision_id, 1)
        _n_row = 0 #len(_rows)
        try:
            _n_col = len(_rows[0])
        except KeyError:
            _n_col = 0

        for i in range(_n_col):
            _column = gtk.TreeViewColumn("Column {0:d}".format(i))

            _cell = gtk.CellRendererPixbuf()
            _cell.set_property('xalign', 0.5)
            _cell.set_property('yalign', 0.5)
            # _cell.connect('edited', edit_tree, int(position[i].text), model)

            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, pixbuf=i)

            _column.set_visible(1)
            self.tvwHardwareMatrix.append_column(_column)

        try:
            gobject_types = [gtk.gdk.Pixbuf] * (_n_col)
            _model = gtk.TreeStore(*gobject_types)
            self.tvwHardwareMatrix.set_model(_model)
            for i in range(_n_row):
                _data = []
                for j in range(_n_col):
                    _data.append(self._lst_matrix_icons[_rows[i][j]])
                _model.append(None, _data)
        except TypeError:
            pass
=======
        # Get the list of all Functions and the list of top-level Functions.
        _functions = matrix.dicRows.values()
        _top_items = [_f for _f in _functions if _f[0] == -1]

        # Load the Function/Testing matrix data.
        _gobject_types = [gobject.TYPE_INT, gobject.TYPE_STRING,
                          gobject.TYPE_STRING] + \
                         [gtk.gdk.Pixbuf, gobject.TYPE_STRING] * \
                         (matrix.n_col)
        _model = gtk.TreeStore(*_gobject_types)
        self.mtxTesting.treeview.set_model(_model)

        # Create the columns for the Function/Testing matrix.  First, remove
        # any exsting columns in the Matrix.
        for _column in self.mtxTesting.treeview.get_columns():
            self.mtxTesting.treeview.remove_column(_column)

        _headings = [_(u"Function\nID"), _(u"Function\nCode"),
                     _(u"Function\nName")] + matrix.lstColumnHeaders
        _editable = [False, False, False] + [True, True] * (matrix.n_col)
        for _index, _heading in enumerate(_headings):
            self.mtxTesting.add_column(_heading, _index,
                                       editable=_editable[_index])

        # Load the Function/Testing matrix.
        self.mtxTesting.load_matrix(_top_items, _functions, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.mtxTesting.treeview.expand_all()
        self.mtxTesting.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.mtxTesting.treeview.get_column(0)
            self.mtxTesting.treeview.row_activated(_path, _column)

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
        _matrix = self._dtc_matrices.dicMatrices[index]

        # Retrieve the Matrix gtk.TreeView() gtk.TreeModel() and selected
        # gtk.TreeIter() (i.e., the selected row).
        (_model, _row) = treeview.get_selection().get_selected()

        # Get the key in the Matrix row dictionary corresponding to the
        # selected row.  This is done by selecting the Function ID from the
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
        #    [(898), ('F-T'), ('Test Function #1'), (<Pixbuf>, '0'),
        #     (<Pixbuf>, '1')]
        #
        # And the corresponding value list in the Matrix row dictionary:
        #
        #    [-1, 898, u'F-T', u'Test Function #1', u'0', u'1']
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
        :param int index:
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        self._dtc_matrices.save_matrix(index - 3)

        button.handler_unblock(self._lst_handler_id[index])
>>>>>>> 98978f0b719800855ef5f1cfd5ce703a5e45632e

        return False
