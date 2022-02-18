# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.validation.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Validation Views."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKMessageDialog,
    RAMSTKModuleView,
    RAMSTKPanel,
    RAMSTKWorkView,
)

# RAMSTK Local Imports
from . import (
    ValidationTaskDescriptionPanel,
    ValidationTaskEffortPanel,
    ValidationTreePanel,
)


class ValidationModuleView(RAMSTKModuleView):
    """Display Validation attribute data in the RAMSTK Module Book.

    The Validation Module View displays all the Validations associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Validation
    Module View are:

    :cvar _tag: the name of the module.

    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "validation"
    _tablabel: str = "Verification"
    _tabtooltip: str = _(
        "Displays the list of verification tasks for the selected Revision."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Validation Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons["tab"] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/validation.png"
        )

        # Initialize private list attributes.
        self._lst_mnu_labels = [
            _("Add Verification Task"),
            _("Delete Selected Task"),
            _("Save Selected Task"),
            _("Save All Tasks"),
        ]
        self._lst_tooltips = [
            _("Add a new verification task."),
            _("Remove the currently selected verification task."),
            _("Save changes to the currently selected verification task."),
            _("Save changes to all verification tasks."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = ValidationTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, f"selected_{self._tag}")

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKValidation table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent().get_parent()
        _prompt = _(
            "You are about to delete Validation {0:d} and all "
            "data associated with it.  Is this really what "
            "you want to do?"
        ).format(self.dic_pkeys["record_id"])
        _dialog: RAMSTKMessageDialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type("question")

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                "request_delete_validation",
                node_id=self.dic_pkeys["record_id"],
            )

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Verification task's record ID.

        :param attributes: the attribute dict for the selected Verification
            task.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["validation_id"] = attributes["validation_id"]
        self.dic_pkeys["record_id"] = attributes["validation_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the requirement module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.do_load_measurement_units(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS
        )
        self._pnlPanel.do_load_verification_types(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        )

        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )


class ValidationGeneralDataView(RAMSTKWorkView):
    """Display general Validation attribute data in the RAMSTK Work Book.

    The Validation Work View displays all the general data attributes for the
    selected Validation. The attributes of a Validation General Data Work View
    are:

    :cvar dict _dic_keys:
    :cvar list _lst_labels: the list of label text.
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
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "validation"
    _tablabel: str = _("General\nData")
    _tabtooltip: str = _(
        "Displays general information for the selected Verification task."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Validation Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate,
            self._do_request_calculate_all,
            super().do_request_update,
            super().do_request_update_all,
        ]
        self._lst_icons = ["calculate", "calculate_all", "save", "save-all"]
        self._lst_mnu_labels = [
            _("Calculate Task"),
            _("Calculate Program"),
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _(
                "Calculate the expected cost and time of the selected Verification "
                "task."
            ),
            _(
                "Calculate the cost and time of the program (i.e., all Verfication "
                "tasks)."
            ),
            _("Save changes to the selected Verification task."),
            _("Save changes to all Verification tasks."),
        ]

        # Initialize private scalar attributes.
        self._pnlTaskDescription: RAMSTKPanel = ValidationTaskDescriptionPanel()
        self._pnlTaskEffort: RAMSTKPanel = ValidationTaskEffortPanel()
        # self._pnlProgramEffort: RAMSTKPanel = ProgramEffortPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().do_set_cursor_active_on_fail,
            "fail_calculate_validation_task",
        )

        pub.subscribe(self._do_set_record_id, "selected_validation")

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate the selected validation task.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_calculate_validation_task",
            node_id=self.dic_pkeys["record_id"],
        )

    def _do_request_calculate_all(self, __button: Gtk.ToolButton) -> None:
        """Request to calculate program cost and time.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_calculate_all_validation_tasks",
        )

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Verification task record ID.

        :param attributes: the attribute dict for the selected Validation task.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["validation_id"] = attributes["validation_id"]
        self.dic_pkeys["record_id"] = attributes["validation_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Validation General Data tab.

        :return: None
        :rtype: None
        """
        _hpaned, _vpaned_right = super().do_make_layout_lrr()

        self._pnlTaskDescription.fmt = self.fmt
        self._pnlTaskDescription.do_load_measurement_units(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MEASUREMENT_UNITS
        )
        self._pnlTaskDescription.do_load_validation_types(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        )
        _hpaned.pack1(self._pnlTaskDescription, True, True)

        self._pnlTaskEffort.fmt = self.fmt
        self._pnlTaskEffort.do_load_validation_types(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_VALIDATION_TYPE
        )
        # self._pnlProgramEffort.fmt = self.fmt
        _vpaned_right.pack1(self._pnlTaskEffort, True, True)
        # _vpaned_right.pack2(self._pnlProgramEffort, True, True)

        self.show_all()
