#!/usr/bin/env python
"""
############################
Function Package Module View
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.function.ModuleBook.py is part of The RTK Project
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
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ModuleView(object):
    """
    The Module Book view ro display all the Functions associated with the
    selected Revision in the RTK Project in a hierarchical list.  The
    attributes of a Function Module Book view are:

    :ivar _model: the :py:class:`rtk.function.Function.Model` data model that
                  is currently selected.
    :ivar _fmea_model: the :py:class:`rtk.fmea.FMEA.Model` data model that is
                       currently selected.
    :ivar list _lst_col_order: list containing the order of the columns in the
                          Module View :class:`gtk.TreeView`.
    :ivar _workbook: the :py:class:`rtk.function.WorkBook.WorkView` associated
                     with this instance of the Module View.
    :ivar dtcFunction: the :py:class:`rtk.function.Function.Function` data
                       controller to use for accessing the Function data
                       models.
    :ivar dtcFMEA: the :py:class:`rtk.fmea.FMEA.FMEA` data controller to use
                   for accessing the FMEA data models.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the list of
                    Functions.
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Function package.

        :param rtk.function.Function controller: the instance of the Function
                                                 data controller to use with
                                                 this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Function
                                      view into.
        :param int position: the page position in the gtk.Notebook() to
                             insert the Function view.  Pass -1 to add to the
                             end.
        :param *args: other user arguments to pass to the Module View.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._dtc_function = controller.dtcFunction
        self._dtc_fmea = controller.dtcFMEA
        self._dtc_profile = controller.dtcProfile
        self._model = None
        self._fmea_model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.mdcRTK = controller

        (self.treeview,
         self._lst_col_order) = Widgets.make_treeview('Function', 1,
                                                      Configuration.RTK_COLORS[2],
                                                      Configuration.RTK_COLORS[3])

        self.treeview.set_tooltip_text(_(u"Displays the hierarchical list of "
                                         u"functions."))
        self.treeview.connect('cursor_changed', self._on_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._on_row_changed)
        self.treeview.connect('button_press_event', self._on_button_press)

        # Connect the cells to the callback function.
        for i in [4, 14, 15]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._on_cell_edited, i,
                             self.treeview.get_model())

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _icon = Configuration.ICON_DIR + '32x32/function.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Functions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the functions for the selected "
                                  u"revision."))

        _hbox = gtk.HBox()
        _hbox.pack_start(_image)
        _hbox.pack_end(_label)
        _hbox.show_all()

        rtk_view.notebook.insert_page(_scrollwindow, tab_label=_hbox,
                                      position=position)

        # Create a List View to associate with this Module View.
        self.listbook = ListView(self)

        # Create a Work View to associate with this Module View.
        self.workbook = WorkView(self)

    def request_load_data(self, dao, revision_id):
        """
        Loads the Function Module Book view gtk.TreeModel() with function
        information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
# TODO: Remove dao parameter after converting all modules.
        (_functions,
         __) = self._dtc_function.request_functions(self.mdcRTK.project_dao,
                                                    revision_id)

        # Find the list of top level Functions.
        _top_funcs = [_f for _f in _functions if _f[19] == -1]

        # Clear the Function Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()

        # Recusively load the Function Module View gtk.TreeModel().
        self._load_treeview(_top_funcs, _functions, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        self.listbook.load()

        return False

    def _load_treeview(self, parents, functions, model, row=None):
        """
        Method to recursively load the gtk.TreeModel().  Recursive loading is
        needed to accomodate the hierarchical structure of Functions.

        :param list parents: the list of top-level functions to load.
        :param list functions: the complete list of functions to use for
                               finding the child functions for each parent.
        :param gtk.TreeModel model: the Function Module View gtk.TreeModel().
        :keyword gtk.TreeIter row:
        """

        for _function in parents:
            if _function[19] == -1:
                row = None
            _piter = model.append(row, _function)
            _parent_id = _function[1]

            self._dtc_fmea.request_fmea(self.mdcRTK.project_dao, None,
                                        _function[0])

            # Find the child functions of the current parent function.  These
            # will be the new parent functions to pass to this method.
            _parents = [_f for _f in functions if _f[19] == _parent_id]
            self._load_treeview(_parents, functions, model, _piter)

        return False

    def update(self, position, new_text):
        """
        Method to update the Module Book gtk.TreeView() with changes to the
        Function data model attributes.  Called by other views when the
        Function data model attributes are edited via their gtk.Widgets().

        :ivar int position: the ordinal position in the Module Book
                            gtk.TreeView() of the data being updated.
        :ivar next_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        _model.set(_row, self._lst_col_order[position], new_text)

        return False

    def _on_button_press(self, treeview, event):
        """
        Method for handling mouse clicks on the Function package Module Book
        gtk.TreeView().

        :param gtk.TreeView treeview: the Function class gtk.TreeView().
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
# TODO: Write a pop-up menu for the Function Module Book gtk.TreeView()
            pass

        return False

    def _on_row_changed(self, treeview, __path, __column):
        """
        Callback function to handle events for the Function package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Function class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = treeview.get_selection().get_selected()

        _function_id = _model.get_value(_row, 1)
        self._model = self._dtc_function.dicFunctions[_function_id]

        try:
            self._fmea_model = self._dtc_fmea.dicFFMEA[_function_id]
        except KeyError:
            self._dtc_fmea.add_fmea(None, _function_id)
            self._fmea_model = self._dtc_fmea.dicFFMEA[_function_id]

        _profile_model = self._dtc_profile.dicProfiles[self._model.revision_id]
        self.workbook.load(self._model, self._fmea_model, _profile_model)

        return False

    def _on_cell_edited(self, __cell, path, new_text, position, model):
        """
        Callback function to handle edits of the Function package Module Book
        gtk.Treeview().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        # Now update the Function data model.
        if self._lst_col_order[position] == 4:
            self._model.code = str(new_text)
        elif self._lst_col_order[position] == 14:
            self._model.name = str(new_text)
        elif self._lst_col_order[position] == 15:
            self._model.remarks = str(new_text)

        self.workbook.update()

        return False
