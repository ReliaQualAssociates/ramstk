#!/usr/bin/env python
"""
###############################
Requirement Package Module View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.requirement.ModuleBook.py is part of The RTK Project
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
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ModuleView(object):
    """
    The Module Book view displays all the Requirements associated with the RTK
    Project in a hierarchical list.  The attributes of a Module Book view are:

    :ivar _model: the :py:class:`rtk.requirement.Requirement.Model` data model
                  that is currently selected.
    :ivar _stakeholder_model: the :py:class:`rtk.stakeholder.Stakeholder.Model`
                              data model that is currently selected.
    :ivar list _lst_col_order: list containing the order of the columns in the
                               Module View gtk.TreeView().
    :ivar _workbook: the :py:class:`rtk.requirement.WorkBook.WorkView`
                     associated with this instance of the Module View.
    :ivar mdcRTK: the :py:class:`rtk.RTK.RTK` master data controller to use.
    :ivar gtk.TreeView treeview: the gtk.TreeView() displaying the list of
                                 Requirements.
    """

    def __init__(self, controller, rtk_view, position):
        """
        Initializes the Module Book view for the Requirement package.

        :param controller: the instance of the :py:class:`rtk.RTK.RTK` master
                           data controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Requirement
                                      view into.
        :param int position: the page position in the gtk.Notebook() to
                             insert the Requirement view.  Pass -1 to add to
                             the end.
        """

        # Define private dictionary attributes.
        self._dic_handler_id = {}

        # Define private list attributes.

        # Define private scalar attributes.
        self._dtc_requirements = controller.dtcRequirement
        self._dtc_stakeholder = controller.dtcStakeholder
        self._dtc_matrices = controller.dtcMatrices
        self._model = None
        self._stakeholder_model = None

        # Define public dictionary attributes.
        self.dicRequirementTypes = {}
        self.dicOwners = {}

        # Define public list attributes.

        # Define public scalar attributes.
        self.mdcRTK = controller

        # Create the main Requirement class treeview.
        _bg_color = Configuration.RTK_COLORS[4]
        _fg_color = Configuration.RTK_COLORS[5]
        (self.treeview,
         self._lst_col_order) = Widgets.make_treeview('Requirement', 2,
                                                      _bg_color, _fg_color)

        # Load the Requirements Type gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[4]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        self.dicRequirementTypes[''] = ["", 0]

        # Each _type is [Description, Code, ID]
        for __, _type in enumerate(Configuration.RTK_REQUIREMENT_TYPES):
            _cellmodel.append([_type[0]])
            self.dicRequirementTypes[_type[0]] = [_type[1], _type[2]]

        # Load the Priority gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[5]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(1, 6):
            _cellmodel.append([str(i)])

        # Load the Owner gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[10]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for _index, _owner in enumerate(Configuration.RTK_WORKGROUPS):
            _cellmodel.append([_owner[0]])
            self.dicOwners[_owner[0]] = [_owner[1], _index]

        self.treeview.set_tooltip_text(_(u"Displays the hierarchical list of "
                                         u"requirements."))
        self.treeview.connect('cursor_changed', self._on_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._on_row_changed)
        self.treeview.connect('button_press_event', self._on_button_press)

        # Connect the cells to the callback function.
        for i in [2, 4, 5, 6, 7, 8, 10]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            self._dic_handler_id[i] = _cell[0].connect('edited',
                                                       self._on_cell_edited, i,
                                                       self.treeview.get_model())

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _icon = Configuration.ICON_DIR + '32x32/requirement.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Requirements") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the engineering requirements for "
                                  u"the selected revision."))

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

    def request_load_data(self):
        """
        Method to load the Requirement Module Book view gtk.TreeModel() with
        Requirement information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_requirements, __) = self._dtc_requirements.request_requirements(
            self.mdcRTK.project_dao, self.mdcRTK.revision_id)

        # Only load the requirements associated with the selected Revision.
        _requirements = [_r for _r in _requirements
                         if _r[0] == self.mdcRTK.revision_id]
        _top_reqs = [_r for _r in _requirements if _r[13] == -1]

        # Clear the Requirement Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()

        # Recusively load the Requirement Module View gtk.TreeModel().
        self._load_treeview(_top_reqs, _requirements, _model)

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

    def _load_treeview(self, parents, requirements, model, row=None):
        """
        Method to recursively load the gtk.TreeModel().  Recursive loading is
        needed to accomodate the hierarchical structure of Requirements.

        :param list parents: the list of top-level requirements to load.
        :param list requirements: the complete list of requirements to use for
                                  finding the child requirements for each
                                  parent.
        :param gtk.TreeModel model: the Requirement Module View
                                    gtk.TreeModel().
        :keyword gtk.TreeIter row: the parent gtk.TreeIter().
        """

        for _requirement in parents:
            if _requirement[13] == -1:
                row = None
            _piter = model.append(row, _requirement)
            _parent_id = _requirement[1]

            self._dtc_stakeholder.request_inputs(self.mdcRTK.project_dao,
                                                 _requirement[0])

            # Find the child requirements of the current parent requirement.
            # These # will be the new parent requirements to pass to this
            # method.
            _parents = [_r for _r in requirements if _r[13] == _parent_id]
            self._load_treeview(_parents, requirements, model, _piter)

        return False

    def update(self, position, new_text):
        """
        Updates the Module Book gtk.TreeView() with changes to the Requirement
        data model attributes.  Called by other views when the Requirement data
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
        Callback method for handling mouse clicks on the Requirement package
        Module Book gtk.TreeView().

        :param gtk.TreeView treeview: the Requirement class gtk.TreeView().
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
# TODO: See bug 178
            pass

        return False

    def _on_row_changed(self, treeview, __path, __column):
        """
        Callback method to handle events for the Requirement package Module
        Book gtk.TreeView().  It is called whenever a Module Book
        gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the Requirement class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = treeview.get_selection().get_selected()

        if _row is not None:
            _requirement_id = _model.get_value(_row, 1)
            self._model = self._dtc_requirements.dicRequirements[_requirement_id]
            self.workbook.load(self._model)

        return False

    def _on_cell_edited(self, cell, path, new_text, position, model):
        """
        Callback requirement to handle edits of the Requirement package Module
        Book gtk.Treeview().

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
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
# TODO: Refactor _on_cell_edited; current McCabe Complexity Metric = 11.
        cell.handler_block(self._dic_handler_id[position])

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        # Now update the Requirement data model.
        if self._lst_col_order[position] == 2:
            self._model.description = str(new_text)
        elif self._lst_col_order[position] == 4:
            self._model.requirement_type = str(new_text)
        elif self._lst_col_order[position] == 5:
            self._model.priority = str(new_text)
        elif self._lst_col_order[position] == 6:
            self._model.specification = str(new_text)
        elif self._lst_col_order[position] == 7:
            self._model.page_number = str(new_text)
        elif self._lst_col_order[position] == 8:
            self._model.figure_number = str(new_text)
        elif self._lst_col_order[position] == 10:
            self._model.owner = str(new_text)

        self.workbook.update()

        cell.handler_unblock(self._dic_handler_id[position])

        return False
