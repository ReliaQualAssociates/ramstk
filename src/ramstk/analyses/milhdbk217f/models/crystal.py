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
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a crystal.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.  Because the part stress model for a crystal is simply the based hazard rate
    (lambdaB) multiplied by the environment factor (piE) and quality factor (piQ), this
    function only needs to return the hardware attributes dict as this calculation is
    performed in the milhdbk217f._do_calculate_part_stress() function.

    :param attributes: the hardware attributes dict for the crystal being calculated.
    :return: the hardware attributes dict.
    :rtype: dict
    """
    return attributes


def calculate_part_stress_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Calculate the part stress base hazard rate (lambdaB).

    This function calculates the MIL-HDBK-217FN2 base hazard rate for the parts stress
    method.

    :param attributes: the hardware attributes dict for the crystal being calculated.
    :return: the calculated part stress base hazard rate (lambdaB).
    :rtype: float
    """
    if attributes["frequency_operating"] >= 0.0:
        return 0.013 * attributes["frequency_operating"] ** 0.23
    else:
        return 0.0


def get_environment_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the crystal being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PI_E[_environment_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_environment_factor: Invalid crystal environment ID {_environment_id}."
        ) from exc


def get_part_count_lambda_b(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate. The list
    PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base hazard rates.  The
    index for PART_COUNT_LAMBDA_B is the environment ID.

    :param attributes: the hardware attributes dict for the crystal being calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PART_COUNT_LAMBDA_B[_environment_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid crystal environment ID "
            f"{_environment_id}."
        ) from exc


def get_part_count_quality_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve the part count quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the crystal being calculated.
    :return: the selected part count quality factor (piQ).
    :rtype: float
    :raises: IndexError when passed an invalid quality ID.
    """
    _quality_id = attributes["quality_id"]

    try:
        return PART_COUNT_PI_Q[_quality_id - 1]
    except IndexError as exc:
        raise IndexError(
            f"get_part_count_quality_factor: Invalid crystal quality ID {_quality_id}."
        ) from exc


def get_part_stress_quality_factor(
    attributes: Dict[str, Union[float, int, str]],
) -> float:
    """Retrieve the part stress quality factor (piQ) for the passed quality ID.

    :param attributes: the hardware attributes dict for the crystal being calculated.
    :return: the selected part stress quality factor (piQ).
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
    except IndexError as exc:
        raise IndexError(
            f"get_part_stress_quality_factor: Invalid crystal quality ID {_quality_id}."
        ) from exc


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various crystal parameters.

    :param attributes: the hardware attributes dict for the crystal being calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    if attributes["frequency_operating"] <= 0.0:
        attributes["frequency_operating"] = 50.0

    return attributes
