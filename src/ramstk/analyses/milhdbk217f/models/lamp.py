# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.lamp.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Lamp MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.lamp import PART_COUNT_LAMBDA_B, PI_E


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a lamp.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.

    :param attributes: the hardware attributes dict for the lamp being calculated.
    :return: attributes; the hardware attributes dict with updated values.
    :rtype: dict
    :raises: KeyError when the hardware attributes dict is missing one or more keys.
    """
    try:
        # Determine the utilization factor (piU).
        if attributes["duty_cycle"] < 10.0:
            attributes["piU"] = 0.1
        elif 10.0 <= attributes["duty_cycle"] < 90.0:
            attributes["piU"] = 0.72
        else:
            attributes["piU"] = 1.0

        # Determine the application factor (piA).
        attributes["piA"] = 3.3 if attributes["application_id"] - 1 else 1.0

        attributes["hazard_rate_active"] = (
            attributes["hazard_rate_active"]
            * attributes["piU"]
            * attributes["piA"]
            * attributes["piE"]
        )

        return attributes
    except KeyError as err:
        raise KeyError(
            f"calculate_part_stress: Missing required lamp attribute: {err}."
        )


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Calculate the part stress base hazard rate (lambdaB).

    This function calculates the MIL-HDBK-217FN2 base hazard rate for the parts stress
    method.

    :param attributes: the hardware attributes dict for the lamp being calculated.
    :return: the calculated part stress base hazard rate (lambdaB).
    :rtype: float
    """
    return 0.074 * attributes["voltage_rated"] ** 1.29


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the lamp being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PI_E[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid lamp environment ID {_environment_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate.  The
    dictionary PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base hazard
    rates.  Keys are for PART_COUNT_LAMBDA_B are:

    #. application_id #. environment_active_id

    :param attributes: the hardware attributes dict for the lamp being calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid active environment ID.
    :raises: KeyError when passed an invalid application ID.
    """
    _application_id = attributes["application_id"]
    _environment_id = attributes["environment_active_id"]

    try:
        return PART_COUNT_LAMBDA_B[_application_id][_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid lamp environment ID "
            f"{_environment_id}."
        )
    except KeyError:
        raise KeyError(
            f"get_part_count_lambda_b: Invalid lamp application ID "
            f"{_application_id}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various lamp parameters.

    :param attributes: the hardware attributes dict for the lamp being calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["piQ"] = 1.0

    if attributes["rated_voltage"] <= 0.0:
        attributes["rated_voltage"] = 28.0

    if attributes["duty_cycle"] <= 0.0:
        attributes["duty_cycle"] = 50.0

    return attributes
