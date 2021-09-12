# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Hardware Panels."""

# Standard Library Imports
from datetime import date
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib
from pubsub import pub

# noinspection PyPackageRequirements
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    RAMSTKTreePanel,
)


class HardwareTreePanel(RAMSTKTreePanel):
    """Panel to display hierarchy of hardware."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_hardwares"
    _tag = "hardware"
    _title = _("Hardware BoM")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self._dic_row_loader = {
            "hardware": self.__do_load_hardware,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.

        # Initialize public dictionary class attributes.
        self.dic_attribute_index_map: Dict[int, List[str]] = {
            2: ["alt_part_number", "string"],
            3: ["cage_code", "string"],
            5: ["cost", "string"],
            8: ["description", "string"],
            9: ["duty_cycle", "float"],
            10: ["figure_number", "string"],
            11: ["lcn", "string"],
            13: ["manufacturer_id", "integer"],
            14: ["mission_time", "float"],
            15: ["name", "string"],
            16: ["nsn", "string"],
            17: ["page_number", "string"],
            19: ["part", "boolean"],
            20: ["part_number", "string"],
            21: ["quantity", "integer"],
            22: ["ref_des", "string"],
            23: ["remarks", "string"],
            24: ["repairable", "boolean"],
            25: ["specification_number", "string"],
            26: ["tagged_part", "boolean"],
            29: ["year_of_manufacture", "string"],
            30: ["cost_type_id", "integer"],
            32: ["category_id", "integer"],
            33: ["subcategory_id", "integer"],
        }
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "hardware_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "alt_part_number": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "cage_code": [
                3,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "comp_ref_des": [
                4,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "cost": [
                5,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "cost_failure": [
                6,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "cost_hour": [
                7,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "description": [
                8,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "duty_cycle": [
                9,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "figure_number": [
                10,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "lcn": [
                11,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "level": [
                12,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "manufacturer_id": [
                13,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "mission_time": [
                14,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "name": [
                15,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "nsn": [
                16,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "page_number": [
                17,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "parent_id": [
                18,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "part": [
                19,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_hardware",
            ],
            "part_number": [
                20,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "quantity": [
                21,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "ref_des": [
                22,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "remarks": [
                23,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "repairable": [
                24,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_hardware",
            ],
            "specification_number": [
                25,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "tagged_part": [
                26,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                "mvw_editing_hardware",
            ],
            "total_part_count": [
                27,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "total_power_dissipation": [
                28,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "year_of_manufacture": [
                29,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "cost_type_id": [
                30,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "attachments": [
                31,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "category_id": [
                32,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
            "subcategory_id": [
                33,
                Gtk.CellRendererText(),
                "edited",
                None,
                "mvw_editing_hardware",
            ],
        }
        self.dic_icons = {"assembly": None, "part": None}

        # Initialize public list class attributes.

        # Initialize public scalar class attributes.

        super().do_make_panel()
        super().do_set_properties()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of hardware.")
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._on_module_switch, "mvwSwitchedPage")

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to changes in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == "hardware" and _row is not None:
            _comprefdes = _model.get_value(_row, self._lst_col_order[4])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Hardware item {0:s}: {1:s}").format(
                str(_comprefdes), str(_name)
            )

            pub.sendMessage("request_set_title", title=_title)

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Hardware package Module View RAMSTKTreeView().

        This method is called whenever a Hardware Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Hardware class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["hardware_id"]
            self._parent_id = _attributes["parent_id"]

            _title = _("Analyzing hardware item {0}: {1}").format(
                str(_attributes["comp_ref_des"]), str(_attributes["name"])
            )

            pub.sendMessage(
                "selected_hardware",
                attributes=_attributes,
            )
            pub.sendMessage(
                "request_set_title",
                title=_title,
            )
            for _table in [
                "design_electric",
                "hardware",
                "reliability",
            ]:
                pub.sendMessage(
                    "request_get_{}_attributes".format(_table),
                    node_id=self._record_id,
                )

    def __do_load_hardware(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a hardware item into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the hardware tree.
        :return: _new_row; the row that was just populated with hardware data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # pylint: disable=unused-variable
        _entity = node.data["hardware"]

        _model = self.tvwTreeView.get_model()

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["assembly"], 22, 22
        )

        if _entity.part == 1:
            # noinspection PyArgumentList
            _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self.dic_icons["part"], 22, 22
            )

        _attributes = [
            _entity.revision_id,
            _entity.hardware_id,
            _entity.alt_part_number,
            _entity.cage_code,
            _entity.comp_ref_des,
            _entity.cost,
            _entity.cost_failure,
            _entity.cost_hour,
            _entity.description,
            _entity.duty_cycle,
            _entity.figure_number,
            _entity.lcn,
            _entity.level,
            _entity.manufacturer_id,
            _entity.mission_time,
            _entity.name,
            _entity.nsn,
            _entity.page_number,
            _entity.parent_id,
            _entity.part,
            _entity.part_number,
            _entity.quantity,
            _entity.ref_des,
            _entity.remarks,
            _entity.repairable,
            _entity.specification_number,
            _entity.tagged_part,
            _entity.total_part_count,
            _entity.total_power_dissipation,
            _entity.year_of_manufacture,
            _entity.cost_type_id,
            _entity.attachments,
            _entity.category_id,
            _entity.subcategory_id,
            _icon,
        ]

        try:
            _new_row = _model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _new_row = None
            _message = _(
                "An error occurred when loading hardware item {0} into the "
                "hardware tree.  This might indicate it was missing it's data "
                "package, some of the data in the package was missing, or "
                "some of the data was the wrong type.  Row data was: "
                "{1}"
            ).format(str(node.identifier), _attributes)
            pub.sendMessage(
                "do_log_warning_msg",
                logger_name="WARNING",
                message=_message,
            )

        return _new_row


class HardwareGeneralDataPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Hardware item."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "hardware"
    _title = _("Hardware General Information")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware General Date panel."""
        super().__init__()

        # Initialize widgets.
        self.chkRepairable: RAMSTKCheckButton = RAMSTKCheckButton(label=_("Repairable"))
        self.cmbCategory: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbSubcategory: RAMSTKComboBox = RAMSTKComboBox()
        self.txtAltPartNum: RAMSTKEntry = RAMSTKEntry()
        self.txtCompRefDes: RAMSTKEntry = RAMSTKEntry()
        self.txtDescription: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtFigureNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtLCN: RAMSTKEntry = RAMSTKEntry()
        self.txtName: RAMSTKEntry = RAMSTKEntry()
        self.txtPageNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtPartNumber: RAMSTKEntry = RAMSTKEntry()
        self.txtRefDes: RAMSTKEntry = RAMSTKEntry()
        self.txtSpecification: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.
        self.dic_attribute_index_map = {
            2: ["alt_part_number", "string"],
            4: ["comp_ref_des", "string"],
            8: ["description", "string"],
            10: ["figure_number", "string"],
            11: ["lcn", "string"],
            15: ["name", "string"],
            17: ["page_number", "string"],
            20: ["part_number", "string"],
            22: ["ref_des", "string"],
            24: ["repairable", "boolean"],
            25: ["specification_number", "string"],
            32: ["category_id", "integer"],
            33: ["subcategory_id", "integer"],
        }
        self.dic_attribute_widget_map = {
            "ref_des": [
                22,
                self.txtRefDes,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The reference designator of the selected hardware item."
                    ),
                },
                _("Reference Designator:"),
            ],
            "comp_ref_des": [
                4,
                self.txtCompRefDes,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The composite reference designator of the selected hardware "
                        "item."
                    )
                },
                _("Composite Ref. Des."),
            ],
            "name": [
                15,
                self.txtName,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "width": 600,
                    "tooltip": _("The name of the selected hardware item."),
                },
                _("Name:"),
            ],
            "description": [
                8,
                self.txtDescription,
                "changed",
                super().on_changed_textview,
                "wvw_editing_hardware",
                "",
                {
                    "width": 600,
                    "tooltip": _("The description of the selected hardware item."),
                },
                _("Description:"),
            ],
            "part_number": [
                20,
                self.txtPartNumber,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "tooltip": _("The part number of the selected hardware item."),
                },
                _("Part Number:"),
            ],
            "alt_part_number": [
                2,
                self.txtAltPartNum,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The alternate part number (if any) of the selected hardware "
                        "item."
                    )
                },
                _("Alternate Part Number:"),
            ],
            "category_id": [
                32,
                self.cmbCategory,
                "changed",
                super().on_changed_combo,
                "wvw_editing_hardware",
                0,
                {},
                _("Category:"),
            ],
            "subcategory_id": [
                33,
                self.cmbSubcategory,
                "changed",
                super().on_changed_combo,
                "wvw_editing_hardware",
                0,
                {},
                _("Subcategory:"),
            ],
            "specification_number": [
                25,
                self.txtSpecification,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The specification (if any) governing the selected hardware "
                        "item."
                    ),
                },
                _("Specification:"),
            ],
            "page_number": [
                17,
                self.txtPageNumber,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The page number in the governing specification for the "
                        "selected hardware item."
                    )
                },
                _("Page Number:"),
            ],
            "figure_number": [
                10,
                self.txtFigureNumber,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The figure number in the governing specification for the "
                        "selected hardware item."
                    )
                },
                _("Figure Number:"),
            ],
            "lcn": [
                11,
                self.txtLCN,
                "changed",
                super().on_changed_entry,
                "wvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The Logistics Control Number (LCN) of the selected hardware "
                        "item."
                    )
                },
                _("LCN:"),
            ],
            "repairable": [
                24,
                self.chkRepairable,
                "toggled",
                super().on_toggled,
                "wvw_editing_hardware",
                0,
                {
                    "tooltip": _(
                        "Indicates whether or not the selected hardware item is "
                        "repairable."
                    )
                },
                "",
            ],
        }
        self.dicSubcategories: Dict[int, Dict[int, str]] = {}

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.cmbCategory.connect("changed", self._request_load_subcategories)
        self.cmbSubcategory.connect("changed", self._request_load_component)

        # Subscribe to PyPubSub messages.
        pub.subscribe(self._do_load_subcategories, "changed_category")

    def do_load_categories(self, category: Dict[int, str]) -> None:
        """Load the category RAMSTKComboBox().

        :param category: the dictionary of hardware categories to load.
        :return: None
        :rtype: None
        """
        _model = self.cmbCategory.get_model()
        _model.clear()

        _categories = []
        # pylint: disable=unused-variable
        for __, _key in enumerate(category):
            _categories.append([category[_key]])
        self.cmbCategory.do_load_combo(entries=_categories)

    def _do_load_subcategories(self, category_id: int) -> None:
        """Load the subcategory RAMSTKComboBox().

        :param category_id: the ID of the selected category.
        :return: None
        """
        _model = self.cmbSubcategory.get_model()
        _model.clear()

        if category_id > 0:
            _subcategories = SortedDict(self.dicSubcategories[category_id])
            _subcategory = []
            for _key in _subcategories:
                _subcategory.append([_subcategories[_key]])
            self.cmbSubcategory.do_load_combo(entries=_subcategory, signal="changed")

    def _request_load_component(self, combo: RAMSTKComboBox) -> None:
        """Request to load the component widgets.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        """
        pub.sendMessage("changed_subcategory", subcategory_id=combo.get_active())
        for _table in [
            "design_electric",
            "hardware",
            "reliability",
        ]:
            pub.sendMessage(
                "request_get_{}_attributes".format(_table),
                node_id=self._record_id,
            )

    def _request_load_subcategories(self, combo: RAMSTKComboBox) -> None:
        """Request to have the subcategory RAMSTKComboBox() loaded.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        """
        self._do_load_subcategories(category_id=combo.get_active())
        pub.sendMessage(
            "hardware_category_changed",
            attributes={
                "category_id": combo.get_active(),
            },
        )


class HardwareLogisticsPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Hardware task."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "hardware"
    _title = _("Hardware Logistics Information")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware Task Description panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbCostType: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbManufacturer: RAMSTKComboBox = RAMSTKComboBox(simple=False)
        self.txtCAGECode: RAMSTKEntry = RAMSTKEntry()
        self.txtCost: RAMSTKEntry = RAMSTKEntry()
        self.txtNSN: RAMSTKEntry = RAMSTKEntry()
        self.txtQuantity: RAMSTKEntry = RAMSTKEntry()
        self.txtYearMade: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_index_map = {
            3: ["cage_code", "string"],
            5: ["cost", "string"],
            13: ["manufacturer_id", "integer"],
            16: ["nsn", "string"],
            21: ["quantity", "integer"],
            29: ["year_of_manufacture", "string"],
            30: ["cost_type_id", "integer"],
        }
        self.dic_attribute_widget_map = {
            "manufacturer_id": [
                13,
                self.cmbManufacturer,
                "changed",
                super().on_changed_combo,
                "mvw_editing_hardware",
                0,
                {},
                _("Manufacturer:"),
            ],
            "cage_code": [
                3,
                self.txtCAGECode,
                "changed",
                super().on_changed_entry,
                "mvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The Commercial and Government Entity (CAGE) Code of the "
                        "selected hardware item."
                    ),
                },
                _("CAGE Code:"),
            ],
            "nsn": [
                16,
                self.txtNSN,
                "changed",
                super().on_changed_entry,
                "mvw_editing_hardware",
                "",
                {
                    "tooltip": _(
                        "The National Stock Number (NSN) of the selected hardware item."
                    )
                },
                _("NSN:"),
            ],
            "year_of_manufacture": [
                29,
                self.txtYearMade,
                "changed",
                super().on_changed_entry,
                "mvw_editing_hardware",
                date.today().year - 2,
                {
                    "width": 100,
                    "tooltip": _(
                        "The year the selected hardware item was introduced to "
                        "the market."
                    ),
                },
                _("Year Introduced:"),
            ],
            "quantity": [
                21,
                self.txtQuantity,
                "changed",
                super().on_changed_entry,
                "mvw_editing_hardware",
                1,
                {
                    "width": 50,
                    "tooltip": _(
                        "The number of the selected hardware items in the design."
                    ),
                },
                _("Quantity:"),
            ],
            "cost": [
                5,
                self.txtCost,
                "changed",
                super().on_changed_entry,
                "mvw_editing_hardware",
                0.0,
                {},
                _("Unit Cost:"),
            ],
            "cost_type_id": [
                30,
                self.cmbCostType,
                "changed",
                super().on_changed_combo,
                "mvw_editing_hardware",
                0,
                {},
                _("Cost Method:"),
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.cmbManufacturer.connect("changed", self._do_load_cage_code)

        # Subscribe to PyPubSub messages.

    def do_load_cost_types(self) -> None:
        """Load the category RAMSTKComboBox().

        :return: None
        """
        self.cmbCostType.do_load_combo([["Assessed"], ["Specified"]])

    def do_load_manufacturers(
        self, manufacturers: Dict[int, Tuple[str, str, str]]
    ) -> None:
        """Load the manufacturer RAMSTKComboBox().

        :param manufacturers: the dictionary with manufacturer information.
            The key is the index from the database table.  The value is a tuple
            with the manufacturer's name, office location, and CAGE code.  An
            example might be:

            ('Sprague', 'New Hampshire', '13606')

        :return: None
        """
        _manufacturer = []
        for _key in manufacturers:
            _manufacturer.append(manufacturers[_key])
        self.cmbManufacturer.do_load_combo(entries=_manufacturer, simple=False)

    def _do_load_cage_code(self, combo: RAMSTKComboBox) -> None:
        """Load the CAGE code whenever the manufacturer is changed.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        :rtype: None
        """
        _model = combo.get_model()
        _row = combo.get_active_iter()

        try:
            _cage_code = str(str(_model.get(_row, 2)[0]))
        except TypeError:
            _cage_code = ""

        self.txtCAGECode.do_update(_cage_code, signal="changed")
        pub.sendMessage(
            "wvw_editing_hardware",
            node_id=[self._record_id, -1],
            package={"cage_code": _cage_code},
        )


class HardwareMiscellaneousPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Hardware task."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "hardware"
    _title = _("Hardware Miscellaneous Information")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware Task Description panel."""
        super().__init__()

        # Initialize widgets.
        self.chkTagged: RAMSTKCheckButton = RAMSTKCheckButton(label=_("Tagged Part"))
        self.txtAttachments: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())
        self.txtRemarks: RAMSTKTextView = RAMSTKTextView(Gtk.TextBuffer())

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.
        self.dic_attribute_index_map = {
            23: ["remarks", "string"],
            26: ["tagged_part", "boolean"],
            31: ["attachments", "string"],
        }
        self.dic_attribute_widget_map = {
            "attachments": [
                31,
                self.txtAttachments,
                "changed",
                super().on_changed_textview,
                "mvw_editing_hardware",
                "",
                {
                    "height": 150,
                    "width": 600,
                    "tooltip": _(
                        "Hyperlinks to any documents associated with the selected "
                        "hardware item."
                    ),
                },
                _("Attachments:"),
            ],
            "remarks": [
                23,
                self.txtRemarks,
                "changed",
                super().on_changed_textview,
                "mvw_editing_hardware",
                "",
                {
                    "height": 150,
                    "width": 600,
                    "tooltip": _(
                        "Enter any remarks associated with the selected hardware item."
                    ),
                },
                _("Remarks:"),
            ],
            "tagged_part": [
                26,
                self.chkTagged,
                "toggled",
                super().on_toggled,
                "mvw_editing_hardware",
                0,
                {},
                "",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Make a fixed type panel.
        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
