# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.requirement.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Requirement Views."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKMessageDialog,
    RAMSTKModuleView,
    RAMSTKWorkView,
)

# RAMSTK Local Imports
from . import (
    RequirementClarityPanel,
    RequirementCompletenessPanel,
    RequirementConsistencyPanel,
    RequirementGeneralDataPanel,
    RequirementTreePanel,
    RequirementVerifiabilityPanel,
)


class RequirementModuleView(RAMSTKModuleView):
    """Display Requirement attribute data in the RAMSTK Module Book.

    The Requirement Module View displays all the Requirements associated with
    the connected RAMSTK Program in a flat list.  The attributes of a
    Requirement Module View are:

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
    _tag: str = "requirement"
    _tablabel: str = "Requirement"
    _tabtooltip: str = _(
        "Displays the requirements hierarchy for the selected Revision."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Requirement Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons["tab"] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/requirement.png"
        )

        # Initialize private list attributes.
        self._lst_callbacks.insert(1, self.do_request_insert_child)
        self._lst_icons[0] = "insert_sibling"
        self._lst_icons.insert(1, "insert_child")
        self._lst_mnu_labels = [
            _("Add Sibling Requirement"),
            _("Add Child Requirement"),
            _("Delete Selected Requirement"),
            _("Save Selected Requirement"),
            _("Save All Requirements"),
        ]
        self._lst_tooltips = [
            _("Add a new sibling requirement."),
            _("Add a new child requirement."),
            _("Remove the currently selected requirement."),
            _("Save changes to the currently selected requirement."),
            _("Save changes to all requirements"),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = RequirementTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, f"selected_{self._tag}")

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        """Request to delete selected record from the RAMSTKRequirement table.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        _parent = self.get_parent().get_parent().get_parent().get_parent().get_parent()
        _prompt = _(
            f"You are about to delete Requirement {self.dic_pkeys['record_id']} and "
            f"all data associated with it.  Is this really what you want to do?"
        )
        _dialog = RAMSTKMessageDialog(parent=_parent)
        _dialog.do_set_message(_prompt)
        _dialog.do_set_message_type("question")

        if _dialog.do_run() == Gtk.ResponseType.YES:
            super().do_set_cursor_busy()
            pub.sendMessage(
                "request_delete_requirement",
                node_id=self.dic_pkeys["record_id"],
            )

        _dialog.do_destroy()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the Requirement's record and parent ID.

        :param attributes: the attributes dict for the selected Requirement.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["requirement_id"]
        self.dic_pkeys["requirement_id"] = attributes["requirement_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the requirement module view.

        :return: None
        """
        super().make_ui()

        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_WORKGROUPS:
            self._pnlPanel.lst_owner.append(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_WORKGROUPS[_key][0]
            )

        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE:
            self._pnlPanel.lst_type.append(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE[_key][1]
            )

        # pylint: disable=unused-variable
        self._pnlPanel.tvwTreeView.do_load_combo_cell(
            self._pnlPanel.tvwTreeView.position["owner"],
            self._pnlPanel.lst_owner,
        )
        self._pnlPanel.tvwTreeView.do_load_combo_cell(
            self._pnlPanel.tvwTreeView.position["priority"],
            ["", "1", "2", "3", "4", "5"],
        )
        self._pnlPanel.tvwTreeView.do_load_combo_cell(
            self._pnlPanel.tvwTreeView.position["requirement_type"],
            self._pnlPanel.lst_type,
        )

        self._pnlPanel.do_set_cell_callbacks(
            "mvw_editing_requirement",
            [
                "derived",
                "description",
                "figure_number",
                "owner",
                "page_number",
                "priority",
                "specification",
                "requirement_type",
                "validated",
                "validated_date",
            ],
        )
        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )


class RequirementGeneralDataView(RAMSTKWorkView):
    """Display general Requirement attribute data in the RAMSTK Work Book.

    The Requirement Work View displays all the general data attributes for the
    selected Requirement.  The attributes of a requirement Work View are:

    :cvar str _tag: the name of the module.
    :cvar str _tablabel: the text to display on the tab's label.
    :cvar str _tabtooltip: the text to display as the tab's tooltip.

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

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "requirement"
    _tablabel: str = _("General\nData")
    _tabtooltip: str = _("Displays general information for the selected Requirement.")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Requirement Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons["create_code"] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/create_code.png"
        )

        # Initialize private list attributes.
        self._lst_callbacks.insert(0, self._do_request_create_code)
        self._lst_icons.insert(0, "create_code")
        self._lst_mnu_labels = [
            _("Create Code"),
            _("Save Selected Requirement"),
            _("Save All Requirements"),
        ]
        self._lst_tooltips = [
            _("Automatically create code for the selected requirement."),
            _("Save changes to the currently selected requirement."),
            _("Save changes to all requirements."),
        ]

        # Initialize private scalar attributes.
        self._pnlGeneralData: RAMSTKFixedPanel = RequirementGeneralDataPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_set_cursor_active, "succeed_create_code")

        pub.subscribe(self._do_set_record_id, "selected_requirement")

    def _do_request_create_code(self, __button: Gtk.ToolButton) -> None:
        """Request that requirement codes be built.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :py:class:`Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        _prefix = self._pnlGeneralData.cmbRequirementType.get_value()

        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_create_requirement_code",
            node_id=self.dic_pkeys["record_id"],
            prefix=_prefix,
        )

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the record and parent ID.

        :param attributes: the attributes dict for the selected requirement.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["requirement_id"]
        self.dic_pkeys["requirement_id"] = attributes["requirement_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Requirement General Data tab.

        :return: None
        :rtype: None
        """
        super().do_make_layout()

        # Add the validation date dialog launcher button to the right of the
        # validated date RAMSTKEntry.
        _fixed: Gtk.Fixed = (
            self._pnlGeneralData.get_children()[0].get_children()[0].get_children()[0]
        )
        _entry: RAMSTKEntry = _fixed.get_children()[-1]
        _x_pos: int = _fixed.child_get_property(_entry, "x") + 205
        _y_pos: int = _fixed.child_get_property(_entry, "y")
        _fixed.put(self._pnlGeneralData.btnValidateDate, _x_pos, _y_pos)

        self._pnlGeneralData.do_load_priorities()
        self._pnlGeneralData.do_load_requirement_types(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_REQUIREMENT_TYPE
        )
        self._pnlGeneralData.do_load_workgroups(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_WORKGROUPS
        )

        self.pack_end(self._pnlGeneralData, True, True, 0)
        self.show_all()


