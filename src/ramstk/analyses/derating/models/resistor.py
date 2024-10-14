# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Capacitor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_power_limit,
    do_check_temperature_limit,
    do_check_voltage_limit,
    do_update_overstress_status,
)


def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
    **kwargs,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for resistors.

    :param environment_id: the index for the environment the resistor is operating in;
        0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the resistor to check derating.
    :param stress_limits: the dict containing the stress derating limits for resistors.
    :return: _overstress, _reason
    :rtype: tuple :raise: IndexError if an unknown environment ID is passed. :raise:
        KeyError if an unknown subcategory ID is passed. :raise: TypeError if a non-
        numeric value is passed for the power ratio, rated power, case temperature, knee
        temperature, rated temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = {
        1: "fixed_composition",
        2: "fixed_film",
        3: "fixed_film_power",
        4: "ixed_film_network",
        5: "fixed_wirewound",
        6: "fixed_wirewound_power",
        7: "fixed_wirewound_chassis",
        8: "thermistor",
        9: "variable_wirewound",
        10: "variable_wirewound_precision",
        11: "variable_wirewound",
        12: "variable_wirewound_power",
        13: "variable_non_wirewound",
        14: "variable_composition",
        15: "variable_film",
    }[subcategory_id]

    # Check power limits.
    _power_limit = _do_get_stress_limit(
        _subcategory, environment_id, kwargs["power_rated"], stress_limits, "power"
    )
    _overstress, _reason = do_update_overstress_status(
        _overstress,
        _reason,
        do_check_power_limit(
            kwargs["power_ratio"],
            _power_limit,
        ),
    )

    # Check temperature limits.
    _temperature_limit = _do_get_stress_limit(
        _subcategory,
        environment_id,
        kwargs["power_rated"],
        stress_limits,
        "temperature",
    )
    _max_temperature = kwargs["temperature_knee"] + _temperature_limit * (
        kwargs["temperature_rated_max"] - kwargs["temperature_knee"]
    )
    _overstress, _reason = do_update_overstress_status(
        _overstress,
        _reason,
        do_check_temperature_limit(
            kwargs["temperature_case"],
            _max_temperature,
            _temperature_limit,
        ),
    )

    # Check voltage limits for specific subcategories.
    if subcategory_id in {2, 4, 5, 6, 7}:
        _voltage_limit = _do_get_stress_limit(
            _subcategory,
            environment_id,
            kwargs["power_rated"],
            stress_limits,
            "voltage",
        )
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_voltage_limit(
                kwargs["voltage_ratio"],
                _voltage_limit,
            ),
        )

    return _overstress, _reason


def _do_get_stress_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Dict[str, List[float]]]],
    limit_type: str,
) -> float:
    """Retrieve power, temperature, or voltage limit.

    :param subcategory: The subcategory of the resistor.
    :param environment_id: The environment index.
    :param rated_power: The rated power of the resistor.
    :param stress_limits: The stress limit dictionary.
    :param limit_type: The type of limit to retrieve ('power', 'temperature',
        'voltage').
    :return: The retrieved limit value.
    """
    if subcategory in {
        "fixed_chip",
        "fixed_composition",
        "fixed_film",
        "fixed_wirewound",
    }:
        return (
            stress_limits[subcategory]["high_power"][limit_type][environment_id]
            if rated_power >= 0.5
            else stress_limits[subcategory]["low_power"][limit_type][environment_id]
        )
    else:
        return stress_limits[subcategory][limit_type][environment_id]
