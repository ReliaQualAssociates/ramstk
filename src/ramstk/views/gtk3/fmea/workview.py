# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.fmea.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK base FME(C)A Work View."""

# Standard Library Imports
import json
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTK_CONTROL_TYPES, RAMSTK_CRITICALITY,
    RAMSTK_FAILURE_PROBABILITY, RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.assistants import AddControlAction
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton, RAMSTKLabel, RAMSTKPanel,
    RAMSTKTextView, RAMSTKWorkView
)


def do_request_insert(attributes: Dict[str, Any], level: str,
                      parent_id: str) -> None:
    """Send the correct request for the FMEA item to insert.

    :param dict attributes: the attributes of the currently selected
        element in the FMEA.
    :param str level: the indenture level in the FMEA of the new element to
        insert.
    :param str parent_id: the node ID in the FMEA treelib Tree() of the
        parent element.
    :return: None
    :rtype: None
    """
    if level == 'mode':
        pub.sendMessage('request_insert_fmea_mode')
    elif level == 'mechanism':
        pub.sendMessage('request_insert_fmea_mechanism',
                        mode_id=str(parent_id))
    elif level == 'cause':
        pub.sendMessage('request_insert_fmea_cause',
                        mode_id=attributes['mode_id'],
                        mechanism_id=attributes['mechanism_id'],
                        parent_id=str(parent_id))
    elif level in ['control', 'action']:
        pub.sendMessage('request_insert_fmea_{0:s}'.format(level),
                        cause_id=attributes['cause_id'],
                        parent_id=str(parent_id))


def get_indenture_level(record_id: str) -> str:
    """Determine the FMEA indenture level based on the record ID.

    :param record_id: the ID of the record to determine the indenture
        level.
    :return: _level; the level in the FMEA that is currently selected.
    :rtype: str
    """
    _level = ''

    if record_id.count(".") == 0:
        _level = 'mode'
    elif record_id.count(".") == 1:
        _level = 'mechanism'
    elif record_id.count(".") == 2:
        _level = 'cause'
    elif record_id.count(".") == 4 and record_id[-1] == "c":
        _level = 'control'
    elif record_id.count(".") == 4 and record_id[-1] == "a":
        _level = 'action'

    return _level


class MethodPanel(RAMSTKPanel):
    """Panel to display FMEA criticality methods."""
    def __init__(self):
        """Initialize an instance of the FMEA methods panel."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            0: ['calculate_1629a', 'boolean'],
            1: ['calculate_rpn', 'boolean'],
        }

        # Initialize private list attributes.
        self._lst_labels: List[str] = [
            "",
            "",
            _("Item Criticality:"),
        ]

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkCriticality: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Calculate Criticality"))
        self.chkRPN: RAMSTKCheckButton = RAMSTKCheckButton(
            label=_("Calculate RPNs"))
        self.txtItemCriticality: RAMSTKTextView = RAMSTKTextView(
            Gtk.TextBuffer())

        self._lst_widgets = [
            self.chkCriticality, self.chkRPN, self.txtItemCriticality
        ]

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_fixed()
        self.__do_set_callbacks()

        # Move the item criticality RAMSTKTextView() below it's label.
        _fixed: Gtk.Fixed = self.get_children()[0].get_children()[0].get_child(
        )
        _label: RAMSTKLabel = _fixed.get_children()[-2]
        _x_pos: int = _fixed.child_get_property(_label, 'x')
        _y_pos: int = _fixed.child_get_property(_label, 'y') + 25
        _fixed.move(self.txtItemCriticality.scrollwindow, _x_pos, _y_pos)

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_panel, 'request_clear_workviews')
        pub.subscribe(self._do_load_panel,
                      'succeed_calculate_fmea_criticality')

    def _do_clear_panel(self) -> None:
        """Clear the widgets on the panel.

        :return: None
        :rtype: None
        """
        self.chkCriticality.do_update(0, signal="toggled")
        self.chkRPN.do_update(0, signal="toggled")

        self.txtItemCriticality.do_update("", signal='changed')

    def _do_load_panel(self, item_criticality: Dict[str, float]) -> None:
        """Update the item criticality RAMSTKTextView() with the results.

        :param item_criticality: the item criticality for the selected
            hardware item.
        :return: None
        :rtype: None
        """
        _item_criticality = ""
        for _key, _value in item_criticality.items():
            _item_criticality = _item_criticality + _key + ": " + str(
                _value) + "\n"

        self.txtItemCriticality.do_update(_item_criticality, 'changed')

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the FMEA widgets.

        :return: None
        :rtype: None
        """
        # ----- CHECKBUTTONS
        self.chkCriticality.dic_handler_id['toggled'] = (
            self.chkCriticality.connect('toggled',
                                        super().on_toggled, 0,
                                        'wvw_editing_fmea'))
        self.chkRPN.dic_handler_id['toggled'] = (self.chkRPN.connect(
            'toggled',
            super().on_toggled, 1, 'wvw_editing_fmea'))

    def __do_set_properties(self) -> None:
        """Set the properties of the Hardware (D)FME(C)A RAMSTK widgets.

        :return: None
        :rtype: None
        """
        # ----- BUTTONS
        # By default, calculate both Task 102 and RPN.
        self.chkCriticality.set_active(True)
        self.chkRPN.set_active(True)
        self.chkCriticality.do_set_properties(tooltip=_(
            "Select this option to calculate the MIL-STD-1629, Task 102 "
            "criticality analysis."))
        self.chkRPN.do_set_properties(tooltip=_(
            "Select this option to calculate the risk priority numbers "
            "(RPN)."))

        # ----- ENTRIES
        self.txtItemCriticality.do_set_properties(
            editable=False,
            height=125,
            tooltip=_(
                "Displays the MIL-STD-1629A, Task 102 item criticality for "
                "the selected hardware item."))


