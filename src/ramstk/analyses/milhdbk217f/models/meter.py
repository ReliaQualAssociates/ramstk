# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.meter.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Meter MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.meter import (
    PART_COUNT_LAMBDA_B,
    PART_COUNT_PI_Q,
    PART_STRESS_LAMBDA_B,
    PART_STRESS_PI_Q,
    PI_E,
    PI_F,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a meter.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.

    :param attributes: the hardware attributes dict for the meter being calculated.
    :return: the hardware attributes dict with updated values.
    :rtype: dict
    :raises: KeyError when the hardware attributes dict is missing one or more keys.
    """
    try:
        attributes["piT"] = get_temperature_stress_factor(
            attributes["temperature_active"], attributes["temperature_rated_max"]
        )

        # Determine the application factor (piA) and function factor (piF).
        if attributes["subcategory_id"] == 2:
            attributes["piA"] = 1.7 if attributes["type_id"] - 1 else 1.0
            attributes["piF"] = PI_F[attributes["application_id"] - 1]

        if attributes["subcategory_id"] == 2:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"]
                * attributes["piA"]
                * attributes["piF"]
                * attributes["piQ"]
            )
        elif attributes["subcategory_id"] == 1:
            attributes["hazard_rate_active"] = (
                attributes["hazard_rate_active"] * attributes["piT"]
            )

        return attributes
    except KeyError as err:
        raise KeyError(
            f"calculate_part_stress: Missing required meter attribute: {err}."
        )


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the meter being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _environment_id: int = attributes["environment_active_id"]
    _subcategory_id: int = attributes["subcategory_id"]

    try:
        return PI_E[_subcategory_id][_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid meter environment ID "
            f"{_environment_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_environment_factor: Invalid meter subcategory ID "
            f"{_subcategory_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate.  The
    dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base
    hazard rates.  Keys for PART_COUNT_LAMBDA_B are:

        #. subcategory_id
        #. environment_active_id
        #. type id

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory    |              Meter            | MIL-HDBK-217F   |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Elapsed Time                  |       12.4      |
    +----------------+-------------------------------+-----------------+
    |        2       | Panel                         |       18.1      |
    +----------------+-------------------------------+-----------------+

    :param attributes: the hardware attributes dict for the meter being calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid active environment ID.
    :raises: KeyError when passed an invalid subcategory ID or type ID.
    """
    _environment_active_id = attributes["environment_active_id"]
    _subcategory_id = attributes["subcategory_id"]
    _type_id = attributes["type_id"]

    try:
        return PART_COUNT_LAMBDA_B[_subcategory_id][_type_id][
            _environment_active_id - 1
        ]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid meter environment ID "
            f"{_environment_active_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid meter subcategory ID "
            f"{_subcategory_id} or type ID {_type_id}."
        )


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part count quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the meter being calculated.
    :return: the selected part count quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    :raises: KeyError when passed an invalid subcategory ID.
    """
    _quality_id: int = attributes["quality_id"]
    _subcategory_id: int = attributes["subcategory_id"]

    try:
        return PART_COUNT_PI_Q[_subcategory_id][_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid meter quality ID "
            f"{_quality_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_quality_factor: Invalid meter subcategory ID "
            f"{_subcategory_id}."
        )


def get_part_stress_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part stress base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217F part stress base hazard rate.

    :param attributes: the hardware attributes dict for the meter being calculated.
    :return: the selected part stress base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid type ID.
    """
    _subcategory_id = attributes["subcategory_id"]
    _type_id = attributes["type_id"]

    try:
        if _subcategory_id == 1:
            return PART_STRESS_LAMBDA_B[1][_type_id - 1]
        elif _subcategory_id == 2:
            return PART_STRESS_LAMBDA_B[2]
        return 0.0
    except IndexError:
        raise IndexError(f"get_part_stress_lambda_b: Invalid meter type ID {_type_id}.")


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part stress quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the meter being calculated.
    :return: the selected part stress quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id: int = attributes["quality_id"]
    _subcategory_id: int = attributes["subcategory_id"]

    try:
        return PART_STRESS_PI_Q[_quality_id - 1] if _subcategory_id == 2 else 1.0
    except IndexError:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid meter quality ID "
            f"{_quality_id}."
        )


def get_temperature_stress_factor(
    temperature_active: float,
    temperature_rated_max: float,
) -> float:
    """Retrieve the temperature stress factor (piT).

    :param temperature_active: the meter operating ambient temperature in C.
    :param temperature_rated_max: the meter maximum rated operating temperature in C.
    :return: the selected temperature stress factor (piT).
    :rtype: float
    :raises: TypeError when passed a string for either temperature.
    :raises: ZeroDivisionError when passed a rated maximum temperature = 0.0.
    """
    _pi_t = 0.0

    try:
        _temperature_ratio = temperature_active / temperature_rated_max
    except TypeError:
        _active_type = type(temperature_active)
        _max_type = type(temperature_rated_max)
        raise TypeError(
            f"get_temperature_stress_factor: Meter active temperature {_active_type} "
            f"and maximum rated temperature {_max_type} must both be non-negative "
            f"numbers."
        )
    except ZeroDivisionError:
        raise ZeroDivisionError(
            "get_temperature_stress_factor: Meter maximum rated temperature cannot "
            "be zero."
        )

    if 0.0 < _temperature_ratio <= 0.5:
        _pi_t = 0.5
    elif 0.5 < _temperature_ratio <= 0.6:
        _pi_t = 0.6
    elif 0.6 < _temperature_ratio <= 0.8:
        _pi_t = 0.8
    elif 0.8 < _temperature_ratio <= 1.0:
        _pi_t = 1.0

    return _pi_t


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various meter parameters.

    MIL-HDBK-217F has no defaults for meters.  This function is needed as a placeholder
    only.

    :param attributes: the hardware attributes dict for the meter being calculated.
    :return: the hardware attributes dict.
    :rtype: dict
    """
    return attributes
