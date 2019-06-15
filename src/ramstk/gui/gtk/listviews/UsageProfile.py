# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.listviews.UsageProfile.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Usage Profile List View Module."""

# Third Party Imports
from pubsub import pub
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.gui.gtk import ramstk
from ramstk.gui.gtk.ramstk.Widget import Gdk, GdkPixbuf, GObject, Gtk, Pango, _

# RAMSTK Local Imports
from .ListView import RAMSTKListView


class ListView(RAMSTKListView):
    """
    Display all the Usage Profiles associated with the selected Revision.

    All attributes of a Usage Profile List View are inherited.
    """

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the List View for the Usage Profile.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :py:class:`ramstk.Configuration.Configuration`
        """
        RAMSTKListView.__init__(self, configuration, module='usage_profile')

        # Initialize private dictionary attributes.
        self._dic_icons['mission'] = \
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/mission.png'
        self._dic_icons['phase'] = \
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + '/32x32/phase.png'
        self._dic_icons['environment'] = \
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + \
            '/32x32/environment.png'

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_treeview()
        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_tree, 'deleted_usage_profile')
        pub.subscribe(self._do_load_tree, 'inserted_usage_profile')
        pub.subscribe(self._do_load_tree, 'retrieved_usage_profile')

    def __make_buttonbox(self, **kwargs):  # pylint: disable=unused-argument
        """
        Make the buttonbox for the Usage Profile List View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Usage Profile List
                             View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _(
                "Add a new Usage Profile entity at the same level "
                "as the currently selected entity.",
            ),
            _(
                "Add a new Usage Profile entity one level below the "
                "currently selected entity.",
            ),
            _(
                "Remove the curently selected entity from the Usage "
                "Profile.",
            ),
        ]
        _callbacks = [
            self.do_request_insert_sibling,
            self.do_request_insert_child,
            self._do_request_delete,
        ]
        _icons = [
            'insert_sibling',
            'insert_child',
            'remove',
        ]

        _buttonbox = ramstk.do_make_buttonbox(
            self,
            icons=_icons,
            tooltips=_tooltips,
            callbacks=_callbacks,
            orientation='vertical',
            height=-1,
            width=-1,
        )

        return _buttonbox

    def __make_cell(self, cell, editable, position, model):
        """
        Make a Gtk.CellRenderer() and set it's properties.

        :param str cell: the type of Gtk.CellRenderer() to create.
        :param bool editable: indicates whether or not the cell should be
                              editable.
        :param int position: the position of the cell in the Gtk.Model().
        :return: _cell
        :rtype: :class:`Gtk.CellRenderer`
        """
        _cellrenderers = {
            'pixbuf': Gtk.CellRendererPixbuf(),
            'text': Gtk.CellRendererText(),
        }

        _cell = _cellrenderers[cell]

        if not editable:
            _cell.set_property('cell-background', 'light gray')
        else:
            _cell.connect('edited', self._on_cell_edit, position, model)

        if cell == 'text':
            _cell.set_property('editable', editable)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
            _cell.set_property('yalign', 0.1)

        return _cell

    def __make_treeview(self):
        """
        Set up the RAMSTKTreeView() for the Usage Profile.

        :return: None
        :rtype: None
        """
        _model = Gtk.TreeStore(
            GdkPixbuf.Pixbuf, GObject.TYPE_INT, GObject.TYPE_STRING,
            GObject.TYPE_STRING, GObject.TYPE_STRING, GObject.TYPE_FLOAT,
            GObject.TYPE_FLOAT, GObject.TYPE_FLOAT, GObject.TYPE_FLOAT,
            GObject.TYPE_INT, GObject.TYPE_INT, GObject.TYPE_STRING,
        )
        self.treeview.set_model(_model)

        for i in range(10):
            _column = Gtk.TreeViewColumn()
            if i == 0:
                _cell = self.__make_cell('pixbuf', False, 0, _model)
                _cell.set_property('xalign', 0.5)
                _column.pack_start(_cell, False)
                _column.set_attributes(_cell, pixbuf=0)

                _cell = self.__make_cell('text', False, 1, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=1)
                _column.set_visible(True)
            elif i == 1:
                _cell = self.__make_cell('text', True, 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

                _cell = self.__make_cell('text', True, 3, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, visible=10)
                _column.set_visible(True)
            elif i in [2, 3, 4]:
                _cell = self.__make_cell('text', True, i + 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2)
                _column.set_visible(True)
            elif i in [5, 6]:
                _cell = self.__make_cell('text', True, i + 2, _model)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2, visible=10)
                _column.set_visible(True)
            else:
                _cell = self.__make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)
                _cell = self.__make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)
                _cell = self.__make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)
                _cell = self.__make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)
                _cell = self.__make_cell('text', False, i + 2, _model)
                _column.pack_start(_cell, True)

                _column.set_visible(False)

            _column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
            self.treeview.append_column(_column)

    def __make_ui(self):
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.tab_label.set_markup(
            "<span weight='bold'>" +
            _("Usage\nProfiles") + "</span>",
        )
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays usage profiles for the selected revision."),
        )

        self.pack_start(self.__make_buttonbox(), False, False, 0)
        RAMSTKListView._make_ui(self)

    def __set_properties(self):
        """
        Set properties of the Failure Definition ListView and widgets.

        :return: None
        :rtype: None
        """
        RAMSTKListView._set_properties(self)
        self.treeview.set_tooltip_text(
            _(
                "Displays the list of usage profiles for the selected "
                "revision.",
            ),
        )

    def _do_load_environment(self, entity, identifier, row):
        """
        Load an environmental condition into the RAMSTK TreeView.

        :param entity: the record from the RAMSTKEnvironment table to load.
        :type entity: :class:`ramstk.dao.programdb.RAMSTKEnvironment`
        :param int identifier: the ID of the Usage Profile being loaded.
        :param row: the Gtk.Iter() to load the entity data into.
        :return: _new_row; the Gtk.Iter() pointing to the next row to load.
        :rtype: :class:`Gtk.Iter`
        """
        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['environment'], 22, 22,
        )
        _attributes = [
            _icon, entity.environment_id, entity.name, '', entity.units,
            entity.minimum, entity.maximum, entity.mean, entity.variance,
            identifier, 1, 'environment',
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _(
                "One or more Environments had the wrong data type "
                "in it's data package and is not displayed in the "
                "Usage Profile.",
            )
            _debug_msg = (
                "RAMSTK ERROR: Data for Environment ID {0:s} for Revision ID "
                "{1:s} is the wrong type for one or more columns.".format(
                    str(entity.environment_id), str(self._revision_id),
                )
            )
            _new_row = None
        except ValueError:
            _user_msg = _(
                "One or more Missions was missing some of it's data "
                "and is not displayed in the Usage Profile.",
            )
            _debug_msg = (
                "RAMSTK ERROR: Too few fields for Environment ID {0:s} for "
                "Revision ID {1:s}.".format(
                    str(entity.environment_id), str(self._revision_id),
                )
            )
            _new_row = None

        return _new_row

    def _do_load_mission(self, entity, identifier, row):
        """
        Load a mission into the RAMSTK TreeView.

        :param entity: the record from the RAMSTKMission table to load.
        :type entity: :class:`ramstk.dao.programdb.RAMSTKMission`
        :param int identifier: the ID of the Usage Profile being loaded.
        :return: _new_row; the Gtk.Iter() pointing to the next row to load.
        :rtype: :class:`Gtk.Iter`
        """
        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['mission'], 22, 22,
        )
        _attributes = [
            _icon, entity.mission_id, entity.description, '',
            entity.time_units, 0.0, entity.mission_time, 0.0, 0.0, identifier,
            0, 'mission',
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _(
                "One or more Missions had the wrong data type in "
                "it's data package and is not displayed in the "
                "Usage Profile.",
            )
            _debug_msg = (
                "RAMSTK ERROR: Data for Mission ID {0:s} for Revision ID "
                "{1:s} is the wrong type for one or more columns.".format(
                    str(entity.mission_id), str(self._revision_id),
                )
            )
            _new_row = None
        except ValueError:
            _user_msg = _(
                "One or more Missions was missing some of it's data "
                "and is not displayed in the Usage Profile.",
            )
            _debug_msg = (
                "RAMSTK ERROR: Too few fields for Mission ID {0:s} for "
                "Revision ID {1:s}.".format(
                    str(entity.mission_id), str(self._revision_id),
                )
            )
            _new_row = None

        return _new_row

    def _do_load_phase(self, entity, identifier, row):
        """
        Load a mission phase into the RAMSTK TreeView.

        :param entity: the record from the RAMSTKMissionPhase table to load.
        :type entity: :class:`ramstk.dao.programdb.RAMSTKMissionPhase`
        :param int identifier: the ID of the Usage Profile being loaded.
        :param row: the Gtk.Iter() to load the entity data into.
        :return: _new_row; the Gtk.Iter() pointing to the next row to load.
        :rtype: :class:`Gtk.Iter`
        """
        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['phase'], 22, 22,
        )
        _attributes = [
            _icon, entity.phase_id, entity.name, entity.description, '',
            entity.phase_start, entity.phase_end, 0.0, 0.0, identifier, 0,
            'phase',
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _(
                "One or more Mission Phases had the wrong data type "
                "in it's data package and is not displayed in the "
                "Usage Profile.",
            )
            _debug_msg = (
                "RAMSTK ERROR: Data for Mission Phase ID {0:s} for Revision "
                "ID {1:s} is the wrong type for one or more columns.".format(
                    str(entity.phase_id), str(self._revision_id),
                )
            )
            _new_row = None
        except ValueError:
            _user_msg = _(
                "One or more Mission Phases was missing some of "
                "it's data and is not displayed in the Usage "
                "Profile.",
            )
            _debug_msg = (
                "RAMSTK ERROR: Too few fields for Mission Phase ID {0:s} for "
                "Revision ID {1:s}.".format(
                    str(entity.phase_id), str(self._revision_id),
                )
            )
            _new_row = None

        return _new_row

    def _do_load_tree(self, tree, row=None):
        """
        Recursively load the Usage Profile List View's Gtk.TreeModel.

        :param tree: the Usage Profile treelib Tree().
        :type tree: :class:`treelib.Tree`
        :param row: the parent row in the Usage Profile Gtk.TreeView() to
                    add the new item.
        :type row: :class:`Gtk.TreeIter`

        :return: None
        :rtype: None
        """
        _row = None
        _model = self.treeview.get_model()

        _node = tree.nodes[list(SortedDict(tree.nodes).keys())[0]]
        _entity = _node.data
        if _entity is None:
            _model.clear()

        try:
            if _entity.is_mission:
                _new_row = self._do_load_mission(
                    _entity, _node.identifier,
                    row,
                )

            elif _entity.is_phase:
                _new_row = self._do_load_phase(_entity, _node.identifier, row)

            elif _entity.is_env:
                _new_row = self._do_load_environment(
                    _entity, _node.identifier,
                    row,
                )
        except AttributeError:
            if _node.identifier != 0:
                _user_msg = _(
                    "One or more Usage Profile line items was "
                    "missing it's data package and is not "
                    "displayed in the Usage Profile.",
                )
                _debug_msg = (
                    "RAMSTK ERROR: There is no data package for Usage "
                    "Profile ID {0:s} for Revision ID {1:s}.".format(
                        str(_node.identifier), str(self._revision_id),
                    )
                )
            _new_row = None

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(tree=_child_tree, row=_new_row)

        _row = _model.get_iter_first()
        self.treeview.expand_all()
        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

    def _do_request_delete(self, __button):
        """
        Request to delete the selected Usage Profile record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 9)

        _prompt = _(
            "You are about to delete Mission, Mission Phase, or "
            "Environment {0:d} and all data associated with it.  Is "
            "this really what you want to do?",
        ).format(_node_id)
        _dialog = ramstk.RAMSTKMessageDialog(
            _prompt, self._dic_icons['question'], 'question',
        )
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage('request_delete_profile', node_id=_node_id)

        _dialog.do_destroy()

    def _do_request_insert(self, **kwargs):
        """
        Request to add an entity to the Usage Profile.

        :return: None
        :rtype: None
        """
        _sibling = kwargs['sibling']

        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _level = _model.get_value(_row, 11)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _level = ''
            _prow = None

        if _sibling and _level == 'mission':
            _entity_id = self._revision_id
            _parent_id = 0
        else:
            _entity_id = _model.get_value(_prow, 1)
            _parent_id = _model.get_value(_prow, 9)

        _dic_level = {'mission': 'phase', 'phase': 'environment'}
        if not _sibling:
            try:
                _level = _dic_level[_level]
            except KeyError:
                _prompt = _("An environmental condition cannot have a child.")
                _dialog = ramstk.RAMSTKMessageDialog(
                    _prompt, self._dic_icons['error'], 'error',
                )
                _dialog.do_destroy()

        pub.sendMessage(
            'request_insert_profile',
            entity_id=_entity_id,
            parent_id=_parent_id,
            level=_level,
        )

    def _do_request_update(self, __button):
        """
        Request to update the currently selected Usage Profile record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 9)

        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_profile', node_id=_node_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Request to update all the Usage Profile records.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_profiles')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview, event):
        """
        Handle mouse clicks on the Usage Profile List View RAMSTKTreeView().

        :param treeview: the Usage Profile ListView Gtk.TreeView().
        :type treeview: :class:`Gtk.TreeView`.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backward
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            _icons = ['insert_sibling', 'insert_child', 'remove', 'save-all']
            _labels = [
                _("Add Sibling Entity"),
                _("Add Child Entity"),
                _("Remove Selected Entity"),
                _("Save Usage Profile"),
            ]
            _callbacks = [
                self.do_request_insert_sibling, self.do_request_insert_child,
                self._do_request_delete, self._do_request_update_all,
            ]

            self.on_button_press(
                event, icons=_icons, labels=_labels, callbacks=_callbacks,
            )

        treeview.handler_unblock(self._lst_handler_id[1])

    @staticmethod
    def _on_cell_edit(__cell, path, new_text, position, model):
        """
        Handle edits of the Usage Profile List View RAMSTKTreeView().

        :param Gtk.CellRenderer __cell: the Gtk.CellRenderer() that was edited.
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param model: the Gtk.TreeModel() the Gtk.CellRenderer() belongs to.
        :type model: :class:`Gtk.TreeModel`
        :return: None
        :rtype: None
        """
        _dic_keys = {
            'mission': {
                2: 'description',
                4: 'time_units',
                6: 'mission_time',
            },
            'phase': {
                2: 'name',
                3: 'descriptino',
                5: 'phase_start',
                6: 'phase_end',
            },
            'environment': {
                2: 'name',
                4: 'units',
                5: 'minimum',
                6: 'maximum',
                7: 'mean',
                8: 'variance',
            },
        }

        if not RAMSTKListView._do_edit_cell(
                __cell, path, new_text, position, model,
        ):

            # Retrieve the Usage Profile data package.
            _node_id = model[path][9]
            _level = model[path][11]

            _key = _dic_keys[_level][position]

            pub.sendMessage(
                'lvw_editing_profile',
                module_id=_node_id,
                key=_key,
                value=new_text,
            )

    def _on_row_change(self, treeview):
        """
        Handle row changes for the Usage Profile package List View.

        This method is called whenever a Usage Profile List View
        RAMSTKTreeView() row is activated or changed.

        :param treeview: the Usage Profile List View class RAMSTK.TreeView().
        :type treeview: :class:`ramstk.gui.gtk.TreeView.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        _attributes = {}

        treeview.handler_block(self._lst_handler_id[0])

        (_model, _row) = treeview.get_selection().get_selected()

        if _row is not None:
            try:
                _level = _model.get_value(_row, 11)
            except TypeError:
                _level = None

            # Change the column headings depending on what is being selected.
            if _level == 'mission':
                _headings = [
                    _("Mission ID"),
                    _("Description"),
                    _("Units"),
                    _("Start Time"),
                    _("End Time"),
                    _(""),
                    _(""),
                    _(""),
                ]
                _attributes['mission_id'] = _model.get_value(_row, 0)
                _attributes['description'] = _model.get_value(_row, 2)
                _attributes['time_units'] = _model.get_value(_row, 4)
                _attributes['mission_time'] = _model.get_value(_row, 6)

            elif _level == 'phase':
                _headings = [
                    _("Phase ID"),
                    _("  Code\t\tDescription"),
                    _("Units"),
                    _("Start Time"),
                    _("End Time"),
                    _(""),
                    _(""),
                    _(""),
                ]
                _attributes['phase_id'] = _model.get_value(_row, 0)
                _attributes['name'] = _model.get_value(_row, 2)
                _attributes['description'] = _model.get_value(_row, 3)
                _attributes['phase_start'] = _model.get_value(_row, 5)
                _attributes['phase_end'] = _model.get_value(_row, 6)

            elif _level == 'environment':
                _headings = [
                    _("Environment ID"),
                    _("Condition"),
                    _("Units"),
                    _("Minimum Value"),
                    _("Maximum Value"),
                    _("Mean Value"),
                    _("Variance"),
                    _(""),
                ]
                _attributes['environment_id'] = _model.get_value(_row, 0)
                _attributes['name'] = _model.get_value(_row, 2)
                _attributes['units'] = _model.get_value(_row, 4)
                _attributes['minimum'] = _model.get_value(_row, 5)
                _attributes['maximum'] = _model.get_value(_row, 6)
                _attributes['mean'] = _model.get_value(_row, 7)
                _attributes['variance'] = _model.get_value(_row, 8)

            else:
                _headings = []

            i = 0
            _columns = treeview.get_columns()
            for _heading in _headings:
                _label = Gtk.Label()
                _label.set_line_wrap(True)
                _label.set_alignment(xalign=0.5, yalign=0.5)
                _label.set_justify(Gtk.Justification.CENTER)
                _label.set_markup(
                    "<span weight='bold'>" + _heading +
                    "</span>",
                )
                _label.set_use_markup(True)
                _label.show_all()
                _columns[i].set_widget(_label)

                i += 1

        treeview.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_usage_profile', attributes=_attributes)
