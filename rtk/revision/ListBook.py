#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.revision.ListBook.py is part of the RTK Project
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

"""
###############################
Revision Package List Book View
###############################
"""

import sys

# Import modules for localization support.
import gettext
import locale

# Modules required for the GUI.
import pango
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
    import rtk.Configuration as Configuration   # pylint: disable=E0401
    import rtk.gui.gtk.Widgets as Widgets       # pylint: disable=E0401

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class ListView(gtk.Notebook):

    """
    The List View displays all the matrices and lists associated with the
    Revision Class.  The attributes of a List View are:

    :ivar list _lst_handler_id: the list of gtk.Widget() signal IDs.
    :ivar _dtc_profile: the :py:class:`rtk.usage.Usage.UsageProfile` data
                        controller associated with this List Book.
    :ivar _dtc_definitions: the :py:class:`rtk.failure_definition.FailureDefinition.FailureDefinition`
                            data controller associated with this List Book.
    :ivar int _revision_id: the Revision ID whose information is being
                            displayed in this List Book.
    :ivar gtk.Button btnAddSibling: the gtk.Button() to add a sibling item to
                                    the Usage Profile.
    :ivar gtk.Button btnAddChild: the gtk.Button() to add a child item to the
                                  Usage Profile.
    :ivar gtk.Button btnRemoveUsage: the gtk.Button() to remove the selected
                                     item from the Usage Profile.
    :ivar gtk.Button btnSaveUsage: the gtk.Button() to save the Usage Profile.
    :ivar gtk.Button btnAddDefinition: the gtk.Button() to add a Failure
                                       Definition.
    :ivar gtk.Button btnRemoveDefinition: the gtk.Button() to remove the
                                          selected Failure Defintion.
    :ivar gtk.Button btnSaveDefinitions: the gtk.Button() to save the Failure
                                         Definitions.
    :ivar gtk.TreeView tvwUsageProfile: the gtk.TreeView() to display the
                                        Usage Profile for the selected
                                        Revision.
    :ivar gtk.TreeView tvwFailureDefinitions: the gtk.TreeView() to display the
                                               Failure Definitions for the
                                               selected Revision.
    """

    def __init__(self, modulebook):
        """
        Method to initialize the List View for the Revision package.

        :param modulebook: the :py:class:`rtk.revision.ModuleBook` to associate
                           with this List Book.
        """

        gtk.Notebook.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._dtc_profile = modulebook.mdcRTK.dtcProfile
        self._dtc_definitions = modulebook.mdcRTK.dtcDefinitions
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.btnAddSibling = Widgets.make_button(width=35,
                                                 image='insert_sibling')
        self.btnAddChild = Widgets.make_button(width=35, image='insert_child')
        self.btnRemoveUsage = Widgets.make_button(width=35, image='remove')
        self.btnSaveUsage = Widgets.make_button(width=35, image='save')
        self.btnAddDefinition = Widgets.make_button(width=35, image='add')
        self.btnRemoveDefinition = Widgets.make_button(width=35,
                                                       image='remove')
        self.btnSaveDefinitions = Widgets.make_button(width=35, image='save')

        self.tvwUsageProfile = gtk.TreeView()
        self.tvwFailureDefinitions = gtk.TreeView()

        # Set the user's preferred gtk.Notebook tab position.
        if Configuration.TABPOS[1] == 'left':
            self.set_tab_pos(gtk.POS_LEFT)
        elif Configuration.TABPOS[1] == 'right':
            self.set_tab_pos(gtk.POS_RIGHT)
        elif Configuration.TABPOS[1] == 'top':
            self.set_tab_pos(gtk.POS_TOP)
        else:
            self.set_tab_pos(gtk.POS_BOTTOM)

        self._create_usage_profile_page()
        self._create_failure_definition_page()

        # Connect to callback functions.
        self._lst_handler_id.append(
            self.btnAddSibling.connect('clicked', self._on_button_clicked, 0))
        self._lst_handler_id.append(
            self.btnAddChild.connect('clicked', self._on_button_clicked, 1))
        self._lst_handler_id.append(
            self.btnRemoveUsage.connect('clicked', self._on_button_clicked, 2))
        self._lst_handler_id.append(
            self.btnSaveUsage.connect('clicked', self._on_button_clicked, 3))
        self._lst_handler_id.append(
            self.tvwUsageProfile.connect('cursor_changed',
                                         self._on_usage_row_changed))

        self._lst_handler_id.append(
            self.btnAddDefinition.connect('clicked',
                                          self._on_button_clicked, 5))
        self._lst_handler_id.append(
            self.btnRemoveDefinition.connect('clicked',
                                             self._on_button_clicked, 6))
        self._lst_handler_id.append(
            self.btnSaveDefinitions.connect('clicked',
                                            self._on_button_clicked, 7))

        self.show_all()

    def _create_usage_profile_page(self):
        """
        Method to create the Revision List Book page for displaying usage
        profiles for the selected Revision.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        # Create the mission profile gtk.TreeView().
        self.tvwUsageProfile.set_tooltip_text(_(u"Displays the usage profile "
                                                u"for the currently selected "
                                                u"revision."))
        _model = gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_INT)
        self.tvwUsageProfile.set_model(_model)

        for i in range(10):
            _column = gtk.TreeViewColumn()
            if i == 0:
                _cell = gtk.CellRendererPixbuf()
                _cell.set_property('xalign', 0.5)
                _column.pack_start(_cell, False)
                _column.set_attributes(_cell, pixbuf=0)

                _cell = gtk.CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=1)

                _column.set_visible(True)
            elif i == 1:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, 3, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, visible=11)

                _column.set_visible(True)
            elif i == 2:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, 4, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=4)
                _column.set_visible(True)
            elif i == 3 or i == 4:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, i + 2,
                              _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2)
                _column.set_visible(True)
            elif i == 5 or i == 6:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_usage_cell_edited, i + 2,
                              _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2, visible=10)
                _column.set_visible(True)
            else:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _column.set_visible(False)

            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            self.tvwUsageProfile.append_column(_column)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _vbox = gtk.VBox()

        _bbox = gtk.HButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _vbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwUsageProfile)

        _frame = Widgets.make_frame(label=_(u"Usage Profile"))
        _frame.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddSibling, False, False)
        _bbox.pack_start(self.btnAddChild, False, False)
        _bbox.pack_start(self.btnRemoveUsage, False, False)
        _bbox.pack_start(self.btnSaveUsage, False, False)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Usage\nProfiles") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays usage profile for the selected "
                                  u"revision."))
        self.insert_page(_vbox, tab_label=_label, position=-1)

        return False

    def _create_failure_definition_page(self):
        """
        Method to create the Revision List Book page for displaying failure
        definitions for the selected Revision.

        :param gtk.Notebook notebook: the gtk.Notebook() to add the page to.
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        _model = gtk.ListStore(gobject.TYPE_INT, gobject.TYPE_STRING)
        self.tvwFailureDefinitions.set_model(_model)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 0)
        _cell.set_property('wrap-width', 250)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Definition\nNumber</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=0)
        self.tvwFailureDefinitions.append_column(_column)

        _cell = gtk.CellRendererText()
        _cell.set_property('editable', 1)
        _cell.set_property('wrap-width', 450)
        _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
        _cell.set_property('yalign', 0.1)
        _cell.connect('edited', self._on_failure_cell_edited, 1, _model)
        _label = gtk.Label()
        _label.set_line_wrap(True)
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.set_markup("<span weight='bold'>Failure Definition</span>")
        _label.set_use_markup(True)
        _label.show_all()
        _column = gtk.TreeViewColumn()
        _column.set_widget(_label)
        _column.set_visible(True)
        _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
        _column.pack_start(_cell, True)
        _column.set_attributes(_cell, text=1)
        self.tvwFailureDefinitions.append_column(_column)

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        # Build-up the containers for the tab.                          #
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
        _vbox = gtk.VBox()

        _bbox = gtk.HButtonBox()
        _bbox.set_layout(gtk.BUTTONBOX_START)

        _vbox.pack_start(_bbox, False, True)

        _scrollwindow = gtk.ScrolledWindow()
        _scrollwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        _scrollwindow.add(self.tvwFailureDefinitions)

        _frame = Widgets.make_frame(label=_(u"Failure Definition List"))
        _frame.set_shadow_type(gtk.SHADOW_OUT)
        _frame.add(_scrollwindow)

        _vbox.pack_end(_frame, True, True)

        _bbox.pack_start(self.btnAddDefinition, False, False)
        _bbox.pack_start(self.btnRemoveDefinition, False, False)
        _bbox.pack_start(self.btnSaveDefinitions, False, False)

        # Insert the tab.
        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Failure\nDefinitions") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays usage profiles for the selected "
                                  u"revision."))
        self.insert_page(_vbox, tab_label=_label, position=-1)

        return False

    def load(self, revision_id):
        """
        Method to load the Revision List Book.

        :param int revision_id: the Revision ID to load the List Book for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self._revision_id = revision_id

        self._load_usage_profile()
        self._load_failure_definitions()

        return False

    def _load_usage_profile(self, path=None):
        """
        Method to load the Usage Profile gkt.TreeView().

        :keyword str path: the path in the gtk.TreeView() to select as active
                           after loading the Usage Profile.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model = self.tvwUsageProfile.get_model()
        _model.clear()
        for _mission in self._dtc_profile.dicProfiles[self._revision_id].dicMissions.values():
            _icon = Configuration.ICON_DIR + '32x32/mission.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = (_icon, _mission.mission_id, _mission.description,
                     '', _mission.time_units, 0.0, _mission.time, 0.0, 0.0, 1,
                     0, 0)
            _mission_row = _model.append(None, _data)

            for _phase in _mission.dicPhases.values():
                _icon = Configuration.ICON_DIR + '32x32/phase.png'
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                _data = (_icon, _phase.phase_id, _phase.code,
                         _phase.description, '', _phase.start_time,
                         _phase.end_time, 0.0, 0.0, 2, 0, 1)
                _phase_row = _model.append(_mission_row, _data)

                for _environment in _phase.dicEnvironments.values():
                    _icon = Configuration.ICON_DIR + '32x32/environment.png'
                    _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
                    _data = (_icon, _environment.environment_id,
                             _environment.name, '', _environment.units,
                             _environment.minimum, _environment.maximum,
                             _environment.mean, _environment.variance, 3, 1, 0)
                    _model.append(_phase_row, _data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                _return = True
        _column = self.tvwUsageProfile.get_column(0)
        try:
            self.tvwUsageProfile.set_cursor(path, None, False)
            self.tvwUsageProfile.row_activated(path, _column)
        except TypeError:
            _return = True
        self.tvwUsageProfile.expand_all()

        return _return

    def _load_failure_definitions(self, path=None):
        """
        Method to load the Failure Definitions gkt.TreeView().

        :keyword str path: the path in the gtk.TreeView() to select as active
                           after loading the Usage Profile.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _definitions = self._dtc_definitions.dicDefinitions[self._revision_id].values()

        _model = self.tvwFailureDefinitions.get_model()
        _model.clear()
        for _definition in _definitions:
            _data = (_definition.definition_id, _definition.definition)
            _model.append(_data)

        if path is None:
            _root = _model.get_iter_root()
            try:
                path = _model.get_path(_root)
            except TypeError:
                _return = True
        _column = self.tvwFailureDefinitions.get_column(0)
        try:
            self.tvwFailureDefinitions.set_cursor(path, None, False)
            self.tvwFailureDefinitions.row_activated(path, _column)
        except TypeError:
            _return = True
        self.tvwFailureDefinitions.expand_all()

        return _return

    def _on_button_clicked(self, button, index):    # pylint: disable=R0914
        """
        Method to respond to gtk.Button() clicked signals and calls the correct
        function or method, passing any parameters as needed.

        :param gtk.Button button: the gtk.Button() that called this method.
        :param int index: the index in the handler ID list of the callback
                          signal associated with the gtk.Button() that called
                          this method.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        button.handler_block(self._lst_handler_id[index])

        if index == 0:                      # Add a sibling.
            self._request_add_sibling()
        elif index == 1:                    # Add a child.
            self._request_add_child()
        elif index == 2:                    # Remove from profile.
            self._request_delete_from_profile()
        elif index == 3:                    # Save profile.
            self._dtc_profile.save_profile(self._revision_id)
        elif index == 5:
            self._request_add_definition()
        elif index == 6:
            self._request_delete_definition()
        elif index == 7:
            self._request_save_definitions()

        button.handler_unblock(self._lst_handler_id[index])

        return False

    def _request_add_sibling(self):         # pylint: disable=R0914
        """
        Method to add a sibling item to the selected Mission, Phase, or
        Environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (_model, _row) = self.tvwUsageProfile.get_selection().get_selected()
        try:
            _level = _model.get_value(_row, 9)
        except TypeError:
            _return = True

        _usage_model = self._dtc_profile.dicProfiles[self._revision_id]

        if _level == 1:                     # id = Mission ID
            _piter = _model.iter_parent(_row)
            (__, _error_code,
             _mission_id) = self._dtc_profile.add_mission(self._revision_id)
            _attributes = _usage_model.dicMissions[_mission_id].get_attributes()
            _icon = Configuration.ICON_DIR + '32x32/mission.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = (_icon, _attributes[0], _attributes[3], '', _attributes[2],
                     0.0, _attributes[1], 0.0, 0.0, 1, 0, 0)
            if _error_code != 0:
                _prompt = _(u"An error occurred when attempting to add a new "
                            u"mission to the usage profile for Revision "
                            u"{0:d}").format(self._revision_id)
                _return = True

        elif _level == 2:                   # id = Phase ID
            _piter = _model.iter_parent(_row)
            _mission_id = _model.get_value(_piter, 1)
            (__, _error_code,
             _phase_id) = self._dtc_profile.add_phase(self._revision_id,
                                                      _mission_id)
            _mission = _usage_model.dicMissions[_mission_id]
            _attributes = _mission.dicPhases[_phase_id].get_attributes()
            _icon = Configuration.ICON_DIR + '32x32/phase.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = (_icon, _attributes[2], _attributes[5], _attributes[6], '',
                     _attributes[3], _attributes[4], 0.0, 0.0, 2, 0, 1)
            if _error_code != 0:
                _prompt = _(u"An error occurred when attempting to add a new "
                            u"phase to mission {0:d}").format(_mission_id)
                _return = True

        elif _level == 3:                   # id = Environment ID
            _piter = _model.iter_parent(_row)
            _phase_id = _model.get_value(_piter, 1)
            _grand_piter = _model.iter_parent(_piter)
            _mission_id = _model.get_value(_grand_piter, 1)
            (__, _error_code,
             _environment_id) = self._dtc_profile.add_environment(self._revision_id,
                                                                  _mission_id,
                                                                  _phase_id)
            _mission = _usage_model.dicMissions[_mission_id]
            _phase = _mission.dicPhases[_phase_id]
            _attributes = _phase.dicEnvironments[_environment_id].get_attributes()
            _icon = Configuration.ICON_DIR + '32x32/environment.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = (_icon, _attributes[4], _attributes[5], '', _attributes[6],
                     _attributes[7], _attributes[8], _attributes[9],
                     _attributes[10], 3, 1, 0)
            if _error_code != 0:
                _prompt = _(u"An error occurred when attempting to add a new "
                            u"environment to mission phase "
                            u"{0:d}").format(_phase_id)
                _return = True

        if not _return:
            # Insert a new row with the new Usage Profile item and then select
            # the newly inserted row for editing.
            _row = _model.insert()
            _path = _model.get_path(_row)
            self.tvwUsageProfile.set_cursor(_path,
                                            self.tvwUsageProfile.get_column(1),
                                            True)
            _column = self.tvwUsageProfile.get_column(0)
            self.tvwUsageProfile.row_activated(_path, _column)
        else:
            Widgets.rtk_error(_prompt)

        return _return

    def _request_add_child(self):           # pylint: disable=R0914
        """
        Method to add a child item to the selected Mission, Phase, or
        Environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (_model, _row) = self.tvwUsageProfile.get_selection().get_selected()
        try:
            _id = _model.get_value(_row, 1)
            _level = _model.get_value(_row, 9)
        except TypeError:
            _return = True

        _usage_model = self._dtc_profile.dicProfiles[self._revision_id]

        if _level == 1:                     # _id = Mission ID
            _piter = _row
            (__, _error_code,
             _phase_id) = self._dtc_profile.add_phase(self._revision_id, _id)
            _mission = _usage_model.dicMissions[_id]
            _attributes = _mission.dicPhases[_phase_id].get_attributes()
            _icon = Configuration.ICON_DIR + '32x32/phase.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = (_icon, _attributes[2], _attributes[5], _attributes[6], '',
                     _attributes[3], _attributes[4], 0.0, 0.0, 2, 0, 1)
            if _error_code != 0:
                _prompt = _(u"An error occurred when attempting to add a new "
                            u"phase to mission {0:d}").format(_id)
                _return = True

        elif _level == 2:                   # _id = Phase ID
            _piter = _model.iter_parent(_row)
            _mission_id = _model.get_value(_piter, 1)
            _piter = _row
            (__, _error_code,
             _environment_id) = self._dtc_profile.add_environment(self._revision_id,
                                                                  _mission_id,
                                                                  _id)
            _mission = _usage_model.dicMissions[_mission_id]
            _phase = _mission.dicPhases[_id]
            _attributes = _phase.dicEnvironments[_environment_id].get_attributes()
            _icon = Configuration.ICON_DIR + '32x32/environment.png'
            _icon = gtk.gdk.pixbuf_new_from_file_at_size(_icon, 22, 22)
            _data = (_icon, _attributes[4], _attributes[5], '', _attributes[6],
                     _attributes[7], _attributes[8], _attributes[9],
                     _attributes[10], 3, 1, 0)
            if _error_code != 0:
                _prompt = _(u"An error occurred when attempting to add a new "
                            u"environment to mission phase {0:d} of mission "
                            u"{1:d}").format(_id, _mission_id)
                _return = True

        else:
            Widgets.rtk_information(_(u"You cannot add a child object to "
                                      u"an environmental condition in a "
                                      u"usage profile."))
            _return = True

        if not _return:
            # Insert a new row with the new Usage Profile item and then select
            # the newly inserted row for editing.
            _row = _model.insert()
            _path = _model.get_path(_row)
            self.tvwUsageProfile.set_cursor(_path,
                                            self.tvwUsageProfile.get_column(1),
                                            True)
            _column = self.tvwUsageProfile.get_column(0)
            self.tvwUsageProfile.row_activated(_path, _column)
        else:
            Widgets.rtk_error(_prompt)

        return _return

    def _request_delete_from_profile(self):
        """
        Method to delete the selected item from the Usage Profile.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (_model, _row) = self.tvwUsageProfile.get_selection().get_selected()
        try:
            _id = _model.get_value(_row, 1)
            _level = _model.get_value(_row, 9)
        except TypeError:
            _return = True

        if _level == 1:                     # _id = Mission ID
            _piter = None
            _prompt = _(u"An error occurred when attempting to delete mission "
                        u"{0:d} from revision {1:d}").format(_id,
                                                             self._revision_id)
            (_results,
             _error_code) = self._dtc_profile.delete_mission(self._revision_id,
                                                             _id)

        elif _level == 2:                   # _id = Phase ID
            _piter = _model.iter_parent(_row)
            _mission_id = _model.get_value(_piter, 1)
            _prompt = _(u"An error occurred when attempting to delete phase "
                        u"{0:d} from mission {1:d}").format(_id, _mission_id)
            (_results,
             _error_code) = self._dtc_profile.delete_phase(self._revision_id,
                                                           _mission_id, _id)

        elif _level == 3:                   # _id = Environment ID
            _piter = _model.iter_parent(_row)
            _phase_id = _model.get_value(_piter, 1)
            _grand_piter = _model.iter_parent(_piter)
            _mission_id = _model.get_value(_grand_piter, 1)
            _prompt = _(u"An error occurred when attempting to delete "
                        u"environment {0:d} from phase {1:d} of mission "
                        u"{2:d}").format(_id, _phase_id, _mission_id)
            (_results,
             _error_code) = self._dtc_profile.delete_environment(self._revision_id,
                                                                 _mission_id,
                                                                 _phase_id,
                                                                 _id)

        if _error_code != 0:
            try:
                _path = _model.get_path(_model.iter_next(_piter))
            except TypeError:
                _path = None
            self._load_usage_profile(_path)
        else:
            Widgets.rtk_error(_prompt)
            _return = True

        return _return

    def _request_add_definition(self):
        """
        Method to add a Failure Definition.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (__,
         _error_code,
         __) = self._dtc_definitions.add_definition(self._revision_id)
        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to add a failure "
                        u"definition to revision "
                        u"{0:d}").format(self._revision_id)
            _return = True
        else:
            self._load_failure_definitions(self._revision_id)

        if _return:
            Widgets.rtk_error(_prompt)

        return _return

    def _request_delete_definition(self):
        """
        Method to delete the selected Failure Definition.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (_model,
         _row) = self.tvwFailureDefinition.get_selection().get_selected()
        try:
            _id = _model.get_value(_row, 1)
        except TypeError:
            _return = True

        (__,
         _error_code,
         __) = self._dtc_definitions.delete_definition(self._revision_id, _id)
        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to delete failure "
                        u"definition {0:d}").format(_id)
            _return = True
        else:
            self._load_failure_definitions(self._revision_id)

        if _return:
            Widgets.rtk_error(_prompt)

        return _return

    def _request_save_definitions(self):
        """
        Method to save the Failure Definitions.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        (__,
         _error_code,
         __) = self._dtc_definitions.save_definitions(self._revision_id)
        if _error_code != 0:
            _prompt = _(u"An error occurred when attempting to save the "
                        u"failure definitions.")
            _return = True

        if _return:
            Widgets.rtk_error(_prompt)

        return _return

    def _on_usage_row_changed(self, treeview):
        """
        Method to handle events for the Revision package List Book Usage
        Profile gtk.TreeView().  It is called whenever a List Book Usage
        Profile gtk.TreeView() row is activated.

        :param gtk.TreeView treeview: the Revision classt gtk.TreeView().
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self.tvwUsageProfile.handler_block(self._lst_handler_id[4])

        (_model, _row) = treeview.get_selection().get_selected()
        _level = _model.get_value(_row, 9)

        _columns = treeview.get_columns()

        # Change the column headings depending on what is being selected.
        if _level == 1:                         # Mission
            _headings = [_(u"Mission ID"), _(u"Description"), _(u"Units"),
                         _(u"Start Time"), _(u"End Time"), _(u""), _(u""),
                         _(u"")]
        elif _level == 2:                       # Mission phase
            _headings = [_(u"Phase ID"), _(u"  Code\t\tDescription"),
                         _(u"Units"), _(u"Start Time"), _(u"End Time"), _(u""),
                         _(u""), _(u"")]
        elif _level == 3:                       # Environment
            _headings = [_(u"Environment ID"), _(u"Condition"), _(u"Units"),
                         _(u"Minimum Value"), _(u"Maximum Value"),
                         _(u"Mean Value"), _(u"Variance"), _(u"")]

        for i in range(7):
            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _headings[i] +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _columns[i].set_widget(_label)

        self.tvwUsageProfile.handler_unblock(self._lst_handler_id[4])

        return False

    def _on_usage_cell_edited(self, __cell, path, new_text, position, model):
        """
        Method to handle edits of the Revision package List Book Usage Profile
        gtk.Treeview()s.

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param gtk.TreeModel model: the gtk.TreeModel() the gtk.CellRenderer()
                                    belongs to.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _row = model.get_iter(path)
        _id = model.get_value(_row, 1)

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))
        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        _usage_model = self._dtc_profile.dicProfiles[self._revision_id]
        # Determine whether we are editing a mission, mission phase, or
        # environment.  Get the values and update the attributes.
        _level = model.get_value(_row, 9)
        if _level == 1:                     # Mission
            _values = (self._revision_id, _id) + model.get(_row, 6, 4, 2)
            _mission = _usage_model.dicMissions[_id]
            _mission.set_attributes(_values)
        elif _level == 2:                   # Mission phase
            _values = model.get(_row, 5, 6, 2, 3)
            _row = model.iter_parent(_row)
            _mission_id = model.get_value(_row, 1)
            _mission = _usage_model.dicMissions[_mission_id]
            _values = (self._revision_id, _mission_id, _id) + _values
            _phase = _mission.dicPhases[_id]
            _phase.set_attributes(_values)
        elif _level == 3:                   # Environment
            _values = model.get(_row, 2, 4, 5, 6, 7, 8)
            _row = model.iter_parent(_row)
            _phase_id = model.get_value(_row, 1)
            _row = model.iter_parent(_row)
            _mission_id = model.get_value(_row, 1)
            _mission = _usage_model.dicMissions[_mission_id]
            _phase = _mission.dicPhases[_phase_id]
            _values = (self._revision_id, _mission_id, _phase_id, 0, _id) + \
                _values
            _environment = _phase.dicEnvironments[_id]
            _environment.set_attributes(_values)

        return False

    def _on_failure_cell_edited(self, __cell, path, new_text, position, model):
        """
        Method to handle edits of the Revision package List Book Failure
        Definition gtk.Treeview()s.

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

        _row = model.get_iter(path)
        _id = model.get_value(_row, 0)

        # Update the gtk.TreeModel() with the new value.
        _type = gobject.type_name(model.get_column_type(position))

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        if position == 1:
            self._dtc_definitions.dicDefinitions[self._revision_id][_id].definition = str(new_text)

        return False
