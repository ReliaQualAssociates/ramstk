# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.fmea.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 FMEA Views."""

# Standard Library Imports
from typing import Any, Dict, List, Tuple

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
from ramstk.views.gtk3.widgets import RAMSTKPanel, RAMSTKWorkView

# RAMSTK Local Imports
from . import FMEAMethodPanel, FMEATreePanel


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
    :cvar str _tag: the name of the module.

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
    :ivar dict _dic_missions: dict containing all the missions associated
        with the selected Revision.
    :ivar dict _dic_mission_phases: dict containing all the mission phases
        associated with each mission in _dic_missions.
    :ivar float _item_hazard_rate: hazard rate of the Hardware item associated
        with the FMEA.
    """

    # Define private dictionary attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "fmea"
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
        self._lst_callbacks.insert(2, super().do_request_delete)
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
            _(
                "Save changes to all entities at the same level as the selected entity "
                "in the (D)FME(C)A."
            ),
        ]

        # Initialize private scalar attributes.
        self._hardware_id: int = 0
        self._item_hazard_rate: float = 0.0

        self._pnlMethods: RAMSTKPanel = FMEAMethodPanel()
        self._pnlPanel: RAMSTKPanel = FMEATreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_record_id, f"selected_{self._tag}")
        pub.subscribe(
            self._on_get_hardware_attributes, "succeed_get_hardware_attributes"
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

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        _attributes = self.__do_get_fmea_ids()

        if self._pnlPanel.level == "cause":
            _level, _no_keys = self.__on_request_insert_control_action()
        elif self._pnlPanel.level == "mechanism":
            _level = "cause"
            _no_keys = ["control_id", "action_id"]
        elif self._pnlPanel.level == "mode":
            _level = "mechanism"
            _no_keys = ["cause_id", "control_id", "action_id"]
        else:
            print("Raise dialog 'cause can't add child to control or action.")
            return

        for _key in _no_keys:
            _attributes.pop(_key)

        super().do_set_cursor_busy()

        pub.sendMessage(f"request_insert_{_level}", attributes=_attributes)

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        """Request to insert a new entity to the FMEA.

        :return: None
        :rtype: None
        """
        _attributes = self.__do_get_fmea_ids()
        _level = self._pnlPanel.level

        if _level in ["action", "control"]:
            _level, _no_keys = self.__on_request_insert_control_action()
        elif _level == "cause":
            _no_keys = ["control_id", "action_id"]
        elif _level == "mechanism":
            _no_keys = ["cause_id", "control_id", "action_id"]
        else:
            _no_keys = ["mechanism_id", "cause_id", "control_id", "action_id"]

        for _key in _no_keys:
            _attributes.pop(_key)

        super().do_set_cursor_busy()

        pub.sendMessage(f"request_insert_{_level}", attributes=_attributes)

    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the hardware ID.

        :param attributes:
        :return: None
        :rtype: None
        """
        self._hardware_id = attributes["hardware_id"]

    def __do_get_fmea_ids(self) -> Dict[str, int]:
        """Read each of the ID columns.

        :return: _attributes
        :rtype: dict
        """
        _attributes = {
            "revision_id": self._revision_id,
            "hardware_id": self._hardware_id,
            "mode_id": 0,
            "mechanism_id": 0,
            "cause_id": 0,
            "control_id": 0,
            "action_id": 0,
        }

        (
            _model,
            _row,
        ) = self._pnlPanel.tvwTreeView.get_selection().get_selected()

        _attributes["mode_id"] = _model.get_value(_row, 2)
        _attributes["mechanism_id"] = _model.get_value(_row, 3)
        _attributes["cause_id"] = _model.get_value(_row, 4)
        _attributes["control_id"] = _model.get_value(_row, 5)
        _attributes["action_id"] = _model.get_value(_row, 6)

        return _attributes

    def __do_load_action_lists(self) -> None:
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

    def __do_load_rpn_lists(self) -> None:
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

    def __do_load_severity_lists(self) -> None:
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
        self.__do_load_action_lists()
        self.__do_load_rpn_lists()
        self.__do_load_severity_lists()
        self._pnlPanel.do_load_comboboxes()

        self.remove(self.get_children()[-1])
        _hpaned.pack1(self._pnlMethods, True, True)
        _hpaned.pack2(self._pnlPanel, True, True)

        self.show_all()

    def __on_request_insert_control_action(self) -> Tuple[str, List[str]]:
        """Raise dialog to select whether to add a control or action.

        :return: _level, _no_keys; the level to add, control or action and the list
            of ID columns to pop from the attributes list.
        :rtype: tuple
        """
        _level = ""
        _no_keys = []

        _dialog = AddControlAction(
            parent=self.get_parent().get_parent().get_parent().get_parent()
        )

        if _dialog.do_run() == Gtk.ResponseType.OK:
            if _dialog.rdoControl.get_active():
                _level = "control"
                _no_keys = ["action_id"]
            elif _dialog.rdoAction.get_active():
                _level = "action"
                _no_keys = ["control_id"]

        _dialog.do_destroy()

        return _level, _no_keys
