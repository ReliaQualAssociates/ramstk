# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.revision.listview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Failure Definition List View Module."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.models.programdb import (
    RAMSTKEnvironment, RAMSTKFailureDefinition,
    RAMSTKMission, RAMSTKMissionPhase
)
from ramstk.views.gtk3 import Gdk, GdkPixbuf, GObject, Gtk, Pango, _
from ramstk.views.gtk3.widgets import (
    RAMSTKListView, RAMSTKMessageDialog, RAMSTKTreeView, do_make_buttonbox
)


def _do_make_column(header: str, index: int,
                    visible: int) -> Gtk.TreeViewColumn:
    """
    Make a column with a CellRendererText() and the passed header text.

    :param str header: the text to display in the header of the column.
    :param int index: the index number in the Gtk.TreeModel() to display in
        this column.
    :param int visible: indicates whether or not the column will be visible.
    :return: _column
    :rtype: :class:`Gtk.TreeViewColumn`
    """
    _cell = Gtk.CellRendererText()
    _cell.set_property('wrap-width', 250)
    _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
    _cell.set_property('yalign', 0.1)
    _label = Gtk.Label()
    _label.set_line_wrap(True)
    _label.set_alignment(xalign=0.5, yalign=0.5)
    _label.set_justify(Gtk.Justification.CENTER)
    _label.set_markup("<span weight='bold'>" + header + "</span>")
    _label.set_use_markup(True)
    _label.show_all()
    _column = Gtk.TreeViewColumn()
    _column.set_widget(_label)
    _column.set_visible(visible)
    _column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
    _column.pack_start(_cell, True)
    _column.set_attributes(_cell, text=index)

    return _column


