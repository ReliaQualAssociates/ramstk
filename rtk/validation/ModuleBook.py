#!/usr/bin/env python
"""
##############################
Validation Package Module View
##############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.validation.ModuleBook.py is part of The RTK Project
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
    import utilities as _util
    import widgets as _widg
except ImportError:
    import rtk.configuration as _conf
    import rtk.utilities as _util
    import rtk.widgets as _widg
#from ListBook import ListView
from WorkBook import WorkView

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ModuleView(object):
    """
    The Module Book view displays all the Validation items associated with the
    RTK Project in a flat list.  The attributes of a Module Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Validation attribute.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View :py:class:`gtk.TreeView`.
    :ivar _model: the :py:class:`rtk.validation.Validation.Model` data model
                  that is currently selected.
    :ivar _listbook: the :py:class:`rtk.validation.ListBook.ListView`
                     associated with this instance of the Module View.
    :ivar _workbook: the :py:class:`rtk.validation.WorkBook.WorkView`
                     associated with this instance of the Module View.
    :ivar dtcValidation: the :py:class:`rtk.validation.Validation` data
                         controller to use for accessing the Validation data
                         models.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the list of
                    Validation tasks.
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Validation package.

        :param controller: the instance of the
                           :py:class:`rtk.validation.Validation` data
                           controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Validation
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Validation view.  Pass -1 to add to the end.
        :param *args: other user arguments to pass to the Module View.
        """

        # Initialize private dict attributes.

        # Initialize private list attribute
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._workbook = None
        self._listbook = None
        self._model = None

        # Initialize public scalar attributes.
        self.dtcValidation = controller

        # Create the main Validation class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Validation', 4,
                                                    None, None,
                                                    _conf.RTK_COLORS[8],
                                                    _conf.RTK_COLORS[9])

        self.treeview.set_tooltip_text(_(u"Displays the list of verification "
                                         u"and validation tasks."))

        # Load the gtk.CellRendererCombo() holding the task types.
        _cell = self.treeview.get_column(
            self._lst_col_order[3]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        _model.append([""])
        for i in range(len(_conf.RTK_TASK_TYPE)):
            _model.append([_conf.RTK_TASK_TYPE[i]])

        # Load the gtk.CellRendererCombo() holding the measurement units.
        _cell = self.treeview.get_column(
            self._lst_col_order[3]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        _model.append([""])
        for i in range(len(_conf.RTK_MEASUREMENT_UNITS)):
            _model.append([_conf.RTK_MEASUREMENT_UNITS[i]])

        # Reset the limits of adjustment on the percent complete
        # gtk.CellRendererSpin() to 0 - 100 with steps of 1.
        _cell = self.treeview.get_column(
            self._lst_col_order[12]).get_cell_renderers()[0]
        _cell.set_property('digits', 0)
        _adjustment = _cell.get_property('adjustment')
        _adjustment.configure(0, 0, 100, 1, 0, 0)

        # Connect gtk.TreeView() editable cells to the callback function.
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

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_changed,
                                  None, None))
        self.treeview.connect('row_activated', self._on_row_changed)
        self.treeview.connect('button_press_event', self._on_button_press)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _icon = _conf.ICON_DIR + '32x32/validation.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Validation") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the development program "
                                  u"verification and validation tasks for the "
                                  u"selected revision."))

        _hbox = gtk.HBox()
        _hbox.pack_start(_image)
        _hbox.pack_end(_label)
        _hbox.show_all()

        rtk_view.notebook.insert_page(_scrollwindow, tab_label=_hbox,
                                      position=position)

        # Create a List View to associate with this Module View.
        #self._listbook = ListView(rtk_view.listview, self, self.dtcMatrices)

        # Create a Work View to associate with this Module View.
        self._workbook = WorkView(rtk_view.workview, self)

    def request_load_data(self, dao, revision_id):
        """
        Loads the Validation Module Book view gtk.TreeModel() with Validataion
        task information.

        :param dao: the :py:class: `rtk.dao.DAO` object used to communicate
                    with the RTK Project database.
        :param int revision_id: the ID of the revision to load validation data
                                for.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Retrieve all the development program tests.
        (_tasks, __) = self.dtcValidation.request_tasks(dao, revision_id)

        # Clear the Validation Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()
        for _task in _tasks:
            _data = [_task[0], _task[1], _task[2],
                     _conf.RTK_TASK_TYPE[_task[3] - 1], _task[4], _task[5],
                     _task[6], _task[7], _task[8], _task[9],
                     _util.ordinal_to_date(_task[10]),
                     _util.ordinal_to_date(_task[11]), _task[12], _task[13],
                     _task[14], _task[15], _task[16], _task[17], _task[18],
                     _task[19], _task[20], _task[21], _task[22], _task[23]]

            _model.append(None, _data)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        self.dtcValidation.request_status(revision_id)

        #self._listbook.load(revision_id)

        return False

    def update(self, position, new_text):
        """
        Updates the selected row in the Module Book gtk.TreeView() with changes
        to the Validation data model attributes.  Called by other views when
        the Validation data model attributes are edited via their
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
        Callback method for handling mouse clicks on the Validation package
        Module Book gtk.TreeView().

        :param gtk.TreeView treeview: the Validation class gtk.TreeView().
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
        Callback function to handle events for the Validation package Module
        Book gtk.TreeView().  It is called whenever a Module Book
        gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the Validation class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        _validation_id = _model.get_value(_row, 1)

        self._model = self.dtcValidation.dicTasks[_validation_id]

        self._workbook.load(self._model)

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, new_text, index):
        """
        Callback method to handle events for the Validation package Module Book
        gtk.CellRenderer().  It is called whenever a Module Book
        gtk.CellRenderer() is edited.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str __path: the path of the gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the gtk.CellRenderer() that was
                             edited.
        :param int index: the position in the Validation package Module Book
                          gtk.TreeView().
        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """

        if index == 2:
            self._model.task_description = new_text
        elif index == 3:
            self._model.task_type = _conf.RTK_TASK_TYPE.index(new_text) + 1
        elif index == 4:
            self._model.task_specification = new_text
        elif index == 5:
            self._model.measurement_unit = _conf.RTK_MEASUREMENT_UNITS.index(new_text) + 1
        elif index == 6:
            self._model.min_acceptable = float(new_text)
        elif index == 7:
            self._model.mean_acceptable = float(new_text)
        elif index == 8:
            self._model.max_acceptable = float(new_text)
        elif index == 9:
            self._model.variance_acceptable = float(new_text)
        elif index == 12:
            self._model.status = float(new_text)
        elif index == 13:
            self._model.minimum_time = float(new_text)
        elif index == 14:
            self._model.average_time = float(new_text)
        elif index == 15:
            self._model.maximum_time = float(new_text)
        elif index == 18:
            self._model.minimum_cost = float(new_text)
        elif index == 19:
            self._model.average_cost = float(new_text)
        elif index == 20:
            self._model.maximum_cost = float(new_text)
        elif index == 23:
            self._model.confidence = float(new_text)

        self._workbook.load(self._model)

        return False
