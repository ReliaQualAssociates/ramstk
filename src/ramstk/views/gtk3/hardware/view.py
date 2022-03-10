# pylint: disable=cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.view.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Hardware Views."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTK_ACTIVE_ENVIRONMENTS,
    RAMSTK_DORMANT_ENVIRONMENTS,
    RAMSTK_HR_DISTRIBUTIONS,
    RAMSTK_HR_MODELS,
    RAMSTK_HR_TYPES,
    RAMSTKUserConfiguration,
)
from ramstk.logger import RAMSTKLogManager
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.design_electric import (
    CapacitorDesignElectricInputPanel,
    ConnectionDesignElectricInputPanel,
    DesignElectricEnvironmentalInputPanel,
    DesignElectricStressInputPanel,
    DesignElectricStressResultPanel,
    ICDesignElectricInputPanel,
    InductorDesignElectricInputPanel,
    MeterDesignElectricInputPanel,
    MiscDesignElectricInputPanel,
    RelayDesignElectricInputPanel,
    ResistorDesignElectricInputPanel,
    SemiconductorDesignElectricInputPanel,
    SwitchDesignElectricInputPanel,
)
from ramstk.views.gtk3.milhdbk217f import (
    CapacitorMilHdbk217FResultPanel,
    ConnectionMilHdbk217FResultPanel,
    ICMilHdbk217FResultPanel,
    InductorMilHdbk217FResultPanel,
    MeterMilHdbk217FResultPanel,
    MiscellaneousMilHdbk217FResultPanel,
    RelayMilHdbk217FResultPanel,
    ResistorMilHdbk217FResultPanel,
    SemiconductorMilHdbk217FResultPanel,
    SwitchMilHdbk217FResultPanel,
)
from ramstk.views.gtk3.reliability import (
    AvailabilityResultsPanel,
    ReliabilityInputPanel,
    ReliabilityResultsPanel,
)
from ramstk.views.gtk3.widgets import RAMSTKModuleView, RAMSTKPanel, RAMSTKWorkView

# RAMSTK Local Imports
from . import (
    HardwareGeneralDataPanel,
    HardwareLogisticsPanel,
    HardwareMiscellaneousPanel,
    HardwareTreePanel,
)


