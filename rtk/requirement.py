#!/usr/bin/env python
"""
This is the Class that is used to represent and hold information related to
the requirements of the Program.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       requirement.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale
import sys

# Modules required for the GUI.
try:
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    import gtk  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gtk.glade  # @UnusedImport
except ImportError:
    sys.exit(1)
try:
    import gobject
except ImportError:
    sys.exit(1)

import pandas as pd

# Import other RTK modules.
import configuration as _conf
import utilities as _util
import widgets as _widg
from _reports_.tabular import ExcelReport

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _vandv_tree_edit(__cell, path, new_text, position, model):
    """
    Function called whenever a gtk.CellRenderer() is edited in the V&V task
    list.

    :param __cell: the gtk.CellRenderer() that was edited.
    :param path: the gtk.TreeView() path of the gtk.CellRenderer() that was
                 edited.
    :param new_text: the new text in the edited gtk.CellRenderer().
    :param position: the column position of the edited gtk.CellRenderer().
    :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
    """

    if position == 4:
        model[path][position] = float(new_text)
    else:
        model[path][position] = new_text

    return False


def _add_to_combo(cell, __path, new_text):
    """
    Function to add a new value to a gtk.CellRendererCombo() that has the
    'has-entry' property set to True.

    :param cell: the gtk.CellRendererCombo() calling this function.
    :type cell: gtk.CellRendererCombo
    :param __path: the path of the currently selected gtk.TreeIter().
    :type __path: string
    :param new_text: the new text that was entered into the
                     gtk.CellRendererCombo().
    :type new_text: string
    :return: False if successful or True if an error is encountered.
    :rtype: boolean
    """

    # Get the current entries in the gtk.CellRendererCombo().
    _current_items = []
    _model = cell.get_property('model')
    _row = _model.get_iter_root()
    while _row is not None:
        _current_items.append(_model.get_value(_row, 0))
        _row = _model.iter_next(_row)

    if new_text not in _current_items:
        _model.append([new_text])

    return False


class Requirement(object):
    """
    The Requirement class is used to represent the requirements in a
    system being analyzed.

    :ivar revision_id: initial_value: 0
    :ivar requirement_id: initial_value: 0
    :ivar assembly_id: initial_value: 0
    :ivar requirement_desc: initial_value: ''
    :ivar requirement_type: initial_value: 0
    :ivar requirement_code: initial_value: ''
    :ivar derived: initial_value: False
    :ivar parent_requirement: initial_value: ''
    :ivar validated: initial_value: False
    :ivar validated_date: initial_value: ''
    :ivar owner: initial_value: 0
    :ivar specification: initial_value: ''
    :ivar page_number: initial_value: ''
    :ivar figure_number: initial_value: ''
    :ivar parent_id: initial_value: 0
    :ivar software_id: initial_value: 0
    :ivar clear_q1: initial_value: 0
    :ivar clear_q2: initial_value: 0
    :ivar clear_q3: initial_value: 0
    :ivar clear_q4: initial_value: 0
    :ivar clear_q5: initial_value: 0
    :ivar clear_q6: initial_value: 0
    :ivar clear_q7: initial_value: 0
    :ivar clear_q8: initial_value: 0
    :ivar clear_q9: initial_value: 0
    :ivar clear_q10: initial_value: 0
    :ivar complete_q1: initial_value: 0
    :ivar complete_q2: initial_value: 0
    :ivar complete_q3: initial_value: 0
    :ivar complete_q4: initial_value: 0
    :ivar complete_q5: initial_value: 0
    :ivar complete_q6: initial_value: 0
    :ivar complete_q7: initial_value: 0
    :ivar complete_q8: initial_value: 0
    :ivar complete_q9: initial_value: 0
    :ivar complete_q10: initial_value: 0
    :ivar consistent_q1: initial_value: 0
    :ivar consistent_q2: initial_value: 0
    :ivar consistent_q3: initial_value: 0
    :ivar consistent_q4: initial_value: 0
    :ivar consistent_q5: initial_value: 0
    :ivar consistent_q6: initial_value: 0
    :ivar consistent_q7: initial_value: 0
    :ivar consistent_q8: initial_value: 0
    :ivar consistent_q9: initial_value: 0
    :ivar consistent_q10: initial_value: 0
    :ivar verifiable_q1: initial_value: 0
    :ivar verifiable_q2: initial_value: 0
    :ivar verifiable_q3: initial_value: 0
    :ivar verifiable_q4: initial_value: 0
    :ivar verifiable_q5: initial_value: 0
    :ivar verifiable_q6: initial_value: 0
    :ivar priority: initial_value: 1
    """

    def __init__(self, application):
        """
        Initializes the Requirement class.

        :param RTK application: the current instance of the RTK application.
        """

        # Define private Requirement class attributes.
        self._ready = False
        self._app = application
        self._selected_tab = 1

        # Define private Requirement class dictionary attributes.
        self._dic_owners = {}

        # Define private Requirement class list attributes.
        self._lst_handler_id = []

        # Define public Requirement class attributes.
        self.requirement_id = 0
        self.assembly_id = 0
        self.requirement_desc = ''
        self.requirement_type = 0
        self.requirement_code = ''
        self.derived = False
        self.parent_requirement = ''
        self.validated = False
        self.validated_date = ''
        self.owner = 0
        self.specification = ''
        self.page_number = ''
        self.figure_number = ''
        self.parent_id = 0
        self.software_id = 0
        self.clear_q1 = 0
        self.clear_q2 = 0
        self.clear_q3 = 0
        self.clear_q4 = 0
        self.clear_q5 = 0
        self.clear_q6 = 0
        self.clear_q7 = 0
        self.clear_q8 = 0
        self.clear_q9 = 0
        self.clear_q10 = 0
        self.complete_q1 = 0
        self.complete_q2 = 0
        self.complete_q3 = 0
        self.complete_q4 = 0
        self.complete_q5 = 0
        self.complete_q6 = 0
        self.complete_q7 = 0
        self.complete_q8 = 0
        self.complete_q9 = 0
        self.complete_q10 = 0
        self.consistent_q1 = 0
        self.consistent_q2 = 0
        self.consistent_q3 = 0
        self.consistent_q4 = 0
        self.consistent_q5 = 0
        self.consistent_q6 = 0
        self.consistent_q7 = 0
        self.consistent_q8 = 0
        self.consistent_q9 = 0
        self.consistent_q10 = 0
        self.verifiable_q1 = 0
        self.verifiable_q2 = 0
        self.verifiable_q3 = 0
        self.verifiable_q4 = 0
        self.verifiable_q5 = 0
        self.verifiable_q6 = 0
        self.priority = 1

        # Create the main REQUIREMENT class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Requirement', 2,
                                                    self._app, None,
                                                    _conf.RTK_COLORS[4],
                                                    _conf.RTK_COLORS[5])

        # Toolbar widgets.
        self.btnAdd = gtk.ToolButton()
        self.btnAddChild = gtk.ToolButton()
        self.btnAddSibling = gtk.ToolButton()
        self.btnAssign = gtk.ToolButton()
        self.btnRemove = gtk.ToolButton()
        self.btnSave = gtk.ToolButton()

        # Stakeholder input page widgets.
        (self.tvwStakeholderInput,
         self._lst_stakeholder_col_order) = _widg.make_treeview('Stakeholder',
                                                                10, self._app,
                                                                None)

        # General data page widgets.
        self.btnValidateDate = _widg.make_button(height=25,
                                                 width=25,
                                                 label="...",
                                                 image='calendar')

        self.chkDerived = _widg.make_check_button()
        self.chkValidated = _widg.make_check_button()

        self.cmbOwner = _widg.make_combo(simple=False)
        self.cmbRqmtType = _widg.make_combo(simple=False)
        self.cmbPriority = _widg.make_combo(width=50, simple=True)

        self.txtCode = _widg.make_entry(width=100, editable=False)
        self.txtFigureNumber = _widg.make_entry()
        self.txtPageNumber = _widg.make_entry()
        self.txtRequirement = gtk.TextBuffer()
        self.txtSpecification = _widg.make_entry()
        self.txtValidatedDate = _widg.make_entry(width=100)

        # Analysis tab widgets.
        self.chkClearQ1 = _widg.make_check_button()
        self.chkClearQ2 = _widg.make_check_button()
        self.chkClearQ3 = _widg.make_check_button()
        self.chkClearQ4 = _widg.make_check_button()
        self.chkClearQ5 = _widg.make_check_button()
        self.chkClearQ6 = _widg.make_check_button()
        self.chkClearQ7 = _widg.make_check_button()
        self.chkClearQ8 = _widg.make_check_button()
        self.chkClearQ9 = _widg.make_check_button()
        self.chkCompleteQ1 = _widg.make_check_button()
        self.chkCompleteQ2 = _widg.make_check_button()
        self.chkCompleteQ3 = _widg.make_check_button()
        self.chkCompleteQ4 = _widg.make_check_button()
        self.chkCompleteQ5 = _widg.make_check_button()
        self.chkCompleteQ6 = _widg.make_check_button()
        self.chkCompleteQ7 = _widg.make_check_button()
        self.chkCompleteQ8 = _widg.make_check_button()
        self.chkCompleteQ9 = _widg.make_check_button()
        self.chkCompleteQ10 = _widg.make_check_button()
        self.chkConsistentQ1 = _widg.make_check_button()
        self.chkConsistentQ2 = _widg.make_check_button()
        self.chkConsistentQ3 = _widg.make_check_button()
        self.chkConsistentQ4 = _widg.make_check_button()
        self.chkConsistentQ5 = _widg.make_check_button()
        self.chkConsistentQ6 = _widg.make_check_button()
        self.chkConsistentQ7 = _widg.make_check_button()
        self.chkConsistentQ8 = _widg.make_check_button()
        self.chkConsistentQ9 = _widg.make_check_button()
        self.chkConsistentQ10 = _widg.make_check_button()
        self.chkVerifiableQ1 = _widg.make_check_button()
        self.chkVerifiableQ2 = _widg.make_check_button()
        self.chkVerifiableQ3 = _widg.make_check_button()
        self.chkVerifiableQ4 = _widg.make_check_button()
        self.chkVerifiableQ5 = _widg.make_check_button()
        self.chkVerifiableQ6 = _widg.make_check_button()

        # V & V tab widgets.
        self.cmbVandVTasks = _widg.make_combo(simple=False)
        self.scwValidation = gtk.ScrolledWindow()
        self.tvwValidation = gtk.TreeView()

        # Put it all together.
        _toolbar = self._create_toolbar()

        self.notebook = self._create_notebook()

        self.vbxRequirement = gtk.VBox()
        self.vbxRequirement.pack_start(_toolbar, expand=False)
        self.vbxRequirement.pack_end(self.notebook)

        self.notebook.connect('switch-page', self._notebook_page_switched)
        self.notebook.connect('select-page', self._notebook_page_switched)

    def create_tree(self):
        """
        Creates the Requirement class gtk.TreeView() and connects it to
        callback functions to handle editing.  Background and foreground colors
        can be set using the user-defined values in the RTK configuration file.

        :return: _scrollwindow
        :rtype: gtk.ScrolledWindow
        """

        self.treeview.set_tooltip_text(_(u"Displays an indented list (tree) "
                                         u"of program requirements."))
        self.treeview.set_enable_tree_lines(True)
        self.treeview.connect('cursor_changed', self._treeview_row_changed,
                              None, None)
        self.treeview.connect('row_activated', self._treeview_row_changed)

        # Connect the cells to the callback function.
        for i in [3, 11, 12, 13]:
            _cell = self.treeview.get_column(
                self._lst_col_order[i]).get_cell_renderers()
            _cell[0].connect('edited', self._requirement_tree_edit, i,
                             self.treeview.get_model())

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)

        return _scrollwindow

    def _create_toolbar(self):
        """
        Method to create the toolbar for the Requirement class work book.

        :return: _toolbar
        :rtype: gtk.ToolBar
        """

        _toolbar = gtk.Toolbar()

        _position = 0

        # Add sibling requirement button.
        self.btnAddSibling.set_tooltip_text(_(u"Adds a new requirement at the "
                                              u"same level as the selected "
                                              u"requirement."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_sibling.png')
        self.btnAddSibling.set_icon_widget(_image)
        self.btnAddSibling.connect('clicked', self._add_requirement, 0)
        _toolbar.insert(self.btnAddSibling, _position)
        _position += 1

        # Add child (derived) requirement button.
        self.btnAddChild.set_tooltip_text(_(u"Adds a new requirement "
                                            u"subordinate to the selected "
                                            u"requirement."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/insert_child.png')
        self.btnAddChild.set_icon_widget(_image)
        self.btnAddChild.connect('clicked', self._add_requirement, 1)
        _toolbar.insert(self.btnAddChild, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Add button.
        self.btnAdd.set_name('Add')
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/add.png')
        self.btnAdd.set_icon_widget(_image)
        self.btnAdd.connect('clicked', self._toolbutton_pressed)
        _toolbar.insert(self.btnAdd, _position)
        _position += 1

        # Remove button.
        self.btnRemove.set_name('Remove')
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/remove.png')
        self.btnRemove.set_icon_widget(_image)
        self.btnRemove.connect('clicked', self._toolbutton_pressed)
        _toolbar.insert(self.btnRemove, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Create report button.
        _button = gtk.MenuToolButton(None, label="")
        _button.set_tooltip_text(_(u"Create Requirement reports."))
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/reports.png')
        _button.set_icon_widget(_image)
        _menu = gtk.Menu()
        _menu_item = gtk.MenuItem(label=_(u"Stakeholder Inputs"))
        _menu_item.set_tooltip_text(_(u"Creates the stakeholder inputs report "
                                      u"for the currently selected revision."))
        _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"Requirements Listing"))
        _menu_item.set_tooltip_text(_(u"Creates the requirements listing "
                                      u"for the currently selected revision."))
        _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _menu_item = gtk.MenuItem(label=_(u"V&V Task Listing"))
        _menu_item.set_tooltip_text(_(u"Creates a report of the V&V tasks "
                                      u"for the currently selected revision "
                                      u"sorted by requirement."))
        _menu_item.connect('activate', self._create_report)
        _menu.add(_menu_item)
        _button.set_menu(_menu)
        _menu.show_all()
        _button.show()
        _toolbar.insert(_button, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Save requirement button.
        self.btnSave.set_name('Save')
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/save.png')
        self.btnSave.set_icon_widget(_image)
        self.btnSave.connect('clicked', self._toolbutton_pressed)
        _toolbar.insert(self.btnSave, _position)
        _position += 1

        _toolbar.insert(gtk.SeparatorToolItem(), _position)
        _position += 1

        # Assign existing V&V task button
        self.btnAssign.set_tooltip_text(_(u"Assigns an existing Verification "
                                          u"and Validation (V&V) task to the "
                                          u"selected requirement."))
        self.btnAssign.set_name('Assign')
        _image = gtk.Image()
        _image.set_from_file(_conf.ICON_DIR + '32x32/assign.png')
        self.btnAssign.set_icon_widget(_image)
        self.btnAssign.connect('clicked', self._toolbutton_pressed)
        _toolbar.insert(self.btnAssign, _position)
        _position += 1

        self.cmbVandVTasks.set_tooltip_text(_(u"List of existing V&V "
                                              u"activities available to "
                                              u"assign to a requirement."))
        _alignment = gtk.Alignment(xalign=0.5, yalign=0.5)
        _alignment.add(self.cmbVandVTasks)
        _toolitem = gtk.ToolItem()
        _toolitem.add(_alignment)
        _toolbar.insert(_toolitem, _position)

        _toolbar.show()

        # Hide the toolbar items associated with the V&V tab.
        self.btnAdd.hide()
        self.btnAssign.hide()
        self.cmbVandVTasks.hide()

        return _toolbar

    def _create_notebook(self):
        """
        Method to create the Requirement class gtk.Notebook().
        """

        def _create_stakeholder_input_tab(self, notebook):
            """
            Function to create the Stakeholder Input gtk.Notebook tab and
            populate it with the appropriate widgets.

            :param rtk.Requirement self: the current instance of a Requirement
                                         class.
            :param gtk.Notebook notebook: the gtk.Notebook() to add the
                                          stakeholder inputs page.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _scwStakeholder = gtk.ScrolledWindow()
            _scwStakeholder.set_policy(gtk.POLICY_AUTOMATIC,
                                       gtk.POLICY_AUTOMATIC)
            _scwStakeholder.add(self.tvwStakeholderInput)

            _fraStakeholder = _widg.make_frame(label=_(u"Stakeholder Inputs"))
            _fraStakeholder.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraStakeholder.add(_scwStakeholder)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display stakeholder input           #
            # information.                                                  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Set the has-entry property for stakeholder and affinity group
            # gtk.CellRendererCombo cells.  Connect the edited signal to the
            # callback function that updates the model to include the new
            # entry that is manually entered by the user.
            _cell = self.tvwStakeholderInput.get_column(
                self._lst_stakeholder_col_order[1]).get_cell_renderers()
            _cell[0].set_property('has-entry', True)
            _cell[0].connect('edited', _add_to_combo)

            _cell = self.tvwStakeholderInput.get_column(
                self._lst_stakeholder_col_order[3]).get_cell_renderers()
            _cell[0].set_property('has-entry', True)
            _cell[0].connect('edited', _add_to_combo)

            for i in range(4, 9):
                _cell = self.tvwStakeholderInput.get_column(
                    self._lst_stakeholder_col_order[i]).get_cell_renderers()
                _cell[0].set_alignment(xalign=0.5, yalign=0.5)

            # Set the priority, customer rating, and planned rating
            # gtk.CellRendererSpin to integer spins with increments of 1.
            # Make it an integer spin by setting the number of digits to 0.
            for i in range(4, 7):
                _cell = self.tvwStakeholderInput.get_column(
                    self._lst_stakeholder_col_order[i]).get_cell_renderers()
                _adjustment = _cell[0].get_property('adjustment')
                _adjustment.set_step_increment(1)
                _cell[0].set_property('adjustment', _adjustment)
                _cell[0].set_property('digits', 0)

            # Insert the tab.
            label = gtk.Label()
            label.set_markup("<span weight='bold'>" +
                             _(u"Stakeholder\nInputs") +
                             "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_tooltip_text(_(u"Displays stakeholder inputs."))
            label.show_all()
            notebook.insert_page(_fraStakeholder,
                                 tab_label=label,
                                 position=-1)

            return False

        def _create_general_data_tab(self, notebook):
            """
            Function to create the Requirement class gtk.Notebook() page for
            displaying general data about the selected Requirement.

            :param rtk.Requirement self: the current instance of a Requirement
                                         class.
            :param gtk.Notebook notebook: the gtk.Notebook() to add the general
                                          data tab.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _fxdGeneralData = gtk.Fixed()

            _fraGeneralData = _widg.make_frame(label=_(u"General Information"))
            _fraGeneralData.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraGeneralData.add(_fxdGeneralData)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display general information.        #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Load the gtk.ComboBox in the Work Book, the gtk.CellRendererCombo
            # in the Tree Book, and the local dictionary with the list of
            # requirement types.  The dictionary uses the noun name of the
            # requirement type as the key and the index in the gtk.ComboBox as
            # the value.
            _query_ = "SELECT fld_requirement_type_desc, \
                              fld_requirement_type_code, \
                              fld_requirement_type_id \
                       FROM tbl_requirement_type"
            _results_ = self._app.COMDB.execute_query(_query_,
                                                      None,
                                                      self._app.ComCnx)
            _widg.load_combo(self.cmbRqmtType, _results_, False)
            _cell_ = self.treeview.get_column(
                self._lst_stakeholder_col_order[4]).get_cell_renderers()
            _cell_model_ = _cell_[0].get_property('model')
            _cell_model_.clear()
            for i in range(len(_results_)):
                _cell_model_.append([_results_[i][0]])
                self._dic_owners[_results_[i][0]] = i + 1

            # Load the gtk.ComboBox in the Work Book, the gtk.CellRendererCombo
            # in the Tree Book, and the local dictionary with the list of
            # groups.  The dictionary uses the noun name of the group as the
            # key and the index in the gtk.ComboBox as the value.
            _query = "SELECT fld_group_name, fld_group_id FROM tbl_groups"
            _results = self._app.COMDB.execute_query(_query, None,
                                                     self._app.ComCnx)
            _model = self.cmbOwner.get_model()
            _cell = self.treeview.get_column(
                self._lst_col_order[10]).get_cell_renderers()
            _cell_model = _cell[0].get_property('model')
            _model.clear()
            _cell_model.clear()
            _model.append(None, ["", "", ""])
            _cell_model.append([""])
            for i in range(len(_results)):
                _data = [_results[i][0], str(_results[i][1]), '']
                _model.append(None, _data)
                _cell_model.append([_results[i][0]])
                self._dic_owners[_results[i][0]] = i + 1

            # Load the priority gtk.Combo().
            _results = [['1'], ['2'], ['3'], ['4'], ['5']]
            _widg.load_combo(self.cmbPriority, _results)

            _labels = [_(u"Requirement ID:"), _(u"Requirement:"),
                       _(u"Requirement Type:"), _(u"Specification:"),
                       _(u"Page Number:"), _(u"Figure Number:"),
                       _(u"Derived:"), _(u"Validated:"), _(u"Owner:"),
                       _(u"Priority:"), _(u"Validated Date:")]
            _max1 = 0
            _max2 = 0
            (_max1, _y_pos) = _widg.make_labels(_labels[2:10],
                                                _fxdGeneralData, 5, 140)
            _x_pos = max(_max1, _max2) + 20

            # Create the tooltips.
            self.txtCode.set_tooltip_text(_(u"Displays the unique code for "
                                            u"the selected requirement."))
            self.cmbRqmtType.set_tooltip_text(_(u"Selects and displays the "
                                                u"type of requirement for the "
                                                u"selected requirement."))
            self.txtSpecification.set_tooltip_text(_(u"Displays the internal "
                                                     u"or industry "
                                                     u"specification "
                                                     u"associated with the "
                                                     u"selected requirement."))
            self.txtPageNumber.set_tooltip_text(_(u"Displays the "
                                                  u"specification page number "
                                                  u"associated with the "
                                                  u"selected requirement."))
            self.txtFigureNumber.set_tooltip_text(_(u"Displays the "
                                                    u"specification figure "
                                                    u"number associated with "
                                                    u"the selected "
                                                    u"requirement."))
            self.chkDerived.set_tooltip_text(_(u"Whether or not the selected "
                                               u"requirement is derived."))
            self.chkValidated.set_tooltip_text(_(u"Whether or not the "
                                                 u"selected requirement has "
                                                 u"been verified and "
                                                 u"validated."))
            self.txtValidatedDate.set_tooltip_text(_(u"Displays the date the "
                                                     u"selected requirement "
                                                     u"was verified and "
                                                     u"validated."))
            self.btnValidateDate.set_tooltip_text(_(u"Launches the calendar "
                                                    u"to select the date the "
                                                    u"requirement was "
                                                    u"validated."))
            self.cmbOwner.set_tooltip_text(_(u"Displays the responsible "
                                             u"organization or individual for "
                                             u"the selected requirement."))
            self.cmbPriority.set_tooltip_text(_(u"Selects and displays the "
                                                u"priority of the selected "
                                                u"requirement."))

            # Place the widgets.
            label = _widg.make_label(_labels[0], 150, 25)
            _fxdGeneralData.put(label, 5, 5)
            _fxdGeneralData.put(self.txtCode, _x_pos, 5)

            label = _widg.make_label(_labels[1], 150, 25)
            _fxdGeneralData.put(label, 5, 35)

            _fxdGeneralData.put(self.cmbRqmtType, _x_pos, _y_pos[0])
            _fxdGeneralData.put(self.txtSpecification, _x_pos, _y_pos[1])
            _fxdGeneralData.put(self.txtPageNumber, _x_pos, _y_pos[2])
            _fxdGeneralData.put(self.txtFigureNumber, _x_pos, _y_pos[3])
            _fxdGeneralData.put(self.chkDerived, _x_pos, _y_pos[4])
            _fxdGeneralData.put(self.chkValidated, _x_pos, _y_pos[5])

            _label = _widg.make_label(_labels[10], 150, 25)
            _fxdGeneralData.put(_label, _x_pos + 25, _y_pos[5])

            _fxdGeneralData.put(self.txtValidatedDate, _x_pos + 200, _y_pos[5])
            _fxdGeneralData.put(self.btnValidateDate, _x_pos + 305, _y_pos[5])
            _fxdGeneralData.put(self.cmbOwner, _x_pos, _y_pos[6])
            _fxdGeneralData.put(self.cmbPriority, _x_pos, _y_pos[7])

            # Connect to callback functions.
            self.txtCode.connect('focus-out-event',
                                 self._callback_entry, 'text', 5)

            _textview = _widg.make_text_view(txvbuffer=self.txtRequirement,
                                             width=400)
            _textview.set_tooltip_text(_(u"Detailed description of the "
                                         u"requirement."))
            _fxdGeneralData.put(_textview, _x_pos, 35)
            _widget = _textview.get_children()[0].get_children()[0]
            self._lst_handler_id.append(
                _widget.connect('focus-out-event', self._callback_entry,
                                'text', 3))

            self.cmbRqmtType.connect('changed', self._callback_combo, 4)
            self._lst_handler_id.append(
                self.txtSpecification.connect('focus-out-event',
                                              self._callback_entry,
                                              'text', 11))
            self._lst_handler_id.append(
                self.txtPageNumber.connect('focus-out-event',
                                           self._callback_entry, 'text', 12))
            self._lst_handler_id.append(
                self.txtFigureNumber.connect('focus-out-event',
                                             self._callback_entry, 'text', 13))

            self.chkDerived.connect('toggled', self._callback_check, 6)
            self.chkValidated.connect('toggled', self._callback_check, 8)
            self.txtValidatedDate.connect('focus-out-event',
                                          self._callback_entry, 'text', 9)
            self.btnValidateDate.connect('button-release-event',
                                         _util.date_select,
                                         self.txtValidatedDate)
            self.cmbOwner.connect('changed', self._callback_combo, 10)
            self.cmbPriority.connect('changed', self._callback_combo, 52)

            _fxdGeneralData.show_all()

            # Insert the tab.
            label = gtk.Label()
            label.set_markup("<span weight='bold'>" +
                             _(u"General\nData") +
                             "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_tooltip_text(_(u"Displays general information about the "
                                     u"selected requirement."))
            label.show_all()
            notebook.insert_page(_fraGeneralData,
                                 tab_label=label,
                                 position=-1)

            return False

        def _create_analysis_tab(self, notebook):
            """
            Function to the create the tab for analyzing the selected
            requirement.

            :param rtk.Requirement self: the current instance of a Requirement
                                         class.
            :param gtk.Notebook notebook: the gtk.Notebook() to add the
                                          analysis tab.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _hpnAnalysis_ = gtk.HPaned()

            # Create quadrant #1 (upper left) for determining if the
            # requirement is clear.
            _vpnLeft_ = gtk.VPaned()
            _hpnAnalysis_.pack1(_vpnLeft_, resize=False)

            _fxdClear_ = gtk.Fixed()

            _scwClear_ = gtk.ScrolledWindow()
            _scwClear_.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            _scwClear_.add_with_viewport(_fxdClear_)

            _fraClear_ = _widg.make_frame(label=_(u"Clarity of Requirement"))
            _fraClear_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraClear_.add(_scwClear_)

            _vpnLeft_.pack1(_fraClear_, resize=False)

            # Create quadrant #3 (lower left) for determining if the
            # requirement is complete.
            _fxdComplete_ = gtk.Fixed()

            _scwComplete_ = gtk.ScrolledWindow()
            _scwComplete_.set_policy(gtk.POLICY_AUTOMATIC,
                                     gtk.POLICY_AUTOMATIC)
            _scwComplete_.add_with_viewport(_fxdComplete_)

            _fraComplete_ = _widg.make_frame(label=_(u"Completeness of "
                                                     u"Requirement"))
            _fraComplete_.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraComplete_.add(_scwComplete_)

            _vpnLeft_.pack2(_fraComplete_, resize=False)

            # Create quadrant #2 (upper right) for determining if the
            # requirement is consistent.
            _vpnRight_ = gtk.VPaned()
            _hpnAnalysis_.pack2(_vpnRight_, resize=False)

            _fxdConsistent_ = gtk.Fixed()

            _scwConsistent_ = gtk.ScrolledWindow()
            _scwConsistent_.set_policy(gtk.POLICY_AUTOMATIC,
                                       gtk.POLICY_AUTOMATIC)
            _scwConsistent_.add_with_viewport(_fxdConsistent_)

            _fraConsistent_ = _widg.make_frame(label=_(u"Consistency of "
                                                       u"Requirement"))
            _fraConsistent_.set_shadow_type(gtk.SHADOW_NONE)
            _fraConsistent_.add(_scwConsistent_)

            _vpnRight_.pack1(_fraConsistent_, resize=False)

            # Create quadrant #4 (lower right) for determining if the
            # requirement is verifiable.
            _fxdVerifiable_ = gtk.Fixed()

            _scwVerifiable_ = gtk.ScrolledWindow()
            _scwVerifiable_.set_policy(gtk.POLICY_AUTOMATIC,
                                       gtk.POLICY_AUTOMATIC)
            _scwVerifiable_.add_with_viewport(_fxdVerifiable_)

            _fraVerifiable_ = _widg.make_frame(label=_(u"Verifiability of "
                                                       u"Requirement"))
            _fraVerifiable_.set_shadow_type(gtk.SHADOW_NONE)
            _fraVerifiable_.add(_scwVerifiable_)

            _vpnRight_.pack2(_fraVerifiable_, resize=False)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display requirements analysis       #
            # information.                                                  #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Create the labels for quadrant #1.
            _labels = [_(u"The requirement clearly states what is needed or "
                         u"desired."),
                       _(u"The requirement is unambiguous and not open to "
                         u"interpretation."),
                       _(u"All terms that can have more than one meaning are "
                         u"qualified so that the desired meaning is readily "
                         u"apparent."),
                       _(u"Diagrams, drawings, etc. are used to increase "
                         u"understanding of the requirement."),
                       _(u"The requirement is free from spelling and "
                         u"grammatical errors."),
                       _(u"The requirement is written in non-technical "
                         u"language using the vocabulary of the stakeholder."),
                       _(u"Stakeholders understand the requirement as "
                         u"written."),
                       _(u"The requirement is clear enough to be turned over "
                         u"to an independent group and still be understood."),
                       _(u"The requirement avoids stating how the problem is "
                         u"to be solved or what techniques are to be used.")]

            (_max1_, _y_pos1_) = _widg.make_labels(_labels, _fxdClear_, 5, 5)

            # Create the labels for quadrant #3.
            _labels = [_(u"Performance objectives are properly documented "
                         u"from the user's point of view."),
                       _(u"No necessary information is missing from the "
                         u"requirement."),
                       _(u"The requirement has been assigned a priority."),
                       _(u"The requirement is realistic given the technology "
                         u"that will used to implement the system."),
                       _(u"The requirement is feasible to implement given the "
                         u"defined project time frame, scope, structure and "
                         u"budget."),
                       _(u"If the requirement describes something as a "
                         u"'standard' the specific source is cited."),
                       _(u"The requirement is relevant to the problem and its "
                         u"solution."),
                       _(u"The requirement contains no implied design "
                         u"details."),
                       _(u"The requirement contains no implied implementation "
                         u"constraints."),
                       _(u"The requirement contains no implied project "
                         u"management constraints.")]

            (_max2_,
             _y_pos2_) = _widg.make_labels(_labels, _fxdComplete_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 50

            # Place the quadrant 1 widgets.
            self.chkClearQ1.connect('toggled', self._callback_check, 16)
            _fxdClear_.put(self.chkClearQ1, _x_pos_, _y_pos1_[0])

            self.chkClearQ2.connect('toggled', self._callback_check, 17)
            _fxdClear_.put(self.chkClearQ2, _x_pos_, _y_pos1_[1])

            self.chkClearQ3.connect('toggled', self._callback_check, 18)
            _fxdClear_.put(self.chkClearQ3, _x_pos_, _y_pos1_[2])

            self.chkClearQ4.connect('toggled', self._callback_check, 19)
            _fxdClear_.put(self.chkClearQ4, _x_pos_, _y_pos1_[3])

            self.chkClearQ5.connect('toggled', self._callback_check, 20)
            _fxdClear_.put(self.chkClearQ5, _x_pos_, _y_pos1_[4])

            self.chkClearQ6.connect('toggled', self._callback_check, 21)
            _fxdClear_.put(self.chkClearQ6, _x_pos_, _y_pos1_[5])

            self.chkClearQ7.connect('toggled', self._callback_check, 22)
            _fxdClear_.put(self.chkClearQ7, _x_pos_, _y_pos1_[6])

            self.chkClearQ8.connect('toggled', self._callback_check, 23)
            _fxdClear_.put(self.chkClearQ8, _x_pos_, _y_pos1_[7])

            self.chkClearQ9.connect('toggled', self._callback_check, 24)
            _fxdClear_.put(self.chkClearQ9, _x_pos_, _y_pos1_[8])

            # self.chkClearQ10.connect('toggled', self._callback_check, 25)

            # Place the quadrant 3 widgets.
            self.chkCompleteQ1.connect('toggled', self._callback_check, 26)
            _fxdComplete_.put(self.chkCompleteQ1, _x_pos_, _y_pos2_[0])

            self.chkCompleteQ2.connect('toggled', self._callback_check, 27)
            _fxdComplete_.put(self.chkCompleteQ2, _x_pos_, _y_pos2_[1])

            self.chkCompleteQ3.connect('toggled', self._callback_check, 28)
            _fxdComplete_.put(self.chkCompleteQ3, _x_pos_, _y_pos2_[2])

            self.chkCompleteQ4.connect('toggled', self._callback_check, 29)
            _fxdComplete_.put(self.chkCompleteQ4, _x_pos_, _y_pos2_[3])

            self.chkCompleteQ5.connect('toggled', self._callback_check, 30)
            _fxdComplete_.put(self.chkCompleteQ5, _x_pos_, _y_pos2_[4])

            self.chkCompleteQ6.connect('toggled', self._callback_check, 31)
            _fxdComplete_.put(self.chkCompleteQ6, _x_pos_, _y_pos2_[5])

            self.chkCompleteQ7.connect('toggled', self._callback_check, 32)
            _fxdComplete_.put(self.chkCompleteQ7, _x_pos_, _y_pos2_[6])

            self.chkCompleteQ8.connect('toggled', self._callback_check, 33)
            _fxdComplete_.put(self.chkCompleteQ8, _x_pos_, _y_pos2_[7])

            self.chkCompleteQ9.connect('toggled', self._callback_check, 34)
            _fxdComplete_.put(self.chkCompleteQ9, _x_pos_, _y_pos2_[8])

            self.chkCompleteQ10.connect('toggled', self._callback_check, 35)
            _fxdComplete_.put(self.chkCompleteQ10, _x_pos_, _y_pos2_[9])

            # Create the labels for quadrant #2.
            _labels = [_(u"The requirement describes a single need or want; "
                         u"it could not be broken into several different "
                         u"requirements."),
                       _(u"The requirement requires non-standard hardware or "
                         u"must use software to implement."),
                       _(u"The requirement can be implemented within known "
                         u"constraints."),
                       _(u"The requirement provides an adequate basis for "
                         u"design and testing."),
                       _(u"The requirement adequately supports the business "
                         u"goal of the project."),
                       _(u"The requirement does not conflict with some "
                         u"constraint, policy or regulation."),
                       _(u"The requirement does not conflict with another "
                         u"requirement."),
                       _(u"The requirement is not a duplicate of another "
                         u"requirement."),
                       _(u"The requirement is in scope for the project.")]

            (_max1_, _y_pos1_) = _widg.make_labels(_labels,
                                                   _fxdConsistent_, 5, 5)

            # Create the labels for quadrant #4.
            _labels = [_(u"The requirement is verifiable by testing, "
                         u"demonstration, review, or analysis."),
                       _(u"The requirement lacks 'weasel words' (e.g. "
                         u"various, mostly, suitable, integrate, maybe, "
                         u"consistent, robust, modular, user-friendly, "
                         u"superb, good)."),
                       _(u"Any performance criteria are quantified such that "
                         u"they are testable."),
                       _(u"Independent testing would be able to determine "
                         u"whether the requirement has been satisfied."),
                       _(u"The task(s) that will validate and verify the "
                         u"final design satisfies the requirement have been "
                         u"identified."),
                       _(u"The identified V&amp;V task(s) have been added to "
                         u"the validation plan (e.g., DVP)")]

            (_max2_, _y_pos2_) = _widg.make_labels(_labels,
                                                   _fxdVerifiable_, 5, 5)
            _x_pos_ = max(_max1_, _max2_) + 50

            # Place the quadrant #2 widgets.
            self.chkConsistentQ1.connect('toggled', self._callback_check, 36)
            _fxdConsistent_.put(self.chkConsistentQ1, _x_pos_, _y_pos1_[0])

            self.chkConsistentQ2.connect('toggled', self._callback_check, 37)
            _fxdConsistent_.put(self.chkConsistentQ2, _x_pos_, _y_pos1_[1])

            self.chkConsistentQ3.connect('toggled', self._callback_check, 38)
            _fxdConsistent_.put(self.chkConsistentQ3, _x_pos_, _y_pos1_[2])

            self.chkConsistentQ4.connect('toggled', self._callback_check, 39)
            _fxdConsistent_.put(self.chkConsistentQ4, _x_pos_, _y_pos1_[3])

            self.chkConsistentQ5.connect('toggled', self._callback_check, 40)
            _fxdConsistent_.put(self.chkConsistentQ5, _x_pos_, _y_pos1_[4])

            self.chkConsistentQ6.connect('toggled', self._callback_check, 41)
            _fxdConsistent_.put(self.chkConsistentQ6, _x_pos_, _y_pos1_[5])

            self.chkConsistentQ7.connect('toggled', self._callback_check, 42)
            _fxdConsistent_.put(self.chkConsistentQ7, _x_pos_, _y_pos1_[6])

            self.chkConsistentQ8.connect('toggled', self._callback_check, 43)
            _fxdConsistent_.put(self.chkConsistentQ8, _x_pos_, _y_pos1_[7])

            self.chkConsistentQ9.connect('toggled', self._callback_check, 44)
            _fxdConsistent_.put(self.chkConsistentQ9, _x_pos_, _y_pos1_[8])

            # self.chkConsistentQ10.connect('toggled', self._callback_check, 45)

            # Place the quadrant #4 widgets.
            self.chkVerifiableQ1.connect('toggled', self._callback_check, 46)
            _fxdVerifiable_.put(self.chkVerifiableQ1, _x_pos_, _y_pos2_[0])

            self.chkVerifiableQ2.connect('toggled', self._callback_check, 47)
            _fxdVerifiable_.put(self.chkVerifiableQ2, _x_pos_, _y_pos2_[1])

            self.chkVerifiableQ3.connect('toggled', self._callback_check, 48)
            _fxdVerifiable_.put(self.chkVerifiableQ3, _x_pos_, _y_pos2_[2])

            self.chkVerifiableQ4.connect('toggled', self._callback_check, 49)
            _fxdVerifiable_.put(self.chkVerifiableQ4, _x_pos_, _y_pos2_[3])

            self.chkVerifiableQ5.connect('toggled', self._callback_check, 50)
            _fxdVerifiable_.put(self.chkVerifiableQ5, _x_pos_, _y_pos2_[4])

            self.chkVerifiableQ6.connect('toggled', self._callback_check, 51)
            _fxdVerifiable_.put(self.chkVerifiableQ6, _x_pos_, _y_pos2_[5])

            # Insert the tab.
            _label_ = gtk.Label()
            _label_.set_markup("<span weight='bold'>" +
                               _(u"Analysis") +
                               "</span>")
            _label_.set_alignment(xalign=0.5, yalign=0.5)
            _label_.set_justify(gtk.JUSTIFY_CENTER)
            _label_.set_tooltip_text(_(u"Analyzes the selected requirement."))
            _label_.show_all()
            notebook.insert_page(_hpnAnalysis_,
                                 tab_label=_label_,
                                 position=-1)

            return False

        def _create_vandv_tab(self, notebook):
            """
            Function to create the Verification and Validation Plan
            gtk.Notebook() tab and populate it with the appropriate widgets.

            :param rtk.Requirement self: the current instance of a Requirement
                                         class.
            :param gtk.Notebook notebook: the gtk.Notebook() to add the V & V
                                          task page.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Build-up the containers for the tab.                          #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _scwVandV = gtk.ScrolledWindow()
            _scwVandV.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            _scwVandV.add_with_viewport(self.tvwValidation)

            _fraVandV = _widg.make_frame(_(u"Verification and Validation Task "
                                           u"List"))
            _fraVandV.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
            _fraVandV.add(_scwVandV)

            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            # Place the widgets used to display V&V task information.       #
            # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
            _labels = [_(u"Task ID"), _(u"Task Description"),
                       _(u"Start Date"), _(u"Due Date"), _(u"% Complete")]
            _model_ = gtk.TreeStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                                    gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_FLOAT)
            self.tvwValidation.set_model(_model_)
            self.tvwValidation.set_tooltip_text(_(u"Provides read-only list "
                                                  u"of basic information for "
                                                  u"Verification and "
                                                  u"Validation (V&V) tasks "
                                                  u"associated with the "
                                                  u"selected Requirement."))

            for i in range(len(_labels)):
                _cell = gtk.CellRendererText()
                _label = gtk.Label()
                _label.set_alignment(xalign=0.5, yalign=0.5)
                _label.set_justify(gtk.JUSTIFY_CENTER)
                _label.set_line_wrap(True)
                _label.set_markup("<span weight='bold'>" +
                                  _labels[i] + "</span>")
                _label.set_use_markup(True)
                _label.show_all()

                _column = gtk.TreeViewColumn()
                _column.set_resizable(True)
                _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
                _column.set_visible(1)
                _column.set_widget(_label)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i)

                if i == 1:
                    _cell.set_property('editable', 1)
                    _cell.connect('edited', _vandv_tree_edit, i,
                                  self.tvwValidation.get_model())
                else:
                    _cell.set_property('editable', 0)
                    _cell.set_property('cell-background', '#BFBFBF')

                self.tvwValidation.append_column(_column)

            # Insert the tab.
            label = gtk.Label()
            label.set_markup("<span weight='bold'>" +
                             _(u"V &amp; V Tasks") +
                             "</span>")
            label.set_alignment(xalign=0.5, yalign=0.5)
            label.set_justify(gtk.JUSTIFY_CENTER)
            label.set_tooltip_text(_(u"Displays the list of V&V tasks for the "
                                     u"selected requirement."))
            label.show_all()
            notebook.insert_page(_fraVandV, tab_label=label, position=-1)

            return False

        _notebook_ = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if _conf.TABPOS[2] == 'left':
            _notebook_.set_tab_pos(gtk.POS_LEFT)
        elif _conf.TABPOS[2] == 'right':
            _notebook_.set_tab_pos(gtk.POS_RIGHT)
        elif _conf.TABPOS[2] == 'top':
            _notebook_.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook_.set_tab_pos(gtk.POS_BOTTOM)

        _create_stakeholder_input_tab(self, _notebook_)
        _create_general_data_tab(self, _notebook_)
        _create_analysis_tab(self, _notebook_)
        _create_vandv_tab(self, _notebook_)

        return _notebook_

    def load_tree(self):
        """
        Method to load the Requirement class gtk.TreeView().

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Select everything from the requirements table.
        _query = "SELECT * FROM tbl_requirements \
                  WHERE fld_revision_id=%d \
                  ORDER BY fld_requirement_id" % \
                 self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        try:
            _n_requirements = len(_results)
        except TypeError:
            _n_requirements = 0

        _model = self.treeview.get_model()
        _model.clear()
        for i in range(_n_requirements):
            if _results[i][self._lst_col_order[7]] == '-':
                _piter = None
            else:
                _piter = _model.get_iter_from_string(
                    _results[i][self._lst_col_order[7]])

            _model.append(_piter, _results[i])

        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)

        _root = _model.get_iter_root()
        if _root is not None:
            _path = _model.get_path(_root)
            _col = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _col)

        return False

    def _load_stakeholder_inputs(self):
        """
        Method to load the stakeholder input tab.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Load the stakeholder gtk.CellRendererCombo with a list of
        # distinct stakeholders already entered into the database.
        _query = "SELECT DISTINCT fld_stakeholder \
                  FROM tbl_stakeholder_input \
                  ORDER BY fld_stakeholder ASC"
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        try:
            _n_stakeholders = len(_results)
        except TypeError:
            _n_stakeholders = 0

        _cell = self.tvwStakeholderInput.get_column(
            self._lst_stakeholder_col_order[1]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        for i in range(_n_stakeholders):
            _model.append([_results[i][0]])

        # Load the stakeholder gtk.CellRendererCombo with a list of distinct
        # affinity groups already entered into the database.
        _query_ = "SELECT DISTINCT fld_group \
                   FROM tbl_stakeholder_input \
                   ORDER BY fld_group ASC"
        _results_ = self._app.DB.execute_query(_query_,
                                               None,
                                               self._app.ProgCnx)
        try:
            _n_groups_ = len(_results_)
        except TypeError:
            _n_groups_ = 0

        _cell_ = self.tvwStakeholderInput.get_column(
            self._lst_stakeholder_col_order[3]).get_cell_renderers()
        _model_ = _cell_[0].get_property('model')
        _model_.clear()
        for i in range(_n_groups_):
            _model_.append([_results_[i][0]])

        # Load the stakeholder gtk.CellRendererCombo with a list of existing
        # requirement codes in the database.
        _query = "SELECT fld_requirement_code, fld_requirement_desc \
                   FROM tbl_requirements \
                   WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        try:
            _n_requirements = len(_results)
        except TypeError:
            _n_requirements = 0

        _cell = self.tvwStakeholderInput.get_column(
            self._lst_stakeholder_col_order[9]).get_cell_renderers()
        _model = _cell[0].get_property('model')
        _model.clear()
        for i in range(_n_requirements):
            _model.append([_results[i][0] + ' - ' + _results[i][1]])

        # Now load the Stakeholder Inputs gtk.TreeView.
        _query = "SELECT fld_input_id, fld_stakeholder, fld_description, \
                         fld_group, fld_priority, fld_customer_rank, \
                         fld_planned_rank, fld_improvement, \
                         fld_overall_weight, fld_requirement_code, \
                         fld_user_float_1, fld_user_float_2, \
                         fld_user_float_3, fld_user_float_4, \
                         fld_user_float_5 \
                  FROM tbl_stakeholder_input \
                  WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query,
                                              None,
                                              self._app.ProgCnx)
        try:
            _n_inputs = len(_results)
        except TypeError:
            _n_inputs = 0

        _model = self.tvwStakeholderInput.get_model()
        _model.clear()
        for i in range(_n_inputs):
            _model.append(None, _results[i])

        return False

    def _load_vandv_tasks(self):
        """
        Method to load the Requirement/Validation task relationship
        matrix.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model, _row) = self.treeview.get_selection().get_selected()

        _query = "SELECT t1.fld_validation_id, t1.fld_task_desc, \
                         t1.fld_start_date, t1.fld_end_date, t1.fld_status \
                  FROM tbl_validation AS t1 \
                  INNER JOIN tbl_validation_matrix AS t2 \
                  ON t2.fld_validation_id=t1.fld_validation_id \
                  WHERE t1.fld_revision_id=%d \
                  AND t2.fld_requirement_id=%d \
                  GROUP BY t1.fld_validation_id" % \
                 (_model.get_value(_row, self._lst_col_order[0]),
                  _model.get_value(_row, self._lst_col_order[1]))
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        try:
            _n_tasks = len(_results)
        except TypeError:
            _n_tasks = 0

        _model = self.tvwValidation.get_model()
        _model.clear()
        for i in range(_n_tasks):
            _model.append(None, [_results[i][0], _results[i][1],
                                 _util.ordinal_to_date(_results[i][2]),
                                 _util.ordinal_to_date(_results[i][3]),
                                 _results[i][4]])

        _root = _model.get_iter_root()
        if _root is not None:
            _path = _model.get_path(_root)
            self.tvwValidation.expand_all()
            self.tvwValidation.set_cursor('0', None, False)
            _col = self.tvwValidation.get_column(0)
            self.tvwValidation.row_activated(_path, _col)

        # Load the list of V&V task to the gtk.ComboBox used to associate
        # existing V&V tasks with requirements.
        _query = "SELECT DISTINCT(fld_validation_id), fld_task_desc, \
                         fld_task_type \
                  FROM tbl_validation \
                  WHERE fld_revision_id=%d" % self._app.REVISION.revision_id
        _results = self._app.DB.execute_query(_query, None, self._app.ProgCnx)

        try:
            _n_tasks = len(_results)
        except TypeError:
            _n_tasks = 0

        _tasks = []
        for i in range(_n_tasks):
            _tasks.append((_results[i][1], _results[i][0], _results[i][2]))

        _widg.load_combo(self.cmbVandVTasks, _tasks, simple=False)

        return False

    def load_notebook(self):
        """
        Method to load the Requirement class gtk.Notebook().

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _load_general_data_tab(self):
            """
            Function to load the widgets on the General Data tab.

            :param rtk.Requirement self: the current instance of a Requirement
                                         class.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            try:
                _idx_ = int(self._dic_owners[self.owner])
            except KeyError:
                _idx_ = 0
            self.cmbOwner.set_active(_idx_)

            try:
                _idx_ = int(self._dic_owners[self.requirement_type])
            except KeyError:
                _idx_ = 0
            self.cmbRqmtType.set_active(_idx_)

            self.chkDerived.set_active(self.derived)
            self.chkValidated.set_active(self.validated)

            self.txtCode.set_text(self.requirement_code)
            self.txtFigureNumber.set_text(self.figure_number)
            self.txtPageNumber.set_text(self.page_number)
            self.txtRequirement.set_text(self.requirement_desc)
            self.txtSpecification.set_text(self.specification)
            self.txtValidatedDate.set_text(self.validated_date)
            self.cmbPriority.set_active(self.priority)

            return False

        def _load_analysis_tab(self):
            """
            Function to load the Requirements Analysis tab widgets with the
            values from the RTK Program database.

            :param rtk.Requirement self: the current instance of a Requirement
                                         class.
            :return: False if successful and True if an error is encountered.
            :rtype: boolean
            """

            self.chkClearQ1.set_active(self.clear_q1)
            self.chkClearQ2.set_active(self.clear_q2)
            self.chkClearQ3.set_active(self.clear_q3)
            self.chkClearQ4.set_active(self.clear_q4)
            self.chkClearQ5.set_active(self.clear_q5)
            self.chkClearQ6.set_active(self.clear_q6)
            self.chkClearQ7.set_active(self.clear_q7)
            self.chkClearQ8.set_active(self.clear_q8)
            self.chkClearQ9.set_active(self.clear_q9)
            # self.chkClearQ10.set_active(self.clear_q10)
            self.chkCompleteQ1.set_active(self.complete_q1)
            self.chkCompleteQ2.set_active(self.complete_q2)
            self.chkCompleteQ3.set_active(self.complete_q3)
            self.chkCompleteQ4.set_active(self.complete_q4)
            self.chkCompleteQ5.set_active(self.complete_q5)
            self.chkCompleteQ6.set_active(self.complete_q6)
            self.chkCompleteQ7.set_active(self.complete_q7)
            self.chkCompleteQ8.set_active(self.complete_q8)
            self.chkCompleteQ9.set_active(self.complete_q9)
            self.chkCompleteQ10.set_active(self.complete_q10)
            self.chkConsistentQ1.set_active(self.consistent_q1)
            self.chkConsistentQ2.set_active(self.consistent_q2)
            self.chkConsistentQ3.set_active(self.consistent_q3)
            self.chkConsistentQ4.set_active(self.consistent_q4)
            self.chkConsistentQ5.set_active(self.consistent_q5)
            self.chkConsistentQ6.set_active(self.consistent_q6)
            self.chkConsistentQ7.set_active(self.consistent_q7)
            self.chkConsistentQ8.set_active(self.consistent_q8)
            self.chkConsistentQ9.set_active(self.consistent_q9)
            self.chkConsistentQ10.set_active(self.consistent_q10)
            self.chkVerifiableQ1.set_active(self.verifiable_q1)
            self.chkVerifiableQ2.set_active(self.verifiable_q2)
            self.chkVerifiableQ3.set_active(self.verifiable_q3)
            self.chkVerifiableQ4.set_active(self.verifiable_q4)
            self.chkVerifiableQ5.set_active(self.verifiable_q5)
            self.chkVerifiableQ6.set_active(self.verifiable_q6)

            return False

        if self._app.winWorkBook.get_child() is not None:
            self._app.winWorkBook.remove(self._app.winWorkBook.get_child())
        self._app.winWorkBook.add(self.vbxRequirement)
        self._app.winWorkBook.show_all()

        (__model, _row) = self.treeview.get_selection().get_selected()
        if _row is not None:
            self._load_stakeholder_inputs()
            _load_general_data_tab(self)
            _load_analysis_tab(self)
            self._load_vandv_tasks()

        self._app.winWorkBook.set_title(_(u"RTK Work Book: Requirements"))

        self.notebook.set_current_page(self._selected_tab)
        if self._selected_tab == 3:
            self.btnAdd.show()
            self.btnAssign.show()
            self.cmbVandVTasks.show()
        else:
            self.btnAdd.hide()
            self.btnAssign.hide()
            self.cmbVandVTasks.hide()

        return False

    def _treeview_clicked(self, treeview, event):
        """
        Callback function for handling mouse clicks on the Requirement
        Object treeview.

        :param gtk.TreeView treeview: the Requirements class gtk.TreeView().
        :param gtk.gdk.Event event: the gtk.gdk.Event() that called this
                                    method (the important attribute is which
                                    mouse button was clicked).
                                    * 1 = left
                                    * 2 = scrollwheel
                                    * 3 = right
                                    * 4 = forward
                                    * 5 = backward
                                    * 8 =
                                    * 9 =
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if event.button == 1:
            self._treeview_row_changed(treeview, None, 0)
        elif event.button == 3:
            print "Pop-up a menu!"

        return False

    def _treeview_row_changed(self, treeview, __path, __column):
        """
        Callback function to handle events for the Requirement class
        gtk.TreeView().  It is called whenever the Requirement class
        gtk.TreeView() is clicked or a row is activated.

        :param gtk.TreeView treeview: the Requirement class gtk.TreeView().
        :param str __path: the activated row gtk.TreeView() path.
        :param int __column: the activated column index in the Revision class
                             gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model_, _row_) = treeview.get_selection().get_selected()

        # If selecting a requirement, load everything associated
        # with the new requirement.
        if _row_ is not None:
            self.requirement_id = int(_model_.get_value(_row_, 1))
            self.assembly_id = int(_model_.get_value(_row_, 2))
            self.requirement_desc = str(_model_.get_value(_row_, 3))
            self.requirement_type = _model_.get_value(_row_, 4)
            self.requirement_code = str(_model_.get_value(_row_, 5))
            self.derived = int(_model_.get_value(_row_, 6))
            self.parent_requirement = _model_.get_value(_row_, 7)
            self.validated = int(_model_.get_value(_row_, 8))

            # Convert the ordinal validated date to a Y-m-d format.
            if _model_.get_value(_row_, 9) > 719163:
                self.validated_date = _util.ordinal_to_date(
                    _model_.get_value(_row_, 9))
            else:
                self.validated_date = ""

            self.owner = _model_.get_value(_row_, 10)
            self.specification = str(_model_.get_value(_row_, 11))
            self.page_number = str(_model_.get_value(_row_, 12))
            self.figure_number = str(_model_.get_value(_row_, 13))
            self.parent_id = _model_.get_value(_row_, 14)
            self.software_id = _model_.get_value(_row_, 15)
            self.clear_q1 = _model_.get_value(_row_, 16)
            self.clear_q2 = _model_.get_value(_row_, 17)
            self.clear_q3 = _model_.get_value(_row_, 18)
            self.clear_q4 = _model_.get_value(_row_, 19)
            self.clear_q5 = _model_.get_value(_row_, 20)
            self.clear_q6 = _model_.get_value(_row_, 21)
            self.clear_q7 = _model_.get_value(_row_, 22)
            self.clear_q8 = _model_.get_value(_row_, 23)
            self.clear_q9 = _model_.get_value(_row_, 24)
            self.clear_q10 = _model_.get_value(_row_, 25)
            self.complete_q1 = _model_.get_value(_row_, 26)
            self.complete_q2 = _model_.get_value(_row_, 27)
            self.complete_q3 = _model_.get_value(_row_, 28)
            self.complete_q4 = _model_.get_value(_row_, 29)
            self.complete_q5 = _model_.get_value(_row_, 30)
            self.complete_q6 = _model_.get_value(_row_, 31)
            self.complete_q7 = _model_.get_value(_row_, 32)
            self.complete_q8 = _model_.get_value(_row_, 33)
            self.complete_q9 = _model_.get_value(_row_, 34)
            self.complete_q10 = _model_.get_value(_row_, 35)
            self.consistent_q1 = _model_.get_value(_row_, 36)
            self.consistent_q2 = _model_.get_value(_row_, 37)
            self.consistent_q3 = _model_.get_value(_row_, 38)
            self.consistent_q4 = _model_.get_value(_row_, 39)
            self.consistent_q5 = _model_.get_value(_row_, 40)
            self.consistent_q6 = _model_.get_value(_row_, 41)
            self.consistent_q7 = _model_.get_value(_row_, 42)
            self.consistent_q8 = _model_.get_value(_row_, 43)
            self.consistent_q9 = _model_.get_value(_row_, 44)
            self.consistent_q10 = _model_.get_value(_row_, 45)
            self.verifiable_q1 = _model_.get_value(_row_, 46)
            self.verifiable_q2 = _model_.get_value(_row_, 47)
            self.verifiable_q3 = _model_.get_value(_row_, 48)
            self.verifiable_q4 = _model_.get_value(_row_, 49)
            self.verifiable_q5 = _model_.get_value(_row_, 50)
            self.verifiable_q6 = _model_.get_value(_row_, 51)
            self.priority = _model_.get_value(_row_, 52)

            self.load_notebook()

        return False

    def _requirement_tree_edit(self, __cell, path, new_text, position, model):
        """
        Method called whenever a Requirement Class gtk.Treeview()
        gtk.CellRenderer() is edited.

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

        # Now update the associated gtk.Widget() in the Work Book with the
        # new value.  We block and unblock the signal handlers for the widgets
        # so a race condition does not ensue.
        if self._lst_col_order[position] == 3:
            # _textview = self.txtRequirement.get_child().get_child()
            # _textview.handler_block(self._lst_handler_id[0])
            self.txtRequirement.set_text(str(new_text))
            # _textview.handler_unblock(self._lst_handler_id[0])
        elif self._lst_col_order[position] == 11:
            self.txtSpecification.handler_block(self._lst_handler_id[1])
            self.txtSpecification.set_text(str(new_text))
            self.txtSpecification.handler_unblock(self._lst_handler_id[1])
        elif self._lst_col_order[position] == 12:
            self.txtPageNumber.handler_block(self._lst_handler_id[2])
            self.txtPageNumber.set_text(str(new_text))
            self.txtPageNumber.handler_unblock(self._lst_handler_id[2])
        elif self._lst_col_order[position] == 13:
            self.txtFigureNumber.handler_block(self._lst_handler_id[3])
            self.txtFigureNumber.set_text(str(new_text))
            self.txtFigureNumber.handler_unblock(self._lst_handler_id[3])

        return False

    def _add_requirement(self, __button, level):
        """
        Method to add a new Requirement to the open RTK Program database.

        :param gtk.ToolButton __button: the gtk.ToolButton() that called this
                                        function.
        :param int level: the indenture level of the Requirement(s) to add.
                          * 0 = sibling
                          * 1 = child or derived
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Find the selected requirement.
        (_model_, _row_) = self.treeview.get_selection().get_selected()

        # Find the parent or sibling requirement.
        if level == 0:                      # Adding derived requirements.
            _parent_ = "-"
            if _row_ is not None:
                _prow_ = _model_.iter_parent(_row_)
                if _prow_ is not None:
                    _parent_ = _model_.get_string_from_iter(_prow_)
            _title_ = _(u"RTK - Add Sibbling Requirements")
            _prompt_ = _(u"How many sibling requirements to add?")

        elif level == 1:                    # Adding sibling requirements.
            _parent_ = "-"
            if _row_ is not None:
                _parent_ = _model_.get_string_from_iter(_row_)
            _title_ = _(u"RTK - Add Derived Requirements")
            _prompt_ = _(u"How many derived requirements to add?")

        _n_requirements_ = _util.add_items(_title_, _prompt_)

        # Now add the number of derived or sibling requirements the user
        # requested.
        for i in range(_n_requirements_):
            _requirement_name = "New Requirement_" + str(i)
            _query = "INSERT INTO tbl_requirements \
                      (fld_revision_id, fld_assembly_id, \
                       fld_requirement_desc, fld_parent_requirement) \
                      VALUES (%d, %d, '%s', '%s')" % \
                     (self._app.REVISION.revision_id,
                      self._app.HARDWARE.assembly_id, _requirement_name,
                      _parent_)
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):

                _util.rtk_error(_(u"Error adding new reuqirement."))
                return True

        self.load_tree()

        return False

    def _add_stakeholder_input(self):
        """
        Method to add one or more stakeholder inputs to the RTK Program
        database.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _n_inputs_ = _util.add_items(title=_(u"RTK - Add Stakeholder Inputs"),
                                     prompt=_(u"How many stakeholder inputs "
                                              u"to add?"))

        if _n_inputs_ > 0:
            # Find the currently selected stakeholder input, if any, and
            # retrieve the revision ID.  If there is no selected stakeholder
            # input, retrieve the revision ID from the public Revision class
            # variable revision_id
            for i in range(_n_inputs_):
                _input = "Stakeholder input %d" % i
                _query = "INSERT INTO tbl_stakeholder_input \
                          (fld_revision_id, fld_stakeholder, \
                           fld_description, fld_group) \
                          VALUES (%d, '', '%s', '')" % \
                         (self._app.REVISION.revision_id, _input)
                if not self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx,
                                                  commit=True):

                    _util.rtk_error(_(u"Error adding new stakeholder input."))
                    return True

            self._load_stakeholder_inputs()

        return False

    def _add_vandv_task(self, _type=0):
        """
        Adds a new Verification and Validation task to the selected
        Requirement to the Program's MySQL or SQLite3 database.

        :param int _type: the type of task to add.
                          * 0 = add new task (default)
                          * 1 = assign existing task
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if _type == 0:
            _task_name = _(u"New V & V Task")

            _query = "INSERT INTO tbl_validation \
                      (fld_revision_id, fld_task_desc) \
                      VALUES (%d, '%s')" % (self._app.REVISION.revision_id,
                                            _task_name)
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Failed to add new V&V task to requirement "
                                  u"%d.") % (self.requirement_id,
                                             _conf.LOG_DIR + "RTK_error.log"))
                return True

            if _conf.BACKEND == 'mysql':
                _query = "SELECT LAST_INSERT_ID()"
            elif _conf.BACKEND == 'sqlite3':
                _query = "SELECT seq \
                          FROM sqlite_sequence \
                          WHERE name='tbl_validation'"
            _task_id = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

            _query = "INSERT INTO tbl_validation_matrix \
                      (fld_revision_id, fld_validation_id, \
                       fld_requirement_id) \
                      VALUES (%d, %d, %d)" % \
                     (self._app.REVISION.revision_id, _task_id[0][0],
                      self.requirement_id)
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Failed to add new V&V task %d to the "
                                  u"validation matrix.") % _task_id[0][0])
                return True

