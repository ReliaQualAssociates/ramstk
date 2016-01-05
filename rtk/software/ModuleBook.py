#!/usr/bin/env python
"""
############################
Software Package Module View
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.software.ModuleBook.py is part of The RTK Project
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

# Import other RTK modules.
try:
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg
#from ListBook import ListView
from WorkBook import WorkView

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ModuleView(object):
    """
    The Module Book view displays all the Software items associated with the
    RTK Project in a hierarchical list.  The attributes of a Module Book view
    are:

    :ivar _model: the :py:class:`rtk.software.Software.Model` data model that
                  is currently selected.

    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View :py:class:`gtk.TreeView`.
    :ivar _workbook: the :py:class:`rtk.software.WorkBook.WorkView` associated
                     with this instance of the Module View.
    :ivar dtcBoM: the :py:class:`rtk.software.BoM` data controller to use for
                  accessing the Software data models.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the hierarchical
                    list of Software.
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Software package.

        :param controller: the instance of the :py:class:`rtk.bom.BoM` data
                           controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Software
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Software view.  Pass -1 to add to the end.
        :param *args: other user arguments to pass to the Module View.
        """

        # Initialize private list attribute
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._model = None

        # Initialize public scalar attributes.
        self.dtcBoM = controller

        # Create the main Software class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Software', 15,
                                                    _conf.RTK_COLORS[21],
                                                    _conf.RTK_COLORS[22])
        _selection = self.treeview.get_selection()

        self.treeview.set_tooltip_text(_(u"Displays the hierarchical list of "
                                         u"the system software."))

        self._lst_handler_id.append(_selection.connect('changed',
                                                       self._on_row_changed))
        #self.treeview.connect('cursor_changed', self._on_row_changed,
        #                      None, None))
        #self._lst_handler_id.append(
        #    self.treeview.connect('row_activated', self._on_row_changed))
        self._lst_handler_id.append(
            self.treeview.connect('button_release_event',
                                  self._on_button_press))

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

        _icon = _conf.ICON_DIR + '32x32/software.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Software") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the system software structure "
                                  u"for the selected revision."))

        _hbox = gtk.HBox()
        _hbox.pack_start(_image)
        _hbox.pack_end(_label)
        _hbox.show_all()

        rtk_view.notebook.insert_page(_scrollwindow, tab_label=_hbox,
                                      position=position)

        # Create a List View to associate with this Module View.
        self.listbook = None
        #self.listbook = ListView(rtk_view.listview, self, self.dtcMatrices)

        # Create a Work View to associate with this Module View.
        self.workbook = WorkView(rtk_view.workview, self)

    def request_load_data(self, dao, revision_id):
        """
        Loads the Software Module Book view gtk.TreeModel() with software
        information.

        :param dao: the :py:class: `rtk.dao.DAO` object used to communicate
                    with the RTK Project database.
        :param int revision_id: the ID of the revision to load software data
                                for.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_software, __) = self.dtcBoM.request_bom(dao, revision_id)

        # Only load the software associated with the selected Revision.
        _software = [_s for _s in _software if _s[0] == revision_id]
        _top_items = [_s for _s in _software if _s[1] == 0]

        # Clear the Software Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()

        # Recusively load the Software Module View gtk.TreeModel().
        self._load_treeview(dao, _top_items, _software, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        #self.listbook.load(revision_id)

        return False

    def _load_treeview(self, dao, parents, software, model, row=None):
        """
        Method to recursively load the gtk.TreeModel().  Recursive loading is
        needed to accomodate the hierarchical structure of Software.

        :param rtk.DAO dao: the Data Access Object to pass to the Software data
                            controller.
        :param list parents: the list of top-level software modules to load.
        :param list software: the complete list of software to use for finding
                              the child software for each parent.
        :param gtk.TreeModel model: the Software Module View gtk.TreeModel().
        :keyword gtk.TreeIter row: the parent gtk.TreeIter().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
# TODO: Is passing the dao object around the best way or is it better as a private instance attribute?
        _icon = _conf.ICON_DIR + '32x32/csci.png'
        _csci_icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _icon = _conf.ICON_DIR + '32x32/unit.png'
        _unit_icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)

        for _software in parents:
            if _software[2] == 1:
                row = None
                _data = list(_software) + [_csci_icon]
            if _software[2] == 2:
                _data = list(_software) + [_csci_icon]
            elif _software[2] == 3:
                _data = list(_software) + [_unit_icon]
            _piter = model.append(row, _data)
            _parent_id = _software[1]

            # Find the child software modules of the current parent software
            # module.  These will be the new parent software modules to pass to
            # this method.
            _parents = [_s for _s in software if _s[34] == _parent_id]
            self._load_treeview(dao, _parents, software, model, _piter)

        return False

    def update(self, position, new_text):
        """
        Updates the selected row in the Module Book gtk.TreeView() with changes
        to the Software data model attributes.  Called by other views when the
        Software data model attributes are edited via their gtk.Widgets().

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
        Callback method for handling mouse clicks on the Software package
        Module Book gtk.TreeView().

        :param gtk.TreeView treeview: the Software class gtk.TreeView().
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
            _selection = treeview.get_selection()
            self._on_row_changed(_selection)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _on_row_changed(self, selection):
        """
        Callback method to handle events for the Software package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeSelection selection: the Software class gtk.TreeView()'s
                                            gtk.TreeSelection().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        selection.handler_block(self._lst_handler_id[0])

        (_model, _row) = selection.get_selected()
        _software_id = _model.get_value(_row, 1)

        self._model = self.dtcBoM.dicSoftware[_software_id]

        self.workbook.load(self._model)

        selection.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, new_text, index):
        """
        Callback method to handle events for the Software package Module Book
        gtk.CellRenderer().  It is called whenever a Module Book
        gtk.CellRenderer() is edited.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str __path: the path of the gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the gtk.CellRenderer() that was
                             edited.
        :param int index: the position in the Software pacakge Module Book
                          gtk.TreeView().
        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """

        if index == 3:
            self._model.description = new_text

        self.workbook.load(self._model)

        return False
