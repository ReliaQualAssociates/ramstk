#!/usr/bin/env python
"""
###############################
Incident Package List Book View
###############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.incident.ListBook.py is part of the RTK Project
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
try:
    import gobject
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
from Assistants import AddComponents

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2016 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ListView(gtk.VBox):
    """
    The List Book view displays all the matrices and lists associated with the
    Incident Class.  The attributes of a Incident List Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Incident attribute.

    +----------+--------------------------------------------+
    | Position | Widget - Signal                            |
    +==========+============================================+
    |     0    | btnAddComponent - 'clicked'                |
    +----------+--------------------------------------------+
    |     1    | btnRemoveComponent - 'clicked'             |
    +----------+--------------------------------------------+
    |     2    | btnSaveComponents - 'clicked'              |
    +----------+--------------------------------------------+
    |     3    | btnAddAction - 'clicked'                   |
    +----------+--------------------------------------------+

    :ivar _mdcRTK: the :py:class:`rtk.RTK.RTK` master data controller.
    :ivar _model: the :py:class:`rtk.incident.Incident.Model` data model to
                  display.
    :ivar _modulebook: the :py:class:`rtk.incident.ModuleBook` associated with
                      the List View.
    :ivar _workbook: the :py:class:`rtk.incident.WorkBook associated with the
                    List View.
    :ivar _component: the :py:class:`rtk.incident.component.Component.Model`
                      associated with the selected Component in the list.
    :ivar gtk.Button btnAddComponent: the gtk.Button() to request the add
                                      component gtk.Assistant() be launched.
    :ivar gtk.Button btnRemoveComponent: the gtk.Button() to request the
                                         selected component be removed from the
                                         list of affected components.
    :ivar gtk.Button btnSaveComponents: the gtk.Button() to request all the
                                        affected components be saved to the
                                        RTK Project database.
    :ivar gtk.Button btnAddAction: the gtk.Button() to request the add action
                                   gtk.Assistant() be launched.
    :ivar gtk.TreeView tvwComponentList: the gtk.TreeView() to display the
                                         list of affected components associated
                                         with the selected Incident.
    :ivar gtk.TreeView tvwActionList: the gtk.TreeView() to display the list of
                                      (corrective) actions associated with the
                                      selected Incident.
    """

    def __init__(self, modulebook):
        """
        Method to initialize the List Book view for the Incident package.

        :param modulebook: the :py:class:`rtk.incident.ModuleBook` to associate
                           with this List Book.
        """

        gtk.VBox.__init__(self)

        # Define private dictionary attributes.

        # Define private list attributes.
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._mdcRTK = modulebook.mdcRTK
        self._modulebook = modulebook
        self._workbook = modulebook.workbook
        self._model = None
        self._component = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.btnAddComponent = Widgets.make_button(width=35, image='add')
        self.btnRemoveComponent = Widgets.make_button(width=35, image='remove')
        self.btnSaveComponents = Widgets.make_button(width=35, image='save')
        self.btnAddAction = Widgets.make_button(width=35, image='add')

        self.tvwComponentList = gtk.TreeView()
        self.tvwActionList = gtk.TreeView()

        # Set tooltips for the gtk.Widgets().
        self.btnAddComponent.set_tooltip_text(
            _(u"Adds an affected component "
              u"to the selected incident."))
        self.btnRemoveComponent.set_tooltip_text(
            _(u"Removes the selected "
              u"component from the list "
              u"of affected components "
              u"for the selected "
              u"incident."))
        self.btnSaveComponents.set_tooltip_text(
            _(u"Saves the affected "
              u"component list to the "
              u"open RTK Program "
              u"database."))
        self.btnAddAction.set_tooltip_text(
            _(u"Adds an action to the selected "
              u"incident."))

        # Connect widget signals to callback methods.
        self._lst_handler_id.append(
            self.btnAddComponent.connect('clicked', self._on_button_clicked,
                                         0))
        self._lst_handler_id.append(
            self.btnRemoveComponent.connect('clicked', self._on_button_clicked,
                                            1))
        self._lst_handler_id.append(
            self.btnSaveComponents.connect('clicked', self._on_button_clicked,
                                           2))
        self._lst_handler_id.append(
            self.btnAddAction.connect('clicked', self._on_button_clicked, 3))

        self.tvwComponentList.connect('cursor_changed',
                                      self._on_component_select, None, None)
        self.tvwComponentList.connect('row_activated',
                                      self._on_component_select)
        self.tvwActionList.connect('cursor_changed', self._on_action_select,
                                   None, None)
        self.tvwActionList.connect('row_activated', self._on_action_select)

        # Put it all together.
        _notebook = self._create_notebook()
        self.pack_start(_notebook)

        self.show_all()

    def _create_notebook(self):
        """
        Method to create the Incident class List View gtk.Notebook().

        :return: _notebook
        :rtype: gtk.Notebook
        """

        _notebook = gtk.Notebook()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[1] == 'left':
            _notebook.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[1] == 'right':
            _notebook.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[1] == 'top':
            _notebook.set_tab_pos(gtk.POS_TOP)
        else:
            _notebook.set_tab_pos(gtk.POS_BOTTOM)

        self._create_component_list_page(_notebook)
        self._create_action_list_page(_notebook)

        return _notebook

    def _create_component_list_page(self, notebook):
        """
        Method to create the Incident component list page in the List View.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Build up the containers for the Incident component list page.
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)
        _bbox.pack_start(self.btnAddComponent, False, False)
        _bbox.pack_start(self.btnRemoveComponent, False, False)
        _bbox.pack_start(self.btnSaveComponents, False, False)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwComponentList)

        _frame = Widgets.make_frame()
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _hbox.pack_end(_frame, True, True)

        # Add the component list.
        _model = gtk.ListStore(
            gobject.TYPE_INT, gobject.TYPE_STRING, gobject.TYPE_INT,
            gobject.TYPE_INT, gobject.TYPE_INT, gobject.TYPE_INT,
            gobject.TYPE_INT, gobject.TYPE_INT, gobject.TYPE_INT,
            gobject.TYPE_INT, gobject.TYPE_FLOAT, gobject.TYPE_FLOAT)
        self.tvwComponentList.set_model(_model)

        _headings = [
            _(u"Component\nID"),
            _(u"Part\nNumber"),
            _(u"Initial\nInstall"),
            _(u"Failure"),
            _(u"Suspension"),
            _(u"OOT\nFailure"),
            _("CND/NFF"),
            _(u"Interval\nCensored"),
            _(u"Use\nOperating\nTime"),
            _(u"Use\nCalendar\nTime"),
            _(u"Time to\nFailure"),
            _(u"Age at\nFailure")
        ]
        for _index, _heading in enumerate(_headings):
            _column = gtk.TreeViewColumn()

            if _index in [0, 1, 10, 11]:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _cell.set_property('background', 'light gray')
                _cell.set_property('foreground', 'black')
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=_index)
            else:
                _cell = gtk.CellRendererToggle()
                _cell.set_property('activatable', 1)
                _cell.connect('toggled', self._on_cellrenderer_toggle, None,
                              _index, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, active=_index)

            _label = Widgets.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            if _index == 0:
                _column.set_visible(False)

            self.tvwComponentList.append_column(_column)

        # Add the Incident component list page to the gtk.Notebook().
        _label = gtk.Label()
        _label.set_markup(
            _(u"<span weight='bold'>"
              u"Affected\nComponents</span>"))
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the list of components impacted "
              u"by the selected program incident."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def _create_action_list_page(self, notebook):
        """
        Method to create the page for creating, displaying, and documenting
        (corrective) actions associated with the selected Incident.

        :param gtk.Notebook notebook: the Incident class gtk.Notebook()
                                      widget.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _hbox = gtk.HBox()

        _bbox = gtk.VButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _hbox.pack_start(_bbox, False, False)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwActionList)

        _hbox.pack_end(_scrollwindow, True, True)

        _bbox.pack_start(self.btnAddAction, False, False)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Place the widgets used to display Incident action information.#
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Create the Action List in quadrant #2 (left middle).
        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_STRING)
        self.tvwActionList.set_model(_model)

        _headings = [
            _(u"Action\nID"),
            _(u"Prescribed\nAction"),
            _(u"Action\nTaken"),
            _(u"Action\nOwner"),
            _(u"Due Date"),
            _(u"Action\nStatus"),
            _("Approved By"),
            _(u"Approval\nDate"),
            _(u"Closed By"),
            _(u"Closure\nDate")
        ]
        for _index, _heading in enumerate(_headings):
            _column = gtk.TreeViewColumn()

            _cell = gtk.CellRendererText()
            _cell.set_property('editable', 0)
            _cell.set_property('background', 'light gray')
            _cell.set_property('foreground', 'black')
            _column.pack_start(_cell, True)
            _column.set_attributes(_cell, text=_index)

            _label = Widgets.make_column_heading(_heading)
            _column.set_widget(_label)
            _column.set_clickable(True)
            _column.set_resizable(True)
            _column.set_sort_column_id(_index)
            if _index in [1, 2]:
                _column.set_visible(False)

            self.tvwActionList.append_column(_column)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup(
            "<span weight='bold'>" + _(u"Incident\nActions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays actions related to the selected "
              u"incident."))

        notebook.insert_page(_hbox, tab_label=_label, position=-1)

        return False

    def load(self, model):
        """
        Method to load the Incident List Book.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._model = model

        self.load_component_list()
        self._load_action_list()

        return False

    def load_component_list(self):
        """
        Method to load the component list for the selected incident.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwComponentList.get_model()
        _model.clear()

        _components = self._modulebook.request_load_components(
            self._model.incident_id)

        for __, _component in enumerate(_components):
            _data = (_component[1], _component[13], _component[7],
                     _component[3], _component[4], _component[6],
                     _component[5], _component[8], _component[9],
                     _component[10], _component[11], _component[12])
            _model.append(_data)

        _row = _model.get_iter_root()
        self.tvwComponentList.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwComponentList.get_column(0)
            self.tvwComponentList.row_activated(_path, _column)

        return False

    def _load_action_list(self):
        """
        Method to load the Incident actions list.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _model = self.tvwActionList.get_model()
        _model.clear()

        _actions = self._modulebook.request_load_actions(
            self._model.incident_id)

        for __, _action in enumerate(_actions):
            _owner = ""
            _approver = ""
            _closer = ""

            if _action[4] > 0:
                _owner = Configuration.RTK_USERS[_action[4] - 1]
            if _action[7] > 0:
                _approver = Configuration.RTK_USERS[_action[7] - 1]
            if _action[10] > 0:
                _closer = Configuration.RTK_USERS[_action[10] - 1]

            _data = (_action[1], _action[2], _action[3], _owner,
                     Utilities.ordinal_to_date(_action[5]),
                     Configuration.RTK_INCIDENT_STATUS[_action[6]], _approver,
                     Utilities.ordinal_to_date(_action[8]), _closer,
                     Utilities.ordinal_to_date(_action[11]))
            _model.append(_data)

        _row = _model.get_iter_root()
        self.tvwActionList.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvwActionList.get_column(0)
            self.tvwActionList.row_activated(_path, _column)

        return False

    def _on_button_clicked(self, button, index):
        """
        Method to respond to gtk.Button() 'clicked' signals.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the signal handler list associated with
                          the Matrix calling this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        button.handler_block(self._lst_handler_id[index])

        if index == 0:
            AddComponents(self._model.revision_id, self._model.incident_id,
                          self._modulebook._dao, self._mdcRTK.dtcComponent,
                          self)
        elif index == 1:
            (_model,
             _row) = self.tvwComponentList.get_selection().get_selected()
            _component_id = _model.get_value(_row, 0)

            self._modulebook.request_delete_component(self._model.incident_id,
                                                      _component_id)
            self.load_component_list()
        elif index == 2:
            _model = self.tvwComponentList.get_model()
            _row = _model.get_iter_root()

            while _row is not None:
                _component_id = _model.get_value(_row, 0)
                self._modulebook.request_save_component(_component_id)
                _row = _model.iter_next(_row)
        elif index == 3:
            self._modulebook.request_add_action(self._model.incident_id)
            self._load_action_list()

        button.handler_unblock(self._lst_handler_id[index])

        return _return

    def _on_component_select(self, treeview, __path, __column):
        """
        Callback function to handle events for the affected component list
        gtk.TreeView().  It is called whenever an affected component
        gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the affected component gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = treeview.get_selection().get_selected()

        if _row is not None:
            _component_id = _model.get_value(_row, 0)
            self._component = self._mdcRTK.dtcComponent.dicComponents[
                _component_id]

        return False

    def _on_cellrenderer_toggle(self, cell, path, __new_text, position, model):
        """
        Method to respond to component list gtk.TreeView() gtk.CellRenderer()
        editing.

        :param gtk.CellRenderer cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer() that
                         was edited.
        :param str __new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().  Where position is:
                             0 = component ID
                             1 = part number
                             2 = initial installation
                             3 = failure
                             4 = suspension
                             5 = OCC fault
                             6 = CND/NFF
                             7 = interval censored
                             8 = use operating time
                             9 = use calendar time
        :param gtk.TreeModel model: the gtk.TreeModel() the edited
                                    gtk.CellRenderer() belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _value = not cell.get_active()
        model[path][position] = _value

        if position == 2:  # Initial installation.
            self._component.initial_installation = 1
            self._component.failure = 0
            self._component.suspension = 0
            self._component.occ_fault = 0
            self._component.cnd_nff = 0
            self._component.interval_censored = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
            model[path][7] = 0
        elif position == 3:  # Failure.
            self._component.initial_installation = 0
            self._component.failure = 1
            self._component.suspension = 0
            self._component.occ_fault = 0
            self._component.cnd_nff = 0
            self._component.interval_censored = 0
            model[path][2] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
            model[path][7] = 0
        elif position == 4:  # Suspension (right).
            self._component.initial_installation = 0
            self._component.failure = 0
            self._component.suspension = 1
            self._component.occ_fault = 0
            self._component.cnd_nff = 0
            self._component.interval_censored = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][5] = 0
            model[path][6] = 0
            model[path][7] = 0
        elif position == 5:  # OCC fault.
            self._component.initial_installation = 0
            self._component.failure = 0
            self._component.suspension = 0
            self._component.occ_fault = 1
            self._component.cnd_nff = 0
            self._component.interval_censored = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][6] = 0
            model[path][7] = 0
        elif position == 6:  # CND/NFF fault.
            self._component.initial_installation = 0
            self._component.failure = 0
            self._component.suspension = 0
            self._component.occ_fault = 0
            self._component.cnd_nff = 1
            self._component.interval_censored = 0
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][7] = 0
        elif position == 7:  # Interval censored.
            self._component.initial_installation = 0
            self._component.failure = 0
            self._component.suspension = 0
            self._component.occ_fault = 0
            self._component.cnd_nff = 0
            self._component.interval_censored = 1
            model[path][2] = 0
            model[path][3] = 0
            model[path][4] = 0
            model[path][5] = 0
            model[path][6] = 0
        elif position == 8:  # Use operating time.
            self._component.use_op_time = 1
            self._component.use_cal_time = 0
            model[path][9] = 0
        elif position == 9:  # Use calendar time.
            self._component.use_op_time = 0
            self._component.use_cal_time = 1
            model[path][8] = 0

        return False

    def _on_action_select(self, treeview, __path, __column):
        """
        Method to handle events for the Incident action list gtk.TreeView().
        It is called whenever an Incident action gtk.TreeView() row is
        activated.

        :param gtk.TreeView treeview: the affected component gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        (_model, _row) = treeview.get_selection().get_selected()

        if _row is not None:
            _action_id = _model.get_value(_row, 0)

            self._workbook.load_action_page(_action_id)

        return False
