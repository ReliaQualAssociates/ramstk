# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.UsageProfile.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""
###############################################################################
Usage Profile Package List Book View
###############################################################################
"""

from pubsub import pub                          # pylint: disable=E0401
from sortedcontainers import SortedDict         # pylint: disable=E0401

# Modules required for the GUI.
import pango                                    # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk                         # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gobject, gtk  # pylint: disable=E0401,W0611
from .ListView import RTKListView


class ListView(RTKListView):
    """
    The Usage Profile List View displays all the usage profiles associated with
    the selected Revision.  The attributes of a Usage Profile List View are:

    :ivar _dtc_usage_profile: the
                              :py:class:`rtk.usage.UsageProfile.UsageProfile`
                              data controller associated with this List View.
    :ivar _revision_id: the Revision ID whose Usage Profiles are being
                        displayed in the List View.
    """

    def __init__(self, controller):
        """
        Method to initialize the List View for the Revision package.

        :param controller: the RTK master data controller instance.
        :type controller: :py:class:`rtk.RTK.RTK`
        """

        RTKListView.__init__(self, controller)

        # Initialize private dictionary attributes.
        self._dic_icons['mission'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/mission.png'
        self._dic_icons['phase'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + '/32x32/phase.png'
        self._dic_icons['environment'] = \
            controller.RTK_CONFIGURATION.RTK_ICON_DIR + \
            '/32x32/environment.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._dtc_usage_profile = None
        self._revision_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self._make_treeview()
        self.treeview.set_rubber_banding(True)
        self.treeview.set_tooltip_text(
            _(u"Displays the list of usage profiles for the selected "
              u"revision."))
        self._lst_handler_id.append(
            self.treeview.connect('cursor_changed',
                                  self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event',
                                  self._on_button_press))

        # _icon = gdk.pixbuf_new_from_file_at_size(self._dic_icons['tab'],
        #                                          22, 22)
        # _image = Image()
        # _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" +
                          _(u"Usage\nProfiles") + "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(_(u"Displays usage profiles for the selected "
                                  u"revision."))

        # self.hbx_tab_label.pack_start(_image)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)

        self.pack_start(self._make_toolbar(), expand=False, fill=False)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')

    def _do_change_row(self, treeview):
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

        self.treeview.handler_block(self._lst_handler_id[0])

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
            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _heading +
                              "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _columns[i].set_widget(_label)

            i += 1

        self.treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Method to handle edits of the Usage Profile List View gtk.Treeview().

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

        _return = False

        if not RTKListView._do_edit_cell(__cell, path, new_text, position,
                                         model):

            # Retrieve the Usage Profile data package.
            _node_id = model[path][9]
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

            pub.sendMessage('editedUsageProfile')
        else:
            _return = True

        return _return

    def _do_load_tree(self, tree, row=None):
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
        _model = self.treeview.get_model()

        _node = tree.nodes[SortedDict(tree.nodes).keys()[0]]
        _entity = _node.data

        try:
            if _entity.is_mission:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['mission'], 22, 22)
                _data = [_icon, _entity.mission_id, _entity.description, '',
                         _entity.time_units, 0.0, _entity.mission_time, 0.0,
                         0.0, _node.identifier, 0, 'mission']
                _row = None

            elif _entity.is_phase:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['phase'], 22, 22)
                _data = [_icon, _entity.phase_id, _entity.name,
                         _entity.description, '', _entity.phase_start,
                         _entity.phase_end, 0.0, 0.0, _node.identifier, 0,
                         'phase']

            elif _entity.is_env:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['environment'], 22, 22)
                _data = [_icon, _entity.environment_id, _entity.name, '',
                         _entity.units, _entity.minimum, _entity.maximum,
                         _entity.mean, _entity.variance, _node.identifier,
                         1, 'environment']

            try:
                _row = _model.append(row, _data)
            except TypeError:
                print "FIXME: Handle TypeError in " \
                      "gtk.gui.listview.UsageProfile.UsageProfile._load_tree"

        except AttributeError:
            _row = None

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, _row)

        return None

    def _do_request_delete(self, __button):
        """
        Method to delete the selected Mission, Mission Phase, or Environment
        and any children from the Usage Profile.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
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

    def _do_request_insert(self, __button, sibling=True):
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
        _model, _row = self.treeview.get_selection().get_selected()
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

    def _do_request_update_all(self, __button):
        """
        Method to save all the Usage Profiles.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :py:class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        return self._dtc_usage_profile.request_update_all()

    def _make_toolbar(self):
        """
        Method to create the toolbar for the Usage Profile ListView.

        :return: _toolbar: the gtk.Toolbar() for the Usage Profile
                           List View.
        :rtype: :py:class:`gtk.Toolbar`
        """

        _icons = ['insert_sibling', 'insert_child', 'remove', 'save']
        _toolbar, _position = RTKListView._make_toolbar(self, _icons,
                                                        'vertical', 56, 56)

        _button = _toolbar.get_nth_item(0)
        _button.set_tooltip_text(_(u"Add a new sibling entity to the selected "
                                   u"entity."))
        _button.connect('clicked', self._do_request_insert, True)

        _button = _toolbar.get_nth_item(1)
        _button.set_tooltip_text(_(u"Add a new child entity to the selected "
                                   u"entity."))
        _button.connect('clicked', self._do_request_insert, False)

        _button = _toolbar.get_nth_item(2)
        _button.set_tooltip_text(_(u"Deletes the selected entity from the "
                                   u"usage profile."))
        _button.connect('clicked', self._do_request_delete)

        _button = _toolbar.get_nth_item(3)
        _button.set_tooltip_text(_(u"Save changes to the usage profile."))
        _button.connect('clicked', self._do_request_update_all)

        _toolbar.show_all()

        return _toolbar

    def _make_treeview(self):
        """
        Method for setting up the gtk.TreeView() for Failure Definitions.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        _model = gtk.TreeStore(gtk.gdk.Pixbuf, gobject.TYPE_INT,
                               gobject.TYPE_STRING, gobject.TYPE_STRING,
                               gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
                               gobject.TYPE_FLOAT, gobject.TYPE_INT,
                               gobject.TYPE_INT, gobject.TYPE_STRING)
        self.treeview.set_model(_model)

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
                _cell.connect('edited', self._do_edit_cell, 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._do_edit_cell, 3, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, visible=11)

                _column.set_visible(True)
            elif i == 2:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._do_edit_cell, 4, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=4)
                _column.set_visible(True)
            elif i == 3 or i == 4:
                _cell = gtk.CellRendererText()
                _cell.set_property('editable', 1)
                _cell.set_property('wrap-width', 250)
                _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
                _cell.set_property('yalign', 0.1)
                _cell.connect('edited', self._do_edit_cell, i + 2,
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
                _cell.connect('edited', self._do_edit_cell, i + 2,
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
            self.treeview.append_column(_column)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Method for handling mouse clicks on the Usage Profile package
        ListView gtk.TreeView().

        :param treeview: the Usage Profile ListView gtk.TreeView().
        :type treeview: :py:class:`gtk.TreeView`.
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

        treeview.handler_block(self._lst_handler_id[0])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            print "FIXME: Rick clicking should launch a pop-up menu with " \
                  "options to insert sibling, insert child, delete " \
                  "(selected), and save all in " \
                  "rtk.gui.gtk.listviews.UsageProfile._on_button_press."

        treeview.handler_unblock(self._lst_handler_id[0])

        return False

    def _on_select_revision(self, revision_id):
        """
        Method to load the Usage Profile List View gtk.TreeModel() with
        Usage Profile information whenever a new Revision is selected.

        :param int revision_id: the Revision ID to select the Usage Profiles
                                for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _return = False

        self._dtc_usage_profile = self._mdcRTK.dic_controllers['profile']
        _profile = self._dtc_usage_profile.request_select_all(revision_id)

        _model = self.treeview.get_model()
        _model.clear()

        self._do_load_tree(_profile)

        _row = _model.get_iter_root()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

        self.treeview.expand_all()
        self._revision_id = revision_id

        return _return
