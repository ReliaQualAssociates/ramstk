# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.milhdbk217f.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 MIL-HDBK-217F Panels."""

# Standard Library Imports
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
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

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "hardware_id"
    _select_msg: str = "succeed_get_milhdbk217f_attributes"
    _tag: str = "milhdbk217f"

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware assessment result view."""
        super().__init__()

        # Initialize widgets.
        self.lblModel: RAMSTKLabel = RAMSTKLabel("")
        self.txtLambdaB: RAMSTKEntry = RAMSTKEntry()
        self.txtPiQ: RAMSTKEntry = RAMSTKEntry()
        self.txtPiE: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = 0
        self._lambda_b: float = 0.0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.category_id: int = 0
        self.subcategory_id: int = 0

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self._do_set_hardware_attributes,
            "selected_hardware",
        )
        pub.subscribe(
            self._do_set_reliability_attributes,
            "succeed_get_reliability_attributes",
        )

    def do_load_entries(self, attributes: Dict[str, Any]) -> None:
        """Load the Hardware assessment results page.

        :param attributes: the attribute dict for the selected Hardware.
        :return: None
        :rtype: None
        """
        self.txtLambdaB.set_sensitive(False)
        self.txtPiE.set_sensitive(False)
        self.txtPiQ.set_sensitive(False)

        # Display the correct calculation model.
        self.__do_set_model_label()

        self.txtLambdaB.do_update(
            str(self.fmt.format(self._lambda_b or 0.0)),
            signal="changed",
        )
        self.txtPiQ.do_update(
            str(self.fmt.format(attributes["piQ"] or 1.0)),
            signal="changed",
        )
        self.txtPiE.do_update(
            str(self.fmt.format(attributes["piE"] or 1.0)),
            signal="changed",
        )

    def _do_set_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        self.category_id = attributes["category_id"]
        self.subcategory_id = attributes["subcategory_id"]

    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None:
        """Set the attributes when the reliability attributes are retrieved.

        :param attributes: the dict of reliability attributes.
        :return: None
        :rtype: None
        """
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._lambda_b = attributes["lambda_b"]

    def __do_set_model_label(self) -> None:
        """Set the text displayed in the hazard rate model RAMSTKLabel().

        :return: None
        :rtype: None
        """
        if self._hazard_rate_method_id == 1:
            self.lblModel.set_markup(
                '<span foreground="blue">\u03BB<sub>p</sub> = '
                "\u03BB<sub>b</sub>\u03C0<sub>Q</sub></span> "
            )
        elif self._hazard_rate_method_id == 2:
            try:
                self.lblModel.set_markup(self._dic_part_stress[self.subcategory_id])
            except KeyError:
                self.lblModel.set_markup("No Model")
        else:
            self.lblModel.set_markup("No Model")
