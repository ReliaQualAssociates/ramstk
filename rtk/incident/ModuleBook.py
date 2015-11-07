#!/usr/bin/env python
"""
############################
Incident Package Module View
############################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.incident.ModuleBook.py is part of The RTK Project
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
    The Module Book view displays all the Incident items associated with the
    RTK Project in a flat list.  The attributes of a Module Book view are:

    :ivar list _lst_handler_id: list containing the ID's of the callback
                                signals for each gtk.Widget() associated with
                                an editable Incident attribute.
    :ivar _lst_col_order: list containing the order of the columns in the
                          Module View :py:class:`gtk.TreeView`.
    :ivar _model: the :py:class:`rtk.incident.Incident.Model` data model
                  that is currently selected.
    :ivar _listbook: the :py:class:`rtk.incident.ListBook.ListView`
                     associated with this instance of the Module View.
    :ivar _workbook: the :py:class:`rtk.incident.WorkBook.WorkView`
                     associated with this instance of the Module View.
    :ivar dtcIncident: the :py:class:`rtk.incident.Incident` data
                         controller to use for accessing the Incident data
                         models.
    :ivar dtcActions: the :py:class:`rtk.incident.action.Action` data
                      controller to use for accessing the Incident Action data
                      models.
    :ivar dtcComponents: the :py:class:`rtk.incident.component.Component` data
                         controller to use for accessing the Incident Component
                         data models.
    :ivar treeview: the :py:class:`gtk.TreeView` displaying the list of
                    Incident tasks.
    """

    def __init__(self, controller, rtk_view, position, *args):
        """
        Initializes the Module Book view for the Incident package.

        :param controller: the instance of the
                           :py:class:`rtk.incident.Incident` data
                           controller to use with this view.
        :param gtk.Notebook rtk_view: the gtk.Notebook() to add the Incident
                                      view into.
        :param int position: the page position in the gtk.Notebook() to insert
                             the Incident view.  Pass -1 to add to the end.
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
        self.dtcIncident = controller
        self.dtcActions = args[0][0]
        self.dtcComponents = args[0][1]
        self.load_all_revisions = False

        # Create the main Incident class treeview.
        (self.treeview,
         self._lst_col_order) = _widg.make_treeview('Incidents', 14, None,
                                                    None, _conf.RTK_COLORS[12],
                                                    _conf.RTK_COLORS[13])

        self.treeview.set_tooltip_text(_(u"Displays the list of program "
                                         u"incidents."))

        # Populate the incident category gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[2]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(_conf.RTK_INCIDENT_CATEGORY)):
            _cellmodel.append([_conf.RTK_INCIDENT_CATEGORY[i]])

        # Populate the incident type gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[3]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(_conf.RTK_INCIDENT_TYPE)):
            _cellmodel.append([_conf.RTK_INCIDENT_TYPE[i]])

        # Populate the incident type gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[6]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(_conf.RTK_INCIDENT_CRITICALITY)):
            _cellmodel.append([_conf.RTK_INCIDENT_CRITICALITY[i]])

        # Populate the incident detection method gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[7]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(_conf.RTK_DETECTION_METHODS)):
            _cellmodel.append([_conf.RTK_DETECTION_METHODS[i]])

        # Populate the incident status gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[9]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(_conf.RTK_INCIDENT_STATUS)):
            _cellmodel.append([_conf.RTK_INCIDENT_STATUS[i]])

        # Populate the project lifesycle gtk.CellRendererCombo().
        _cell = self.treeview.get_column(
            self._lst_col_order[29]).get_cell_renderers()
        _cellmodel = _cell[0].get_property('model')
        _cellmodel.clear()
        _cellmodel.append([""])
        for i in range(len(_conf.RTK_LIFECYCLE)):
            _cellmodel.append([_conf.RTK_LIFECYCLE[i]])
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

        _icon = _conf.ICON_DIR + '32x32/incident.png'
        _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
        _image = gtk.Image()
        _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Incidents") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays the development program "
                                  u"incidents for the selected revision or, "
                                  u"alternately, all revisions."))

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
        Loads the Incident Module Book view gtk.TreeModel() with Validataion
        task information.

        :param dao: the :py:class: `rtk.dao.DAO` object used to communicate
                    with the RTK Project database.
        :param int revision_id: the ID of the revision to load incident data
                                for.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self._dao = dao

        # Retrieve all the development program tests.
        (_incidents,
         __) = self.dtcIncident.request_incidents(dao, revision_id,
                                                  self.load_all_revisions,
                                                  query)

        # Clear the Incident Module View gtk.TreeModel().
        _model = self.treeview.get_model()
        _model.clear()
        for _incident in _incidents:
            # The software failure detection method should only be set if this
            # is a software failure.
            if _incident[7] == 0:
                _detection_method = ''
            else:
                _detection_method = _conf.RTK_DETECTION_METHODS[_incident[7]]
            if _incident[9] == 0:
                _status = ''
            else:
                _status = _conf.RTK_INCIDENT_STATUS[_incident[9] - 1]

            _data = [_incident[0], _incident[1],
                     _conf.RTK_INCIDENT_CATEGORY[_incident[2] - 1],
                     _conf.RTK_INCIDENT_TYPE[_incident[3] - 1],
                     _incident[4], _incident[5],
                     _conf.RTK_INCIDENT_CRITICALITY[_incident[6] - 1],
                     _detection_method, _incident[8],
                     _status,
                     _incident[10], _incident[11], _incident[12],
                     _incident[13], _incident[14], _incident[15],
                     _incident[16], _incident[17], _incident[18],
                     _util.ordinal_to_date(_incident[19]), _incident[20],
                     _incident[21], _util.ordinal_to_date(_incident[22]),
                     _incident[23], _incident[24],
                     _util.ordinal_to_date(_incident[25]), _incident[26],
                     _incident[27], _util.ordinal_to_date(_incident[28]),
                     _conf.RTK_LIFECYCLE[_incident[29] - 1], _incident[30],
                     _incident[31]]

            _model.append(None, _data)

        _row = _model.get_iter_root()
        self.treeview.expand_all()
        self.treeview.set_cursor('0', None, False)
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.row_activated(_path, _column)

        #self._listbook.load(revision_id)

        return False

    def request_filter_incidents(self, revision_id, query):
        """
        Method to request a filtered set of incidents.

        :param int revision_id: the revision ID for the filtered incident list.
        :param str query: the query with the filtering criteria to pass to the
                          open RTK Program database.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.request_load_data(self._dao, revision_id, query)

        return False

    def request_load_components(self, incident_id):
        """
        Method to load the components.

        :param int incident_id: the ID of the incident to load the component
                                list for.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Retrieve all the affected components associated with the selected
        # incident.
        (_components,
         __) = self.dtcComponents.request_components(self._dao, incident_id)

        return _components

    def request_add_component(self, incident_id, hardware_id):
        """
        Method to add an affected component to the selected Incident.

        :param int incident_id: the Incident ID to add the new component to.
        :param int hardware_id: the Hardware ID of the new component to add.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results, _error_code) = self.dtcComponents.add_component(incident_id,
                                                                   hardware_id)

        # TODO: Handle error codes.
        return(_results, _error_code)

    def request_delete_component(self, incident_id, hardware_id):
        """
        Method to delete an affected component from the selected Incident.

        :param int incident_id: the Incident ID to delete the component from.
        :param int hardware_id: the Hardware ID of the component to delete.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results,
         _error_code) = self.dtcComponents.delete_component(incident_id,
                                                            hardware_id)

        # TODO: Handle error codes.
        return(_results, _error_code)

    def request_save_component(self, hardware_id):
        """
        Method to save an affected component to the selected Incident.

        :param int hardware_id: the Hardware ID of the component to save.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results,
         _error_code) = self.dtcComponents.save_component(hardware_id)

        # TODO: Handle error codes.
        return(_results, _error_code)

    def request_load_actions(self, incident_id):
        """
        Method to load the actions for the selected Incident.

        :param int incident_id: the ID of the incident to load the action
                                list for.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Retrieve all the affected components associated with the selected
        # incident.
        (_actions,
         __) = self.dtcActions.request_actions(self._dao, incident_id)

        return _actions

    def request_add_action(self, incident_id):
        """
        Method to add an action to the selected Incident.

        :param int incident_id: the Incident ID to add the new component to.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results, _error_code) = self.dtcActions.add_action(incident_id)

        # TODO: Handle error codes.
        return(_results, _error_code)

    def request_save_action(self, action_id):
        """
        Method to save the selected action.

        :param int action_id: the Action ID of the action to save.
        :return: (_results, _error_code) from the SQL query
        :rtype: tuple
        """

        (_results,
         _error_code) = self.dtcActions.save_action(action_id)

        # TODO: Handle error codes.
        return(_results, _error_code)

    def update(self, position, new_text):
        """
        Updates the selected row in the Module Book gtk.TreeView() with changes
        to the Incident data model attributes.  Called by other views when
        the Incident data model attributes are edited via their
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
        Callback method for handling mouse clicks on the Incident package
        Module Book gtk.TreeView().

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
        Callback function to handle events for the Incident package Module
        Book gtk.TreeView().  It is called whenever a Module Book
        gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the Incident class gtk.TreeView().
        :param str __path: the actived row gtk.TreeView() path.
        :param gtk.TreeViewColumn __column: the actived gtk.TreeViewColumn().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        _incident_id = _model.get_value(_row, 1)

        self._model = self.dtcIncident.dicIncidents[_incident_id]

        self._workbook.load(self._model)

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_cell_edited(self, __cell, __path, new_text, index):
        """
        Callback method to handle events for the Incident package Module Book
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

        if self._lst_col_order[index] == 2:
            try:
                self._model.incident_category = _conf.RTK_INCIDENT_CATEGORY.index(new_text) + 1
            except ValueError:
                self._model.incident_category = 0
        elif self._lst_col_order[index] == 3:
            try:
                self._model.incident_type = _conf.RTK_INCIDENT_TYPE.index(new_text) + 1
            except ValueError:
                self._model.incident_type = 0
        elif self._lst_col_order[index] == 6:
            try:
                self._model.criticality = _conf.RTK_INCIDENT_CRITICALITY.index(new_text) + 1
            except ValueError:
                self._model.criticality = 0
        elif self._lst_col_order[index] == 7:
            try:
                self._model.detection_method = _conf.RTK_DETECTION_METHODS.index(new_text) + 1
            except ValueError:
                self._model.detection_method = 0
        elif self._lst_col_order[index] == 8:
            self._model.remarks = new_text
        elif self._lst_col_order[index] == 9:
            try:
                self._model.status = _conf.RTK_INCIDENT_STATUS.index(new_text) + 1
            except ValueError:
                self._model.status = 0
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
                self._model.life_cycle = _conf.RTK_LIFECYCLE.index(new_text) + 1
            except ValueError:
                self._model.life_cycle = 0

        self._workbook.update()

        return False
