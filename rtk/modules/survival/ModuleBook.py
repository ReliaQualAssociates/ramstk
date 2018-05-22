#!/usr/bin/env python
"""
############################
Survival Package Module View
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.survival.ModuleBook.py is part of The RTK Project
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
    The Module Book view displays all the Survival items associated with the
    RTK Project in a flat list.  The attributes of a Module Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Survival attribute.
    :ivar list _lst_col_order: list containing the order of the columns in the
                               Module View :py:class:`gtk.TreeView`.
    :ivar _model: the :py:class:`rtk.survival.Survival.Model` data model
                  that is currently selected.
    :ivar _listbook: the :py:class:`rtk.survival.ListBook.ListView`
                     associated with this instance of the Module View.
    :ivar _workbook: the :py:class:`rtk.survival.WorkBook.WorkView`
                     associated with this instance of the Module View.
    :ivar dtcSurvival: the :py:class:`rtk.survival.Survival` data
                         controller to use for accessing the Survival data
                         models.
    :ivar gtk.TreeView treeview: the gtk.TreeView() displaying the list of
                                 Survival analyses.
    """

    def __init__(self, controller, rtk_view, position):
        """
        Initializes the Module Book view for the Survival package.

        :param controller: the instance of the :py:class:`rtk.RTK.RTK` master
                           data controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Testing
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Testing view.  Pass -1 to add to the end.
        """

        # Initialize private dict attributes.

        # Initialize private list attribute
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self.workbook = None
        self.listbook = None
        self._model = None

        # Initialize public scalar attributes.
        self.mdcRTK = controller
        self.mdcRTK.dtcSurvival = controller.dtcSurvival

        # Create the main Survival class treeview.
        _fg_color = Configuration.RTK_COLORS[12]
        _bg_color = Configuration.RTK_COLORS[13]
        (self.treeview, self._lst_col_order) = Widgets.make_treeview(
            'Dataset', 13, _fg_color, _bg_color)

        self.treeview.set_tooltip_text(
            _(u"Displays the list of survival "
              u"analyses."))

        # Connect gtk.TreeView() editable cells to the callback function.
        i = 0
        for _column in self.treeview.get_columns():
            _cell = _column.get_cell_renderers()[0]
            try:
                if _cell.get_property('editable'):
                    _cell.connect('edited', self._on_cellrenderer_edited,
                                  self._lst_col_order[i])
            except TypeError:
                pass
            i += 1

        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_changed, None,
                                  None))
        self.treeview.connect('row_activated', self._on_row_changed)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _icon = Configuration.ICON_DIR + '32x32/survival.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Survival\nAnalyses") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the development program "
              u"survival analyses for the selected "
              u"revision."))

        _hbox = gtk.HBox()
        _hbox.pack_start(_image)
        _hbox.pack_end(_label)
        _hbox.show_all()

        rtk_view.notebook.insert_page(
            _scrollwindow, tab_label=_hbox, position=position)

        # Create a List View to associate with this Module View.
        self.listbook = ListView(self)

        # Create a Work View to associate with this Module View.
        self.workbook = WorkView(self)

    def request_load_data(self):
        """
        Method to load the Survival Module Book view gtk.TreeModel() with
        Survival analyses information.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve all the development program survival analyses.
        (_survivals, __) = self.mdcRTK.dtcSurvival.request_survival(
            self.mdcRTK.project_dao, self.mdcRTK.revision_id)

        # Clear the Survival Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()
        for _survival in _survivals:
            _model.append(None, _survival[1:])

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        return False

    def request_add_survival(self, revision_id):
        """
        Method to request adding a new Survival analysis to the selected
        revision.

        :param int revision_id: the Revision ID to add the new Survival
                                analysis to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_results,
         _error_code) = self.mdcRTK.dtcSurvival.add_survival(revision_id)

        # If the Survival analysis was successfully added to the database, add
        # it from the list.
        if _results:
            self.request_load_data(self.mdcRTK.project_dao, revision_id)

        return False

    def request_delete_survival(self, survival_id):
        """
        Method to request deleting the selected Survival analysis.

        :param int survival_id: the Survival ID to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_results,
         _error_code) = self.mdcRTK.dtcSurvival.delete_survival(survival_id)

        # If the Survival analysis was successfully removed from the database,
        # remove it from the list.
        if _results:
            (_model, _row) = self.treeview.get_selected().get_selection()
            _model.remove(_row)

        return False

    def request_save_survival(self, survival_id):
        """
        Method to request the selected Survival analysis be saved.

        :param int survival_id: the ID of the Survival analysis to save.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_results,
         _error_code) = self.mdcRTK.dtcSurvival.save_survival(survival_id)

        return False

    def request_load_records(self, survival_id):
        """
        Loads the Survival Module Book view gtk.TreeModel() with Survival
        analyses information.

        :param in survival_id: the ID of the Survival analysis associated with
                               the Dataset.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_records, __) = self.mdcRTK.dtcSurvival.request_records(survival_id)

        return _records

    def request_add_record(self, survival_id):
        """
        Method to request a record be added to the selected Dataset.

        :param int survival_id: the ID of the Survival analysis the record will
                                be added to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_result,
         _error_code) = self.mdcRTK.dtcSurvival.add_record(survival_id)

        return False

    def request_delete_record(self, survival_id, record_id):
        """
        Method to request a record be deleted from the selected Dataset.

        :param int survival_id: the ID of the Survival analysis the record will
                                be deleted from.
        :param int record_id: the ID of the record to be deleted.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_result, _error_code) = self.mdcRTK.dtcSurvival.delete_record(
            survival_id, record_id)

        return False

    def request_save_records(self, survival_id):
        """
        Method to request the Survival analysis records be saved.

        :param int survival_id: the ID of the Survival analysis to save the
                                records for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _survival = self.mdcRTK.dtcSurvival.dicSurvival[survival_id]

        for _record_id in _survival.dicRecords.keys():
            (_results, _error_code) = self.mdcRTK.dtcSurvival.save_record(
                survival_id, _record_id, _survival.dicRecords[_record_id])

        return False

    def request_calculate_tbf(self, survival_id):
        """
        Method to request the interarrival times be calculated in a dataset.

        :param int survival_id: the ID of the Survival analyses the dataset
                                belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _survival = self.mdcRTK.dtcSurvival.dicSurvival[survival_id]
        _records = _survival.dicRecords

        _keys = [_key for _key in _records.keys()]
        _records[_keys[0]].interarrival_time = _records[_keys[
            0]].right_interval
        for i in range(len(_keys) - 1):
            _survival.calculate_tbf(_keys[i], _keys[i + 1])

        return False

    def request_consolidate_dataset(self, survival_id):
        """
        Consolidates the data set so there are only unique failure times,
        suspension times, and intervals with a quantity value rather than a
        single record for each event.

        :param int survival_id: the Survival ID of the dataset to consolidate.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.mdcRTK.dtcSurvival.consolidate_dataset()

        # Reload the dataset tree.
        self.request_load_records(survival_id)

        return False

    def update(self, position, new_text):
        """
        Updates the selected row in the Module Book gtk.TreeView() with changes
        to the Survival data model attributes.  Called by other views when the
        Survival data model attributes are edited via their gtk.Widgets().

        :param int position: the ordinal position in the Module Book
                             gtk.TreeView() of the data being updated.
        :param str new_text: the new value of the attribute to be updated.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = self.treeview.get_selection().get_selected()
        try:
            _model.set(_row, self._lst_col_order[position], new_text)
        except TypeError:
            print position, self._lst_col_order[position], new_text

        return False

    def _on_button_press(self, treeview, event):
        """
        Method to handle mouse clicks on the Survival package Module Book
        gtk.TreeView().

        :param gtk.TreeView treeview: the Survival class gtk.TreeView().
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
        Callback function to handle events for the Survival package Module
        Book gtk.TreeView().  It is called whenever a Module Book
        gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the Survival class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        _survival_id = _model.get_value(_row, 0)

        self._model = self.mdcRTK.dtcSurvival.dicSurvival[_survival_id]
        self.mdcRTK.dtcSurvival.request_records(_survival_id)

        self.workbook.load(self._model)
        self.listbook.load(self._model)

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cellrenderer_edited(self, __cell, __path, new_text, index):
        """
        Callback method to handle events for the Survival package Module Book
        gtk.CellRenderer().  It is called whenever a Module Book
        gtk.CellRenderer() is edited.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str __path: the path of the gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the gtk.CellRenderer() that was
                             edited.
        :param int index: the position in the Survival package Module Book
                          gtk.TreeView().
        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """

        from datetime import datetime

        if self._lst_col_order[index] == 2:
            try:
                self._model.description = new_text
            except ValueError:
                self._model.description = ''
        elif self._lst_col_order[index] == 5:
            try:
                self._model.confidence = float(new_text)
            except ValueError:
                self._model.confidence = 0.75
        elif self._lst_col_order[index] == 34:
            try:
                self._model.start_time = float(new_text)
            except ValueError:
                self._model.start_time = 0.0
        elif self._lst_col_order[index] == 9:
            try:
                self._model.rel_time = float(new_text)
            except ValueError:
                self._model.rel_time = 100.0
        elif self._lst_col_order[index] == 10:
            try:
                self._model.n_rel_points = int(new_text)
            except ValueError:
                self._model.n_rel_points = 10
        elif self._lst_col_order[index] == 35:
            try:
                self._model.start_date = Utilities.date_to_ordinal(new_text)
            except ValueError:
                self._model.start_date = datetime.today().toordinal()
        elif self._lst_col_order[index] == 36:
            try:
                self._model.end_date = Utilities.date_to_ordinal(new_text)
            except ValueError:
                self._model.end_date = datetime.today().toordinal()

        self.workbook.update()

        return False
