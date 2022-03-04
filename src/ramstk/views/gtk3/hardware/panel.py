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
    _lst_cost_types: List[str] = ["", "Assessed", "Specified"]

    # Define private scalar class attributes.
    _record_field = "hardware_id"
    _select_msg = "succeed_retrieve_all_hardware"
    _tag = "hardware"
    _title = _("Hardware BoM")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware panel."""
        super().__init__()

        # Initialize private dictionary class attributes.
        self.tvwTreeView.dic_row_loader = {
            "hardware": self.__do_load_hardware,
        }

        # Initialize private list class attributes.

        # Initialize private scalar class attributes.
        self._category_id: int = 0

        # Initialize public dictionary class attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Revision ID"),
                "gint",
            ],
            "hardware_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Hardware ID"),
                "gint",
            ],
            "alt_part_number": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Alt. Part Num."),
                "gchararray",
            ],
            "cage_code": [
                3,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("CAGE Code"),
                "gchararray",
            ],
            "comp_ref_des": [
                4,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Comp. Ref. Des."),
                "gchararray",
            ],
            "cost": [
                5,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Cost"),
                "gfloat",
            ],
            "cost_failure": [
                6,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Cost/Failure"),
                "gfloat",
            ],
            "cost_hour": [
                7,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Cost/Hour"),
                "gfloat",
            ],
            "description": [
                8,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Description"),
                "gchararray",
            ],
            "duty_cycle": [
                9,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Duty Cycle"),
                "gfloat",
            ],
            "figure_number": [
                10,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Figure Number"),
                "gchararray",
            ],
            "lcn": [
                11,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("LCN"),
                "gchararray",
            ],
            "level": [
                12,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Level"),
                "gint",
            ],
            "manufacturer_id": [
                13,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Manufacturer"),
                "gchararray",
            ],
            "mission_time": [
                14,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Mission Time"),
                "gfloat",
            ],
            "name": [
                15,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Name"),
                "gchararray",
            ],
            "nsn": [
                16,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("NSN"),
                "gchararray",
            ],
            "page_number": [
                17,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Page Number"),
                "gchararray",
            ],
            "parent_id": [
                18,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Parent ID"),
                "gint",
            ],
            "part": [
                19,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Part?"),
                "gint",
            ],
            "part_number": [
                20,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Part Number"),
                "gchararray",
            ],
            "quantity": [
                21,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Quantity"),
                "gint",
            ],
            "ref_des": [
                22,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Ref. Des."),
                "gchararray",
            ],
            "remarks": [
                23,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Remarks"),
                "gchararray",
            ],
            "repairable": [
                24,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                f"mvw_editing_{self._tag}",
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Repairable?"),
                "gint",
            ],
            "specification_number": [
                25,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Specification"),
                "gchararray",
            ],
            "tagged_part": [
                26,
                Gtk.CellRendererToggle(),
                "toggled",
                None,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Tagged Part"),
                "gint",
            ],
            "total_part_count": [
                27,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Part Count"),
                "gint",
            ],
            "total_power_dissipation": [
                28,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Power Dissipation"),
                "gfloat",
            ],
            "year_of_manufacture": [
                29,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                date.today(),
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Year of Manufacture"),
                "gint",
            ],
            "cost_type_id": [
                30,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Cost Type"),
                "gchararray",
            ],
            "attachments": [
                31,
                Gtk.CellRendererText(),
                "edited",
                None,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Attachments"),
                "gchararray",
            ],
            "category_id": [
                32,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Category"),
                "gchararray",
            ],
            "subcategory_id": [
                33,
                Gtk.CellRendererCombo(),
                "changed",
                super().on_cell_change,
                f"mvw_editing_{self._tag}",
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Subcategory"),
                "gchararray",
            ],
        }
        self.dic_icons = {"assembly": None, "part": None}
        self.dic_subcategories: Dict[int, List[str]] = {0: [""]}

        # Initialize public list class attributes.
        self.lst_categories: List[str] = [""]
        self.lst_manufacturers: List[str] = [""]

        # Initialize public scalar class attributes.
        self.part: int = 0

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of hardware.")
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._on_module_switch,
            "mvwSwitchedPage",
        )
        pub.subscribe(
            self._on_workview_edit,
            f"wvw_editing_{self._tag}",
        )

    def do_load_comboboxes(self) -> None:
        """Load the Gtk.CellRendererCombo()s.

        :return: None
        :rtype: None
        """
        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["category_id"],
            self.lst_categories,
        )

        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["manufacturer_id"],
            self.lst_manufacturers,
        )

        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["cost_type_id"],
            self._lst_cost_types,
        )

        _cell = self.tvwTreeView.get_column(
            self.tvwTreeView.position["category_id"]
        ).get_cells()
        _cell[0].connect("edited", self._on_category_change)

    def _on_category_change(
        self, __combo: Gtk.CellRendererCombo, path: str, new_text: str
    ) -> None:
        """Load the subcategories whenever the category combo is changed.

        :param __combo: the category list Gtk.CellRendererCombo().  Unused in
            this method.
        :param path: the path identifying the edited cell.
        :param new_text: the new text (category description).
        :return: None
        :rtype: None
        """
        self.__do_load_subcategories(new_text)

        _model = self.tvwTreeView.get_model()
        _model[path][self.tvwTreeView.position["subcategory_id"]] = ""

    def _on_module_switch(self, module: str = "") -> None:
        """Respond to change in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        if module == self._tag and _row is not None:
            _comprefdes = _model.get_value(
                _row, self.tvwTreeView.position["comp_ref_des"]
            )
            _name = _model.get_value(_row, self.tvwTreeView.position["name"])
            _title = _(f"Analyzing Hardware item {_comprefdes}: {_name}")

            pub.sendMessage(
                "request_set_title",
                title=_title,
            )

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
            self.part = _attributes["part"]

            _attributes["category_id"] = self.lst_categories.index(
                _attributes["category_id"]
            )
            self._category_id = _attributes["category_id"]

            _attributes["cost_type_id"] = ["", "Assessed", "Specified"].index(
                _attributes["cost_type_id"]
            )
            _attributes["manufacturer_id"] = self.lst_manufacturers.index(
                _attributes["manufacturer_id"]
            )
            _attributes["subcategory_id"] = self.dic_subcategories[
                _attributes["category_id"]
            ].index(_attributes["subcategory_id"])

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

            # We need the reliability attributes to be requested first so the
            # component panels will get reliability attributes first.  Some of the
            # reliability attributes control widget sensitivity on the component panels.
            for _table in [
                "reliability",
                "design_electric",
                "milhdbk217f",
            ]:
                pub.sendMessage(
                    f"request_get_{_table}_attributes",
                    node_id=self._record_id,
                )

    def _on_workview_edit(self, node_id: int, package: Dict[str, Any]) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

        This is a wrapper for the metaclass method do_refresh_tree().  It is
        necessary to handle RAMSTKComboBox() changes because the package value will
        be an integer and the Gtk.CellRendererCombo() needs a string input to update.

        :param node_id: the ID of the hardware item being edited.
        :param package: the key:value for the data being updated.
        :return: None
        """
        [[_key, _value]] = package.items()

        _column = self.tvwTreeView.get_column(self.tvwTreeView.position[_key])
        _cell = _column.get_cells()[-1]

        if isinstance(_cell, Gtk.CellRendererCombo):
            if _key == "manufacturer_id":
                package[_key] = self.lst_manufacturers[_value]
            elif _key == "cost_type_id":
                package[_key] = self._lst_cost_types[_value]
            elif _key == "category_id":
                package[_key] = self.lst_categories[_value]
            elif _key == "subcategory_id":
                package[_key] = self.dic_subcategories[self._category_id][_value]

            super().do_refresh_tree(node_id, package)

    def __do_load_hardware(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a hardware item into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the item to load into the hardware tree.
        :return: _new_row; the row that was just populated with hardware data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        # pylint: disable=unused-variable
        _entity = node.data["hardware"]

        # noinspection PyArgumentList
        _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
            self.dic_icons["assembly"], 22, 22
        )

        if _entity.part == 1:
            # noinspection PyArgumentList
            _icon = GdkPixbuf.Pixbuf.new_from_file_at_size(
                self.dic_icons["part"], 22, 22
            )

        self._category_id = _entity.category_id

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
            self.lst_manufacturers[_entity.manufacturer_id],
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
            self._lst_cost_types[_entity.cost_type_id],
            _entity.attachments,
            self.lst_categories[self._category_id],
            self.dic_subcategories[self._category_id][_entity.subcategory_id],
            _icon,
        ]

        try:
            _new_row = self.tvwTreeView.unfilt_model.append(row, _attributes)
        except (AttributeError, TypeError, ValueError):
            _message = _(
                f"An error occurred when loading hardware item {node.identifier} into "
                f"the hardware tree.  This might indicate it was missing it's data "
                f"package, some of the data in the package was missing, or "
                f"some of the data was the wrong type.  Row data was: "
                f"{_attributes}"
            )
            pub.sendMessage(
                "do_log_warning_msg",
                logger_name="WARNING",
                message=_message,
            )

        return _new_row

    def __do_load_subcategories(self, category: str) -> None:
        """Load subcategory Gtk.CellRendererCombo() when a new category is selected.

        :param category: the ID of the newly selected category.
        :return: None
        :rtype: None
        """
        _category_id = self.lst_categories.index(category)

        self.tvwTreeView.do_load_combo_cell(
            self.tvwTreeView.position["subcategory_id"],
            self.dic_subcategories[_category_id],
        )


class HardwareGeneralDataPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Hardware item."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "hardware_id"
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
        self.dic_attribute_widget_map = {
            "ref_des": [
                22,
                self.txtRefDes,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The reference designator of the selected hardware item."
                    ),
                },
                _("Reference Designator:"),
                "gchararray",
            ],
            "comp_ref_des": [
                4,
                self.txtCompRefDes,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The composite reference designator of the selected hardware "
                        "item."
                    )
                },
                _("Composite Ref. Des."),
                "gchararray",
            ],
            "name": [
                15,
                self.txtName,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "width": 600,
                    "tooltip": _("The name of the selected hardware item."),
                },
                _("Name:"),
                "gchararray",
            ],
            "description": [
                8,
                self.txtDescription,
                "changed",
                super().on_changed_textview,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "width": 600,
                    "tooltip": _("The description of the selected hardware item."),
                },
                _("Description:"),
                "gchararray",
            ],
            "part_number": [
                20,
                self.txtPartNumber,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _("The part number of the selected hardware item."),
                },
                _("Part Number:"),
                "gchararray",
            ],
            "alt_part_number": [
                2,
                self.txtAltPartNum,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The alternate part number (if any) of the selected hardware "
                        "item."
                    )
                },
                _("Alternate Part Number:"),
                "gchararray",
            ],
            "category_id": [
                32,
                self.cmbCategory,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {},
                _("Category:"),
                "gint",
            ],
            "subcategory_id": [
                33,
                self.cmbSubcategory,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {},
                _("Subcategory:"),
                "gint",
            ],
            "specification_number": [
                25,
                self.txtSpecification,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The specification (if any) governing the selected hardware "
                        "item."
                    ),
                },
                _("Specification:"),
                "gchararray",
            ],
            "page_number": [
                17,
                self.txtPageNumber,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The page number in the governing specification for the "
                        "selected hardware item."
                    )
                },
                _("Page Number:"),
                "gchararray",
            ],
            "figure_number": [
                10,
                self.txtFigureNumber,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The figure number in the governing specification for the "
                        "selected hardware item."
                    )
                },
                _("Figure Number:"),
                "gchararray",
            ],
            "lcn": [
                11,
                self.txtLCN,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The Logistics Control Number (LCN) of the selected hardware "
                        "item."
                    )
                },
                _("LCN:"),
                "gchararray",
            ],
            "repairable": [
                24,
                self.chkRepairable,
                "toggled",
                super().on_toggled,
                f"wvw_editing_{self._tag}",
                0,
                {
                    "tooltip": _(
                        "Indicates whether or not the selected hardware item is "
                        "repairable."
                    )
                },
                "",
                "gint",
            ],
        }
        self.dicSubcategories: Dict[int, Dict[int, str]] = {}

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.cmbCategory.connect(
            "changed",
            self._request_load_subcategories,
        )
        self.cmbSubcategory.connect(
            "changed",
            self._request_load_component,
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._do_load_subcategories,
            "changed_category",
        )
        pub.subscribe(
            self._do_set_comp_ref_des,
            "succeed_make_comp_ref_des",
        )

    def do_load_categories(self, category: Dict[int, str]) -> None:
        """Load the category RAMSTKComboBox().

        :param category: the dictionary of hardware categories to load.
        :return: None
        :rtype: None
        """
        _model = self.cmbCategory.get_model()
        _model.clear()

        _categories = [[value] for value in category.values()]
        self.cmbCategory.do_load_combo(entries=_categories)  # type: ignore

    def _do_load_subcategories(self, category_id: int) -> None:
        """Load the subcategory RAMSTKComboBox().

        :param category_id: the ID of the selected category.
        :return: None
        """
        _model = self.cmbSubcategory.get_model()
        _model.clear()

        if category_id > 0:
            _subcategories = SortedDict(self.dicSubcategories[category_id])
            _subcategory = [[_subcategories[_key]] for _key in _subcategories]
            self.cmbSubcategory.do_load_combo(entries=_subcategory, signal="changed")

    def _do_set_comp_ref_des(self, comp_ref_des: str) -> None:
        """Set the value in the composite reference designator RAMSTKEntry().

        :param comp_ref_des: the composite reference designator value.
        :return: None
        :rtype: None
        """
        self.txtCompRefDes.do_update(
            comp_ref_des,
            signal="changed",
        )

    def _request_load_component(self, combo: RAMSTKComboBox) -> None:
        """Request to load the component widgets.

        :param combo: the RAMSTKComboBox() that called this method.
        :return: None
        """
        pub.sendMessage(
            "wvw_editing_hardware",
            node_id=self._record_id,
            package={
                "subcategory_id": combo.get_active(),
            },
        )
        pub.sendMessage(
            "changed_subcategory",
            subcategory_id=combo.get_active(),
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
    _record_field = "hardware_id"
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
        self.dic_attribute_widget_map = {
            "manufacturer_id": [
                13,
                self.cmbManufacturer,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {},
                _("Manufacturer:"),
                "gint",
            ],
            "cage_code": [
                3,
                self.txtCAGECode,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The Commercial and Government Entity (CAGE) Code of the "
                        "selected hardware item."
                    ),
                },
                _("CAGE Code:"),
                "gchararray",
            ],
            "nsn": [
                16,
                self.txtNSN,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                "",
                {
                    "tooltip": _(
                        "The National Stock Number (NSN) of the selected hardware item."
                    )
                },
                _("NSN:"),
                "gchararray",
            ],
            "year_of_manufacture": [
                29,
                self.txtYearMade,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                date.today().year - 2,
                {
                    "width": 100,
                    "tooltip": _(
                        "The year the selected hardware item was introduced to "
                        "the market."
                    ),
                },
                _("Year Introduced:"),
                "gchararray",
            ],
            "quantity": [
                21,
                self.txtQuantity,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                1,
                {
                    "width": 50,
                    "tooltip": _(
                        "The number of the selected hardware items in the design."
                    ),
                },
                _("Quantity:"),
                "gint",
            ],
            "cost": [
                5,
                self.txtCost,
                "changed",
                super().on_changed_entry,
                f"wvw_editing_{self._tag}",
                0.0,
                {},
                _("Unit Cost:"),
                "gfloat",
            ],
            "cost_type_id": [
                30,
                self.cmbCostType,
                "changed",
                super().on_changed_combo,
                f"wvw_editing_{self._tag}",
                0,
                {},
                _("Cost Method:"),
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

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
        _manufacturer = list(manufacturers.values())
        self.cmbManufacturer.do_load_combo(
            entries=_manufacturer,  # type: ignore
            simple=False,
        )

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
            f"wvw_editing_{self._tag}",
            node_id=self._record_id,
            package={"cage_code": _cage_code},
        )


class HardwareMiscellaneousPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Hardware task."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "hardware_id"
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
        self.dic_attribute_widget_map = {
            "attachments": [
                31,
                self.txtAttachments,
                "changed",
                super().on_changed_textview,
                f"mvw_editing_{self._tag}",
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
                "gchararray",
            ],
            "remarks": [
                23,
                self.txtRemarks,
                "changed",
                super().on_changed_textview,
                f"mvw_editing_{self._tag}",
                "",
                {
                    "height": 150,
                    "width": 600,
                    "tooltip": _(
                        "Enter any remarks associated with the selected hardware item."
                    ),
                },
                _("Remarks:"),
                "gchararray",
            ],
            "tagged_part": [
                26,
                self.chkTagged,
                "toggled",
                super().on_toggled,
                f"mvw_editing_{self._tag}",
                0,
                {},
                "",
                "gint",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        # Subscribe to PyPubSub messages.
