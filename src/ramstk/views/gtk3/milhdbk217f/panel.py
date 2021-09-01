# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.milhdbk217f.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 MIL-HDBK-217F Panels."""

# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _
from ramstk.views.gtk3.widgets import RAMSTKComboBox, RAMSTKFixedPanel


class MilHdbk217FInputPanel(RAMSTKFixedPanel):
    """Display Hardware assessment input attribute data.

    The Hardware assessment input view displays all the assessment inputs for
    the selected Hardware item.  This includes, currently, inputs for
    MIL-HDBK-217FN2 parts count and part stress analyses.  The attributes of a
    Hardware assessment input view are:

    :ivar _hazard_rate_method_id: the ID of the method to use for estimating
        the Hardware item's hazard rate.
    :ivar _subcategory_id: the ID of the Hardware item's subcategory.
    :ivar _title: the text to put on the RAMSTKFrame() holding the
        assessment input widgets.
    :ivar cmbQuality: select and display the quality level of the hardware
        item.
    """

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "selected_hardware"
    _tag = "mil_hdbk_217f"
    _title = _("Design Ratings")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the Hardware assessment input view."""
        super().__init__()

        # Initialize widgets.
        self.cmbQuality: RAMSTKComboBox = RAMSTKComboBox()

        # Initialize private dictionary attributes.

        # Initialize private list attributes.
        self._lst_labels: List[str] = []
        self._lst_tooltips: List[str] = []

        # Initialize private scalar attributes.
        self._hazard_rate_method_id: int = -1
        self._subcategory_id: int = -1

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

    def do_load_common(self, attributes: Dict[str, Any]) -> None:
        """Load the component common widgets.

        :param attributes: the attributes dictionary for the selected
            Component.
        :return: None
        :rtype: None
        """
        self._record_id = attributes["hardware_id"]
        self._hazard_rate_method_id = attributes["hazard_rate_method_id"]
        self._subcategory_id = attributes["subcategory_id"]

        self.do_load_comboboxes(attributes["subcategory_id"])
        self._do_set_sensitive()

        self.cmbQuality.do_update(attributes["quality_id"], signal="changed")

    def do_set_properties(self, **kwargs: Dict[str, Any]) -> None:
        """Set properties for Hardware assessment input widgets.

        :return: None
        :rtype: None
        """
        super().do_set_properties(bold=True, title=self._title)

        _idx = 0
        for _widget in self._lst_widgets:
            _widget.do_set_properties(tooltip=self._lst_tooltips[_idx])
            _idx += 1