class FailureDefinition(RAMSTKListView):
    """
    Display all the Failure Definitions associated with the selected Revision.

    The attributes of the Failure Definition List View are:

    :ivar int _definition_id: the Failure Definition ID of the definition
        selected in the List View.
    """
    def __init__(self, configuration, logger, module='failure_definition') -> None:
        """
        Initialize the List View for the Failure Definition package.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the module.
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._definition_id = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_treeview()
        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_tree, 'succeed_delete_failure_definition')
        pub.subscribe(self._do_load_tree, 'succeed_insert_failure_definition')
        pub.subscribe(self.__do_load_tree,
                      'succeed_get_failure_definitions_attributes')

    def __do_load_tree(self, attributes: Dict[int, Any]) -> None:
        """
        Wrapper method for _do_load_tree().

        The pubsub message the ListView listens for sends a data package named
        attributes.  _do_load_tree() needs a data package named tree.  This
        method simply makes that conversion happen.

        :param dict attributes: the failure definition dict for the selected
            revision ID.
        :return: None
        :rtype: None
        """
        if attributes is not None:
            self._do_load_tree(tree=attributes)

    def __make_buttonbox(self) -> Gtk.ButtonBox:
        """
        Make the buttonbox for the Failure Definition List View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Failure Definition
            List View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _("Add a new Failure Definition."),
            _("Remove the currently selected Failure Definition.")
        ]
        _callbacks = [self._do_request_insert, self._do_request_delete]
        _icons = ['add', 'remove']

        _buttonbox = do_make_buttonbox(self,
                                       icons=_icons,
                                       tooltips=_tooltips,
                                       callbacks=_callbacks,
                                       orientation='vertical',
                                       height=-1,
                                       width=-1)

        return _buttonbox

    def __make_treeview(self) -> None:
        """
        Set up the RAMSTKTreeView() for Failure Definitions.

        :return: None
        :rtype: None
        """
        _model = Gtk.ListStore(GObject.TYPE_INT, GObject.TYPE_INT,
                               GObject.TYPE_STRING)
        self.treeview.set_model(_model)

        for _header in enumerate(
                ["Revision ID", "Definition\nNumber", "Failure Definition"]):
            _column = _do_make_column(_header[1], _header[0], _header[0])
            self.treeview.append_column(_column)

        _cell = self.treeview.get_columns()[2].get_cells()[0]
        _cell.set_property('editable', True)
        self._lst_handler_id.append(
            _cell.connect('edited', self._on_cell_edit, 2))

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.tab_label.set_markup("<span weight='bold'>"
                                  + _("Failure\nDefinitions") + "</span>")
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays failure definitions for the "
              "selected revision."))

        self.pack_start(self.__make_buttonbox(), False, False, 0)

        super().make_ui()

    def __set_properties(self) -> None:
        """
        Set properties of the Failure Definition ListView and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_tooltip_text(
            _("Displays the list of failure definitions for the selected "
              "revision."))

    def _do_load_tree(self, tree: Dict[int, RAMSTKFailureDefinition]) -> None:
        """
        Load the Failure Definition List View's Gtk.TreeModel.

        :param tree: the Failure Definition attributes dict.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

        for _key in tree:
            _entity = tree[_key]

            _attributes: Tuple[int, int, str] = (0, 0, '')
            if _entity is not None:
                _attributes = (_entity.revision_id, _entity.definition_id,
                               _entity.definition)
            try:
                _row = _model.append(_attributes)
            except ValueError:
                _row = None

        self.do_expand_tree()

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected Failure Definition record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prompt = _("You are about to delete Failure Definition {0:d} and "
                    "all data associated with it.  Is this really what you "
                    "want to do?").format(self._definition_id)
        _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons['question'],
                                      'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            pub.sendMessage('request_delete_failure_definition',
                            revision_id=self._revision_id,
                            node_id=self._definition_id)

        _dialog.do_destroy()

    def _do_request_insert(self, __button: Gtk.ToolButton) -> None:  # pylint: disable=unused-argument
        """
        Request to add a Failure Definition record.

        :param __button: the gtk.ToolButton() that called this method.
        :type __button: :class:`gtk.ToolButton`
        :return: None
        :rtype: None
        """
        pub.sendMessage('request_insert_failure_definition',
                        revision_id=self._revision_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to update the currently selected Failure Definition record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_failure_definition',
                        revision_id=self._revision_id,
                        node_id=self._definition_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to update all Failure Definitions records.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_failure_definitions',
                        revision_id=self._revision_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on Failure Definition List View RAMSTKTreeView().

        :param treeview: the Failure Definition ListView Gtk.TreeView().
        :type treeview: :class:`ramstk.gui.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backward
                      * 8 =
                      * 9 =
        :type event: :py:class:`Gdk.Event`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.
        if event.button == 3:
            self.on_button_press(event,
                                 icons=['add', 'remove', 'save', 'save-all'],
                                 labels=[
                                     _("Add New Definition"),
                                     _("Remove Selected Definition"),
                                     _("Save Selected Definition"),
                                     _("Save All Definitions")
                                 ],
                                 callbacks=[
                                     self._do_request_insert,
                                     self._do_request_delete,
                                     self._do_request_update,
                                     self._do_request_update_all
                                 ])

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of the Failure Definition List View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        super().on_cell_edit(__cell, path, new_text, position)

        pub.sendMessage('lvw_editing_failure_definition',
                        node_id=[self._revision_id, self._definition_id, ''],
                        package={'definition': new_text})

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle row changes for the Failure Definition package List View.

        This method is called whenever a Failure Definition List View
        RAMSTKTreeView() row is activated or changed.

        :param selection: the Failure Definition class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        _attributes = {}

        selection.handler_block(self._lst_handler_id[0])

        _model, _row = selection.get_selected()

        if _row is not None:
            _attributes['revision_id'] = _model.get_value(_row, 0)
            _attributes['definition_id'] = _model.get_value(_row, 1)
            _attributes['definition'] = _model.get_value(_row, 2)

            self._definition_id = _attributes['definition_id']

            pub.sendMessage('selected_failure_definition',
                            attributes=_attributes)

        selection.handler_unblock(self._lst_handler_id[0])


class UsageProfile(RAMSTKListView):
    """
    Display all the Usage Profiles associated with the selected Revision.

    All attributes of a Usage Profile List View are inherited.
    """
    def __init__(self, configuration, logger, module='usage_profile') -> None:
        """
        Initialize the List View for the Usage Profile.

        :param configuration: the RAMSTK Configuration class instance.
        :type configuration: :class:`ramstk.Configuration.Configuration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        :param str module: the name of the module.
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_icons['mission'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/mission.png')
        self._dic_icons['phase'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/phase.png')
        self._dic_icons['environment'] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR
            + '/32x32/environment.png')

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_treeview()
        self.__set_properties()
        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_tree, 'succeed_delete_environment')
        pub.subscribe(self._do_load_tree, 'succeed_delete_mission')
        pub.subscribe(self._do_load_tree, 'succeed_delete_mission_phase')
        pub.subscribe(self._do_load_tree, 'succeed_insert_environment')
        pub.subscribe(self._do_load_tree, 'succeed_insert_mission')
        pub.subscribe(self._do_load_tree, 'succeed_insert_mission_phase')
        pub.subscribe(self.__do_load_tree,
                      'succeed_get_usage_profile_attributes')

    def __do_load_tree(self, attributes: Tree) -> None:
        """
        Wrapper method for _do_load_tree().

        The pubsub message the ListView listens for sends a data package named
        attributes.  _do_load_tree() needs a data package named tree.  This
        method simply makes that conversion happen.

        :param attributes: the usage profile Tree() for the selected revision
            ID.
        :type attributes: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

        if attributes is not None:
            for _n in attributes.children(self._revision_id):
                _mission: Tree = attributes.subtree(_n.identifier)
                self._do_load_tree(_mission, row=None)

    @staticmethod
    def __get_attributes(selection: Gtk.TreeSelection, level: str) -> Dict:
        """
        Retrieve the attributes for the line being edited.

        :param selection: the Gtk.TreeSelection that is currently selected.
        :type selection: :class:`Gtk.TreeSelection`
        :param str level: the indenture level in the Usage Profile that is
            selected.
        :return: a dict of attributes and values.
        :rtype: dict
        """
        _attributes = {}

        _model, _row = selection.get_selected()

        if level == 'mission':
            _attributes['mission_id'] = _model.get_value(_row, 0)
            _attributes['description'] = _model.get_value(_row, 2)
            _attributes['time_units'] = _model.get_value(_row, 4)
            _attributes['mission_time'] = _model.get_value(_row, 6)
        elif level == 'phase':
            _attributes['phase_id'] = _model.get_value(_row, 0)
            _attributes['name'] = _model.get_value(_row, 2)
            _attributes['description'] = _model.get_value(_row, 3)
            _attributes['phase_start'] = _model.get_value(_row, 5)
            _attributes['phase_end'] = _model.get_value(_row, 6)
        elif level == 'environment':
            _attributes['environment_id'] = _model.get_value(_row, 0)
            _attributes['name'] = _model.get_value(_row, 2)
            _attributes['units'] = _model.get_value(_row, 4)
            _attributes['minimum'] = _model.get_value(_row, 5)
            _attributes['maximum'] = _model.get_value(_row, 6)
            _attributes['mean'] = _model.get_value(_row, 7)
            _attributes['variance'] = _model.get_value(_row, 8)

        return _attributes

    @staticmethod
    def __get_headings(level):
        """
        Get the list of headings for the Usage Profile treeview.

        :param level: the level (mission, phase, environment) to retrieve
            headers for.
        :return: list of headings
        :rtype: list
        """
        return {
            'mission': [
                _("Mission ID"),
                _("Description"),
                _("Units"),
                _("Start Time"),
                _("End Time"),
                _(""),
                _(""),
                _("")
            ],
            'phase': [
                _("Phase ID"),
                _("  Code\t\tDescription"),
                _("Units"),
                _("Start Time"),
                _("End Time"),
                _(""),
                _(""),
                _("")
            ],
            'environment': [
                _("Environment ID"),
                _("Condition"),
                _("Units"),
                _("Minimum Value"),
                _("Maximum Value"),
                _("Mean Value"),
                _("Variance"),
                _("")
            ]
        }[level]

    def __make_buttonbox(self) -> Gtk.ButtonBox:
        """
        Make the buttonbox for the Usage Profile List View.

        :return: _buttonbox; the Gtk.ButtonBox() for the Usage Profile List
            View.
        :rtype: :class:`Gtk.ButtonBox`
        """
        _tooltips = [
            _("Add a new Usage Profile entity at the same level "
              "as the currently selected entity."),
            _("Add a new Usage Profile entity one level below the "
              "currently selected entity."),
            _("Remove the curently selected entity from the Usage "
              "Profile.")
        ]
        _callbacks = [
            self._do_request_insert_sibling, self._do_request_insert_child,
            self._do_request_delete
        ]
        _icons = ['insert_sibling', 'insert_child', 'remove']

        _buttonbox = do_make_buttonbox(self,
                                       icons=_icons,
                                       tooltips=_tooltips,
                                       callbacks=_callbacks,
                                       orientation='vertical',
                                       height=-1,
                                       width=-1)

        return _buttonbox

    def __make_cell(self, cell: str, editable: bool,
                    position: int) -> Gtk.CellRenderer:
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
            'text': Gtk.CellRendererText()
        }

        _cell = _cellrenderers[cell]

        if not editable:
            _cell.set_property('cell-background', 'light gray')
        else:
            _cell.connect('edited', self._on_cell_edit, position)

        if cell == 'text':
            _cell.set_property('editable', editable)
            _cell.set_property('wrap-width', 250)
            _cell.set_property('wrap-mode', Pango.WrapMode.WORD_CHAR)
            _cell.set_property('yalign', 0.1)

        return _cell

    def __make_treeview(self) -> None:
        """
        Set up the RAMSTKTreeView() for the Usage Profile.

        :return: None
        :rtype: None
        """
        _model = Gtk.TreeStore(GdkPixbuf.Pixbuf, GObject.TYPE_INT,
                               GObject.TYPE_STRING, GObject.TYPE_STRING,
                               GObject.TYPE_STRING, GObject.TYPE_FLOAT,
                               GObject.TYPE_FLOAT, GObject.TYPE_FLOAT,
                               GObject.TYPE_FLOAT, GObject.TYPE_STRING,
                               GObject.TYPE_INT, GObject.TYPE_STRING)
        self.treeview.set_model(_model)

        for i in range(10):
            _column = Gtk.TreeViewColumn()
            if i == 0:
                _cell = self.__make_cell('pixbuf', False, 0)
                _cell.set_property('xalign', 0.5)
                _column.pack_start(_cell, False)
                _column.set_attributes(_cell, pixbuf=0)

                _cell = self.__make_cell('text', False, 1)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=1)
                _column.set_visible(True)
            elif i == 1:
                _cell = self.__make_cell('text', True, 2)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=2)

                _cell = self.__make_cell('text', True, 3)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=3, visible=10)
                _column.set_visible(True)
            elif i in [2, 3, 4]:
                _cell = self.__make_cell('text', True, i + 2)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2)
                _column.set_visible(True)
            elif i in [5, 6]:
                _cell = self.__make_cell('text', True, i + 2)
                _column.pack_start(_cell, True)
                _column.set_attributes(_cell, text=i + 2, visible=10)
                _column.set_visible(True)
            else:
                _cell = self.__make_cell('text', False, i + 2)
                _column.pack_start(_cell, True)
                _cell = self.__make_cell('text', False, i + 2)
                _column.pack_start(_cell, True)
                _cell = self.__make_cell('text', False, i + 2)
                _column.pack_start(_cell, True)
                _cell = self.__make_cell('text', False, i + 2)
                _column.pack_start(_cell, True)
                _cell = self.__make_cell('text', False, i + 2)
                _column.pack_start(_cell, True)

                _column.set_visible(False)

            _column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
            self.treeview.append_column(_column)

    def __make_ui(self) -> None:
        """
        Build the user interface.

        :return: None
        :rtype: None
        """
        self.tab_label.set_markup("<span weight='bold'>" + _("Usage\nProfiles")
                                  + "</span>")
        self.tab_label.set_alignment(xalign=0.5, yalign=0.5)
        self.tab_label.set_justify(Gtk.Justification.CENTER)
        self.tab_label.show_all()
        self.tab_label.set_tooltip_text(
            _("Displays usage profiles for the selected revision."))

        self.pack_start(self.__make_buttonbox(), False, False, 0)

        super().make_ui()

    def __set_properties(self) -> None:
        """
        Set properties of the Failure Definition ListView and widgets.

        :return: None
        :rtype: None
        """
        self.treeview.set_tooltip_text(
            _("Displays the list of usage profiles for the selected "
              "revision."))

    def _do_load_environment(self, entity: RAMSTKEnvironment, identifier: int,
                             row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load an environmental condition into the RAMSTK TreeView.

        :param entity: the record from the RAMSTKEnvironment table to load.
        :type entity: :class:`ramstk.db.programdb.RAMSTKEnvironment`
        :param int identifier: the ID of the Usage Profile being loaded.
        :param row: the Gtk.Iter() to load the entity data into.
        :return: _new_row; the Gtk.Iter() pointing to the next row to load.
        :rtype: :class:`Gtk.TreeIter`
        """
        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['environment'], 22, 22)
        _attributes = [
            _icon, entity.environment_id, entity.name, '', entity.units,
            entity.minimum, entity.maximum, entity.mean, entity.variance,
            identifier, 1, 'environment'
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _("One or more Environments for revision ID {0:d} had "
                          "the wrong data type in it's data package and was "
                          "not displayed in the Usage "
                          "Profile.".format(self._revision_id))
            _debug_msg = (
                "RAMSTK ERROR: Data for Environment ID {0:s} for Revision ID "
                "{1:s} is the wrong type for one or more columns.".format(
                    str(entity.environment_id), str(self._revision_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Environments for revision ID {0:d} was "
                          "missing some of it's data and was not displayed in "
                          "the Usage Profile.".format(self._revision_id))
            _debug_msg = (
                "RAMSTK ERROR: Too few fields for Environment ID {0:s} for "
                "Revision ID {1:s}.".format(str(entity.environment_id),
                                            str(self._revision_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_mission(self, entity: RAMSTKMission, identifier: int,
                         row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a mission into the RAMSTK TreeView.

        :param entity: the record from the RAMSTKMission table to load.
        :type entity: :class:`ramstk.db.programdb.RAMSTKMission`
        :param int identifier: the ID of the Usage Profile being loaded.
        :return: _new_row; the Gtk.Iter() pointing to the next row to load.
        :rtype: :class:`Gtk.Iter`
        """
        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons['mission'], 22, 22)
        _attributes = [
            _icon, entity.mission_id, entity.description, '',
            entity.time_units, 0.0, entity.mission_time, 0.0, 0.0, identifier,
            0, 'mission'
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _("One or more Missions had the wrong data type in "
                          "it's data package and is not displayed in the "
                          "Usage Profile.")
            _debug_msg = (
                "Data for Mission ID {0:s} for Revision ID {1:s} is the wrong "
                "type for one or more columns.".format(str(entity.mission_id),
                                                       str(self._revision_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Missions was missing some of it's data "
                          "and is not displayed in the Usage Profile.")
            _debug_msg = (
                "Too few fields for Mission ID {0:s} for Revision ID "
                "{1:s}.".format(str(entity.mission_id),
                                str(self._revision_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_phase(self, entity: RAMSTKMissionPhase, identifier: int,
                       row: Gtk.TreeIter) -> Gtk.TreeIter:
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
            self._dic_icons['phase'], 22, 22)
        _attributes = [
            _icon, entity.phase_id, entity.name, entity.description, '',
            entity.phase_start, entity.phase_end, 0.0, 0.0, identifier, 0,
            'phase'
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except TypeError:
            _user_msg = _("One or more Mission Phases had the wrong data type "
                          "in it's data package and is not displayed in the "
                          "Usage Profile.")
            _debug_msg = (
                "RAMSTK ERROR: Data for Mission Phase ID {0:s} for Revision "
                "ID {1:s} is the wrong type for one or more columns.".format(
                    str(entity.phase_id), str(self._revision_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Mission Phases was missing some of "
                          "it's data and is not displayed in the Usage "
                          "Profile.")
            _debug_msg = (
                "RAMSTK ERROR: Too few fields for Mission Phase ID {0:s} for "
                "Revision ID {1:s}.".format(str(entity.phase_id),
                                            str(self._revision_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_tree(self, tree: Tree, row: Gtk.TreeIter = None) -> None:
        """
        Recursively load the Usage Profile List View's Gtk.TreeModel.

        :param tree: the Usage Profile treelib Tree().
        :type tree: :class:`treelib.Tree`
        :param row: the parent row in the Usage Profile Gtk.TreeView() to add
            the new item.
        :type row: :class:`Gtk.TreeIter`
        :return: None
        :rtype: None
        """
        _new_row: Gtk.TreeIter = None
        _model = self.treeview.get_model()

        _node = tree.nodes[list(tree.nodes.keys())[0]]
        _entity = _node.data
        # The root node will have no data package, so this indicates the need to
        # clear the tree in preparation for the load.
        if _entity is None:
            _model.clear()

        try:
            if _entity.is_mission:
                _new_row = self._do_load_mission(_entity, _node.identifier,
                                                 row)
            elif _entity.is_phase:
                _new_row = self._do_load_phase(_entity, _node.identifier, row)
            elif _entity.is_env:
                _new_row = self._do_load_environment(_entity, _node.identifier,
                                                     row)
        except AttributeError:
            _user_msg = _("One or more Usage Profile line items was "
                          "missing it's data package and is not "
                          "displayed in the Usage Profile.")
            _debug_msg = (
                "There is no data package for Usage Profile ID {0:s} for "
                "Revision ID {1:s}.".format(str(_node.identifier),
                                            str(self._revision_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, row=_new_row)

        self.do_expand_tree()

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected Usage Profile record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.selection.get_selected()
        _node_id = _model.get_value(_row, 9)
        _level = _model.get_value(_row, 11)

        _prow = _model.iter_parent(_row)
        try:
            _parent_id = _model.get_value(_prow, 9)
        except TypeError:
            _parent_id = -1

        _prompt = _("You are about to delete {1:s} {0:s} and all data "
                    "associated with it.  Is this really what you want to "
                    "do?").format(_node_id, _level)
        _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons['question'],
                                      'question')
        _response = _dialog.do_run()

        if _response == Gtk.ResponseType.YES:
            if _level == 'mission':
                pub.sendMessage('request_delete_mission',
                                revision_id=self._revision_id,
                                node_id=_node_id)
            elif _level == 'phase':
                pub.sendMessage('request_delete_mission_phase',
                                revision_id=self._revision_id,
                                mission_id=_parent_id,
                                node_id=_node_id)
            elif _level == 'environment':
                pub.sendMessage('request_delete_environment',
                                revision_id=self._revision_id,
                                phase_id=_parent_id,
                                node_id=_node_id)

        _dialog.do_destroy()

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """
        Request to add an entity to the Usage Profile.

        :return: None
        :rtype: None
        """
        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self.treeview.selection.get_selected()
        _level = _model.get_value(_row, 11)
        _prow = _model.iter_parent(_row)

        if _level == 'mission':
            _mission_id = _model.get_value(_row, 9)
            pub.sendMessage('request_insert_mission_phase',
                            revision_id=self._revision_id,
                            mission_id=_mission_id)
        elif _level == 'phase':
            _phase_id = _model.get_value(_row, 1)
            _mission_id = _model.get_value(_prow, 9)
            pub.sendMessage('request_insert_environment',
                            revision_id=self._revision_id,
                            mission_id=_mission_id,
                            phase_id=_phase_id)
        elif _level == 'environment':
            _prompt = _("An environmental condition cannot have a child.")
            _dialog = RAMSTKMessageDialog(_prompt, self._dic_icons['error'],
                                          'error')
            _dialog.do_run()
            _dialog.do_destroy()

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """
        Request to add a sibling entity to the Usage Profile.

        :return: None
        :rtype: None
        """
        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self.treeview.selection.get_selected()
        try:
            _level = _model.get_value(_row, 11)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _level = 'mission'
            _prow = None

        if _level == 'mission':
            pub.sendMessage('request_insert_mission',
                            revision_id=self._revision_id)
        elif _level == 'phase':
            _mission_id = _model.get_value(_prow, 9)
            pub.sendMessage('request_insert_mission_phase',
                            revision_id=self._revision_id,
                            mission_id=_mission_id)
        elif _level == 'environment':
            _gprow = _model.iter_parent(_prow)
            _mission_id = _model.get_value(_gprow, 9)
            _phase_id = _model.get_value(_prow, 9).split('.')[1]
            pub.sendMessage('request_insert_environment',
                            revision_id=self._revision_id,
                            mission_id=_mission_id,
                            phase_id=_phase_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to update the currently selected Usage Profile record.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.selection.get_selected()
        _node_id = _model.get_value(_row, 9)

        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_usage_profile',
                        revision_id=self._revision_id,
                        node_id=_node_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to update all the Usage Profile records.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_usage_profiles',
                        revision_id=self._revision_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
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
            self.on_button_press(
                event,
                icons=['insert_sibling', 'insert_child', 'remove', 'save-all'],
                labels=[
                    _("Add Sibling Entity"),
                    _("Add Child Entity"),
                    _("Remove Selected Entity"),
                    _("Save Usage Profile")
                ],
                callbacks=[
                    self.do_request_insert_sibling,
                    self.do_request_insert_child, self._do_request_delete,
                    self._do_request_update_all
                ])

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, __cell: Gtk.CellRenderer, path: str, new_text: Any,
                      position: int) -> None:
        """
        Handle edits of the Usage Profile List View RAMSTKTreeView().

        :param Gtk.CellRenderer __cell: the Gtk.CellRenderer() that was edited.
        :param str path: the Gtk.TreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        _dic_keys = {
            'mission': {
                2: 'description',
                4: 'time_units',
                6: 'mission_time'
            },
            'phase': {
                2: 'name',
                3: 'description',
                5: 'phase_start',
                6: 'phase_end'
            },
            'environment': {
                2: 'name',
                4: 'units',
                5: 'minimum',
                6: 'maximum',
                7: 'mean',
                8: 'variance'
            }
        }

        _model, _row = self.treeview.selection.get_selected()

        _node_id = _model.get_value(_row, 9)
        _level = _model.get_value(_row, 11)

        try:
            _key = _dic_keys[_level][position]
            super().on_cell_edit(__cell, path, new_text, position)
            pub.sendMessage('lvw_editing_usage_profile',
                            node_id=[self._revision_id, -1, _node_id],
                            package={_key: new_text})
        except KeyError:
            _status = _("Mission start time is always set to 0.0.  Your "
                        "edits will not be saved.")
            pub.sendMessage('request_set_status', status=_status)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle row changes for the Usage Profile package List View.

        This method is called whenever a Usage Profile List View
        RAMSTKTreeView() row is activated or changed.

        :param selection: the Usage Profile class Gtk.TreeSelection().
        :type selection: :class:`Gtk.TreeSelection`
        :return: None
        :rtype: None
        """
        _attributes: Dict[str, Any] = {}
        _headings: List[str] = []
        _level: str = ''

        selection.handler_block(self._lst_handler_id[0])

        _model, _row = selection.get_selected()

        if _row is not None:
            try:
                _level = _model.get_value(_row, 11)
            except TypeError:
                _level = ''
            _headings = self.__get_headings(_level)

            # Change the column headings depending on what is being selected.
            i = 0
            _columns = self.treeview.get_columns()
            for _heading in _headings:
                _label = Gtk.Label()
                _label.set_line_wrap(True)
                _label.set_alignment(xalign=0.5, yalign=0.5)
                _label.set_justify(Gtk.Justification.CENTER)
                _label.set_markup("<span weight='bold'>" + _heading
                                  + "</span>")
                _label.set_use_markup(True)
                _label.show_all()
                _columns[i].set_widget(_label)

                i += 1

        selection.handler_unblock(self._lst_handler_id[0])

        pub.sendMessage('selected_usage_profile',
                        attributes=self.__get_attributes(selection, _level))
