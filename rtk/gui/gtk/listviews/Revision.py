#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.Revision.py is part of the RTK Project
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
    # noinspection PyUnresolvedReferences
    import pygtk
    pygtk.require('2.0')
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gobject
except ImportError:
    sys.exit(1)

# Import other RTK modules.
try:
    import gui.gtk.Widgets as Widgets
    from gui.gtk.listviews.UsageProfile import ListView as lvwUsageProfile
    from gui.gtk.listviews.FailureDefinition \
        import ListView as lvwFailureDefinition
except ImportError:
    import rtk.gui.gtk.Widgets as Widgets       # pylint: disable=E0401
    from rtk.gui.gtk.listviews.UsageProfile import ListView as lvwUsageProfile
    from rtk.gui.gtk.listviews.FailureDefinition \
        import ListView as lvwFailureDefinition

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "Weibullguy" Rowland'

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

    def __init__(self, controller):
        """
        Method to initialize the List View for the Revision package.

        :param controller: the RTK Master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        gtk.Notebook.__init__(self)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._configuration = controller.RTK_CONFIGURATION
        self._dtc_revision = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.lvw_usage_profile = lvwUsageProfile(self._mdcRTK)
        self.lvw_failure_definition = lvwFailureDefinition(self._mdcRTK)

        try:
            locale.setlocale(locale.LC_ALL, self._configuration.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        # Set the user's preferred gtk.Notebook tab position.
        if self._configuration.RTK_TABPOS['listbook'] == 'left':
            self.set_tab_pos(gtk.POS_LEFT)
        elif self._configuration.RTK_TABPOS['listbook'] == 'right':
            self.set_tab_pos(gtk.POS_RIGHT)
        elif self._configuration.RTK_TABPOS['listbook'] == 'top':
            self.set_tab_pos(gtk.POS_TOP)
        else:
            self.set_tab_pos(gtk.POS_BOTTOM)

        self.insert_page(self.lvw_usage_profile,
                         tab_label=self.lvw_usage_profile.hbx_tab_label,
                         position=-1)
        self.insert_page(self.lvw_failure_definition,
                         tab_label=self.lvw_failure_definition.hbx_tab_label,
                         position=-1)

        self.show_all()

    def on_module_change(self):
        """
        Method to load the Revision List Book.

        :param int revision_id: the Revision ID to load the List Book for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        #self._revision_id = revision_id
        print "Loaded Revision"

        #self._load_usage_profile()
        #self._load_failure_definitions()

        return False

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
            _icon = self._configuration.ICON_DIR + '32x32/mission.png'
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
            _icon = self._configuration.ICON_DIR + '32x32/phase.png'
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
            _icon = self._configuration.ICON_DIR + '32x32/environment.png'
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
            _row = _model.insert(_piter, -1, _data)
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
            _icon = self._configuration.ICON_DIR + '32x32/phase.png'
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
            _icon = self._configuration.ICON_DIR + '32x32/environment.png'
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
            _row = _model.insert(_piter, -1, _data)
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
