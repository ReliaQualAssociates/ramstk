#!/usr/bin/env python
"""
############################
Revision Package Module View
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.revision.ModuleBook.py is part of The RTK Project
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
    import Configuration as _conf
    import gui.gtk.Widgets as _widg
except ImportError:
    import rtk.Configuration as _conf
    import rtk.gui.gtk.Widgets as _widg
from ListBook import ListView
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
    The Module Book view displays all the Revisions associated with the RTK
    Project in a flat list.  The attributes of a Module Book view are:

    :ivar _dtc_profile: the :class:`rtk.usage.UsageProfile.UsageProfile` data
                        controller to use for accessing the Usage Profile data
                        models.
    :ivar _dtc_definitions: the :py:class:`rtk.failure_definition.FailureDefinition.FailureDefinition`
                            data controller to use for accessing the Failure
                            Definition data models.
    :ivar _model: the :py:class:`rtk.revision.Revision.Model` data model that
                  is currently selected.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View gtk.TreeView().
    :ivar dmcRTK: the :py:class:`rtk.RTK.RTK` data controller instance.
    :ivar gtk.TreeView treeview: the gtk.TreeView() displaying the list of
                                 Revisions.
    :ivar listbook:
    :ivar workbook:
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Revision package.

        :param controller: the :py:class:`rtk.RTK.RTK` data controller to use
                           with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Revision
                                      view into.
        :param int position: the page position in the gtk.Notebook() to
                             insert the Revision view.  Pass -1 to add to the
                             end.
        :param *args: other user-defined arguments.
        """

        # Initialize private scalar attributes.
        self._dtc_revision = controller.dtcRevision
        self._dtc_matrices = controller.dtcMatrices
        self._dtc_profile = controller.dtcProfile
        self._dtc_definitions = controller.dtcDefinitions
        self._dtc_hardware = controller.dtcHardwareBoM
        self._model = None

        # Initialize public scalar attributes.
        self.mdcRTK = controller

        # Create the main Revision class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Revision', 0,
                                                    _conf.RTK_COLORS[0],
                                                    _conf.RTK_COLORS[1])

        self.treeview.set_tooltip_text(_(u"Displays the list of revisions."))
        self.treeview.connect('cursor_changed', self._on_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._on_row_changed)
        self.treeview.connect('button_press_event', self._on_button_press)

        # Connect the cells to the callback function.
        for i in [17, 20, 22]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._on_cell_edited, i,
                             self.treeview.get_model())

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _icon = _conf.ICON_DIR + '32x32/revision.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Revisions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the program revisions."))

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

    def request_load_data(self, dao, revision_id=None):
        """
        Loads the Revision Module Book view gtk.TreeModel() with revision
        information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
        # TODO: Remove dao and revision_id parameters after converting all modules.
        (_revisions,
         __) = self._dtc_revision.request_revisions(self.mdcRTK.project_dao)

        _model = self.treeview.get_model()
        _model.clear()
        for _revision in _revisions:
            _model.append(None, _revision)
            self._dtc_profile.request_profile(_revision[0],
                                              self.mdcRTK.project_dao)
            self._dtc_definitions.request_definitions(_revision[0],
                                                      self.mdcRTK.project_dao)
            # TODO: Remove the last two parameters after re-writing the method.
            self._dtc_matrices.request_matrix(_revision[0], None, 0)

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
        Updates the Module Book gtk.TreeView() with changes to the Revision
        data model attributes.  Called by other views when the Revision data
        model attributes are edited via their gtk.Widgets().

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
        Callback function for handling mouse clicks on the Revision package
        Module Book gtk.TreeView().

        :param gtk.TreeView treeview: the Revision class gtk.TreeView().
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
        Callback function to handle events for the Revision package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Revision class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = treeview.get_selection().get_selected()

        _revision_id = _model.get_value(_row, 0)
        self._model = self._dtc_revision.dicRevisions[_revision_id]

        # Load the remaining active RTK modules for the selected revision.
        self.mdcRTK.load_revision(_revision_id)

        # Load the hardware list for the selected revision.
        _query = "SELECT fld_name, fld_hardware_id, fld_description \
                  FROM rtk_hardware \
                  WHERE fld_revision_id={0:d} \
                  AND fld_part=0".format(self._model.revision_id)
        (_results,
         _error_code,
         __) = self.mdcRTK.project_dao.execute(_query, commit=False)
        _conf.RTK_HARDWARE_LIST = [_assembly for _assembly in _results]

        # Load the software list for the selected revision.
        _query = "SELECT fld_description, fld_software_id, fld_description \
                  FROM rtk_software \
                  WHERE fld_revision_id={0:d}".format(self._model.revision_id)
        (_results,
         _error_code,
         __) = self.mdcRTK.project_dao.execute(_query, commit=False)
        _conf.RTK_SOFTWARE_LIST = [_module for _module in _results]

        self.workbook.load(self._model)
        self.listbook.load(_revision_id)

        return False

    def _on_cell_edited(self, __cell, path, new_text, position, model):
        """
        Callback function to handle edits of the Revision package Module Book
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

        # Now update the Revision data model.
        if self._lst_col_order[position] == 17:
            self._model.name = str(new_text)
        elif self._lst_col_order[position] == 20:
            self._model.remarks = str(new_text)
        elif self._lst_col_order[position] == 22:
            self._model.code = str(new_text)

        self.workbook.update()

        return False
