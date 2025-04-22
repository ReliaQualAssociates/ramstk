# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.tree_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Hardware tree panel module."""

# Standard Library Imports
from datetime import date
from typing import Dict, List, Tuple, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCellRendererCombo,
    RAMSTKCellRendererText,
    RAMSTKCellRendererToggle,
    RAMSTKTreePanel,
    WidgetConfig,
    make_widget_config,
)


class HardwareTreePanel(RAMSTKTreePanel):
    """Panel to display the hierarchy of hardware (a.k.a., bill of materials)."""

    # Define private class attributes.
    _record_field = "hardware_id"
    _select_msg = "succeed_retrieve_all_hardware"
    _tag = "hardware"
    _title = _("Hardware BoM")

    def __init__(self) -> None:
        """Initialize an instance of the Hardware panel."""
        super().__init__()

        # Initialize private instance attributes.
        self._lst_cost_types: List[str] = ["", "Assessed", "Specified"]
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "revision_id",
                    "index": 0,
                    "label_text": _("Revision ID"),
                    "listen_topic": "wvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "hardware_id",
                    "index": 1,
                    "label_text": _("Hardware ID"),
                    "listen_topic": "wvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "alt_part_number",
                    "index": 2,
                    "label_text": _("Alt. Part Num."),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "cage_code",
                    "index": 3,
                    "label_text": _("CAGE Code"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "comp_ref_des",
                    "index": 4,
                    "label_text": _("Comp. Ref. Des."),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost",
                    "index": 5,
                    "label_text": _("Cost"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_per_failure",
                    "index": 6,
                    "label_text": _("Cost/Failure"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "cost_hour",
                    "index": 7,
                    "label_text": _("Cost/Hour"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 8,
                    "label_text": _("Description"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 100.0,
                    "field": "duty_cycle",
                    "index": 9,
                    "label_text": _("Duty Cycle"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "figure_number",
                    "index": 10,
                    "label_text": _("Figure Number"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "lcn",
                    "index": 11,
                    "label_text": "LCN",
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "level",
                    "index": 12,
                    "label_text": _("Level"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "manufacturer_id",
                    "index": 13,
                    "label_text": _("Manufacturer"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 1.0,
                    "field": "mission_time",
                    "index": 14,
                    "label_text": _("Mission Time"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "name",
                    "index": 15,
                    "label_text": _("Name"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "nsn",
                    "index": 16,
                    "label_text": "NSN",
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "page_number",
                    "index": 17,
                    "label_text": _("Page Number"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "parent_id",
                    "index": 18,
                    "label_text": _("Parent ID"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "part",
                    "index": 19,
                    "label_text": _("Part?"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "part_number",
                    "index": 20,
                    "label_text": _("Part Number"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "quantity",
                    "index": 21,
                    "label_text": _("Quantity"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "ref_des",
                    "index": 22,
                    "label_text": _("Ref. Des."),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "Remarks",
                    "index": 23,
                    "label_text": _("Remarks"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "repairable",
                    "index": 24,
                    "label_text": _("Repairable"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "specification_number",
                    "index": 25,
                    "label_text": _("Specification"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererToggle(),
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "tagged_part",
                    "index": 26,
                    "label_text": _("Tagged Part"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": 1,
                    "field": "total_part_count",
                    "index": 27,
                    "label_text": _("Part Count"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gfloat",
                    "default": 0.0,
                    "field": "total_power_dissipation",
                    "index": 28,
                    "label_text": _("Power Dissipation"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gint",
                    "default": date.today().year,
                    "field": "year_of_manufacture",
                    "index": 29,
                    "label_text": _("Year of Manufacture"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "cost_type_id",
                    "index": 30,
                    "label_text": _("Cost Type"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "attachments",
                    "index": 31,
                    "label_text": _("Attachments"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": False,
                    "visible": False,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererCombo(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "category_id",
                    "index": 32,
                    "label_text": _("Category"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
            make_widget_config(
                RAMSTKCellRendererText(),
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "subcategory_id",
                    "index": 33,
                    "label_text": _("Subcategory"),
                    "listen_topic": "wvw_editing_hardware",
                    "send_topic": "mvw_editing_hardware",
                },
                {
                    "editable": True,
                    "visible": True,
                },
            ),
        ]
        self._category_id: int = 0

        # Initialize public instance attributes.
        self.dic_icons = {"assembly": "", "part": ""}
        self.dic_subcategories: Dict[int, List[str]] = {0: [""]}
        self.lst_categories: List[str] = [""]
        self.lst_manufacturers: List[str] = [""]
        self.part: int = 0

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_tree_panel()
        super().do_set_widget_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _("Displays the hierarchical list of hardware.")
        )
        self.tvwTreeView.dic_row_loader = {
            "hardware": self.__do_load_hardware,
        }

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "mvwSwitchedPage": self._on_module_switch,
                f"wvw_editing_{self._tag}": self._on_workview_edit,
            }
        )

    # ----- ----- RAMSTKTreePanel specific methods. ----- ----- #
    def _on_module_switch(self, module: str = "") -> None:
        """Respond to change in selected Module View module (tab).

        :param module: the name of the module that was just selected.
        """
        # FIXME: This method needs to use something other than the position dict of
        #  the RAMSTKTreeView class to get the column numbers.
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
        """Handle events for the Hardware package Module View RAMSTKTreeView.

        This method is called whenever a Hardware Module View RAMSTKTreeView row is
        activated/changed.

        :param selection: the Hardware class Gtk.TreeSelection.
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            # FIXME: Can we move setting the record ID and parent ID to the super class?
            self._record_id = _attributes["hardware_id"]
            self._parent_id = _attributes["parent_id"]
            self.part = _attributes["part"]

            _attributes["category_id"] = self.lst_categories.index(
                _attributes["category_id"]
            )
            self._category_id = _attributes["category_id"]

            _attributes["cost_type_id"] = self._lst_cost_types.index(
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

            super().do_set_title(_title)

            # FIXME: Is this the best way to do this?  Look into changing this when
            #  refactoring the reliability, design_electric, and milhdbk217f modules.
            # We need the reliability attributes to be requested first so the
            # component panels will get reliability attributes first.  Some reliability
            # attributes control widget sensitivity on the component panels.
            for _table in [
                "reliability",
                "design_electric",
                "milhdbk217f",
            ]:
                pub.sendMessage(
                    f"request_get_{_table}_attributes",
                    node_id=self._record_id,
                )

    # ----- -- HardwareTreePanel specific methods. --- ----- #
    def do_load_categories(
        self,
        categories: Dict[int, Tuple[str]],
        subcategories: Dict[int, Dict[int, Tuple[str]]],
    ) -> None:
        """Load the categories into the RAMSTKTreeView.

        :param categories: the list of categories to load into the RAMSTKTreeView.
        :param subcategories: the list of subcategories to load into the RAMSTKTreeView.
        """
        for _category in categories.keys():
            self.lst_categories.append(categories[_category][0])
            self.do_load_subcategories(_category, subcategories)

        self.tvwTreeView.do_load_cellrenderercombo("category_id", self.lst_categories)

        # FIXME: Need to use something other than the RAMSTKTreeView.position to find
        #  the correct index.
        # _cell = self.tvwTreeView.get_column(
        #    self.tvwTreeView.position["category_id"]
        # ).get_cells()
        # _cell[0].connect("edited", self._on_category_change)

    def do_load_cost_types(self) -> None:
        """Load the cost types into the RAMSTKTreeView."""
        self.tvwTreeView.do_load_cellrenderercombo("cost_type_id", self._lst_cost_types)

    def do_load_manufacturers(
        self,
        manufacturers: Dict[int, Tuple[str, str, str]],
    ) -> None:
        """Load the manufacturers into the RAMSTKTreeView.

        :param manufacturers: the list of manufacturers to load into the RAMSTKTreeView.
        """
        for _manufacturer in manufacturers:
            self.lst_manufacturers.append(manufacturers[_manufacturer][0])

        self.tvwTreeView.do_load_cellrenderercombo(
            "manufacturer_id",
            self.lst_manufacturers,
        )

    def do_load_subcategories(
        self, category: int, subcategories: Dict[int, Dict[int, Tuple[str]]]
    ) -> None:
        """Load the subcategories into the RAMSTKTreeView.

        :param category: the category to load the subcategories into.
        :param subcategories: the list of subcategories to load into the RAMSTKTreeView.
        """
        # TODO: This may need to be changed so the subcategory ID's in
        #  dic_subcategories always start at 1 for each category.
        self.dic_subcategories[category] = [""]
        for _subcategory in subcategories[category].keys():
            self.dic_subcategories[category].append(
                subcategories[category][_subcategory][0]
            )

    def _on_workview_edit(
        self, node_id: int, package: Dict[str, Union[bool, float, int, str]]
    ) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

        This is a wrapper for the metaclass method do_refresh_tree().  It is necessary
        to handle RAMSTKComboBox() changes because the package value will be an integer
        and the Gtk.CellRendererCombo() needs a string input to update.

        :param node_id: the ID of the hardware item being edited.
        :param package: the key:value for the data being updated.
        """
        for _key, _value in package.items():
            _column = self.tvwTreeView.get_column(self.tvwTreeView.position[_key])
            _cell = _column.get_cells()[-1]

            if isinstance(_cell, RAMSTKCellRendererCombo) and isinstance(_value, int):
                if _key == "manufacturer_id":
                    package[_key] = self.lst_manufacturers[_value]
                elif _key == "cost_type_id":
                    package[_key] = self._lst_cost_types[_value]
                elif _key == "category_id":
                    package[_key] = self.lst_categories[_value]
                elif _key == "subcategory_id":
                    package[_key] = self.dic_subcategories[self._category_id][_value]

            super().do_refresh_tree(node_id, package)

    def _on_category_change(
        self, __combo: RAMSTKCellRendererCombo, path: str, new_text: str
    ) -> None:
        """Load the subcategories whenever the category combo is changed.

        :param __combo: the category list RAMSTKCellRendererCombo(). Unused in this
            method.
        :param path: the path identifying the edited cell.
        :param new_text: the new text (category description).
        """
        self.__do_load_subcategories(new_text)

        _model = self.tvwTreeView.get_model()
        _model[path][self.tvwTreeView.position["subcategory_id"]] = ""

    def __do_load_hardware(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a hardware item into the RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the item to load into the hardware tree.
        :return: _new_row; the row that was just populated with hardware data.
        :rtype: :class:`Gtk.TreeIter`
        """
        # FIXME: This method needs to accept a treelib.Tree object with all the
        #  requirements and then pass that tree to the treeview method do_load_tree.
        #  This method should handle all exceptions and return None.
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
        except (AttributeError, TypeError, ValueError) as exc:
            _message = _(
                f"An error occurred when loading hardware item {node.identifier} "
                f"into the hardware tree.  Row data was: {_attributes}.  Exception "
                f"{exc}."
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
        """
        _category_id = self.lst_categories.index(category)

        self.tvwTreeView.do_load_cellrenderercombo(
            "subcategory_id", self.dic_subcategories[_category_id]
        )
