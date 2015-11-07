#!/usr/bin/env python
"""
############################
Survival Package Module View
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.survival.ModuleBook.py is part of The RTK Project
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
    The Module Book view displays all the Survival items associated with the
    RTK Project in a flat list.  The attributes of a Module Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Survival attribute.
    :ivar _lst_col_order: list containing the order of the columns in the
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
    :ivar dtcActions: the :py:class:`rtk.survival.action.Action` data
                      controller to use for accessing the Survival Action data
                      models.
    :ivar dtcComponents: the :py:class:`rtk.survival.component.Component` data
                         controller to use for accessing the Survival Component
                         data models.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the list of
                    Survival tasks.
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Survival package.

        :param controller: the instance of the
                           :py:class:`rtk.survival.Survival` data
                           controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Survival
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Survival view.  Pass -1 to add to the end.
        :param *args: other user arguments to pass to the Module View.
        """

        # Initialize private dict attributes.

        # Initialize private list attribute
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._workbook = None
        self._listbook = None
        self._model = None
        self._dao = None

        # Initialize public scalar attributes.
        self.dtcSurvival = controller

        # Create the main Survival class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Dataset', 16, None,
                                                    None, _conf.RTK_COLORS[12],
                                                    _conf.RTK_COLORS[13])

        self.treeview.set_tooltip_text(_(u"Displays the list of survival "
                                         u"analyses."))

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

        _icon = _conf.ICON_DIR + '32x32/survival.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Survival\nAnalyses") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the development program "
                                  u"survival analyses for the selected "
                                  u"revision."))

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

    def request_load_data(self, dao, revision_id, query=None):
        """
        Loads the Survival Module Book view gtk.TreeModel() with Survival
        analyses information.

        :param dao: the :py:class: `rtk.dao.DAO` object used to communicate
                    with the RTK Project database.
        :param int revision_id: the ID of the revision to load survival data
                                for.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._dao = dao

        # Retrieve all the development program survival analyses.
        (_survivals,
         __) = self.dtcSurvival.request_survival(dao, revision_id)

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

        #self._listbook.load(revision_id)

        return False

    def request_add_dataset(self, survival_id):
        """
        Method to request a Dataset be added to the selected Survival analysis.

        :param int survival_id: the ID of the Survival analysis the selected
                                Dataset belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_results, _error_code) = self.dtcSurvival.add_dataset(survival_id)

        return False

    def request_delete_dataset(self, survival_id):
        """
        Method to request the selected Dataset be deleted from the selected
        Survival analysis.

        :param int survival_id: the ID of the Survival analysis the selected
                                Dataset belongs to.
        :param int dataset_id: the ID of the Dataset to delete.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_results, _error_code) = self.dtcSurvival.delete_dataset(survival_id,
                                                                  dataset_id)

        return False

    def request_save_dataset(self, survival_id, dataset_id):
        """
        Method to request the selected Dataset be saved.

        :param int survival_id: the ID of the Survival analysis the selected
                                Dataset belongs to.
        :param int dataset_id: the ID of the Dataset to save.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_results, _error_code) = self.dtcSurvival.save_dataset(survival_id,
                                                                dataset_id)

        return False

    def request_load_records(self, survival_id, dataset_id):
        """
        Loads the Survival Module Book view gtk.TreeModel() with Survival
        analyses information.

        :param in survival_id: the ID of the Survival analysis associated with
                               the Dataset.
        :param int dataset_id: the ID of the Dataset records to retrieve.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_dataset,
         __) = self.dtcSurvival.request_records(survival_id, dataset_id)

        return _dataset

    def request_add_record(self, survival_id, dataset_id):
        """
        Method to request a record be added to the selected Dataset.

        :param int survival_id: the ID of the Survival analysis the record will
                                be added to.
        :param int dataset_id: the ID of the Dataset the record will be added
                               to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_result, _error_code) = self.dtcSurvival.add_record(survival_id,
                                                             dataset_id)

        return False

    def request_delete_record(self, survival_id, dataset_id, record_id):
        """
        Method to request a record be deleted from the selected Dataset.

        :param int survival_id: the ID of the Survival analysis the record will
                                be deleted from.
        :param int dataset_id: the ID of the Dataset the record will be deleted
                               from.
        :param int record_id: the ID of the record to be deleted.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_result, _error_code) = self.dtcSurvival.delete_record(survival_id,
                                                                dataset_id,
                                                                record_id)

        return False

    def update(self, position, new_text):
        """
        Updates the selected row in the Module Book gtk.TreeView() with changes
        to the Survival data model attributes.  Called by other views when
        the Survival data model attributes are edited via their
        gtk.Widgets().

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
            print position, new_text

        return False

    def _on_button_press(self, treeview, event):
        """
        Callback method for handling mouse clicks on the Survival package
        Module Book gtk.TreeView().

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
        :rtype: boolean
        """

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        _survival_id = _model.get_value(_row, 0)

        self._model = self.dtcSurvival.dicSurvival[_survival_id]
        self.dtcSurvival.request_datasets(_survival_id)

        self._workbook.load(self._model)

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, new_text, index):
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

        self._workbook.update()

        return False
