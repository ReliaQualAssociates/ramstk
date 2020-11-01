# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.usage_profile.listview.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Usage Profile list view."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub
from treelib import Tree

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.models.programdb import (
    RAMSTKEnvironment, RAMSTKMission, RAMSTKMissionPhase
)
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView, RAMSTKPanel


# noinspection PyUnresolvedReferences
class UsageProfilePanel(RAMSTKPanel):
    """Panel to display hierarchical list of usage profiles."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the usage profile panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attributes: Dict[str, Dict[str, Any]] = {
            'mission': {
                'description': [None, 'edited', 2],
                'time_units': [None, 'edited', 4],
                'mission_time': [None, 'edited', 6],
            },
            'phase': {
                'name': [None, 'edited', 2],
                'description': [None, 'edited', 3],
                'phase_start': [None, 'edited', 5],
                'phase_end': [None, 'edited', 6],
            },
            'environment': {
                'name': [None, 'edited', 2],
                'units': [None, 'edited', 4],
                'minimum': [None, 'edited', 5],
                'maximum': [None, 'edited', 6],
                'mean': [None, 'edited', 7],
                'variance': [None, 'edited', 8],
            }
        }
        self._dic_element_keys = {
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
        self._dic_headings = {
            'mission': [
                _("Mission ID"),
                _("Mission Description"),
                _("Units"),
                _("Start Time"),
                _("End Time"),
                _(""),
                _(""),
                _(""),
            ],
            'phase': [
                _("Phase ID"),
                _("Phase Description"),
                _("Units"),
                _("Start Time"),
                _("End Time"),
                _(""),
                _(""),
                _(""),
            ],
            'environment': [
                _("Environment ID"),
                _("Condition Description"),
                _("Units"),
                _("Minimum Value"),
                _("Maximum Value"),
                _("Mean Value"),
                _("Variance"),
                _(""),
            ],
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Usage Profile")

        # Initialize public dictionary class attributes.
        self.dic_icons = {'mission': None, 'phase': None, 'environment': None}

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_delete, 'succeed_delete_environment')
        pub.subscribe(super().on_delete, 'succeed_delete_mission')
        pub.subscribe(super().on_delete, 'succeed_delete_mission_phase')

        pub.subscribe(self._do_load_tree, 'succeed_retrieve_usage_profile')
        pub.subscribe(self._do_load_tree, 'succeed_insert_environment')
        pub.subscribe(self._do_load_tree, 'succeed_insert_mission')
        pub.subscribe(self._do_load_tree, 'succeed_insert_mission_phase')
        pub.subscribe(self._on_module_switch, 'lvwSwitchedPage')

    def do_set_callbacks(self) -> None:
        """Set callbacks for the stakeholder input list view.

        :return: None
        """
        self.tvwTreeView.dic_handler_id[
            'changed'] = self.tvwTreeView.selection.connect(
                'changed', self._on_row_change)

        _idx = 1
        for _key in [
                'col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8',
                'col9', 'col10'
        ]:
            _cell = self.tvwTreeView.get_column(
                self.tvwTreeView.position[_key]).get_cells()[0]
            _cell.connect('edited',
                          super().on_cell_edit, 'lvw_editing_usage_profile',
                          _idx)
            _idx += 1

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        """Set properties of the RAMSTKPanel() widgets.

        :return: None
        """
        super().do_set_properties(**{
            'bold': True,
            'title': self._title,
        })

        self.tvwTreeView.set_tooltip_text(
            _("Displays the usage profiles for the selected revision."))

    def _do_load_environment(self, **kwargs: Dict[str, Any]) -> Gtk.TreeIter:
        """Load an environmental condition into the RAMSTK TreeView.

        :return: _new_row; the Gtk.Iter() pointing to the next row to load.
        :rtype: :class:`Gtk.TreeIter`
        """
        _entity: RAMSTKEnvironment = kwargs.get('entity', None)
        _identifier: int = kwargs.get('identifier', 0)  # type: ignore
        _row: Gtk.TreeIter = kwargs.get('row', None)

        _model = self.tvwTreeView.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons['environment'], 22, 22)
        _attributes = [
            _entity.environment_id, _entity.name, '', _entity.units,
            _entity.minimum, _entity.maximum, _entity.mean, _entity.variance,
            _identifier, 1, 'environment', _icon
        ]

        try:
            _new_row = _model.append(_row, _attributes)
        except TypeError:
            _debug_msg = (
                "RAMSTK ERROR: Data for Environment ID {0:s} is the wrong "
                "type for one or more columns.".format(
                    str(_entity.environment_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = (
                "RAMSTK ERROR: Too few fields for Environment ID {0:s}.".
                format(str(_entity.environment_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_mission(self, **kwargs: Dict[str, Any]) -> Gtk.TreeIter:
        """Load a mission into the RAMSTK TreeView.

        :return: _new_row; the Gtk.Iter() pointing to the next row to load.
        :rtype: :class:`Gtk.TreeIter`
        """
        _entity: RAMSTKMission = kwargs.get('entity', None)
        _identifier: int = kwargs.get('identifier', 0)  # type: ignore
        _row: Gtk.TreeIter = kwargs.get('row', None)

        _model = self.tvwTreeView.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons['mission'], 22, 22)
        _attributes = [
            _entity.mission_id, _entity.description, '', _entity.time_units,
            0.0, _entity.mission_time, 0.0, 0.0, _identifier, 0, 'mission',
            _icon
        ]

        try:
            _new_row = _model.append(_row, _attributes)
        except TypeError:
            _user_msg = _("One or more Missions had the wrong data type in "
                          "it's data package and is not displayed in the "
                          "Usage Profile.")
            _debug_msg = ("Data for Mission ID {0:s} is the wrong "
                          "type for one or more columns.".format(
                              str(_entity.mission_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Missions was missing some of it's data "
                          "and is not displayed in the Usage Profile.")
            _debug_msg = ("Too few fields for Mission ID {0:s}.".format(
                str(_entity.mission_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_phase(self, **kwargs: Dict[str, Any]) -> Gtk.TreeIter:
        """Load a mission phase into the RAMSTK TreeView.

        :return: _new_row; the Gtk.Iter() pointing to the next row to load.
        :rtype: :class:`Gtk.TreeIter`
        """
        _entity: RAMSTKMissionPhase = kwargs.get('entity', None)
        _identifier: int = kwargs.get('identifier', 0)  # type: ignore
        _row: Gtk.TreeIter = kwargs.get('row', None)

        _model = self.tvwTreeView.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons['phase'],
                                                       22, 22)
        _attributes = [
            _entity.phase_id, _entity.name, _entity.description, '',
            _entity.phase_start, _entity.phase_end, 0.0, 0.0, _identifier, 0,
            'phase', _icon
        ]

        try:
            _new_row = _model.append(_row, _attributes)
        except TypeError:
            _user_msg = _("One or more Mission Phases had the wrong data type "
                          "in it's data package and is not displayed in the "
                          "Usage Profile.")
            _debug_msg = (
                "RAMSTK ERROR: Data for Mission Phase ID {0:s} is the wrong "
                "type for one or more columns.".format(str(_entity.phase_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _user_msg = _("One or more Mission Phases was missing some of "
                          "it's data and is not displayed in the Usage "
                          "Profile.")
            _debug_msg = (
                "RAMSTK ERROR: Too few fields for Mission Phase ID {0:s}.".
                format(str(_entity.phase_id)))
            self.RAMSTK_LOGGER.do_log_info(__name__, _user_msg)
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_tree(self, tree: Tree, row: Gtk.TreeIter = None) -> None:
        """Recursively load the Usage Profile List View's Gtk.TreeModel.

        :param tree: the Usage Profile treelib Tree().
        :param row: the parent row in the Usage Profile Gtk.TreeView() to add
            the new item.
        :return: None
        """
        _new_row: Gtk.TreeIter = None
        _model = self.tvwTreeView.get_model()

        _node = tree.nodes[list(tree.nodes.keys())[0]]
        _entity = _node.data
        # The root node will have no data package, so this indicates the need
        # to clear the tree in preparation for the load.
        if _entity is None:
            _model.clear()
        elif _entity['usage_profile'].is_mission:
            _new_row = self._do_load_mission(
                **{
                    'entity': _entity['usage_profile'],
                    'identifier': _node.identifier,
                    'row': row
                })
        elif _entity['usage_profile'].is_phase:
            _new_row = self._do_load_phase(
                **{
                    'entity': _entity['usage_profile'],
                    'identifier': _node.identifier,
                    'row': row
                })
        elif _entity['usage_profile'].is_env:
            _new_row = self._do_load_environment(
                **{
                    'entity': _entity['usage_profile'],
                    'identifier': _node.identifier,
                    'row': row
                })

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, row=_new_row)

        super().do_expand_tree()

    def _on_module_switch(self, module: str = '') -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == 'stakeholder' and _row is not None:
            _code = _model.get_value(_row, self._lst_col_order[1])
            _name = _model.get_value(_row, self._lst_col_order[3])
            _title = _("Analyzing Usage Profile item {0:s}: {1:s}").format(
                str(_code), str(_name))

            pub.sendMessage('request_set_title', title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle row changes for the Usage Profile package List View.

        This method is called whenever a Usage Profile List View
        RAMSTKTreeView() row is activated or changed.

        :param selection: the Usage Profile class Gtk.TreeSelection().
        :return: None
        """
        _level: str = ''

        _model, _row = selection.get_selected()

        if _row is not None:
            self._record_id = _model.get_value(_row, 9)
            try:
                _prow = _model.iter_parent(_row)
                self._parent_id = _model.get_value(_prow, 9)
            except TypeError:
                self._parent_id = -1

            try:
                _level = _model.get_value(_row, 10)
                self._dic_attribute_keys = self._dic_element_keys[_level]
                self._dic_attribute_updater = self._dic_attributes[_level]
            except TypeError:
                _level = ''
                self._dic_attribute_keys = {}
                self._dic_attribute_updater = {}

            # Change the column headings depending on what is being selected.
            i = 0
            _columns = self.tvwTreeView.get_columns()
            for _heading in self._dic_headings[_level]:
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


