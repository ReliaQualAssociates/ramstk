# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Hardware Panels."""

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import GdkPixbuf, Gtk, _
from ramstk.views.gtk3.widgets import RAMSTKTreePanel


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
        self.dic_attribute_index_map = {
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
        self.dic_attribute_widget_map = {
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
            _code = _model.get_value(_row, self._lst_col_order[5])
            _name = _model.get_value(_row, self._lst_col_order[15])
            _title = _("Analyzing Hardware item {0:s}: {1:s}").format(
                str(_code), str(_name)
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
                "request_get_all_hardware_attributes",
                node_id=self._record_id,
            )
            pub.sendMessage(
                "request_set_title",
                title=_title,
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
