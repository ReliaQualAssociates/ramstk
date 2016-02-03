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
import Configuration as _conf
import gui.gtk.Widgets as _widg
from gui.gtk.Matrix import Matrix as rtkMatrix

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ListView(gtk.VBox):
    """
    The List Book view displays all the matrices and lists associated with the
    Function Class.  The attributes of a List Book view are:

    :ivar _listview:
    :ivar _modulebook:
    :ivar _dtc_matrices:
    :ivar _lst_matrix_icons: list of icons to use in the various Matrix views.
    :ivar gtk.TreeView tvwHardwareMatrix:
    :ivar gtk.TreeView tvwSoftwareMatrix:
    :ivar gtk.TreeView tvwTestMatrix:
    :ivar gtk.TreeView tvwPartsList:
    :ivar gtk.TreeView tvwIncidentsList:
    """

    def __init__(self, modulebook):
        """
        Initializes the Work Book view for the Revision package.

        :param modulebook: the :py:class:`rtk.function.ModuleBook` to associate
                           with this List Book.
        """

        gtk.VBox.__init__(self)

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

        # Parts List page widgets.
        self.tvwPartsList = gtk.TreeView()

        # Incidents List page widgets.
        self.tvwIncidentsList = gtk.TreeView()

        # Put it all together.
        # _toolbar = self._create_toolbar()
        # self.pack_start(_toolbar, expand=False)

        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_notebook(self):
        """
        Method to create the Revision class gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[1] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_hardware_matrix_page(_notebook)
        self._create_software_matrix_page(_notebook)
        self._create_testing_matrix_page(_notebook)
        self._create_parts_list_page(_notebook)
        self._create_incidents_list_page(_notebook)

        return _notebook

    def _create_hardware_matrix_page(self, notebook):
        """
        Method to create the Function/Hardware matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Build up the containers for the Function/Hardware matrix page.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwHardwareMatrix)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Hardware\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system functions and system "
                                  u"hardware items."))

        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_software_matrix_page(self, notebook):
        """
        Creates the function-software matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Create the Parts list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwSoftwareMatrix)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Software\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system functions and system "
                                  u"software items."))

        notebook.insert_page(_frame, tab_label=_label, position=-1)

        return False

    def _create_testing_matrix_page(self, notebook):
        """
        Creates the function-testing matrix page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Create the Parts list.
        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwTestMatrix)

        _frame = _widg.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _label = gtk.Label()
        _label.set_markup(_(u"<span weight='bold'>Testing\nMatrix</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the matrix showing relationships "
                                  u"between system functions and system "
                                  u"tests."))

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
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

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
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

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

        return False
