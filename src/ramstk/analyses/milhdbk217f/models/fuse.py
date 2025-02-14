# type: ignore
# -*- coding: utf-8 -*-
#
#       ramstk.analyses.milhdbk217f.models.fuse.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Fuse MIL-HDBK-217F Calculations Module."""

# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.constants.fuse import PART_COUNT_LAMBDA_B, PI_E


def calculate_part_stress(
    attributes: Dict[str, Union[float, int, str]]
) -> Dict[str, Union[float, int, str]]:
    """Calculate the part stress active hazard rate for a fuse.

    This function calculates the MIL-HDBK-217FN2 hazard rate using the part stress
    method.  Because the part stress model for a fuse is simply the product of the based
    hazard rate (lambdaB) and the environment factor (piE), this function only needs to
    return the hardware attributes dict as this calculation is performed in the
    milhdbk217f._do_calculate_part_stress() function.

    :param attributes: the hardware attributes dict for the fuse being calculated.
    :return: the hardware attributes dict.
    :rtype: dict
    """
    return attributes


def get_environment_factor(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the environment factor (piE) for the passed environment ID.

    :param attributes: the hardware attributes dict for the fuse being calculated.
    :return: the selected environment factor (pIE).
    :rtype: float
    :raises: IndexError when passed an invalid environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PI_E[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_environment_factor: Invalid fuse environment ID {_environment_id}."
        )


def get_part_count_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part count base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part count base hazard rate. The list
    PART_COUNT_LAMBDA_B contains the MIL-HDBK-217FN2 part count base hazard rates.  The
    index for PART_COUNT_LAMBDA_B is the environment ID.

    :param attributes: the hardware attributes dict for the fuse being calculated.
    :return: the selected part count base hazard rate (lambdaB).
    :rtype: float
    :raises: IndexError when passed an invalid active environment ID.
    """
    _environment_id = attributes["environment_active_id"]

    try:
        return PART_COUNT_LAMBDA_B[_environment_id - 1]
    except IndexError:
        raise IndexError(
            f"get_part_count_lambda_b: Invalid fuse environment ID {_environment_id}."
        )


def get_part_stress_lambda_b(attributes: Dict[str, Union[float, int, str]]) -> float:
    """Retrieve the part stress base hazard rate (lambdaB).

    This function retrieves the MIL-HDBK-217FN2 part stress base hazard rate.

    :param attributes: the hardware attributes dict for the fuse being calculated.
    :return: the selected part stress base hazard rate (lambdaB).
    :rtype: float
    """
    return 0.010


def set_default_values(
    attributes: Dict[str, Union[float, int, str]],
) -> Dict[str, Union[float, int, str]]:
    """Set the default value for various fuse parameters.

    :param attributes: the hardware attributes dict for the fuse being calculated.
    :return: the updated hardware attributes dict.
    :rtype: dict
    """
    attributes["piQ"] = 1.0

    if attributes["lambda_b"] <= 0.0:
        attributes["lambda_b"] = 0.01

    return attributes
