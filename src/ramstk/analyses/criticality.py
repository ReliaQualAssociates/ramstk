# -*- coding: utf-8 -*-
#
#       ramstk.analyses.criticality.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2019 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""FMEA Criticality Analysis Module."""

# RAMSTK Package Imports
from ramstk.exceptions import OutOfRangeError


def calculate_rpn(sod):
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
    if not 0 < sod['rpn_severity'] < 11:
        raise OutOfRangeError(("RPN severity is outside the range [1, 10]."))
    if not 0 < sod['rpn_occurrence'] < 11:
        raise OutOfRangeError(("RPN occurrence is outside the range [1, 10]."))
    if not 0 < sod['rpn_detection'] < 11:
        raise OutOfRangeError(("RPN detection is outside the range [1, 10]."))

    _rpn = (int(sod['rpn_severity']) * int(sod['rpn_occurrence'])
            * int(sod['rpn_detection']))

    return _rpn


def calculate_mode_hazard_rate(item_hr, mode_ratio):
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
    if item_hr < 0.0:
        raise OutOfRangeError(("calculate_mode_hazard_rate() was passed a "
                               "negative value for the item hazard rate."))
    if not 0.0 <= mode_ratio <= 1.0:
        raise OutOfRangeError(("calculate_mode_hazard_rate() was passed a "
                               "failure mode ratio outside the range of "
                               "[0.0, 1.0]."))

    return item_hr * mode_ratio


def calculate_mode_criticality(mode_hr, mode_op_time, eff_prob):
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
    if mode_op_time < 0.0:
        raise OutOfRangeError(("calculate_mode_criticality() was passed a "
                               "negative value for failure mode operating "
                               "time."))
    if not 0.0 <= eff_prob <= 1.0:
        raise OutOfRangeError(("calculate_mode_criticality() was passed a "
                               "failure effect probability outside the range "
                               "of [0.0, 1.0]."))

    return mode_hr * mode_op_time * eff_prob