class FMEAPanel(RAMSTKPanel):
    """Panel to display FMEA analysis."""

    # Define private dictionary class attributes.
    _dic_column_masks: Dict[str, List[bool]] = {
        'mode': [
            True, True, True, True, True, True, True, True, True, True, True,
            True, True, True, True, True, True, True, True, True, False, True,
            False, False, False, False, False, False, False, False, False,
            False, False, False, True, False, False, False, True, True, False,
            True, False, False
        ],
        'mechanism': [
            True, True, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False, False, True, True, True, False, False, False, False,
            False, False, False, False, False, False, True, True, True, False,
            False, True, True, False, False
        ],
        'cause': [
            True, True, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False, False, True, True, True, False, False, False, False,
            False, False, False, False, False, False, True, True, True, False,
            False, False, True, False, False
        ],
        'control': [
            True, True, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, True, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False, False, False, True, False, False
        ],
        'action': [
            True, True, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, False, False, False,
            False, False, False, False, False, False, True, True, True, True,
            True, True, True, True, True, False, False, False, False, False,
            False, False, True, False, False
        ]
    }
    _dic_headings = {
        'mode': [_("Mode ID"), _("Failure\nMode")],
        'mechanism': [_("Mechanism ID"),
                      _("Failure\nMechanism")],
        'cause': [_("Cause ID"), _("Failure\nCause")],
        'control': [_("Control ID"), _("Existing\nControl")],
        'action': [_("Action ID"), _("Recommended\nAction")]
    }

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'fmea'

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self):
        """Initialize an instance of the FMEA analysis panel."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_attribute_keys: Dict[int, List[str]] = {
            1: ['description', 'text'],
            2: ['mission', 'text'],
            3: ['mission_phase', 'text'],
            4: ['effect_local', 'text'],
            5: ['effect_next', 'text'],
            6: ['effect_end', 'text'],
            7: ['detection_method', 'text'],
            8: ['other_indications', 'text'],
            9: ['isolation_method', 'text'],
            10: ['design_provisions', 'text'],
            11: ['operator_actions', 'text'],
            12: ['severity_class', 'text'],
            13: ['hazard_rate_source', 'text'],
            14: ['mode_probability', 'float'],
            15: ['effect_probability', 'float'],
            16: ['mode_ratio', 'float'],
            17: ['mode_hazard_rate', 'float'],
            18: ['mode_op_time', 'float'],
            19: ['mode_criticality', 'float'],
            20: ['type_id', 'integer'],
            21: ['rpn_severity', 'integer'],
            22: ['rpn_occurrence', 'integer'],
            23: ['rpn_detection', 'integer'],
            24: ['rpn', 'integer'],
            25: ['action_category', 'integer'],
            26: ['action_owner', 'integer'],
            27: ['action_due_date', 'text'],
            28: ['action_status', 'integer'],
            29: ['action_taken', 'text'],
            30: ['action_approved', 'boolean'],
            31: ['action_approve_date', 'text'],
            32: ['action_closed', 'boolean'],
            33: ['action_close_date', 'text'],
            34: ['rpn_severity_new', 'integer'],
            35: ['rpn_occurrence_new', 'integer'],
            36: ['rpn_detection_new', 'integer'],
            37: ['rpn_new', 'integer'],
            38: ['critical_item', 'boolean'],
            39: ['single_point', 'boolean'],
            40: ['pof_include', 'boolean'],
            41: ['remarks', 'text'],
        }
        self._dic_mission_phases: Dict[str, List[str]] = {"": [""]}
        self._dic_row_loader = {
            'mode': self.__do_load_mode,
            'mechanism': self.__do_load_mechanism,
            'cause': self.__do_load_cause,
            'control': self.__do_load_control,
            'action': self.__do_load_action,
        }

        # Initialize private list attributes.
        self._lst_fmea_data: List[Any] = [
            0, "Description", "Mission", "Mission Phase", "Effect, Local",
            "Effect, Next", "Effect, End", "Detection Method", "Other "
            "Indications", "Isolation Method", "Design Provision",
            "Operator Actions", "Severity Class", "h(t) Data Source",
            "Failure Probability", 0.0, 0.0, 0.0, 0.0, 0.0, "Control Type",
            "RPN Severity", "RPN Occurrence", "RPN Detection", 0, "Action "
            "Category", "Action Owner", "Action Due Date", "Action Status",
            "Action Taken", 0, "Action Approval Date", 0,
            "Action Closure Date", "RPN New Severity", "RPN New Occurrence",
            "RPN New Detection", 0, 0, 0, 0, "Remarks", None, ""
        ]
        self._lst_missions: List[str] = [""]

        # Initialize private scalar attributes.
        self._title = _(
            "(Design) Failure Mode, Effects, (and Criticality) Analysis "
            "[(D)FME(C)A]")

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dic_action_category: Dict[int, Tuple[str, str, str, int]] = {}
        self.dic_action_status: Dict[int, Tuple[str, str, str]] = {}
        self.dic_detection: Dict[int, Dict[str, Any]] = {}
        self.dic_icons: Dict[str, str] = {}
        self.dic_occurrence: Dict[int, Dict[str, Any]] = {}
        self.dic_severity: Dict[int, Dict[str, Any]] = {}
        self.dic_users: Dict[int, Tuple[str, str, str, str, str]] = {}

        # Make a fixed type panel.
        self.__do_set_properties()
        super().do_make_panel_treeview()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_clear_tree, 'request_clear_workviews')
        pub.subscribe(super().do_load_panel, 'succeed_retrieve_hardware_fmea')
        pub.subscribe(super().do_load_panel, 'succeed_calculate_rpn')

        # pub.subscribe(self._do_load_panel,
        #              'succeed_calculate_fmea_criticality')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_action')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_cause')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_control')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_mechanism')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_mode')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_delete_fmea')

        pub.subscribe(self.__do_load_missions,
                      'succeed_get_usage_profile_attributes')

    def do_load_combobox(self) -> None:
        """Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        self.__do_load_action_category()
        self.__do_load_control_type()
        self.__do_load_failure_probability()
        self.__do_load_rpn_detection()
        self.__do_load_rpn_occurrence()
        self.__do_load_rpn_severity()
        self.__do_load_severity_class()
        self.__do_load_status()
        self.__do_load_users()

    def do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the FMEA widgets.

        :return: None
        :rtype: None
        """
        # CellRendererToggle columns.
        for _column in [30, 32, 38, 39, 40]:
            _cell = self.tvwTreeView.get_column(
                self._lst_col_order[_column]).get_cells()

            _cell[0].connect('toggled', super().on_cell_toggled, _column)

        # CellRendererCombo and CellRendererText columns.
        for _column in [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 33, 34, 35, 36,
                37, 41
        ]:
            _cell = self.tvwTreeView.get_column(
                self._lst_col_order[_column]).get_cells()

            _cell[0].connect('edited', self.__on_cell_edit, _column)

    # pylint: disable=unused-argument
    def _on_delete_insert_fmea(self, node_id: int, tree: treelib.Tree) -> None:
        """Update FMEA worksheet whenever an element is inserted or deleted.

        :param node_id: the ID of the inserted/deleted FMEA element.  This
            argument is broadcast with the PyPubSub message and must remain
            with it's current spelling.
        :param tree: the treelib Tree() containing the FMEA module's data.
        :return: None
        :rtype: None
        """
        super().do_load_panel(tree)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the FMEA Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param selection: the current Gtk.TreeViewSelection() in the
            FMEA RAMSTKTreView().
        :type selection: :class:`Gtk.TreeViewSelection`
        :return: None
        :rtype: None
        """
        _model, _row = selection.get_selected()

        try:
            self._record_id = _model.get_value(_row, 0)
            _mission = _model.get_value(_row, 2)
        except TypeError:
            self._record_id = '0'
            _mission = ""

        _level = get_indenture_level(self._record_id)
        (self.tvwTreeView.headings['col0'],
         self.tvwTreeView.headings['col1']) = super().do_get_headings(_level)

        self._do_load_mission_phases(_mission)

        super().do_set_headings()

    def __do_get_mission(self, entity: object) -> None:
        """Retrieve the mission information.

        :param entity: the FMEA entity to get the mission information.
        :return: None
        :rtype: None
        """
        try:
            # noinspection PyUnresolvedReferences
            self._lst_fmea_data[2] = self._dic_missions[
                entity.mission]  # type: ignore
        except (AttributeError, KeyError):
            self._lst_fmea_data[2] = ""

        try:
            # noinspection PyUnresolvedReferences
            self._lst_fmea_data[3] = self._dic_mission_phases[
                entity.mission_phase]  # type: ignore
        except (AttributeError, KeyError):
            self._lst_fmea_data[3] = ""

    def __do_get_rpn_names(self, entity: object) -> Tuple[str, str, str, str]:
        """Retrieve the RPN category for the selected mechanism or cause.

        :param entity: the RAMSTKMechanism or RAMSTKCause object to be read.
        :return: (_occurrence, _detection, _occurrence_new, _detection_new)
        :rtype: tuple
        """
        # noinspection PyUnresolvedReferences
        _occurrence = str(
            self.dic_occurrence[entity.rpn_occurrence]['name'])  # type: ignore
        # noinspection PyUnresolvedReferences
        _detection = str(
            self.dic_detection[entity.rpn_detection]['name'])  # type: ignore
        # noinspection PyUnresolvedReferences
        _occurrence_new = str(
            self.dic_occurrence[entity.rpn_occurrence_new]  # type: ignore
            ['name'])
        # noinspection PyUnresolvedReferences
        _detection_new = str(
            self.dic_detection[entity.rpn_detection_new]  # type: ignore
            ['name'])

        return _occurrence, _detection, _occurrence_new, _detection_new

    def __do_get_rpn_values(self, position: int, name: str) -> int:
        """Retrieve the RPN value for the selected SOD description.

        :param str name: the noun name in the severity, detection,
            or occurrence list.
        :return: _value
        :rtype: int
        """
        _rpn = {}
        _value = 0

        _rpn = {
            21: self.dic_severity,
            22: self.dic_occurrence,
            23: self.dic_detection,
            34: self.dic_severity,
            35: self.dic_occurrence,
            36: self.dic_detection,
        }[position]

        for _item in _rpn.items():
            if _item[1]['name'] == name:
                _value = int(_item[1]['value'])

        return _value

    def __do_load_action(self, node: treelib.Node,
                         row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load an action record into the RAMSTKTreeView().

        :param node: the treelib Node() with the action data to load.
        :param row: the parent row of the action to load into the FMEA form.
        :return: _new_row; the row that was just populated with action data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["action"], 22, 22)

        _attributes = [
            node.identifier, _entity.action_recommended, "", "", "", "", "",
            "", "", "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, "", "",
            "", "", 0, _entity.action_category, _entity.action_owner,
            _entity.action_due_date.strftime('%Y-%m-%d'),
            _entity.action_status, _entity.action_taken,
            _entity.action_approved,
            _entity.action_approve_date.strftime('%Y-%m-%d'),
            _entity.action_closed,
            _entity.action_close_date.strftime('%Y-%m-%d'), "", "", "", 0, 0,
            0, 0, "", _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure cause action {0:s} "
                "in the FMEA.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}").format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_action_category(self) -> None:
        """Load the action category Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[25])
        for _item in self.dic_action_category:
            _model.append([self.dic_action_category[_item][1]])

    def __do_load_cause(self, node: treelib.Node,
                        row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure cause record into the RAMSTKTreeView().

        :param node: the treelib Node() with the cause data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the cause to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with cause data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        (_occurrence, _detection, _occurrence_new,
         _detection_new) = self.__do_get_rpn_names(_entity)

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["cause"],
                                                       22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", "", "", "", "", "",
            "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, "", "",
            _occurrence, _detection, _entity.rpn, "", "", "", "", "", 0, "", 0,
            "", "", _occurrence_new, _detection_new, _entity.rpn_new, 0, 0, 0,
            "", _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure cause {0:s} in the "
                "FMEA.  This might indicate it was missing it's data package, "
                "some of the data in the package was missing, or some of the "
                "data was the wrong type.  Row data was: {1}").format(
                    str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_control(self, node: treelib.Node,
                          row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a control record into the RAMSTKTreeView().

        :param node: the treelib Node() with the control data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the control to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with control data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["control"], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", "", "", "", "", "",
            "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, _entity.type_id,
            "", "", "", 0, "", "", "", "", "", 0, "", 0, "", "", "", "", 0, 0,
            0, 0, "", _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure cause control {0:s} "
                "in the FMEA.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: {1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_control_type(self) -> None:
        """Load the control type Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[20])
        for _item in RAMSTK_CONTROL_TYPES:
            _model.append([_item])

    def __do_load_failure_probability(self) -> None:
        """Load the failure probability Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[14])
        for _item in RAMSTK_FAILURE_PROBABILITY:
            _model.append([_item[0]])

    def __do_load_mechanism(self, node: treelib.Node,
                            row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        (_occurrence, _detection, _occurrence_new,
         _detection_new) = self.__do_get_rpn_names(_entity)

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["mechanism"], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", "", "", "", "", "",
            "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, "", "",
            _occurrence, _detection, _entity.rpn, "", "", "", "", "", 0, "", 0,
            "", "", _occurrence_new, _detection_new, _entity.rpn_new, 0, 0,
            _entity.pof_include, "", _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure mechanism {0:s} in "
                "the FMEA.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: {1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_missions(self, attributes: treelib.Tree) -> None:
        """Load the mission and mission phase dicts.

        :param attributes: the treelib Tree() containing the usage profile.
        :type attributes: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _nid = attributes.root
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[2])

        self._lst_missions = [""]
        _model.append([""])
        for _node in attributes.children(_nid):
            _model.append([_node.tag])
            self._lst_missions.append(_node.tag)

    def __do_load_mission_phases(self, mission: str) -> None:
        """Load the mission phase Gtk.CellRendererCombo().

        :param str mission: the mission that was selected.
        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[3])
        _model.append([""])

        try:
            for _phase in self._dic_mission_phases[mission]:
                _model.append([_phase])
        except KeyError:
            pass

    def __do_load_mode(self, node: treelib.Node,
                       row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a failure mode record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the FMEA form.
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.tvwTreeView.get_model()

        _severity = self.dic_severity[_entity.rpn_severity]['name']
        _severity_new = self.dic_severity[_entity.rpn_severity_new]['name']
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self.dic_icons["mode"],
                                                       22, 22)

        self.__do_get_mission(_entity)

        _attributes = [
            node.identifier, _entity.description, _entity.mission,
            _entity.mission_phase, _entity.effect_local, _entity.effect_next,
            _entity.effect_end, _entity.detection_method,
            _entity.other_indications, _entity.isolation_method,
            _entity.design_provisions, _entity.operator_actions,
            _entity.severity_class, _entity.hazard_rate_source,
            _entity.mode_probability, _entity.effect_probability,
            _entity.mode_ratio, _entity.mode_hazard_rate, _entity.mode_op_time,
            _entity.mode_criticality, "", _severity, "", "", 0, "", "", "", "",
            "", 0, "", 0, "", _severity_new, "", "", 0, _entity.critical_item,
            _entity.single_point, 0, _entity.remarks, _icon
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading failure mode {0:s} in the "
                "FMEA.  This might indicate it was missing it's data package, "
                "some of the data in the package was missing, or some of the "
                "data was the wrong type.  Row data was: {1}").format(
                    str(node.identifier), _attributes)
            pub.sendMessage('do_log_warning_msg',
                            logger_name='WARNING',
                            message=_message)

        return _new_row

    def __do_load_rpn_detection(self) -> None:
        """Load the RPN detection Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        for _position in [23, 36]:
            _model = self.tvwTreeView.get_cell_model(
                self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(self.dic_detection):
                _model.append([self.dic_detection[_item]['name']])

    def __do_load_rpn_occurrence(self) -> None:
        """Load the RPN occurrence Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        for _position in [22, 35]:
            _model = self.tvwTreeView.get_cell_model(
                self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(self.dic_occurrence):
                _model.append([self.dic_occurrence[_item]['name']])

    def __do_load_rpn_severity(self) -> None:
        """Load the RPN severity Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        for _position in [21, 34]:
            _model = self.tvwTreeView.get_cell_model(
                self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(self.dic_severity):
                _model.append([self.dic_severity[_item]['name']])

    def __do_load_severity_class(self) -> None:
        """Load the severity classification Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[12])
        for _item in RAMSTK_CRITICALITY:
            _model.append([_item[0]])

    def __do_load_status(self) -> None:
        """Load the action status Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[28])
        for _item in self.dic_action_status:
            _model.append([self.dic_action_status[_item][0]])

    def __do_load_users(self) -> None:
        """Load the RAMSTK users Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_cell_model(self._lst_col_order[26])
        for _item in self.dic_users:
            _user = (self.dic_users[_item][0] + ", "
                     + self.dic_users[_item][1])
            _model.append([_user])

    def __do_set_properties(self) -> None:
        """Set the properties of the Hardware (D)FME(C)A RAMSTK widgets.

        :return: None
        :rtype: None
        """
        # noinspection PyTypeChecker
        super().do_set_properties(bold=True, title=self._title)

        self.tvwTreeView.set_tooltip_text(
            _("Displays the (Design) Failure Mode and Effects "
              "(and Criticality) Analysis [(D)FME(C)A] for the "
              "currently selected Hardware item."))

    def __on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: Any,
                       position: int) -> None:
        """Handle edits of the FMEA Work View RAMSTKTreeview().

        :param Gtk.CellRenderer cell: the Gtk.CellRenderer() that was edited.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param position: the column position of the edited
            Gtk.CellRenderer().
        :return: None
        """
        self.tvwTreeView.do_edit_cell(cell, path, new_text, position)

        if position in [21, 22, 23, 34, 35, 36]:
            new_text = self.__do_get_rpn_values(self._lst_col_order[position],
                                                new_text)

        try:
            _key = self._dic_column_keys[self._lst_col_order[position]]
        except (IndexError, KeyError):
            _key = ''

        #// TODO: Update ramstk_action fld_action_recommended to fld_description.
        #//
        #// Updating fld_action_recommended to fld_description makes
        #// ramstk_action consistent with other FMEA tables in position 1.
        if self._lst_col_order[position] == 1 and self._record_id[-1] == 'a':
            _key = 'action_recommended'

        pub.sendMessage('wvw_editing_fmea',
                        node_id=[self._record_id, -1],
                        package={_key: new_text})


class FMEA(RAMSTKWorkView):
    """Display FMEA attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (FMEA). The attributes of a FMEA Work View are:

    :cvar dict _dic_column_masks: dict with the list of masking values for
        the FMEA worksheet.  Key is the FMEA indenture level, value is a
        list of True/False values for each column in the worksheet.
    :cvar dict _dic_headings: dict with the variable headings for the first two
        columns.  Key is the name of the FMEA indenture level, value is a list
        of heading text.
    :cvar dict _dic_keys:
    :cvar dict _dic_column_keys:
    :cvar list _lst_control_type: list containing the types of controls that
        can be implemented.
    :cvar list _lst_labels: list containing the label text for each widget
        label.
    :cvar bool _pixbuf: indicates whether or icons are displayed in the
        RAMSTKTreeView.  If true, a GDKPixbuf column will be appended when
        creating the RAMSTKTreeView.  Default is True.
    :cvar str _module: the name of the module.

    :ivar list _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar list _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar list _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar list _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    :ivar dict _dic_missions: dict containing all this missions associated
        with the selected Revision.
    :ivar dict _dic_mission_phases: dict containing all the mission phases
        associated with each mission in _dic_missions.
    :ivar float _item_hazard_rate: hazard rate of the Hardware item associated
        with the FMEA.
    """

    # Define private dictionary attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _module: str = 'fmea'
    _pixbuf: bool = True
    _tablabel: str = _("FMEA")
    _tabtooltip: str = _("Displays failure mode and effects "
                         "analysis (FMEA) information for the selected "
                         "Hardware item.")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        """Initialize the Work View for the FMEA.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks: List[object] = [
            self._do_request_insert_sibling,
            self._do_request_insert_child,
            self._do_request_delete,
            self._do_request_calculate,
            self._do_request_update,
            self._do_request_update_all,
        ]
        self._lst_icons: List[str] = [
            "insert_sibling",
            "insert_child",
            "remove",
            "calculate",
            'save',
            'save-all',
        ]
        self._lst_mnu_labels: List[str] = [
            _("Add Sibling"),
            _("Add Child"),
            _("Delete Selected"),
            _("Save Selected"),
            _("Save (D)FME(C)A"),
        ]
        self._lst_tooltips: List[str] = [
            _("Add a new (D)FME(C)A entity at the same level as the "
              "currently selected entity."),
            _("Add a new (D)FME(C)A entity one level below the currently "
              "selected entity."),
            _("Delete the selected entity from the (D)FME(C)A."),
            _("Calculate the Task 102 criticality and/or risk priority "
              "number (RPN)."),
            _("Save changes to the selected entity in the (D)FME(C)A."),
            _("Save changes to all entities in the (D)FME(C)A."),
        ]

        # Initialize private scalar attributes.
        self._item_hazard_rate: float = 0.0

        self._pnlMethods: RAMSTKPanel = MethodPanel()
        self._pnlPanel: RAMSTKPanel = FMEAPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()
        self.__do_set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_parent, 'selected_hardware')
        pub.subscribe(self._on_get_hardware_attributes,
                      'succeed_get_all_hardware_attributes')

        # pub.subscribe(self.do_set_cursor_active, 'succeed_delete_fmea')
        pub.subscribe(self.do_set_cursor_active, 'succeed_insert_fmea')
        pub.subscribe(self.do_set_cursor_active, 'succeed_update_fmea')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_delete_fmea')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_insert_action')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_insert_cause')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_insert_control')
        pub.subscribe(self.do_set_cursor_active_on_fail,
                      'fail_insert_mechanism')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_insert_mode')
        pub.subscribe(self.do_set_cursor_active_on_fail, 'fail_update_fmea')

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Calculate the FMEA RPN or criticality.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        if self._pnlMethods.chkCriticality.get_active():
            pub.sendMessage("request_calculate_criticality",
                            item_hr=self._item_hazard_rate)

        if self._pnlMethods.chkRPN.get_active():
            pub.sendMessage("request_calculate_rpn", method='mechanism')

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected entity from the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected(
        )
        _node_id = _model.get_value(_row, 0)

        super().do_set_cursor_busy()
        pub.sendMessage("request_delete_fmea", node_id=_node_id)
        super().do_set_cursor_active()

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected(
        )
        try:
            _parent_id = _model.get_value(_row, 0)
            _attributes = _model.get_value(_row, 43).replace("'", '"')
            _attributes = json.loads("{0}".format(_attributes))
            _level = get_indenture_level(self._record_id)
        except TypeError:
            _parent_id = '0'
            _attributes = {}
            _level = 'mode'

        _level = {
            'mode': 'mechanism',
            'mechanism': 'cause',
            'cause': 'control_action'
        }[_level]

        if _level == 'control_action':
            _level = self.__on_request_insert_control_action()

        super().do_set_cursor_busy()
        do_request_insert(_attributes, _level, _parent_id)

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected(
        )
        try:
            _attributes = _model.get_value(_row, 43).replace("'", '"')
            _attributes = json.loads("{0}".format(_attributes))
            _parent_id = _model.get_value(_model.iter_parent(_row), 0)
            _level = get_indenture_level(self._record_id)
        except TypeError:
            _attributes = {}
            _parent_id = '0'
            _level = 'mode'

        if _level in ['control', 'action']:
            _level = self.__on_request_insert_control_action()

        super().do_set_cursor_busy()
        do_request_insert(_attributes, _level, _parent_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Request to save the currently selected entity in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_fmea', node_id=self._record_id)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """Request to save all the entities in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        super().do_set_cursor_busy()
        pub.sendMessage('request_update_all_fmea')

    def _do_set_parent(self, attributes: Dict[str, Any]) -> None:
        """Set the parent (hardware) ID when a new hardware item is selected.

        :param dict attributes: the attributes of the newly selected hardware
            item.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes['hardware_id']

    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the hardware item hazard rate.

        :param attributes:
        :return:
        """
        self._item_hazard_rate = attributes['hazard_rate_active']

    def __do_set_callbacks(self) -> None:
        """Set the callback methods and functions for the FMEA widgets.

        :return: None
        :rtype: None
        """
        self._pnlPanel.tvwTreeView.dic_handler_id[
            'button-press'] = self._pnlPanel.tvwTreeView.connect(
                "button_press_event",
                super().on_button_press)

    def __make_ui(self) -> None:
        """Build the user interface for the FMEA tab.

        :return: None
        :rtype: None
        """
        _hpaned: Gtk.HPaned = super().do_make_layout_lr()

        self._pnlPanel.dic_action_category = \
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_CATEGORY
        self._pnlPanel.dic_action_status = \
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_STATUS
        self._pnlPanel.dic_detection =  \
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION
        self._pnlPanel.dic_occurrence =  \
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE
        self._pnlPanel.dic_severity =  \
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY
        self._pnlPanel.dic_users = self.RAMSTK_USER_CONFIGURATION.RAMSTK_USERS
        self._pnlPanel.dic_icons = self._dic_icons

        self.do_embed_treeview_panel()
        self._pnlPanel.do_load_combobox()
        self._pnlPanel.do_set_callbacks()

        self.remove(self.get_children()[-1])
        _hpaned.pack1(self._pnlMethods, True, True)
        _hpaned.pack2(self._pnlPanel, True, True)

        self.show_all()

    def __on_request_insert_control_action(self) -> str:
        """Raise dialog to select whether to add a control or action.

        :return: _level; the level to add, control or action.
        :rtype: str
        """
        _level = ""

        _dialog = AddControlAction(
            parent=self.get_parent().get_parent().get_parent().get_parent())

        if _dialog.do_run() == Gtk.ResponseType.OK:
            if _dialog.rdoControl.get_active():
                _level = "control"
            elif _dialog.rdoAction.get_active():
                _level = "action"

        _dialog.do_destroy()

        return _level
