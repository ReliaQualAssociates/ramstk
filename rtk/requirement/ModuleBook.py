#!/usr/bin/env python
"""
###############################
Requirement Package Module View
###############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       ModuleBook.py is part of The RTK Project
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
try:
    import gobject
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
from ListBook import ListView
from WorkBook import WorkView

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext

# TODO: Fix all docstrings; copy-paste errors.
class ModuleView(object):
    """
    The Module Book view displays all the Requirements associated with the RTK
    Project in a hierarchical list.  The attributes of a Module Book view are:

    :ivar _model: the :class:`rtk.requirement.Requirement.Model` data model
                  that is currently selected.
    :ivar _stakeholder_model: the :class:`rtk.stakeholder.Stakeholder.Model`
                              data model that is currently selected.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View :class:`gtk.TreeView`.
    :ivar _workbook: the :class:`rtk.requirement.WorkBook.WorkView` associated
                     with this instance of the Module View.
    :ivar dtcRequirement: the :class:`rtk.requirement.Requirement.Requirement`
                          data controller to use for accessing the Requirement
                          data models.
    :ivar dtcStakeholder: the :class:`rtk.stakeholder.Stakeholder.Stakeholder`
                          data controller to use for accessing the Stakeholder
                          data models.
    :ivar treeview: the :class:`gtk.TreeView` displaying the list of
                    Requirements.
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Function package.

        :param rtk.requirement.Requirement controller: the instance of the
                                                       Requirement data
                                                       controller to use with
                                                       this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Requirement
                                      view into.
        :param int position: the page position in the gtk.Notebook() to
                             insert the Requirement view.  Pass -1 to add to the
                             end.
        :param *args: other user arguments to pass to the Module View.
        """

        # Initialize private scalar attributes.
        self._model = None
        self._stakeholder_model = None

        # initialize public dict attributes.
        self.dicRequirementTypes = {}
        self.dicOwners = {}

        # Initialize public scalar attributes.
        self.dtcRequirement = controller
        self.dtcStakeholder = args[0][0]
        self.dtcMatrices = args[0][1]
        self.site_dao = args[0][2]

        # Create the main Requirement class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Requirement', 2,
                                                    None, None,
                                                    _conf.RTK_COLORS[4],
                                                    _conf.RTK_COLORS[5])
# TODO: Move this to RTK.py and create an application-wide dict.
        # Load the Requirements Type gtk.CellRendererCombo()
        _query = "SELECT fld_requirement_type_desc, \
                         fld_requirement_type_code, \
                         fld_requirement_type_id \
                  FROM tbl_requirement_type"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _cell = self.treeview.get_column(
            self._lst_col_order[4]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        self.dicRequirementTypes[''] = ["", 0]
        for i in range(len(_results)):
            _cellmodel.append([_results[i][0]])
            self.dicRequirementTypes[_results[i][0]] = [_results[i][1],
                                                        _results[i][2]]

        # Load the Priority gtk.CellRendererCombo()
        _cell = self.treeview.get_column(
            self._lst_col_order[5]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(1, 6):
            _cellmodel.append([str(i)])
# TODO: Move this to RTK.py and create an application-wide dict.
        # Load the Owner gtk.CellRendererCombo()
        _query = "SELECT fld_group_name, fld_group_id \
                  FROM tbl_groups \
                  ORDER BY fld_group_name ASC"
        (_results, _error_code, __) = self.site_dao.execute(_query,
                                                            commit=False)
        _cell = self.treeview.get_column(
            self._lst_col_order[10]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(_results)):
            _cellmodel.append([_results[i][0]])
            self.dicOwners[_results[i][0]] = [_results[i][1], i]

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
            _cell[0].connect('edited', self._on_cell_edited, i,
                             self.treeview.get_model())

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Requirements") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the engineering requirements for "
                                  u"the selected revision."))

        _scrollwindow.show_all()

        rtk_view.notebook.insert_page(_scrollwindow, tab_label=_label,
                                      position=position)

        # Create a List View to associate with this Module View.
        self._listbook = ListView(rtk_view.listview, self, self.dtcMatrices)

        # Create a Work View to associate with this Module View.
        self._workbook = WorkView(rtk_view.workview, self)

    def request_load_data(self, dao, revision_id):
        """
        Loads the Requirement Module Book view gtk.TreeModel() with requirement
        information.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_requirements,
         __) = self.dtcRequirement.request_requirements(dao, revision_id)

        # Only load the requirements associated with the selected Revision.
        _requirements = [_r for _r in _requirements if _r[0] == revision_id]
        _top_reqs = [_r for _r in _requirements if _r[13] == -1]

        # Clear the Requirement Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()

        # Recusively load the Requirement Module View gtk.TreeModel().
        self._load_treeview(dao, _top_reqs, _requirements, _model)

        # Select the first row in the gtk.TreeView().
        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        #self._listbook.load(revision_id)

        return False

    def _load_treeview(self, dao, parents, requirements, model, row=None):
        """
        Method to recursively load the gtk.TreeModel().  Recursive loading is
        needed to accomodate the hierarchical structure of Requirements.

        :param rtk.DAO dao: the Data Access Object to pass to the FMEA data
                            controller.
        :param list parents: the list of top-level requirements to load.
        :param list requirements: the complete list of requirements to use for
                                  finding the child requirements for each
                                  parent.
        :param gtk.TreeModel model: the Requirement Module View gtk.TreeModel().
        :keyword gtk.TreeIter row: the parent gtk.TreeIter().
        """
# TODO: Is passing the dao object around the best way or is it better as a private instance attribute?
        for _requirement in parents:
            if _requirement[13] == -1:
                row = None
            _piter = model.append(row, _requirement)
            _parent_id = _requirement[1]

            self.dtcStakeholder.request_inputs(dao, _requirement[0])

            # Find the child requirements of the current parent requirement.
            # These # will be the new parent requirements to pass to this
            # method.
            _parents = [_r for _r in requirements if _r[13] == _parent_id]
            self._load_treeview(dao, _parents, requirements, model, _piter)

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
        Callback requirement for handling mouse clicks on the Requirement package
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
            print "Pop-up a menu!"

        return False

    def _on_row_changed(self, treeview, __path, __column):
        """
        Callback requirement to handle events for the Requirement package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Requirement class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = treeview.get_selection().get_selected()

        _requirement_id = _model.get_value(_row, 1)
        self._model = self.dtcRequirement.dicRequirements[_requirement_id]

        self._workbook.load(self._model)

        return False

    def _on_cell_edited(self, __cell, path, new_text, position, model):
        """
        Callback requirement to handle edits of the Requirement package Module
        Book gtk.Treeview().

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

        self._workbook.update()

        return False
