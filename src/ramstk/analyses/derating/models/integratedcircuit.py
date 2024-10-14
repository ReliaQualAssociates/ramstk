# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.integratedcircuit.py is part of the RAMSTK
#       Project
#
# All rights reserved.
# Copyright since 2017 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Integrated Circuit derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_current_limit,
    do_check_temperature_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, Dict[str, List[float]]]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for integrated circuits.

    :param environment_id: the index for the environment the integrated circuit is
        operating in; 0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the integrated circuit to check
        derating.
    :param stress_limits: the dict containing the stress derating limits for integrated
        circuits.
    :return: _overstress, _reason
    :rtype: tuple :raise: IndexError if an unknown environment ID is passed. :raise:
        KeyError if an unknown subcategory ID, package ID, or technology ID are passed.
        :raise: TypeError if a non-numeric value is passed for the current ratio or
        junction temperature.
    """
    _overstress: int = 0
    _reason: str = ""

    # Map subcategory, technology, and package IDs.
    _subcategory = {
        1: "digital",
        2: "linear",
        3: "microprocessor",
        4: "memory",
    }[subcategory_id]
    _technology = {
        1: "bipolar",
        2: "mos",
    }[kwargs["technology_id"]]
    _package = {
        1: "hermetic",
        2: "hermetic",
        3: "hermetic",
        4: "plastic1",
        5: "plastic1",
        6: "plastic1",
        7: "plastic2",
        8: "plastic2",
        9: "plastic2",
    }[kwargs["package_id"]]

    _overstress, _reason = do_check_current_limit(
        kwargs["current_ratio"],
        stress_limits[_subcategory][_technology][_package]["current"][environment_id],
    )

    _overstress, _reason = do_update_overstress_status(
        _overstress,
        _reason,
        do_check_temperature_limit(
            kwargs["temperature_junction"],
            stress_limits[_subcategory][_technology][_package]["temperature"][
                environment_id
            ],
            0.0,  # No delta for temperature check
        ),
    )

    return _overstress, _reason
