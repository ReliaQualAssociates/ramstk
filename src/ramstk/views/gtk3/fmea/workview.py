# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.fmea.workview.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2020 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK base FME(C)A Work View."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple
import json

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (RAMSTK_CONTROL_TYPES, RAMSTK_CRITICALITY,
                                  RAMSTK_FAILURE_PROBABILITY,
                                  RAMSTKUserConfiguration)
from ramstk.logger import RAMSTKLogManager
from ramstk.utilities import boolean_to_integer
from ramstk.views.gtk3 import Gdk, GdkPixbuf, Gtk, _
from ramstk.views.gtk3.assistants import AddControlAction
from ramstk.views.gtk3.widgets import (RAMSTKCheckButton, RAMSTKLabel,
                                       RAMSTKTextView, RAMSTKTreeView,
                                       RAMSTKWorkView)


def do_request_insert(attributes: Dict[str, Any], level: str,
                      parent_id: str) -> None:
    """
    Send the correct request for the FMEA item to insert.

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


class FMEA(RAMSTKWorkView):
    """
    Display FMEA attribute data in the Work Book.

    The WorkView displays all the attributes for the Failure Mode and Effects
    Analysis (FMEA). The attributes of a FMEA Work View are:

    :cvar list _lst_control_type: list containing the types of controls that
        can be implemented.
    :cvar list _lst_fmea_data: list containing the FMEA row data.

    :ivar dict _dic_missions: a dict containing all this missions associated
        with the selected Revision.
    :ivar dict _dic_mission_phases: a dict containing all the mission phases
        associated with each mission in _dic_missions.
    :ivar float _item_hazard_rate: the hazard rate of the Function or Hardware
        item associated with the FMEA.
    """

    # Define private class dict attributes.
    _dic_keys = {
        1: "description",
        2: "mission",
        3: "mission_phse",
        4: "effect_local",
        5: "effect_next",
        6: "effect_end",
        7: "detection_method",
        8: "other_indications",
        9: "isolation_method",
        10: "design_provisions",
        11: "operator_actions",
        12: "severity_class",
        13: "hazard_rate_source",
        14: "mode_probability",
        15: "effect_probability",
        16: "mode_ratio",
        17: "mode_hazard_rate",
        18: "mode_op_time",
        19: "mode_criticality",
        20: "type_id",
        21: "rpn_severity",
        22: "rpn_occurrence",
        23: "rpn_detection",
        24: "rpn",
        25: "action_category",
        26: "action_owner",
        27: "action_due_date",
        28: "action_status",
        29: "action_taken",
        30: "action_approved",
        31: "action_approve_date",
        32: "action_closed",
        33: "action_close_date",
        34: "rpn_severity_new",
        35: "rpn_occurrence_new",
        36: "rpn_detection_new",
        37: "rpn_new",
        38: "critical_item",
        39: "single_point",
        40: "pof_include",
        41: "remarks"
    }
    _dic_column_keys = _dic_keys

    # Define private class list attributes.
    _lst_control_type: List[bool] = [_("Prevention"), _("Detection")]
    _lst_mode_mask: List[bool] = [
        True, True, True, True, True, True, True, True, True, True, True, True,
        True, True, True, True, True, True, True, True, False, True, False,
        False, False, False, False, False, False, False, False, False, False,
        False, True, False, False, False, True, True, False, True, False, False
    ]
    _lst_mechanism_mask: List[bool] = [
        True, True, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        False, False, True, True, True, False, False, False, False, False,
        False, False, False, False, False, True, True, True, False, False,
        True, True, False, False
    ]
    _lst_cause_mask: List[bool] = [
        True, True, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        False, False, True, True, True, False, False, False, False, False,
        False, False, False, False, False, True, True, True, False, False,
        False, True, False, False
    ]
    _lst_control_mask: List[bool] = [
        True, True, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        True, False, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        False, True, False, False
    ]
    _lst_action_mask: List[bool] = [
        True, True, False, False, False, False, False, False, False, False,
        False, False, False, False, False, False, False, False, False, False,
        False, False, False, False, False, True, True, True, True, True, True,
        True, True, True, False, False, False, False, False, False, False,
        True, False, False
    ]
    _lst_labels: List[str] = ["", "", _("Item Criticality:")]

    # Define private class scalar attributes.
    _pixbuf: bool = True

    def __init__(self,
                 configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager,
                 module: str = 'fmea') -> None:
        """
        Initialize the Work View for the FMEA.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration: :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger, module)

        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False)

        # Initialize private dictionary attributes.
        self._dic_mission_phases: Dict[str, List[str]] = {"": [""]}

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
        self._item_hazard_rate: float = 0.0

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

        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_parent, 'selected_hardware')
        pub.subscribe(self._do_clear_page, 'request_clear_workviews')
        pub.subscribe(self._do_load_missions,
                      'succeed_get_usage_profile_attributes')
        pub.subscribe(self._do_load_tree, 'succeed_retrieve_hardware_fmea')
        pub.subscribe(self._do_load_tree, 'succeed_calculate_rpn')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_action')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_cause')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_control')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_mechanism')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_insert_mode')
        pub.subscribe(self._on_delete_insert_fmea, 'succeed_delete_fmea')
        pub.subscribe(self._on_get_hardware_attributes,
                      'succeed_get_all_hardware_attributes')
        pub.subscribe(self._do_update_item_criticality,
                      'succeed_calculate_fmea_criticality')

    def __do_load_action_category(self) -> None:
        """
        Load the action category Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_cell_model(self._lst_col_order[25])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_CATEGORY:
            _model.append([
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_CATEGORY[_item][1]
            ])

    def __do_load_control_type(self) -> None:
        """
        Load the control type Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_cell_model(self._lst_col_order[20])
        for _item in RAMSTK_CONTROL_TYPES:
            _model.append([_item])

    def __do_load_failure_probability(self) -> None:
        """
        Load the failure probability Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_cell_model(self._lst_col_order[14])
        for _item in RAMSTK_FAILURE_PROBABILITY:
            _model.append([_item[0]])

    def __do_load_rpn_detection(self) -> None:
        """
        Load the RPN detection Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _detection = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION

        for _position in [23, 36]:
            _model = self.treeview.get_cell_model(
                self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(_detection):
                _model.append([_detection[_item]['name']])

    def __do_load_rpn_occurrence(self) -> None:
        """
        Load the RPN occurrence Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _occurrence = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE

        for _position in [22, 35]:
            _model = self.treeview.get_cell_model(
                self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(_occurrence):
                _model.append([_occurrence[_item]['name']])

    def __do_load_rpn_severity(self) -> None:
        """
        Load the RPN severity Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _severity = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY

        for _position in [21, 34]:
            _model = self.treeview.get_cell_model(
                self._lst_col_order[_position])
            _model.append("")
            for _item in sorted(_severity):
                _model.append([_severity[_item]['name']])

    def __do_load_severity_class(self) -> None:
        """
        Load the severity classification Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_cell_model(self._lst_col_order[12])
        for _item in RAMSTK_CRITICALITY:
            _model.append([_item[0]])

    def __do_load_status(self) -> None:
        """
        Load the action status Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_cell_model(self._lst_col_order[28])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_STATUS:
            _model.append([
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_STATUS[_item][0]
            ])

    def __do_load_users(self) -> None:
        """
        Load the RAMSTK users Gtk.CellRendererCombo().

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_cell_model(self._lst_col_order[26])
        for _item in self.RAMSTK_USER_CONFIGURATION.RAMSTK_USERS:
            _user = (self.RAMSTK_USER_CONFIGURATION.RAMSTK_USERS[_item][0]
                     + ", "
                     + self.RAMSTK_USER_CONFIGURATION.RAMSTK_USERS[_item][1])
            _model.append([_user])

    def __load_combobox(self) -> None:
        """
        Load the Gtk.CellRendererCombo()s.

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

    def __make_ui(self) -> None:
        """
        Make the FMEA Work View page.

        :return: None
        :rtype: None
        """
        # This page has the following layout:
        #
        # +-----+-----+---------------------------------+
        # |  B  |  W  |                                 |
        # |  U  |  I  |                                 |
        # |  T  |  D  |                                 |
        # |  T  |  G  |          SPREAD SHEET           |
        # |  O  |  E  |                                 |
        # |  N  |  T  |                                 |
        # |  S  |  S  |                                 |
        # +-----+-----+---------------------------------+
        #                                    buttons -----+--> self
        #                                                 |
        #  RAMSTKFixed ---+-->Gtk.VPaned -->RAMSTKFrame --+
        #                 |
        #  RAMSTKFrame ---+
        # Make the buttons.
        super().make_toolbuttons(
            icons=["insert_sibling", "insert_child", "remove", "calculate"],
            tooltips=[
                _("Add a new (D)FME(C)A entity at the same level as the "
                  "currently selected entity."),
                _("Add a new (D)FME(C)A entity one level below the currently "
                  "selected entity."),
                _("Remove the selected entity from the (D)FME(C)A."),
                _("Calculate the Task 102 criticality and/or risk priority "
                  "number (RPN).")
            ],
            callbacks=[
                self._do_request_insert_sibling, self._do_request_insert_child,
                self._do_request_delete, self._do_request_calculate
            ])
        super().make_ui_with_treeview(title=[
            "",
            _("(Design) Failure Mode, Effects, (and Criticality) Analysis "
              "[(D)FME(C)A]")
        ])

        # Move the item criticality RAMSTKTextView() below it's label.
        _fixed = self.get_children()[1].get_children()[0].get_child()
        _label = _fixed.get_children()[-1]
        _x_pos = _fixed.child_get_property(_label, 'x')
        _y_pos = _fixed.child_get_property(_label, 'y') + 25
        _fixed.put(self.txtItemCriticality.scrollwindow, _x_pos, _y_pos)

        # Set the tab label.
        _label = RAMSTKLabel(_("FMEA"))
        _label.do_set_properties(
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_("Displays failure mode and effects analysis (FMEA) "
                      "information for the selected Hardware"))
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self) -> None:
        """
        Set the callback methods and functions for the FMEA widgets.

        :return: None
        :rtype: None
        """
        self.txtItemCriticality.dic_handler_id['changed'] = 0

        self._lst_handler_id.append(
            self.treeview.connect("button_press_event", self._on_button_press))

        # CellRendererToggle columns.
        for _column in [30, 32, 38, 39, 40]:
            _cell = self.treeview.get_column(
                self._lst_col_order[_column]).get_cells()

            _cell[0].connect('toggled', self._on_cell_toggled, _column)

        # CellRendererCombo and CellRendererText columns.
        for _column in [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
                19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 31, 33, 34, 35, 36,
                37, 41
        ]:
            _cell = self.treeview.get_column(
                self._lst_col_order[_column]).get_cells()

            _cell[0].connect('edited', self._on_cell_edit, _column)

    def __set_properties(self) -> None:
        """
        Set the properties of the Hardware (D)FME(C)A RAMSTK widgets.

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

        # ----- TREEVIEWS
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _("Displays the (Design) Failure Mode and Effects "
              "(and Criticality) Analysis [(D)FME(C)A] for the "
              "currently selected Hardware item."))

    def _do_clear_page(self) -> None:
        """
        Clear the contents of the FMEA.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _model.clear()

    def _do_load_action(self, node: treelib.Node,
                        row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load an action record into the RAMSTKTreeView().

        :param node: the treelib Node() with the action data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the action to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with action data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons["action"], 22, 22)

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
            0, 0, "", _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("FMEA action {0:s} was missing it's data "
                           "package.").format(str(_entity.action_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for FMEA action ID {0:s} is the wrong type for one or "
                "more columns.".format(str(_entity.action_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for FMEA action "
                          "ID {0:s}.".format(str(_entity.action_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_cause(self, node: treelib.Node,
                       row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure cause record into the RAMSTKTreeView().

        :param node: the treelib Node() with the cause data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the cause to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with cause data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        (_occurrence, _detection, _occurrence_new,
         _detection_new) = self._get_rpn_names(_entity)

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons["cause"], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", "", "", "", "", "",
            "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, "", "",
            _occurrence, _detection, _entity.rpn, "", "", "", "", "", 0, "", 0,
            "", "", _occurrence_new, _detection_new, _entity.rpn_new, 0, 0, 0,
            "", _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Failure cause {0:s} was missing it's data "
                           "package.").format(str(_entity.cause_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for failure cause ID {0:s} is the wrong type for one or "
                "more columns.".format(str(_entity.cause_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for failure "
                          "cause ID {0:s}.".format(str(_entity.cause_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_control(self, node: treelib.Node,
                         row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a control record into the RAMSTKTreeView().

        :param node: the treelib Node() with the control data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the control to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with control data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons["control"], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", "", "", "", "", "",
            "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, _entity.type_id,
            "", "", "", 0, "", "", "", "", "", 0, "", 0, "", "", "", "", 0, 0,
            0, 0, "", _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("FMEA control {0:s} was missing it's data "
                           "package.").format(str(_entity.control_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for FMEA control ID {0:s} is the wrong type for one or "
                "more columns.".format(str(_entity.control_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for FMEA "
                          "control ID {0:s}.".format(str(_entity.control_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_mechanism(self, node: treelib.Node,
                           row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mechanism record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mechanism data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mechanism to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mechanism data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        (_occurrence, _detection, _occurrence_new,
         _detection_new) = self._get_rpn_names(_entity)

        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self._dic_icons["mechanism"], 22, 22)

        _attributes = [
            node.identifier, _entity.description, "", "", "", "", "", "", "",
            "", "", "", "", "", "", 0.0, 0.0, 0.0, 0.0, 0.0, "", "",
            _occurrence, _detection, _entity.rpn, "", "", "", "", "", 0, "", 0,
            "", "", _occurrence_new, _detection_new, _entity.rpn_new, 0, 0,
            _entity.pof_include, "", _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Failure mechanism {0:s} was missing it's data "
                           "package.").format(str(_entity.mechanism_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = (
                "Data for failure mechanism ID {0:s} is the wrong type for "
                "one or more columns.".format(str(_entity.mechanism_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for "
                          "failure mechanism ID {0:s}.".format(
                              str(_entity.mechanism_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_missions(self, attributes: treelib.Tree) -> None:
        """
        Load the mission and mission phase dicts.

        :param attributes: the treelib Tree() containing the usage profile.
        :type attributes: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        _nid = attributes.root
        _model = self.treeview.get_cell_model(self._lst_col_order[2])

        self._lst_missions = [""]
        _model.append([""])
        for _node in attributes.children(_nid):
            _model.append([_node.tag])
            self._lst_missions.append(_node.tag)

    def _do_load_mission_phases(self, mission: str) -> None:
        """
        Load the mission phase Gtk.CellRendererCombo().

        :param str mission: the mission that was selected.
        :return: None
        :rtype: None
        """
        _model = self.treeview.get_cell_model(self._lst_col_order[3])
        _model.append([""])

        try:
            for _phase in self._dic_mission_phases[mission]:
                _model.append([_phase])
        except KeyError:
            pass

    def _do_load_mode(self, node: treelib.Node,
                      row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Load a failure mode record into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :type node: :class:`treelib.Node`
        :param row: the parent row of the mode to load into the FMEA form.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just populated with mode data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        [[__, _entity]] = node.data.items()  # pylint: disable=unused-variable

        _model = self.treeview.get_model()

        _severity = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY[
            _entity.rpn_severity]['name']
        _severity_new = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY[
            _entity.rpn_severity_new]['name']
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(self._dic_icons["mode"],
                                                       22, 22)

        self._get_mission(_entity)

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
            _entity.single_point, 0, _entity.remarks, _icon,
            str(_entity.get_attributes())
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except AttributeError:
            _debug_msg = _("Failure mode {0:s} was missing it's data "
                           "package.").format(str(_entity.mode_id))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
        except TypeError:
            _debug_msg = ("Data for failure mode ID {0:s} is the wrong "
                          "type for one or more columns.".format(
                              str(_entity.mode_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None
        except ValueError:
            _debug_msg = ("Too few fields in the data package for Mode ID "
                          "{0:s}.".format(str(_entity.mode_id)))
            self.RAMSTK_LOGGER.do_log_debug(__name__, _debug_msg)
            _new_row = None

        return _new_row

    def _do_load_row(self, node: treelib.Node,
                     row: Gtk.TreeIter) -> Gtk.TreeIter:
        """
        Determines which type of row to load and loads the data.

        :param node: the FMEA treelib Node() whose data is to be loaded.
        :type nose: :class:`treelib.Node`
        :param row: the parent row for the row to be loaded.
        :type row: :class:`Gtk.TreeIter`
        :return: _new_row; the row that was just added to the FMEA treeview.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # The root node will have no data package, so this indicates the need
        # to clear the tree in preparation for the load.
        if node.tag == 'fmea':
            self._do_clear_page()
        else:
            _method = {
                'mode': self._do_load_mode,
                'mechanism': self._do_load_mechanism,
                'cause': self._do_load_cause,
                'control': self._do_load_control,
                'action': self._do_load_action
            }[node.tag]
            # noinspection PyArgumentList
            _new_row = _method(node, row)

        return _new_row

    def _do_load_tree(self, tree: treelib.Tree,
                      row: Gtk.TreeIter = None) -> None:
        """
        Iterate through tree and load the FMEA RAMSTKTreeView().

        :param tree: the treelib.Tree() containing the data packages for the
            (D)FME(C)A.
        :type tree: :class:`treelib.Tree`
        :param row: the last row to be loaded with FMEA data.
        :type row: :class:`Gtk.TreeIter`
        :return: None
        :rtype: None
        """
        _node = tree.nodes[list(tree.nodes.keys())[0]]

        _new_row = self._do_load_row(_node, row)

        for _n in tree.children(_node.identifier):
            _child_tree = tree.subtree(_n.identifier)
            self._do_load_tree(_child_tree, row=_new_row)

        super().do_expand_tree()

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """
        Calculate the FMEA RPN or criticality.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()

        if self.chkCriticality.get_active():
            pub.sendMessage("request_calculate_criticality",
                            item_hr=self._item_hazard_rate)

        if self.chkRPN.get_active():
            pub.sendMessage("request_calculate_rpn", method='mechanism')

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """
        Request to delete the selected entity from the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 0)

        pub.sendMessage("request_delete_fmea", node_id=_node_id)

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """
        Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _parent_id = _model.get_value(_row, 0)
            _attributes = _model.get_value(_row, 43).replace("'", '"')
            _attributes = json.loads("{0}".format(_attributes))
            _level = self._get_indenture_level()
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
            _level = self._on_request_insert_control_action()

        do_request_insert(_attributes, _level, _parent_id)

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """
        Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _attributes = _model.get_value(_row, 43).replace("'", '"')
            _attributes = json.loads("{0}".format(_attributes))
            _prow = _model.iter_parent(_row)
            _parent_id = _model.get_value(_prow, 0)
            _level = self._get_indenture_level()
        except TypeError:
            _attributes = {}
            _parent_id = '0'
            _level = 'mode'

        if _level in ['control', 'action']:
            _level = self._on_request_insert_control_action()

        do_request_insert(_attributes, _level, _parent_id)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save the currently selected entity in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_fmea', node_id=self._record_id)
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        """
        Request to save all the entities in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.do_set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage('request_update_all_fmea')
        self.do_set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_set_headings(self) -> List[bool]:
        """
        Set the heading text for the FMEA columns.

        :return: _set_visible; a list of True/False for the columns to be
            set visible.
        :rtype: list
        """
        _headings = {
            'mode': [_("Mode ID"),
                     _("Failure\nMode"), self._lst_mode_mask],
            'mechanism': [
                _("Mechanism ID"),
                _("Failure\nMechanism"), self._lst_mechanism_mask
            ],
            'cause':
            [_("Cause ID"),
             _("Failure\nCause"), self._lst_cause_mask],
            'control':
            [_("Control ID"),
             _("Existing\nControl"), self._lst_control_mask],
            'action':
            [_("Action ID"),
             _("Recommended\nAction"), self._lst_action_mask]
        }

        _level = self._get_indenture_level()

        self.treeview.headings[self._lst_col_order[0]] = _headings[_level][0]
        self.treeview.headings[self._lst_col_order[1]] = _headings[_level][1]

        return self._do_set_visible_columns(_headings[_level][2])

    def _do_set_parent(self, attributes: Dict[str, Any]) -> None:
        """
        Sets the parent (hardware) ID whenever a new hardware item is selected.

        :param dict attributes: the attributes of the newly selected hardware
            item.
        :return: None
        :rtype: None
        """
        self._parent_id = attributes['hardware_id']

    def _do_set_visible_columns(self, mask: List[bool]) -> List[bool]:
        """
        Set the list of True/False for the visible FMEA columns.

        :param list mask: the list of True/False mask for the type of FMEA
            object selected.
        :return: _set_visible; a list of True/False for the columns to be
            set visible.
        :rtype: list
        """
        return self.treeview.visible and mask

    def _do_update_item_criticality(self, item_criticality: str) -> None:
        """
        Update the item criticality RAMSTKTextView() with the results.

        :param dict item_criticality: the item criticality for the selected
            hardware item.
        :return: None
        :rtype: None
        """
        _item_criticality = ""
        for _key, _value in item_criticality.items():
            _item_criticality = _item_criticality + _key + ": " + str(
                _value) + "\n"

        self.txtItemCriticality.do_update(_item_criticality, 0, 'edited')

    def _get_indenture_level(self) -> str:
        """
        Determine the FMEA indenture level based on the record ID.

        :return: _level; the level in the FMEA that is currently selected.
        :rtype: str
        """
        _level = ''

        if self._record_id.count(".") == 0:
            _level = 'mode'
        elif self._record_id.count(".") == 1:
            _level = 'mechanism'
        elif self._record_id.count(".") == 2:
            _level = 'cause'
        elif self._record_id.count(".") == 4 and self._record_id[-1] == "c":
            _level = 'control'
        elif self._record_id.count(".") == 4 and self._record_id[-1] == "a":
            _level = 'action'

        return _level

    def _get_mission(self, entity: object) -> None:
        """
        Retrieve the mission information.

        :param entity: the FMEA entity to get the mission information.
        :return: None
        :rtype: None
        """
        try:
            self._lst_fmea_data[2] = self._dic_missions[entity.mission]
        except (AttributeError, KeyError):
            self._lst_fmea_data[2] = ""

        try:
            self._lst_fmea_data[3] = self._dic_mission_phases[
                entity.mission_phase]
        except (AttributeError, KeyError):
            self._lst_fmea_data[3] = ""

    def _get_rpn_names(self, entity: object) -> Tuple[str, str, str, str]:
        """
        Retrieve the RPN category for the selected mechanism or cause.

        :param entity: the RAMSTKMechanism or RAMSTKCause object to be read.
        :type entity: :class:`ramstk.models.programdb.RAMSTKMechanism` or
            :class:`ramstk.models.programdb.RAMSTKCause`
        :return: (_occurrence, _detection, _occurrence_new, _detection_new)
        :rtype: tuple
        """
        _occurrence = str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE[
            entity.rpn_occurrence]['name'])
        _detection = str(self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION[
            entity.rpn_detection]['name'])
        _occurrence_new = str(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE[
                entity.rpn_occurrence_new]['name'])
        _detection_new = str(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION[
                entity.rpn_detection_new]['name'])

        return (_occurrence, _detection, _occurrence_new, _detection_new)

    def _get_rpn_values(self, position: int, name: str) -> int:
        """
        Retrieve the RPN value for the selected SOD description.

        :param str name: the noun name in the severity, detection,
            or occurrence list.
        :return: _value
        :rtype: int
        """
        _rpn = {}
        _value = 0

        if position in [21, 34]:
            _rpn = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY
        elif position in [22, 35]:
            _rpn = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE
        elif position in [23, 36]:
            _rpn = self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION

        for _item in _rpn.items():
            if _item[1]['name'] == name:
                _value = int(_item[1]['value'])

        return _value

    def _on_button_press(self, treeview: RAMSTKTreeView,
                         event: Gdk.Event) -> None:
        """
        Handle mouse clicks on the FMEA Work View RAMSTKTreeView().

        :param treeview: the FMEA TreeView RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.TreeView.RAMSTKTreeView`.
        :param event: the Gdk.Event() that called this method (the
                      important attribute is which mouse button was clicked).

                      * 1 = left
                      * 2 = scrollwheel
                      * 3 = right
                      * 4 = forward
                      * 5 = backwards
                      * 8 =
                      * 9 =

        :type event: :class:`Gdk.Event`.
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[1])

        # The cursor-changed signal will call the _on_change_row.  If
        # _on_change_row is called from here, it gets called twice.  Once on
        # the currently selected row and once on the newly selected row.  Thus,
        # we don't need (or want) to respond to left button clicks.

        if event.button == 3:
            _icons = [
                "insert_sibling", "insert_child", "remove", "calculate", "save"
            ]
            _labels = [
                _("Insert Sibling"),
                _("Insert Child"),
                _("Remove"),
                _("Calculate"),
                _("Save")
            ]
            _callbacks = [
                self._do_request_insert_sibling, self._do_request_insert_child,
                self._do_request_delete, self._do_request_calculate,
                self._do_request_update_all
            ]
            RAMSTKWorkView.on_button_press(self,
                                           event,
                                           icons=_icons,
                                           labels=_labels,
                                           callbacks=_callbacks)

        treeview.handler_unblock(self._lst_handler_id[1])

    def _on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: str,
                      position: int) -> None:
        """
        Handle edits of the FMEA Work View RAMSTKTreeview().

        :param Gtk.CellRenderer cell: the Gtk.CellRenderer() that was edited.
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
            Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        self.treeview.do_edit_cell(cell, path, new_text, position)

        if position in [21, 22, 23, 34, 35, 36]:
            new_text = self._get_rpn_values(self._lst_col_order[position],
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

    # pylint: disable=unused-argument
    def _on_cell_toggled(self, cell: Gtk.CellRenderer, path: str,
                         position: int) -> None:
        """
        Handle edits of the FMEA Work View RAMSTKTreeview() toggle cells.

        :param Gtk.CellRenderer cell: the Gtk.CellRenderer() that was toggled.
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was toggled.
        :param int position: the column position of the toggled
            Gtk.CellRenderer().
        :return: None
        :rtype: None
        """
        _new_text = boolean_to_integer(cell.get_active())

        try:
            _key = self._dic_column_keys[self._lst_col_order[position]]
        except (IndexError, KeyError):
            _key = ''

        pub.sendMessage('wvw_editing_fmea',
                        node_id=[self._record_id, -1],
                        package={_key: _new_text})

    # pylint: disable=unused-argument
    def _on_delete_insert_fmea(self, node_id: int, tree: treelib.Tree) -> None:
        """
        Update FMEA worksheet whenever an element is inserted or deleted.

        :param int node_id: the ID of the inserted/deleted FMEA element.
        :param tree: the treelib Tree() containing the FMEA module's data.
        :type tree: :class:`treelib.Tree`
        :return: None
        :rtype: None
        """
        self._do_load_tree(tree)

    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """

        :param attributes:
        :return:
        """
        self._item_hazard_rate = attributes['hazard_rate_active']

    def _on_request_insert_control_action(self) -> str:
        """
        Raise dialog to select whether to add a control or action.

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

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """
        Handle events for the FMEA Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param treeview: the FMEA RAMSTKTreeView().
        :type treeview: :class:`ramstk.views.gtk3.widgets.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        selection.handler_block(self._lst_handler_id[0])

        _model, _row = selection.get_selected()
        try:
            self._record_id = _model.get_value(_row, 0)
            _mission = _model.get_value(_row, 2)
        except TypeError:
            self._record_id = '0'
            _mission = ""

        self._do_load_mission_phases(_mission)
        _set_visible = self._do_set_headings()

        _columns = self.treeview.get_columns()
        i = 0
        for _heading in self.treeview.headings:
            _label = RAMSTKLabel(_heading)
            _label.do_set_properties(height=-1,
                                     justify=Gtk.Justification.CENTER,
                                     wrap=True)
            _label.show_all()
            _columns[i].set_widget(_label)
            _columns[i].set_visible(_set_visible[self._lst_col_order[i]])

            i += 1

        selection.handler_unblock(self._lst_handler_id[0])
