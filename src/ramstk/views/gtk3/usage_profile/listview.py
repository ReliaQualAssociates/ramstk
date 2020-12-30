# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.usage_profile.listview.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK Usage Profile list view."""

# Standard Library Imports
from typing import Any, Dict, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKListView, RAMSTKPanel


# noinspection PyUnresolvedReferences,PyTypeChecker
class UsageProfilePanel(RAMSTKPanel):
    """Panel to display hierarchical list of usage profiles."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'usage_profile'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the usage profile panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_attributes: Dict[str, Dict[str, Any]] = {
            'mission': {
                'description': [None, 'edited', 1],
                'time_units': [None, 'edited', 3],
                'mission_time': [None, 'edited', 5],
            },
            'phase': {
                'name': [None, 'edited', 1],
                'description': [None, 'edited', 2],
                'phase_start': [None, 'edited', 4],
                'phase_end': [None, 'edited', 5],
            },
            'environment': {
                'name': [None, 'edited', 1],
                'units': [None, 'edited', 3],
                'minimum': [None, 'edited', 4],
                'maximum': [None, 'edited', 5],
                'mean': [None, 'edited', 6],
                'variance': [None, 'edited', 7],
            }
        }
        self._dic_element_keys = {
            'mission': {
                1: ['description', 'string'],
                3: ['time_units', 'string'],
                5: ['mission_time', 'float'],
            },
            'phase': {
                1: ['name', 'string'],
                2: ['description', 'string'],
                4: ['phase_start', 'float'],
                5: ['phase_end', 'float'],
            },
            'environment': {
                1: ['name', 'string'],
                3: ['units', 'string'],
                4: ['minimum', 'float'],
                5: ['maximum', 'float'],
                6: ['mean', 'float'],
                7: ['variance', 'float'],
            }
        }
        self._dic_headings = {
            'mission': {
                'col0': _("Mission ID"),
                'col1': _("Mission Description"),
                'col2': _(""),
                'col3': _("Units"),
                'col4': _("Start Time"),
                'col5': _("End Time"),
                'col6': _(""),
                'col7': _(""),
                'col8': _(""),
                'col9': _(""),
                'col10': _(""),
                'pixbuf': _(""),
            },
            'phase': {
                'col0': _("Phase ID"),
                'col1': _("Phase Name"),
                'col2': _("Phase Description"),
                'col3': _(""),
                'col4': _("Start Time"),
                'col5': _("End Time"),
                'col6': _(""),
                'col7': _(""),
                'col8': _(""),
                'col9': _(""),
                'col10': _(""),
                'pixbuf': _(""),
            },
            'environment': {
                'col0': _("Environment ID"),
                'col1': _("Condition Name"),
                'col2': _(""),
                'col3': _("Units"),
                'col4': _("Minimum Value"),
                'col5': _("Maximum Value"),
                'col6': _("Mean Value"),
                'col7': _("Variance"),
                'col8': _(""),
                'col9': _(""),
                'col10': _(""),
                'pixbuf': _(""),
            },
        }
        self._dic_row_loader = {
            'mission': self.__do_load_mission,
            'mission_phase': self.__do_load_phase,
            'environment': self.__do_load_environment,
        }
        self._dic_visible = {
            'mission': {
                'col0': True,
                'col1': True,
                'col2': False,
                'col3': True,
                'col4': True,
                'col5': True,
                'col6': False,
                'col7': False,
                'col8': False,
                'col9': False,
                'col10': False,
                'pixbuf': False,
            },
            'phase': {
                'col0': True,
                'col1': True,
                'col2': True,
                'col3': False,
                'col4': True,
                'col5': True,
                'col6': False,
                'col7': False,
                'col8': False,
                'col9': False,
                'col10': False,
                'pixbuf': False,
            },
            'environment': {
                'col0': True,
                'col1': True,
                'col2': False,
                'col3': True,
                'col4': True,
                'col5': True,
                'col6': True,
                'col7': True,
                'col8': False,
                'col9': False,
                'col10': False,
                'pixbuf': False,
            },
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._title = _("Usage Profile")

        # Initialize public dictionary class attributes.
        self.dic_icons = {'mission': None, 'phase': None, 'environment': None}
        self.dic_units: Dict[str, Tuple[str, str, str]] = {}

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel_treeview()

        # Subscribe to PyPubSub messages.
        # ISSUE: Move PyPubSub subscribers up to RAMSTKPanel() class.
        # //
        # // The subscribers in each List, Module, and Work View for the
        # // succeed_retrieve_{0}, succeed_insert_{0}, and succeed_delete_{0}
        # // topics should be moved to the RAMSTKPanel() class once all the
        # // data managers have been refactored so the applicable methods are
        # // publishing the correct MDS.
        pub.subscribe(super().do_load_panel,
                      'succeed_retrieve_{0}'.format(self._module))
        pub.subscribe(super().do_load_panel,
                      'succeed_insert_{0}'.format(self._module))
        pub.subscribe(super().on_delete,
                      'succeed_delete_{0}'.format(self._module))

    def do_load_combobox(self) -> None:
        """Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[3])
        for _unit in self.dic_units:
            _model.append([self.dic_units[_unit][1]])

    def do_set_callbacks(self) -> None:
        """Set callbacks for the stakeholder input list view.

        :return: None
        """
        super().do_set_callbacks()
        super().do_set_cell_callbacks('lvw_editing_usage_profile',
                                      [1, 2, 3, 4, 5, 6, 7])

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
            self._record_id = _model.get_value(_row, 8)
            try:
                _prow = _model.iter_parent(_row)
                self._parent_id = _model.get_value(_prow, 0)
            except TypeError:
                self._parent_id = -1

            try:
                _level = _model.get_value(_row, 10)
                self._dic_attribute_keys = self._dic_element_keys[_level]
                self._dic_attribute_updater = self._dic_attributes[_level]

                # Change the column headings depending on what is being
                # selected.
                self.tvwTreeView.headings = self._dic_headings[_level]
                self.tvwTreeView.visible = self._dic_visible[_level]
                super().do_set_headings()

                pub.sendMessage('selected_usage_profile',
                                attributes={'record_id': self._record_id})
            except TypeError:
                _level = ''
                self._dic_attribute_keys = {}
                self._dic_attribute_updater = {}

    def __do_load_environment(self, node: treelib.Node,
                              row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load an environmental condition into the RAMSTK TreeView.

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons['environment'], 22, 22)

        _attributes = [
            _entity.environment_id, _entity.name, '', _entity.units,
            _entity.minimum, _entity.maximum, _entity.mean, _entity.variance,
            node.identifier, 1, 'environment', _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading environment {0:s} in the "
                "usage profile.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_mission(self, node: treelib.Node,
                          row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a mission into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # pylint: disable=unused-variable
        [[__, _entity]] = node.data.items()

        _model = self.tvwTreeView.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons['mission'], 22, 22)

        _attributes = [
            _entity.mission_id, _entity.description, '', _entity.time_units,
            0.0, _entity.mission_time, 0.0, 0.0, node.identifier, 0, 'mission',
            _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading mission {0:s} in the usage "
                "profile.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_phase(self, node: treelib.Node,
                        row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a mission phase into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons['phase'],
                                                       22, 22)
        _attributes = [
            _entity.phase_id, _entity.name, _entity.description, '',
            _entity.phase_start, _entity.phase_end, 0.0, 0.0, node.identifier,
            0, 'phase', _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading mission phase {0:s} in the "
                "usage profile.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row


class UsageProfile(RAMSTKListView):
    """Display Usage Profiles associated with the selected Revision.

    The attributes of a Usage Profile List View are:

    :cvar _module: the name of the module.

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
        self._lst_callbacks[0] = self._do_request_insert_sibling
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, self._do_request_delete)
        self._lst_col_order = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self._lst_icons[0] = 'insert_sibling'
        self._lst_icons.insert(1, 'insert_child')
        self._lst_icons.insert(2, 'remove')
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
        pub.subscribe(self._do_set_record_id, 'selected_usage_profile')

    # pylint: disable=unused-argument
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected Usage Profile record.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _model, _row = self._pnlPanel.tvwTreeView.selection.get_selected()
        _node_id = _model.get_value(_row, 8)
        _level = _model.get_value(_row, 10)

        _parent = self.get_parent().get_parent().get_parent().get_parent(
        ).get_parent()
        _dialog = super().do_raise_dialog(parent=_parent)
        _dialog.do_set_message(
            message=_("You are about to delete {1:s} {0:s} and all data "
                      "associated with it.  Is this really what you want to "
                      "do?").format(_node_id, _level))
        _dialog.do_set_message_type(message_type='question')

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                'request_delete_usage_profile',
                node_id=_node_id,
            )

        _dialog.do_destroy()

    # pylint: disable=unused-argument
    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to add an entity to the Usage Profile.

        :return: None
        """
        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self._pnlPanel.tvwTreeView.selection.get_selected()
        _level = _model.get_value(_row, 10)
        _prow = _model.iter_parent(_row)

        super().do_set_cursor_busy()
        if _level == 'mission':
            _mission_id = _model.get_value(_row, 0)
            pub.sendMessage(
                'request_insert_mission_phase',
                mission_id=_mission_id,
            )
        elif _level == 'phase':
            _phase_id = _model.get_value(_row, 0)
            _mission_id = _model.get_value(_prow, 0)
            pub.sendMessage(
                'request_insert_environment',
                mission_id=_mission_id,
                phase_id=_phase_id,
            )
        elif _level == 'environment':
            _error = _("An environmental condition cannot have a child.")
            _parent = self.get_parent().get_parent().get_parent().get_parent(
            ).get_parent()
            _dialog = super().do_raise_dialog(parent=_parent)
            _dialog.do_set_message(message=_error)
            _dialog.do_set_message_type(message_type='error')
            _dialog.do_run()
            _dialog.do_destroy()
            pub.sendMessage(
                "fail_insert_usage_profile",
                error_message=_error,
            )

    # pylint: disable=unused-argument
    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to add a sibling entity to the Usage Profile.

        :return: None
        """
        # Get the currently selected row, the level of the currently selected
        # item, and it's parent row in the Usage Profile.
        _model, _row = self._pnlPanel.tvwTreeView.selection.get_selected()
        try:
            _level = _model.get_value(_row, 10)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _level = 'mission'
            _prow = None

        super().do_set_cursor_busy()
        if _level == 'mission':
            pub.sendMessage('request_insert_mission', )
        elif _level == 'phase':
            _mission_id = _model.get_value(_prow, 0)
            pub.sendMessage(
                'request_insert_mission_phase',
                mission_id=_mission_id,
            )
        elif _level == 'environment':
            _gprow = _model.iter_parent(_prow)
            _mission_id = _model.get_value(_gprow, 0)
            _phase_id = _model.get_value(_prow, 0)
            pub.sendMessage(
                'request_insert_environment',
                mission_id=_mission_id,
                phase_id=_phase_id,
            )

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the usage profile's record ID.

        :param attributes: the attributes dict for the selected usage
            profile element.
        :return: None
        :rtype: None
        """
        self._record_id = attributes['record_id']

    def __make_ui(self):
        """Build the user interface for the usage profile list view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.dic_units = \
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS

        self._pnlPanel.do_set_properties()
        self._pnlPanel.do_load_combobox()
        self._pnlPanel.do_set_callbacks()
        self._pnlPanel.tvwTreeView.dic_handler_id[
            'button-press'] = self._pnlPanel.tvwTreeView.connect(
                "button_press_event",
                super().on_button_press)
        for _element in ['mission', 'phase', 'environment']:
            self._pnlPanel.dic_icons[_element] = self._dic_icons[_element]
