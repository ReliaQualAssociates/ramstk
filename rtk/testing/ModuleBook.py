#!/usr/bin/env python
"""
###########################
Testing Package Module View
###########################
"""

# -*- coding: utf-8 -*-
#
#       rtk.testing.ModuleBook.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors 
#    may be used to endorse or promote products derived from this software 
#    without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER 
#    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR 
#    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
#    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

# Import other RTK modules.
try:
    import Configuration
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.gui.gtk.Widgets as Widgets
from ListBook import ListView
from WorkBook import WorkView

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ModuleView(object):
    """
    The Module Book view displays all the Testing items associated with the
    RTK Project in a hierarchical list.  The attributes of a Module Book view
    are:

    :ivar _model: the :py:class:`rtk.testing.Testing.Model` data model that
                  is currently selected.

    :ivar list _lst_col_order: list containing the order of the columns in the
                               Module View gtk.TreeView.
    :ivar _workbook: the :py:class:`rtk.testing.WorkBook.WorkView` associated
                     with this instance of the Module View.
    :ivar dtcTesting: the :py:class:`rtk.testing.Testing.Testing` data
                      controller to use for accessing the Testing data models.
    :ivar treeview: the gtk.TreeView displaying the list of Tests.
    """

    def __init__(self, controller, rtk_view, position):
        """
        Method to initialize the Module Book view for the Testing package.

        :param controller: the instance of the :py:class:`rtk.RTK.RTK` master
                           data controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Testing
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Testing view.  Pass -1 to add to the end.
        """

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.mdcRTK = controller

        # Create the main Testing class treeview.
        _bg_color = Configuration.RTK_COLORS[10]
        _fg_color = Configuration.RTK_COLORS[11]
        (self.treeview,
         self._lst_col_order) = Widgets.make_treeview('Testing', 8,
                                                      _bg_color, _fg_color)

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

        _icon = Configuration.ICON_DIR + '32x32/testing.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Testing") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the development program tests "
                                  u"for the selected revision."))

        _hbox = gtk.HBox()
        _hbox.pack_start(_image)
        _hbox.pack_end(_label)
        _hbox.show_all()

        rtk_view.notebook.insert_page(_scrollwindow, tab_label=_hbox,
                                      position=position)

        self.treeview.set_tooltip_text(_(u"Displays the list of development "
                                         u"program tests."))

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_changed,
                                  None, None))
        self.treeview.connect('row_activated', self._on_row_changed)
        # self.treeview.connect('button_press_event', self._on_button_press)

        # Create a List View to associate with this Module View.
        self.listbook = ListView(self)

        # Create a Work View to associate with this Module View.
        self.workbook = WorkView(self)

    def request_load_data(self):
        """
        Method to load the Testing Module Book view gtk.TreeModel() with
        testing information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
# TODO: Consider re-writing request_load_data; current McCabe Complexity metric = 10.
        # Retrieve all the development program tests.
        (_tests,
         __) = self.mdcRTK.dtcTesting.request_tests(self.mdcRTK.project_dao,
                                                    self.mdcRTK.revision_id)

        # Clear the Testing Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()
        for _test in _tests:
            if _test[5] == 0:
                _icon = Configuration.ICON_DIR + '32x32/testing.png'
            elif _test[5] == 1:
                _icon = Configuration.ICON_DIR + '32x32/halthass.png'
            elif _test[5] == 2:
                _icon = Configuration.ICON_DIR + '32x32/accelerated.png'
            elif _test[5] == 3:
                _icon = Configuration.ICON_DIR + '32x32/ess.png'
            elif _test[5] == 4:
                _icon = Configuration.ICON_DIR + '32x32/growth.png'
                self.mdcRTK.dtcGrowth.request_tests(self.mdcRTK.project_dao,
                                                    _test)
            elif _test[5] == 5:
                _icon = Configuration.ICON_DIR + '32x32/demonstration.png'
            elif _test[5] == 6:
                _icon = Configuration.ICON_DIR + '32x32/prat.png'

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

        return False

    def update(self, position, new_text):
        """
        Method to update the selected row in the Module Book gtk.TreeView()
        with changes to the Testing data model attributes.  Called by other
        views when the Testing data model attributes are edited via their
        gtk.Widgets().

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
        Method to handle mouse clicks on the Testing package Module Book
        gtk.TreeView().

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
        Method to handle events for the Testing package Module Book
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
            self._model = self.mdcRTK.dtcGrowth.dicTests[_test_id]
        else:
            self._model = self.mdcRTK.dtcTesting.dicTests[_test_id]

        self.workbook.load(self._model)
        self.listbook.load(self._model)

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, __new_text, __index):
        """
        Method to handle events for the Testing package Module Book
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
        self.workbook.load(self._model)

        return False
