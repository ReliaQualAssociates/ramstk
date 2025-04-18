# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.milhdbk217f.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The MIL-HDBK-217F panel module."""

# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.utilities import do_subscribe_to_messages
from ramstk.views.gtk3.widgets import RAMSTKEntry, RAMSTKFixedPanel, RAMSTKLabel


class MilHdbk217FResultPanel(RAMSTKFixedPanel):
    """Display Hardware assessment results attribute data.

    The widgets of a MIL-HDBK-217F result panel are:

    :ivar txtLambdaB: displays the base hazard rate of the hardware item.
    :ivar txtPiQ: displays the quality factor for the hardware item.
    :ivar txtPiE: displays the environment factor for the hardware item.

    The attributes of a MIL-HDBK-217F result panel are:

    :ivar _hazard_rate_method_id: the ID of the method selected to calculate the
        hazard rate of the selected component.
    :ivar _lambda_b: the base hazard rate of the selected component.
    :ivar category_id: the hardware category ID of the selected component.
    :ivar subcategory_id: the hardware subcategory ID of the selected component.
    """

    # Define private class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_milhdbk217f_attributes"
    _tag: str = "milhdbk217f"

    def __init__(self) -> None:
        """Initialize an instance of the Hardware assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.lblModel: RAMSTKLabel = RAMSTKLabel("")
        self.txtLambdaB: RAMSTKEntry = RAMSTKEntry()
        self.txtPiQ: RAMSTKEntry = RAMSTKEntry()
        self.txtPiE: RAMSTKEntry = RAMSTKEntry()

        # Initialize private instance attributes.
        self._hazard_rate_method_id: int = 0
        self._lambda_b: float = 0.0

        # Initialize public instance attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        # Subscribe to PyPubSub messages.
        do_subscribe_to_messages(
            {
                "selected_hardware": self._do_set_hardware_attributes,
                "succeed_get_reliability_attributes": self._do_set_reliability_attributes,  # noqa
                "succeed_get_milhdbk217f_attributes": self._do_load_entries,
            }
        )

    def do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the Hardware assessment results page.

        :param attributes: the attribute dict for the selected Hardware.
        """
        super().do_set_widget_sensitivity(
            [
                self.txtLambdaB,
                self.txtPiE,
                self.txtPiQ,
            ],
            False,
        )

        # Display the correct calculation model.
        self.__do_set_model_label()
        self.lblModel.do_update(
            {"hazard_rate_model": self._dic_part_stress[self.subcategory_id]}
        )
        self.txtLambdaB.do_update(
            {"lambda_b": str(self.fmt.formant(self._lambda_b or 0.0))}
        )
        self.txtPiE.do_update({"piE": str(self.fmt.format(attributes["piE"] or 1.0))})
        self.txtPiQ.do_update({"piQ": str(self.fmt.format(attributes["piQ"] or 1.0))})

    def _do_set_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self.category_id = attributes["category_id"]
        self.subcategory_id = attributes["subcategory_id"]

    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._lambda_b = attributes["lambda_b"]

    def __do_set_model_label(self) -> None:
        """Set the text displayed in the hazard rate model RAMSTKLabel()."""
        _model_text = "No Model"

        if self._hazard_rate_method_id == 1:
            _model_text = (
                '<span foreground="blue">\u03bb<sub>p</sub> = '
                "\u03bb<sub>b</sub>\u03c0<sub>Q</sub></span>"
            )
        elif self._hazard_rate_method_id == 2:
            _model_text = self._dic_part_stress.get(self.subcategory_id, "No Model")

        self.lblModel.do_update({"hazard_rate_model": _model_text})
