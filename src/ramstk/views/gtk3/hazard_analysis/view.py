# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hazard_analysis.view.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Hazard Analysis Views."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.assistants import EditFunction
from ramstk.views.gtk3.widgets import RAMSTKPanel, RAMSTKWorkView

# RAMSTK Local Imports
from . import HazardsTreePanel


class HazardsWorkView(RAMSTKWorkView):
    """Display HazOps attribute data in the Work Book.

    The WorkView displays all the attributes for the Hazards Analysis (HazOps).
    The attributes of a HazOps Work View are:

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
    :ivar int _hazard_id: the ID of the currently selected hazard.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag = "hazard"
    _tablabel = _("FHA")
    _tabtooltip = _("Displays the Hazards analysis for the selected Function.")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Work View for the HazOps.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_edit_function)
        self._lst_callbacks.insert(1, super().do_request_insert_sibling)
        self._lst_callbacks.insert(2, self.do_request_delete)
        self._lst_callbacks.insert(3, self._do_request_calculate)
        self._lst_icons.insert(0, "edit")
        self._lst_icons.insert(1, "add")
        self._lst_icons.insert(2, "remove")
        self._lst_icons.insert(3, "calculate")
        self._lst_mnu_labels = [
            _("Edit User Functions"),
            _("Add Hazard"),
            _("Delete Selected Hazard"),
            _("Calculate HazOp"),
            _("Save Selected Hazard"),
            _("Save All Hazards"),
        ]
        self._lst_tooltips = [
            _("Edit the hazards analysis user defined functions."),
            _("Add a new hazard to the HazOps analysis."),
            _("Delete the selected hazard from the selected function."),
            _("Calculate the HazOps analysis."),
            _("Save changes to the selected hazard."),
            _("Save changes to all hazards."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel: RAMSTKPanel = HazardsTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_hazard")
        pub.subscribe(self._on_select_function, "selected_function")

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate the HazOps HRI.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage("request_calculate_fha", node_id=self.dic_pkeys["record_id"])

    def _do_request_edit_function(self, __button: Gtk.ToolButton) -> None:
        """Request to edit the Similar Item analysis user-defined functions.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        (
            _model,
            _row,
        ) = self._pnlPanel.tvwTreeView.get_selection().get_selected()  # noqa

        _dialog = EditFunction(
            self._pnlPanel.tvwTreeView,
            dlgparent=self.get_parent().get_parent().get_parent().get_parent(),
            module="Hazards",
            labels=[
                _(
                    "You can define up to five functions.  "
                    "You can use the user float, the "
                    "user integer values, and results of "
                    "other functions.\n\n \
        User float is uf[1-3]\n \
        User integer is ui[1-3]\n \
        Function result is res[1-5]\n\n"
                ),
                _(
                    "For example, uf1*uf2+ui1, multiplies "
                    "the first two user float files and "
                    "adds the value to first user integer "
                    "field.\n\n"
                ),
            ],
            edit_message="wvw_editing_hazard",
            id_column=2,
            func_columns=[22, 23, 24, 25, 26],
        )

        if _dialog.do_run() == Gtk.ResponseType.OK:
            _functions = _dialog.do_set_functions(self._pnlPanel.tvwTreeView)
            if _dialog.chkApplyAll.get_active():
                _row = _model.get_iter_first()
                while _row is not None:
                    self._pnlPanel.do_refresh_functions(_row, _functions)
                    _row = _model.iter_next(_row)
            else:
                self._pnlPanel.do_refresh_functions(_row, _functions)

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the record ID when a hazard is selected.

        :param attributes: the hazard dict for the selected hazard ID.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["hazard_id"] = attributes["hazard_id"]
        self.dic_pkeys["record_id"] = attributes["hazard_id"]

    def _on_select_function(self, attributes: Dict[str, Any]) -> None:
        """Set the parent ID when a function is selected.

        :param attributes: the function dict for the selected function ID.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["parent_id"] = attributes["function_id"]
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["function_id"] = attributes["function_id"]

    def __do_load_lists(self) -> None:
        """Load the pick lists associated with Hazards.

        :return: None
        :rtype: None
        """
        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_HAZARDS:
            _hazard = (
                f"{self.RAMSTK_USER_CONFIGURATION.RAMSTK_HAZARDS[_key][0]}, "
                f"{self.RAMSTK_USER_CONFIGURATION.RAMSTK_HAZARDS[_key][1]}"
            )
            self._pnlPanel.lst_hazards.append(_hazard)

        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_SEVERITY:
            _severity = self.RAMSTK_USER_CONFIGURATION.RAMSTK_SEVERITY[_key][1]
            self._pnlPanel.lst_severity.append(_severity)

        for _probability in self.RAMSTK_USER_CONFIGURATION.RAMSTK_FAILURE_PROBABILITY:
            self._pnlPanel.lst_probability.append(_probability[0])

    def __make_ui(self) -> None:
        """Build the user interface for the Function Hazard Analysis tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()
        super().do_embed_treeview_panel()

        self.__do_load_lists()
        self._pnlPanel.do_load_comboboxes()

        self.show_all()
