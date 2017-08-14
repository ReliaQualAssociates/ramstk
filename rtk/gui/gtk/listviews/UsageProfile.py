#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.UsageProfile.py is part of the RTK Project
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
###############################################################################
Usage Profile Package List Book View
###############################################################################
"""

import sys

# Import modules for localization support.
import gettext
import locale

from pubsub import pub
from sortedcontainers import SortedDict

# Modules required for the GUI.
import pango
try:
    # noinspection PyUnresolvedReferences
    from pygtk import require
    require('2.0')
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    from gtk import JUSTIFY_CENTER, HBox, ToolButton, Label, \
        TREE_VIEW_COLUMN_AUTOSIZE, Image, gdk, TreeStore, TreeViewColumn, \
        ScrolledWindow, CellRendererText, TreeView, VBox, CellRendererPixbuf, \
        Toolbar
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    import gtk.glade
except ImportError:
    sys.exit(1)
try:
    # noinspection PyUnresolvedReferences
    from gobject import type_name, TYPE_INT, TYPE_STRING, TYPE_FLOAT
except ImportError:
    sys.exit(1)

# Import other RTK modules.
from gui.gtk import rtk

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

_ = gettext.gettext


class ListView(gtk.VBox):
    """
    The List View displays all the matrices and lists associated with the
    Revision Class.  The attributes of a List View are:

    :ivar _lst_handler_id: the list of gtk.Widget() signal IDs.
    :ivar _mdcRTK: the current instance of the RTK master data controller.
    :ivar _dtc_usage_profile: the
                              :py:class:`rtk.usage.UsageProfile.UsageProfile`
                              data controller associated with this ListView.
    :ivar _revision_id: the Revision ID whose information is being displayed
                        in the ModuleBook.
    :ivar tvw_profile: the :py:class:`gtk.TreeView` to display the Usage
                       Profiles for the selected Revision.
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Revision package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        VBox.__init__(self)

        # Initialize private dictionary attributes.
        self._dic_icons = {'tab':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/revision.png',
                           'mission':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/mission.png',
                           'phase':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/phase.png',
                           'environment':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/environment.png',
                           'sibling':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/insert_sibling.png',
                           'child':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/insert_child.png',
                           'remove':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/remove.png',
                           'save':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/save.png',
                           'error':
                           controller.RTK_CONFIGURATION.RTK_ICON_DIR +
                           '/32x32/error.png'}

        # Initialize private list attributes.
        self._lst_handler_id = []

        # Initialize private scalar attributes.
        self._mdcRTK = controller
        self._dtc_usage_profile = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.tvw_profile = TreeView()

        try:
            locale.setlocale(locale.LC_ALL,
                             controller.RTK_CONFIGURATION.RTK_LOCALE)
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')

        _model = TreeStore(gdk.Pixbuf, TYPE_INT,
                           TYPE_STRING, TYPE_STRING,
                           TYPE_STRING, TYPE_FLOAT,
                           TYPE_FLOAT, TYPE_FLOAT,
                           TYPE_FLOAT, TYPE_INT,
                           TYPE_INT, TYPE_STRING)
        self.tvw_profile.set_model(_model)

        for i in range(10):
            _column = TreeViewColumn()
            if i == 0:
                _cell = CellRendererPixbuf()
                _cell.set_property('xalign', 0.5)
                _column.pack_start(_cell, False)
                _column.set_attributes(_cell, pixbuf=0)

                _cell = CellRendererText()
                _cell.set_property('background', 'light gray')
                _cell.set_property('editable', 0)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=1)

                _column.set_visible(True)
            elif i == 1:
                _cell = CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edited, 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

                _cell = CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edited, 3, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, visible=11)

                _column.set_visible(True)
            elif i == 2:
                _cell = CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edited, 4, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=4)
                _column.set_visible(True)
            elif i == 3 or i == 4:
                _cell = CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edited, i + 2,
                              _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2)
                _column.set_visible(True)
            elif i == 5 or i == 6:
                _cell = CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._on_cell_edited, i + 2,
                              _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2, visible=10)
                _column.set_visible(True)
            else:
                _cell = CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _cell = CellRendererText()
                _cell.set_property('editable', 0)
                _column.pack_start(_cell, True)

                _column.set_visible(False)

            _column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
            self.tvw_profile.append_column(_column)

        self.tvw_profile.set_rubber_banding(True)
        self.tvw_profile.set_tooltip_text(
                _(u"Displays the list of usage profiles for the selected "
                  u"revision."))
        self._lst_handler_id.append(
                self.tvw_profile.connect('cursor_changed',
                                         self._on_row_changed))
        self._lst_handler_id.append(
                self.tvw_profile.connect('button_press_event',
                                         self._on_button_press))

        _icon = gdk.pixbuf_new_from_file_at_size(self._dic_icons['tab'],
                                                 22, 22)
        _image = Image()
        _image.set_from_pixbuf(_icon)

        _label = Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Usage\nProfiles") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays usage profiles for the selected "
                                  u"revision."))

        self.hbx_tab_label = HBox()
        # self.hbx_tab_label.pack_start(_image)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _toolbar = self._create_toolbar()

        _scrolledwindow = ScrolledWindow()
        _scrolledwindow.add(self.tvw_profile)

        self.pack_start(_toolbar, expand=False, fill=False)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')

    def _create_toolbar(self):
        """
        Creates the toolbar for the Usage Profile ListView.

        :return: _toolbar: the gtk.Toolbar() for the Usage Profile
                          ListView.
        :rtype: :py:class:`gtk.Toolbar`
        """

        _toolbar = Toolbar()

        _position = 0

        # Add a new sibling entity.
        _button = ToolButton()
        _button.set_tooltip_text(_(u"Add a new sibling entity to the selected "
                                   u"entity."))
        _image = Image()
        _image.set_from_file(self._dic_icons['sibling'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_insert, True)
        _toolbar.insert(_button, _position)
        _position += 1

        # Add a new child entity.
        _button = ToolButton()
        _button.set_tooltip_text(_(u"Add a new child entity to the selected "
                                   u"entity."))
        _image = Image()
        _image.set_from_file(self._dic_icons['child'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_insert, False)
        _toolbar.insert(_button, _position)
        _position += 1

        # Delete button
        _button = ToolButton()
        _button.set_tooltip_text(_(u"Deletes the selected entity from the "
                                   u"usage profile."))
        _image = Image()
        _image.set_from_file(self._dic_icons['remove'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_delete)
        _toolbar.insert(_button, _position)
        _position += 1

        # Save button
        _button = ToolButton()
        _button.set_tooltip_text(_(u"Save changes to the usage profile."))
        _image = Image()
        _image.set_from_file(self._dic_icons['save'])
        _button.set_icon_widget(_image)
        _button.connect('clicked', self._request_update_all)
        _toolbar.insert(_button, _position)

        _toolbar.show_all()

        return _toolbar

    def _load_tree(self, tree, row=None):
        """
        Method to recursively load the Usage Profile List View's gtk.TreeModel
        with the Usage Profile tree.

        :param tree: the Usage Profile treelib Tree().
        :type tree: :py:class:`treelib.Tree`
        :param row: the parent row in the Usage Profile gtk.TreeView() to
                    add the new item.
        :type row: :py:class:`gtk.TreeIter`
        :return: None
        :rtype: None
        """

        _data = []
        _model = self.tvw_profile.get_model()

        _node = tree.nodes[SortedDict(tree.nodes).keys()[0]]
        _entity = _node.data

        try:
            if _entity.is_mission:
                _icon = gdk.pixbuf_new_from_file_at_size(
                        self._dic_icons['mission'], 22, 22)
                _data = [_icon, _entity.mission_id, _entity.description, '',
                         _entity.time_units, 0.0, _entity.mission_time, 0.0,
                         0.0, _node.identifier, 0, 'mission']
                _row = None

            elif _entity.is_phase:
                _icon = gdk.pixbuf_new_from_file_at_size(
                        self._dic_icons['phase'], 22, 22)
                _data = [_icon, _entity.phase_id, _entity.name,
                         _entity.description, '', _entity.phase_start,
                         _entity.phase_end, 0.0, 0.0, _node.identifier, 0,
                         'phase']

            elif _entity.is_env:
                _icon = gdk.pixbuf_new_from_file_at_size(
                        self._dic_icons['environment'], 22, 22)
                _data = [_icon, _entity.environment_id, _entity.name, '',
                         _entity.units, _entity.minimum, _entity.maximum,
                         _entity.mean, _entity.variance, _node.identifier,
                         1, 'environment']

            try:
                _row = _model.append(row, _data)
            except TypeError:
                print "FIXME: Handle TypeError in gtk.gui.listview.UsageProfile.UsageProfile._load_tree"

        except AttributeError:
            _row = None

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._load_tree(_child_tree, _row)

        return None

    def _on_select_revision(self, revision_id):
        """
        Method to load the Usage Profile List View gtk.TreeModel() with
        Usage Profile information whenever a new Revision is selected.

        :param int revision_id: the Revision ID to select the Failure
                                Definitions for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model = self.tvw_profile.get_model()
        _model.clear()

        self._dtc_usage_profile = self._mdcRTK.dic_controllers['profile']
        _profile = self._dtc_usage_profile.request_select_all(revision_id)

        self._load_tree(_profile)

        _row = _model.get_iter_root()
        self.tvw_profile.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.tvw_profile.get_column(0)
            self.tvw_profile.set_cursor(_path, None, False)
            self.tvw_profile.row_activated(_path, _column)

        self._revision_id = revision_id

        return _return

    @staticmethod
    def _on_button_press(__treeview, event):
        """
        Method for handling mouse clicks on the Usage Profile package
        ListView gtk.TreeView().

        :param __treeview: the Usage Profile ListView gtk.TreeView().
        :type __treeview: :py:class:`gtk.TreeView`.
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backward
                      * 8 =
                      * 9 =

        :type event: :py:class:`gtk.gdk.Event`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if event.button == 1:
            pass
        elif event.button == 3:
            # FIXME: See bug 190.
            pass

        return False

    def _on_cell_edited(self, __cell, path, new_text, position, model):
        """
        Method to handle edits of the Revision package Module Book
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
        _type = type_name(model.get_column_type(position))
        _node_id = model[path][9]

        if _type == 'gchararray':
            model[path][position] = str(new_text)
        elif _type == 'gint':
            model[path][position] = int(new_text)
        elif _type == 'gfloat':
            model[path][position] = float(new_text)

        # Retrieve the Usage Profile data package.
        _entity = \
            self._dtc_usage_profile.request_select(_node_id)

        # Build a list of attributes based on the type of data package.
        _attributes = []
        if _entity.is_mission:
            for i in [2, 6, 4]:
                _attributes.append(model[path][i])
        elif _entity.is_phase:
            for i in [3, 2, 5, 6]:
                _attributes.append(model[path][i])
        elif _entity.is_env:
            for i in [2, 4, 5, 6, 7, 8]:
                _attributes.append(model[path][i])
            _attributes.append(_entity.ramp_rate)
            _attributes.append(_entity.low_dwell_time)
            _attributes.append(_entity.high_dwell_time)

        _entity.set_attributes(_attributes)

        return False

    def _on_row_changed(self, treeview):
        """
        Method to handle events for the Usage Profile List View
        gtk.TreeView().  It is called whenever a List View gtk.TreeView()
        row is activated.

        :param treeview: the Usage Profile ListView class gtk.TreeView().
        :type treeview: :py:class:`gtk.TreeView`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self.tvw_profile.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()
        try:
            _level = _model.get_value(_row, 11)
        except TypeError:
            _level = None

        _columns = treeview.get_columns()

        # Change the column headings depending on what is being selected.
        if _level == 'mission':
            _headings = [_(u"Mission ID"), _(u"Description"), _(u"Units"),
                         _(u"Start Time"), _(u"End Time"), _(u""), _(u""),
                         _(u"")]
        elif _level == 'phase':
            _headings = [_(u"Phase ID"), _(u"  Code\t\tDescription"),
                         _(u"Units"), _(u"Start Time"), _(u"End Time"), _(u""),
                         _(u""), _(u"")]
        elif _level == 'environment':
            _headings = [_(u"Environment ID"), _(u"Condition"), _(u"Units"),
                         _(u"Minimum Value"), _(u"Maximum Value"),
                         _(u"Mean Value"), _(u"Variance"), _(u"")]
        else:
            _headings = []

        i = 0
        for _heading in _headings:
            _label = Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _heading +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _columns[i].set_widget(_label)

            i += 1

        self.tvw_profile.handler_unblock(self._lst_handler_id[0])

        return _return

    def _request_insert(self, __button, sibling=True):
        """
        Method to add a Mission, Mission Phase, or Environment to the Usage
        Profile.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :param bool sibling: indicator variable that determines whether a
                             sibling entity be added (default) or a child
                             entity be added to the currently selected entity.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self.tvw_profile.get_selection().get_selected()
        _level = _model.get_value(_row, 11)
        _prow = _model.iter_parent(_row)

        if sibling:
            if _level == 'mission':
                _entity_id = self._revision_id
                _parent_id = 0
            else:
                _entity_id = _model.get_value(_prow, 1)
                _parent_id = _model.get_value(_prow, 9)
        else:
            _entity_id = _model.get_value(_row, 1)
            _parent_id = _model.get_value(_row, 9)

        if _level == 'mission' and not sibling:
            _level = 'phase'

        elif _level == 'phase' and not sibling:
            _level = 'environment'

        elif _level == 'environment' and not sibling:
            _prompt = _(u"An environmental condition cannot have a child.")
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        if (not _return and
                not self._dtc_usage_profile.request_insert(_entity_id,
                                                           _parent_id,
                                                           _level)):
            self._on_select_revision(self._revision_id)
        else:
            _return = True

        return _return

    def _request_delete(self, __button):
        """
        Method to delete the selected Mission, Mission Phase, or Environment
        and any children from the Usage Profile.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model, _row = self.tvw_profile.get_selection().get_selected()
        _node_id = _model.get_value(_row, 9)
        _level = _model.get_value(_row, 11)

        if not self._dtc_usage_profile.request_delete(_node_id):
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"A problem occurred while attempting to delete {0:s} "
                        u"with ID {1:d}.").format(_level.title(), _node_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _request_update_all(self, __button):
        """
        Method to save all the Usage Profiles.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_usage_profile.request_update_all()
