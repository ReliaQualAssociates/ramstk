# -*- coding: utf-8 -*-
#
#       ramstk.analyses.derating.models.resistor.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Resistor derating analysis functions."""

# Standard Library Imports
from typing import Dict, List, Tuple, Union

# RAMSTK Package Imports
from ramstk.analyses.derating.derating_utils import (
    do_check_power_limit,
    do_check_temperature_limit,
    do_check_voltage_limit,
    do_update_overstress_status,
)


# pylint: disable=too-many-locals
def do_derating_analysis(
    environment_id: int,
    subcategory_id: int,
    stress_limits: Dict[str, Dict[str, Union[Dict[str, List[float]], List[float]]]],
    *,
    power_rated: float,
    power_ratio: float,
    temperature_case: float,
    temperature_knee: float,
    temperature_rated_max: float,
    voltage_ratio: float,
) -> Tuple[int, str]:
    """Check actual stresses against derating criteria for resistors.

    :param environment_id: the index for the environment the resistor is operating in;
        0=protected, 1=normal, 2=severe.
    :param subcategory_id: the subcategory ID of the resistor to check derating.
    :param stress_limits: the dict containing the stress derating limits for resistors.
    :param power_rated: the rated power of the resistor being checked for overstress.
    :param power_ratio: the operating to rated power ratio of the resistor being checked
        for overstress.
    :param temperature_case: the operating temperature of the resistor being checked for
        overstress.
    :param temperature_knee: the knee temperature of the resistor being checked for
        overstress.
    :param temperature_rated_max: the maximum rated temperature of the resistor being
        checked for overstress.
    :param voltage_ratio: the operating to rated voltage ratio of the resistor being
        checked for overstress.
    :return: _overstress, _reason
    :rtype: tuple
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid subcategory ID.
    :raises: TypeError when passed a non-numeric value for the power ratio, rated power,
        case temperature, knee temperature, rated temperature, or voltage ratio.
    """
    _overstress: int = 0
    _reason: str = ""

    _subcategory = _get_subcategory_name(subcategory_id)

    try:
        # Check power limits.
        _power_limit = _get_stress_limit(
            _subcategory, environment_id, power_rated, stress_limits, "power"
        )
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_power_limit(
                power_ratio,
                _power_limit,
            ),
        )

        # Check temperature limits.
        _temperature_limit = _get_stress_limit(
            _subcategory,
            environment_id,
            power_rated,
            stress_limits,
            "temperature",
        )
        _max_temperature = temperature_knee + _temperature_limit * (
            temperature_rated_max - temperature_knee
        )
        _overstress, _reason = do_update_overstress_status(
            _overstress,
            _reason,
            do_check_temperature_limit(
                temperature_case,
                _max_temperature,
                0.0,
            ),
        )

        # Check voltage limits for specific subcategories.
        if subcategory_id in {2, 4, 5, 6, 7}:
            _voltage_limit = _get_stress_limit(
                _subcategory,
                environment_id,
                power_rated,
                stress_limits,
                "voltage",
            )
            _overstress, _reason = do_update_overstress_status(
                _overstress,
                _reason,
                do_check_voltage_limit(
                    voltage_ratio,
                    _voltage_limit,
                ),
            )

        return _overstress, _reason
    except IndexError as exc:
        raise IndexError(
            f"do_derating_analysis: Invalid resistor environment ID "
            f"{environment_id}."
        ) from exc
    except TypeError as exc:
        raise TypeError(
            f"do_derating_analysis: Invalid resistor power ratio type "
            f"{type(power_ratio)}, rated power type {type(power_rated)}, case "
            f"temperature type {type(temperature_case)}, knee temperature type "
            f"{type(temperature_knee)}, rated temperature type "
            f"{type(temperature_rated_max)}, or voltage ratio type "
            f"{type(voltage_ratio)}.  All should be <type 'float'>."
        ) from exc


def _get_subcategory_name(
    subcategory_id: int,
) -> str:
    """Retrieve the resistor subcategory nome.

    :param subcategory_id: the subcategory ID of the resistor being checked for
        overstress.
    :return: the selected subcategory name.
    :rtype: str
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _subcategory_names = {
        1: "fixed_composition",
        2: "fixed_film",
        3: "fixed_film_power",
        4: "fixed_film_network",
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
    }
    try:
        return _subcategory_names[subcategory_id]
    except KeyError as exc:
        raise KeyError(
            f"_get_subcategory_name: Invalid resistor subcategory ID {subcategory_id}."
        ) from exc


def _get_stress_limit(
    subcategory: str,
    environment_id: int,
    rated_power: float,
    stress_limits: Dict[str, Dict[str, Union[Dict[str, List[float]], List[float]]]],
    limit_type: str,
) -> float:
    """Retrieve power, temperature, or voltage stress limits.

    :param subcategory: The subcategory string of the resistor being checked for
        overstress.
    :param environment_id: The environment ID of the resistor being checked for
        overstress.
    :param rated_power: The rated power of the resistor being checked for overstress.
    :param stress_limits: The stress limit dictionary.
    :param limit_type: The type of limit to retrieve ('power', 'temperature',
        'voltage').
    :return: The selected stress limit value.
    """
    if subcategory in {
        "fixed_chip",
        "fixed_composition",
        "fixed_film",
        "fixed_wirewound",
    }:
        return (
            stress_limits[subcategory]["high_power"][limit_type][environment_id]  # type: ignore[call-overload]
            if rated_power >= 0.5
            else stress_limits[subcategory]["low_power"][limit_type][environment_id]  # type: ignore[call-overload]
        )
    else:
        return stress_limits[subcategory][limit_type][environment_id]  # type: ignore[index, return-value]
