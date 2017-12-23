#!/usr/bin/env python
"""
############################
Incident Package Module View
############################
"""

# -*- coding: utf-8 -*-
#
#       rtk.incident.ModuleBook.py is part of The RTK Project
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
    The Module Book view displays all the Incident items associated with the
    RTK Project in a flat list.  The attributes of a Module Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Incident attribute.
    :ivar list _lst_col_order: list containing the order of the columns in the
                               Module View gtk.TreeView().
    :ivar _model: the :py:class:`rtk.incident.Incident.Model` data model
                  that is currently selected.
    :ivar _dao: the :py:class:`rtk.dao.DAO.DAO` object used to communicate with
                the open RTK Project database.
    :ivar mdcRTK: the :py:class:`rtk.RTK.RTK` master data controller associated
                  with this Module View.
    :ivar workbook: the :py:class:`rtk.incident.WorkBook.WorkView`
                    associated with this instance of the Module View.
    :ivar listbook: the :py:class:`rtk.incident.ListBook.ListView`
                    associated with this instance of the Module View.
    :ivar bool load_all_revisions: indicats whether or not to load the
                                   Incidents from every Revision or only the
                                   selected Revision.
    :ivar gtk.TreeView treeview: the gtk.TreeView() displaying the list of
                                 Incidents.
    """

    def __init__(self, controller, rtk_view, position):
        """
        Method to initialize the Module Book view for the Incident package.

        :param controller: the instance of the :py:class:`rtk.RTK.RTK` master
                           data controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Incident
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Incident view.  Pass -1 to add to the end.
        """

        # Define private dictionary attributes.

        # Define private list attribute
        self._lst_handler_id = []

        # Define private scalar attributes.
        self._model = None

        # Define public dictionary attributes.

        # Define public list attributes.

        # Define public scalar attributes.
        self.mdcRTK = controller
        self.workbook = None
        self.listbook = None
        self.load_all_revisions = False

        # Create the main Incident class treeview.
        _fg_color = Configuration.RTK_COLORS[12]
        _bg_color = Configuration.RTK_COLORS[13]
        (self.treeview, self._lst_col_order) = Widgets.make_treeview(
            'Incidents', 11, _fg_color, _bg_color)

        # Populate the incident category gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[2]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(Configuration.RTK_INCIDENT_CATEGORY)):
            _cellmodel.append([Configuration.RTK_INCIDENT_CATEGORY[i]])

        # Populate the incident type gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[3]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(Configuration.RTK_INCIDENT_TYPE)):
            _cellmodel.append([Configuration.RTK_INCIDENT_TYPE[i]])

        # Populate the incident type gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[6]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(Configuration.RTK_INCIDENT_CRITICALITY)):
            _cellmodel.append([Configuration.RTK_INCIDENT_CRITICALITY[i]])

        # Populate the incident detection method gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[7]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(Configuration.RTK_DETECTION_METHODS)):
            _cellmodel.append([Configuration.RTK_DETECTION_METHODS[i]])

        # Populate the incident status gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[9]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(Configuration.RTK_INCIDENT_STATUS)):
            _cellmodel.append([Configuration.RTK_INCIDENT_STATUS[i]])

        # Populate the project lifesycle gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[29]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(Configuration.RTK_LIFECYCLE)):
            _cellmodel.append([Configuration.RTK_LIFECYCLE[i]])
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
        self.treeview.set_tooltip_text(
            _(u"Displays the list of program "
              u"incidents."))

        # Connect gtk.Widget() signals to callback methods.
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed', self._on_row_changed, None,
                                  None))
        self.treeview.connect('row_activated', self._on_row_changed)
        self.treeview.connect('button_press_event', self._on_button_press)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.add(self.treeview)
        _scrollwindow.show_all()

        _icon = Configuration.ICON_DIR + '32x32/incident.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Incidents") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays the development program "
              u"incidents for the selected revision or, "
              u"alternately, all revisions."))

        _hbox = gtk.HBox()
        _hbox.pack_start(_image)
        _hbox.pack_end(_label)
        _hbox.show_all()

        rtk_view.notebook.insert_page(
            _scrollwindow, tab_label=_hbox, position=position)

        # Create a Work View to associate with this Module View.
        self.workbook = WorkView(self)

        # Create a List View to associate with this Module View.
        self.listbook = ListView(self)

    def request_load_data(self, query=None):
        """
        Method to load the Incident Module Book view gtk.TreeModel() with
        Validataion task information.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve all the development program tests.
        (_incidents, __) = self.mdcRTK.dtcIncident.request_incidents(
            self.mdcRTK.project_dao, self.mdcRTK.revision_id,
            self.load_all_revisions, query)

        # Clear the Incident Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()
        for _incident in _incidents:
            # The software failure detection method should only be set if this
            # is a software failure.
            if _incident[7] == 0:
                _detection_method = ''
            else:
                _detection_method = Configuration.RTK_DETECTION_METHODS[
                    _incident[7]]
            if _incident[9] == 0:
                _status = ''
            else:
                _status = Configuration.RTK_INCIDENT_STATUS[_incident[9] - 1]

            _data = [
                _incident[0], _incident[1],
                Configuration.RTK_INCIDENT_CATEGORY[_incident[2] - 1],
                Configuration.RTK_INCIDENT_TYPE[_incident[3] - 1],
                _incident[4], _incident[5],
                Configuration.RTK_INCIDENT_CRITICALITY[_incident[6] - 1],
                _detection_method, _incident[8], _status, _incident[10],
                _incident[11], _incident[12], _incident[13], _incident[14],
                _incident[15], _incident[16], _incident[17], _incident[18],
                Utilities.ordinal_to_date(
                    _incident[19]), _incident[20], _incident[21],
                Utilities.ordinal_to_date(
                    _incident[22]), _incident[23], _incident[24],
                Utilities.ordinal_to_date(
                    _incident[25]), _incident[26], _incident[27],
                Utilities.ordinal_to_date(_incident[28]),
                Configuration.RTK_LIFECYCLE[_incident[29] - 1], _incident[30],
                _incident[31]
            ]

            _model.append(None, _data)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        return False

    def request_filter_incidents(self, revision_id, query):
        """
        Method to request a filtered set of incidents.

        :param str query: the query with the filtering criteria to pass to the
                          open RTK Program database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.request_load_data(query)

        return False

    def request_load_components(self, incident_id):
        """
        Method to load the components.

        :param int incident_id: the ID of the incident to load the component
                                list for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve all the affected components associated with the selected
        # incident.
        (_components, __) = self.mdcRTK.dtcComponent.request_components(
            self.mdcRTK.project_dao, incident_id)

        return _components

    def request_add_component(self, incident_id, hardware_id):
        """
        Method to add an affected component to the selected Incident.

        :param int incident_id: the Incident ID to add the new component to.
        :param int hardware_id: the Hardware ID of the new component to add.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results, _error_code) = self.mdcRTK.dtcComponent.add_component(
            incident_id, hardware_id)
        # TODO: Handle error codes.
        return (_results, _error_code)

    def request_delete_component(self, incident_id, hardware_id):
        """
        Method to delete an affected component from the selected Incident.

        :param int incident_id: the Incident ID to delete the component from.
        :param int hardware_id: the Hardware ID of the component to delete.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results, _error_code) = self.mdcRTK.dtcComponent.delete_component(
            incident_id, hardware_id)
        # TODO: Handle error codes.
        return (_results, _error_code)

    def request_save_component(self, hardware_id):
        """
        Method to save an affected component to the selected Incident.

        :param int hardware_id: the Hardware ID of the component to save.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results,
         _error_code) = self.mdcRTK.dtcComponent.save_component(hardware_id)
        # TODO: Handle error codes.
        return (_results, _error_code)

    def request_load_actions(self, incident_id):
        """
        Method to load the actions for the selected Incident.

        :param int incident_id: the ID of the incident to load the action
                                list for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Retrieve all the affected components associated with the selected
        # incident.
        (_actions, __) = self.mdcRTK.dtcAction.request_actions(
            self.mdcRTK.project_dao, incident_id)

        return _actions

    def request_add_action(self, incident_id):
        """
        Method to add an action to the selected Incident.

        :param int incident_id: the Incident ID to add the new component to.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results, _error_code) = self.mdcRTK.dtcAction.add_action(incident_id)
        # TODO: Handle error codes.
        return (_results, _error_code)

    def request_save_action(self, action_id):
        """
        Method to save the selected action.

        :param int action_id: the Action ID of the action to save.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results, _error_code) = self.mdcRTK.dtcAction.save_action(action_id)
        # TODO: Handle error codes.
        return (_results, _error_code)

    def update(self, position, new_text):
        """
        Method to update the selected row in the Module Book gtk.TreeView()
        with changes to the Incident data model attributes.  Called by other
        views when the Incident data model attributes are edited via their
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
        Method for handling mouse clicks on the Incident package Module Book
        gtk.TreeView().

        :param gtk.TreeView treeview: the Incident class gtk.TreeView().
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
        Method to handle events for the Incident package Module Book
        gtk.TreeView().  It is called whenever a Module Book gtk.TreeView()
        row is activated.

        :param gtk.TreeView treeview: the Incident class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        _incident_id = _model.get_value(_row, 1)

        self._model = self.mdcRTK.dtcIncident.dicIncidents[_incident_id]

        self.workbook.load(self._model)
        self.listbook.load(self._model)

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, new_text, index):
        """
        Method to handle events for the Incident package Module Book
        gtk.CellRenderer().  It is called whenever a Module Book
        gtk.CellRenderer() is edited.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str __path: the path of the gtk.CellRenderer() that was edited.
        :param str new_text: the new text in the gtk.CellRenderer() that was
                             edited.
        :param int index: the position in the Incident package Module Book
                          gtk.TreeView().
        :return: False if successful and True if an error is encountered.
        :rtype: bool
        """
        # TODO: Consider refactoring _on_cell_edited; current McCabe Complexity metric = 12.
        if self._lst_col_order[index] == 2:
            try:
                _category = Configuration.RTK_INCIDENT_CATEGORY.index(
                    new_text) + 1
            except ValueError:
                _category = 0
            self._model.incident_category = _category
        elif self._lst_col_order[index] == 3:
            try:
                _type = Configuration.RTK_INCIDENT_TYPE.index(new_text) + 1
            except ValueError:
                _type = 0
            self._model.incident_type = _type
        elif self._lst_col_order[index] == 6:
            try:
                _criticality = Configuration.RTK_INCIDENT_CRITICALITY.index(
                    new_text) + 1
            except ValueError:
                _criticality = 0
            self._model.criticality = _criticality
        elif self._lst_col_order[index] == 7:
            try:
                _method = Configuration.RTK_DETECTION_METHODS.index(
                    new_text) + 1
            except ValueError:
                _method = 0
            self._model.detection_method = _method
        elif self._lst_col_order[index] == 8:
            self._model.remarks = new_text
        elif self._lst_col_order[index] == 9:
            try:
                _status = Configuration.RTK_INCIDENT_STATUS.index(new_text) + 1
            except ValueError:
                _status = 0
            self._model.status = _status
        elif self._lst_col_order[index] == 10:
            self._model.test = new_text
        elif self._lst_col_order[index] == 11:
            self._model.test_case = new_text
        elif self._lst_col_order[index] == 12:
            self._model.execution_time = float(new_text)
        elif self._lst_col_order[index] == 14:
            self._model.cost = float(new_text)
        elif self._lst_col_order[index] == 29:
            try:
                _cycle = Configuration.RTK_LIFECYCLE.index(new_text) + 1
            except ValueError:
                _cycle = 0
            self._model.life_cycle = _cycle

        self.workbook.update()

        return False