# FIXME: This seems a kludgy way to do this.  Try to make it more efficient.
            self._app.VALIDATION.load_tree()
            self.load_notebook()
            self.btnAssign.show()
            self.cmbVandVTasks.show()

        elif _type == 1:
            _model = self.cmbVandVTasks.get_model()
            _row = self.cmbVandVTasks.get_active_iter()
            _task_id = int(_model.get_value(_row, 1))

            _query = "INSERT INTO tbl_validation_matrix \
                      (fld_revision_id, fld_validation_id, \
                       fld_requirement_id) \
                      VALUES (%d, %d, %d)" % (self._app.REVISION.revision_id,
                                              _task_id, self.requirement_id)
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Failed to add new V&V task %d to the "
                                  u"validation matrix.") % _task_id[0][0])
                return True

        self._load_vandv_tasks()

        return False

    def _delete_requirement(self):
        """
        Deletes the currently selected requirement from the RTK Program
        database.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        # Delete any and all derived requirements.
        _query = "DELETE FROM tbl_requirements \
                  WHERE fld_parent_requirement=%d" % \
                 _model_.get_string_from_iter(_row_)
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):

            _util.rtk_error(_(u"Error deleting derived requirements from "
                              u"requirement %d." %
                              _model_.get_value(_row_, 1)))
            return True

        # Then delete the requirement itself.
        _query = "DELETE FROM tbl_requirements \
                  WHERE fld_revision_id=%d \
                  AND fld_requirement_id=%d" % (self._app.REVISION.revision_id,
                                                _model_.get_value(_row_, 1))
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):

            _util.rtk_error(_(u"Error deleting requirement %d." %
                              _model_.get_value(_row_, 1)))
            return True

        self.load_tree()

        return False

    def _delete_stakeholder_input(self):
        """
        Method to delete the selected stakeholder input from the RTK Program
        Database.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model,
         _row) = self.tvwStakeholderInput.get_selection().get_selected()

        _query = "DELETE FROM tbl_stakeholder_input \
                  WHERE fld_input_id=%d" % \
                 _model.get_value(_row, self._lst_stakeholder_col_order[0])
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):

            _util.rtk_error(_(u"Error deleting stakeholder input."))
            return True

        self._load_stakeholder_inputs()

        return False

    def _delete_vandv_task(self):
        """
        Method to delete the selected V & V Task link from the selected
        Requirement.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model,
         _row) = self.tvwValidation.get_selection().get_selected()

        _task_id = _model.get_value(_row, 0)

        _query = "DELETE FROM tbl_validation_matrix \
                  WHERE fld_revision_id=%d \
                  AND fld_requirement_id=%d \
                  AND fld_validation_id=%d" % \
                 (self._app.REVISION.revision_id, self.requirement_id,
                  _task_id)
        if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                          commit=True):
            _util.rtk_error(_(u"Error removing link to V & V task %d from "
                              u"requirement %d.") %
                            (self.requirement_id, _task_id))
            return True

        self._load_vandv_tasks()

        return False

    def save_requirement(self, __button=None):
        """
        Saves the Requirement class information to the open RTK Program
        database.

        :param gtk.Button __button: the gtk.Button() that called this function.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _save_line(model, __path, row, self):
            """
            Saves a single row in the Requirement class gtk.TreeModel() to the
            open RTK Program database.

            :param gtk.TreeModel model: the Requirement class gtk.TreeModel().
            :param str __path: the path of the selected row in the Requirement
                               class gtk.TreeModel().
            :param gtk.TreeIter row: the selected gtk.TreeIter() in the
                                     Requirement class gtk.TreeView().
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _date = _util.date_to_ordinal(model.get_value(
                row, self._lst_col_order[9]))

            _values = (model.get_value(row, self._lst_col_order[2]),
                       model.get_value(row, self._lst_col_order[3]),
                       model.get_value(row, self._lst_col_order[4]),
                       model.get_value(row, self._lst_col_order[5]),
                       model.get_value(row, self._lst_col_order[6]),
                       model.get_value(row, self._lst_col_order[7]),
                       model.get_value(row, self._lst_col_order[8]),
                       _date,
                       model.get_value(row, self._lst_col_order[10]),
                       model.get_value(row, self._lst_col_order[11]),
                       model.get_value(row, self._lst_col_order[12]),
                       model.get_value(row, self._lst_col_order[13]),
                       model.get_value(row, self._lst_col_order[14]),
                       model.get_value(row, self._lst_col_order[15]),
                       model.get_value(row, self._lst_col_order[16]),
                       model.get_value(row, self._lst_col_order[17]),
                       model.get_value(row, self._lst_col_order[18]),
                       model.get_value(row, self._lst_col_order[19]),
                       model.get_value(row, self._lst_col_order[20]),
                       model.get_value(row, self._lst_col_order[21]),
                       model.get_value(row, self._lst_col_order[22]),
                       model.get_value(row, self._lst_col_order[23]),
                       model.get_value(row, self._lst_col_order[24]),
                       model.get_value(row, self._lst_col_order[25]),
                       model.get_value(row, self._lst_col_order[26]),
                       model.get_value(row, self._lst_col_order[27]),
                       model.get_value(row, self._lst_col_order[28]),
                       model.get_value(row, self._lst_col_order[29]),
                       model.get_value(row, self._lst_col_order[30]),
                       model.get_value(row, self._lst_col_order[31]),
                       model.get_value(row, self._lst_col_order[32]),
                       model.get_value(row, self._lst_col_order[33]),
                       model.get_value(row, self._lst_col_order[34]),
                       model.get_value(row, self._lst_col_order[35]),
                       model.get_value(row, self._lst_col_order[36]),
                       model.get_value(row, self._lst_col_order[37]),
                       model.get_value(row, self._lst_col_order[38]),
                       model.get_value(row, self._lst_col_order[39]),
                       model.get_value(row, self._lst_col_order[40]),
                       model.get_value(row, self._lst_col_order[41]),
                       model.get_value(row, self._lst_col_order[42]),
                       model.get_value(row, self._lst_col_order[43]),
                       model.get_value(row, self._lst_col_order[44]),
                       model.get_value(row, self._lst_col_order[45]),
                       model.get_value(row, self._lst_col_order[46]),
                       model.get_value(row, self._lst_col_order[47]),
                       model.get_value(row, self._lst_col_order[48]),
                       model.get_value(row, self._lst_col_order[49]),
                       model.get_value(row, self._lst_col_order[50]),
                       model.get_value(row, self._lst_col_order[51]),
                       model.get_value(row, self._lst_col_order[52]),
                       model.get_value(row, self._lst_col_order[0]),
                       model.get_value(row, self._lst_col_order[1]))

            _query = "UPDATE tbl_requirements \
                      SET fld_assembly_id=%d, fld_requirement_desc='%s', \
                          fld_requirement_type='%s', \
                          fld_requirement_code='%s', fld_derived=%d, \
                          fld_parent_requirement='%s', fld_validated=%d, \
                          fld_validated_date=%d, fld_owner='%s', \
                          fld_specification='%s', fld_page_number='%s', \
                          fld_figure_number='%s', fld_parent_id=%d, \
                          fld_software_id=%d, fld_clear_q1=%d, \
                          fld_clear_q2=%d, fld_clear_q3=%d, fld_clear_q4=%d, \
                          fld_clear_q5=%d, fld_clear_q6=%d, fld_clear_q7=%d, \
                          fld_clear_q8=%d, fld_clear_q9=%d, \
                          fld_clear_q10=%d, fld_complete_q1=%d, \
                          fld_complete_q2=%d, fld_complete_q3=%d, \
                          fld_complete_q4=%d, fld_complete_q5=%d, \
                          fld_complete_q6=%d, fld_complete_q7=%d, \
                          fld_complete_q8=%d, fld_complete_q9=%d, \
                          fld_complete_q10=%d, fld_consistent_q1=%d, \
                          fld_consistent_q2=%d, fld_consistent_q3=%d, \
                          fld_consistent_q4=%d, fld_consistent_q5=%d, \
                          fld_consistent_q6=%d, fld_consistent_q7=%d, \
                          fld_consistent_q8=%d, fld_consistent_q9=%d, \
                          fld_consistent_q10=%d, fld_verifiable_q1=%d, \
                          fld_verifiable_q2=%d, fld_verifiable_q3=%d, \
                          fld_verifiable_q4=%d, fld_verifiable_q5=%d, \
                          fld_verifiable_q6=%d, fld_priority=%d \
                      WHERE fld_revision_id=%d \
                      AND fld_requirement_id=%d" % _values
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error saving requirement %d.") %
                                model.get_value(row, self._lst_col_order[1]))
                return True

            return False

        _model = self.treeview.get_model()
        _model.foreach(_save_line, self)

        self._save_stakeholder_inputs()
        self._save_vandv_tasks()

        return False

    def _save_stakeholder_inputs(self):
        """
        Method to save the stakeholder inputs to the RTK Program database.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _save_line(model, __path, row, self):
            """
            Function to save each node in the Stakeholder Input gtk.TreeView().

            :param gtk.TreeModel model: the stakeholder inputs gtk.TreeModel().
            :param str __path: the path of the active gtk.TreeIter()row in the
                               stakeholder inputs gtk.TreeModel().
            :param gtk.TreeIter row: the selected gtk.TreeIter() in the
                                     stakeholder inputs gtk.TreeView().
            :param rtk.Requirement self: the current instance of the
                                         Requirement class.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _user_def_ = []

            _priority_ = model.get_value(
                row, self._lst_stakeholder_col_order[4])
            _current_sat_ = model.get_value(
                row, self._lst_stakeholder_col_order[5])
            _planned_sat_ = model.get_value(
                row, self._lst_stakeholder_col_order[6])
            _user_def_.append(max(1.0, model.get_value(
                row, self._lst_stakeholder_col_order[10])))
            _user_def_.append(max(1.0, model.get_value(
                row, self._lst_stakeholder_col_order[11])))
            _user_def_.append(max(1.0, model.get_value(
                row, self._lst_stakeholder_col_order[12])))
            _user_def_.append(max(1.0, model.get_value(
                row, self._lst_stakeholder_col_order[13])))
            _user_def_.append(max(1.0, model.get_value(
                row, self._lst_stakeholder_col_order[14])))

            _improvement_ = 1.0 + 0.2 * (_planned_sat_ - _current_sat_)
            _overall_ = _priority_ * _improvement_ * _user_def_[0] * \
                _user_def_[1] * _user_def_[2] * _user_def_[3] * _user_def_[4]

            model.set_value(row, self._lst_stakeholder_col_order[7],
                            _improvement_)
            model.set_value(row, self._lst_stakeholder_col_order[8],
                            _overall_)

            _values = (model.get_value(row,
                                       self._lst_stakeholder_col_order[1]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[2]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[3]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[4]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[5]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[6]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[7]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[8]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[9]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[10]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[11]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[12]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[13]),
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[14]),
                       self._app.REVISION.revision_id,
                       model.get_value(row,
                                       self._lst_stakeholder_col_order[0]))
            _query = "UPDATE tbl_stakeholder_input \
                      SET fld_stakeholder='%s', fld_description='%s', \
                          fld_group='%s', fld_priority=%d, \
                          fld_customer_rank=%d, fld_planned_rank=%d, \
                          fld_improvement=%f, fld_overall_weight=%f, \
                          fld_requirement_code='%s', fld_user_float_1=%f, \
                          fld_user_float_2=%f, fld_user_float_3=%f, \
                          fld_user_float_4=%f, fld_user_float_5=%f \
                      WHERE fld_revision_id=%d \
                      AND fld_input_id=%d" % _values
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error saving stakeholder input %d.") %
                                model.get_value(
                                    row, self._lst_stakeholder_col_order[0]))
                return True

            return False

        self._input_weight()
        _model_ = self.tvwStakeholderInput.get_model()
        _model_.foreach(_save_line, self)

        return False

    def _save_vandv_tasks(self):
        """
        Saves the Validation Task list treeview information to the RTK Program
        database.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        def _save_line(model, __path, row, self):
            """
            Saves each task associated with the selected Requirement to the RTK
            Program database.

            :param gtk.TreeModel model: the Requirement class V&V task list
                                        gtk.TreeModel().
            :param str __path: the path of the active row in the Requirement
                               class V&V task list gtk.TreeModel().
            :param gtk.TreeIter row: the selected gtk.TreeIter() in the
                                     Requirement class V&V task list
                                     gtk.TreeView().
            :param rtk.Requirement self: the current instance of the
                                         Requirement class.
            :return: False if successful or True if an error is encountered.
            :rtype: boolean
            """

            _start = _util.date_to_ordinal(model.get_value(
                row, self._lst_col_order[2]))
            _end = _util.date_to_ordinal(model.get_value(
                row, self._lst_col_order[3]))
            _query = "UPDATE tbl_validation \
                      SET fld_task_desc='%s', fld_start_date=%d, \
                          fld_end_date=%d, fld_status=%f \
                      WHERE fld_validation_id=%d" % \
                     (model.get_value(row, self._lst_col_order[1]), _start,
                      _end, model.get_value(row, self._lst_col_order[4]),
                      model.get_value(row, self._lst_col_order[0]))
            if not self._app.DB.execute_query(_query, None, self._app.ProgCnx,
                                              commit=True):
                _util.rtk_error(_(u"Error saving V&V task %d.") %
                                model.get_value(row, self._lst_col_order[0]))
                return True

            return False

        _util.set_cursor(self._app, gtk.gdk.WATCH)

        _model_ = self.tvwValidation.get_model()
        _model_.foreach(_save_line, self)

        _util.set_cursor(self._app, gtk.gdk.LEFT_PTR)

        return False

    def _callback_check(self, check, index):
        """
        Callback function to retrieve and save checkbutton changes.

        :param gtk.CheckButton check: the gtk.CheckButton() that called this
                                      method.
        :param int index: the position in the Requirement class gtk.TreeView()
                          associated with the data from the calling
                          gtk.CheckButton().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()
        _model_.set_value(_row_, index, check.get_active())

        return False

    def _callback_combo(self, combo, index):
        """
        Callback function to retrieve and save combobox changes.

        :param gtk.ComboBox combo: the gtk.ComboBox() that called this method.
        :param int index: the position in the Requirement class gtk.TreeView()
                          associated with the data from the calling
                          gtk.ComboBox().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        try:
            i = int(combo.get_active())
        except TypeError:
            _model_ = combo.get_model()
            _row_ = combo.get_active_iter()
            i = _model_.get_value(_row_, 1)

        if index == 4:                      # Requirement type.
            self._create_code()
            i = combo.get_model().get_value(combo.get_active_iter(), 0)
        elif index == 10:                   # Requirement owner.
            i = combo.get_model().get_value(combo.get_active_iter(), 0)

        # Update the Requirement Tree.
        _model_.set_value(_row_, index, i)

        return False

    def _callback_entry(self, entry, __event, convert, index):
        """
        Callback function to retrieve and save entry changes.

        :param gtk.Entry entry: the gtk.Entry() that called this method.
        :param gtk.gdk.Event __event: the gtk.gdk.Event() that called this
                                      method.
        :param str convert: the data type to convert the gtk.Entry() contents
                            to.
        :param int index: the position in the Requirement class gtk.TreeView()
                          associated with the data from the calling
                          gtk.Entry().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        if convert == 'text':
            if index == 3:
                _text_ = self.txtRequirement.get_text(
                    *self.txtRequirement.get_bounds())
            else:
                _text_ = entry.get_text()

        elif convert == 'int':
            _text_ = int(entry.get_text())

        elif convert == 'float':
            _text_ = float(entry.get_text().replace('$', ''))

        # Update the Requirement Tree.
        try:
            _model_.set_value(_row_, index, _text_)
        except TypeError:                   # There are no requirements.
            return True

        return False

    def _create_code(self):
        """
        This function creates the Requirement code based on the type of
        requirement it is and it's index in the database.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model_, _row_) = self.treeview.get_selection().get_selected()

        cmbmodel = self.cmbRqmtType.get_model()
        cmbrow = self.cmbRqmtType.get_active_iter()

        prefix = cmbmodel.get_value(cmbrow, 1)
        suffix = str(_model_.get_value(_row_, 1))

        zeds = 4 - len(suffix)
        pad = '0' * zeds

        code = '%s-%s%s' % (prefix, pad, suffix)

        _model_.set_value(_row_, 5, code)
        self.txtCode.set_text(code)

        return False

    def _input_weight(self):
        """
        Method for calculating the overall weighting of a stakeholder input.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        (_model,
         _row) = self.tvwStakeholderInput.get_selection().get_selected()

        try:
            _priority = _model.get_value(
                _row, self._lst_stakeholder_col_order[4])
            _current_sat = _model.get_value(
                _row, self._lst_stakeholder_col_order[5])
            _planned_sat = _model.get_value(
                _row, self._lst_stakeholder_col_order[6])
            _user_def_1 = max(1.0, _model.get_value(
                _row, self._lst_stakeholder_col_order[10]))
            _user_def_2 = max(1.0, _model.get_value(
                _row, self._lst_stakeholder_col_order[11]))
            _user_def_3 = max(1.0, _model.get_value(
                _row, self._lst_stakeholder_col_order[12]))
            _user_def_4 = max(1.0, _model.get_value(
                _row, self._lst_stakeholder_col_order[13]))
            _user_def_5 = max(1.0, _model.get_value(
                _row, self._lst_stakeholder_col_order[14]))
        except TypeError:
            return True

        _improvement = 1.0 + 0.2 * (_planned_sat - _current_sat)
        _overall = _priority * _improvement * _user_def_1 * _user_def_2 * \
            _user_def_3 * _user_def_4 * _user_def_5

        _model.set_value(_row, self._lst_stakeholder_col_order[7],
                         _improvement)
        _model.set_value(_row, self._lst_stakeholder_col_order[8], _overall)

        return False

    def _notebook_page_switched(self, __notebook, __page, page_num):
        """
        Called whenever the Requirement class Work Book notebook page is
        changed.

        :param gtk.Notebook __notebook: the Requirement class gtk.Notebook().
        :param gtk.Widget __page: the newly selected page's child widget.
        :param int page_num: the newly selected page number.
                             * 0 = Stakeholder Input
                             * 1 = General Data
                             * 2 = Analysis
                             * 3 = V & V Tasks
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        if page_num == 0:
            self.btnAdd.set_tooltip_text(_(u"Adds one or more new stakeholder "
                                           u"inputs to the open RTK Program "
                                           u"database."))
            self.btnRemove.set_tooltip_text(_(u"Removes the selected "
                                              u"stakeholder input from the "
                                              u"open RTK Program database."))
            self.btnSave.set_tooltip_text(_(u"Saves the selected stakeholder "
                                            u"input to the open RTK Program "
                                            u"database."))
            self.btnAdd.show()
            self.btnAddChild.hide()
            self.btnAddSibling.hide()
            self.btnRemove.show()
            self.btnSave.show()
            self.btnAssign.hide()
            self.cmbVandVTasks.hide()
        elif page_num == 1:
            self.btnRemove.set_tooltip_text(_(u"Removes the selected "
                                              u"requirement from the open RTK "
                                              u"Program database."))
            self.btnSave.set_tooltip_text(_(u"Saves the selected requirement "
                                            u"to the open RTK Program "
                                            u"database."))
            self.btnAdd.hide()
            self.btnAddChild.show()
            self.btnAddSibling.show()
            self.btnRemove.show()
            self.btnSave.show()
            self.btnAssign.hide()
            self.cmbVandVTasks.hide()
        elif page_num == 2:
            self.btnRemove.set_tooltip_text(_(u"Removes the selected "
                                              u"requirement from the open RTK "
                                              u"Program database."))
            self.btnSave.set_tooltip_text(_(u"Saves the selected requirement "
                                            u"to the open RTK Program "
                                            u"database."))
            self.btnAdd.hide()
            self.btnAddChild.show()
            self.btnAddSibling.show()
            self.btnRemove.show()
            self.btnSave.show()
            self.btnAssign.hide()
            self.cmbVandVTasks.hide()
        elif page_num == 3:
            self.btnAdd.set_tooltip_text(_(u"Adds one or more new V&V tasks "
                                           u"to the open RTK Program database "
                                           u"and assigns them to the selected "
                                           u"requirement."))
            self.btnRemove.set_tooltip_text(_(u"Removes the selected V&V task "
                                              u"from the requirement."))
            self.btnSave.set_tooltip_text(_(u"Saves the selected requirement "
                                            u"to the open RTK Program "
                                            u"database."))
            self.btnAdd.show()
            self.btnAddChild.show()
            self.btnAddSibling.show()
            self.btnRemove.show()
            self.btnSave.show()
            self.btnAssign.show()
            self.cmbVandVTasks.show()

        self._selected_tab = page_num

        return False

    def _toolbutton_pressed(self, button):
        """
        Method to react to the Requirement class gtk.ToolButton() clicked
        events.

        :param gtk.ToolButton button: the gtk.ToolButton() that was pressed.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _page_ = self.notebook.get_current_page()

        if _page_ == 0:                     # Stakeholder Input tab.
            if button.get_name() == 'Add':
                self._add_stakeholder_input()
            elif button.get_name() == 'Remove':
                self._delete_stakeholder_input()
            elif button.get_name() == 'Save':
                self._save_stakeholder_inputs()
        elif _page_ == 1 or _page_ == 2:    # General Data tab.
            if button.get_name() == 'Remove':
                self._delete_requirement()
            elif button.get_name() == 'Save':
                self.save_requirement(None)
        elif _page_ == 3:                   # V&V Tasks tab.
            if button.get_name() == 'Add':
                self._add_vandv_task(0)
            elif button.get_name() == 'Assign':
                self._add_vandv_task(1)
            elif button.get_name() == 'Remove':
                self._delete_vandv_task()
            elif button.get_name() == 'Save':
                self._save_vandv_tasks()

        return False

    def _create_report(self, menuitem):
        """
        Method to create reports related to the Revision class.

        :param gtk.MenuItem menuitem: the gtk.MenuItem() that called this
                                      method.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        import xlwt
        from datetime import datetime
        from os import path

        # Launch a dialog to let the user select the path to the file
        # containing the ensuing report.
        _dialog = gtk.FileChooserDialog(title=_(u"RTK - Create Report"),
                                        parent=None,
                                        action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                        buttons=(gtk.STOCK_OK,
                                                 gtk.RESPONSE_ACCEPT,
                                                 gtk.STOCK_CANCEL,
                                                 gtk.RESPONSE_REJECT))
        _dialog.set_current_folder(_conf.PROG_DIR)
        _dialog.set_current_name(menuitem.get_label() + '.xls')

        # Set some filters to select all files or only some text files.
        _filter = gtk.FileFilter()
        _filter.set_name(_(u"Report Type"))
        _filter.add_pattern("*.pdf")
        _filter.add_pattern("*.xls")
        _filter.add_pattern("*.xlsx")
        _dialog.add_filter(_filter)

        _filter = gtk.FileFilter()
        _filter.set_name(_(u"All files"))
        _filter.add_pattern("*")
        _dialog.add_filter(_filter)

        # Get the path of the output file or return.
        if _dialog.run() == gtk.RESPONSE_ACCEPT:
            _filename = _dialog.get_filename()
            _dialog.destroy()
        else:
            _dialog.destroy()
            return False

        # Using the output file extension, select the correct writer.
        _ext = path.splitext(_filename)[-1][1:]
        if _ext.startswith('.'):
            _ext = _ext[1:]

        if _ext == 'xls':
            _writer = ExcelReport(_filename, engine='xlwt')

        _today = datetime.today().strftime('%Y-%m-%d')

        # Write the correct report.
        if menuitem.get_label() == 'Stakeholder Inputs':
            _title = 'Stakeholder Input Report'

            _model = self.tvwStakeholderInput.get_model()
            _row = _model.get_iter_root()

            # Retrieve the list of stakeholder inputs.
            _defs = []
            while _row is not None:
                _defs.append((_model.get_value(_row, 0),
                              _model.get_value(_row, 1),
                              _model.get_value(_row, 2),
                              _model.get_value(_row, 3),
                              _model.get_value(_row, 4),
                              _model.get_value(_row, 5),
                              _model.get_value(_row, 6),
                              _model.get_value(_row, 7),
                              _model.get_value(_row, 8),
                              _model.get_value(_row, 9)))
                _row = _model.iter_next(_row)

            # Create a pandas data frame from the results.
            _data = pd.DataFrame(_defs,
                                 columns=['Input ID', 'Stakeholder', 'Input',
                                          'Affinity Group', 'Priority',
                                          'Satisfaction w/ Exisiting Product',
                                          'Planned Satisfaction',
                                          'Improvement Factor',
                                          'Overall Weighting',
                                          'Implementing Requirement'])

            # Write the stakeholder inputs to the file.
            _writer.write_title(_title, self._app.REVISION.name,
                                srow=0, scol=0)
            _writer.write_content(_data, self._app.REVISION.name,
                                  srow=5, scol=0)

        # Write a list of requirements.
        elif menuitem.get_label() == 'Requirements Listing':
            _title = 'Requirements Listing Report'

            _model = self.treeview.get_model()
            _row = _model.get_iter_root()

            # Retrieve the list of requirements.
            _defs = []
            while _row is not None:
                # Convert ordinal dates to human-readable dates.
                _vdate = _util.ordinal_to_date(
                    _model.get_value(_row, self._lst_col_order[9]))
                if _vdate == '1970-01-01':
                    _vdate = ''
                _defs.append((_model.get_value(_row, self._lst_col_order[5]),
                              _model.get_value(_row, self._lst_col_order[3]),
                              _model.get_value(_row, self._lst_col_order[4]),
                              _model.get_value(_row, self._lst_col_order[52]),
                              _model.get_value(_row, self._lst_col_order[10]),
                              _model.get_value(_row, self._lst_col_order[11]),
                              _model.get_value(_row, self._lst_col_order[7]),
                              _vdate))
                _row = _model.iter_next(_row)

            _data = pd.DataFrame(_defs,
                                 columns=['Requirement Code', 'Description',
                                          'Requirement Type', 'Priority',
                                          'Owner', 'Specification',
                                          'Parent Requirement (if derived)',
                                          'Date Validated'])

            # Write the requirements list to the file.
            _writer.write_title(_title, self._app.REVISION.name,
                                srow=0, scol=0)
            _writer.write_content(_data, self._app.REVISION.name,
                                  srow=5, scol=0)

        # Write a list of V&V tasks sorted by requirement.
        elif menuitem.get_label() == 'V&V Task Listing':
            _title = 'Verification and Validation Task Report'

            _model = self.treeview.get_model()
            _row = _model.get_iter_root()

            # Retrieve all the V&V tasks sorted by requirement.
            _query = "SELECT t2.fld_requirement_id, t1.fld_validation_id, \
                             t1.fld_task_desc, t1.fld_start_date, \
                             t1.fld_end_date, t1.fld_status \
                      FROM tbl_validation AS t1 \
                      INNER JOIN tbl_validation_matrix AS t2 \
                      ON t2.fld_validation_id=t1.fld_validation_id \
                      WHERE t1.fld_revision_id=%d \
                      ORDER BY t2.fld_requirement_id" % \
                     _model.get_value(_row, self._lst_col_order[0])
            _results = self._app.DB.execute_query(_query, None,
                                                  self._app.ProgCnx)

            # Convert ordinal dates to human-readable dates.
            _tasks = []
            for _record in _results:
                _record = list(_record)
                _record[3] = _util.ordinal_to_date(_record[3])
                _record[4] = _util.ordinal_to_date(_record[4])
                _tasks.append(tuple(_record))

            _data = pd.DataFrame(_tasks,
                                 columns=['Requirement ID', 'Task ID',
                                          'Task Description',
                                          'Start Date', 'Due Date',
                                          '% Complete'])

            # Write the requirements list to the file.
            _writer.write_title(_title, self._app.REVISION.name,
                                srow=0, scol=0)
            _writer.write_content(_data, self._app.REVISION.name,
                                  srow=5, scol=0)

        _writer.close()

        return False
