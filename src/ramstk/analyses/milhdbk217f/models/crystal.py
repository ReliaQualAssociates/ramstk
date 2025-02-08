# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.crystal.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Crystal MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.crystal import (
    PART_COUNT_LAMBDA_B,
    PART_COUNT_PI_Q,
    PART_STRESS_PI_Q,
    PI_E,
)


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress hazard rate for a crystal.

    This function calculates the MIL-HDBK-217F hazard rate using the part stress method.

    :param attributes: the attributes for the crystal being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary with
        updated values.
    :rtype: dict
    """
    attributes["hazard_rate_active"] = (
        attributes["hazard_rate_active"] * attributes["piQ"] * attributes["piE"]
    )

    return attributes


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Calculate the part stress base hazard rate.

    :param attributes: the attributes for the crystal being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary with
        updated values.
    :rtype: dict
    """
    if attributes["frequency_operating"] >= 0.0:
        return 0.013 * attributes["frequency_operating"] ** 0.23
    else:
        return 0.0


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE).

    :param attributes: the attribute dict for the crystal being calculated.
    :return: _pi_e; the environment factor for the active environment.
    :rtype: float
    :raises: IndexError if passed an invalid active environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PI_E[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid crystal environment ID {_environment_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate for a crystal.

    :param attributes: the attribute dict for the crystal being calculated.
    :return: _base_hr; the part count base hazard rate for the active environment.
    :rtype: float
    :raises: IndexError if passed an unknown active environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PART_COUNT_LAMBDA_B[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid crystal environment ID "
            f"{_environment_id}."
        )


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part count quality factor.

    :param attributes: the dict of connection attributes.
    :return: _pi_q: the quality factor.
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]

    try:
        return PART_COUNT_PI_Q[_quality_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid crystal quality ID {_quality_id}."
        )


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]]
) -> float:
    """Retrieve the part stress quality factor.

    :param attributes: the dict of connection attributes.
    :return: _pi_q: the quality factor.
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id: int = attributes["quality_id"]
    _subcategory_id: int = attributes["subcategory_id"]

    try:
        if _subcategory_id in {4, 5}:
            return PART_STRESS_PI_Q[_quality_id - 1]
        else:
            return 1.0
    except IndexError:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid crystal quality ID {_quality_id}."
        )


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value of various parameters.

    :param attributes: the attribute dict for the crystal being calculated.
    :return: attributes; the updated attribute dict.
    :rtype: dict
    """
    if attributes["frequency_operating"] <= 0.0:
        attributes["frequency_operating"] = 50.0

    return attributes
