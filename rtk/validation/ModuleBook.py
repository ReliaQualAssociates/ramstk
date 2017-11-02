#!/usr/bin/env python
"""
##############################
Validation Package Module View
##############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.validation.ModuleBook.py is part of The RTK Project
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
    import Utilities
    import gui.gtk.Widgets as Widgets
except ImportError:
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities
    import rtk.gui.gtk.Widgets as Widgets
# from ListBook import ListView
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
    The Module Book view displays all the Validation items associated with the
    RTK Project in a flat list.  The attributes of a Module Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Validation attribute.
    :ivar list _lst_col_order: list containing the order of the columns in the
                               Module View :py:class:`gtk.TreeView`.
    :ivar _model: the :py:class:`rtk.validation.Validation.Model` data model
                  that is currently selected.
    :ivar _listbook: the :py:class:`rtk.validation.ListBook.ListView`
                     associated with this instance of the Module View.
    :ivar _workbook: the :py:class:`rtk.validation.WorkBook.WorkView`
                     associated with this instance of the Module View.
    :ivar mdcRTK: the :py:class:`rtk.RTK.RTK` master data controller to use.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the list of
                    Validation tasks.
    """

    def __init__(self, controller, rtk_view, position):
        """
        Method to initialize the Module Book view for the Validation package.

        :param controller: the instance of the :py:class:`rtk.RTK.RTK` master
                           data controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Validation
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Validation view.  Pass -1 to add to the end.
        """

        # Define private dictionary attributes.

        # Define private list attribute
        self._lst_handler_id = []

        # Define private scalar attributes.
        self.workbook = None
        self.listbook = None
        self._model = None

        # Define public dictionary attributes.

        # Define public list attribute

        # Define public scalar attributes.
        self.mdcRTK = controller

        # Create the main Validation class treeview.
        _fg_color = Configuration.RTK_COLORS[8]
        _bg_color = Configuration.RTK_COLORS[9]
        (self.treeview,
         self._lst_col_order) = Widgets.make_treeview('Validation', 4,
                                                      _fg_color, _bg_color)

        # Load the gtk.CellRendererCombo() holding the task types.
        _cell = self.treeview.get_column(
            self._lst_col_order[3]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        _model.append([""])
        for i in range(len(Configuration.RTK_TASK_TYPE)):
            _model.append([Configuration.RTK_TASK_TYPE[i]])

        # Load the gtk.CellRendererCombo() holding the measurement units.
        _cell = self.treeview.get_column(
            self._lst_col_order[3]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        _model.append([""])

        for i in range(len(Configuration.RTK_MEASUREMENT_UNITS)):
            _model.append([Configuration.RTK_MEASUREMENT_UNITS[i]])

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

        # Set gtk.Widget() tooltips.
        self.treeview.set_tooltip_text(_(u"Displays the list of verification "
                                         u"and validation tasks."))

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_changed,
                                  None, None))
        self.treeview.connect('row_activated', self._on_row_changed)
        self.treeview.connect('button_press_event', self._on_button_press)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _icon = Configuration.ICON_DIR + '32x32/validation.png'
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
        # self.listbook = ListView(self)

        # Create a Work View to associate with this Module View.
        self.workbook = WorkView(self)

    def request_load_data(self):
        """
        Method to load the Validation Module Book view gtk.TreeModel() with
        Validation task information.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve all the development program Validation tasks.
        (_tasks,
         __) = self.mdcRTK.dtcValidation.request_tasks(self.mdcRTK.project_dao,
                                                       self.mdcRTK.revision_id)

        # Clear the Validation Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()
        for _task in _tasks:
            _data = [_task[0], _task[1], _task[2],
                     Configuration.RTK_TASK_TYPE[_task[3] - 1], _task[4],
                     _task[5], _task[6], _task[7], _task[8], _task[9],
                     Utilities.ordinal_to_date(_task[10]),
                     Utilities.ordinal_to_date(_task[11]), _task[12],
                     _task[13], _task[14], _task[15], _task[16], _task[17],
                     _task[18], _task[19], _task[20], _task[21], _task[22],
                     _task[23]]

            _model.append(None, _data)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        self.mdcRTK.dtcValidation.request_status(self.mdcRTK.revision_id)

        return False

    def update(self, position, new_text):
        """
        Method to update the selected row in the Module Book gtk.TreeView()
        with changes to the Validation data model attributes.  Called by other
        views when the Validation data model attributes are edited via their
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
        Method to handle mouse clicks on the Validation package Module Book
        gtk.TreeView().

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
        Method to handle events for the Validation package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Validation class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        _validation_id = _model.get_value(_row, 1)

        self._model = self.mdcRTK.dtcValidation.dicTasks[_validation_id]

        self.workbook.load(self._model)
        # self.listbook.load(revision_id)

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, new_text, index):
        """
        Method to handle events for the Validation package Module Book
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
# WARNING: Refactor _on_cell_edited; current McCabe Complexity metric = 17.
        if self._lst_col_order[index] == 2:
            self._model.task_description = new_text
        elif self._lst_col_order[index] == 3:
            _task_type = Configuration.RTK_TASK_TYPE.index(new_text) + 1
            self._model.task_type = _task_type
        elif self._lst_col_order[index] == 4:
            self._model.task_specification = new_text
        elif self._lst_col_order[index] == 5:
            _unit = Configuration.RTK_MEASUREMENT_UNITS.index(new_text) + 1
            self._model.measurement_unit = _unit
        elif self._lst_col_order[index] == 6:
            self._model.min_acceptable = float(new_text)
        elif self._lst_col_order[index] == 7:
            self._model.mean_acceptable = float(new_text)
        elif self._lst_col_order[index] == 8:
            self._model.max_acceptable = float(new_text)
        elif self._lst_col_order[index] == 9:
            self._model.variance_acceptable = float(new_text)
        elif self._lst_col_order[index] == 12:
            self._model.status = float(new_text)
        elif self._lst_col_order[index] == 13:
            self._model.minimum_time = float(new_text)
        elif self._lst_col_order[index] == 14:
            self._model.average_time = float(new_text)
        elif self._lst_col_order[index] == 15:
            self._model.maximum_time = float(new_text)
        elif self._lst_col_order[index] == 18:
            self._model.minimum_cost = float(new_text)
        elif self._lst_col_order[index] == 19:
            self._model.average_cost = float(new_text)
        elif self._lst_col_order[index] == 20:
            self._model.maximum_cost = float(new_text)
        elif self._lst_col_order[index] == 23:
            self._model.confidence = float(new_text)

        self.workbook.load(self._model)

        return False
