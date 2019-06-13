# -*- coding: utf-8 -*-
#
#       ramstk.gui.gtk.workviews.fmea.DFMEA.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK DFME(C)A Work View."""

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.gui.gtk.ramstk import (
    RAMSTKCheckButton, RAMSTKFrame, RAMSTKLabel, RAMSTKTextView,
)
from ramstk.gui.gtk.ramstk.Widget import Gdk, Gtk, _

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

    # Define private dict attributes.
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

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_clear_page, "closed_program")
        pub.subscribe(self._do_load_missions, "selected_revision")
        pub.subscribe(self._do_load_missions, "lvw_editing_usage_profile")
        pub.subscribe(self.do_load_page, "retrieved_dfmeca")

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

    def __set_properties(self):
        """
        Set the properties of the Hardware (D)FME(C)A RAMSTK widgets.

        :return: None
        :rtype: None
        """
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
        self.txtItemCriticality.do_set_properties(
            editable=False,
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

    def _do_clear_page(self):
        """
        Clear the contents of the Hardware (D)FME(C)A page.

        :return: None
        :rtype: None
        """
        FMEA.do_clear_page(self)

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
