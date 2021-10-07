# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.fmea.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 FMEA Views."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTK_CONTROL_TYPES,
    RAMSTK_CRITICALITY,
    RAMSTK_FAILURE_PROBABILITY,
    RAMSTKUserConfiguration,
)
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.assistants import AddControlAction
from ramstk.views.gtk3.widgets import RAMSTKMessageDialog, RAMSTKPanel, RAMSTKWorkView

# RAMSTK Local Imports
from . import FMEAMethodPanel, FMEATreePanel


def do_request_insert(level: str, parent_id: str) -> None:
    """Send the correct request for the FMEA item to insert.

    :param level: the indenture level in the FMEA of the new element to
        insert.
    :param parent_id: the node ID in the FMEA treelib Tree() of the
        parent element.
    :return: None
    :rtype: None
    """
    if level == "mode":
        pub.sendMessage("request_insert_fmea_mode")
    elif level == "mechanism":
        pub.sendMessage("request_insert_fmea_mechanism", mode_id=str(parent_id))
    elif level == "cause":
        pub.sendMessage("request_insert_fmea_cause", parent_id=str(parent_id))
    elif level in ["control", "action"]:
        pub.sendMessage(f"request_insert_fmea_{level}", parent_id=str(parent_id))


class FMEAWorkView(RAMSTKWorkView):
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
    _module: str = "fmea"
    _pixbuf: bool = True
    _tablabel: str = _("FMEA")
    _tabtooltip: str = _(
        "Displays failure mode and effects analysis (FMEA) information for the "
        "selected Hardware item."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Work View for the FMEA.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_insert_sibling)
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, self._do_request_delete)
        self._lst_callbacks.insert(3, self._do_request_calculate)
        self._lst_icons.insert(0, "insert_sibling")
        self._lst_icons.insert(1, "insert_child")
        self._lst_icons.insert(2, "remove")
        self._lst_icons.insert(3, "calculate")
        self._lst_mnu_labels.insert(0, _("Add Sibling"))
        self._lst_mnu_labels.insert(1, _("Add Child"))
        self._lst_mnu_labels.insert(2, _("Delete Selected"))
        self._lst_mnu_labels.insert(3, _("Calculate FMEA"))
        self._lst_tooltips: List[str] = [
            _(
                "Add a new (D)FME(C)A entity at the same level as the "
                "currently selected entity."
            ),
            _(
                "Add a new (D)FME(C)A entity one level below the currently "
                "selected entity."
            ),
            _("Delete the selected entity from the (D)FME(C)A."),
            _(
                "Calculate the Task 102 criticality and/or risk priority "
                "number (RPN)."
            ),
            _("Save changes to the selected entity in the (D)FME(C)A."),
            _("Save changes to all entities in the (D)FME(C)A."),
        ]

        # Initialize private scalar attributes.
        self._item_hazard_rate: float = 0.0

        self._pnlMethods: RAMSTKPanel = FMEAMethodPanel()
        self._pnlPanel: RAMSTKPanel = FMEATreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_fmea")
        pub.subscribe(
            self._on_get_hardware_attributes, "succeed_get_all_hardware_attributes"
        )

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Calculate the FMEA RPN or criticality.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        if self._pnlMethods.chkCriticality.get_active():
            pub.sendMessage(
                "request_calculate_criticality", item_hr=self._item_hazard_rate
            )

        if self._pnlMethods.chkRPN.get_active():
            pub.sendMessage("request_calculate_rpn", method="mechanism")

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete the selected entity from the FMEA.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent()
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected()
        _node_id = _model.get_value(_row, 0)

        _prompt = _(
            "You are about to delete {1} item {0} and all "
            "data associated with it.  Is this really what "
            "you want to do?"
        ).format(_node_id, self._module.title())
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type("question")

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                "request_delete_fmea",
                node_id=_node_id,
            )

        _dialog.do_destroy()

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected()
        try:
            _parent_id = _model.get_value(_row, 0)
            _level = {
                1: "mechanism",
                2: "cause",
                3: "control_action",
            }[len(str(_parent_id).split("."))]
        except TypeError:
            _parent_id = "0"
            _level = "mechanism"

        if _level == "control_action":
            _level = self.__on_request_insert_control_action()

        super().do_set_cursor_busy()

        # noinspection PyArgumentList
        do_request_insert(_level, _parent_id)

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        # Try to get the information needed to add a new entity at the correct
        # location in the FMEA.  If there is nothing in the FMEA, by default
        # add a failure Mode.
        _model, _row = self._pnlPanel.tvwTreeView.get_selection().get_selected()
        try:
            _parent_id = _model.get_value(_model.iter_parent(_row), 0)
            _level = {
                0: "mode",
                1: "mechanism",
                2: "cause",
                3: "control_action",
            }[len(str(_parent_id).split("."))]
        except TypeError:
            _parent_id = "0"
            _level = "mode"

        if _level == "control_action":
            _level = self.__on_request_insert_control_action()

        super().do_set_cursor_busy()
        # noinspection PyArgumentList
        do_request_insert(_level, _parent_id)

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the record and revision ID when a hardware item is selected.

        :param attributes: the hazard dict for the selected hardware ID.
        :return: None
        :rtype: None
        """
        self._record_id = attributes["node_id"]

    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the hardware item hazard rate.

        :param attributes:
        :return:
        """
        self._item_hazard_rate = attributes["hazard_rate_active"]

    def __do_load_action_combos(self):
        """Load the Gtk.CellRendererCombo()s associated with FMEA actions.

        :return: None
        :rtype: None
        """
        self._pnlPanel.lst_action_category = [
            x[1][1]
            for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_CATEGORY.items()
        ]
        self._pnlPanel.lst_action_status = [
            x[1][0] for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_ACTION_STATUS.items()
        ]
        self._pnlPanel.lst_users = [
            x[1][0] + ", " + x[1][1]
            for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_USERS.items()
        ]
        self._pnlPanel.lst_control_types = RAMSTK_CONTROL_TYPES

    def __do_load_rpn_combos(self):
        """Load the Gtk.CellRendererCombo()s associated with RPNs.

        :return: None
        :rtype: None
        """
        self._pnlPanel.lst_rpn_detection = [
            x[1]["name"]
            for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_DETECTION.items()
        ]
        self._pnlPanel.lst_rpn_detection.insert(0, "")
        self._pnlPanel.lst_rpn_occurrence = [
            x[1]["name"]
            for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_OCCURRENCE.items()
        ]
        self._pnlPanel.lst_rpn_occurrence.insert(0, "")
        self._pnlPanel.lst_rpn_severity = [
            x[1]["name"]
            for x in self.RAMSTK_USER_CONFIGURATION.RAMSTK_RPN_SEVERITY.items()
        ]
        self._pnlPanel.lst_rpn_severity.insert(0, "")

    def __do_load_severity_combos(self):
        """Load the Gtk.CellRendererCombo()s associated with CA risk.

        :return: None
        :rtype: None
        """
        self._pnlPanel.lst_mode_probability = [x[0] for x in RAMSTK_FAILURE_PROBABILITY]
        self._pnlPanel.lst_severity_class = [x[0] for x in RAMSTK_CRITICALITY]

    def __make_ui(self) -> None:
        """Build the user interface for the FMEA tab.

        :return: None
        :rtype: None
        """
        _hpaned: Gtk.HPaned = super().do_make_layout_lr()

        self._pnlPanel.dic_icons = self._dic_icons

        super().do_embed_treeview_panel()
        self.__do_load_action_combos()
        self.__do_load_rpn_combos()
        self.__do_load_severity_combos()
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
            parent=self.get_parent().get_parent().get_parent().get_parent()
        )

        if _dialog.do_run() == Gtk.ResponseType.OK:
            if _dialog.rdoControl.get_active():
                _level = "control"
            elif _dialog.rdoAction.get_active():
                _level = "action"

        _dialog.do_destroy()

        return _level
