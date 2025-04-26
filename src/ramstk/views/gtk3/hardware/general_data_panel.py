# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.hardware.general_data_panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The HardwareGeneralDataPanel module."""

# Standard Library Imports
from typing import Dict, List, Tuple

# Third Party Imports
from pubsub import pub

# noinspection PyPackageRequirements
from sortedcontainers import SortedDict

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKCheckButton,
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTextView,
    WidgetConfig,
    make_widget_config,
)


class HardwareGeneralDataPanel(RAMSTKFixedPanel):
    """Panel to display general data about the selected Hardware item."""

    # Define private class attributes.
    _record_field = "hardware_id"
    _select_msg = "selected_hardware"
    _tag = "hardware"
    _title = _("Hardware General Information")

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

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.txtRefDes,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "ref_des",
                    "index": 22,
                    "label_text": _("Reference Designator:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The reference designator of the selected hardware item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtCompRefDes,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "comp_ref_des",
                    "index": 4,
                    "label_text": _("Composite Ref. Des.:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The composite reference designator of the selected hardware "
                        "item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtName,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "name",
                    "index": 15,
                    "label_text": _("Name:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _("The name of the selected hardware item."),
                    "visible": True,
                    "width_request": 600,
                },
            ),
            make_widget_config(
                self.txtDescription,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "description",
                    "index": 8,
                    "label_text": _("Description:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _("The description of the selected hardware item."),
                    "visible": True,
                    "width_request": 600,
                },
            ),
            make_widget_config(
                self.txtPartNumber,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "part_number",
                    "index": 20,
                    "label_text": _("Part Number:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _("The part number of the selected hardware item."),
                    "visible": True,
                    "width_request": 600,
                },
            ),
            make_widget_config(
                self.txtAltPartNum,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "alt_part_number",
                    "index": 2,
                    "label_text": _("Alternate Part Number:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _("The part number of the selected hardware item."),
                    "visible": True,
                    "width_request": 600,
                },
            ),
            make_widget_config(
                self.cmbCategory,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "category_id",
                    "index": 32,
                    "label_text": _("Part Category:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The hazard rate model category of the selected hardware item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.cmbSubcategory,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "subcategory_id",
                    "index": 33,
                    "label_text": _("Part Subcategory:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The hazard rate model subcategory of the selected hardware "
                        "item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtSpecification,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "specification_number",
                    "index": 25,
                    "label_text": _("Specification:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The specification (if any) governing the selected hardware "
                        "item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtPageNumber,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "page_number",
                    "index": 17,
                    "label_text": _("Page Number:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The page number in the governing specification for the "
                        "selected hardware item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtFigureNumber,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "figure_number",
                    "index": 25,
                    "label_text": _("Figure Number:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The figure number in the governing specification for the "
                        "selected hardware item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.txtLCN,
                {
                    "datatype": "gchararray",
                    "default": "",
                    "field": "lcn",
                    "index": 11,
                    "label_text": _("LCN:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "The Logistics Control Number (LCN) of the selected hardware "
                        "item."
                    ),
                    "visible": True,
                },
            ),
            make_widget_config(
                self.chkRepairable,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "repairable",
                    "index": 24,
                    "label_text": _("Repairable:"),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _(
                        "Indicates whether or not the selected hardware item is "
                        "repairable."
                    ),
                    "visible": True,
                },
            ),
        ]

        # Initialize public instance attributes.
        self.dicSubcategories: Dict[int, Dict[int, str]] = {}

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        self._do_set_widget_callbacks()

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "request_load_categories": self.do_load_categories,
                "changed_category": self._do_load_subcategories,
                "succeed_make_comp_ref_des": self._do_set_comp_ref_des,
            }
        )

    # ----- ----- HardwareGeneralDataPanel specific methods. ----- ----- #
    def do_load_categories(self, category: Dict[int, Tuple[str]]) -> None:
        """Load the category RAMSTKComboBox.

        :param category: the dictionary of hardware categories to load.
        """
        self.cmbCategory.get_model().clear()

        _categories = [[value[0]] for value in category.values()]
        self.cmbCategory.do_load_combo(_categories)

    def _do_load_subcategories(self, category_id: int) -> None:
        """Load the subcategory RAMSTKComboBox.

        :param category_id: the ID of the selected category.
        """
        self.cmbSubcategory.get_model().clear()

        if category_id > 0:
            _subcategories = SortedDict(self.dicSubcategories[category_id])
            _subcategory = [[_subcategories[_key]][0] for _key in _subcategories]
            self.cmbSubcategory.do_load_combo(_subcategory)

    def _do_set_comp_ref_des(self, comp_ref_des: str) -> None:
        """Set the value in the composite reference designator RAMSTKEntry.

        :param comp_ref_des: the composite reference designator value.
        """
        self.txtCompRefDes.do_update({"comp_ref_des": comp_ref_des})

    def _do_set_widget_callbacks(self) -> None:
        """Set the callback methods for the widgets on the HardwareGeneralDataPanel."""
        super().do_set_widget_callbacks()

        self.cmbCategory.connect(
            "changed",
            self._request_load_subcategories,
        )
        self.cmbSubcategory.connect(
            "changed",
            self._request_load_component,
        )

    def _request_load_component(self, combo: RAMSTKComboBox) -> None:
        """Request to load the component widgets.

        :param combo: the RAMSTKComboBox that called this method.
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
        """Request to have the subcategory RAMSTKComboBox loaded.

        :param combo: the RAMSTKComboBox that called this method.
        """
        self._category_id = (  # pylint: disable=attribute-defined-outside-init
            combo.get_active()
        )

        self._do_load_subcategories(category_id=self._category_id)
        pub.sendMessage(
            "hardware_category_changed",
            attributes={"category_id": self._category_id},
        )
