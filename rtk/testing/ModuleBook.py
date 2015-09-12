#!/usr/bin/env python
"""
###########################
Testing Package Module View
###########################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.testing.ModuleBook.py is part of The RTK Project
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

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import configuration as _conf
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.widgets as _widg
#from ListBook import ListView
from WorkBook import WorkView

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

# TODO: Fix all docstrings; copy-paste errors.
class ModuleView(object):
    """
    The Module Book view displays all the Testing items associated with the
    RTK Project in a hierarchical list.  The attributes of a Module Book view
    are:

    :ivar _model: the :py:class:`rtk.testing.Testing.Model` data model that
                  is currently selected.

    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View :py:class:`gtk.TreeView`.
    :ivar _workbook: the :py:class:`rtk.testing.WorkBook.WorkView` associated
                     with this instance of the Module View.
    :ivar dtcTesting: the :py:class:`rtk.testing.BoM` data controller to use for
                  accessing the Testing data models.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the hierarchical
                    list of Testing.
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Testing package.

        :param controller: the instance of the :py:class:`rtk.testing.Testing`
                           data controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Testing
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Testing view.  Pass -1 to add to the end.
        :param *args: other user arguments to pass to the Module View.
        """

        # Initialize private list attribute
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._model = None

        # Initialize public scalar attributes.
        self.dtcTesting = controller
        self.dtcGrowth = args[0][0]

        # Create the main Testing class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Testing', 11,
                                                    None, None,
                                                    _conf.RTK_COLORS[10],
                                                    _conf.RTK_COLORS[11])
        _selection = self.treeview.get_selection()

        self.treeview.set_tooltip_text(_(u"Displays the list of development "
                                         u"program tests."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_changed,
                                  None, None))
        #self.treeview.connect('row_activated', self._on_row_changed)
        #self.treeview.connect('button_press_event', self._on_button_press)

        i = 0
        for _column in self.treeview.get_columns():
            _cell = _column.get_cell_renderers()[0]
            try:
                if _cell.get_property('editable'):
                    _cell.connect('edited', self._on_cell_edited,
                                  self._lst_col_order[i])
            except TypeError:
                pass
            i += 1

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Testing") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the development program tests "
                                  u"for the selected revision."))

        rtk_view.notebook.insert_page(_scrollwindow, tab_label=_label,
                                      position=position)

        # Create a List View to associate with this Module View.
        self._listbook = None
        #self._listbook = ListView(rtk_view.listview, self, self.dtcMatrices)

        # Create a Work View to associate with this Module View.
        self._workbook = WorkView(rtk_view.workview, self)

    def request_load_data(self, dao, revision_id):
        """
        Loads the Testing Module Book view gtk.TreeModel() with testing
        information.

        :param dao: the :py:class: `rtk.dao.DAO` object used to communicate
                    with the RTK Project database.
        :param int revision_id: the ID of the revision to load testing data
                                for.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Retrieve all the development program tests.
        (_tests, __) = self.dtcTesting.request_tests(dao, revision_id)

        # Clear the Testing Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()
        for _test in _tests:
            if _test[5] == 0:
                _icon = _conf.ICON_DIR + '32x32/testing.png'
            elif _test[5] == 1:
                _icon = _conf.ICON_DIR + '32x32/halthass.png'
            elif _test[5] == 2:
                _icon = _conf.ICON_DIR + '32x32/accelerated.png'
            elif _test[5] == 3:
                _icon = _conf.ICON_DIR + '32x32/ess.png'
            elif _test[5] == 4:
                _icon = _conf.ICON_DIR + '32x32/growth.png'
                self.dtcGrowth.request_tests(dao, _test)
            elif _test[5] == 5:
                _icon = _conf.ICON_DIR + '32x32/demonstration.png'
            elif _test[5] == 6:
                _icon = _conf.ICON_DIR + '32x32/prat.png'

            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = list(_test) + [_icon]

            _model.append(None, _data)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        #self._listbook.load(revision_id)

        return False

    def update(self, position, new_text):
        """
        Updates the selected row in the Module Book gtk.TreeView() with changes
        to the Testing data model attributes.  Called by other views when the
        Testing data model attributes are edited via their gtk.Widgets().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.treeview.get_selection().get_selected()
        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_button_press(self, treeview, event):
        """
        Callback method for handling mouse clicks on the Testing package
        Module Book gtk.TreeView().

        :param gtk.TreeView treeview: the Testing class gtk.TreeView().
        :param gtk.gdk.Event event: the gtk.gdk.Event() that called this method
                                    (the important attribute is which mouse
                                    button was clicked).
                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if event.button == 1:
            self._on_row_changed(treeview, None, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _on_row_changed(self, treeview, __path, __column):
        """
        Callback function to handle events for the Testing package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Testing class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        _test_id = _model.get_value(_row, 2)
        _test_type = _model.get_value(_row, 5)

        if _test_type == 4:                 # Reliability growth
            self._model = self.dtcGrowth.dicTests[_test_id]
        else:
            self._model = self.dtcTesting.dicTests[_test_id]

        self._workbook.load(self._model)

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, __new_text, __index):
        """
        Callback method to handle events for the Testing package Module Book
        gtk.CellRenderer().  It is called whenever a Module Book
        gtk.CellRenderer() is edited.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str __path: the path of the gtk.CellRenderer() that was edited.
        :param str __new_text: the new text in the gtk.CellRenderer() that was
                               edited.
        :param int __index: the position in the Testing pacakge Module Book
                            gtk.TreeView().
        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """
        # TODO: Use this function or delete it.
        self._workbook.load(self._model)

        return False