class HardwareModuleView(RAMSTKModuleView):
    """Display Hardware attribute data in the RAMSTK Module Book.

    The Hardware Module View displays all the Hardware associated with the
    connected RAMSTK Program in a flat list.  The attributes of a Hardware
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
    _tablabel: str = "Hardware"
    _tabtooltip: str = _(
        "Displays the hardware hierarchy (BoM) for the selected Revision."
    )
    _tag: str = "hardware"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Hardware Module View.

        :param configuration: the RAMSTK Configuration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons["tab"] = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR + "/32x32/hardware.png"
        )

        # Initialize private list attributes.
        self._lst_callbacks[0] = self._do_request_insert_sibling
        self._lst_callbacks.insert(1, self._do_request_insert_child)
        self._lst_callbacks.insert(2, self._do_request_insert_part)
        self._lst_callbacks.insert(4, self._do_request_calculate_hardware)
        self._lst_callbacks.insert(5, self._do_request_calculate_all_hardware)
        self._lst_icons[0] = "insert_sibling"
        self._lst_icons.insert(1, "insert_child")
        self._lst_icons.insert(2, "insert_part")
        self._lst_icons.insert(4, "calculate")
        self._lst_icons.insert(5, "calculate_all")
        self._lst_mnu_labels: List[str] = [
            _("Add Sibling Assembly"),
            _("Add Child Assembly"),
            _("Add Piece Part"),
            _("Delete Selected"),
            _("Calculate the Selected"),
            _("Calculate the System"),
            _("Save Selected Hardware"),
            _("Save All Hardware"),
        ]
        self._lst_tooltips: List[str] = [
            _(
                "Adds a new hardware assembly at the same hierarchy level as the "
                "selected hardware item (i.e., a sibling hardware item)."
            ),
            _(
                "Adds a new hardware assembly one level subordinate to the selected "
                "hardware item (i.e., a child hardware item)."
            ),
            _(
                "Adds a new hardware component/piece-part to the the selected hardware "
                "assembly."
            ),
            _("Remove the currently selected hardware item and any children."),
            _("Calculate the selected hardware item and all of it's children."),
            _("Calculate the entire system."),
            _("Save changes to the selected hardware item."),
            _("Save changes to the entire system."),
        ]

        # Initialize private scalar attributes.
        self._pnlPanel = HardwareTreePanel()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._do_set_record_id,
            f"selected_{self._tag}",
        )

    def _do_request_calculate_hardware(self, __button: Gtk.ToolButton) -> None:
        """Send request to calculate the selected hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_calculate_hardware",
            node_id=self.dic_pkeys["record_id"],
        )

    def _do_request_calculate_all_hardware(self, __button: Gtk.ToolButton) -> None:
        """Send request to iteratively calculate all hardware items.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_calculate_hardware",
            node_id=1,
        )

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> Any:
        """Request to insert a new child assembly under the selected assembly.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        if self._pnlPanel.part == 1:
            _message = _(
                "You cannot add a child item to a part.  First set the "
                "component category to nothing to convert this part to an "
                "assembly and then try again."
            )
            _parent = (
                self.get_parent().get_parent().get_parent().get_parent().get_parent()
            )
            _dialog = super().do_raise_dialog(parent=_parent)
            _dialog.do_set_message(message=_message)
            _dialog.do_set_message_type(message_type="info")
            _dialog.do_run()
            _dialog.do_destroy()
            return

        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": self.dic_pkeys["revision_id"],
                "hardware_id": self.dic_pkeys["hardware_id"],
                "parent_id": self.dic_pkeys["hardware_id"],
                "part": 0,
                "record_id": self.dic_pkeys["record_id"],
            },
        )

    def _do_request_insert_part(self, __button: Gtk.ToolButton) -> None:
        """Send request to insert a piece part to the selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        if self._pnlPanel.part == 1:
            _message = _(
                "You cannot add a part to another part.  First set the "
                "component category to nothing to convert this part to an "
                "assembly and then try again."
            )
            _parent = (
                self.get_parent().get_parent().get_parent().get_parent().get_parent()
            )
            _dialog = super().do_raise_dialog(parent=_parent)
            _dialog.do_set_message(message=_message)
            _dialog.do_set_message_type(message_type="info")
            _dialog.do_run()
            _dialog.do_destroy()
            return

        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": self.dic_pkeys["revision_id"],
                "hardware_id": self.dic_pkeys["hardware_id"],
                "parent_id": self.dic_pkeys["hardware_id"],
                "part": 1,
                "record_id": self.dic_pkeys["record_id"],
            },
        )

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> Any:
        """Send request to insert a new sibling Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        """
        if self.dic_pkeys["parent_id"] == 0:
            _message = _(
                "You cannot have two top-level items for a single revision.  "
                "If you want to add a new system, you need create a new RAMSTK "
                "Program database.  If you want to add a new configuration, "
                "variant, etc. of the system in this Program database, "
                "add a new Revision."
            )
            _parent = (
                self.get_parent().get_parent().get_parent().get_parent().get_parent()
            )
            _dialog = super().do_raise_dialog(parent=_parent)
            _dialog.do_set_message(message=_message)
            _dialog.do_set_message_type(message_type="info")
            _dialog.do_run()
            _dialog.do_destroy()
            return

        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_insert_hardware",
            attributes={
                "revision_id": self.dic_pkeys["revision_id"],
                "hardware_id": self.dic_pkeys["hardware_id"],
                "parent_id": self.dic_pkeys["parent_id"],
                "part": 0,
                "record_id": self.dic_pkeys["record_id"],
            },
        )

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the work stream module's record ID and, if any, parent ID.

        :param attributes: the attribute dict for the selected work stream module item.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["hardware_id"] = attributes["hardware_id"]
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["hardware_id"]

    def __do_load_lists(self) -> None:
        """Load the pick lists associated with Hardware.

        :return: None
        :rtype: None
        """
        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_CATEGORIES:
            self._pnlPanel.lst_categories.append(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_CATEGORIES[_key]
            )
            self._pnlPanel.dic_subcategories[_key] = [""]

            for _subkey in self.RAMSTK_USER_CONFIGURATION.RAMSTK_SUBCATEGORIES[_key]:
                self._pnlPanel.dic_subcategories[_key].append(
                    self.RAMSTK_USER_CONFIGURATION.RAMSTK_SUBCATEGORIES[_key][_subkey]
                )

        for _key in self.RAMSTK_USER_CONFIGURATION.RAMSTK_MANUFACTURERS:
            self._pnlPanel.lst_manufacturers.append(
                self.RAMSTK_USER_CONFIGURATION.RAMSTK_MANUFACTURERS[_key][0]
            )

    def __make_ui(self) -> None:
        """Build the user interface for the function module view.

        :return: None
        """
        super().make_ui()

        self._pnlPanel.dic_icons = self._dic_icons

        self.__do_load_lists()
        self._pnlPanel.do_load_comboboxes()

        self._pnlPanel.do_set_cell_callbacks(
            "mvw_editing_hardware",
            [
                "alt_part_number",
                "cage_code",
                "cost",
                "description",
                "duty_cycle",
                "figure_number",
                "lcn",
                "manufacturer_id",
                "mission_time",
                "name",
                "nsn",
                "page_number",
                "part",
                "part_number",
                "quantity",
                "ref_des",
                "remarks",
                "repairable",
                "specification_number",
                "tagged_part",
                "year_of_manufacture",
            ],
        )
        self._pnlPanel.tvwTreeView.dic_handler_id[
            "button-press"
        ] = self._pnlPanel.tvwTreeView.connect(
            "button_press_event", super().on_button_press
        )


class HardwareGeneralDataView(RAMSTKWorkView):
    """Display general Hardware attribute data in the RAMSTK Work Book.

    The Hardware Work View displays all the general data attributes for the
    selected Hardware.  The attributes of a Hardware General Data Work View
    are:

    :cvar _module: the name of the module.

    :ivar _lst_callbacks: the list of callback methods for the view's
        toolbar buttons and pop-up menu.  The methods are listed in the order
        they appear on the toolbar and pop-up menu.
    :ivar _lst_icons: the list of icons for the view's toolbar buttons
        and pop-up menu.  The icons are listed in the order they appear on the
        toolbar and pop-up menu.
    :ivar _lst_mnu_labels: the list of labels for the view's pop-up
        menu.  The labels are listed in the order they appear in the menu.
    :ivar _lst_tooltips: the list of tooltips for the view's
        toolbar buttons and pop-up menu.  The tooltips are listed in the
        order they appear on the toolbar or pop-up menu.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _tag: str = "hardware"
    _tablabel: str = _("General\nData")
    _tabtooltip: str = _("Displays general information for the selected Hardware")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize the Hardware Work View general data page.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :type configuration:
            :class:`ramstk.configuration.RAMSTKUserConfiguration`
        :param logger: the RAMSTKLogManager class instance.
        :type logger: :class:`ramstk.logger.RAMSTKLogManager`
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_icons[
            "comp_ref_des"
        ] = f"{self.RAMSTK_USER_CONFIGURATION.RAMSTK_ICON_DIR}/32x32/rollup.png"

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self._pnlGeneralData: RAMSTKPanel = HardwareGeneralDataPanel()
        self._pnlLogistics: RAMSTKPanel = HardwareLogisticsPanel()
        self._pnlMiscellaneous: RAMSTKPanel = HardwareMiscellaneousPanel()

        self._lst_callbacks = [
            self._do_request_make_comp_ref_des,
            super().do_request_update,
            super().do_request_update_all,
        ]
        self._lst_icons = [
            "comp_ref_des",
            "save",
            "save-all",
        ]
        self._lst_mnu_labels = [
            _("Comp. Ref. Des."),
            _("Save"),
            _("Save All"),
        ]
        self._lst_tooltips = [
            _(
                "Creates the composite reference designator for the "
                "selected hardware item."
            ),
            _("Save changes to the currently selected hardware item."),
            _("Save changes to all hardware items."),
        ]

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._do_set_record_id,
            f"selected_{self._tag}",
        )

    def _do_request_make_comp_ref_des(self, __button: Gtk.ToolButton) -> None:
        """Send request to create the composite reference designator.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        super().do_set_cursor_busy()
        pub.sendMessage(
            "request_make_comp_ref_des", node_id=self.dic_pkeys["record_id"]
        )
        super().do_set_cursor_active()

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the work stream module's record ID and, if any, parent ID.

        :param attributes: the attributes dict for the selected work stream
            module item.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["hardware_id"] = attributes["hardware_id"]
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["hardware_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Hardware General Data tab.

        :return: None
        :rtype: None
        """
        _hpaned, _vpaned_right = super().do_make_layout_lrr()

        self._pnlGeneralData.fmt = self.fmt
        self._pnlGeneralData.dicSubcategories = (
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_SUBCATEGORIES
        )
        self._pnlGeneralData.do_load_categories(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_CATEGORIES
        )
        _hpaned.pack1(self._pnlGeneralData, True, True)

        self._pnlLogistics.do_load_cost_types()
        self._pnlLogistics.do_load_manufacturers(
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_MANUFACTURERS
        )
        _vpaned_right.pack1(self._pnlLogistics, True, True)

        _vpaned_right.pack2(self._pnlMiscellaneous, True, True)

        self.show_all()


