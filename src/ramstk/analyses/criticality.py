# -*- coding: utf-8 -*-
#
#       ramstk.analyses.criticality.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Criticality Analysis Module."""

# Standard Library Imports
from typing import Dict, Union

# RAMSTK Package Imports
from ramstk.exceptions import OutOfRangeError


def calculate_rpn(sod: Dict[str, int]) -> int:
    """Calculate the Risk Priority Number (RPN).

        RPN = S * O * D

        >>> SOD = {'rpn_severity': 5, 'rpn_occurrence': 8, 'rpn_detection': 7}
        >>> criticality.calculate_rpn(SOD)
        280

        >>> SOD['rpn_severity'] = 0
        >>> criticality.calculate_rpn(SOD)
        Traceback (most recent call last):
        ...
        ramstk.exceptions.OutOfRangeError: RPN severity is outside the range [1, 10].   # noqa


    :param sod: a dict containing the S, O, and D values from which to
        calculate the RPN.
    :return: _rpn; the calculated risk priority number (RPN).
    :rtype: int
    :raise: OutOfRangeError if one of the inputs falls outside the range
        [1, 10].
    """
    _do_validate_range(sod["rpn_severity"], 1, 10, "RPN severity")
    _do_validate_range(sod["rpn_occurrence"], 1, 10, "RPN occurrence")
    _do_validate_range(sod["rpn_detection"], 1, 10, "RPN detection")

    return (
        int(sod["rpn_severity"])
        * int(sod["rpn_occurrence"])
        * int(sod["rpn_detection"])
    )


def calculate_mode_hazard_rate(item_hr: float, mode_ratio: float) -> float:
    """Calculate the failure mode hazard rate.

        >>> item_hr=0.000617
        >>> mode_ratio=0.23
        >>> calculate_mode_hazard_rate(item_hr, mode_ratio)
        0.00014191

    :param item_hr: the hazard rate of the (hardware) item the mode is
        associated with.
    :param mode_ratio:
    :return: _mode_hazard_rate; the hazard rate of the failure mode.
    :rtype: float
    :raise: OutOfRangeError if passed a negative item hazard rate or a mode
        ratio outside [0.0, 1.0].
    """
    _do_validate_range(item_hr, 0.0, float("inf"), "Item hazard rate")
    _do_validate_range(mode_ratio, 0.0, 1.0, "Mode ratio")

    return item_hr * mode_ratio


def calculate_mode_criticality(
    mode_hr: float, mode_op_time: float, eff_prob: float
) -> float:
    """Calculate the MIL-HDBK-1629A, Task 102 criticality.

        >>> mode_hr=0.00021595
        >>> mode_op_time=4.15
        >>> eff_prob=1.0
        >>> calculate_mode_criticality(mode_hr, mode_op_time, eff_prob)

    :param mode_hr: the hazard rate of the failure mode.
    :param mode_op_time: the operating time of the failure mode (i.e.,
        the time at risk).
    :param eff_prob: the probability the end effect is the one observed.
    :return: _criticality; the calculated Task 102 criticality.
    :rtype: float
    :raise: OutOfRangeError if passed a negative mode operating time or an
        effect probability outside [0.0, 1.0].
    """
    _do_validate_range(mode_op_time, 0.0, float("inf"), "Mode operating time")
    _do_validate_range(eff_prob, 0.0, 1.0, "Effect probability")

    return mode_hr * mode_op_time * eff_prob


def _do_validate_range(
    value: Union[int, float], min_val: float, max_val: float, name: str
) -> None:
    """Validate that a value is within a specified range.

    :param value: The value to validate.
    :type value: int or float
    :param min_val: The minimum allowable value (inclusive).
    :type min_val: float
    :param max_val: The maximum allowable value (inclusive).
    :type max_val: float
    :param name: The name of the value being validated (for error messages).
    :type name: str
    :raises OutOfRangeError: If the value is outside the specified range.
    """
    if not min_val <= value <= max_val:
        raise OutOfRangeError(f"{name} is outside the range [{min_val}, {max_val}].")
