# -*- coding: utf-8 -*-
#
#       ramstk.controllers.mode.analysismanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Failure Mode Controller Package analysis manager."""

# Standard Library Imports
from collections import defaultdict
from typing import Any, Dict

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.analyses.criticality import (
    calculate_mode_criticality,
    calculate_mode_hazard_rate,
)
from ramstk.configuration import RAMSTKUserConfiguration
from ramstk.controllers import RAMSTKAnalysisManager


class AnalysisManager(RAMSTKAnalysisManager):
    """Contain the attributes and methods of the FMEA analysis manager."""

    def __init__(
        self, configuration: RAMSTKUserConfiguration, **kwargs: Dict[str, Any]
    ) -> None:
        """Initialize an instance of the FMEA analysis manager.

        :param configuration: the user configuration instance associated
            with the current instance of the RAMSTK application.
        """
        super().__init__(configuration, **kwargs)

        # Initialize private dictionary attributes.

        # Initialize private list attributes.

        # Initialize private scalar attributes.

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().on_get_tree, "succeed_retrieve_modes")
        pub.subscribe(super().on_get_tree, "succeed_get_mode_tree")

        pub.subscribe(self._do_calculate_criticality, "request_calculate_criticality")

    def _do_calculate_criticality(self, item_hr: float) -> None:
        """Calculate MIL-STD-1629A, Task 102 criticality of a hardware item.

        :param item_hr: the hazard rate of the hardware item the criticality is
            being calculated for.
        :return: None
        :rtype: None
        """
        _item_criticality: Dict[str, float] = defaultdict(float)
        for _mode in self._tree.children(0):
            _mode.data["mode"].mode_hazard_rate = calculate_mode_hazard_rate(
                item_hr, _mode.data["mode"].mode_ratio
            )
            _mode.data["mode"].mode_criticality = calculate_mode_criticality(
                _mode.data["mode"].mode_hazard_rate,
                _mode.data["mode"].mode_op_time,
                _mode.data["mode"].effect_probability,
            )
            _item_criticality[_mode.data["mode"].severity_class] += _mode.data[
                "mode"
            ].mode_criticality

        pub.sendMessage(
            "succeed_calculate_mode_criticality",
            item_criticality=_item_criticality,
        )