class UsageProfile(RAMSTKListView):
    """Display Usage Profiles associated with the selected Revision.

    The attributes of a Usage Profile List View are:

    :cvar _module: the name of the module.

    :ivar _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dict class attributes.

    # Define private scalar class attributes.
    _module: str = 'usage_profile'
    _tablabel = "<span weight='bold'>" + _("Usage\nProfiles") + "</span>"
    _tabtooltip = _("Displays usage profiles for the selected revision.")
    _view_type = 'list'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize an instance of the Usage Profile list view.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_insert_sibling,
            self._do_request_insert_child,
            self._do_request_delete,
            self.do_request_update,
            self.do_request_update_all,
        ]
        self._lst_col_order = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self._lst_icons = [
            'insert_sibling',
            'insert_child',
            'remove',
            'save',
            'save-all',
        ]
        self._lst_mnu_labels = [
            _("Add Sibling"),
            _("Add Child"),
            _("Delete Selected"),
            _("Save Selected"),
            _("Save Profile"),
        ]
        self._lst_tooltips = [
            _("Add a new usage profile entity at the same level "
              "as the currently selected entity."),
            _("Add a new usage profile entity one level below the "
              "currently selected entity."),
            _("Delete the currently selected entity from the usage profile."),
            _("Save changes to the currently selected entity in the usage "
              "profile."),
            _("Save changes to all entities in the usage profile."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = UsageProfilePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_set_cursor_active,
                      'succeed_delete_usage_profile')
        pub.subscribe(self.do_set_cursor_active,
                      'succeed_insert_usage_profile')
        pub.subscribe(self.do_set_cursor_active,
                      'succeed_update_usage_profile')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_delete_environment')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_delete_mission')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_delete_mission_phase')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_environment')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_insert_mission')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_mission_phase')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_update_usage_profile')

    # pylint: disable=unused-argument
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected Usage Profile record.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()
        _node_id = _model.get_value(_row, 9)
        _level = _model.get_value(_row, 11)

        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _dialog = super().do_raise_dialog(parent=_parent)
        _dialog.do_set_message(
            message=_("You are about to delete {1:s} {0:s} and all data "
                      "associated with it.  Is this really what you want to "
                      "do?").format(_node_id, _level))
        _dialog.do_set_message_type(message_type='question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            self.__do_request_delete(_level)

        _dialog.do_destroy()

    # pylint: disable=unused-argument
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to add an entity to the Usage Profile.

        :return: None
        """
        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self.tvwTreeView.selection.get_selected()
        _level = _model.get_value(_row, 11)
        _prow = _model.iter_parent(_row)

        super().do_set_cursor_busy()
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
            _parent = self.get_parent().get_parent().get_parent().get_parent(
            ).get_parent()
            _dialog = super().do_raise_dialog(parent=_parent)
            _dialog.do_set_message(
                message=_("An environmental condition cannot have a child."))
            _dialog.do_set_message_type(message_type='error')
            _dialog.do_run()
            _dialog.do_destroy()

    # pylint: disable=unused-argument
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to add a sibling entity to the Usage Profile.

        :return: None
        """
        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self.tvwTreeView.selection.get_selected()
        try:
            _level = _model.get_value(_row, 11)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _level = 'mission'
            _prow = None

        super().do_set_cursor_busy()
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

    def __do_request_delete(self, level: str) -> None:
        """Send the correct delete message.

        :param level: the indenture level of the Usage Profile element to
            delete.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()
        _node_id = _model.get_value(_row, 9)

        super().do_set_cursor_busy()
        if level == 'mission':
            pub.sendMessage('request_delete_mission',
                            revision_id=self._revision_id,
                            node_id=_node_id)
        elif level == 'phase':
            pub.sendMessage('request_delete_mission_phase',
                            revision_id=self._revision_id,
                            mission_id=self._parent_id,
                            node_id=_node_id)
        elif level == 'environment':
            pub.sendMessage('request_delete_environment',
                            revision_id=self._revision_id,
                            phase_id=self._parent_id,
                            node_id=_node_id)

    def __make_ui(self):
        """Build the user interface for the usage profile list view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_set_callbacks()
        for _element in ['mission', 'phase', 'environment']:
            self._pnlPanel.dic_icons[_element] = self._dic_icons[_element]