class RequirementAnalysisView(RAMSTKWorkView):
    """Display Requirement attribute data in the RAMSTK Work Book.

    The Requirement Analysis Work View displays all the analysis questions and
    answers for the selected Requirement. The attributes of a Requirement
    Analysis Work View are:

    :cvar str _tag: the name of the module.
    :cvar str _tablabel: the text to display on the tab's label.
    :cvar str _tabtooltip: the text to display as the tab's tooltip.

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

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "requirement"
    _tablabel: str = "<span weight='bold'>" + _("Analysis") + "</span>"
    _tabtooltip: str = _("Analyzes the selected requirement.")

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Requirements analysis work view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._pnlClarity: RAMSTKFixedPanel = RequirementClarityPanel()
        self._pnlCompleteness: RAMSTKFixedPanel = RequirementCompletenessPanel()
        self._pnlConsistency: RAMSTKFixedPanel = RequirementConsistencyPanel()
        self._pnlVerifiability: RAMSTKFixedPanel = RequirementVerifiabilityPanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_set_record_id, "selected_requirement")

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the record and parent ID.

        :param attributes: the attributes dict for the selected requirement.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["requirement_id"]
        self.dic_pkeys["requirement_id"] = attributes["requirement_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Requirement Analysis tab.

        :return: None
        :rtype: None
        """
        _vpaned_left, _vpaned_right = super().do_make_layout_llrr()

        _vpaned_left.pack1(self._pnlClarity, False)
        _vpaned_left.pack2(self._pnlCompleteness, False)
        _vpaned_right.pack1(self._pnlConsistency, False)
        _vpaned_right.pack2(self._pnlVerifiability, False)

        self.show_all()
