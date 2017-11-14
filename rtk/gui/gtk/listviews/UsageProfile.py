# -*- coding: utf-8 -*-
#
#       rtk.gui.gtk.listviews.UsageProfile.py is part of the RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Usage Profile List View Module."""

from pubsub import pub  # pylint: disable=E0401
from sortedcontainers import SortedDict  # pylint: disable=E0401

# Modules required for the GUI.
import pango  # pylint: disable=E0401

# Import other RTK modules.
from gui.gtk import rtk  # pylint: disable=E0401
from gui.gtk.rtk.Widget import _, gobject, gtk  # pylint: disable=E0401,W0611
from .ListView import RTKListView


class ListView(RTKListView):
    """
    Display all the Usage Profiles associated with the selected Revision.

    The attributes of a Usage Profile List View are:

    :ivar _revision_id: the Revision ID whose Usage Profiles are being
                        displayed in the List View.
    """

    def __init__(self, controller):
        """
        Initialize the List View for the Usage Profile.

        :param controller: the RTK master data controller instance.
        :type controller: :class:`rtk.RTK.RTK`
        """
        RTKListView.__init__(self, controller, module='usage_profile')

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
            self.treeview.connect('cursor_changed', self._do_change_row))
        self._lst_handler_id.append(
            self.treeview.connect('button_press_event', self._on_button_press))

        # _icon = gdk.pixbuf_new_from_file_at_size(self._dic_icons['tab'],
        #                                          22, 22)
        # _image = Image()
        # _image.set_from_pixbuf(_icon)

        _label = gtk.Label()
        _label.set_markup("<span weight='bold'>" + _(u"Usage\nProfiles") +
                          "</span>")
        _label.set_alignment(xalign=0.5, yalign=0.5)
        _label.set_justify(gtk.JUSTIFY_CENTER)
        _label.show_all()
        _label.set_tooltip_text(
            _(u"Displays usage profiles for the selected "
              u"revision."))

        # self.hbx_tab_label.pack_start(_image)
        self.hbx_tab_label.pack_end(_label)
        self.hbx_tab_label.show_all()

        _scrolledwindow = gtk.ScrolledWindow()
        _scrolledwindow.add(self.treeview)

        self.pack_start(self._make_buttonbox(), expand=False, fill=False)
        self.pack_end(_scrolledwindow, expand=True, fill=True)

        self.show_all()

        pub.subscribe(self._on_select_revision, 'selectedRevision')

    def _do_change_row(self, treeview):
        """
        Handle row changes for the Usage Profile package List View.

        This method is called whenever a Usage Profile List View
        RTKTreeView() row is activated or changed.

        :param treeview: the Usage Profile List View class RTK.TreeView().
        :type treeview: :class:`rtk.gui.gtk.TreeView.RTKTreeView`
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
            _headings = [
                _(u"Mission ID"),
                _(u"Description"),
                _(u"Units"),
                _(u"Start Time"),
                _(u"End Time"),
                _(u""),
                _(u""),
                _(u"")
            ]
        elif _level == 'phase':
            _headings = [
                _(u"Phase ID"),
                _(u"  Code\t\tDescription"),
                _(u"Units"),
                _(u"Start Time"),
                _(u"End Time"),
                _(u""),
                _(u""),
                _(u"")
            ]
        elif _level == 'environment':
            _headings = [
                _(u"Environment ID"),
                _(u"Condition"),
                _(u"Units"),
                _(u"Minimum Value"),
                _(u"Maximum Value"),
                _(u"Mean Value"),
                _(u"Variance"),
                _(u"")
            ]
        else:
            _headings = []

        i = 0
        for _heading in _headings:
            _label = gtk.Label()
            _label.set_line_wrap(True)
            _label.set_alignment(xalign=0.5, yalign=0.5)
            _label.set_justify(gtk.JUSTIFY_CENTER)
            _label.set_markup("<span weight='bold'>" + _heading + "</span>")
            _label.set_use_markup(True)
            _label.show_all()
            _columns[i].set_widget(_label)

            i += 1

        self.treeview.handler_unblock(self._lst_handler_id[0])

        return _return

    def _do_edit_cell(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Usage Profile List View RTKTreeView().

        :param gtk.CellRenderer __cell: the gtk.CellRenderer() that was edited.
        :param str path: the gtk.TreeView() path of the gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited gtk.CellRenderer().
        :param int position: the column position of the edited
                             gtk.CellRenderer().
        :param model: the gtk.TreeModel() the gtk.CellRenderer() belongs to.
        :type model: :class:`gtk.TreeModel`
        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """
        _return = False

        if not RTKListView._do_edit_cell(__cell, path, new_text, position,
                                         model):

            # Retrieve the Usage Profile data package.
            _node_id = model[path][9]
            _entity = \
                self._dtc_data_controller.request_select(_node_id)

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
        Recursively load the Usage Profile List View's gtk.TreeModel.

        :param tree: the Usage Profile treelib Tree().
        :type tree: :class:`treelib.Tree`
        :param row: the parent row in the Usage Profile gtk.TreeView() to
                    add the new item.
        :type row: :class:`gtk.TreeIter`
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
                _data = [
                    _icon, _entity.mission_id, _entity.description, '',
                    _entity.time_units, 0.0, _entity.mission_time, 0.0, 0.0,
                    _node.identifier, 0, 'mission'
                ]
                _row = None

            elif _entity.is_phase:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['phase'], 22, 22)
                _data = [
                    _icon, _entity.phase_id, _entity.name, _entity.description,
                    '', _entity.phase_start, _entity.phase_end, 0.0, 0.0,
                    _node.identifier, 0, 'phase'
                ]

            elif _entity.is_env:
                _icon = gtk.gdk.pixbuf_new_from_file_at_size(
                    self._dic_icons['environment'], 22, 22)
                _data = [
                    _icon, _entity.environment_id, _entity.name, '',
                    _entity.units, _entity.minimum, _entity.maximum,
                    _entity.mean, _entity.variance, _node.identifier, 1,
                    'environment'
                ]

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
        Request to delete the selected Usage Profile record.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 9)
        _level = _model.get_value(_row, 11)

        if not self._dtc_data_controller.request_delete(_node_id):
            self._on_select_revision(self._revision_id)
        else:
            _prompt = _(u"A problem occurred while attempting to delete {0:s} "
                        u"with ID {1:d}.").format(_level.title(), _node_id)
            rtk.RTKMessageDialog(_prompt, self._dic_icons['error'], 'error')

            _return = True

        return _return

    def _do_request_insert(self, __button, sibling=True):
        """
        Request to add an entity to the Usage Profile.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
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

        if (not _return and not self._dtc_data_controller.request_insert(
                _entity_id, _parent_id, _level)):
            self._on_select_revision(self._revision_id)
        else:
            _return = True

        return _return

    def _do_request_update_all(self, __button):
        """
        Request to update all the Usage Profile records.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        return self._dtc_data_controller.request_update_all()

    def _make_buttonbox(self):
        """
        Make the buttonbox for the Usage Profile List View.

        :return: _buttonbox; the gtk.ButtonBox() for the Usage Profile List
                             View.
        :rtype: :class:`gtk.ButtonBox`
        """
        _tooltips = [
            _(u"Add a new Usage Profile entity at the same level "
              u"as the currently selected entity."),
            _(u"Add a new Usage Profile entity one level below the "
              u"currently selected entity."),
            _(u"Remove the curently selected entity from the Usage "
              u"Profile."),
            _(u"Save the Usage Profile to the open RTK Program "
              u"database."),
            _(u"Create the Mission and Usage Profile report.")
        ]
        _callbacks = [
            self._do_request_insert, self._do_request_insert,
            self._do_request_delete, self._do_request_update_all
        ]
        _icons = [
            'insert_sibling', 'insert_child', 'remove', 'save', 'reports'
        ]

        _buttonbox = RTKListView._make_buttonbox(self, _icons, _tooltips,
                                                 _callbacks, 'vertical')

        return _buttonbox

    def _make_cell(self, cell, editable, position, model):
        """
        Make a gtk.CellRenderer() and set it's properties.

        :param str cell: the type of gtk.CellRenderer() to create.
        :param bool editable: indicates whether or not the cell should be
                              editable.
        :param int position: the position of the cell in the gtk.Model().
        :return: _cell
        :rtype: :class:`gtk.CellRenderer`
        """
        _cellrenderers = {
            'pixbuf': gtk.CellRendererPixbuf(),
            'text': gtk.CellRendererText()
        }

        _cell = _cellrenderers[cell]

        if not editable:
            _cell.set_property('cell-background', 'light gray')
        else:
            _cell.connect('edited', self._do_edit_cell, position, model)

        if cell == 'text':
            _cell.set_property('editable', editable)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', pango.WRAP_WORD_CHAR)
            _cell.set_property('yalign', 0.1)

        return _cell

    def _make_treeview(self):
        """
        Set up the RTKTreeView() for the Usage Profile.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        _model = gtk.TreeStore(
            gtk.gdk.Pixbuf, gobject.TYPE_INT, gobject.TYPE_STRING,
            gobject.TYPE_STRING, gobject.TYPE_STRING, gobject.TYPE_FLOAT,
            gobject.TYPE_FLOAT, gobject.TYPE_FLOAT, gobject.TYPE_FLOAT,
            gobject.TYPE_INT, gobject.TYPE_INT, gobject.TYPE_STRING)
        self.treeview.set_model(_model)

        for i in range(10):
            _column = gtk.TreeViewColumn()
            if i == 0:
                _cell = self._make_cell('pixbuf', False, 0, _model)
                _cell.set_property('xalign', 0.5)
                _column.pack_start(_cell, False)
                _column.set_attributes(_cell, pixbuf=0)

                _cell = self._make_cell('text', False, 1, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=1)
                _column.set_visible(True)
            elif i == 1:
                _cell = self._make_cell('text', True, 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

                _cell = self._make_cell('text', True, 3, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, visible=11)
                _column.set_visible(True)
            elif i in [2, 3, 4]:
                _cell = self._make_cell('text', True, i + 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2)
                _column.set_visible(True)
            elif i in [5, 6]:
                _cell = self._make_cell('text', True, i + 2, _model)
                _cell.connect('edited', self._do_edit_cell, i + 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2, visible=10)
                _column.set_visible(True)
            else:
                _cell = self._make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)
                _cell = self._make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)
                _cell = self._make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)
                _cell = self._make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)
                _cell = self._make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)

                _column.set_visible(False)

            _column.set_sizing(gtk.TREE_VIEW_COLUMN_AUTOSIZE)
            self.treeview.append_column(_column)

        return _return

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Usage Profile List View RTKTreeView().

        :param treeview: the Usage Profile ListView gtk.TreeView().
        :type treeview: :class:`gtk.TreeView`.
        :param event: the gtk.gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backward
                      * 8 =
                      * 9 =

        :type event: :class:`gtk.gdk.Event`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _menu = gtk.Menu()
            _menu.popup(None, None, None, event.button, event.time)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_sibling'])
            _menu_item.set_label(_(u"Add Sibling Entity"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['insert_child'])
            _menu_item.set_label(_(u"Add Child Entity"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_insert)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['remove'])
            _menu_item.set_label(_(u"Remove Selected Entity"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_delete)
            _menu_item.show()
            _menu.append(_menu_item)

            _menu_item = gtk.ImageMenuItem()
            _image = gtk.Image()
            _image.set_from_file(self._dic_icons['save'])
            _menu_item.set_label(_(u"Save Usage Profile"))
            _menu_item.set_image(_image)
            _menu_item.set_property('use_underline', True)
            _menu_item.connect('activate', self._do_request_update_all)
            _menu_item.show()
            _menu.append(_menu_item)

        treeview.handler_unblock(self._lst_handler_id[1])

        return False

    def _on_select_revision(self, module_id):
        """
        Load the Usage Profile List View gtk.TreeModel().

        :param int module_id: the Revision ID to select the Usage Profiles for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        self._revision_id = module_id

        # pylint: disable=attribute-defined-outside-init
        # It is defined in RTKBaseView.__init__
        self._dtc_data_controller = self._mdcRTK.dic_controllers['profile']
        _profile = self._dtc_data_controller.request_select_all(
            self._revision_id)

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

        return _return