class HardwareAssessmentInputView(RAMSTKWorkView):
    """Display Hardware assessment input attribute data.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2 and NSWC-11.  The attributes of a Hardware assessment
    input view are:

    :cvar list _lst_labels: the text to use for the assessment input widget
        labels.
    :cvar str _tag: the name of the module.

    :ivar dict _dic_assessment_input: dictionary of component-specific
        AssessmentInputs classes.
    :ivar int _hardware_id: the ID of the Hardware item currently being
        displayed.
    :ivar int _hazard_rate_method_id: the ID of the hazard rate method used for
        Hardware item.
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

    # Define private dict attributes.

    # Define private list attributes.
    _lst_title: List[str] = [_("Operating Stresses")]

    # Define private scalar class attributes.
    _tag: str = "hardware"
    _tablabel: str = _("Assessment\nInputs")
    _tabtooltip: str = _(
        "Displays reliability assessment inputs for the selected hardware item."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize an instance of the Hardware assessment input view.

        :param configuration: the RAMSTKUserConfiguration class instance.
        :param logger: the RAMSTKLogManager class instance.
        """
        super().__init__(configuration, logger)

        # Initialize private dictionary attributes.
        self._dic_component_panels: Dict[int, RAMSTKPanel] = {
            1: ICDesignElectricInputPanel(),
            2: SemiconductorDesignElectricInputPanel(),
            3: ResistorDesignElectricInputPanel(),
            4: CapacitorDesignElectricInputPanel(),
            5: InductorDesignElectricInputPanel(),
            6: RelayDesignElectricInputPanel(),
            7: SwitchDesignElectricInputPanel(),
            8: ConnectionDesignElectricInputPanel(),
            9: MeterDesignElectricInputPanel(),
            10: MiscDesignElectricInputPanel(),
        }

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate,
            self._do_request_update,
            super().do_request_update_all,
        ]
        self._lst_icons = [
            "calculate",
            "save",
            "save-all",
        ]
        self._lst_tooltips = [
            _(
                "Calculate the currently selected hardware item and all of "
                "it's children."
            ),
            _("Save changes to the currently selected hardware item."),
            _("Save changes to all hardware items."),
        ]

        # Initialize private scalar attributes.
        self._pnlReliabilityInput: RAMSTKPanel = ReliabilityInputPanel()
        self._pnlEnvironmentalInput: RAMSTKPanel = (
            DesignElectricEnvironmentalInputPanel()
        )
        self._pnlStressInput: RAMSTKPanel = DesignElectricStressInputPanel()

        # We need to carry these as an attribute for this view because the
        # lower part of each is dynamically loaded with the component panels.
        self._vpnLeft: Gtk.VPaned = Gtk.VPaned()
        self._vpnRight: Gtk.VPaned = Gtk.VPaned()

        self._hazard_rate_method_id: int = 0
        self._subcategory_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            super().do_set_cursor_active,
            "succeed_calculate_hardware",
        )

        pub.subscribe(
            self._do_pack_component_panel,
            "selected_hardware",
        )
        pub.subscribe(
            self._do_pack_component_panel,
            "succeed_get_hardware_attributes",
        )
        pub.subscribe(
            self._do_pack_component_panel,
            "hardware_category_changed",
        )
        pub.subscribe(
            self._do_set_record_id,
            f"selected_{self._tag}",
        )

    def _do_pack_component_panel(self, attributes: Dict[str, Any]) -> None:
        """Pack panel used to display component-specific input attributes.

        :param attributes: dict containing the attributes of the hardware
            item being loaded.
        :return: None
        :rtype: None
        """
        # If there was a component selected, hide it's widgets.  We get an
        # attribute error if no parts have been selected in the current
        # session.
        if self._vpnRight.get_child2() is not None:
            self._vpnRight.remove(self._vpnRight.get_child2())

        # Retrieve the appropriate component-specific view.
        if attributes["category_id"] > 0:
            _panel: RAMSTKPanel = self._dic_component_panels[attributes["category_id"]]
            _panel.fmt = self.fmt
            _panel.category_id = attributes["category_id"]
            self._vpnRight.pack2(_panel, True, True)
            self.show_all()

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Send request to calculate the selected hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        try:
            super().do_set_cursor_busy()
            pub.sendMessage(
                "request_calculate_hardware",
                node_id=self.dic_pkeys["record_id"],
            )
        except KeyError as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        """Send request to update all tables for the selected hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :return: None
        :rtype: None
        """
        for _table in [
            "design_electric",
            "hardware",
            "reliability",
        ]:
            pub.sendMessage(
                f"request_update_{_table}",
                node_id=self.dic_pkeys["record_id"],
            )

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the work stream module's record ID and, if any, parent ID.

        :param attributes: the attributes dict for the selected work stream
            module item.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["hardware_id"] = attributes["hardware_id"]
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["hardware_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Hardware Assessment Input tab.

        :return: None
        :rtype: None
        """
        self._vpnLeft, self._vpnRight = super().do_make_layout_llrr()

        # Top left quadrant.
        self._pnlReliabilityInput.fmt = self.fmt
        self._pnlReliabilityInput.do_load_hr_distributions(RAMSTK_HR_DISTRIBUTIONS)
        self._pnlReliabilityInput.do_load_hr_methods(RAMSTK_HR_MODELS)
        self._pnlReliabilityInput.do_load_hr_types(RAMSTK_HR_TYPES)
        self._vpnLeft.pack1(self._pnlReliabilityInput, True, True)

        # Bottom left quadrant.
        self._pnlEnvironmentalInput.fmt = self.fmt
        self._pnlEnvironmentalInput.do_load_environment_active(
            RAMSTK_ACTIVE_ENVIRONMENTS
        )
        self._pnlEnvironmentalInput.do_load_environment_dormant(
            RAMSTK_DORMANT_ENVIRONMENTS
        )
        self._vpnLeft.pack2(self._pnlEnvironmentalInput, True, True)

        # Top right quadrant.
        self._pnlStressInput.fmt = self.fmt
        self._vpnRight.pack1(self._pnlStressInput, True, True)

        self.show_all()


class HardwareAssessmentResultsView(RAMSTKWorkView):
    """Display Hardware assessment results data in the RAMSTK Work View.

    The Hardware Assessment Results view displays all the assessment results
    for the selected Hardware.  The attributes of a Hardware Assessment Results
    View are:

    :cvar list _lst_labels: the text to use for the reliability assessment
        results widget labels.
    :cvar str _tag: the name of the module.

    :ivar dict _dic_assessment_results: dictionary of component-specific
        AssessmentResults classes.
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

    # Define private list class attributes.
    _lst_title = [_("Assessment Model Results"), _("Stress Results")]

    # Define private scalar class attributes.
    _tag: str = "hardware"
    _tablabel: str = _("Assessment\nResults")
    _tabtooltip: str = _(
        "Displays reliability, maintainability, and availability assessment results "
        "for the selected Hardware item."
    )

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None:
        """Initialize an instance of the Hardware assessment output view.

        :param configuration: the RAMSTK User Configuration class instance.
        :type configuration: :class:`ramstk.configuration.UserConfiguration`
        """
        super().__init__(configuration, logger)

        # Create a logger specifically for this class.
        self.RAMSTK_LOGGER.do_create_logger(
            __name__,
            self.RAMSTK_USER_CONFIGURATION.RAMSTK_LOGLEVEL,
            to_tty=False,
        )

        # Initialize private dictionary attributes.
        self._dic_component_results: Dict[int, RAMSTKPanel] = {
            1: ICMilHdbk217FResultPanel(),
            2: SemiconductorMilHdbk217FResultPanel(),
            3: ResistorMilHdbk217FResultPanel(),
            4: CapacitorMilHdbk217FResultPanel(),
            5: InductorMilHdbk217FResultPanel(),
            6: RelayMilHdbk217FResultPanel(),
            7: SwitchMilHdbk217FResultPanel(),
            8: ConnectionMilHdbk217FResultPanel(),
            9: MeterMilHdbk217FResultPanel(),
            10: MiscellaneousMilHdbk217FResultPanel(),
        }

        # Initialize private list attributes.
        self._lst_callbacks = [
            self._do_request_calculate,
            super().do_request_update,
            super().do_request_update_all,
        ]
        self._lst_icons = [
            "calculate",
            "save",
            "save-all",
        ]
        self._lst_tooltips = [
            _("Calculate the currently selected Hardware item."),
            _("Save changes to the currently selected Hardware item."),
            _("Save changes to all Hardware items."),
        ]

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = 0
        self._subcategory_id: int = 0

        self._pnlAvailabilityResults: RAMSTKPanel = AvailabilityResultsPanel()
        self._pnlReliabilityResults: RAMSTKPanel = ReliabilityResultsPanel()
        self._pnlStressResults: RAMSTKPanel = DesignElectricStressResultPanel()

        # We need to carry these as an attribute for this view because the
        # lower part of each is dynamically loaded with the component panels.
        self._vpnLeft: Gtk.VPaned = Gtk.VPaned()
        self._vpnRight: Gtk.VPaned = Gtk.VPaned()

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        self.__make_ui()

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._do_pack_component_panel,
            "selected_hardware",
        )
        pub.subscribe(
            self._do_pack_component_panel,
            "succeed_get_hardware_attributes",
        )
        pub.subscribe(
            self._do_pack_component_panel,
            "hardware_category_changed",
        )
        pub.subscribe(
            self._do_set_record_id,
            f"selected_{self._tag}",
        )

    def _do_pack_component_panel(self, attributes: Dict[str, Any]) -> None:
        """Load the results specific to hardware components.

        :param attributes:
        :return: None
        :rtype: None
        """
        # If there was a component selected, hide it's widgets.  We get an
        # attribute error if no parts have been selected in the current
        # session.
        if self._vpnRight.get_child2() is not None:
            self._vpnRight.remove(self._vpnRight.get_child2())

        # Retrieve the appropriate component-specific view.
        if attributes["category_id"] > 0:
            _panel: RAMSTKPanel = self._dic_component_results[attributes["category_id"]]
            _panel.fmt = self.fmt
            self._vpnRight.pack2(_panel, True, True)
            self.show_all()

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        """Send request to calculate the selected Hardware item.

        :param __button: the Gtk.ToolButton() that called this method.
        :type __button: :class:Gtk.ToolButton`
        :return: None
        :rtype: None
        """
        try:
            super().do_set_cursor_busy()
            pub.sendMessage(
                "request_calculate_hardware",
                node_id=self.dic_pkeys["record_id"],
            )
        except (IndexError, KeyError) as _error:
            self.RAMSTK_LOGGER.do_log_exception(__name__, _error)
            _parent = self.get_parent().get_parent().get_parent().get_parent()
            _dialog = super().do_raise_dialog(parent=_parent)
            _dialog.do_set_message(
                _(
                    f"One or more inputs necessary to calculate "
                    f'hardware ID {self.dic_pkeys["hardware_id"]} is '
                    f"missing."
                )
            )
            _dialog.do_set_message_type("warning")
            _dialog.do_run()
            _dialog.do_destroy()
            pub.sendMessage(
                "fail_calculate_hardware",
                error_message=_error,
            )

    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None:
        """Set the work stream module's record ID and, if any, parent ID.

        :param attributes: the attribute dict for the selected work stream
            module item.
        :return: None
        :rtype: None
        """
        self.dic_pkeys["revision_id"] = attributes["revision_id"]
        self.dic_pkeys["hardware_id"] = attributes["hardware_id"]
        self.dic_pkeys["parent_id"] = attributes["parent_id"]
        self.dic_pkeys["record_id"] = attributes["hardware_id"]

    def __make_ui(self) -> None:
        """Build the user interface for the Hardware Assessment Results tab.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        self._vpnLeft, self._vpnRight = super().do_make_layout_llrr()

        # Top left quadrant.
        self._pnlReliabilityResults.fmt = self.fmt
        self._vpnLeft.pack1(self._pnlReliabilityResults, True, True)

        # Bottom left quadrant.
        self._pnlAvailabilityResults.fmt = self.fmt
        self._vpnLeft.pack2(self._pnlAvailabilityResults, True, True)

        # Top right quadrant.
        self._pnlStressResults.fmt = self.fmt
        self._vpnRight.pack1(self._pnlStressResults, True, True)

        self.show_all()
