# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.fmea.DFMEA.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK DFME(C)A Work View."""

# Third Party Imports
from pubsub import pub
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import (RAMSTKCheckButton, RAMSTKFrame,
                                   RAMSTKLabel, RAMSTKTextView)
from ramstk.gui.gtk.ramstk.Widget import Gdk, GdkPixbuf, Gtk, _
from ramstk.gui.gtk.workviews.WorkView import RAMSTKWorkView

# RAMSTK Local Imports
from .FMEA import FMEA


class DFMECA(FMEA):
    """
    Display Hardware (D)FME(C)A attribute data in the Work Book.

    The WorkView displays all the attributes for the Hardware (Design) Failure
    Mode and Effects (and Criticality) Analysis [(D)FME(C)A]. The attributes of
    a (D)FME(C)A Work View are:

    :ivar int _hardware_id: the ID of the Hardware item whose (D)FME(C)A is
    being displayed.
    :ivar chkCriticality: RAMSTHCheckButton() to indicate whether or not to
    calculate the MIL-STD-1629A, Task 102 criticality.
    :type chkCriticality: :class:`ramstk.gui.gtk.ramstk.RAMSTKCheckButton`
    :ivar chkRPN: RAMSTKCheckButton() to indicate whether or not to calculate
    RPNs.
    :type chkRPN: :class:`ramstk.gui.gtk.ramstk.RAMSTKCheckButton`
    :ivar treeview: the RAMSTKTreeView() holding the (D)FME(C)A.
    :type treeview: :class:`ramstk.gui.gtk.ramstk.View.RAMSTKTreeView`
    :ivar txtItemCriticality: RAMSTKTextView() to display item criticality
    results.
    :type txtItemCriticality: :class:`ramstk.gui.gtk.ramstk.RAMSTKTextView`
    """

    def __init__(self, configuration, **kwargs):  # pylint: disable=unused-argument
        """
        Initialize the Work View for the Hardware (D)FME(C)A.

        :param configuration: the RAMSTK configuration instance.
        :type configuration: :class:`ramstk.RAMSTK.Configuration`
        """
        FMEA.__init__(self, configuration, module="DFMECA", **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hardware_id = None

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.chkCriticality = RAMSTKCheckButton(
            label=_("Calculate Criticality"), )
        self.chkRPN = RAMSTKCheckButton(label=_("Calculate RPNs"))
        self.txtItemCriticality = RAMSTKTextView(Gtk.TextBuffer())

        self.__set_properties()
        self.__make_ui()
        self.__load_combobox()
        self.__set_callbacks()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, "closed_program")
        pub.subscribe(self._do_load_missions, "selected_revision")
        pub.subscribe(self._do_load_missions, "lvw_editing_usage_profile")
        pub.subscribe(self._do_load_page, "retrieved_dfmeca")

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
        Make the Hardware (D)FME(C)A Work View page.

        :return: None
        :rtype: None
        """
        _buttonbox = FMEA._make_buttonbox(
            self,
            tooltips=[
                _(
                    "Add a new (D)FME(C)A entity at the same level as the "
                    "currently selected entity.", ),
                _(
                    "Add a new (D)FME(C)A entity one level below the currently "
                    "selected entity.", ),
                _("Remove the selected entity from the (D)FME(C)A."),
            ],
            callbacks=[
                self.do_request_insert_sibling,
                self.do_request_insert_child,
                self._do_request_delete,
            ],
            icons=["insert_sibling", "insert_child", "remove"],
        )

        self.pack_start(_buttonbox, False, True, 0)

        _vbox = Gtk.VBox()

        _fixed = Gtk.Fixed()
        _vbox.pack_start(_fixed, False, True, 0)

        _fixed.put(self.chkCriticality, 5, 5)
        _fixed.put(self.chkRPN, 5, 35)
        _fixed.put(self.txtItemCriticality.scrollwindow, 550, 5)

        _scrollwindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC,
        )
        _scrollwindow.add(self.treeview)

        _vbox.pack_end(_scrollwindow, True, True, 0)

        _frame = RAMSTKFrame(
            label=_(
            "Hardware (Design) Failure Mode, Effects, (and Criticality) "
            "Analysis [(D)FME(C)A]", ), )
        _frame.add(_vbox)

        self.pack_end(_frame, True, True, 0)

        _label = RAMSTKLabel(
            _("(D)FME(C)A"),
            height=30,
            width=-1,
            justify=Gtk.Justification.CENTER,
            tooltip=_(
                "Displays the Design Failure Mode, Effects, (and "
                "Criticality) Analysis [(D)FME(C)A] for the selected "
                "Hardware item.", ),
        )
        self.hbx_tab_label.pack_start(_label, True, True, 0)

        self.show_all()

    def __set_callbacks(self):
        """
        Set the callback methods and functions for the (D)FME(C)A widgets.

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
                    self._on_cell_edit,
                    None,
                    i,
                    self.treeview.get_model(),
                )
            elif isinstance(_cell[0], Gtk.CellRendererCombo):
                _cell[0].connect(
                    "edited",
                    self._on_cell_edit,
                    i,
                    self.treeview.get_model(),
                )
            else:
                _cell[0].connect(
                    "edited",
                    self._on_cell_edit,
                    i,
                    self.treeview.get_model(),
                )

    def __set_properties(self):
        """
        Set the properties of the Hardware (D)FME(C)A RAMSTK widgets.

        :return: None
        :rtype: None
        """
        # Set failure mode column headings.
        for _index in [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15,
                16,
                17,
                18,
                19,
                21,
                34,
                38,
                39,
                41,
        ]:
            self._dic_headings["mode"][_index] = self.treeview.headings[
                self._lst_col_order[_index]
            ]

        # Set failure mechanism column headings.
        self._dic_headings["mechanism"][0] = _("Mechanism ID")
        self._dic_headings["mechanism"][1] = _("Failure\nMechanism")
        for _index in [22, 23, 24, 35, 36, 37, 40]:
            self._dic_headings["mechanism"][_index] = self.treeview.headings[
                self._lst_col_order[_index]
            ]

        self._dic_headings["cause"][0] = _("Cause ID")
        self._dic_headings["cause"][1] = _("Failure\nCause")
        for _index in [22, 23, 24, 25, 26, 27]:
            self._dic_headings["cause"][_index] = self.treeview.headings[
                self._lst_col_order[_index]
            ]

        self._dic_headings["control"][0] = _("Control ID")
        self._dic_headings["control"][1] = _("Existing\nControl")
        self._dic_headings["control"][20] = self.treeview.headings[
            self._lst_col_order[20]
        ]

        self._dic_headings["action"][0] = _("Action ID")
        self._dic_headings["action"][1] = _("Recommended\nAction")
        for _index in [25, 26, 27, 28, 29, 30, 31, 32, 33]:
            self._dic_headings["action"][_index] = self.treeview.headings[
                self._lst_col_order[_index]
            ]

        # ----- BUTTONS
        # By default, calculate both Task 102 and RPN.
        self.chkCriticality.set_active(True)
        self.chkRPN.set_active(True)
        self.chkCriticality.do_set_properties(
            tooltip=_(
            "Select this option to calculate the (D)FME(C)A MIL-STD-1629, "
            "Task 102 criticality analysis.", ), )
        self.chkRPN.do_set_properties(
            tooltip=_(
            "Select this option to calculate the (D)FME(C)A risk priority "
            "numbers (RPN).", ), )

        # ----- ENTRIES
        self.txtItemCriticality.set_editable(False)
        self.txtItemCriticality.do_set_properties(
            height=75,
            tooltip=_(
                "Displays the MIL-SD-1629, Task 102 item criticality for the "
                "selected hardware item.", ),
        )

        _bg_color = Gdk.RGBA(red=173.0, green=216.0, blue=230.0, alpha=1.0)
        self.txtItemCriticality.override_background_color(
            Gtk.StateFlags.NORMAL,
            _bg_color,
        )
        self.txtItemCriticality.override_background_color(
            Gtk.StateFlags.ACTIVE,
            _bg_color,
        )
        self.txtItemCriticality.override_background_color(
            Gtk.StateFlags.PRELIGHT,
            _bg_color,
        )
        self.txtItemCriticality.override_background_color(
            Gtk.StateFlags.SELECTED,
            _bg_color,
        )
        self.txtItemCriticality.override_background_color(
            Gtk.StateFlags.INSENSITIVE,
            _bg_color,
        )

        # ----- TREEVIEWS
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.treeview.set_tooltip_text(
            _(
                "Displays the (Design) Failure Mode and Effects "
                "(and Criticality) Analysis [(D)FME(C)A] for the "
                "currently selected Hardware item.", ), )

    def _do_change_row(self, treeview):
        """
        Handle events for the Hardware (D)FME(C)A Work View RAMSTKTreeView().

        This method is called whenever a RAMSTKTreeView() row is activated.

        :param treeview: the Hardware (D)FME(C)A RAMSTKTreeView().
        :type treeview: :class:`ramstk.gui.gtk.ramstk.RAMSTKTreeView`
        :return: None
        :rtype: None
        """
        treeview.handler_block(self._lst_handler_id[0])

        _model, _row = treeview.get_selection().get_selected()
        try:
            _mission = _model.get_value(_row, 2)
            _node_id = _model.get_value(_row, 43)
            _headings = self._dic_headings[self._get_level(_node_id)]
        except TypeError:
            _mission = ""
            _node_id = 0
            _headings = []

        if self._get_level(_node_id) == "mode":
            self._do_load_mission_phases(_mission)

        _columns = self.treeview.get_columns()

        i = 0
        for _heading in _headings:
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

    def _do_clear_page(self):
        """
        Clear the contents of the Hardware (D)FME(C)A page.

        :return: None
        :rtype: None
        """
        FMEA._do_clear_page(self)

        self.chkCriticality.set_active(False)
        self.chkRPN.set_active(False)
        self.txtItemCriticality.do_get_buffer.set_text("")

    def _do_load_mission_phases(self, mission):
        """
        Load the mission phase Gtk.CellRendererCombo().

        :param str mission: the mission that was selected.
        :return: None
        :rtype: None
        """
        _model = self._get_cell_model(self._lst_col_order[3])
        _model.clear()
        _model.append(("", ))

        try:
            for _phase in self._dic_mission_phases[mission]:
                _model.append((_phase, ))
        except KeyError:
            pass

    def _do_load_missions(self, module_id):
        """
        Respond to `selected_revision` signal from pypubsub.

        :param int module_id: the ID of the Revision that was selected.
        :return: None
        :rtype: None
        """
        _attributes = {"revision_id": module_id}
        self.dic_controllers["profile"].request_do_select_all(_attributes)
        _tree = self.dic_controllers["profile"].request_tree()

        _missions = _tree.children(0)
        for _mission in _missions:
            self._dic_missions[
                _mission.data.description
            ] = _mission.data.mission_time
            _phases = []
            for _phase in _tree.children(_mission.identifier):
                _phases.append(_phase.data.description)
            self._dic_mission_phases[_mission.data.description] = _phases

        _model = self._get_cell_model(self._lst_col_order[2])
        _model.clear()
        _model.append(("", ))

        try:
            for _mission in self._dic_missions:
                _model.append((_mission, ))
        except KeyError:
            pass

    def _do_load_page(self, attributes):
        """
        Iterate through the tree and load the Hardware (D)FME(C)A RAMSTKTreeView().

        :param dict attributes: a dict of attribute key:value pairs for the
        selected Hardware (D)FME(C)A.
        :return: None
        :rtype: None
        """
        _tree = attributes["tree"]
        _row = attributes["row"]
        _detection = ["", ""]
        _occurrence = ["", ""]
        _severity = ["", ""]

        _data = []
        _model = self.treeview.get_model()

        _node = _tree.nodes[list(SortedDict(_tree.nodes).keys())[0]]
        _entity = _node.data
        if _entity is not None:
            try:
                _severity.append(
                    self._get_rpn_severity(
                        _entity.rpn_severity,
                        score=False,
                    ), )
                _severity.append(
                    self._get_rpn_severity(
                        _entity.rpn_severity_new,
                        score=False,
                    ), )
            except AttributeError:
                pass

            try:
                _occurrence.append(
                    self._get_rpn_occurrence(
                        _entity.rpn_occurrence,
                        score=False,
                    ), )
                _occurrence.append(
                    self._get_rpn_occurrence(
                        _entity.rpn_occurrence_new,
                        score=False,
                    ), )
            except AttributeError:
                pass

            try:
                _detection.append(
                    self._get_rpn_detection(
                        _entity.rpn_detection,
                        score=False,
                    ), )
                _detection.append(
                    self._get_rpn_detection(
                        _entity.rpn_detection_new,
                        score=False,
                    ), )
            except AttributeError:
                pass

        try:
            self._lst_fmea_data[21] = _severity[0]
            self._lst_fmea_data[22] = _occurrence[0]
            self._lst_fmea_data[23] = _detection[0]
            self._lst_fmea_data[34] = _severity[1]
            self._lst_fmea_data[35] = _occurrence[1]
            self._lst_fmea_data[36] = _detection[1]
            self._lst_fmea_data[43] = _node.identifier

            if _entity.is_mode:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["mode"],
                    22,
                    22,
                )
                try:
                    self._dic_missions[_entity.mission]
                except KeyError:
                    _entity.mission = ""

                self._lst_fmea_data[0] = _entity.mode_id
                self._lst_fmea_data[1] = _entity.description
                self._lst_fmea_data[2] = _entity.mission
                self._lst_fmea_data[3] = _entity.mission_phase
                self._lst_fmea_data[4] = _entity.effect_local
                self._lst_fmea_data[5] = _entity.effect_next
                self._lst_fmea_data[6] = _entity.effect_end
                self._lst_fmea_data[7] = _entity.detection_method
                self._lst_fmea_data[8] = _entity.other_indications
                self._lst_fmea_data[9] = _entity.isolation_method
                self._lst_fmea_data[10] = _entity.design_provisions
                self._lst_fmea_data[11] = _entity.operator_actions
                self._lst_fmea_data[12] = _entity.severity_class
                self._lst_fmea_data[13] = _entity.hazard_rate_source
                self._lst_fmea_data[14] = _entity.mode_probability
                self._lst_fmea_data[15] = _entity.effect_probability
                self._lst_fmea_data[16] = _entity.mode_ratio
                self._lst_fmea_data[17] = _entity.mode_hazard_rate
                self._lst_fmea_data[18] = _entity.mode_op_time
                self._lst_fmea_data[19] = _entity.mode_criticality
                self._lst_fmea_data[38] = _entity.critical_item
                self._lst_fmea_data[39] = _entity.single_point
                self._lst_fmea_data[41] = _entity.remarks

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

            elif _entity.is_cause:
                _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                    self._dic_icons["cause"],
                    22,
                    22,
                )
                self._lst_fmea_data[0] = _entity.cause_id
                self._lst_fmea_data[1] = _entity.description
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

            try:
                _new_row = _model.append(_row, self._lst_fmea_data)
            except TypeError:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more Hardware FMEA line items had "
                        "the wrong data type in it's data package and "
                        "is not displayed in the FMEA form.", ), )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    _(
                        "RAMSTK ERROR: Data for FMEA ID {0:s} for Hardware "
                        "ID {1:s} is the wrong type for one or more "
                        "columns.".format(
                            str(_node.identifier),
                            str(self._hardware_id),
                        ), ), )
                _new_row = None
            except ValueError:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more Hardware FMEA line items was missing some "
                        "of it's data and is not displayed in the FMEA form.",
                    ), )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    _(
                        "RAMSTK ERROR: Too few fields for FMEA ID {0:s} for "
                        "Hardware ID {1:s}.".format(
                            str(_node.identifier),
                            str(self._hardware_id),
                        ), ), )
                _new_row = None

        except AttributeError:
            if _node.identifier != 0:
                self.RAMSTK_CONFIGURATION.RAMSTK_USER_LOG.info(
                    _(
                        "One or more Hardware FMEA line items was "
                        "missing it's data package and is not "
                        "displayed in the FMEA form.", ), )
                self.RAMSTK_CONFIGURATION.RAMSTK_DEBUG_LOG.error(
                    _(
                        "RAMSTK ERROR: There is no data package for FMEA "
                        "ID {0:s} for Hardware "
                        "ID {1:s}.".format(
                            str(_node.identifier),
                            str(self._hardware_id),
                        ), ), )
            _new_row = None

        for _n in _tree.children(_node.identifier):
            _child_tree = _tree.subtree(_n.identifier)
            self._do_load_page(
                attributes={
                    "tree": _child_tree,
                    "row": _new_row,
                }, )

        _row = _model.get_iter_first()
        self.treeview.expand_all()

        RAMSTKWorkView.on_select(
            self,
            title=_("Analyzing Failure Modes for Hardware ID {0:d}").format(
                self._hardware_id, ),
        )

        if _row is not None:
            _path = _model.get_path(_row)
            _column = self.treeview.get_column(0)
            self.treeview.set_cursor(_path, None, False)
            self.treeview.row_activated(_path, _column)

    def _do_request_insert(self, **kwargs):
        """
        Request to insert a new entity to the Hardware (D)FME(C)A.

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
                True: [self._hardware_id, _node_id, False, False],
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

        FMEA._do_request_insert(
            self,
            entity_id=_entity_id,
            parent_id=_parent_id,
            level=_level,
            choose=_choose,
            undefined=_undefined,
        )

    @staticmethod
    def _get_level(node_id):
        """
        Return the level in the Hardware FMEA based on the Node ID.

        :param str node_id: the Node ID of the selected Node in the Functional
                            FMEA Tree().
        :return: _level
        :rtype: str
        """
        _level = None

        if node_id.count(".") == 1:
            _level = "mode"
        elif node_id.count(".") == 2:
            _level = "mechanism"
        elif node_id.count(".") == 3:
            _level = "cause"
        elif node_id.count(".") == 4 and node_id[-1] == "c":
            _level = "control"
        elif node_id.count(".") == 4 and node_id[-1] == "a":
            _level = "action"

        return _level

    def _get_rpn_detection(self, detection, score=True):
        """
        Retrieve the integer value of the RPN Occurence score based on name.

        :param str,int detection: the noun name given to the RPN Occurence
                                  score (score=True) or the integer value of
                                  the RPN Detection score.
        :keyword bool score: indicates whether to return the RPN Detection
                             score for passed noun name (default) or the noun
                             name of the passed RPN Occurence score.
        :return: _rpn_detection
        :rtype: int or str depending on value of keyword score.
        """
        _rpn_detection = 0

        if score:
            try:
                _rpn_detection = [
                    x[4] for x in list(
                        self.RAMSTK_CONFIGURATION.RAMSTK_RPN_DETECTION.values(
                        ), ) if x[1] == detection
                ][0]
            except IndexError:
                _rpn_detection = 0
        else:
            try:
                _rpn_detection = self.RAMSTK_CONFIGURATION.RAMSTK_RPN_DETECTION[
                    detection
                ][1]
            except (AttributeError, KeyError):
                _rpn_detection = ""

        return _rpn_detection

    def _get_rpn_occurrence(self, occurrence, score=True):
        """
        Retrieve the integer value of the RPN Occurence score based on name.

        :param str,int occurrence: the noun name given to the RPN Occurence
                                   score (score=True) or the integer value of
                                   the RPN Occurrence score.
        :keyword bool score: indicates whether to return the RPN Occurrence
                             score for passed noun name (default) or the noun
                             name of the passed RPN Occurence score.
        :return: _rpn_occurrence
        :rtype: int or str depending on value of keyword score.
        """
        _rpn_occurrence = 0

        if score:
            try:
                _rpn_occurrence = [
                    x[4] for x in list(
                        self.RAMSTK_CONFIGURATION.RAMSTK_RPN_OCCURRENCE.values(
                        ), ) if x[1] == occurrence
                ][0]
            except IndexError:
                _rpn_occurrence = 0
        else:
            try:
                _rpn_occurrence = self.RAMSTK_CONFIGURATION.RAMSTK_RPN_OCCURRENCE[
                    occurrence
                ][1]
            except (AttributeError, KeyError):
                _rpn_occurrence = ""

        return _rpn_occurrence

    def _get_rpn_severity(self, severity, score=True):
        """
        Retrieve the corresponding value of the RPN Severity score.

        :param str,int severity: the noun name given to the RPN Severity score (score=True) or the integer value of the RPN Severity score.
        :keyword bool score: indicates whether to return the RPN Severity score for passed noun name (default) or the noun name of the passed RPN Severity score.
        :return: _rpn_severity
        :rtype: int or str depending on value of keyword score.
        """
        _rpn_severity = 0

        if score:
            try:
                _rpn_severity = [
                    x[4] for x in list(
                        self.RAMSTK_CONFIGURATION.RAMSTK_RPN_SEVERITY.values(),
                    ) if x[1] == severity
                ][0]
            except IndexError:
                _rpn_severity = 0
        else:
            try:
                _rpn_severity = self.RAMSTK_CONFIGURATION.RAMSTK_RPN_SEVERITY[
                    severity
                ][1]
            except (AttributeError, KeyError):
                _rpn_severity = ""

        return _rpn_severity

    def _on_cell_edit(self, __cell, path, new_text, position, model):
        """
        Handle edits of the (D)FME(C)A RAMSTKTreeview().

        :param Gtk.CellRenderer __cell: the Gtk.CellRenderer() that was edited.
        :param str path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
                         that was edited.
        :param str new_text: the new text in the edited Gtk.CellRenderer().
        :param int position: the column position of the edited
                             Gtk.CellRenderer().
        :param Gtk.TreeModel model: the Gtk.TreeModel() the Gtk.CellRenderer()
                                    belongs to.
        :return: None
        :rtype: None
        """
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
            41: "remarks",
        }

        _node_id = model.get_value(model.get_iter(path), 0)
        try:
            _key = _dic_keys[position]
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
