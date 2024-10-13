# -*- coding: utf-8 -*-
#
#       ramstk.analyses.stress.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Component Stress Calculations Module."""


def calculate_stress_ratio(stress_operating, stress_rated):
    """Calculate the operating electrical stress ratio of a device.

    Inputs can be floats, integers, or a combination.

    >>> calculate_stress_ratio(0.382, 1.29)
    0.2961240310077519
    >>> calculate_stress_ratio(1, 2)
    0.5
    >>> calculate_stress_ratio(0.382, 2)
    0.191
    >>> calculate_stress_ratio(1, 1.29)
    0.7751937984496123

    :param stress_operating: the device's operating level of the stress.
    :param stress_rated: the devices's rated stress.
    :return: the ratio of operating stress to rated stress.
    :rtype: float
    :raise: TypeError if an input value is non-numerical.
    :raise: ZeroDivisionError if the rated stress is zero.
    """
    if not isinstance(stress_operating, (int, float)) or not isinstance(
        stress_rated, (int, float)
    ):
        raise TypeError("Inputs must be numerical (int or float).")

    if stress_operating < 0 or stress_rated < 0:
        raise ValueError("Stress values must be non-negative.")

    if stress_rated == 0:
        raise ZeroDivisionError("Rated stress must not be zero.")

    return stress_operating / stress_rated
