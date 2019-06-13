# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.fmea.FMEA.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK base FME(C)A Work View."""

# Third Party Imports
from pubsub import pub
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.gui.gtk.assistants import AddControlAction
from ramstk.gui.gtk.ramstk import (
    RAMSTKLabel, RAMSTKMessageDialog, RAMSTKTreeView,
)
from ramstk.gui.gtk.ramstk.Widget import Gdk, GdkPixbuf, Gtk, _
from ramstk.gui.gtk.workviews.WorkView import RAMSTKWorkView


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

    # Define private list attributes.
    _lst_control_type = [_("Prevention"), _("Detection"),]
    _lst_fmea_data = [
        0,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        "",
        "",
        "",
        "",
        0,
        "",
        "",
        "",
        "",
        "",
        0,
        "",
        0,
        "",
        "",
        "",
        "",
        0,
        0,
        0,
        0,
        "",
        None,
        "",
    ]

    def __init__(self, configuration, **kwargs):
        """
        Initialize the Work View for the FMEA.

        :param configuration: the RAMSTK configuration instance.
        :type configuration: :class:`ramstk.RAMSTK.Configuration`
        """
        _module = kwargs["module"]
        RAMSTKWorkView.__init__(self, configuration, module=_module)

        # Initialize private dictionary attributes.
        self._dic_icons["mode"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/mode.png"
        )
        self._dic_icons["mechanism"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/mechanism.png"
        )
        self._dic_icons["cause"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/cause.png"
        )
        self._dic_icons["control"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/control.png"
        )
        self._dic_icons["action"] = (
            self.RAMSTK_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/action.png"
        )

        self._dic_missions = {}
        self._dic_mission_phases = {"": []}

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        if _module == "FFMEA":
            self._functional = True
        else:
            self._functional = False
        self._item_hazard_rate = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        _fmt_file = (
            self.RAMSTK_CONFIGURATION.RAMSTK_CONF_DIR + "/layouts/" +
            self.RAMSTK_CONFIGURATION.RAMSTK_FORMAT_FILE["fmea"]
        )
        _fmt_path = "/root/tree[@name='FMEA']/column"
        self.treeview = RAMSTKTreeView(
            _fmt_path,
            0,
            _fmt_file,
            "#FFFFFF",
            "#000000",
            pixbuf=True,
            indexed=True,
        )
        self._lst_col_order = self.treeview.order

        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_clear_page, "closed_program")

    def __load_combobox(self):
        """
        Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        # Load the severity classes into the Gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[12])
        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_SEVERITY:
            _model.append(
                (self.RAMSTK_CONFIGURATION.RAMSTK_SEVERITY[_item][1], ), )

        # Load the users into the Gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[26])
        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_USERS:
            _user = (
                self.RAMSTK_CONFIGURATION.RAMSTK_USERS[_item][0] + ", " +
                self.RAMSTK_CONFIGURATION.RAMSTK_USERS[_item][1]
            )
            _model.append((_user, ))

        # Load the status values into the Gtk.CellRendererCombo()
        _model = self._get_cell_model(self._lst_col_order[28])
        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_ACTION_STATUS:
            _model.append(
                (self.RAMSTK_CONFIGURATION.RAMSTK_ACTION_STATUS[_item][0], ), )

        # Load the RPN severity classes into the Gtk.CellRendererCombo().
        for _position in [21, 34]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append(("", ))
            for _item in sorted(self.RAMSTK_CONFIGURATION.RAMSTK_RPN_SEVERITY):
                _model.append((
                    self.RAMSTK_CONFIGURATION.RAMSTK_RPN_SEVERITY[_item][1], ))

        # Load the RPN occurrence classes into the Gtk.CellRendererCombo().
        for _position in [22, 35]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append(("", ))
            for _item in sorted(
                    self.RAMSTK_CONFIGURATION.RAMSTK_RPN_OCCURRENCE, ):
                _model.append(
                    (
                        self.RAMSTK_CONFIGURATION.RAMSTK_RPN_OCCURRENCE[_item][1],
                    ), )

        # Load the RPN detection classes into the Gtk.CellRendererCombo().
        for _position in [23, 36]:
            _model = self._get_cell_model(self._lst_col_order[_position])
            _model.append(("", ))
            for _item in sorted(
                    self.RAMSTK_CONFIGURATION.RAMSTK_RPN_DETECTION, ):
                _model.append(
                    (
                        self.RAMSTK_CONFIGURATION.RAMSTK_RPN_DETECTION[_item][1],
                    ), )

        # Load the failure probabilities into the Gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[14])
        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_FAILURE_PROBABILITY:
            _model.append((_item[0], ))

        # Load the control type Gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[20])
        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_CONTROL_TYPES:
            _model.append((_item, ))

        # Load the action category Gtk.CellRendererCombo().
        _model = self._get_cell_model(self._lst_col_order[25])
        for _item in self.RAMSTK_CONFIGURATION.RAMSTK_ACTION_CATEGORY:
            _model.append(
                (
                    self.RAMSTK_CONFIGURATION.RAMSTK_ACTION_CATEGORY[_item][1],
                ), )

    def __make_ui(self):
        """
        Make the FMEA Work View page.

        :return: None
        :rtype: None
        """
        # Hide the columns that are only associated with Hardware (D)FME(C)A if
        # this is a Functional FMEA.
        if self._functional:
            _model = self.treeview.get_model()
            _columns = self.treeview.get_columns()

            for _column in [
                    2,
                    3,
                    7,
                    8,
                    9,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    21,
                    22,
                    23,
                    24,
                    34,
                    35,
                    36,
                    37,
                    38,
                    39,
                    40,
            ]:
                _column.set_visible(False)

    def __set_callbacks(self):
        """
        Set the callback methods and functions for the common FMEA widgets.

        :return: None
        :rtype: None
        """
        self._lst_handler_id.append(
            self.treeview.connect("cursor_changed", self._do_change_row), )
        self._lst_handler_id.append(
            self.treeview.connect(
                "button_press_event",
                self._on_button_press,
            ), )

        for i in self._lst_col_order:
            _cell = self.treeview.get_column(
                self._lst_col_order[i], ).get_cells()

            if isinstance(_cell[0], Gtk.CellRendererPixbuf):
                pass
            elif isinstance(_cell[0], Gtk.CellRendererToggle):
                _cell[0].connect(
                    "toggled",
                    self.on_cell_edit,
                    None,
                    i,
                    self.treeview.get_model(),
                )
            elif isinstance(_cell[0], Gtk.CellRendererCombo):
                _cell[0].connect(
                    "edited",
                    self.on_cell_edit,
                    i,
                    self.treeview.get_model(),
                )
            else:
                _cell[0].connect(
                    "edited",
                    self.on_cell_edit,
                    i,
                    self.treeview.get_model(),
                )

    def _do_change_row(self, treeview):
        """
        Handle events for the FMEA Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param treeview: the FMEA RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            _mission = _model.get_value(_row, 2)
            _node_id = _model.get_value(_row, 43)
        except TypeError:
            _mission = ""
            _node_id = 0

        if self._get_level(_node_id) == "mode":
            self.treeview.headings[self._lst_col_order[0]] = _("Mode ID")
            self.treeview.headings[self._lst_col_order[1]] = _("Failure\nMode")
            self._do_load_mission_phases(_mission)
        elif self._get_level(_node_id) == "mechanism":
            self.treeview.headings[self._lst_col_order[0]] = _("Mechanism ID")
            self.treeview.headings[self._lst_col_order[1]] = _("Failure\nMechanism")
        elif self._get_level(_node_id) == "cause":
            self.treeview.headings[self._lst_col_order[0]] = _("Cause ID")
            self.treeview.headings[self._lst_col_order[1]] = _("Failure\nCause")
        elif self._get_level(_node_id) == "control":
            self.treeview.headings[self._lst_col_order[0]] = _("Control ID")
            self.treeview.headings[self._lst_col_order[1]] = _("Existing\nControl")
        elif self._get_level(_node_id) == "action":
            self.treeview.headings[self._lst_col_order[0]] = _("Mechanism ID")
            self.treeview.headings[self._lst_col_order[1]] = _("Recommended\nAction")

        _columns = self.treeview.get_columns()

        i = 0
        for _heading in self.treeview.headings:
            _label = RAMSTKLabel(
                _heading,
                height=-1,
                justify=Gtk.Justification.CENTER,
                wrap=True,
            )
            _label.show_all()
            _columns[i].set_widget(_label)

            if _heading == "":
                _columns[i].set_visible(False)
            else:
                _columns[i].set_visible(True)

            i += 1

        treeview.handler_unblock(self._lst_handler_id[0])

    def _do_refresh_view(self, model, __path, row):
        """
        Refresh the FMEA Work View after a successful calculation.

        :return: None
        :rtype: None
        """
        #if row is not None:
        #    _node_id = model.get_value(row, 43)

        #    _level = self._get_level(_node_id)
        #    _node = self._dtc_data_controller.request_do_select(_node_id)

        #    if _level == "mode":
        #        model.set_value(
        #            row,
        #            self._lst_col_order[17],
        #            _node.mode_hazard_rate,
        #        )
        #        model.set_value(
        #            row,
        #            self._lst_col_order[19],
        #            _node.mode_criticality,
        #        )
        #    elif _level in ["mechanism", "cause"]:
        #        model.set_value(row, self._lst_col_order[24], _node.rpn)
        #        model.set_value(row, self._lst_col_order[37], _node.rpn_new)
        #if not self._functional:
        #    _str_item_crit = ""
        #    _dic_item_crit = self._dtc_data_controller.request_item_criticality(
        #    )

        #    for _key in _dic_item_crit:
        #        _str_item_crit = _str_item_crit + _("{0:s}: {1:g}\n").format(
        #            _key,
        #            _dic_item_crit[_key],
        #        )

        #    self.txtItemCriticality.do_get_buffer().set_text(
        #        str(_str_item_crit), )

    def _do_request_calculate(self, __button):
        """
        Calculate the FMEA RPN or criticality.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _criticality = self.chkCriticality.get_active()
        _rpn = self.chkRPN.get_active()

        pub.sendMessage(
            "request_calculate_fmea",
            item_hr=self._item_hazard_rate,
            criticality=_criticality,
            rpn=_rpn,
        )

    def _do_request_delete(self, __button):
        """
        Request to delete the selected entity from the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 43)

        pub.sendMessage(
            "request_delete_fmea",
            node_id=_node_id,
        )

    def do_clear_page(self):
        """
        Clear the contents of the FMEA.

        :return: None
        :rtype: None
        """
        _model = self.treeview.get_model()
        _columns = self.treeview.get_columns()

        for _column in _columns:
            self.treeview.remove_column(_column)

        _model.clear()

    def do_load_page(self, attributes):
        """
        Iterate through tree and load the FMEA RAMSTKTreeView().

        :param dict attributes: a dict of attribute key:value pairs for the
        selected (F)(D)FME(C)A.
        :return: None
        :rtype: None
        """
        _tree = attributes["tree"]
        _row = attributes["row"]

        if self._functional:
            _type = "Functional"
            _parent_id = self._function_id
        else:
            _type = "Hardware"
            _parent_id = self._hardware_id

        _model = self.treeview.get_model()

        _node = _tree.nodes[list(SortedDict(_tree.nodes).keys())[0]]
        _entity = _node.data

        # Load the mission and RPN information if this is a Hardware (D)FME(C)A.
        if _entity is not None and not self._functional:
            try:
                self._dic_missions[_entity.mission]
            except KeyError:
                _entity.mission = ""

            try:
                self._lst_fmea_data[21] = self._get_rpn_severity(
                    _entity.rpn_severity,
                    score=False,
                )
                self._lst_fmea_data[34] = self._get_rpn_severity(
                    _entity.rpn_severity_new,
                    score=False,
                )
            except AttributeError:
                pass

            try:
                self._lst_fmea_data[22] = self._get_rpn_occurrence(
                    _entity.rpn_occurrence,
                    score=False,
                )
                self._lst_fmea_data[35] = self._get_rpn_occurrence(
                    _entity.rpn_occurrence_new,
                    score=False,
                )
            except AttributeError:
                pass

            try:
                self._lst_fmea_data[23] = self._get_rpn_detection(
                    _entity.rpn_detection,
                    score=False,
                )
                self._lst_fmea_data[36] = self._get_rpn_detection(
                    _entity.rpn_detection_new,
                    score=False,
                )
            except AttributeError:
                pass

        try:
            if _entity.is_mode:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["mode"],
                    22,
                    22,
                )
                self._lst_fmea_data[0] = _entity.mode_id
                self._lst_fmea_data[1] = _entity.description
                self._lst_fmea_data[4] = _entity.effect_local
                self._lst_fmea_data[5] = _entity.effect_next
                self._lst_fmea_data[6] = _entity.effect_end
                self._lst_fmea_data[10] = _entity.design_provisions
                self._lst_fmea_data[11] = _entity.operator_actions
                self._lst_fmea_data[12] = _entity.severity_class
                self._lst_fmea_data[41] = _entity.remarks

                if not self._functional:
                    self._lst_fmea_data[2] = _entity.mission
                    self._lst_fmea_data[3] = _entity.mission_phase
                    self._lst_fmea_data[7] = _entity.detection_method
                    self._lst_fmea_data[8] = _entity.other_indications
                    self._lst_fmea_data[9] = _entity.isolation_method
                    self._lst_fmea_data[13] = _entity.hazard_rate_source
                    self._lst_fmea_data[14] = _entity.mode_probability
                    self._lst_fmea_data[15] = _entity.effect_probability
                    self._lst_fmea_data[16] = _entity.mode_ratio
                    self._lst_fmea_data[17] = _entity.mode_hazard_rate
                    self._lst_fmea_data[18] = _entity.mode_op_time
                    self._lst_fmea_data[19] = _entity.mode_criticality
                    self._lst_fmea_data[38] = _entity.critical_item
                    self._lst_fmea_data[39] = _entity.single_point

                _row = None

            elif _entity.is_mechanism:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["mechanism"],
                    22,
                    22,
                )
                self._lst_fmea_data[0] = _entity.mechanism_id
                self._lst_fmea_data[1] = _entity.description
                self._lst_fmea_data[24] = _entity.rpn
                self._lst_fmea_data[37] = _entity.rpn_new
                self._lst_fmea_data[40] = _entity.pof_include

            elif _entity.is_cause and _row is not None:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["cause"],
                    22,
                    22,
                )
                self._lst_fmea_data[0] = _entity.cause_id
                self._lst_fmea_data[1] = _entity.description

                if not self._functional:
                    self._lst_fmea_data[24] = _entity.rpn
                    self._lst_fmea_data[37] = _entity.rpn_new

            elif _entity.is_control and _row is not None:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["control"],
                    22,
                    22,
                )
                self._lst_fmea_data[0] = _entity.control_id
                self._lst_fmea_data[1] = _entity.description
                self._lst_fmea_data[20] = _entity.type_id

            elif _entity.is_action and _row is not None:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["action"],
                    22,
                    22,
                )
                self._lst_fmea_data[0] = _entity.action_id
                self._lst_fmea_data[1] = _entity.action_recommended
                self._lst_fmea_data[25] = _entity.action_category
                self._lst_fmea_data[26] = _entity.action_owner
                self._lst_fmea_data[27] = _entity.action_due_date
                self._lst_fmea_data[28] = _entity.action_status
                self._lst_fmea_data[29] = _entity.action_taken
                self._lst_fmea_data[30] = _entity.action_approved
                self._lst_fmea_data[31] = _entity.action_approve_date
                self._lst_fmea_data[32] = _entity.action_closed
                self._lst_fmea_data[33] = _entity.action_close_date

            self._lst_fmea_data[42] = _icon
            self._lst_fmea_data[43] = _node.identifier

            try:
                _new_row = _model.append(_row, self._lst_fmea_data)
            except TypeError:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more {0:s} FMEA line items had "
                        "the wrong data type in it's data package and "
                        "is not displayed in the FMEA form.", ).format(_type),
                )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    _(
                        "RAMSTK ERROR: Data for FMEA ID {0:s} for {2:s} "
                        "ID {1:s} is the wrong type for one or more "
                        "columns.".format(
                            str(_node.identifier),
                            str(_parent_id),
                            _type,
                        ), ), )
                _new_row = None
            except ValueError:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more {0:s} FMEA line items was missing some "
                        "of it's data and is not displayed in the FMEA form.",
                    ).format(_type), )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    _(
                        "RAMSTK ERROR: Too few fields for FMEA ID {0:s} for "
                        "{2:s} ID {1:s}.".format(
                            str(_node.identifier),
                            str(_parent_id),
                            _type,
                        ), ), )
                _new_row = None

        except AttributeError:
            if _node.identifier != 0:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more {0:s} FMEA line items was "
                        "missing it's data package and is not "
                        "displayed in the FMEA form.", ).format(_type), )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    _(
                        "RAMSTK ERROR: There is no data package for FMEA "
                        "ID {0:s} for {2:s} "
                        "ID {1:s}.".format(
                            str(_node.identifier),
                            str(_parent_id),
                            _type,
                        ), ), )
            _new_row = None

        for _n in _tree.children(_node.identifier):
            _child_tree = _tree.subtree(_n.identifier)
            self.do_load_page(
                attributes={
                    "tree": _child_tree,
                    "row": _new_row,
                }, )

        _row = _model.get_iter_first()
        self.treeview.expand_all()

        RAMSTKWorkView.on_select(
            self,
            title=_("Analyzing Failure Modes for {1:s} ID {0:d}").format(
                _parent_id,
                _type,
            ),
        )

        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

    def _do_request_insert(self, **kwargs):
        """
        Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        _sibling = kwargs["sibling"]

        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self.treeview.get_selection().get_selected()
        try:
            _node_id = _model.get_value(_row, 43)
            _level = self._get_level(_node_id)
            _prow = _model.iter_parent(_row)
        except TypeError:
            _node_id = 0
            _level = "mode"
            _prow = None

        # Dict to hold the set of arguments to use for flow control.
        # Outer key is FMEA level.  Inner key determines whether sibling or
        # child is requested for insert.  Value is the entity ID, parent ID,
        # whether to raise ActionControl dialog, and if an undefined condition
        # exists (no child for control or action).
        _dic_args = {
            "mode": {
                True: [self._parent_id, _node_id, False, False],
                False: [_model.get_value(_prow, 0), _node_id, False, False],
            },
            "mechanism": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 43),
                    False,
                    False,
                ],
                False: [_model.get_value(_row, 0), _node_id, False, False],
            },
            "cause": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 43),
                    False,
                    False,
                ],
                False: [_model.get_value(_row, 0), _node_id, True, False],
            },
            "control": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 43),
                    True,
                    False,
                ],
                False: [_model.get_value(_row, 0), _node_id, True, True],
            },
            "action": {
                True: [
                    _model.get_value(_prow, 0),
                    _model.get_value(_prow, 43),
                    True,
                    False,
                ],
                False: [_model.get_value(_row, 0), _node_id, True, True],
            },
        }

        # The _entity_id is the RAMSTK Program database Hardware ID, Mode ID,
        # Mechanism ID, or Cause ID to add the new entity to.  The _parent_id
        # is the Node ID of the parent node in the treelib Tree().
        (
            _entity_id,
            _parent_id,
            _choose,
            _undefined,
        ) = _dic_args[_sibling][_level]

        if _undefined:
            _prompt = _(
                "A FMEA control or an action cannot have a child entity.", )
            _dialog = RAMSTKMessageDialog(
                _prompt,
                self._dic_icons["error"],
                "error",
            )

            if _dialog.do_run() == Gtk.ResponseType.OK:
                _dialog.do_destroy()

        if _choose:
            _dialog = AddControlAction()

            if _dialog.do_run() == Gtk.ResponseType.OK:
                _control = _dialog.rdoControl.get_active()
                _action = _dialog.rdoAction.get_active()

                if _control:
                    _level = "control"
                elif _action:
                    _level = "action"

            _dialog.do_destroy()

        if not _undefined:
            pub.sendMessage(
                "request_insert_fmea",
                entity_id=_entity_id,
                parent_id=_parent_id,
                level=_level,
            )

    def _do_request_update(self, __button):
        """
        Request to save the currently selected entity in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _model, _row = self.treeview.get_selection().get_selected()
        _node_id = _model.get_value(_row, 43)

        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage("request_update_fmea", node_id=_node_id)
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _do_request_update_all(self, __button):
        """
        Request to save all the entities in the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:`Gtk.ToolButton`.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self.set_cursor(Gdk.CursorType.WATCH)
        pub.sendMessage("request_update_all_fmea")
        self.set_cursor(Gdk.CursorType.LEFT_PTR)

    def _get_cell_model(self, column):
        """
        Retrieve the Gtk.CellRendererCombo() Gtk.TreeModel().

        :param int column: the column number to retrieve the cell from.
        :return: _model
        :rtype: :class:`Gtk.TreeModel`
        """
        _column = self.treeview.get_column(column)
        _cell = _column.get_cells()[0]
        _model = _cell.get_property("model")
        _model.clear()

        return _model

    def _on_button_press(self, treeview, event):
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
                "insert_sibling",
                "insert_child",
                "remove",
                "calculate",
                "save",
            ]
            _labels = [
                _("Insert Sibling"),
                _("Insert Child"),
                _("Remove"),
                _("Calculate"),
                _("Save"),
            ]
            _callbacks = [
                self._do_request_insert_sibling,
                self._do_request_insert_child,
                self._do_request_delete,
                self._do_request_calculate,
                self._do_request_update_all,
            ]
            RAMSTKWorkView.on_button_press(
                self,
                event,
                icons=_icons,
                labels=_labels,
                callbacks=_callbacks,
            )

        treeview.handler_unblock(self._lst_handler_id[1])

    def on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the Functional FMEA Work View RAMSTKTreeview().

        :param __cell: the Gtk.CellRenderer() that was edited.
        :type __cell: :class:`Gtk.CellRenderer`.
        :param str path: the path that was edited.
        :param str new_text: the edited text.
        :param int position: the column position in the RAMSTKTreeView() that
        is being edited.
        :param model: the Gtk.TreeModel() for the Functional FMEA
        RAMSTKTreeView().
        :type model: :class:`Gtk.TreeModel`
        :return: None
        :rtype: None
        """
        _node_id = model.get_value(model.get_iter(path), 0)
        try:
            _key = self._dic_keys[position]
        except KeyError:
            _key = ""

        if not self.treeview.do_edit_cell(
                __cell,
                path,
                new_text,
                position,
                model,
        ):

            self.do_set_cursor(Gdk.CursorType.WATCH)
            pub.sendMessage(
                'wvw_editing_fmea',
                module_id=_node_id,
                key=_key,
                value=new_text,
            )
            self.do_set_cursor(Gdk.CursorType.LEFT_PTR)
