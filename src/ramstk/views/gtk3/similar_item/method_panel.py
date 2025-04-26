# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.similar_item.method_panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The Similar Item Method panel module."""

# Standard Library Imports
from typing import Dict, List, Union

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKFixedPanel,
    WidgetConfig,
    make_widget_config,
)


class SimilarItemMethodPanel(RAMSTKFixedPanel):
    """Panel to display Similar Item analysis methods."""

    # Define private class attributes.
    _record_field = "hardware_id"
    _select_msg = "succeed_get_similar_item_attributes"
    _tag = "similar_item"
    _title = _("Similar Item Method")

    def __init__(self):
        """Initialize an instance of the Similar Item methods panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbSimilarItemMethod: RAMSTKComboBox = RAMSTKComboBox()

        # Initialize private instance attributes.
        self._lst_widget_configuration: List[WidgetConfig] = [
            make_widget_config(
                self.cmbSimilarItemMethod,
                {
                    "datatype": "gint",
                    "default": 0,
                    "field": "similar_item_method_id",
                    "index": 29,
                    "label_text": _("Select Similar Item Method "),
                    "listen_topic": "mvw_editing_hardware",
                    "send_topic": "wvw_editing_hardware",
                },
                {
                    "editable": True,
                    "tooltip": _("Select the similar item analysis method."),
                    "visible": True,
                },
            ),
        ]
        self._method_id: int = 0
        self._on_edit_message = f"wvw_editing_{self._tag}"

        # Initialize public instance attributes.
        self.method_id: int = 0

        super().do_set_widget_attributes()
        super().do_set_widget_properties()
        super().do_make_fixed_panel()
        self._do_set_widget_callbacks()
        self._do_load_methods()

    # ----- SimilarItemMethodPanel specific methods. ----- #
    def _do_load_methods(self) -> None:
        """Load Similar Item analysis RAMSTKComboBox."""
        self.cmbSimilarItemMethod.do_load_combo(
            [
                [_("Topic 633"), 0],
                [_("User-Defined"), 1],
            ],
        )

    def _do_set_sensitive(self, attributes: Dict[str, Union[int, float, str]]) -> None:
        """Set widget sensitivity as needed for the selected R(t) goal.

        :param attributes: the Similar Item attribute dict.
        """
        self.cmbSimilarItemMethod.set_sensitive(True)
        self.cmbSimilarItemMethod.do_update(
            {"similar_item_method_id": attributes["similar_item_method_id"]},
        )

    def _do_set_widget_callbacks(self) -> None:
        """Set the widget callbacks for the Similar Item Method panel."""
        super().do_set_widget_callbacks()

        self.cmbSimilarItemMethod.dic_handler_id["changed"] = (
            self.cmbSimilarItemMethod.connect(
                "changed",
                self._on_method_changed,
            )
        )

    def _on_method_changed(self, combo: RAMSTKComboBox) -> None:
        """Let others know when similar item method combo changes.

        :param combo: the similar item calculation method RAMSTKComboBox().
        """
        self.method_id = combo.get_active()

        pub.sendMessage(
            "succeed_change_similar_item_method",
            method_id=self.method_id,
        )
